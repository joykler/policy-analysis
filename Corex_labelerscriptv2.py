import os
import re
import json
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

# USER SETTINGS
with open("corex_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

USE_FOLDER = config["USE_FOLDER"]
SOURCE_FOLDER_PATH = config["SOURCE_FOLDER_PATH"]
OUTPUT_FOLDER = config["OUTPUT_FOLDER"]
MODEL_FOLDER = config["MODEL_FOLDER"]
FOLDER_MODE = config["FOLDER_MODE"]  # Default to False if not specified
YEAR_FILTER = tuple(config["YEAR_FILTER"])
DOC_TYPES = config["DOC_TYPES"]
TOKENS_PER_CHUNK = config["SENTS_PER_CHUNK"]  # Now: tokens per chunk!
CONFIDENCE_THRESHOLD = config["CONFIDENCE_THRESHOLD"]
MIN_COSINE = config["MIN_COSINE"]

def simple_tokenizer(text):
    return text.split()

def find_txt_files_by_folder(base_folder, year_filter=None, doc_types=None, simple_mode=False):
    matches = []
    if simple_mode:
        for fname in os.listdir(base_folder):
            if fname.lower().endswith('.txt'):
                matches.append(os.path.join(base_folder, fname))
        return matches
    for root, _, files in os.walk(base_folder):
        path_parts = os.path.normpath(root).split(os.sep)
        if len(path_parts) < 3:
            continue
        document_type = path_parts[-3]
        year = path_parts[-2]
        year_ok = True
        type_ok = True
        if year_filter and year_filter[0] is not None:
            year_ok = year.isdigit() and (str(year_filter[0]) <= year <= str(year_filter[1]))
        if doc_types:
            type_ok = document_type.lower() in [dt.lower() for dt in doc_types]
        if not (year_ok and type_ok):
            continue
        for fname in files:
            if fname.lower().endswith('.txt'):
                matches.append(os.path.join(root, fname))
    return matches

def confirm_and_print_settings(files=None):
    print("\n========= FILTER SETTINGS =========")
    print(f"Source folder:      {SOURCE_FOLDER_PATH}")
    print(f"Output folder:      {OUTPUT_FOLDER}")
    print(f"Year filter:        {YEAR_FILTER}")
    print(f"Doc type filter:    {DOC_TYPES}")
    print(f"Tokens per chunk:   {TOKENS_PER_CHUNK}")
    print(f"Min confidence:     {CONFIDENCE_THRESHOLD}")
    print(f"Min cosine:         {MIN_COSINE}")
    print(f"Model folder:       {MODEL_FOLDER}")
    print("------------------------------------")
    if files is not None:
        print(f"Found {len(files)} .txt files to process after filtering.")
        preview = files[:10] if len(files) > 10 else files
        print("First files to process:")
        for f in preview:
            print(f"  - {f}")
        if len(files) > 10:
            print("  ...")
    print()

def load_topic_data(model_folder):
    with open(os.path.join(model_folder, "lda_topicdata.json"), "r", encoding="utf-8") as f:
        topic_data = json.load(f)
    return topic_data["topic_names"], topic_data["topic_word_lists"]

def load_topic_word_scores(model_folder):
    with open(os.path.join(model_folder, "corex_topicdata_ranked.json"), "r", encoding="utf-8") as f:
        topic_data = json.load(f)
    return topic_data["topic_word_scores"]

def process_file_chunk(
    file_path,
    model_folder,
    tokens_per_chunk,
    confidence_threshold,
    min_cosine,
    topic_names,
    topic_word_lists,
    topic_word_scores,
):
    try:
        import spacy
        from nltk.corpus import stopwords
        from nltk.stem.snowball import SnowballStemmer

        with open(os.path.join(model_folder, "corex_model.pkl"), "rb") as f:
            corex_model = pickle.load(f)
        with open(os.path.join(model_folder, "corex_vectorizer.pkl"), "rb") as f:
            vectorizer = pickle.load(f)
        with open(os.path.join(model_folder, "lda_stopwords.json"), "r", encoding="utf-8") as f:
            custom_stopwords = set(json.load(f))

        nlp = spacy.load("nl_core_news_sm")
        stemmer = SnowballStemmer('dutch')
        stop_words = custom_stopwords

        def clean_and_tokenize(text):
            text = re.sub(r'[^A-Za-zÀ-ÿ0-9 ]', ' ', text.lower())
            tokens = [stemmer.stem(w) for w in text.split() if w not in stop_words and len(w) > 2]
            return tokens

        def split_tokens(text):
            """Split the text into tokens using spacy, return as list."""
            doc = nlp(str(text))
            return [t.text for t in doc if not t.is_space]

        def chunk_by_tokens(token_list, tokens_per_chunk=tokens_per_chunk):
            """Chunk token list into strings of N tokens."""
            return [
                " ".join(token_list[i:i+tokens_per_chunk]).strip()
                for i in range(0, len(token_list), tokens_per_chunk)
                if token_list[i:i+tokens_per_chunk]
            ]

        def compute_cosine_with_anchors(chunk, topic_word_lists, vectorizer):
            chunk_vec = vectorizer.transform([" ".join(clean_and_tokenize(chunk))])
            max_cos = 0
            for anchor_list in topic_word_lists:
                anchor_vec = vectorizer.transform([" ".join(anchor_list)])
                cos = (chunk_vec @ anchor_vec.T).A[0, 0]
                norm = np.linalg.norm(chunk_vec.data) * np.linalg.norm(anchor_vec.data)
                cos = cos / norm if norm != 0 else 0
                if cos > max_cos:
                    max_cos = cos
            return max_cos

        def compute_cosine_with_anchors_weighted(chunk, topic_word_scores, vectorizer, clean_and_tokenize=None):
            vocab = vectorizer.get_feature_names_out()
            if clean_and_tokenize is not None:
                tokens = clean_and_tokenize(chunk)
            elif isinstance(chunk, str):
                tokens = chunk.split()
            else:
                tokens = chunk
            chunk_vec = np.zeros(len(vocab))
            for word in tokens:
                if word in vocab:
                    idx = np.where(vocab == word)[0][0]
                    chunk_vec[idx] += 1
            max_cos = 0
            for topic_scores in topic_word_scores:
                anchor_vec = np.zeros(len(vocab))
                for word, score in topic_scores.items():
                    if word in vocab:
                        idx = np.where(vocab == word)[0][0]
                        anchor_vec[idx] = score
                norm_chunk = np.linalg.norm(chunk_vec)
                norm_anchor = np.linalg.norm(anchor_vec)
                if norm_chunk != 0 and norm_anchor != 0:
                    cos = np.dot(chunk_vec, anchor_vec) / (norm_chunk * norm_anchor)
                else:
                    cos = 0
                if cos > max_cos:
                    max_cos = cos
            return max_cos

        def assign_topic_corex(chunk):
            tokens = clean_and_tokenize(chunk)
            if not tokens:
                return None, 0.0
            sent_str = " ".join(tokens)
            X = vectorizer.transform([sent_str])
            topic_probs = corex_model.transform(X)[0]
            best_topic = int(np.argmax(topic_probs))
            confidence = float(topic_probs[best_topic])
            if confidence > confidence_threshold:
                return best_topic, confidence
            else:
                return None, confidence

        path_parts = os.path.normpath(file_path).split(os.sep)
        try:
            document_type = path_parts[-3]
            year = path_parts[-2]
        except IndexError:
            document_type = None
            year = None
        fname = os.path.basename(file_path)
        out_list = []
        with open(file_path, encoding='utf-8') as f:
            text = f.read()
        # CHANGED: tokenizing and chunking by tokens
        tokens = split_tokens(text)
        chunks = chunk_by_tokens(tokens)
        for i, chunk in enumerate(chunks):
            tokens = clean_and_tokenize(chunk)
            if not tokens:
                topic_idx = None
                confidence = 0.0
                topic_probs = [0.0] * len(topic_names)
            else:
                sent_str = " ".join(tokens)
                X = vectorizer.transform([sent_str])
                topic_probs = corex_model.transform(X)[0]
                topic_idx = int(np.argmax(topic_probs))
                confidence = float(topic_probs[topic_idx])
            cosine = compute_cosine_with_anchors(chunk, topic_word_lists, vectorizer)
            cosine_weighted = compute_cosine_with_anchors_weighted(chunk, topic_word_scores, vectorizer, clean_and_tokenize)
            out_list.append({
                'filename': fname,
                'filepath': file_path,
                'document_type': document_type,
                'year': year,
                'chunk_num': i,
                'chunk_text': chunk,
                'topic': topic_names[topic_idx] if topic_idx is not None else None,
                'confidence': confidence,
                'cosine': cosine,
                'cosine_weighted': cosine_weighted,
                'topic_probs': list(topic_probs) if hasattr(topic_probs, "__iter__") else [0.0] * len(topic_names) # Save full topic_probs vector as a list
            })
        return out_list
    except Exception as e:
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    topic_names, topic_word_lists = load_topic_data(MODEL_FOLDER)
    topic_word_scores = load_topic_word_scores(MODEL_FOLDER)
    if USE_FOLDER:
        files = find_txt_files_by_folder(SOURCE_FOLDER_PATH, year_filter=YEAR_FILTER, doc_types=DOC_TYPES, simple_mode=FOLDER_MODE)
        confirm_and_print_settings(files)
        if len(files) == 0:
            print("No files found that match the filter settings! Exiting.")
            exit()
        confirm = input("Continue? (yes/no): ").strip().lower()
        if not confirm.startswith('y'):
            print("Aborted by user.")
            exit()
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        jobs = [
            (
                f,
                MODEL_FOLDER,
                TOKENS_PER_CHUNK,
                CONFIDENCE_THRESHOLD,
                MIN_COSINE,
                topic_names,
                topic_word_lists,
                topic_word_scores
            )
            for f in files
        ]
        total_files = len(jobs)
        completed = 0
        results = []
        start = time.time()
        print(f"Processing {total_files} files...")
        with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = [executor.submit(process_file_chunk, *job) for job in jobs]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.extend(result)
                completed += 1
                if completed % 100 == 0 or completed == total_files:
                    elapsed = time.time() - start
                    sec_per_file = elapsed / completed
                    print(f"Processed {completed}/{total_files} files "
                          f"in {elapsed/60:.1f} min "
                          f"({sec_per_file:.2f} sec/file, est. total {(sec_per_file*total_files)/60:.1f} min)",
                          flush=True)
        if not results:
            print("No results found after processing.")
            exit()
        train_source = pd.DataFrame(results)
        out_path = os.path.join(OUTPUT_FOLDER, 'chunk_topic_corex_assignments.csv')
        train_source.to_csv(out_path, index=False, encoding='utf-8')
        print(f"\nResults saved to {out_path}")
        print(train_source.head(20))
    else:
        print("Excel mode not implemented.")
