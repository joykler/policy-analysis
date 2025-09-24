# Policy Analysis Workspace

This repository documents how I explore Dutch Caribbean policy documents (2010-2025) to trace the history and afterlives of slavery. The README is written for collaborators, supervisors, and teachers who want to understand my workflow, modular design choices, and the pain points where I still need support.

## 1. Research Purpose & Project Goals
1.a **Overall study focus** – Analyse how Dutch government policy texts discuss slavery, colonialism, racism, and remembrance, and compare those narratives with slavery-specific scholarship to detect silences or emphases.
1.b **Policy model objective** – Train a policy-domain detector that recognises overlapping domains inside lengthy documents by tagging chunks with labels such as `policy_economy` or `policy_education` while keeping filenames like `policy_topic_predictions.csv` clear about their origin.
1.c **Slavery model objective** – Build a slavery-focused classifier capable of spotting direct mentions and indirect contextual references, saving outputs like `slavery_topic_predictions.csv` or `slavery_context_labels.parquet` for transparent provenance.
1.d **Expected outputs** – Deliver reusable topic models, yearly corpora diagnostics, and labelled datasets that enable cross-source comparisons and diagrams illustrating dominant themes and their relationships.

## 2. Workflow Overview
2.a **Inputs** – Maintain `inputs/training-docs/policy/` and `inputs/training-docs/slavery/` as the canonical corpora; when cloning new sources, adopt names such as `policy_2023_publicaties` or `slavery_archive_books` to preserve provenance.
2.b **Dictionaries** – Curate policy and slavery dictionaries using notebooks like `Build_Dictionary.ipynb`; add versions like `policy_dictionairy_2015.xlsx` or `slavery_dictionairy_updates.xlsx` to reflect corpus-specific iterations.
2.c **Labeling** – Use regex routines and Corex topic models to check dictionary coverage per year; the matched segments become training data for BERTje models stored as `policy_regex_matched_results_2015.csv` or `slavery_corex_topics_2023.json`.
2.d **Training** – Fine-tune two BERTje pipelines: a policy classifier trained on regex-labelled policy chunks and a slavery classifier pre-trained on slavery scholarship before being adapted to policy documents.
2.e **Analysis & visualisation** – Produce topic counts per document, yearly comparisons, and co-occurrence diagrams to show where slavery-related language appears within policy domains.

## 3. Workspace Orientation
3.a **Notebook collection** – Central notebooks include `Build_Dictionary.ipynb`, `Clean_words.ipynb`, `Discover_Topics.ipynb`, `regex-precoding#2.ipynb`, and `topic modelling-application.ipynb`. Keep variables like `policydocument_pages`, `slaverydocument_pages`, or `policy_2015_dictionary_path` explicit when editing cells.
3.b **Command-line scripts** – Scripts in `scripts/` replicate notebook logic for reproducibility (`build_dictionary.py`, `discover_topics.py`, `topic_dictionary.py`). Pass arguments such as `--input policydocument_path` or `--dictionary slavery_dictionairy_path` to emphasise corpus context.
3.c **Model artefacts** – Store pickled artefacts (`Policy-label2topic.pickle`, `Policy-topic2label.pickle`, `slavery-label2topic.pickle`, `slavery-topic2label.pickle`, `label_encoder.pkl`) at the repository root so both Corex and BERTje steps can access them.
3.d **Extended stopwords** – `stopwords_extra.txt` expands default stop lists with policy- and slavery-specific vocabulary; add new files like `policy_stopwords_2023.txt` if a corpus requires special filtering.

## 4. Discover Topics Workflow
4.a **Notebook-driven exploration** – `Discover_Topics.ipynb` handles loading, preprocessing, and model fitting. Configure variables such as `policydocument_path`, `slaverydocument_path`, and `num_topics` to keep experiments source-aware.
4.b **Command-line runs** – Run `python scripts/discover_topics.py policydocument_path --topics 10 --topn 15` (or the slavery equivalent) to mirror notebook steps in batch jobs.
4.c **Corex integration** – Combine LDA and Corex by naming outputs `policy_corex_topics.pkl` or `slavery_corex_topics.pkl`, helping me compare interpretability across corpora.
4.d **Topic outputs** – Save per-document summaries as `policy_topic_counts.csv`, `slavery_topic_counts.csv`, or `topic_counts_per_document.csv` when merging results for cross-corpus dashboards.

## 5. Corex & BERTje Training (corexlabelerscriptv6)
5.a **Corex labeler cells** – Within `Discover_Topics.ipynb`, generate Corex-based label suggestions and export them as `policy_corexlabeler_labels.json` or `slavery_corexlabeler_labels.json` for manual review.
5.b **BERTje predictions** – After fine-tuning, write predictions to `bertje_policy_predictions.csv`, `bertje_slavery_predictions.csv`, or dated versions like `policy_bertje_predictions_2023.csv` to record the training slice.
5.c **Topic label mappings** – Keep dictionaries synchronised by updating files such as `policy_label2topic_2015.pkl` or `slavery_topic2label_2023.pkl` whenever label schemes evolve.

## 6. Regex Precoding Pipeline
6.a **Notebook workflow** – `regex-precoding#2.ipynb` guides the creation and evaluation of regex patterns. Define dictionaries like `policy_regex_patterns` or `slavery_regex_patterns` so collaborators can inject new expressions per corpus.
6.b **Primary exports** – Archive match reports as `policy-regex-matched_results.csv`, `slavery-regex-matched_results.csv`, or year-specific files (`policy_regex_matched_results_2015.csv`) to trace when a pattern set was evaluated.
6.c **Filtered matches** – Use folders such as `Policy_regex_filtered_matched` to store cleaned sentence-level matches. When extending to slavery, create parallels like `Slavery_regex_filtered_matched` with consistent column names.
6.d **Sentence-level excerpts** – Generate context files (`policy-regex-matched_sentences.csv`, `slavery-regex-matched_sentences.csv`) to assist manual validation or teaching demonstrations on ambiguous matches.

## 7. Topic Modelling Application
7.a **Application notebook** – `topic modelling-application.ipynb` stitches together dictionary outputs, regex matches, and topic models for end-to-end evaluation. Toggle inputs like `policydictionary_path` or `slaverydictionary_path` to reuse it across sources.
7.b **Visual reporting** – `Visualisatie.ipynb` builds comparative charts. Save images with descriptive names such as `policy_2015_topic_share.png` or `slavery_2023_cooccurrence.png` for lectures or feedback sessions.
7.c **Aggregate tables** – Maintain `topic_counts_per_document.csv` and variants like `topic_counts_per_document (3).csv`, adding a `source_corpus` column when merging policy and slavery outputs for cross-tabulation.

## 8. Dictionaries & Vocabulary Assets
8.a **Primary dictionaries** – `Policy_dictionairy.xlsx` and `Slavery_dictionairy.xlsx` capture curated vocabularies. Clone them into `policy_dictionary_2015.xlsx` or `slavery_dictionary_research.xlsx` when testing new hypotheses without overwriting baselines.
8.b **Topic dictionary workbooks** – `inputs/topic_dictionary/` holds consolidated dictionaries (`policy.xlsx`, `Policy2.xlsx`, `slavery.xlsx`). Use sheet names that include corpus and iteration numbers so reviewers see which experiment produced them.
8.c **Stopword extensions** – Expand `stopwords_extra.txt` with companion files like `policy_stopwords_additions.txt` or `slavery_stopwords_additions.txt` before running dictionary updates.
8.d **Dictionary-building notebook** – `Build_Dictionary.ipynb` remains the canonical pipeline; set variables such as `policydocument_folder` and `slaverydictionary_output` to keep outputs traceable.

## 9. Source Text Collections
9.a **Policy archive text (policyarchive_text)** – Located in `inputs/training-docs/policy/`, subdivided by year (`all-from-2015`, `all-from-2023`) and document type (`beleidsnotas`, `kamerstukken`, `rapporten`, `publicaties`, `jaarverslagen`). Each folder stores `.raw.txt` files extracted from PDF pages, preserving metadata for chronological comparisons.
9.b **Slavery text (slavery_text)** – Stored in `inputs/training-docs/slavery/`, where each book or report includes PDFs and split raw text pages (`0001.raw.txt`, etc.). Variables like `slaverydocument_pages` or `slavery_pdf_path` help me track provenance when scripting ingestion routines.
9.c **Automation scripts** – PowerShell helpers (`#0-Copy-PolicyDocsFromArchiveRepo.ps1`, `#1-Export-RawTextPagesFromPdfFiles.ps1`, `#2-Remove-IntroPagesFromRawTextDirs.ps1`) streamline ingestion; adapt parameters such as `-PolicyArchiveRoot` or `-SlaveryArchiveRoot` for new corpora.

## 10. Collaboration Notes & Current Challenges
10.a **Documentation priority** – I am still aligning notebook naming conventions and variable scopes so that each pipeline remains modular; contributions that improve parameter handling or add source-aware wrappers are welcome.
10.b **Data quality hurdles** – Some policy PDFs have inconsistent metadata, which complicates year-based comparisons. Any automated scripts that verify filenames like `policy_2012_kamerstukken.raw.txt` would reduce manual checking.
10.c **Model evaluation gaps** – I need clearer validation dashboards comparing policy and slavery predictions over time. Suggestions on structuring evaluation notebooks (e.g., `policy_vs_slavery_evaluation.ipynb`) would help me explain results to teachers.

---

### Testing
⚠️ Not run (documentation-only change).
