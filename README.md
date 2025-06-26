# policy-analysis

This repository contains lightweight tools for dictionary building and topic discovery. Steps below reference numbers like **1.a** so you can follow them sequentially.

## 1. Dictionary creation

1.a **Install requirements**

```bash
pip install -r requirements.txt
```

PDF text extraction relies on **PyMuPDF**, included in the requirements file.

1.b **Run the command line tool**

```bash
python scripts/build_dictionary.py PATH_TO_POLICY_DOCS policy_dictionary.txt --language dutch --stem
```

Provide the directory containing your PDF/TXT files. Use descriptive output names such as `theory_dictionary_2023.txt` so the source remains clear.

1.c **Use the notebook**

Open `Build_Dictionary.ipynb` and configure variables for each source:

```python
policy_documents_path = 'Policy-documents'
policy_dictionary_output = 'policy_dictionary.txt'

theory_documents_path = 'sources'
theory_dictionary_output = 'theory_dictionary.txt'
```

Run the numbered cells (2.a, 2.b, ...) to generate each dictionary.

1.d **Generate stopword list**

Run `Clean_words.ipynb` after installing the requirements. Cell **1.a** writes a combined list of Dutch, English and policy-specific stop words to `stopwords_extra.txt`. Other notebooks read this file when cleaning text.

## 2. Topic discovery

2.a **Prepare documents** – place PDFs or text files in clearly named folders (e.g. `policydocument_2015.pdf`, `theorydocument_slavery.pdf`).

2.b **Run via command line**

```bash
python scripts/discover_topics.py PATH_TO_DOCS --topics 5 --topn 10
```

2.c **Filter dominating terms** – add `--drop-common 10` to remove words shared across more than ten topics.

```bash
python scripts/discover_topics.py PATH_TO_DOCS --topics 5 --topn 10 --drop-common 10
```

2.d **Use the notebook**

Open `Discover_Topics.ipynb` and set parameters:

```python
policydocument_path = 'Policy-documents'
slaverydocument_path = 'sources'
num_topics = 5
```

Execute the cells (2.a–2.d) to train the LDA model and print topics.

## 3. Modular design

Scripts and notebooks accept arbitrary source paths so you can mix policy, theory or slavery documents. Adopt clear variable names like `policy_vocab`, `theory_vocab` or `slaverydocument_path` to keep outputs organized by origin.

## 4. Create topic dictionaries

4.a **Run the helper script** – after training an LDA model, convert the topics to dictionary files using `scripts/topic_dictionary.py`.

```bash
python scripts/topic_dictionary.py PATH_TO_DOCS topic_output_dir \
    --labels policy_2015,policy_2016,policy_2017 --topics 5 --topn 15
```

Each label corresponds to a topic index (0, 1, ...). The script writes
`<label>_dictionary.txt` files containing the top words for that topic. Use
descriptive labels such as `slavery_2023` or `theory_reform` so the source
remains clear.

4.b **Refine manually** – open the generated dictionary files and remove
overlapping or irrelevant terms. You can rerun the script with new labels to
produce additional versions.
4.c **Filter dominating terms** – when discovering topics (see step 2.c), add `--drop-common 10` to drop words that appear in many topics before exporting dictionaries.


## 5. Alternative topic modelling methods

5.a **Hierarchical LDA (hLDA)** – explore deeper topic structures by nesting
topics. Gensim implements `models.hdpmodel.HdpModel` which can serve as a
starting point for hLDA.

5.b **Non-negative Matrix Factorization (NMF)** – NMF is another technique that
uses matrix factorisation rather than probabilistic modelling. It often yields
different topics from LDA. Scikit-learn provides a straightforward
implementation.

5.c **BERTopic** – this method leverages transformers to embed sentences before
clustering them into topics. The `bertopic` package can be installed
separately and integrated with the existing corpus-building utilities.

These approaches can all reuse the same `gather_files` and `build_corpus`
functions so you can mix policy, theory or slavery documents while keeping
variables like `policydocument_path` or `theory_vocab` explicit.
