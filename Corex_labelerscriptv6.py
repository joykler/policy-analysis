import os
import re
import json
import pickle
import numpy as np
import pandas as pd
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import langid

print("=== RUNNING THE COSINE-WEIGHTED COREX TOPIC ASSIGNMENT SCRIPT ===")

# =========================
# CONFIGURATION
# =========================
with open("corex_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

USE_FOLDER        = config.get("USE_FOLDER", True)
SOURCE_FOLDER     = config.get("SOURCE_FOLDER_PATH", "./data")
OUTPUT_FOLDER     = config.get("OUTPUT_FOLDER", "./out")
MODEL_FOLDER      = config.get("MODEL_FOLDER", "./model")
FOLDER_MODE       = config.get("FOLDER_MODE", False)  # simple listing of .txt in base folder
YEAR_FILTER       = tuple(config.get("YEAR_FILTER", (None, None)))  # (start, end) inclusive or (None, None)
DOC_TYPES         = config.get("DOC_TYPES", [])  # [] = no filter
TOKENS_PER_CHUNK  = config.get("TOKENS_PER_CHUNK", config.get("SENTS_PER_CHUNK", 250))
MIN_COSINE        = float(config.get("MIN_COSINE", 0.15))
STEM              = bool(config.get("STEM", True))  # allow turning off stemming if desired

# =========================
# PATH PARSING (robust year & doctype extraction)
# =========================
YEAR_RE = re.compile(r"^(19|20)\d{2}$")

def extract_year_and_doctype(file_path, base_folder=None, doc_types=None):
    """
    Returns (year:str|None, doctype:str|None) based on path segments.
    - Finds the first segment that looks like a year (19xx/20xx).
    - Picks the closest non-year alpha segment as document_type.
    - If doc_types is provided, prefers an exact case-insensitive match.
    Works both on absolute and relative paths.
    """
    parts = os.path.normpath(file_path).split(os.sep)
    if base_folder:
        try:
            rel = os.path.relpath(file_path, base_folder)
            parts = os.path.normpath(rel).split(os.sep)
        except Exception:
            pass

    # Locate year
    year_idx = None
    for i, p in enumerate(parts):
        if YEAR_RE.match(str(p)):
            year_idx = i
            break
    year = parts[year_idx] if year_idx is not None else None

    # Candidate doctype segments = any non-year parts
    candidates = [(i, p) for i, p in enumerate(parts) if i != year_idx]

    # Prefer whitelist match if provided
    doc = None
    if doc_types:
        wanted = {dt.lower(): dt for dt in doc_types}
        for i, p in candidates:
            key = str(p).lower()
            if key in wanted:
                doc = wanted[key]
                break

    # Otherwise: choose the closest neighbor to year, else last alpha-like segment
    def alpha_like(s): return any(c.isalpha() for c in str(s))
    if doc is None and candidates:
        if year_idx is not None:
            for _, p in sorted(candidates, key=lambda ip: abs(ip[0] - year_idx)):
                if alpha_like(p):
                    doc = str(p)
                    break
        if doc is None:
            for _, p in reversed(candidates):
                if alpha_like(p):
                    doc = str(p)
                    break

    return (year, doc)

# =========================
# FILE DISCOVERY (uses robust extractor)
# =========================
def find_txt_files_by_folder(base_folder, year_filter=None, doc_types=None, simple_mode=False):
    matches = []
    if simple_mode:
        for fname in os.listdir(base_folder):
            if fname.lower().endswith(".txt"):
                matches.append(os.path.join(base_folder, fname))
        return matches

    for root, _, files in os.walk(base_folder):
        for fname in files:
            if not fname.lower().endswith(".txt"):
                continue
            fpath = os.path.join(root, fname)
            year, doctype = extract_year_and_doctype(fpath, base_folder, doc_types)

            # Year filter (inclusive)
            year_ok = True
            if year_filter and year_filter[0] is not None:
                year_ok = year is not None and (str(year_filter[0]) <= str(year) <= str(year_filter[1]))

            # Doc type filter
            type_ok = True
            if doc_types:
                type_ok = doctype is not None and doctype.lower() in [dt.lower() for dt in doc_types]

            if year_ok and type_ok:
                matches.append(fpath)
    return matches

def confirm_and_print_settings(files=None):
    print("\n========= FILTER SETTINGS =========")
    print(f"Source folder:      {SOURCE_FOLDER}")
    print(f"Output folder:      {OUTPUT_FOLDER}")
    print(f"Year filter:        {YEAR_FILTER}")
    print(f"Doc type filter:    {DOC_TYPES}")
    print(f"Tokens per chunk:   {TOKENS_PER_CHUNK}")
    print(f"Min cosine:         {MIN_COSINE}")
    print(f"Model folder:       {MODEL_FOLDER}")
    print("------------------------------------")
    if files is not None:
        print(f"Found {len(files)} .txt files to process after filtering.")
        preview = files[:10] if len(files) > 10 else files
        print("First files to process:")
        for f in preview:
            y, d = extract_year_and_doctype(f, base_folder=SOURCE_FOLDER, doc_types=DOC_TYPES)
            print(f"  - {f}   ->  year={y} | document_type={d}")
        if len(files) > 10:
            print("  ...")
    print()

# =========================
# TOKENIZATION & HELPERS
# =========================
def simple_tokenizer(text):
    return text.split()

def split_tokens_spacy(text, nlp):
    doc = nlp(str(text))
    return [t.text for t in doc if not t.is_space]

def chunk_tokens(tokens, chunk_size):
    return [tokens[i:i+chunk_size] for i in range(0, len(tokens), chunk_size)]

def keep_sentence(sentence, min_words=4):
    """Keep sentence if short OR not English."""
    words = sentence.strip().split()
    if len(words) < min_words:
        return True
    lang, _ = langid.classify(sentence)
    return lang != 'en'

# =========================
# MODEL LOADING & COSINES
# =========================
def load_topic_data(model_folder):
    with open(os.path.join(model_folder, "lda_topicdata.json"), "r", encoding="utf-8") as f:
        topic_data = json.load(f)
    return topic_data["topic_names"], topic_data["topic_word_lists"]

def load_topic_word_scores(model_folder):
    with open(os.path.join(model_folder, "corex_topicdata_ranked.json"), "r", encoding="utf-8") as f:
        topic_data = json.load(f)
    return topic_data["topic_word_scores"]

def precompute_anchor_vectors(topic_word_scores, vectorizer):
    vocab = vectorizer.get_feature_names_out()
    n_topics = len(topic_word_scores)
    anchor_vecs = np.zeros((n_topics, len(vocab)))
    for t, topic_scores in enumerate(topic_word_scores):
        for word, score in topic_scores.items():
            if word in vectorizer.vocabulary_:
                idx = np.where(vocab == word)[0][0]
                anchor_vecs[t, idx] = score
    anchor_norms = np.linalg.norm(anchor_vecs, axis=1)
    return anchor_vecs, anchor_norms

def compute_cosine_with_anchors(chunk_tokens, topic_word_lists, vectorizer):
    chunk_vec = vectorizer.transform([" ".join(chunk_tokens)])
    max_cos = 0.0
    for anchor_list in topic_word_lists:
        anchor_vec = vectorizer.transform([" ".join(anchor_list)])
        cos = (chunk_vec @ anchor_vec.T).A[0, 0]
        norm = np.linalg.norm(chunk_vec.data) * np.linalg.norm(anchor_vec.data)
        cos = (cos / norm) if norm != 0 else 0.0
        if cos > max_cos:
            max_cos = cos
    return max_cos

def weighted_cosines_for_chunk(tokens, vocab, anchor_vecs, anchor_norms):
    chunk_vec = np.zeros(len(vocab))
    for word in tokens:
        if word in vocab:
            idx = np.where(vocab == word)[0][0]
            chunk_vec[idx] += 1
    chunk_norm = np.linalg.norm(chunk_vec)
    cosines = np.zeros(len(anchor_vecs))
    if chunk_norm == 0:
        return cosines
    dot_products = anchor_vecs @ chunk_vec
    valid = anchor_norms != 0
    cosines[valid] = dot_products[valid] / (anchor_norms[valid] * chunk_norm)
    return cosines

# =========================
# WORKER
# =========================
def process_file_chunk(
    file_path,
    model_folder,
    tokens_per_chunk,
    min_cosine,
    topic_names,
    topic_word_lists,
    topic_word_scores,
    source_folder,
    doc_types,
    stem=True
):
    try:
        import spacy
        from nltk.stem.snowball import SnowballStemmer

        # Load model artifacts per process (safe for ProcessPool)
        with open(os.path.join(model_folder, "corex_model.pkl"), "rb") as f:
            corex_model = pickle.load(f)
        with open(os.path.join(model_folder, "corex_vectorizer.pkl"), "rb") as f:
            vectorizer = pickle.load(f)
        with open(os.path.join(model_folder, "lda_stopwords.json"), "r", encoding="utf-8") as f:
            custom_stopwords = set(json.load(f))

        nlp = spacy.load("nl_core_news_sm")
        stemmer = SnowballStemmer('dutch')
        stop_words = custom_stopwords

        vocab = vectorizer.get_feature_names_out()
        anchor_vecs, anchor_norms = precompute_anchor_vectors(topic_word_scores, vectorizer)

        # Robust year & doctype (same logic as filtering)
        year, document_type = extract_year_and_doctype(
            file_path, base_folder=source_folder, doc_types=doc_types
        )
        fname = os.path.basename(file_path)

        out_list = []
        with open(file_path, encoding='utf-8') as f:
            raw_text = f.read()

        # Split into sentences, keep non-English (and short) -> Dutch-heavy
        sentences = re.split(r'(?<=[.!?])\s+', raw_text)
        filtered_sentences = [s for s in sentences if keep_sentence(s)]
        filtered_text = ' '.join(filtered_sentences)

        # Tokenize with spaCy (keeps Dutch handling)
        tokens = split_tokens_spacy(filtered_text, nlp)

        # Lower, stopwords, length & alpha filter; optional stemming
        if stem:
            tokens = [
                stemmer.stem(w) for w in tokens
                if w.lower() not in stop_words and len(w) > 2 and w.isalpha()
            ]
        else:
            tokens = [
                w.lower() for w in tokens
                if w.lower() not in stop_words and len(w) > 2 and w.isalpha()
            ]

        # Chunk by token count
        chunks = chunk_tokens(tokens, tokens_per_chunk)

        for i, chunk_tokenlist in enumerate(chunks if chunks else [[]]):
            if not chunk_tokenlist:
                out_list.append({
                    'filename': fname,
                    'filepath': file_path,
                    'document_type': document_type,
                    'year': year,
                    'chunk_num': i,
                    'chunk_text': '',
                    'topic': None,
                    'cosine': 0.0,
                    'cosine_weighted': [0.0]*len(topic_names),
                    'topic_probs': [0.0]*len(topic_names),
                    'topic_assigned': [False]*len(topic_names),
                })
                continue

            sent_str = " ".join(chunk_tokenlist)
            X = vectorizer.transform([sent_str])
            topic_probs = list(corex_model.transform(X)[0])
            assigned_topic_mask = [p > 0 for p in topic_probs]

            # Weighted cosines (per topic)
            cosines_full = weighted_cosines_for_chunk(chunk_tokenlist, vocab, anchor_vecs, anchor_norms)
            topic_cosines_weighted = list(cosines_full)

            # Classic cosine: max over anchor lists
            cosine = compute_cosine_with_anchors(chunk_tokenlist, topic_word_lists, vectorizer)

            # Assign topic TRUE only if:
            # (a) Corex says topic present  AND
            # (b) either classic cosine >= threshold OR weighted cosine for that topic >= threshold
            topic_label_mask = []
            for j in range(len(topic_names)):
                label = False
                if assigned_topic_mask[j]:
                    if (cosine >= min_cosine) or (topic_cosines_weighted[j] >= min_cosine):
                        label = True
                topic_label_mask.append(label)

            assigned_topics = [topic_names[t] for t, is_assigned in enumerate(topic_label_mask) if is_assigned]

            out_list.append({
                'filename': fname,
                'filepath': file_path,
                'document_type': document_type,
                'year': year,
                'chunk_num': i,
                'chunk_text': sent_str,
                'topic': '|'.join(assigned_topics) if assigned_topics else None,
                'cosine': float(cosine),
                'cosine_weighted': [float(v) for v in topic_cosines_weighted],
                'topic_probs': [float(v) for v in topic_probs],
                'topic_assigned': topic_label_mask,
            })

        return out_list

    except Exception as e:
        import traceback
        traceback.print_exc()
        return []

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    topic_names, topic_word_lists = load_topic_data(MODEL_FOLDER)
    topic_word_scores = load_topic_word_scores(MODEL_FOLDER)

    if USE_FOLDER:
        files = find_txt_files_by_folder(
            SOURCE_FOLDER,
            year_filter=YEAR_FILTER,
            doc_types=DOC_TYPES,
            simple_mode=FOLDER_MODE
        )
        confirm_and_print_settings(files)

        if len(files) == 0:
            print("No files found that match the filter settings! Exiting.")
            raise SystemExit(0)

        confirm = input("Continue? (yes/no): ").strip().lower()
        if not confirm.startswith('y'):
            print("Aborted by user.")
            raise SystemExit(0)

        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        jobs = [
            (
                f,
                MODEL_FOLDER,
                TOKENS_PER_CHUNK,
                MIN_COSINE,
                topic_names,
                topic_word_lists,
                topic_word_scores,
                SOURCE_FOLDER,
                DOC_TYPES,
                STEM
            )
            for f in files
        ]

        total_files = len(jobs)
        completed = 0
        results = []
        start = time.time()
        print(f"Processing {total_files} files...")

        # Use all CPUs by default
        with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = [executor.submit(process_file_chunk, *job) for job in jobs]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.extend(result)
                completed += 1
                if completed % 100 == 0 or completed == total_files:
                    elapsed = time.time() - start
                    sec_per_file = elapsed / max(completed, 1)
                    print(
                        f"Processed {completed}/{total_files} files "
                        f"in {elapsed/60:.1f} min "
                        f"({sec_per_file:.2f} sec/file, est. total {(sec_per_file*total_files)/60:.1f} min)",
                        flush=True
                    )

        if not results:
            print("No results found after processing.")
            raise SystemExit(0)

        df_out = pd.DataFrame(results)

        out_path = os.path.join(OUTPUT_FOLDER, 'chunk_topics_corex_assignments.csv')
        df_out.to_csv(out_path, index=False, encoding='utf-8')

        print(f"\nResults saved to {out_path}")
        print(df_out.head(20))

    else:
        print("Excel mode not implemented.")
