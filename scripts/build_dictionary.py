#!/usr/bin/env python3
"""Create a cleaned dictionary from text or PDF sources.

This utility collects text files or PDF documents, performs basic cleaning
(footer/header removal, tokenization, normalization), filters stop words and
optionally stems tokens. It outputs a sorted list of unique tokens or, if
requested, a frequency list which can serve as a seed dictionary for
subsequent topic modelling work.
"""

import argparse
import os
import re
from collections import Counter
from typing import Iterable, List, Sequence

import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import wordpunct_tokenize
import fitz  # PyMuPDF


# ---------------------------------------------------------------------------
# Text extraction and preprocessing
# ---------------------------------------------------------------------------

def extract_text_from_file(path: str) -> str:
    """Return text extracted from ``path`` which can be a PDF or TXT file."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        text = []
        with fitz.open(path) as doc:
            for page in doc:
                text.append(page.get_text())
        return "\n".join(text)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def clean_text(text: str) -> str:
    """Apply light cleanup heuristics to remove page numbers and blank lines."""
    lines: List[str] = []
    for line in text.splitlines():
        line = line.strip()
        # skip empty lines or lone page numbers like "12" or "page 12"
        if not line or re.fullmatch(r"page?\s*\d+", line.lower()):
            continue
        lines.append(line)
    return " ".join(lines)


def tokenize(text: str, stop_words: Sequence[str], stemmer: SnowballStemmer | None) -> List[str]:
    """Tokenize ``text`` and return a list of filtered tokens."""
    tokens = []
    for tok in wordpunct_tokenize(text.lower()):
        if tok.isalpha() and tok not in stop_words:
            if stemmer:
                tok = stemmer.stem(tok)
            tokens.append(tok)
    return tokens


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def gather_files(input_path: str) -> List[str]:
    """Collect all supported files from ``input_path``."""
    if os.path.isdir(input_path):
        out: List[str] = []
        for root, _, files in os.walk(input_path):
            for name in files:
                if name.lower().endswith((".txt", ".raw.txt", ".pdf")):
                    out.append(os.path.join(root, name))
        return out
    return [input_path]


def read_extra_stopwords(path: str | None) -> List[str]:
    if not path:
        return []
    with open(path, "r", encoding="utf-8") as fh:
        return [w.strip().lower() for w in fh if w.strip()]


def build_vocabulary(files: Iterable[str], stop_words: Sequence[str], stemmer: SnowballStemmer | None) -> Counter:
    """Build token frequency counter from ``files``."""
    vocab: Counter = Counter()
    for path in files:
        raw_text = extract_text_from_file(path)
        cleaned = clean_text(raw_text)
        tokens = tokenize(cleaned, stop_words, stemmer)
        vocab.update(tokens)
    return vocab


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Create vocabulary from text or PDF files")
    parser.add_argument("input", help="File or directory to process")
    parser.add_argument("output", help="Path for the resulting dictionary file")
    parser.add_argument("--language", default="dutch", help="Language for NLTK stopwords (default: dutch)")
    parser.add_argument("--extra-stopwords", help="Optional file with extra stop words, one per line")
    parser.add_argument("--stem", action="store_true", help="Apply Snowball stemming")
    parser.add_argument("--min-frequency", type=int, default=1, help="Only keep tokens appearing at least this many times")
    parser.add_argument("--freq-list", help="If set, also write <word>\t<count> to this file")
    args = parser.parse_args()

    nltk.download("stopwords", quiet=True)
    stop_words = set(stopwords.words(args.language))
    stop_words.update(read_extra_stopwords(args.extra_stopwords))

    stemmer = SnowballStemmer(args.language) if args.stem else None

    files = gather_files(args.input)
    vocab = build_vocabulary(files, stop_words, stemmer)

    # Filter by frequency and sort alphabetically
    words = sorted([w for w, c in vocab.items() if c >= args.min_frequency])

    with open(args.output, "w", encoding="utf-8") as fh:
        for word in words:
            fh.write(f"{word}\n")

    if args.freq_list:
        with open(args.freq_list, "w", encoding="utf-8") as fh:
            for word in words:
                fh.write(f"{word}\t{vocab[word]}\n")


if __name__ == "__main__":
    main()
