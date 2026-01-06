# Checkpoint 6 Changes - Alignment with New Dot Product Scores

## Date: 2025-12-04

## Overview
Updated Checkpoint 6 (Training Data Preparation) and Checkpoint 8 (BERTJE Predictions) to align with the new dot product scoring system that uses wider score ranges instead of compressed 0-1 cosine similarity.

## Problem Found

### Cell 44 - Training Data Distribution Table
**Issue:** Hardcoded threshold of `0.4` used to count "high relevance" chunks:
```python
# OLD CODE (lines 186, 190, 210, 214)
train_count = (train_opt4[score_col] >= 0.4).sum()  # ❌ Assumes 0-1 range
```

This threshold was designed for the old cosine similarity range (0-1). With dot product scores (0-200+), a threshold of 0.4 would incorrectly classify almost all chunks as "high relevance".

### Cell 69 - BERTJE Prediction Classification
**Issue:** Hardcoded thresholds from old rescaled 0-2 system:
```python
# OLD CODE (lines 51-60, 87-100)
if score < 0.25: return 0    # Noise
elif score < 0.50: return 1  # Context
elif score < 1.00: return 2  # Weak
elif score < 1.50: return 3  # Moderate
else: return 4               # Core
```

These thresholds were calibrated for the artificial 0-2 rescaled range. With raw dot product scores, these would misclassify everything.

## Solutions Implemented

### Cell 44 - Dynamic Percentile-Based Threshold

**Changed to calculate threshold from actual score distribution:**

```python
# NEW CODE
# Calculate dynamic threshold (use P75 across all topics as baseline)
all_scores = pd.concat([train_opt4[score_cols].stack(), val_opt4[score_cols].stack()])
score_median = all_scores.median()
score_p75 = all_scores.quantile(0.75)

# Use P75 as "high relevance" threshold
relevance_threshold = score_p75

print(f"Using P75 as 'high relevance' threshold: {relevance_threshold:.2f}")

# Count chunks above this adaptive threshold
train_count = (train_opt4[score_col] >= relevance_threshold).sum()
```

**Benefits:**
- ✅ Automatically adapts to actual score distribution
- ✅ Works with any score range (0.07-0.65 OR 5-200)
- ✅ Consistent definition of "high relevance" (top 25%)
- ✅ Self-documenting (shows the threshold value)

### Cell 69 - Percentile-Based BERTJE Classification

**Changed to calculate thresholds from BERTJE prediction distribution:**

```python
# NEW CODE
# Calculate percentile-based thresholds from actual predictions
all_bertje_scores = topic_scores.flatten()
p95 = np.percentile(all_bertje_scores, 95)
p75 = np.percentile(all_bertje_scores, 75)
p50 = np.percentile(all_bertje_scores, 50)
p25 = np.percentile(all_bertje_scores, 25)
p10 = np.percentile(all_bertje_scores, 10)

print(f"BERTJE score distribution percentiles:")
print(f"  P95 (top 5%):     {p95:.2f}")
print(f"  P75 (top 25%):    {p75:.2f}")
print(f"  P50 (median):     {p50:.2f}")
print(f"  P25 (bottom 75%): {p25:.2f}")
print(f"  P10 (bottom 10%): {p10:.2f}")

def score_to_ordinal(score):
    """Convert score to ordinal class based on percentiles."""
    if score >= p75:
        return 4  # Core (top 25%)
    elif score >= p50:
        return 3  # Moderate (above median)
    elif score >= p25:
        return 2  # Weak (above bottom quartile)
    elif score >= p10:
        return 1  # Context (bottom quartile but not noise)
    else:
        return 0  # Noise (bottom 10%)
```

**Also updated confidence assignment:**

```python
# Calculate margin percentiles too
margin_p75 = np.percentile(all_margins, 75)
margin_p50 = np.percentile(all_margins, 50)
margin_p25 = np.percentile(all_margins, 25)

def assign_confidence(row):
    score = row['bertje_primary_score']
    margin = row['bertje_margin']

    # Core: top 25% score AND high margin
    if score >= p75 and margin >= margin_p75:
        return 'core'
    # Moderate: above median score AND decent margin
    elif score >= p50 and margin >= margin_p25:
        return 'moderate'
    # Weak: above bottom quartile
    elif score >= p25:
        return 'weak'
    # Context: above noise threshold
    elif score >= p10:
        return 'context'
    # Noise: bottom 10%
    else:
        return 'noise'
```

**Benefits:**
- ✅ Adapts to BERTJE model's actual prediction distribution
- ✅ Works regardless of whether model was trained on cosine or dot product scores
- ✅ Consistent tier definitions across different runs
- ✅ Shows percentile thresholds for transparency

## Files Modified

1. **Cell 44** (lines 169-230) - Training data distribution table
   - Replaced hardcoded `>= 0.4` with dynamic `>= score_p75`
   - Added score distribution statistics output
   - Updated column names and descriptions

2. **Cell 69** (lines 43-112) - BERTJE prediction classification
   - Replaced hardcoded thresholds with percentile-based
   - Added percentile calculation and reporting
   - Updated both ordinal classification and confidence assignment

## Expected Behavior

### Cell 44 Output Example

**Old system (cosine 0-1 range):**
```
Using P75 as 'high relevance' threshold: 0.42

Topic                          Train_High  Train_Mean  Val_High  Val_Mean
Persistent_Poverty             1234        0.38        245       0.37
Social_Fragmentation           987         0.35        198       0.34
```

**New system (dot product 0-200 range):**
```
Using P75 as 'high relevance' threshold: 67.34

Topic                          Train_High  Train_Mean  Val_High  Val_Mean
Persistent_Poverty             1234        45.23       245       44.89
Social_Fragmentation           987         38.67       198       37.92
```

### Cell 69 Output Example

**Old system:**
```
BERTJE score distribution percentiles:
  P95 (top 5%):     0.89
  P75 (top 25%):    0.72
  P50 (median):     0.51
  P25 (bottom 75%): 0.33
  P10 (bottom 10%): 0.18
```

**New system:**
```
BERTJE score distribution percentiles:
  P95 (top 5%):     142.56
  P75 (top 25%):    98.23
  P50 (median):     56.78
  P25 (bottom 75%): 34.12
  P10 (bottom 10%): 12.45
```

## Compatibility Notes

### Training Data CSVs
The saved training/validation CSV files contain the same columns as before:
- `score_Topic_Name` (updated from `cos_Topic_Name`)
- `text`, `label`, `label_id`, `is_pseudo`
- All metadata columns preserved

### BERTJE Predictions
The BERTJE prediction output includes:
- `bertje_Topic_score` - continuous scores (raw model output)
- `bertje_Topic_class` - ordinal classes (0-4, percentile-based)
- `bertje_confidence` - tier labels (noise/context/weak/moderate/core)
- `bertje_primary_topic`, `bertje_max_score`, `bertje_margin`

## Testing Checklist

After running the updated cells:

### Cell 44 Testing
- [ ] Check that `relevance_threshold` is printed and reasonable (not 0.4)
- [ ] Verify `Train_Mean` scores match your actual distribution (not 0.3-0.7)
- [ ] Ensure "high relevance" counts make sense (should be ~25% of chunks)
- [ ] Check that different topics show varying mean scores

### Cell 69 Testing
- [ ] Verify percentile thresholds are printed (P10, P25, P50, P75, P95)
- [ ] Check that percentiles match your score range (not 0-1)
- [ ] Ensure confidence tiers have reasonable distribution:
  - Core: ~5-10% of chunks
  - Moderate: ~15-25% of chunks
  - Weak: ~25-35% of chunks
  - Context: ~25-35% of chunks
  - Noise: ~10-15% of chunks

## Additional Changes Made

Beyond the main threshold fixes, also updated:

1. **Column name references** in comments from "cosine" to "score"
2. **Print statements** to reflect dot product scoring
3. **Added statistics output** showing:
   - Calculated thresholds
   - Percentile distributions
   - Mean and standard deviation by topic

## Rollback Instructions

If you need to revert these changes:

1. Restore from backup:
   ```bash
   cp A__dictionary_discovery_v19_unified_embedding.ipynb.backup A__dictionary_discovery_v19_unified_embedding.ipynb
   ```

2. Or manually revert cells 44 and 69 using version control

## Questions / Issues?

If the percentile-based thresholds don't work well:

1. **Check score distribution first:**
   ```python
   print(all_scores_df['max_score'].describe())
   ```

2. **Verify embeddings are unnormalized:**
   ```python
   test_emb = st_model.encode(["test"], normalize_embeddings=False)[0]
   print(f"Norm: {np.linalg.norm(test_emb)}")  # Should be 20-30, not ~1.0
   ```

3. **Adjust percentile choices if needed:**
   - Currently using P75 for "high relevance"
   - Can change to P80 (stricter) or P70 (more lenient)
   - Just change `quantile(0.75)` to desired percentile

## Related Documentation

- [SCORING_CHANGES_SUMMARY.md](SCORING_CHANGES_SUMMARY.md) - Main scoring system changes
- [verify_scoring_changes.py](verify_scoring_changes.py) - Verification script
