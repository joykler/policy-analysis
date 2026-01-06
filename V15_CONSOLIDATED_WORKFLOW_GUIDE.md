# Dictionary Discovery v15 - Consolidated Workflow Guide

## Overview

Version 15 introduces a **streamlined 4-stage processing pipeline** that consolidates the previous 5-cell, multi-function approach into a single, cohesive workflow with comprehensive filtering statistics.

### Key Improvements

- ✅ **Single function call** replaces complex multi-cell execution
- ✅ **Comprehensive statistics** showing what was filtered at each stage
- ✅ **Clear 4-stage architecture** with well-defined inputs/outputs
- ✅ **Unified configuration** with dataclass-based settings
- ✅ **Per-document reporting** showing filtering details for each file
- ✅ **Same output structure** - fully compatible with existing workflow

---

## The 4-Stage Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│ STAGE 1: Configuration & Source Loading                     │
│ ────────────────────────────────────────────────────────────│
│ • Load configuration from CONFIG dict                        │
│ • Apply overrides (CP1_SOURCE, CP1_SOURCE_CHUNKS, etc.)     │
│ • Auto-detect processing mode (PDF/text/chunked)             │
│ • Print configuration summary                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 2: Document Loading & Text Filtering                  │
│ ────────────────────────────────────────────────────────────│
│ PDF Mode:                                                    │
│   1. Extract pages from PDF                                  │
│   2. Filter pages (word count, sentences, English/numeric   │
│      ratio, layout detection, reference sections)            │
│   3. Detect and remove headers/footers                       │
│   4. Filter content (bibliographies, footnotes, indexes)     │
│   5. Save preprocessed text (optional)                       │
│                                                               │
│ Text Mode:                                                   │
│   1. Load text file directly                                 │
│                                                               │
│ Statistics Reported:                                         │
│   • Per-document: X/Y pages kept (filtered: reason=count)   │
│   • Aggregate: Total pages, filter breakdown by reason      │
│   • Content: Bibliography/footnote characters removed        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 3: Chunking & Dual Text Processing                    │
│ ────────────────────────────────────────────────────────────│
│ 1. Split document text into sentences                       │
│ 2. Group sentences into fixed-size chunks (e.g., 10/chunk)  │
│ 3. Filter chunks:                                            │
│    • Minimum sentence count (e.g., ≥2)                      │
│    • Minimum token count (e.g., ≥300)                       │
│    • English-only chunks (optional)                          │
│ 4. Create TWO text versions per chunk:                      │
│    • raw_text: Original sentence text                       │
│    • text_for_scoring: Processed (stopwords removed,        │
│      optionally stemmed)                                     │
│ 5. Generate unique chunk UIDs (file_hash:chunk_idx)         │
│                                                               │
│ Statistics Reported:                                         │
│   • Total chunks created                                     │
│   • Average chunks per document                              │
│   • Chunks filtered (reason=count)                           │
│   • Average tokens (raw vs processed)                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ STAGE 4: Validation & Statistics Reporting                  │
│ ────────────────────────────────────────────────────────────│
│ 1. Validate DataFrame structure                              │
│ 2. Save to CSV (Other_data/chunked_corpus.csv)              │
│ 3. Generate comprehensive statistics report:                 │
│    • Document-level stats                                    │
│    • PDF page-level stats (if PDF mode)                     │
│    • Content-level stats (bibliography/footnotes removed)    │
│    • Chunk-level stats                                       │
│    • Error summary                                           │
│ 4. Return chunks_df and final_stats dict                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Usage

### Basic Usage (Default Settings)

```python
# Execute the pipeline with default CONFIG settings
chunked_corpus, cp1_stats = run_checkpoint1_pipeline(CONFIG, fs)
```

### With Source Override

```python
# Override corpus source (different folder)
chunked_corpus, cp1_stats = run_checkpoint1_pipeline(
    CONFIG,
    fs,
    cp1_source="C:/path/to/other/PDF/folder"
)
```

### Load Pre-Chunked Data

```python
# Skip all processing, load existing chunked CSV
chunked_corpus, cp1_stats = run_checkpoint1_pipeline(
    CONFIG,
    fs,
    cp1_source_chunks="workflow_data/slavery_v10/Other_data/chunked_corpus.csv"
)
```

### Force Processing Mode

```python
# Force text mode even if PDFs are present
chunked_corpus, cp1_stats = run_checkpoint1_pipeline(
    CONFIG,
    fs,
    cp1_force_mode='text'
)
```

---

## Configuration Options

All configuration is centralized in the `ProcessingConfig` dataclass, automatically loaded from the `CONFIG` dictionary.

### Document Filtering (corpus_filter)

```python
CONFIG['corpus_filter'] = {
    'enabled': True,
    'years': [2020, 2021, 2022],  # Only these years
    'year_range': (2015, 2023),    # Or a range
    'doc_types': ['policy', 'report'],  # Filter by doc_type
    'filename_patterns': [r'.*slavery.*'],  # Include patterns
    'exclude_patterns': [r'.*draft.*'],      # Exclude patterns
}
```

### PDF Page Filtering (pdf_processing)

```python
CONFIG['pdf_processing'] = {
    'min_word_count': 50,              # Minimum words per page
    'min_sentences_per_page': 3,       # Minimum sentences per page
    'max_english_ratio': 0.5,          # Maximum English ratio (0-1)
    'max_numeric_ratio': 0.3,          # Maximum numeric ratio (0-1)
    'detect_layout_pages': True,       # Filter TOC/title pages
    'layout_whitespace_threshold': 0.7,  # Whitespace threshold
    'layout_avg_line_length': 30,      # Minimum avg line length
    'remove_reference_sections': True,  # Filter bibliography pages
    'remove_headers_footers': True,    # Remove repeated headers/footers
    'save_intermediate_text': True,    # Save preprocessed pages
}
```

### Content Filtering (new in v15)

Content filtering is automatically applied based on `pdf_processing` settings. Additional fine-tuning available via:

- **Bibliography removal**: Detects and removes bibliography sections (headers + citation patterns)
- **Footnote removal**: Removes superscript numbers, ibid, op. cit., author-year citations
- **Index skipping**: Entirely skips index pages (name-page number lists)

Patterns detected in **Dutch and English**:
- Headers: bibliografie, bibliography, literatuur, bronnen, references, noten, index, bijlagen
- Footnote markers: numbered footnotes, superscripts, ibid/op.cit, page refs (p. 123)
- Citations: Author (Year), DOI/URLs, publisher info

### Chunking (chunking)

```python
CONFIG['chunking'] = {
    'sentences_per_chunk': 10,         # Sentences per chunk
    'min_sentences_to_keep': 2,        # Minimum to keep chunk
    'drop_likely_english': True,       # Filter English sentences
    'remove_stopwords': True,          # Remove stopwords for scoring
    'use_stemming': False,             # Apply Dutch stemming
}
```

New in v15:
- **Minimum tokens**: Chunks with <300 tokens (after processing) are filtered out
- **Dual text versions**: `raw_text` (original) and `text_for_scoring` (processed)

---

## Statistics Reporting

### Per-Document Statistics (During Processing)

```
  [15/26] document_name.pdf
    PDF: 45/50 pages kept (filtered: too_few_words=3, layout_page=2), index pages=5
```

Shows:
- Document progress (15 of 26)
- Pages kept vs total
- Filter reasons with counts
- Content filters applied (index pages)

### Final Statistics Report (After Processing)

#### Document-Level
```
DOCUMENT-LEVEL STATISTICS
  Total documents found: 26
  Skipped by filters: 3
    year_out_of_range: 2
    doc_type_excluded: 1
  Successfully processed: 23
  Failed: 0
```

#### PDF Page-Level (PDF mode only)
```
PDF PAGE-LEVEL STATISTICS
  Total pages extracted: 1,250
  Pages kept after filtering: 875
  Pages filtered out: 375

  Filter breakdown:
    too_few_words: 145 (11.6%)
    layout_page: 89 (7.1%)
    too_few_sentences: 67 (5.4%)
    reference_section: 42 (3.4%)
    too_much_english: 32 (2.6%)
```

#### Content-Level (PDF mode only)
```
CONTENT-LEVEL STATISTICS
  Index pages removed: 45
  Bibliography characters removed: 125,430
  Footnote markers removed: 8,234
  Total content filtered: 12.3% of original text
```

#### Chunk-Level
```
CHUNK-LEVEL STATISTICS
  Total chunks created: 3,456
  Average chunks per document: 150.3
  Min/Max chunks per document: 45/287

  Chunks filtered out:
    too_few_sentences: 123
    all_english: 45
    too_few_tokens: 89

  Average tokens per chunk:
    raw_text: 487.3
    text_for_scoring: 312.1
```

---

## Output Structure

The output DataFrame (`chunked_corpus`) has the same structure as previous versions:

| Column | Type | Description |
|--------|------|-------------|
| `file_path` | str | Full path to source document |
| `chunk_uid` | str | Unique chunk ID (file_hash:chunk_idx) |
| `raw_text` | str | Original chunk text (sentences joined) |
| `text_for_scoring` | str | Processed text (stopwords removed, optionally stemmed) |
| `sentence_count` | int | Number of sentences in chunk |
| `doc_type` | str | Document type (from path structure) |
| `year` | str | Year (from path structure) |
| `document_folder` | str | Parent folder name |
| `filename` | str | Original filename |

**Fully compatible** with:
- Checkpoint 2 (Vocabulary Building)
- Checkpoint 3 (Dictionary Expansion)
- Checkpoint 4 (Topic Vectors)
- Checkpoint 5 (Chunk Scoring)
- Checkpoint 6 (Training Data Preparation)
- Checkpoint 7 (Model Training)

---

## Filtering Summary

### What Gets Filtered and When

#### Stage 2: Document & Page Filtering

**Document-Level** (before processing):
- ❌ Documents outside specified years
- ❌ Documents with wrong doc_type
- ❌ Documents not matching filename patterns
- ❌ Documents matching exclude patterns

**PDF Page-Level**:
- ❌ Empty pages (<1 word)
- ❌ Pages with <50 words (configurable)
- ❌ Pages with <3 sentences (configurable)
- ❌ Pages with >50% English words (configurable)
- ❌ Pages with >30% numeric characters (configurable)
- ❌ Layout pages (high whitespace, short lines)
- ❌ Reference sections (>20% citation density)

**Cross-Page Processing**:
- ✂️ Repeated headers (first 3 lines, >60% of pages)
- ✂️ Repeated footers (last 3 lines, >60% of pages)
- ✂️ Page numbers (standalone number lines)

**Content-Level**:
- ❌ **Index pages** (name-page number lists) → entire page removed
- ✂️ **Bibliography sections** (detected headers + citation patterns) → split off and removed
- ❌ **Bibliography-only pages** → entire page removed
- ✂️ **Footnote markers** (superscripts, ibid, op.cit, author-year) → removed inline
- ✂️ **Cross-references** (zie ook, cf., see also) → removed
- ✂️ **Page references** (p. 123, pp. 45-67) → removed

#### Stage 3: Chunk Filtering

- ❌ Chunks with <2 sentences (configurable)
- ❌ Chunks with <300 tokens after processing
- ❌ All-English chunks (if drop_likely_english=True)
- ✂️ Stopwords and numbers (for text_for_scoring only)
- ✂️ Stemming (optional, for text_for_scoring only)

---

## Comparison: v14 vs v15

| Aspect | v14 (5 cells) | v15 (4 cells) |
|--------|---------------|---------------|
| **Cells** | 5 separate cells | 4 cells (1 header, 1 import, 1 functions, 1 execution) |
| **Execution** | Multi-step manual execution | Single function call |
| **Configuration** | Scattered across cells | Unified ProcessingConfig dataclass |
| **Statistics** | Inline prints | Comprehensive structured report |
| **Per-document stats** | Limited | Detailed filtering breakdown |
| **Content filtering** | Manual integration | Automatic in pipeline |
| **Error handling** | Basic try/catch | Centralized error tracking |
| **Maintainability** | Complex, scattered | Modular, clear stages |
| **Output structure** | Same | Same (fully compatible) |

---

## Migration from v14

If you have existing notebooks using v14:

1. **Replace cells 11-15** with the new consolidated cells from v15
2. **Update execution** from manual multi-cell to single function call:

```python
# v14 (multiple cells)
corpus_source = Path(CP1_SOURCE or CONFIG['paths']['corpus_dir'])
corpus_mode = detect_mode(corpus_source)
files = discover_files(corpus_source)
# ... more cells ...

# v15 (single call)
chunked_corpus, cp1_stats = run_checkpoint1_pipeline(CONFIG, fs)
```

3. **Configuration is compatible** - no changes needed to CONFIG dict
4. **Output is identical** - downstream checkpoints work without modification

---

## Advanced Usage

### Custom Configuration

```python
# Create custom config with overrides
from consolidated_checkpoint1 import ProcessingConfig

custom_config = ProcessingConfig(
    corpus_source=Path("custom/path"),
    pdf_min_word_count=100,  # Stricter filtering
    chunk_min_tokens=500,     # Larger chunks
    scoring_use_stemming=True  # Enable stemming
)

# Run with custom config
# (Note: would need to modify function to accept config object directly)
```

### Accessing Detailed Statistics

```python
chunked_corpus, stats = run_checkpoint1_pipeline(CONFIG, fs)

# Access structured statistics
print(f"Documents processed: {stats['documents']['processed']}")
print(f"Total chunks: {stats['chunks']['total']}")
print(f"Pages filtered: {stats['pages']['filter_reasons']}")

# Save statistics to JSON
import json
with open('checkpoint1_stats.json', 'w') as f:
    json.dump(stats, f, indent=2)
```

### Processing Multiple Corpora

```python
corpora = [
    ("PDF sources/policy", "policy_corpus"),
    ("PDF sources/historical", "historical_corpus"),
]

all_chunks = []
for corpus_path, output_name in corpora:
    chunks, stats = run_checkpoint1_pipeline(
        CONFIG,
        fs,
        cp1_source=corpus_path
    )
    chunks['corpus_name'] = output_name
    all_chunks.append(chunks)

combined_corpus = pd.concat(all_chunks, ignore_index=True)
```

---

## Troubleshooting

### Issue: "No PDF or TXT files found"

**Solution**: Check that:
- `corpus_source` path exists
- Files have `.pdf` or `.txt` extensions
- Subdirectories are searched (uses `**/*.pdf` pattern)

### Issue: "All chunks filtered out"

**Cause**: Filtering may be too aggressive

**Solutions**:
- Lower `chunk_min_tokens` (default: 300)
- Lower `chunk_min_sentences` (default: 2)
- Disable `scoring_drop_english` if corpus is mixed language
- Check PDF page filtering thresholds

### Issue: "PyMuPDF not installed"

**Solution**: Install PyMuPDF:
```bash
pip install PyMuPDF
```

### Issue: Processing is slow

**Solutions**:
- Disable `pdf_save_preprocessed` if you don't need intermediate text
- Process PDFs once, then use pre-chunked mode for iterations:
  ```python
  # First run (full processing)
  chunks, stats = run_checkpoint1_pipeline(CONFIG, fs)

  # Subsequent runs (load pre-chunked)
  chunks, stats = run_checkpoint1_pipeline(
      CONFIG, fs,
      cp1_source_chunks="workflow_data/.../Other_data/chunked_corpus.csv"
  )
  ```

---

## Technical Details

### Architecture

```
ProcessingConfig (dataclass)
  ↓
load_configuration() → config
  ↓
load_and_filter_documents(config) → documents, doc_stats
  ↓
chunk_and_process_documents(documents, config) → chunks_df, chunk_stats
  ↓
validate_and_save_corpus(chunks_df, doc_stats, chunk_stats) → final_stats
```

### Key Classes

- **ProcessingConfig**: Unified configuration dataclass
- **DocumentStats**: Per-document statistics
- **ProcessingStats**: Aggregate statistics across all documents

### Key Functions

- `run_checkpoint1_pipeline()`: Main orchestration function
- `load_configuration()`: Stage 1 - Config setup
- `load_and_filter_documents()`: Stage 2 - Document loading
- `chunk_and_process_documents()`: Stage 3 - Chunking
- `validate_and_save_corpus()`: Stage 4 - Validation & saving

### Pattern Detection

**Bibliography Headers** (case-insensitive):
- Dutch: bibliografie, literatuur, bronnen, noten, bijlagen
- English: bibliography, references, footnotes, appendix

**Footnote Patterns**:
- Numbered: `1. Author (2020)`
- Superscripts: `word23 `, `sentence.45`
- Latin: ibid, ibidem, op. cit, loc. cit
- Citations: `Author (2023)`, `p. 45`

**Index Patterns**:
- Name entries: `Lastname, Firstname 12, 45, 67`
- Page number density: 5+ page numbers in sequence

---

## Future Enhancements

Potential improvements for v16:

1. **Parallel processing** for large corpora
2. **Caching** of PDF extraction results
3. **Configurable pattern detection** for different document types
4. **Machine learning-based** section classification
5. **Interactive filtering** threshold tuning
6. **Visualization** of filtering statistics

---

## Support

For issues or questions about the consolidated workflow:

1. Check the troubleshooting section above
2. Review the comprehensive statistics output for filtering details
3. Examine `checkpoint1_stats.json` for detailed metrics
4. Test with a small sample corpus first

## Changes from Original v14

1. ✅ **Consolidated 5 cells into 4** with clear separation of concerns
2. ✅ **Single function call** execution (was: multi-step manual)
3. ✅ **Comprehensive per-document statistics** (was: basic totals)
4. ✅ **Unified configuration** (was: scattered across cells)
5. ✅ **Integrated content filtering** (was: separate optional step)
6. ✅ **Structured statistics reporting** (was: inline prints)
7. ✅ **Better error tracking** (was: exceptions halt execution)
8. ✅ **Same output structure** (fully backward compatible)

---

**Version**: 15.0
**Date**: 2025-01-25
**Compatibility**: Works with all downstream checkpoints (CP2-CP7)
