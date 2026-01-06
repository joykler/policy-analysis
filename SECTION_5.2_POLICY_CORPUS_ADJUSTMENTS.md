# Section 5.2 Adjustments for Policy Corpus

## Problem
Section 5.2 in `A__dictionary_discovery_v20_unified_embedding.ipynb` uses hardcoded thresholds designed for a slavery corpus with score range ~0.6-1.2. Your **Policy corpus** has a very different score distribution:

- **Score range**: 6.53 - 12.24 (range: 5.71)
- **Mean**: 10.53, **Std**: 0.93
- **CV**: mean 0.077, max 0.182 (much lower than expected)
- **Z-max**: mean 1.42, range 0.65-1.73

## Required Code Changes

### Change 1: Corpus Type Detection (Line ~285)

**Current:**
```python
if corpus_max < 10.0:
    corpus_type = "slavery"
    print(f"Detected corpus type: SLAVERY (low score range)")
else:
    corpus_type = "policy"
    print(f"Detected corpus type: POLICY (high score range)")
```

**Fix:**
```python
if corpus_max < 5.0:  # Changed from 10.0 to 5.0
    corpus_type = "slavery"
    print(f"Detected corpus type: SLAVERY (low score range)")
else:
    corpus_type = "policy"
    print(f"Detected corpus type: POLICY (high score range)")
```

**Reason**: Your policy max is 12.24, typical slavery max is ~1.2. Threshold of 10.0 is too high.

---

### Change 2: CV Normalization (Line ~326)

**Current:**
```python
cv = std_score / mean_score if mean_score > 0 else 0
differentiation = cv / 0.55  # Upper bound covers both corpora
differentiation = np.clip(differentiation, 0, 1)
```

**Fix:**
```python
cv = std_score / mean_score if mean_score > 0 else 0

# Corpus-specific CV normalization
if corpus_type == "slavery":
    cv_upper_bound = 0.55  # Slavery corpus has higher CV values
else:  # policy
    cv_upper_bound = 0.20  # Policy corpus has lower CV (max ~0.18)

differentiation = cv / cv_upper_bound
differentiation = np.clip(differentiation, 0, 1)
```

**Reason**: Policy corpus CV maxes out at 0.182. Using 0.55 means nothing reaches high differentiation scores.

---

### Change 3: Weak Signal Detection (Line ~320)

**Current:**
```python
# Weak-signal detection: Flag chunks in bottom 20% of corpus range
low_signal_threshold = 0.20  # 20% of corpus range
weak_signal = magnitude < low_signal_threshold
```

**Fix:**
```python
# Weak-signal detection: Corpus-specific thresholds
if corpus_type == "slavery":
    low_signal_threshold = 0.20  # 20% of corpus range
else:  # policy
    low_signal_threshold = 0.10  # 10% of corpus range (less aggressive)

weak_signal = magnitude < low_signal_threshold
```

**Reason**: In policy corpus, 20% threshold only flags 1.7% of data. Using 10% will flag ~10% (more reasonable for noise filtering).

**Alternative (more robust):** Use quantile-based thresholds instead of fixed percentages:
```python
# Calculate weak signal threshold from data (10th percentile)
q10_score = all_scores_df['max_score'].quantile(0.10)
low_signal_threshold_score = (q10_score - corpus_min) / corpus_range

# Per-chunk weak signal detection
weak_signal = magnitude < low_signal_threshold_score
```

---

### Change 4: Z-score Normalization (Line ~332)

**Current:**
```python
z_max = (max_score - mean_score) / std_score if std_score > 0 else 0
contrast = (z_max - 0.60) / 1.13  # Scale 0.60-1.73 to 0-1
contrast = np.clip(contrast, 0, 1)
```

**Fix:**
```python
z_max = (max_score - mean_score) / std_score if std_score > 0 else 0

# Corpus-specific Z-score normalization
if corpus_type == "slavery":
    z_min, z_range = 0.60, 1.13  # Original slavery corpus range
else:  # policy
    z_min, z_range = 0.65, 1.08  # Policy corpus range: 0.65-1.73

contrast = (z_max - z_min) / z_range
contrast = np.clip(contrast, 0, 1)
```

**Reason**: Policy corpus Z-max has min 0.65 (vs 0.60 in slavery). Small adjustment but more accurate.

---

## Implementation Strategy

### Option A: Modify Existing Function
Update the `calculate_significance` function (starting ~line 299) to include corpus-type conditional logic for all normalization parameters.

### Option B: Separate Functions
Create two separate functions:
- `calculate_significance_slavery()`
- `calculate_significance_policy()`

Call the appropriate one based on `corpus_type`.

---

## Expected Impact

After these changes, for your **Policy corpus** you should see:

1. **Correct detection**: "Detected corpus type: POLICY (high score range)"
2. **Higher differentiation scores**: CV values will be normalized by 0.20 instead of 0.55, making chunks with CV > 0.10 score higher
3. **More balanced weak signal filtering**: ~10% of chunks flagged instead of 1.7%
4. **Slightly adjusted contrast scores**: Better aligned with your Z-max distribution

This will lead to:
- **More chunks in high_significance** (because CV normalization will be appropriate)
- **Better noise filtering** (10% vs 1.7%)
- **More accurate significance scores** overall

---

## Testing After Changes

Run this to verify the changes work:

```python
# After running modified Section 5.2
print(f"Corpus type detected: {corpus_type}")
print(f"\nCV normalization bound: {cv_upper_bound if 'cv_upper_bound' in locals() else 'NOT SET'}")
print(f"Weak signal threshold: {low_signal_threshold:.3f}")

# Check distribution shifts
print("\nSignificance category counts:")
print(all_scores_df['significance_category'].value_counts())
print(f"\nHigh significance: {(all_scores_df['significance_category'] == 'high_significance').sum() / len(all_scores_df) * 100:.1f}%")
```

---

## Summary

The core issue is that **Policy corpus has ~10x higher scores but lower CV variance** than Slavery corpus. The fixed thresholds need to become **corpus-adaptive** to properly classify both types of data.

**Priority order of changes:**
1. **Corpus detection** (line 285) - CRITICAL
2. **CV normalization** (line 326) - HIGH IMPACT
3. **Weak signal threshold** (line 320) - MEDIUM IMPACT
4. **Z-score normalization** (line 332) - LOW IMPACT (already close)
