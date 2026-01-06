# Text Field Usage Fix - Executive Summary

## Problem Identified

The notebook has **inconsistent text field usage** between different pipeline stages:

```
Pipeline Flow (Intended):
raw_text → text_for_processing → text_for_scoring

Current Usage:
✓ Vocabulary building: text_for_scoring (correct)
✓ Topic scoring: text_for_scoring (correct)
✗ BERTJE training: raw_text (WRONG - should be text_for_scoring)
⚠ Prediction: text_for_scoring with fallback to raw_text (needs warning)
```

## Why This Matters

### Impact on Model Quality

1. **Train/Test Mismatch**:
   - Model trains on `raw_text` (unprocessed)
   - Model predicts on `text_for_scoring` (cleaned, validated)
   - Different input distributions → degraded performance

2. **English Text Contamination**:
   - If `scoring_drop_english=True` is enabled:
     - `text_for_scoring` = Dutch only (English removed)
     - `raw_text` = Dutch + English (mixed)
   - BERTJE learns from English-contaminated text
   - Predictions made on Dutch-only text
   - **Result**: Vocabulary mismatch

3. **Validation Failures Ignored**:
   - `text_for_scoring` excludes chunks that are too short/long
   - `raw_text` includes ALL chunks
   - Training on invalid chunks → noise in model

### Example Scenario

```
Chunk in corpus:
  raw_text = "Dit is een beleid about slavery legacy with English terms"
  text_for_processing = "Dit is een beleid about slavery legacy with English terms"
  text_for_scoring = "Dit is een beleid slavery legacy" (English removed, cleaned)

Current behavior (WRONG):
  - Vocabulary built from: "Dit is een beleid slavery legacy" ✓
  - Scoring uses: "Dit is een beleid slavery legacy" ✓
  - BERTJE trains on: "Dit is een beleid about slavery legacy with English terms" ✗
  - BERTJE predicts: "Dit is een beleid slavery legacy" ✓

After fix (CORRECT):
  - All stages use: "Dit is een beleid slavery legacy" ✓✓✓✓
```

## Cells Requiring Fixes

### Cell 41 - All Labeled Data (CRITICAL)
```python
# BEFORE
Scores_all_labeled['text'] = Scores_all_labeled['raw_text']

# AFTER
Scores_all_labeled['text'] = Scores_all_labeled['text_for_scoring']
```

### Cell 44 - High Confidence Labeled Data (CRITICAL)
```python
# BEFORE
df_labeled['text'] = df_labeled['raw_text']

# AFTER
df_labeled['text'] = df_labeled['text_for_scoring']
```

### Cell 45 - Pseudo-labels + Unlabeled Data (CRITICAL)
```python
# BEFORE
df_pseudo["text"] = df_pseudo["raw_text"]
df_unlabeled["text"] = df_unlabeled["raw_text"]

# AFTER
df_pseudo["text"] = df_pseudo["text_for_scoring"]
df_unlabeled["text"] = df_unlabeled["text_for_scoring"]
```

### Cell 70 - Prediction Fallback (MINOR)
```python
# BEFORE
elif 'raw_text' in corpus_df.columns:
    texts = corpus_df['raw_text'].fillna('').tolist()

# AFTER
elif 'raw_text' in corpus_df.columns:
    print('WARNING: text_for_scoring missing, falling back to raw_text')
    texts = corpus_df['raw_text'].fillna('').tolist()
```

## Cells Using Text Fields Correctly (No Change)

✓ **Cell 15** - Creates `raw_text` and `text_for_processing`
✓ **Cell 16** - Transforms `text_for_processing` → `text_for_scoring`
✓ **Cell 22** - Vocabulary building uses `text_for_scoring`
✓ **Cell 36** - Topic scoring uses `text_for_scoring`
✓ **Cell 37** - Display uses `raw_text` (appropriate)
✓ **Cell 76** - Validation uses `raw_text` (appropriate for display)
✓ **Cell 77** - Snippets use `raw_text` (appropriate for visualization)

## Implementation Plan

### Step 1: Apply Fixes
Run `fix_text_field_usage.py` to automatically update cells 41, 44, 45, 70

### Step 2: Verify Changes
- Open notebook in Jupyter
- Check cells 41, 44, 45, 70 manually
- Confirm `text_for_scoring` is now used

### Step 3: Regenerate Training Data
After fixes, you MUST re-run cells to regenerate training data:
- Run Cell 41 → Regenerates `Scores_all_labeled`
- Run Cell 44 → Regenerates `df_labeled`
- Run Cell 45 → Regenerates `df_pseudo`, `df_unlabeled`

### Step 4: Retrain BERTJE (Optional but Recommended)
- Re-run cells 46-60 to retrain BERTJE on cleaned text
- Compare model quality before/after

### Step 5: Test Prediction
- Run Cell 70 on full corpus
- Verify no "WARNING" message appears (text_for_scoring present)
- Check prediction quality

## Expected Improvements

After fixing and retraining:

1. **Consistency**: All pipeline stages use same cleaned text
2. **Better vocabulary alignment**: BERTJE embeddings match scoring vocabulary
3. **No English contamination**: If enabled, fully respected throughout
4. **Higher prediction quality**: Train/test distribution match

## Validation Checklist

After implementing fixes and retraining:

- [ ] Cell 41 uses `text_for_scoring`
- [ ] Cell 44 uses `text_for_scoring`
- [ ] Cell 45 uses `text_for_scoring` (both pseudo and unlabeled)
- [ ] Cell 70 shows warning if fallback used
- [ ] Training data regenerated (re-ran cells 41, 44, 45)
- [ ] BERTJE model retrained (optional: cells 46-60)
- [ ] Predictions tested on full corpus
- [ ] No vocabulary mismatch warnings in logs
- [ ] Backup of original notebook saved

## Files Generated

1. `TEXT_FIELD_USAGE_ANALYSIS.md` - Detailed cell-by-cell analysis
2. `TEXT_FIELD_FIX_SUMMARY.md` - This executive summary
3. `fix_text_field_usage.py` - Automated fix script
4. `A__dictionary_discovery_v24_unified_embedding_backup.ipynb` - Backup (auto-created)

## Next Steps

1. Review this summary and the detailed analysis
2. Run `python fix_text_field_usage.py` when ready
3. Re-run affected cells in notebook
4. Optionally retrain BERTJE for improved quality

---

**Critical Note**: These fixes are essential for Stage 2 (Policy corpus) where English text is more prevalent. For Stage 1 (Slavery corpus), impact may be smaller but consistency is still important for reproducibility.
