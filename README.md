# policy-analysis

## Dictionary creation
You can build token dictionaries either via the command line or with the new
Jupyter notebook.

1.a **Script usage** – generate a dictionary from PDF or text sources:
```bash
python scripts/build_dictionary.py INPUT_PATH output.txt --language dutch --stem
```

1.b **Notebook usage** – open `Build_Dictionary.ipynb` and follow the numbered
cells to set your document paths (`policy_documents_path` or
`theory_documents_path`) and create outputs such as `policy_dictionary.txt`.

## Topic discovery
LDA topic modelling can likewise be run from a script or interactively.

2.a **Script usage**:
```bash
python scripts/discover_topics.py INPUT_PATH --topics 5 --topn 15
```

2.b **Notebook usage** – open `Discover_Topics.ipynb`, adjust variables like
`policydocument_path` and run the cells to train the model and view the topics.