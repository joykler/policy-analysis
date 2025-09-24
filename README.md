# Policy Analysis Workspace

## 1. Getting Started
1.a **Create your workspace clone** – Copy the repository and place it inside your preferred development folder so you can edit notebooks such as `Build_Dictionary.ipynb`, `Discover_Topics.ipynb`, and `topic modelling-application.ipynb` without altering raw inputs.

1.b **Install Python dependencies** – Use the root-level `requirements.txt` to ensure local notebooks and scripts share the same environment when you run modular pipelines for policy or slavery sources.

1.c **Review training inputs** – Inspect `inputs/training-docs/` to confirm both the policy archive text and slavery text corpora are available before launching any notebook-driven workflow.

## 2. Directory Orientation
2.a **Notebook collection** – Core analyses live in notebooks such as `Build_Dictionary.ipynb`, `Clean_words.ipynb`, `Discover_Topics.ipynb`, `regex-precoding#2.ipynb`, and `topic modelling-application.ipynb`; keep source-specific variables like `policydocument_path` or `slaverydocument_path` explicit when editing them.

2.b **Command-line scripts** – Automated routines reside in `scripts/build_dictionary.py`, `scripts/discover_topics.py`, and `scripts/topic_dictionary.py`, letting you reproduce notebook logic with clear source arguments (e.g., `--input policydocument_path`).

2.c **Model artefacts** – Store pretrained resources (`Policy-label2topic.pickle`, `Policy-topic2label.pickle`, `slavery-label2topic.pickle`, `slavery-topic2label.pickle`, `label_encoder.pkl`) in the repository root so both Corex and BERTje steps can reuse them per corpus.

2.d **Extended stopwords** – The shared `stopwords_extra.txt` extends language-specific stop lists with policy- and slavery-specific vocabulary; reference it when normalising multiple corpora.

## 3. Discover Topics Workflow
3.a **Notebook-driven exploration** – `Discover_Topics.ipynb` guides you through data loading, preprocessing, and topic modelling; adjust parameters like `policydocument_path`, `slaverydocument_path`, or `num_topics` to keep each run source-aware.

3.b **Command-line runs** – Execute `python scripts/discover_topics.py policydocument_path --topics 10 --topn 15` (or the slavery equivalent) for batch jobs that mirror the notebook's modular cells.

3.c **Corex integration** – Dedicated cells import `corextopic`, fit `Corex` models, and extract topic-word lists, enabling you to compare Corex topics against LDA within the same notebook while naming objects such as `policy_corex_topics` or `slavery_corex_topics` for clarity.

3.d **Topic outputs** – Summaries such as `topic_counts_per_document.csv` capture per-document topic weights; duplicate them with descriptive names (`policy_topic_counts.csv`, `slavery_topic_counts.csv`) when branching analyses.

## 4. Corex & BERTje Training (corexlabelerscriptv6)
4.a **Corex labeler cells** – Reuse the Corex sections in `Discover_Topics.ipynb` to generate label suggestions; persist results with names like `policy_corexlabeler_labels.json` to distinguish policy versus slavery experiments.

4.b **BERTje predictions** – The repository stores `bertje_policy_predictions.csv`, `bertje_slavery_predictions.csv`, and `bertje_topic_predictions.csv` alongside `label_encoder.pkl`; regenerate them after fine-tuning by saving new files such as `policy_bertje_predictions_2023.csv` to keep provenance obvious.

4.c **Topic label mappings** – Synchronise Corex and BERTje outputs with the pickled dictionaries (`Policy-label2topic.pickle`, `slavery-topic2label.pickle`) and name any new variants by source and year (e.g., `policy_label2topic_2015.pkl`).

## 5. Regex Precoding Pipeline
5.a **Notebook workflow** – `regex-precoding#2.ipynb` orchestrates pattern design, application, and evaluation; configure variables such as `policy_regex_patterns` and `slavery_regex_patterns` for modular reuse.

5.b **Primary exports** – CSV outputs (`policy-regex-matched_results.csv`, `slavery-regex-matched_results.csv`, `train-regex-matched_results.csv`) catalogue matches per document; create derivatives with explicit naming like `policy_regex_matched_results_2015.csv` to track versions.

5.c **Filtered matches** – `Policy_regex_filtered_matched` retains topic-labelled policy sentences, showing fields `sentence`, `topic`, `document`, and `label`; replicate the filtering logic for other corpora (e.g., `slavery_regex_filtered_matched.csv`).

5.d **Sentence-level excerpts** – Use `policy-regex-matched_sentences.csv` and `slavery-regex-matched_sentences.csv` to inspect context; maintain corpus-aware filenames when generating new reports (e.g., `slavery_regex_matched_sentences_2023.csv`).

## 6. Topic Modelling Application
6.a **Application notebook** – `topic modelling-application.ipynb` combines dictionary outputs, regex matches, and topic models into end-to-end analyses; toggle inputs such as `policydictionary_path` or `slaverydictionary_path` to reuse it across sources.

6.b **Visual reporting** – `Visualisatie.ipynb` supports plotting topic distributions or regex coverage; label figures with corpus-specific titles (e.g., "Slavery 2023 Topic Share").

6.c **Aggregate tables** – Maintain per-document metrics in `topic_counts_per_document.csv` and its variants (`topic_counts_per_document (3).csv`); extend them with columns like `source_corpus` to simplify cross-source comparisons.

## 7. Dictionaries & Vocabulary Assets
7.a **Primary dictionaries** – `Policy_dictionairy.xlsx` and `Slavery_dictionairy.xlsx` store curated vocabularies; clone them into `policy_dictionary_2015.xlsx` or `slavery_dictionary_research.xlsx` when experimenting with new corpora.

7.b **Topic dictionary workbooks** – `inputs/topic_dictionary/` contains consolidated topic dictionaries (`policy.xlsx`, `Policy2.xlsx`, `slavery.xlsx`); use sheet names and filenames that encode corpus and iteration numbers for clarity.

7.c **Stopword extensions** – Augment `stopwords_extra.txt` with source-specific tokens (e.g., `policystopwords_2023.txt`) before re-running dictionary or topic extraction routines.

7.d **Dictionary-building notebook** – `Build_Dictionary.ipynb` provides the canonical pipeline; assign variables like `policydocument_folder` and `slaverydictionary_output` so outputs remain source-labelled.

## 8. Source Text Collections
8.a **Policy archive text (policyarchive_text)** – The policy corpus resides under `inputs/training-docs/policy/`, subdivided by year (`all-from-2015`, `all-from-2023`) and document type (`beleidsnotas`, `kamerstukken`, `rapporten`, `publicaties`, `jaarverslagen`); each final folder holds `.raw.txt` files extracted from PDF pages, nested by publication date to preserve metadata from the policy archive.

8.b **Slavery text (slavery_text)** – The slavery corpus is stored in `inputs/training-docs/slavery/`, where each book or report has both the original PDF and the split raw text pages (`0001.raw.txt`, etc.); leverage these folders for targeted analyses by naming variables `slaverydocument_pages` or `slavery_pdf_path` when scripting pipelines.

## 9. Auxiliary Resources
9.a **Automation scripts** – PowerShell helpers (`#0-Copy-PolicyDocsFromArchiveRepo.ps1`, `#1-Export-RawTextPagesFromPdfFiles.ps1`, `#2-Remove-IntroPagesFromRawTextDirs.ps1`) streamline document ingestion; adapt them with parameters like `-PolicyArchiveRoot` or `-SlaveryArchiveRoot` to remain source-aware.

9.b **Precomputed analytics** – Files such as `matched_results.csv` and `bertje_topic_predictions.csv` provide ready-made baselines; duplicate them under names like `policy_matched_results_baseline.csv` or `slavery_topic_predictions_experiment1.csv` whenever you run new experiments.

---

### Testing
⚠️ Not run (read-only analysis request).
