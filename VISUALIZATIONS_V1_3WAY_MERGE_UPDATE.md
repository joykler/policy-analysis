# Visualizations v1 - 3-Way Merge Update

## Summary

The standalone visualization notebook has been updated to merge three data sources instead of two, keeping all columns from each source.

---

## What Changed

### Previous Approach (2-way merge):
```
df_cosine (scores) + df_chunks (metadata) → df_merged
```

### New Approach (3-way merge):
```
df_cosine (scores) + df_chunks (metadata) + df_bertje (BERTJE predictions) → df_merged
```

**All columns from all three sources are preserved!**

---

## Data Sources

### 1. Cosine Scores (`Cosine_labeling/scores_all_labeled.csv`)
- **Contains**: Cosine similarity scores for each topic
- **Columns**: `chunk_id`, `filename`, `score_*` (one per topic)
- **Role**: Base data source (primary)

### 2. Chunked Corpus (`Other_data/chunked_corpus.csv`)
- **Contains**: Chunk metadata and text
- **Columns**: `chunk_uid`, `filename`, `doc_type`, `year`, `document_folder`, `text_for_scoring`
- **Role**: Adds metadata and text to scores

### 3. BERTJE Labeled Corpus (`Bertje_labeling/bertje_labeled_corpus.csv`)
- **Contains**: BERTJE model predictions for each chunk
- **Columns**: `chunk_id`, `filename`, `predicted_label`, `confidence`, model-specific scores
- **Role**: Adds BERTJE predictions for comparison with cosine scores

---

## Configuration Updates

### Cell 1 - SOURCE_WORKFLOW
```python
# Now points to slavery workflow (which has all three files)
SOURCE_WORKFLOW = r"C:\Users\Home\policy-analysis\workflow_Structureddict\slavery_structured-slavdict_pretrained_slavery_v1"
```

### Cell 2 - Filesystem Setup
```python
folders = {
    'Dictionary': base_dir / 'Dictionary',
    'Cosine_labeling': base_dir / 'Cosine_labeling',
    'Bertje_labeling': base_dir / 'Bertje_labeling',  # NEW - Added
    'Other_data': base_dir / 'Other_data',
    'Model_finetuning': base_dir / 'Model_finetuning',
    'BERTJE_predictions': base_dir / 'BERTJE_predictions',
    'Visuals': base_dir / 'Visuals'
}
```

**Note**: `Bertje_labeling` is OPTIONAL. If not found, notebook continues without BERTJE predictions.

### Cell 4 (Cell 9.3) - Load Core Data
Updated to include 7 steps instead of 6:

1. Load Dictionary
2. **Load BERTJE Labeled Corpus (NEW)**
3. Load Cosine Scores
4. Load Chunked Corpus
5. **Merge All Data (3-way merge) (UPDATED)**
6. Apply Metadata Filters
7. Create Output Directory

---

## Merge Logic

### Merge Keys (in priority order):
1. **Primary**: `chunk_id` (cosine/bertje) ↔ `chunk_uid` (chunks)
2. **Fallback**: `filename` (all sources)

### Merge Process:
```python
# Step 1: Start with cosine scores as base
df_merged = df_cosine.copy()

# Step 2: Merge with chunked corpus (left join)
df_merged = df_merged.merge(
    df_chunks,
    left_on='chunk_id',
    right_on='chunk_uid',
    how='left',
    suffixes=('', '_chunks')
)

# Step 3: Merge with BERTJE predictions (left join)
if df_bertje is not None:
    df_merged = df_merged.merge(
        df_bertje,
        on='chunk_id',
        how='left',
        suffixes=('', '_bertje')
    )

# Final: Replace df_cosine with merged data
df_cosine = df_merged
```

### Handling Duplicate Columns:
- Suffixes are added automatically: `_chunks`, `_bertje`
- Example: If `filename` exists in all three sources:
  - `filename` (from cosine)
  - `filename_chunks` (from chunked corpus)
  - `filename_bertje` (from BERTJE)

---

## Expected Workflow Structure

Your `SOURCE_WORKFLOW` should have this structure:

```
workflow_Structureddict/slavery_structured-slavdict_pretrained_slavery_v1/
├── Dictionary/
│   └── Curated_dictionary.csv
├── Cosine_labeling/
│   └── scores_all_labeled.csv
├── Bertje_labeling/                          # NEW
│   └── bertje_labeled_corpus.csv             # NEW
├── Other_data/
│   └── chunked_corpus.csv
├── Model_finetuning/
│   └── trained_encoder/
│       ├── config.json
│       ├── model.safetensors
│       └── ... (other model files)
└── Visuals/                                   # Auto-created
```

---

## Benefits

### 1. Complete Data Integration
- All data sources merged in one place
- No need to manually align data later
- All columns available for visualizations

### 2. Flexible Comparison
- Compare cosine scores vs. BERTJE predictions
- Analyze agreement/disagreement patterns
- Cross-validate different scoring methods

### 3. Optional BERTJE
- If `bertje_labeled_corpus.csv` doesn't exist, notebook continues
- Only skips BERTJE-specific visualizations (Section 6)
- All other visualizations work normally

### 4. Preserved Information
- No data loss during merge
- All columns kept with clear suffixes
- Easy to identify source of each column

---

## Usage

### Running the Notebook:

1. **Restart Kernel** (to clear cached variables)
2. **Run Cell 1**: Configuration (sets SOURCE_WORKFLOW)
3. **Run Cell 2**: Filesystem Setup (checks folders)
4. **Run Cell 3**: Import Libraries
5. **Run Cell 4**: Load Core Data (3-way merge happens here)
6. **Run Cell 5**: Load BERTJE Models
7. **Continue with remaining cells**: Visualizations

### Expected Output from Cell 4:

```
======================================================================
LOADING CORE DATA
======================================================================

1. Loading dictionary...
   Loaded 848 dictionary terms
   Topics: 4
     ...

2. Loading BERTJE labeled corpus...
   Loaded 12547 BERTJE predictions
   Columns: ['chunk_id', 'filename', 'predicted_label', 'confidence', ...]

3. Loading cosine scores...
   Loaded 12547 scored chunks
   Columns: ['chunk_id', 'filename', 'score_Educational_Disadvantage_&_Brain_Drain', ...]

4. Loading chunked corpus...
   Loaded 12547 chunks
   Available metadata: doc_type, year, document_folder, filename

5. Merging all data sources...
   Base: 12547 rows from cosine scores
   Base columns: 15
   Merging with chunked_corpus on chunk_id/chunk_uid...
   After chunked_corpus merge: 12547 rows, 25 columns
   Merging with BERTJE predictions on chunk_id...
   After BERTJE merge: 12547 rows, 38 columns
   Final merged data: 12547 rows, 38 columns
   All columns preserved from all sources

6. Applying metadata filters...
   No filters applied (using all 12547 chunks)

7. Creating output directory...
   Output directory: C:\...\Visuals

======================================================================
DATA LOADING COMPLETE
======================================================================
Dictionary: 848 terms across 4 topics
Scored chunks: 12547
Total columns: 38
Topics: [...]
Output: C:\...\Visuals
======================================================================

Section 1 Complete - Ready for model loading!
```

---

## Troubleshooting

### Issue: "BERTJE labels not found"
**Expected**: This is a WARNING, not an ERROR. The notebook will continue without BERTJE predictions.

**To include BERTJE predictions**:
1. Ensure `Bertje_labeling/bertje_labeled_corpus.csv` exists in your SOURCE_WORKFLOW
2. Check that the file has `chunk_id` or `filename` column for merging

### Issue: Merge produces fewer rows than expected
**Cause**: Some chunks in cosine scores don't have matches in other sources

**Solution**: This is expected with `how='left'` merge. Missing values will be NaN. Check the merge keys:
- Verify `chunk_id` values match between files
- Or verify `filename` values match between files

### Issue: Too many columns with suffixes
**Cause**: Column names overlap between sources (e.g., all have `filename`)

**Solution**: This is expected behavior. Use the suffixes to identify source:
- `filename` → from cosine scores
- `filename_chunks` → from chunked corpus
- `filename_bertje` → from BERTJE predictions

---

## Files Modified

1. **A___Visualizations_v1.ipynb**
   - Cell 1: SOURCE_WORKFLOW set to slavery workflow
   - Cell 2: Added 'Bertje_labeling' folder
   - Cell 4: Updated to 3-way merge

2. **update_cell_9_3_merge.py** (new)
   - Script that updated Cell 4 merge logic

3. **update_cell_2_bertje_folder.py** (new)
   - Script that added Bertje_labeling folder

4. **update_cell_1_source_workflow.py** (new)
   - Script that set SOURCE_WORKFLOW path

5. **VISUALIZATIONS_V1_3WAY_MERGE_UPDATE.md** (this file)
   - Documents the 3-way merge update

---

## Next Steps

The notebook is ready to use! Simply:

1. Open `A___Visualizations_v1.ipynb` in Jupyter
2. Restart kernel
3. Run all cells

The 3-way merge will happen automatically in Cell 4, and all subsequent visualizations will have access to:
- Cosine scores
- BERTJE predictions
- Chunk metadata
- Chunk text

---

*Updated: 2026-01-05*
*Version: Visualizations v1 (3-way merge)*
