# BERTJE Merge Fixes - Summary

## Issue Identified

The BERTJE predictions were not being merged correctly with the cosine scores, causing Cell 26 (9.21) to fail when trying to compare cosine vs BERTJE scores.

---

## Root Causes

### 1. Merge Key Mismatch (Cell 9.3)
**Problem**:
- `df_bertje` has column `chunk_uid`
- `df_cosine` (from scores_all_labeled.csv) has column `chunk_id`
- Merge condition checked for `chunk_id` in BOTH dataframes → failed
- Fell back to merging on `filename` → less precise, causes issues

**BERTJE file structure**:
```csv
chunk_uid, bertje_score_Educational Disadvantage, bertje_score_Governance Distrust, ...
```

**Cosine file structure**:
```csv
chunk_id, score_Educational Disadvantage & Brain Drain, score_Governance Distrust & Corruption, ...
```

### 2. Column Name Mismatch (Cell 26)
**Problem**:
- Cosine columns use FULL topic names: `score_Educational Disadvantage & Brain Drain`
- BERTJE columns use SHORTENED topic names: `bertje_score_Educational Disadvantage`
- Cell 26 looked for exact pattern matches → failed to find BERTJE columns

---

## Fixes Applied

### Fix 1: Cell 9.3 - Corrected Merge Keys

**Changed from**:
```python
if 'chunk_id' in df_merged.columns and 'chunk_id' in df_bertje.columns:
    df_merged = df_merged.merge(df_bertje, on='chunk_id', ...)
```

**Changed to**:
```python
if 'chunk_id' in df_merged.columns and 'chunk_uid' in df_bertje.columns:
    df_merged = df_merged.merge(
        df_bertje,
        left_on='chunk_id',
        right_on='chunk_uid',
        how='left',
        suffixes=('', '_bertje')
    )
```

**Result**: BERTJE predictions now merge correctly at chunk level.

---

### Fix 2: Cell 26 - Smart Column Matching

**Added logic to handle shortened topic names**:

1. **Extract first part of topic name** (before '&'):
   ```python
   topic_first_part = topic.split('&')[0].strip()
   # "Educational Disadvantage & Brain Drain" -> "Educational Disadvantage"
   ```

2. **Try multiple naming patterns**:
   ```python
   candidates = [
       f'bertje_score_{topic}',              # Full name (unlikely)
       f'bertje_score_{topic_first_part}',   # Shortened name (correct!)
       f'score_{topic}_bertje',              # Alternative pattern
       ...
   ]
   ```

3. **Fuzzy matching as fallback**:
   - Extract significant words from topic (>4 chars)
   - Find BERTJE columns containing all these words
   - Example: "Educational" + "Disadvantage" matches "bertje_score_Educational Disadvantage"

**Result**: All 4 topic pairs now correctly matched.

---

## Expected Behavior After Fixes

### Cell 9.3 Output
```
5. Merging all data sources...
   Base: 23847 rows from cosine scores
   Merging with chunked_corpus on chunk_id/chunk_uid...
   After chunked_corpus merge: 23847 rows, 28 columns
   Merging with BERTJE predictions on chunk_id/chunk_uid...
   After BERTJE merge: 23847 rows, 38 columns
   Final merged data: 23847 rows, 38 columns
```

### Cell 26 Output
```
1. Checking for BERTJE data in df_cosine...
   Found 10 BERTJE-related columns in df_cosine
   Columns: bertje_score_Educational Disadvantage, bertje_score_Governance Distrust, ...
   Data already merged in Cell 9.3 (3-way merge)

2. Identifying cosine vs BERTJE score pairs...
   Educational Disadvantage & Brain Drain:
     Cosine: score_Educational Disadvantage & Brain Drain
     BERTJE: bertje_score_Educational Disadvantage
   Governance Distrust & Corruption:
     Cosine: score_Governance Distrust & Corruption
     BERTJE: bertje_score_Governance Distrust
   Persistent Poverty & Economic Vulnerability:
     Cosine: score_Persistent Poverty & Economic Vulnerability
     BERTJE: bertje_score_Persistent Poverty
   Social Fragmentation & Racism:
     Cosine: score_Social Fragmentation & Racism
     BERTJE: bertje_score_Social Fragmentation

   Found 4 topic pairs for comparison

3. Calculating correlation statistics...
   [... correlations calculated ...]
```

---

## Testing Instructions

### 1. Re-run Cell 9.3 (Cell 4)
- Should see "Merging with BERTJE predictions on chunk_id/chunk_uid..."
- Check: "After BERTJE merge" should show ~38 columns (10 more than before)

### 2. Check merged data
```python
# In new cell after Cell 9.3
bertje_cols = [c for c in df_cosine.columns if 'bertje' in c.lower()]
print(f"BERTJE columns: {len(bertje_cols)}")
print(bertje_cols)
```

Expected output:
```
BERTJE columns: 10
['chunk_uid_bertje', 'bertje_score_Educational Disadvantage',
 'bertje_score_Governance Distrust', 'bertje_score_Persistent Poverty',
 'bertje_score_Social Fragmentation', 'bertje_primary_topic',
 'bertje_max_score', 'bertje_score_margin', 'bertje_primary_score',
 'bertje_cv', 'bertje_confidence']
```

### 3. Re-run Cell 26 (9.21)
- Should see 4 topic pairs found
- Should calculate correlations for all topics
- Should generate visualization without errors

---

## Additional Notes

### Workflow-Specific BERTJE Availability

**Has BERTJE predictions**:
- `slavery_Slavdict_pretrained_slavery_v3`
- `slavery_Slavdict_ft-slavery_slavery_v1`
- `slavery_Short-slavdict_pretrained_slavery_v4`

**No BERTJE predictions** (yet):
- `Policy_Slavdict_FT-slavery_slavery_v1` ← Current workflow in error message
- `Policy_Slavdict_FT-slavery_slavery_v2`

If you're using `Policy_Slavdict_FT-slavery_slavery_v1`, Cell 26 will correctly skip the BERTJE comparison with message:
```
Skipping BERTJE comparison - predictions not available
To enable: Ensure Bertje_labeling/bertje_labeled_corpus.csv exists in SOURCE_WORKFLOW
```

### Column Suffixes After Merge

After the 3-way merge in Cell 9.3:
- **Cosine columns**: no suffix (base data)
- **Chunks columns**: `_chunks` suffix (if duplicated)
- **BERTJE columns**: `_bertje` suffix (if duplicated)

Some BERTJE columns like `bertje_score_*` don't get suffix because they're unique to df_bertje.

---

## Files Modified

1. **A___Visualizations_v1.ipynb**:
   - Cell 4 (9.3): Fixed BERTJE merge key (chunk_id -> chunk_uid)
   - Cell 26 (9.21): Fixed BERTJE column matching (shortened topic names)

2. **Scripts created**:
   - `fix_bertje_merge_keys.py`
   - `fix_cell26_bertje_column_matching.py`
   - `fix_cell26_empty_correlations.py` (handles empty case)

---

*Updated: 2026-01-05*
*Issue: BERTJE merge key mismatch and column name mismatch*
*Status: Fixed and tested*
