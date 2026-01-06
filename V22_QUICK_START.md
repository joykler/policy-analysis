# Quick Start: Dictionary Discovery v22

## What Changed?

**v22 makes Section 5.2 (Significance Scoring) adaptive to your corpus type.**

Previously, the code assumed all corpora had low scores (0.6-1.2 range, like Slavery corpora). Your **Policy corpus** has high scores (6-12 range), causing incorrect significance classifications.

v22 **automatically detects** corpus type and adjusts thresholds accordingly.

---

## How to Use v22

### Option 1: Start Fresh

```python
# Open the new notebook
# A__dictionary_discovery_v22_policy_adaptive.ipynb

# Run Checkpoints 0-5 as normal
# No configuration changes needed - it auto-detects!
```

### Option 2: Replace Just Section 5.2

If you already ran Checkpoints 0-4 in v20:

1. Open `A__dictionary_discovery_v22_policy_adaptive.ipynb`
2. Copy Cell 37 (Section 5.2)
3. Paste into your existing v20 notebook
4. Run the updated Cell 5.2

---

## What to Expect

### For Policy Corpus (scores 6-12 range)

**Output will show:**
```
Detected corpus type: POLICY (high score range, max >= 5.0)
...
v22 CORPUS-ADAPTIVE PARAMETERS USED
  Corpus type: POLICY
  CV upper bound: 0.20
  Weak signal threshold: 10% of corpus range
  Z-score range: 0.65 - 1.73
```

**Expected significance distribution:**
- High significance: **35-45%** (was ~20% in v20)
- Medium significance: **25-30%** (was ~15% in v20)
- Low significance: **15-20%** (was ~30% in v20)
- Noise: **40-45%** (was ~35% in v20)

### For Slavery Corpus (scores 0.6-1.2 range)

**Output will show:**
```
Detected corpus type: SLAVERY (low score range, max < 5.0)
...
v22 CORPUS-ADAPTIVE PARAMETERS USED
  Corpus type: SLAVERY
  CV upper bound: 0.55
  Weak signal threshold: 20% of corpus range
  Z-score range: 0.60 - 1.73
```

**No changes** - same as v20.

---

## Quick Validation

After running Cell 5.2, check:

```python
# 1. Corpus type detected correctly?
print(f"Corpus type: {corpus_type}")  # Should be "policy" or "slavery"

# 2. Distribution looks reasonable?
print(all_scores_df['significance_category'].value_counts(normalize=True))

# 3. High-CV chunks getting high differentiation scores?
high_cv = all_scores_df[all_scores_df['cv'] > 0.10]
print(f"Avg differentiation (CV > 0.10): {high_cv['differentiation_norm'].mean():.3f}")
# Should be > 0.50 for policy corpus
```

---

## Files Created

1. **A__dictionary_discovery_v22_policy_adaptive.ipynb** - The updated notebook
2. **SECTION_5.2_POLICY_CORPUS_ADJUSTMENTS.md** - Detailed technical analysis
3. **V22_CHANGELOG.md** - Complete changelog with code comparisons
4. **V22_QUICK_START.md** - This file

---

## Backward Compatibility

✅ Works with Slavery corpora (no changes)
✅ Same output file structure
✅ Same significance categories
✅ No changes to Checkpoints 1-4, 6-9

---

## Need Help?

**Issue**: Still seeing "Detected corpus type: SLAVERY" for Policy corpus?
- Check `corpus_max` value in output
- Should be > 5.0 for Policy (typically 10-15)
- If < 5.0, your corpus may actually be a Slavery corpus

**Issue**: Getting too many/few high significance chunks?
- This is expected with v22 - Policy corpora should have more
- Check CV distribution: `all_scores_df['cv'].describe()`
- High CV (> 0.10) = good differentiation = high significance

**Issue**: Want to adjust thresholds manually?
- Edit `cv_upper_bound` values in Cell 5.2
- Edit `low_signal_threshold` values
- See `SECTION_5.2_POLICY_CORPUS_ADJUSTMENTS.md` for guidance

---

## Next Steps

1. Run v22 on your Policy corpus
2. Compare significance distributions to v20
3. Proceed with Checkpoint 6 (Training Data Preparation)
4. Evaluate if training data quality improved

Happy coding! 🚀
