#!/usr/bin/env python3
"""Automatically discover topics in text or PDF files using LDA."""

import argparse
import os
import re
from typing import Iterable, List, Sequence

import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import wordpunct_tokenize
import fitz  # PyMuPDF

from gensim import corpora, models


def extract_text_from_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        parts = []
        with fitz.open(path) as doc:
            for page in doc:
                parts.append(page.get_text())
        return "\n".join(parts)
    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        return fh.read()


def clean_text(text: str) -> str:
    lines: List[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or re.fullmatch(r"page?\s*\d+", line.lower()):
            continue
        lines.append(line)
    return " ".join(lines)


def tokenize(text: str, stop_words: Sequence[str], stemmer: SnowballStemmer | None) -> List[str]:
    tokens = []
    for tok in wordpunct_tokenize(text.lower()):
        if tok.isalpha() and tok not in stop_words:
            if stemmer:
                tok = stemmer.stem(tok)
            tokens.append(tok)
    return tokens


def gather_files(input_path: str) -> List[str]:
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


def build_corpus(files: Iterable[str], stop_words: Sequence[str], stemmer: SnowballStemmer | None) -> tuple[list[list[str]], corpora.Dictionary]:
    texts: list[list[str]] = []
    for path in files:
        raw = extract_text_from_file(path)
        cleaned = clean_text(raw)
        tokens = tokenize(cleaned, stop_words, stemmer)
        if tokens:
            texts.append(tokens)
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(toks) for toks in texts]
    return corpus, dictionary


def discover_topics(corpus, dictionary, num_topics: int, passes: int = 5) -> models.LdaModel:
    lda = models.LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary, passes=passes)
    return lda


def main() -> None:
    parser = argparse.ArgumentParser(description="Discover topics using LDA")
    parser.add_argument("input", help="File or directory with documents")
    parser.add_argument("--language", default="dutch", help="Language for stopwords (default: dutch)")
    parser.add_argument("--extra-stopwords", help="File with additional stop words")
    parser.add_argument("--stem", action="store_true", help="Apply stemming")
    parser.add_argument("--topics", type=int, default=10, help="Number of topics")
    parser.add_argument("--passes", type=int, default=5, help="Training passes for LDA")
    parser.add_argument("--topn", type=int, default=10, help="Words per topic to display")
    args = parser.parse_args()

    nltk.download("stopwords", quiet=True)
    stop_words = set(stopwords.words(args.language))
    stop_words.update(read_extra_stopwords(args.extra_stopwords))

    stemmer = SnowballStemmer(args.language) if args.stem else None

    files = gather_files(args.input)
    corpus, dictionary = build_corpus(files, stop_words, stemmer)

    lda = discover_topics(corpus, dictionary, args.topics, args.passes)

    for i, topic in lda.show_topics(num_topics=args.topics, num_words=args.topn, formatted=False):
        words = ", ".join(w for w, _ in topic)
        print(f"Topic {i}: {words}")


if __name__ == "__main__":
    main()
