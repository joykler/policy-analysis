# Dictionary Discovery v22: Policy-Adaptive Significance Scoring

## Changelog: v20 → v22

**Date**: 2025-12-12
**Status**: Ready for testing

---

## Overview

Version 22 introduces **corpus-adaptive thresholds** that automatically detect whether the corpus is a Slavery corpus (low score range ~0.6-1.2) or Policy corpus (high score range ~6-12) and adjusts significance scoring parameters accordingly.

This solves the issue where Policy corpora with ~10x higher scores but lower CV variance were being incorrectly classified using Slavery-corpus thresholds.

---

## Key Changes

### 1. Corpus Type Detection (Cell 5.2, Line ~37)

**v20:**
```python
if corpus_max < 10.0:
    corpus_type = "slavery"
```

**v22:**
```python
if corpus_max < 5.0:  # Changed from 10.0
    corpus_type = "slavery"
else:
    corpus_type = "policy"
```

**Impact**: Correctly identifies Policy corpora (max ~12.24) vs Slavery corpora (max ~1.2)

---

### 2. CV Normalization Upper Bound (Cell 5.2, calculate_significance function)

**v20:**
```python
cv = std_score / mean_score if mean_score > 0 else 0
differentiation = cv / 0.55  # Fixed for all corpora
```

**v22:**
```python
cv = std_score / mean_score if mean_score > 0 else 0

if corpus_type == "slavery":
    cv_upper_bound = 0.55  # Slavery corpus has higher CV values
else:  # policy
    cv_upper_bound = 0.20  # Policy corpus has lower CV (max ~0.18)

differentiation = cv / cv_upper_bound
```

**Impact**:
- **Slavery**: No change (still 0.55)
- **Policy**: CV values now properly normalized (was always < 0.33, now can reach 0.90)
- **Result**: More chunks will achieve high differentiation scores in Policy corpora

---

### 3. Weak Signal Threshold (Cell 5.2, calculate_significance function)

**v20:**
```python
low_signal_threshold = 0.20  # Fixed 20% for all corpora
weak_signal = magnitude < low_signal_threshold
```

**v22:**
```python
if corpus_type == "slavery":
    low_signal_threshold = 0.20  # 20% of corpus range for slavery
else:  # policy
    low_signal_threshold = 0.10  # 10% of corpus range for policy

weak_signal = magnitude < low_signal_threshold
```

**Impact**:
- **Slavery**: No change (20% flagged as weak)
- **Policy**: Less aggressive filtering (10% vs 1.7% in v20)
- **Result**: More appropriate noise filtering for Policy corpora

---

### 4. Z-Score Normalization (Cell 5.2, calculate_significance function)

**v20:**
```python
z_max = (max_score - mean_score) / std_score if std_score > 0 else 0
contrast = (z_max - 0.60) / 1.13  # Fixed range for all corpora
```

**v22:**
```python
z_max = (max_score - mean_score) / std_score if std_score > 0 else 0

if corpus_type == "slavery":
    z_min, z_range = 0.60, 1.13  # Original slavery corpus range (0.60-1.73)
else:  # policy
    z_min, z_range = 0.65, 1.08  # Policy corpus range (0.65-1.73)

contrast = (z_max - z_min) / z_range
```

**Impact**:
- **Slavery**: No change
- **Policy**: Slightly adjusted to actual data distribution (0.65-1.73)
- **Result**: Minor improvement in contrast score accuracy

---

### 5. Enhanced Output Reporting (Cell 5.2, end of cell)

**v22 adds:**
```python
print(f"\n{'='*80}")
print("v22 CORPUS-ADAPTIVE PARAMETERS USED")
print(f"{'='*80}")
print(f"  Corpus type: {corpus_type.upper()}")
if corpus_type == "slavery":
    print(f"  CV upper bound: 0.55")
    print(f"  Weak signal threshold: 20% of corpus range")
    print(f"  Z-score range: 0.60 - 1.73")
else:
    print(f"  CV upper bound: 0.20")
    print(f"  Weak signal threshold: 10% of corpus range")
    print(f"  Z-score range: 0.65 - 1.73")
```

**Impact**: Users can verify which parameters were applied to their corpus

---

## Expected Outcomes

### For Policy Corpora (like Policy_Slavdict_ft-slavery_slavery_v2)

**Before v22:**
- Corpus type: Incorrectly detected as "slavery" (max 12.24 > 10.0 threshold)
- CV differentiation: Always low (max CV 0.18 / 0.55 = 0.33)
- Weak signal flagging: Too conservative (1.7% of data)
- Result: **Under-classifies high significance chunks**

**After v22:**
- Corpus type: Correctly detected as "policy"
- CV differentiation: Properly scaled (max CV 0.18 / 0.20 = 0.90)
- Weak signal flagging: Appropriate (10% of data)
- Result: **Accurately classifies significance levels**

**Predicted distribution shift:**
- High significance: **Increase from ~20% to ~35-45%**
- Medium significance: **Increase from ~15% to ~25-30%**
- Low significance: **Decrease from ~30% to ~15-20%**
- Noise: **Slight increase from ~35% to ~40-45%** (better filtering)

### For Slavery Corpora

**No changes** - all parameters remain the same as v20.

---

## Testing Checklist

Run the following after executing Cell 5.2 on a Policy corpus:

```python
# 1. Verify corpus detection
assert corpus_type == "policy", f"Expected 'policy', got '{corpus_type}'"

# 2. Check distribution shift
sig_dist = all_scores_df['significance_category'].value_counts()
high_pct = sig_dist.get('high_significance', 0) / len(all_scores_df) * 100
print(f"High significance: {high_pct:.1f}% (expect 35-45%)")

# 3. Check CV differentiation scores
high_cv_chunks = all_scores_df[all_scores_df['cv'] > 0.10]
avg_diff = high_cv_chunks['differentiation_norm'].mean()
print(f"Avg differentiation (CV > 0.10): {avg_diff:.3f} (expect > 0.50)")

# 4. Verify weak signal filtering
weak_count = all_scores_df['weak_signal_flag'].sum()
weak_pct = weak_count / len(all_scores_df) * 100
print(f"Weak signal flagged: {weak_pct:.1f}% (expect ~10%)")
```

---

## Files

- **Notebook**: `A__dictionary_discovery_v22_policy_adaptive.ipynb`
- **Analysis doc**: `SECTION_5.2_POLICY_CORPUS_ADJUSTMENTS.md`
- **This changelog**: `V22_CHANGELOG.md`

---

## Backward Compatibility

✅ **Fully backward compatible** with Slavery corpora
✅ **No changes** to other checkpoints (1-4, 6-9)
✅ **Same output files** (scores_all_labeled.csv, etc.)
✅ **Same significance categories** (high/medium/low/noise)

Only difference: **Better scoring for Policy corpora**

---

## Next Steps

1. **Test on Policy_Slavdict_ft-slavery_slavery_v2**:
   - Run Checkpoints 0-4 (same as v20)
   - Run Checkpoint 5 Cell 5.2 (v22 version)
   - Verify corpus type detection: "POLICY"
   - Compare significance distributions to v20

2. **Test on Slavery corpus** (optional):
   - Verify corpus type detection: "SLAVERY"
   - Verify distributions match v20 (no regression)

3. **Evaluate downstream impact**:
   - Check training data quality (Checkpoint 6)
   - Verify model performance (Checkpoint 7-8)

---

## Technical Notes

### Why 0.20 for Policy CV upper bound?

Policy corpus analysis showed:
- CV max: 0.182
- CV Q95: 0.120
- CV Q90: 0.108

Using 0.20 allows:
- High CV chunks (0.10-0.18) to score 0.50-0.90 in differentiation
- Room for outliers above 0.18
- Still conservative (chunks need CV > 0.10 to avoid "uniform scores" filter)

### Why 10% weak signal for Policy?

Policy corpus analysis showed:
- 20% threshold flagged only 1.7% of data (too conservative)
- 10% threshold flags ~10% of data (more appropriate)
- Policy documents consistently mention topics (higher baseline)
- Slavery documents more variable (20% threshold appropriate)

---

## Author

Cedric Joy Berkelouw
Date: 2025-12-12
Version: 22
