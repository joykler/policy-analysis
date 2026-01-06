# Stratified Sampling Implementation for BERTJE Training

## What Was Added

I've added stratified sampling by confidence level to your notebook to fix BERTJE's score compression issue.

### Changes Made:

1. **New Config Option** (Cell 5 - CONFIG):
   ```python
   "training": {
       ...
       "apply_confidence_sampling": True,  # Enable/disable stratified sampling
       ...
   }
   ```

2. **New Cell 7.5b** (Inserted between data loading and dataset creation):
   - Applies stratified sampling to training data
   - Rebalances confidence level distribution
   - Filters none-confidence to only include BERTJE agreements

---

## How It Works

### Target Distribution:

```python
TARGET_DISTRIBUTION = {
    'high': 0.40,    # 40% high confidence (up from ~16%)
    'low': 0.40,     # 40% low confidence (down from ~44%)
    'none': 0.20     # 20% none confidence (down from ~40%)
}
```

### Sampling Strategy:

1. **High Confidence** (margin > 0.050):
   - **OVERSAMPLE** from 16% to 40% (with replacement)
   - These teach BERTJE to give high scores (70-90%)
   - These show what "absent topics" look like (0-5%)

2. **Low Confidence** (margin 0.025-0.050):
   - **MAINTAIN** at ~40%
   - These are genuine multi-topic chunks
   - Critical for policy document analysis

3. **None Confidence** (margin < 0.025):
   - **DOWNSAMPLE** from 40% to 20%
   - **FILTER**: Only include where `primary_topic == bertje_primary_topic`
   - Removes likely noise while keeping difficult multi-topic cases

---

## Expected Impact

### Problem It Fixes:

**Current BERTJE behavior**:
- Scores compressed in 20-45% range
- Can't reach 70%+ for dominant topics
- Can't reach 0-10% for absent topics

**Root cause**: 84% of training data has flat scores (low/none confidence)
- BERTJE learned: "Most chunks have flat scores"
- This is technically correct for the training distribution!

### After Stratified Sampling:

**Expected improvements**:
- High scores will reach 60-75% (vs current 35-48%)
- Low scores will reach 5-15% (vs current 20-30%)
- Better differentiation between topics
- Reduced false positives
- Multi-topic detection preserved (60% of training still multi-topic)

**Predicted accuracy**: 70-75% multi-label correlation (up from 60-65%)

---

## Usage

### Enable Sampling (Default):
```python
CONFIG["training"]["apply_confidence_sampling"] = True
```

Run the notebook normally. Cell 7.5b will:
1. Show original distribution
2. Apply stratified sampling
3. Show final distribution
4. Report sampling statistics

### Disable Sampling:
```python
CONFIG["training"]["apply_confidence_sampling"] = False
```

Uses all training data as-is (original behavior).

---

## What Gets Printed

When Cell 7.5b runs, you'll see:

```
Applying stratified sampling to reduce score compression bias...

Original distribution:
  high         605 ( 15.7%)
  low         1693 ( 43.9%)
  none        1556 ( 40.4%)

Total before sampling: 3854

  high: Sampled 1542 from 605 (upsampling with replacement)
  low: Sampled 1542 from 1693 (downsampling)
  none: 1556 available, 797 where BERTJE agrees
  none: Sampled 771 from 797 (downsampling)

After stratified sampling:
  high        1542 (40.0% - target 40%)
  low         1542 (40.0% - target 40%)
  none         771 (20.0% - target 20%)

Total after sampling: 3855

Stratified sampling applied successfully
  This should reduce score compression by increasing high-confidence examples.
```

---

## Technical Details

### Upsampling High Confidence:

Since there are only 605 high-confidence chunks but we need 1,542:
- Samples WITH REPLACEMENT from the 605
- Some chunks will appear 2-3 times in training
- This is standard practice for class imbalance
- BERTJE will see more examples of clear single-topic patterns

### Filtering None Confidence:

Only includes none-confidence chunks where BERTJE agrees with cosine (51% of none chunks):
- Agreement suggests there IS signal despite flat scores
- Disagreement suggests noise or mislabeling
- Reduces from 1,556 to ~797 none-confidence chunks

### No Impact on Validation:

Validation data is NOT sampled - uses original distribution
- Tests BERTJE on realistic data distribution
- Prevents overfitting to resampled training distribution

---

## Why This Is Better Than Other Approaches

### ❌ Don't: Exclude Low/None Confidence Entirely
- Would reduce data from 3,854 to 605 (-84%)
- Would only teach single-topic patterns
- Would make BERTJE bad at multi-topic documents

### ❌ Don't: Weight Loss Function
- More complex to implement
- Doesn't address data distribution imbalance
- Harder to debug

### ✓ Do: Stratified Sampling (This Approach)
- Maintains sample size (3,855 chunks)
- Teaches both single and multi-topic patterns
- Simple and interpretable
- Can be toggled on/off easily
- Addresses root cause (training distribution mismatch)

---

## Relationship to Your Research

From your semantic evaluation analysis:

**Current accuracy**: 30% exact, 65% reasonable

**Main issues identified**:
1. Score compression (biggest problem) ← **This fixes it**
2. SOCIAL topic weakness (cultural content) ← Needs better examples
3. False positives on absent topics ← **This helps**

**This implementation addresses issues #1 and #3 directly.**

For issue #2 (SOCIAL topic), you'll need to add/augment training examples with:
- Cultural identity content
- Collective memory
- Social welfare (not just discrimination/racism)

---

## Next Steps

1. **Run the notebook** with `apply_confidence_sampling=True`
2. **Train BERTJE** with the resampled data
3. **Evaluate** on your test set:
   - Check if scores now reach 70%+ for dominant topics
   - Check if scores now reach 0-10% for absent topics
   - Verify multi-topic detection is preserved

4. **Compare** to baseline:
   - Run once with `apply_confidence_sampling=False` (baseline)
   - Run once with `apply_confidence_sampling=True` (stratified)
   - Compare multi-label correlation metrics

5. **Tune if needed**:
   - Adjust TARGET_DISTRIBUTION ratios
   - Try 50/30/20 or 35/40/25 if needed
   - Current 40/40/20 is recommended starting point

---

## Expected Timeline for Improvement

- **Immediate**: Score ranges should widen in training metrics
- **After 1-2 epochs**: Validation scores should show less compression
- **After full training**: Multi-label correlation should improve from 60-65% to 70-75%

---

## Verification

After training with stratified sampling, check:

```python
# Load predictions
predictions = pd.read_csv('bertje_predictions.csv')

# Check score ranges
for topic in topics:
    scores = predictions[f'bertje_{topic}_score']
    print(f"{topic}:")
    print(f"  Range: {scores.min():.3f} - {scores.max():.3f}")
    print(f"  Std: {scores.std():.3f}")
    print(f"  Median: {scores.median():.3f}")

# Expected improvements:
# - Max scores should reach 0.65-0.80 (vs current 0.48)
# - Min scores should reach 0.05-0.15 (vs current 0.20)
# - Std should increase (more differentiation)
```

If you see wider ranges and higher max scores, stratified sampling is working!

---

## Summary

**What changed**: Added optional stratified sampling in Cell 7.5b

**Why**: Fix BERTJE's score compression (caused by 84% flat-score training data)

**How**: Oversample high-confidence (40%), maintain low-confidence (40%), downsample none-confidence (20%)

**Expected result**: Scores will use full 0-90% range instead of compressed 20-45% range

**Toggle**: Set `CONFIG["training"]["apply_confidence_sampling"]` to True/False

This should significantly improve BERTJE's multi-label correlation for your next finetuning phase! 🎯
