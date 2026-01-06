# Training Analysis - Epoch 5 Results

**Date**: 2025-12-09
**Model**: BERTje Continuous Multi-Label Regression
**Training**: 5 epochs completed

---

## Results Summary

### ✓ **GOOD NEWS**
- **Pearson Correlation: 0.87** - Model IS learning patterns!
- 73.8% of chunks have Pearson > 0.85 (excellent pattern match)
- Top-2 overlap: 83.8% (model captures multi-label correctly)

### ⚠️ **PROBLEMS**
- **Euclidean Distance: 3.15** (target: <1.0) - Predictions off by ~3 points on average
- **CV Correlation: 0.38** (target: >0.75) - Not learning differentiation well
- **Pairwise Error: 1.30** (target: <0.5) - Relative strengths off
- **Global MAE: 1.18** (target: <0.8) - Magnitude errors too high

### ❌ **CRITICAL ISSUES**
- **Negative R² values** on 3/4 topics (Governance: -1.78, Economic: -1.98, Racism: -3.06)
- **Negative R² means**: Model predictions WORSE than just predicting the mean!

---

## What's Happening?

### Pattern Learning: ✓ WORKING
The **Pearson correlation of 0.87** means:
- Model understands which chunks are Educational vs Governance vs Economic vs Racism
- Captures the **shape** of multi-topic combinations
- 74% of chunks have excellent pattern match (>0.85)

**This is GOOD!** The model learned the semantic patterns.

### Magnitude Scaling: ❌ BROKEN
The problem is **SCALE**:
- Predictions are in **wrong range**
- Model might be predicting [2, 1.5, 1, 1.2] when labels are [7, 5, 4, 6]
- Same **pattern** (order preserved), but wrong **magnitude**

Evidence:
1. **High Pearson** (0.87) = Good pattern
2. **High MAE** (1.18) + **High Euclidean** (3.15) = Wrong scale
3. **Negative R²** = Predictions worse than mean (systematic bias)

---

## Root Cause Analysis

### Issue 1: Output Range Mismatch

**Labels**: Scores range [0.9 - 9.2] per topic (mean ~4-5)
**Model outputs**: Likely in different range (e.g., [0-2] or unbounded)

Looking at the architecture (Cell 48):
```python
# Model outputs (from regression heads)
pred = head(sentence_embedding)  # Unbounded output

# Loss clamping
logits_clamped = torch.clamp(logits, 0.0, 2.0)  # CLAMPED TO [0, 2]!
loss = MSE(logits_clamped, labels)  # But labels are [0.9 - 9.2]
```

**PROBLEM**: Model outputs clamped to [0, 2], but labels are [1-9]. Model can NEVER predict 7.5!

### Issue 2: CV Mismatch

**Pred CV**: 0.36
**Label CV**: 0.46

Model predictions are **less differentiated** than labels. Model outputting more uniform scores.

### Issue 3: Negative R²

R² = 1 - (SS_residual / SS_total)

**Negative R² happens when**:
- SS_residual > SS_total
- Predictions are worse than just predicting the mean
- Systematic bias (e.g., always predicting 2.0 when mean is 4.8)

**Example**:
```
Labels:     [7.5, 4.8, 4.9, 5.7] (mean = 5.725)
Predictions: [2.0, 1.5, 1.6, 1.8] (wrong scale, but right pattern!)

Pearson: High (pattern matches)
R²: Negative (far from actual values)
MAE: High (off by ~3-4 points)
```

---

## Diagnosis: Output Clamping Issue

### The Problem

In **Cell 48** (Model Architecture):

```python
if labels is not None:
    loss_fct = nn.MSELoss()
    # Clamp predictions to [0, 2] for training stability
    logits_clamped = torch.clamp(logits, 0.0, 2.0)  # ← PROBLEM HERE
    loss = loss_fct(logits_clamped, labels.float())
```

**Why this is wrong**:
- Clamps outputs to [0, 2]
- But labels are in [0.9 - 9.2] range
- Model physically CANNOT output values > 2.0
- Loss computed on clamped values, so gradients don't push beyond 2.0

**During inference** (prediction):
```python
return SequenceClassifierOutput(
    logits=logits,  # Returns UNCLAMPED (unbounded)
)
```

So:
- **Training**: Outputs clamped to [0, 2], learns wrong scale
- **Inference**: Outputs unbounded, but model never learned to output >2

---

## Solutions (Ranked by Effectiveness)

### Dataset Hygiene (2025-12-09)
- **UNLABELED / noise chunks are now excluded from every train/val split** (Cell 6.3 update). They are still exported as workflow_data\slavery_Slavdict_pretraining_slavery_v25\Model_finetuning\unlabeled_pool.csv so we can reference irrelevant content for heuristics without letting it pollute loss or evaluation metrics.
- This keeps the "ignore this chunk" signal available for downstream filtering, while ensuring reported effectiveness reflects only meaningful supervision data.


### 🥇 **Solution 1: Remove Clamp, Scale Labels to [0, 1]** (RECOMMENDED)

**Approach**: Normalize labels to [0, 1], remove clamp, use sigmoid output

**Changes needed**:

1. **Dataset** (Cell 50): Normalize labels
```python
# Min-max normalize per topic
min_scores = [0.908, 0.749, 1.280, 0.892]  # From your data
max_scores = [9.222, 7.618, 8.588, 8.345]

for topic_idx, topic in enumerate(topics):
    score = row[f"score_{topic}"]
    normalized = (score - min_scores[topic_idx]) / (max_scores[topic_idx] - min_scores[topic_idx])
    label_vec.append(normalized)  # Now in [0, 1]
```

2. **Model** (Cell 48): Add sigmoid, remove clamp
```python
def forward(...):
    # ... (existing code)

    # Apply sigmoid to bound outputs to [0, 1]
    logits = torch.sigmoid(torch.cat(topic_predictions, dim=1))

    loss = None
    if labels is not None:
        loss_fct = nn.MSELoss()
        loss = loss_fct(logits, labels.float())  # No clamp needed
```

3. **Metrics** (Cell 51): Denormalize for interpretation
```python
# Denormalize predictions and labels for metrics
predictions_denorm = predictions * (max_scores - min_scores) + min_scores
labels_denorm = labels * (max_scores - min_scores) + min_scores

# Compute metrics on denormalized values
```

**Pros**:
- ✓ Stable training (bounded outputs)
- ✓ Balanced across topics (all in [0, 1])
- ✓ Interpretable (sigmoid → probability-like)
- ✓ Matches label range

**Cons**:
- Need to denormalize for interpretation
- Slight complexity in data pipeline

---

### 🥈 **Solution 2: Remove Clamp, Keep Raw Scores** (SIMPLER)

**Approach**: Just remove the clamp, train on raw scores

**Changes needed**:

**Model** (Cell 48): Remove clamp entirely
```python
if labels is not None:
    loss_fct = nn.MSELoss()
    # NO CLAMPING - let model learn full range
    loss = loss_fct(logits, labels.float())
```

**Pros**:
- ✓ Very simple (one line change)
- ✓ Model can learn full range [0-10]
- ✓ No normalization needed

**Cons**:
- ⚠ Unbounded outputs (model could predict negative or >10)
- ⚠ May be less stable (larger gradients)
- ⚠ Different topics have different scales (Racism mean=4.82, Edu mean=3.93)

**Mitigation**: Add clamp during INFERENCE only:
```python
def forward(...):
    logits = torch.cat(topic_predictions, dim=1)

    # During inference, clamp to reasonable range
    if not self.training:
        logits = torch.clamp(logits, 0.0, 10.0)

    loss = None
    if labels is not None:
        loss_fct = nn.MSELoss()
        loss = loss_fct(logits, labels.float())  # No clamp during training
```

---

### 🥉 **Solution 3: Scale Labels to [0, 2], Keep Clamp** (QUICK FIX)

**Approach**: Rescale labels to match model's [0, 2] range

**Changes needed**:

**Dataset** (Cell 50): Scale labels
```python
# Global scaling to [0, 2]
for topic in topics:
    score = row[f"score_{topic}"]
    # Empirical range: [0.9 - 9.2] → scale to [0, 2]
    scaled = (score - 0.9) / (9.2 - 0.9) * 2.0
    label_vec.append(scaled)  # Now in [0, 2]
```

**Metrics** (Cell 51): Rescale back
```python
# Rescale predictions and labels to original range
predictions_rescaled = (predictions / 2.0) * (9.2 - 0.9) + 0.9
labels_rescaled = (labels / 2.0) * (9.2 - 0.9) + 0.9
```

**Pros**:
- ✓ Minimal changes (just data rescaling)
- ✓ Keeps existing clamp logic

**Cons**:
- ⚠ Arbitrary [0, 2] range (why not [0, 1]?)
- ⚠ Doesn't balance per-topic scales
- ⚠ Less interpretable

---

## Recommended Action Plan

### **Immediate: Try Solution 2 (Remove Clamp)**

**Why**: Simplest fix, might work immediately

**Steps**:
1. Edit Cell 48 (Model Architecture)
2. Remove clamp in training loss
3. Add clamp during inference (0-10 range)
4. Re-run training (Cell 58)
5. Check if MAE, R², Euclidean improve

**Expected improvement**:
- MAE should drop from 1.18 → <0.8
- R² should become positive
- Euclidean should drop from 3.15 → <1.5

### **If Still Issues: Implement Solution 1 (Normalize)**

**Why**: Most robust, balanced training

**Steps**:
1. Update Cell 50 (Dataset) to normalize labels [0, 1]
2. Update Cell 48 (Model) to use sigmoid output
3. Update Cell 51 (Metrics) to denormalize for reporting
4. Re-run training
5. Should hit all targets

---

## What to Watch For

### After Implementing Fix

**Training should show**:
- ✓ Loss decreasing consistently (currently: 5.37 at epoch 5)
- ✓ MAE < 0.8 by epoch 3-5
- ✓ R² positive (>0.5 ideally)
- ✓ Euclidean < 1.0

**If problems persist**:
- Check learning rate (try 2e-5 instead of 5e-5)
- Increase epochs (try 10 instead of 5)
- Check for data issues (NaN, outliers)

---

## The Good News

**Pattern learning is working!** Pearson = 0.87 means:
- Model understands topic semantics ✓
- Multi-label co-occurrence captured ✓
- Just needs magnitude scaling fix ✓

With the clamp removed/fixed, the model should quickly learn the correct magnitude scale while maintaining its good pattern learning.

---

## Current Performance Summary

| Metric | Target | Current | Status | After Fix (Est.) |
|--------|--------|---------|--------|------------------|
| Pearson | >0.85 | 0.87 | ✓ PASS | 0.87-0.90 |
| Euclidean | <1.0 | 3.15 | ✗ FAIL | <1.0 |
| CV Correlation | >0.75 | 0.38 | ✗ FAIL | 0.65-0.80 |
| Pairwise Error | <0.5 | 1.30 | ✗ FAIL | <0.5 |
| Global MAE | <0.8 | 1.18 | ✗ FAIL | <0.8 |
| Targets Met | 80% | 20% | ⚠ NEEDS WORK | 80%+ |

**Conclusion**: Fix output scaling → all metrics should improve dramatically while maintaining good Pearson correlation.
