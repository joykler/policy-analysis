# Re-run Instructions: Enable Unnormalized Embeddings

## Issue Found

Your current workflow output shows:
```
Max score: 0.6186
Range: 0.15 - 0.62
```

This indicates **normalized embeddings are still being used** (compressed 0-1 range).

## Root Cause

In **Cell 4**, the `st_embed` function had:
```python
normalize_embeddings=True  # ❌ Wrong - compresses to 0-1 range
```

## Fix Applied

Changed to:
```python
normalize_embeddings=False  # ✅ Correct - preserves magnitude
```

## What This Means

### Before (normalized):
- Cosine similarity range: 0.0 - 1.0
- Even with dot product, scores compressed to ~0.15 - 0.62
- No magnitude information preserved
- Significance scoring won't work correctly

### After (unnormalized):
- Dot product range: ~0.77 - 9.22 (based on validation data)
- Magnitude information preserved
- Significance scoring works as designed
- CV-based noise filtering effective

## Next Steps

### 1. Re-run from Cell 4 onward

You need to regenerate ALL embeddings and scores with unnormalized embeddings:

```
Cell 4  → Topic vectors (with normalize_embeddings=False)
Cell 36 → Chunk scoring (dot product will now give wider range)
Cell 37 → Significance classification (calibrated for 0-9 range)
```

### 2. Expected Changes

**Cell 36 output should show:**
```
DOT PRODUCT SCORE DISTRIBUTION
  Min:  ~0.77
  Max:  ~9.22
  Range: ~8.45
```

**Cell 37 output should show:**
- High significance chunks: Clear topic differentiation
- Noise chunks: Uniform scores with CV < 0.10
- Proper distribution across 4 significance tiers

### 3. Validation

After re-running, check:

✅ **Score range is wide** (~0.77 - 9.22, not 0.15 - 0.62)
```python
print(f"Max score: {all_scores_df['max_score'].max():.2f}")
# Should be ~9.0, not ~0.6
```

✅ **CV detects noise correctly**
```python
# Check a known noise example
noise_example = all_scores_df[all_scores_df['cv'] < 0.10].iloc[0]
print(f"Noise chunk scores: {noise_example[topic_cols].values}")
# Should show uniform pattern like [4.88, 4.89, 4.92, 4.83]
```

✅ **Significance distribution makes sense**
```python
print(all_scores_df['significance_category'].value_counts())
# Should have reasonable distribution across tiers
```

## Why This Matters

### Problem with Normalized Embeddings + Dot Product

When embeddings are normalized (unit length), dot product becomes mathematically equivalent to cosine similarity:

```python
# Normalized embeddings
a_norm = a / ||a||
b_norm = b / ||b||

dot(a_norm, b_norm) = dot(a, b) / (||a|| * ||b||)  # This IS cosine!
```

So even though we switched to `np.dot()`, we were still getting cosine-like compressed scores because the embeddings were normalized.

### Solution: Unnormalized Embeddings + Dot Product

```python
# Unnormalized embeddings preserve magnitude
dot(a, b) = similarity × ||a|| × ||b||

# Higher magnitude = stronger semantic content
# Weighted topic vectors naturally produce proportional scores
```

This gives us the **expressive 0-9 range** needed for significance scoring.

## Calibration Note

The significance scoring in Cell 37 is calibrated for the **0.77 - 9.22 range** based on validation with workflow `slavery_Slavdict_pretraining_slavery_v25`.

If your data has a different range after re-running, you may need to adjust the magnitude normalization in Cell 37:

```python
# Current (calibrated for 2-9 range):
magnitude = (max_score - 2.0) / 7.0

# If your range is different, adjust:
# magnitude = (max_score - min_observed) / (max_observed - min_observed)
```

But this is unlikely to be needed - SBERT embeddings typically have similar magnitude ranges across corpora.

## Summary

1. ✅ **Fixed:** Cell 4 now has `normalize_embeddings=False`
2. ⏳ **Next:** Re-run Cell 4, 36, 37 to regenerate with unnormalized embeddings
3. ✅ **Verify:** Check that max_score is ~9.0, not ~0.6
4. ✅ **Validate:** Confirm CV detects noise and significance tiers make sense

Once re-run, you'll have the proper significance-based classification that filters noise via CV!
