# policy-analysis

## Dictionary creation
Use `scripts/build_dictionary.py` to build a clean token dictionary from PDF or text files.

Example:
```bash
python scripts/build_dictionary.py INPUT_PATH output.txt --language dutch --stem
```

## Topic discovery
Use `scripts/discover_topics.py` to automatically group documents into topics using LDA.

Example:
```bash
python scripts/discover_topics.py INPUT_PATH --topics 5 --topn 15
```
