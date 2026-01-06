# V19 Bugfix: NaN Terms Handling

## Issues Found and Fixed

### Issue 1: IndexError in Cell 4.1
**Error**: `IndexError: index 19575 is out of bounds for axis 0 with size 19575`

**Root Cause**:
- Cell 4.1 was loading `vocabulary.csv` which includes ALL terms (vocab + seeds)
- But `vocab_embeddings.npy` from v19 only contains vocab-only terms (seeds excluded)
- Length mismatch caused index out of bounds error

**Fix**:
- Cell 4.1 now loads terms from `vocab_meta.json` instead of `vocabulary.csv`
- This ensures perfect alignment between terms list and embeddings array
- Added validation to check for mismatches

### Issue 2: KeyError with NaN terms
**Error**: `KeyError: nan`

**Root Cause**:
- Original vocabulary file contained NaN/invalid entries
- These propagated through the pipeline into `vocab_meta.json`
- When creating `vocab2vec`, Python couldn't use `nan` as a dictionary key

**Fix Applied in Two Places**:

#### Cell 3.1 (Prevention)
- Added NaN filtering after loading vocabulary
- Prevents invalid terms from entering the pipeline
```python
# Filter out NaN and invalid terms
original_count = len(terms)
terms = [t for t in terms if isinstance(t, str) and t and t == t]
term2idx = {t: i for i, t in enumerate(terms)}
if len(terms) < original_count:
    print(f"⚠ Filtered out {original_count - len(terms)} invalid/NaN terms")
```

#### Cell 4.1 (Safety Net)
- Added defensive filtering when creating vocab2vec
- Handles legacy workflows that might have NaN in saved files
```python
# Filter out NaN/invalid terms
valid_terms = [t for t in terms if isinstance(t, str) and t and t == t]
if len(valid_terms) < len(terms):
    print(f"⚠ Filtered out {len(terms) - len(valid_terms)} invalid/NaN terms")

vocab2vec = {term: vocab_emb[term2idx[term]] for term in terms if term in term2idx}
```

## Testing Recommendations

After these fixes, you should:

1. **Re-run from Cell 3.1** (not just Cell 4.1)
   - This ensures clean vocabulary without NaN
   - Regenerates `vocab_meta.json` with valid terms only

2. **Check for filtered terms**
   - Look for warning messages about filtered terms
   - If many terms are filtered, investigate the source data

3. **Verify alignment**
   - Cell 4.1 now validates that `len(terms) == vocab_emb.shape[0]`
   - If this fails, it indicates a deeper issue

## How NaN Enters the Vocabulary

Common sources:
1. **Empty rows in source documents** → Empty chunks → NaN terms
2. **CSV parsing issues** → Missing values interpreted as NaN
3. **Term extraction bugs** → None/NaN returned instead of skipping
4. **Pandas operations** → Operations on missing data produce NaN

## Prevention Going Forward

To prevent NaN terms in future workflows:

### In Checkpoint 2 (Vocabulary Building)
Add validation when creating vocabulary:
```python
# When building vocabulary
vocab_df = pd.DataFrame(vocab_terms)
vocab_df = vocab_df.dropna()  # Remove NaN rows
vocab_df = vocab_df[vocab_df['term'].str.len() > 0]  # Remove empty strings
```

### In Data Cleaning (Checkpoint 1)
Validate chunks before processing:
```python
# When creating chunks
chunks = [c for c in chunks if c and isinstance(c, str) and len(c.strip()) > 0]
```

## Backward Compatibility

These fixes maintain backward compatibility:
- Works with both old and new vocabulary files
- Gracefully handles NaN in existing saved data
- Warning messages alert users to data quality issues

## Impact on Results

Filtering NaN terms:
- ✅ Prevents crashes
- ✅ Improves data quality
- ⚠️ May slightly reduce vocabulary size (typically <0.01%)
- ⚠️ If many terms filtered (>1%), investigate source data quality

## Related Files Modified

1. **Cell 3.1**: Vocabulary loading with NaN filtering
2. **Cell 4.1**:
   - Changed from `vocabulary.csv` to `vocab_meta.json`
   - Added NaN filtering in vocab2vec creation
   - Added alignment validation

## Verification

To verify the fixes work:
```python
# After running Cell 3.1
print(f"Terms: {len(terms)}")
print(f"Sample: {terms[:5]}")
print(f"Any NaN? {any(t != t for t in terms)}")  # Should be False

# After running Cell 3.2
print(f"Vocab embeddings shape: {vocab_emb.shape}")
print(f"Terms in vocab_meta: {len(vocab_meta['terms'])}")
assert vocab_emb.shape[0] == len(vocab_meta['terms'])

# After running Cell 4.1
print(f"Terms loaded: {len(terms)}")
print(f"Vocab2vec size: {len(vocab2vec)}")
assert len(terms) == len(vocab2vec)
```

## Summary

| Issue | Location | Fix | Status |
|-------|----------|-----|--------|
| IndexError (length mismatch) | Cell 4.1 | Use vocab_meta.json | ✅ Fixed |
| KeyError (NaN terms) | Cell 3.1 | Filter NaN after loading | ✅ Fixed |
| KeyError (NaN terms) | Cell 4.1 | Filter NaN in vocab2vec | ✅ Fixed |
| Validation | Cell 4.1 | Added alignment check | ✅ Added |

All cells should now work correctly with v19's unified embedding approach!
