# BERTJE TRAINING RECOMMENDATION - V21 Dataset
**Multi-Label Regression Perspective**

**Date:** 2025-11-28
**Status:** ✅ **PROCEED WITH TRAINING**

---

## EXECUTIVE SUMMARY

### ✅ YES - Dataset is sufficient for BERTJE multi-label regression training

**Key Corrections from Initial Analysis:**
- ❌ I initially evaluated as single-label classification (wrong approach)
- ✅ Correct approach: Multi-label regression predicting 4 continuous scores (0-2.0)
- ✅ From this perspective, the data provides adequate training signal

---

## DATA OVERVIEW

**Total chunks:** 1,520
**Usable for training (score ≥0.5):** ~1,186 chunks

### Training Examples Per Topic:

| Topic | High (≥1.0) | Moderate (0.5-1.0) | Low (<0.5) | Very High (≥1.5) |
|-------|-------------|-------------------|-----------|------------------|
| **Educational** | 59 | 291 | 1170 | 7 ✅ |
| **Governance** | 46 | 678 | 796 | **0** ❌ |
| **Poverty** | 31 | 621 | 868 | **2** ❌ |
| **Racism** | 126 | 776 | 618 | 3 ⚠️ |

---

## CRITICAL FINDING: Score Compression

**After rescaling, maximum observed scores are:**
- Educational: 2.00 ✅ (reaches full range)
- Governance: **1.38** ❌ (compressed)
- Poverty: **1.64** ⚠️ (barely reaches high range)
- Racism: **1.53** ⚠️ (barely reaches high range)

**Impact:** Model will learn compressed score ranges, especially for Governance

---

## WHAT THE MODEL WILL LEARN

### ✅ Model WILL Learn Well:
1. **Presence vs Absence** - plenty of low/high score examples
2. **Relative topic strength** - which topic is stronger in a chunk
3. **Weak vs Moderate presence** - good variety of mid-range scores
4. **Multi-topic patterns** - 32 chunks have 2+ topics ≥1.0

### ⚠️ Model Will Learn with Limitations:
1. **Governance scores capped at ~1.3** - no training examples >1.38
2. **Poverty scores rarely >1.5** - only 2 training examples
3. **Very strong presence** - limited examples of scores ≥1.5

### Expected Prediction Ranges After Training:
```
Educational: 0.0 - 1.8 (good range)
Governance:  0.0 - 1.2 (compressed)
Poverty:     0.0 - 1.4 (slightly compressed)
Racism:      0.0 - 1.4 (slightly compressed)
```

**This is acceptable** for ranking and filtering purposes.

---

## RECOMMENDED TRAINING APPROACH

### Model Architecture

```python
# Multi-label regression
Input: Dutch text (BERTJE tokenization)
Output: 4 continuous scores [edu, gov, pov, rac] ∈ [0, 2.0]
Loss: MSE or Huber Loss
```

### Training Data Selection

**Option A - Conservative (Recommended for initial training):**
```python
# Use chunks with max_score ≥ 1.0
train_data = df[df['max_rescaled'] >= 1.0]  # ~226 chunks
# Benefits: Higher quality, clearer signals
# Drawback: Smaller dataset
```

**Option B - Inclusive (Better coverage):**
```python
# Use chunks with max_score ≥ 0.5
train_data = df[df['max_rescaled'] >= 0.5]  # ~1,186 chunks
# Benefits: More training data, better coverage of moderate scores
# Drawback: Noisier weak signals
```

**Recommended:** Start with Option B, use Option A for validation

### Sampling Strategy

**Topic Balancing:**
```python
topic_weights = {
    'Educational': 2.5,  # Oversample minority (151 → ~377 effective)
    'Governance': 1.0,   # Standard (373 → 373 effective)
    'Poverty': 1.4,      # Moderate oversample (268 → ~375 effective)
    'Racism': 0.5,       # Undersample majority (728 → ~364 effective)
}
```

**Score-Based Weighting:**
```python
# Boost rare high scores to help model learn full range
def sample_weight(max_score):
    if max_score >= 1.5: return 3.0   # Very high - rare, boost heavily
    if max_score >= 1.0: return 2.0   # High - moderate boost
    if max_score >= 0.5: return 1.0   # Moderate - standard weight
    return 0.3                        # Weak - downweight
```

### Loss Function

```python
import torch
import torch.nn as nn

# Weighted MSE with per-topic and per-sample weights
class WeightedMSELoss(nn.Module):
    def forward(self, pred, target, sample_weights, topic_weights):
        # pred, target: [batch, 4] (4 topics)
        # sample_weights: [batch]
        # topic_weights: [4]

        squared_errors = (pred - target) ** 2  # [batch, 4]
        weighted = squared_errors * topic_weights  # [batch, 4]
        sample_weighted = weighted * sample_weights.unsqueeze(1)  # [batch, 4]
        return sample_weighted.mean()
```

---

## TRAINING CONFIGURATION

### Hyperparameters

```python
model = BertjeForRegression(num_labels=4, output_range=(0.0, 2.0))

training_args = {
    'learning_rate': 2e-5,
    'batch_size': 16,
    'epochs': 5,
    'warmup_steps': 100,
    'weight_decay': 0.01,
    'max_seq_length': 512,
}

# Sample weighting
sample_weights = compute_sample_weights(
    df,
    topic_weights={'Educational': 2.5, 'Governance': 1.0, 'Poverty': 1.4, 'Racism': 0.5},
    score_boost={1.5: 3.0, 1.0: 2.0, 0.5: 1.0}
)
```

### Data Splits

```python
# Stratified split maintaining topic balance
train_df, val_df = stratified_split(
    df,
    test_size=0.15,
    stratify_col='primary_topic_rescaled'
)

# ~1,006 train, ~180 validation
```

---

## EXPECTED PERFORMANCE

### Realistic Expectations:

**Correlation with ground truth scores:**
- Educational: r = 0.75 - 0.85 (good)
- Governance: r = 0.65 - 0.75 (moderate, due to compression)
- Poverty: r = 0.65 - 0.75 (moderate, few high examples)
- Racism: r = 0.70 - 0.80 (good)

**MSE per topic:**
- Educational: 0.15 - 0.25
- Governance: 0.20 - 0.30 (higher due to compression)
- Poverty: 0.20 - 0.30
- Racism: 0.15 - 0.25

**Ranking Performance:**
- Excellent at identifying which topic is strongest
- Good at separating relevant (≥0.5) vs irrelevant (<0.5)
- Moderate at distinguishing high (1.0-1.5) vs very high (≥1.5)

---

## OPTIONAL IMPROVEMENTS

### If Time Permits (4-8 hours):

**1. Augment Governance High-Score Examples:**
- Manually review Governance chunks scoring 1.2-1.38
- Identify 20 truly strong governance chunks
- Relabel these as 1.6-2.0 for training
- **Benefit:** Expands Governance prediction range

**2. Augment Poverty High-Score Examples:**
- Find 20 chunks with clear strong poverty content
- Manually assign scores 1.5-2.0
- **Benefit:** Better learning of strong poverty signals

**3. Filter Extreme Boilerplate:**
- Remove pure table of contents chunks
- Remove parliamentary motion lists (sentence count <5)
- **Benefit:** Reduces noise, ~50-100 chunks removed

**Impact:** Would improve model quality by ~5-10%, but NOT required for functionality

---

## EVALUATION STRATEGY

### Validation Metrics:

```python
# 1. Per-topic MSE
mse_per_topic = ((pred - actual) ** 2).mean(axis=0)

# 2. Per-topic correlation
corr_per_topic = [pearsonr(pred[:, i], actual[:, i]) for i in range(4)]

# 3. Ranking accuracy (is top-scored topic correct?)
ranking_acc = (pred.argmax(axis=1) == actual.argmax(axis=1)).mean()

# 4. Threshold-based F1 (score ≥ 1.0 = relevant)
for threshold in [0.5, 1.0, 1.5]:
    pred_binary = (pred >= threshold)
    actual_binary = (actual >= threshold)
    f1 = f1_score(actual_binary, pred_binary, average='macro')
```

### Expected Validation Results:

| Metric | Target | Acceptable |
|--------|--------|------------|
| Overall MSE | <0.20 | <0.30 |
| Ranking Accuracy | >75% | >65% |
| F1 @ threshold 1.0 | >0.70 | >0.60 |
| Correlation (avg) | >0.75 | >0.65 |

---

## DEPLOYMENT CONSIDERATIONS

### Score Interpretation Guide:

```
For each topic, the model predicts a score 0.0 - 2.0:

0.0 - 0.5:  Topic is ABSENT or barely mentioned
0.5 - 1.0:  Topic is WEAKLY present (peripheral mention)
1.0 - 1.5:  Topic is CLEARLY present (substantive discussion)
1.5 - 2.0:  Topic is STRONGLY present (central theme)

Special cases due to training data limitations:
- Governance scores rarely exceed 1.2 (compressed range)
- Poverty scores rarely exceed 1.4 (limited high examples)
```

### Use Cases:

**✅ Good for:**
- Filtering documents by topic relevance (threshold ≥0.5 or ≥1.0)
- Ranking documents by topic strength
- Identifying multi-topic documents
- Relative comparison between topics in same document

**⚠️ Limited for:**
- Distinguishing "very strong" (1.5-2.0) from "strong" (1.0-1.5) for Gov/Pov
- Absolute score calibration (use relative scores instead)

**❌ Not suitable for:**
- Fine-grained severity assessment (Gov/Pov only have 2-3 very high examples)
- Expecting full 0-2.0 range utilization for all topics

---

## RISK MITIGATION

### Identified Risks & Mitigations:

**1. Score Compression (Gov/Pov)**
- **Risk:** Model never predicts Gov >1.3, Pov >1.5
- **Mitigation:** Document limitation, accept compressed range, focus on ranking
- **Impact:** Medium - affects absolute scores but not relative ordering

**2. Topic Imbalance**
- **Risk:** Model biased toward Racism (48% of data)
- **Mitigation:** Apply topic balancing weights (Racism 0.5x, Educational 2.5x)
- **Impact:** Low - addressed by sampling strategy

**3. Boilerplate Administrative Text**
- **Risk:** Model learns to score administrative text higher
- **Mitigation:** This is actually OK - administrative education text IS about education
- **Impact:** Low - acceptable differentiation

**4. Limited Very-High Examples**
- **Risk:** Model doesn't learn what "very strong" looks like for Gov/Pov
- **Mitigation:** Accept limitation or manually augment (optional 4-8 hours)
- **Impact:** Medium - limits score range but doesn't break ranking

---

## FINAL RECOMMENDATION

### ✅ **PROCEED WITH TRAINING**

**Recommended Timeline:**

1. **Setup (2 hours):**
   - Prepare training data from V21 dataset
   - Implement multi-label regression architecture
   - Configure weighted sampling

2. **Training (4-8 hours compute):**
   - Train BERTJE model with configuration above
   - Monitor validation metrics
   - Tune hyperparameters if needed

3. **Evaluation (2 hours):**
   - Calculate correlation, MSE, ranking accuracy
   - Analyze per-topic performance
   - Document score compression for Gov/Pov

4. **Optional Enhancement (4-8 hours):**
   - Manual augmentation of Gov/Pov high-score examples
   - Retrain with augmented data
   - Compare performance improvement

**Total Time:** 8-10 hours (basic), 12-18 hours (with enhancements)

### Expected Outcome:

**A working multi-label regression model that:**
- ✅ Accurately detects topic presence/absence
- ✅ Ranks chunks by topic relevance well
- ✅ Handles multi-topic documents appropriately
- ⚠️ Has compressed score ranges for Governance/Poverty
- ⚠️ Performs moderately well (not state-of-art, but usable)

**This is sufficient for:**
- Document filtering and ranking
- Topic-based corpus exploration
- Multi-label topic detection
- Relative strength comparison

**This is NOT sufficient for:**
- High-precision classification
- Fine-grained severity assessment
- Production-critical applications
- Publishing academic benchmarks

---

## CONCLUSION

The V21 dataset **IS sufficient** for training a BERTJE multi-label regression model, with the understanding that:

1. **Score compression exists** for Governance/Poverty (accept this limitation)
2. **Model will work well for ranking and filtering** (primary use case)
3. **Optional enhancements can improve quality** but aren't required
4. **Realistic expectations** about performance are essential

**Recommendation: START TRAINING with configuration above.**

Document limitations clearly, and decide on optional enhancements based on initial model performance.
