#!/usr/bin/env python3
"""Convert LDA topics to dictionary files with labels."""

import argparse
import os
from typing import Sequence, Dict, List

from gensim import models

from discover_topics import (
    gather_files,
    build_corpus,
    discover_topics,
    read_extra_stopwords,
    extract_topic_words,
    filter_common_terms,
)



def save_topic_words(topics: Dict[int, List[str]], labels: Sequence[str], output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    for index, label in enumerate(labels):
        out_path = os.path.join(output_dir, f"{label}_dictionary.txt")
        with open(out_path, "w", encoding="utf-8") as fh:
            for word in topics.get(index, []):
                fh.write(f"{word}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export labeled topic dictionaries")
    parser.add_argument("input", help="File or directory with documents")
    parser.add_argument("output", help="Directory where dictionary files are written")
    parser.add_argument("--labels", required=True, help="Comma separated topic labels in order")
    parser.add_argument("--language", default="dutch", help="Language for stopwords")
    parser.add_argument("--extra-stopwords", help="File with additional stop words")
    parser.add_argument("--stem", action="store_true", help="Apply stemming")
    parser.add_argument("--topics", type=int, default=5, help="Number of topics")
    parser.add_argument("--passes", type=int, default=5, help="Training passes for LDA")
    parser.add_argument("--topn", type=int, default=15, help="Words per topic")
    parser.add_argument(
        "--drop-common",
        type=int,
        default=0,
        help="Remove words that appear in more than N topics",
    )
    args = parser.parse_args()

    labels = [label.strip() for label in args.labels.split(',') if label.strip()]

    files = gather_files(args.input)
    from nltk.corpus import stopwords
    from nltk.stem.snowball import SnowballStemmer
    import nltk

    nltk.download("stopwords", quiet=True)
    stop_words = set(stopwords.words(args.language))
    stop_words.update(read_extra_stopwords(args.extra_stopwords))

    stemmer = SnowballStemmer(args.language) if args.stem else None

    corpus, dictionary = build_corpus(files, stop_words, stemmer)
    lda = discover_topics(corpus, dictionary, args.topics, args.passes)

    topics = extract_topic_words(lda, args.topn)
    topics = filter_common_terms(topics, args.drop_common)
    save_topic_words(topics, labels, args.output)


if __name__ == "__main__":
    main()

