# Dictionary Discovery v15 - Cell Structure Reference

## Overview

The v15 notebook has been split into **logical, modular code blocks** for better readability and maintenance. Each cell has a specific purpose in the 4-stage processing pipeline.

**Total Cells**: 85 (21 cells for Checkpoint 1)

---

## Checkpoint 1 Cell Structure

### Cell 10: Markdown Separator
```markdown
---
# CHECKPOINT 1: Text Processing
---
```
- Marks the start of Checkpoint 1

---

### Cell 11: Markdown Header
```markdown
## Consolidated Text Processing Pipeline (Checkpoint 1)

This checkpoint uses a streamlined 4-stage workflow...
```
- Explains the consolidated approach
- Overview of the 4 stages

---

### Cell 12: Imports and Dependencies
**Lines**: 7
**Purpose**: Import the consolidated pipeline module

```python
# Import consolidated pipeline
from pathlib import Path
import pandas as pd
import numpy as np
```

**Loads**: Basic imports needed for execution

---

### Cell 13: Configuration Dataclass (STAGE 1)
**Lines**: 183
**Cell ID**: `config_dataclass_013`
**Purpose**: Configuration management and Stage 1 implementation

**Contains**:
- `ProcessingConfig` dataclass
  - All configuration parameters in one place
  - Loaded from CONFIG dict
  - Support for overrides
- `detect_corpus_mode(corpus_source)` function
  - Auto-detects if source contains PDFs or text files
- `load_configuration(config_dict, overrides)` function
  - **STAGE 1**: Configuration & Source Loading
  - Validates and prints configuration summary

**Key Functions**:
```python
config = load_configuration(
    config_dict=CONFIG,
    cp1_source=None,  # Override source path
    cp1_source_chunks=None,  # Load pre-chunked CSV
    cp1_force_mode=None  # Force 'pdf', 'text', or 'chunked'
)
```

**Prints**: `✓ Configuration dataclass and Stage 1 functions loaded`

---

### Cell 14: Content Filtering Patterns & Functions
**Lines**: 143
**Cell ID**: `content_filtering_014`
**Purpose**: Detect and remove bibliographies, footnotes, and indexes

**Contains**:

**Pattern Definitions**:
- `BIBLIOGRAPHY_HEADERS` (6 patterns, Dutch + English)
- `BIBLIOGRAPHY_PATTERNS` (6 citation patterns)
- `INDEX_PATTERNS` (2 index detection patterns)

**Detection Functions**:
- `detect_bibliography_section(text, threshold=0.3)` → bool
- `detect_index_section(text, threshold=0.4)` → bool

**Filtering Functions**:
- `split_text_before_bibliography(text)` → (main_text, biblio_text)
- `remove_footnote_markers(text, aggressive=False)` → (cleaned_text, num_removed)
- `filter_page_content(page_text, config)` → (filtered_text, stats)

**Patterns Detected**:
- Bibliography headers: bibliografie, bibliography, literatuur, bronnen, references, noten, index, bijlagen
- Footnotes: superscripts, ibid, op. cit., author-year citations, page refs
- Indexes: name-page number lists, dense page numbers

**Prints**: `✓ Content filtering patterns and functions loaded`

---

### Cell 15: PDF Processing Functions
**Lines**: 262
**Cell ID**: `pdf_processing_015`
**Purpose**: Extract and filter PDF pages

**Contains**:

**Dataclasses**:
- `DocumentStats` - Per-document statistics
- `ProcessingStats` - Aggregate statistics

**PDF Functions**:
- `extract_text_from_pdf(pdf_path)` → List[(page_num, text)]
  - Extracts all pages using PyMuPDF
- `filter_pdf_page(page_text, config)` → (keep: bool, reason: str)
  - Applies quality filters (word count, sentences, English ratio, numeric ratio, layout detection, reference sections)
- `detect_headers_footers(pages, threshold=0.6)` → Dict
  - Finds repeated text across pages
- `remove_headers_footers(text, header_footer_data)` → str
  - Removes detected headers/footers
- `save_preprocessed_text(pdf_path, pages, workflow_fs, corpus_source)`
  - Saves filtered pages to `Preprocessed_text/` folder
- `process_pdf_document(pdf_path, config, workflow_fs, corpus_source)` → (text, stats)
  - **Main PDF pipeline**: extract → filter → clean → save

**Filtering Criteria**:
1. Empty pages
2. Word count < threshold (default: 50)
3. Sentence count < threshold (default: 3)
4. English ratio > threshold (default: 0.5)
5. Numeric ratio > threshold (default: 0.3)
6. Layout pages (whitespace/line length)
7. Reference sections (citation density)

**Prints**: `✓ PDF processing functions loaded`

---

### Cell 16: Stage 2 - Document Loading & Filtering
**Lines**: 173
**Cell ID**: `stage2_loading_016`
**Purpose**: Load documents from corpus and apply filtering pipeline

**Contains**:

**Functions**:
- `should_include_document(file_path, corpus_source, config)` → (include: bool, reason: str)
  - Checks year, doc_type, filename pattern filters
- `load_and_filter_documents(config, workflow_fs)` → (documents, stats)
  - **STAGE 2**: Document Loading & Text Filtering
  - Discovers files (PDF or text)
  - Applies document-level filters
  - Processes each document:
    - **PDF mode**: Full filtering pipeline (extract → filter pages → remove headers/footers → filter content)
    - **Text mode**: Direct loading
  - Returns list of document dicts with metadata

**Processing Flow**:
1. Handle pre-chunked mode (return empty)
2. Discover files (PDF or text)
3. Apply corpus filters (year, doc_type, patterns)
4. Process each document:
   - PDF: `process_pdf_document()` → filtered text
   - Text: Load file directly
5. Collect documents with metadata

**Per-Document Output**:
```
[15/26] document_name.pdf
  PDF: 45/50 pages kept (filtered: too_few_words=3, layout_page=2), index pages=5
```

**Prints**: `✓ Stage 2 (Document Loading & Filtering) loaded`

---

### Cell 17: Text Processing Utilities
**Lines**: 74
**Cell ID**: `text_utilities_017`
**Purpose**: Text cleaning and processing utilities

**Contains**:

**NLTK Setup**:
- Downloads stopwords if needed
- Initializes Dutch stemmer

**Constants**:
- `DUTCH_STOPWORDS` - NLTK Dutch stopwords
- `ENGLISH_STOPWORDS` - NLTK English stopwords
- `CUSTOM_STOPWORDS` - Extended Dutch stopwords (bijlage, inleiding, conclusie, etc.)
- `ALL_STOPWORDS` - Combined set
- `DUTCH_STEMMER` - Snowball Dutch stemmer
- `ENGLISH_HINTS` - Common English words (26)
- `DUTCH_HINTS` - Common Dutch words (28)

**Functions**:
- `likely_english_sentence(sentence)` → bool
  - Compares English vs Dutch hint word counts
- `remove_stopwords_and_numbers(text)` → str
  - Removes stopwords and digits
- `stem_text(text)` → str
  - Applies Dutch Snowball stemming
- `short_file_hash(path, n=8)` → str
  - Creates 8-character SHA1 hash
- `make_chunk_uid(file_path, chunk_idx)` → str
  - Format: `{hash}:{chunk_idx:05d}`
- `split_into_sentences(text)` → List[str]
  - Splits on `.!?` followed by whitespace
- `count_tokens(text)` → int
  - Counts tokens (whitespace-separated)

**Prints**: `✓ Text processing utilities loaded`

---

### Cell 18: Stage 3 - Chunking & Processing
**Lines**: 114
**Cell ID**: `stage3_chunking_018`
**Purpose**: Chunk documents and create dual text versions

**Contains**:

**Function**:
- `chunk_and_process_documents(documents, config, pre_chunked_df=None)` → (chunks_df, stats)
  - **STAGE 3**: Chunking & Dual Text Processing

**Processing Flow**:
1. Handle pre-chunked mode (return as-is)
2. For each document:
   - Split into sentences
   - Group into fixed-size chunks (e.g., 10 sentences)
   - Filter by minimum sentences (e.g., ≥2)
   - Create **raw_text** (original sentences)
   - Create **text_for_scoring** (processed):
     - Filter English sentences (optional)
     - Remove stopwords (optional)
     - Apply stemming (optional)
   - Filter by minimum tokens (e.g., ≥300)
   - Generate unique chunk UID
3. Create DataFrame with metadata
4. Return chunks and statistics

**Output Columns**:
- file_path, chunk_uid, raw_text, text_for_scoring
- sentence_count, doc_type, year, document_folder, filename

**Prints**: `✓ Stage 3 (Chunking & Processing) loaded`

---

### Cell 19: Stage 4 - Validation & Statistics
**Lines**: 133
**Cell ID**: `stage4_validation_019`
**Purpose**: Validate output and generate comprehensive statistics

**Contains**:

**Function**:
- `validate_and_save_corpus(chunks_df, output_path, doc_stats, chunk_stats, config)` → final_stats
  - **STAGE 4**: Validation & Statistics Reporting

**Processing Flow**:
1. Validate DataFrame structure (required columns)
2. Save to CSV (`Other_data/chunked_corpus.csv`)
3. Generate comprehensive statistics report:
   - **Document-level**: Total/processed/failed/skipped, filter reasons
   - **PDF page-level**: Extracted/kept/filtered, breakdown by reason with percentages
   - **Content-level**: Index/bibliography/footnotes removed (character counts)
   - **Chunk-level**: Total/filtered, average per document, token counts
   - **Errors**: List of failed documents
4. Return structured stats dictionary

**Statistics Report Format**:
```
================================================================================
PROCESSING STATISTICS REPORT
================================================================================

--------------------------------DOCUMENT-LEVEL STATISTICS--------------------------------
  Total documents found: 26
  Successfully processed: 23
  Failed: 0

---------------------------------PDF PAGE-LEVEL STATISTICS---------------------------------
  Total pages extracted: 1,250
  Pages kept after filtering: 875
  Pages filtered out: 375

  Filter breakdown:
    too_few_words: 145 (11.6%)
    layout_page: 89 (7.1%)
    ...

--------------------------------CONTENT-LEVEL STATISTICS--------------------------------
  Index pages removed: 45
  Bibliography characters removed: 125,430
  Footnote markers removed: 8,234
  Total content filtered: 12.3% of original text

----------------------------------CHUNK-LEVEL STATISTICS----------------------------------
  Total chunks created: 3,456
  Average chunks per document: 150.3
  ...
```

**Prints**: `✓ Stage 4 (Validation & Statistics) loaded`

---

### Cell 20: Main Pipeline Function
**Lines**: 55
**Cell ID**: `main_pipeline_020`
**Purpose**: Orchestrate the complete 4-stage pipeline

**Contains**:

**Function**:
- `run_checkpoint1_pipeline(config_dict, workflow_fs, cp1_source, cp1_source_chunks, cp1_force_mode)` → (chunks_df, final_stats)

**Processing Flow**:
1. **STAGE 1**: Load configuration
2. Handle pre-chunked mode (load CSV, skip to validation)
3. **STAGE 2**: Load and filter documents
4. **STAGE 3**: Chunk and process documents
5. **STAGE 4**: Validate and save corpus
6. Return chunks DataFrame and final statistics

**Usage**:
```python
chunks_df, stats = run_checkpoint1_pipeline(
    CONFIG,
    workflow_fs=fs,
    cp1_source=None,  # Override corpus source
    cp1_source_chunks=None,  # Load pre-chunked CSV
    cp1_force_mode=None  # Force processing mode
)
```

**Prints**: `✓ Main pipeline function (run_checkpoint1_pipeline) loaded`

---

### Cell 21: Execution Cell
**Lines**: 17
**Cell ID**: `execute_pipeline_021`
**Purpose**: Execute the complete pipeline

**Code**:
```python
# Execute the consolidated pipeline
# Customize these parameters as needed:

# Option 1: Default (use CONFIG settings)
chunked_corpus, cp1_stats = run_checkpoint1_pipeline(CONFIG, fs)

# Option 2: Override corpus source
# chunked_corpus, cp1_stats = run_checkpoint1_pipeline(
#     CONFIG, fs,
#     cp1_source="C:/path/to/other/corpus"
# )

# Option 3: Load pre-chunked data
# chunked_corpus, cp1_stats = run_checkpoint1_pipeline(
#     CONFIG, fs,
#     cp1_source_chunks="workflow_data/v10/Other_data/chunked_corpus.csv"
# )

print(f"\n{'='*80}")
print(f"✓ Checkpoint 1 pipeline executed successfully")
print(f"  Output: {len(chunked_corpus)} chunks")
print(f"{'='*80}\n")
```

**Prints**: Pipeline execution confirmation with chunk count

---

## Cell Dependencies

### Execution Order

```
Cell 12: Imports
  ↓
Cell 13: Configuration (Stage 1)
  ↓
Cell 14: Content Filtering Functions
  ↓
Cell 15: PDF Processing Functions
  ↓
Cell 16: Stage 2 (Document Loading)
  ↓
Cell 17: Text Processing Utilities
  ↓
Cell 18: Stage 3 (Chunking)
  ↓
Cell 19: Stage 4 (Validation)
  ↓
Cell 20: Main Pipeline Function
  ↓
Cell 21: Execution
```

### Dependency Graph

```
Cell 13 (Config) ─────────────────────┐
                                      ↓
Cell 14 (Content Filter) ──→ Cell 15 (PDF Processing) ──→ Cell 16 (Stage 2)
                                                                    ↓
Cell 17 (Text Utils) ───────────────────────────────→ Cell 18 (Stage 3)
                                                                    ↓
                                                          Cell 19 (Stage 4)
                                                                    ↓
Cell 13, 16, 18, 19 ───────────────────────────────→ Cell 20 (Main Pipeline)
                                                                    ↓
                                                          Cell 21 (Execution)
```

---

## Function Call Flow

When you run **Cell 21** (Execution), here's what happens:

```
run_checkpoint1_pipeline(CONFIG, fs)
  │
  ├─→ load_configuration(CONFIG, overrides)  [Cell 13 - Stage 1]
  │     └─→ detect_corpus_mode(corpus_source)
  │
  ├─→ load_and_filter_documents(config, fs)  [Cell 16 - Stage 2]
  │     ├─→ should_include_document(file, corpus, config)
  │     └─→ For each document:
  │           └─→ process_pdf_document(pdf_path, config, fs, corpus)  [Cell 15]
  │                 ├─→ extract_text_from_pdf(pdf_path)
  │                 ├─→ filter_pdf_page(page_text, config)  [for each page]
  │                 ├─→ detect_headers_footers(pages)
  │                 ├─→ remove_headers_footers(text, hf_data)
  │                 ├─→ filter_page_content(page_text, config)  [Cell 14]
  │                 │     ├─→ detect_index_section(text)
  │                 │     ├─→ split_text_before_bibliography(text)
  │                 │     │     └─→ detect_bibliography_section(text)
  │                 │     └─→ remove_footnote_markers(text)
  │                 └─→ save_preprocessed_text(...)
  │
  ├─→ chunk_and_process_documents(documents, config)  [Cell 18 - Stage 3]
  │     ├─→ split_into_sentences(text)  [Cell 17]
  │     ├─→ likely_english_sentence(sentence)  [Cell 17]
  │     ├─→ remove_stopwords_and_numbers(text)  [Cell 17]
  │     ├─→ stem_text(text)  [Cell 17, optional]
  │     ├─→ count_tokens(text)  [Cell 17]
  │     └─→ make_chunk_uid(file_path, idx)  [Cell 17]
  │
  └─→ validate_and_save_corpus(chunks_df, ..., stats, config)  [Cell 19 - Stage 4]
        └─→ Returns (chunks_df, final_stats)
```

---

## Configuration Reference

### CONFIG Dictionary Structure

Configuration is centralized in the `CONFIG` dictionary (defined earlier in the notebook) and loaded by `Cell 13`:

```python
CONFIG = {
    'paths': {
        'corpus_dir': 'PDF sources',
        # ...
    },
    'corpus_filter': {
        'enabled': False,
        'years': [2020, 2021],
        'year_range': (2015, 2023),
        'doc_types': ['policy'],
        'filename_patterns': [r'.*slavery.*'],
        'exclude_patterns': [r'.*draft.*'],
    },
    'pdf_processing': {
        'min_word_count': 50,
        'min_sentences_per_page': 3,
        'max_english_ratio': 0.5,
        'max_numeric_ratio': 0.3,
        'detect_layout_pages': True,
        'layout_whitespace_threshold': 0.7,
        'layout_avg_line_length': 30,
        'remove_reference_sections': True,
        'remove_headers_footers': True,
        'save_intermediate_text': True,
    },
    'chunking': {
        'sentences_per_chunk': 10,
        'min_sentences_to_keep': 2,
        'drop_likely_english': True,
        'remove_stopwords': True,
        'use_stemming': False,
    },
}
```

---

## Output Structure

### chunks_df DataFrame

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| file_path | str | Full path to source document | `C:/corpus/policy/2023/doc/file.pdf` |
| chunk_uid | str | Unique chunk ID | `a1b2c3d4:00042` |
| raw_text | str | Original chunk text | `De slavernij was een systeem...` |
| text_for_scoring | str | Processed text (no stopwords) | `slavernij systeem koloniaal...` |
| sentence_count | int | Number of sentences | `10` |
| doc_type | str | Document type from path | `policy` |
| year | str | Year from path | `2023` |
| document_folder | str | Parent folder | `slavery_report` |
| filename | str | Original filename | `Allen_2023.pdf` |

### final_stats Dictionary

```python
{
    'timestamp': '2025-01-25T12:30:45',
    'config': {
        'corpus_source': 'PDF sources',
        'corpus_mode': 'pdf',
        'chunk_sentences_per_chunk': 10,
        'chunk_min_tokens': 300
    },
    'documents': {
        'total': 26,
        'processed': 23,
        'failed': 0,
        'skipped': 3
    },
    'pages': {
        'extracted': 1250,
        'kept': 875,
        'filter_reasons': {
            'too_few_words': 145,
            'layout_page': 89,
            # ...
        }
    },
    'content': {
        'bibliography_chars_removed': 125430,
        'footnote_markers_removed': 8234,
        'index_pages_removed': 45
    },
    'chunks': {
        'total': 3456,
        'filtered': {
            'too_few_sentences': 123,
            'all_english': 45,
            'too_few_tokens': 89
        },
        'avg_per_document': 150.3
    },
    'output_file': 'workflow_data/.../Other_data/chunked_corpus.csv'
}
```

---

## Quick Reference

### Run the Pipeline (Default)
```python
# Cell 21
chunked_corpus, cp1_stats = run_checkpoint1_pipeline(CONFIG, fs)
```

### Run with Custom Source
```python
# Cell 21
chunked_corpus, cp1_stats = run_checkpoint1_pipeline(
    CONFIG, fs,
    cp1_source="C:/path/to/custom/corpus"
)
```

### Load Pre-Chunked Data
```python
# Cell 21
chunked_corpus, cp1_stats = run_checkpoint1_pipeline(
    CONFIG, fs,
    cp1_source_chunks="workflow_data/v10/Other_data/chunked_corpus.csv"
)
```

### Force Processing Mode
```python
# Cell 21
chunked_corpus, cp1_stats = run_checkpoint1_pipeline(
    CONFIG, fs,
    cp1_force_mode='text'  # or 'pdf'
)
```

---

## Troubleshooting

### If a Cell Fails

1. **Check the cell's print statement** - Each cell prints a confirmation when loaded successfully
2. **Run cells in order** - Cells must be executed sequentially (12 → 13 → ... → 21)
3. **Check dependencies** - Ensure all imports are available (PyMuPDF, nltk, pandas, numpy)
4. **Review error message** - Error will indicate which function failed

### Common Issues

**"PyMuPDF not installed"**
```bash
pip install PyMuPDF
```

**"NLTK stopwords not found"**
- Cell 17 auto-downloads stopwords
- If it fails, manually run: `nltk.download('stopwords')`

**"No PDF or TXT files found"**
- Check `CONFIG['paths']['corpus_dir']` path
- Ensure files have `.pdf` or `.txt` extensions

---

## Cell Modification Guide

### To Adjust Filtering Thresholds

**Edit Cell 13** (ProcessingConfig defaults):
```python
pdf_min_word_count: int = 50  # Change to 100 for stricter filtering
pdf_min_sentences: int = 3     # Change to 5 for stricter filtering
```

### To Add New Content Patterns

**Edit Cell 14** (Pattern definitions):
```python
BIBLIOGRAPHY_HEADERS = [
    # Add new patterns here
    r'^\s*(?:your_new_pattern)',
]
```

### To Modify Chunking Logic

**Edit Cell 18** (chunk_and_process_documents function):
```python
# Modify how chunks are created or filtered
```

### To Customize Statistics

**Edit Cell 19** (validate_and_save_corpus function):
```python
# Add new statistics to the report
```

---

## Summary

**Total Cells**: 10 (for Checkpoint 1 logic)
**Total Lines**: ~1,160 (split from 1,171)
**Execution**: Single function call in Cell 21
**Output**: Same structure as v14 (backward compatible)

**Benefits of Split Structure**:
- ✅ Clear separation of concerns
- ✅ Easy to modify individual components
- ✅ Better code readability
- ✅ Each cell has specific purpose
- ✅ Can test functions independently
- ✅ Clear print confirmations for debugging

---

**Version**: 15.0
**Date**: 2025-01-25
**Notebook**: dictionary_discovery_v15_consolidated.ipynb
