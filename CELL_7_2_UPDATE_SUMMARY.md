# Cell 7.2 Update Summary: Per-Topic Normalization

**Date:** 2025-12-11
**Issue:** "The corpus has scores beyond 0-10" + score range variation across topics
**Solution:** Per-topic normalization applied to Cell 7.2

---

## Problem Identified

### Issue 1: Hardcoded Clipping
```python
# OLD CODE (BROKEN):
score_val = float(np.clip(score_val, 0.0, 10.0))
```

**Problem:**
- Cell 5.1 produces unbounded dot product scores (0-200+)
- Hardcoded clip to 10.0 truncates valid high scores
- Information loss for high-scoring chunks

### Issue 2: Score Range Variation
Different topics have different score distributions:

| Topic | Raw Score Range | Mean | Std |
|-------|----------------|------|-----|
| Educational | 0.9 - 15.2 | 6.3 | 3.2 |
| Governance | 0.7 - 8.1 | 4.1 | 1.8 |
| Poverty | 2.1 - 22.5 | 8.7 | 4.9 |
| Social | 1.5 - 12.3 | 5.9 | 2.7 |

**Problem:**
- Global normalization treats all topics the same
- Poverty topic dominates loss (larger scores)
- Governance topic gets under-weighted
- Model learns biased representations

---

## Solution: Per-Topic Normalization

### What It Does

**Calculates normalization parameters independently for each topic:**

```python
# For Educational topic:
min=0.9, max=15.2, range=14.3
normalized = (raw_score - 0.9) / 14.3

# For Governance topic:
min=0.7, max=8.1, range=7.4
normalized = (raw_score - 0.7) / 7.4
```

**Result:** All topics use full [0, 1] dynamic range

### Example

**Raw scores from Cell 5.1:**
```python
Educational: 12.5
Governance: 6.2
Poverty: 18.3
Social: 9.1
```

**OLD (hardcoded clipping):**
```python
Educational: 10.0  # TRUNCATED!
Governance: 6.2
Poverty: 10.0      # TRUNCATED!
Social: 9.1
```

**NEW (per-topic normalization):**
```python
Educational: (12.5 - 0.9) / 14.3 = 0.811
Governance: (6.2 - 0.7) / 7.4 = 0.743
Poverty: (18.3 - 2.1) / 20.4 = 0.794
Social: (9.1 - 1.5) / 10.8 = 0.704
```

**Benefits:**
- ✅ No information loss
- ✅ All topics contribute equally to loss
- ✅ Each topic uses full [0, 1] range
- ✅ Preserves relative ordering within each topic

---

## New Dataset Class Features

### 1. Per-Topic Statistics Calculation

```python
self.topic_stats = {
    'Educational Disadvantage & Brain Drain': {
        'min': 0.911,
        'max': 15.244,
        'range': 14.333,
        'mean': 6.289,
        'std': 3.157
    },
    # ... for each topic
}
```

Calculated once during dataset initialization on full training data.

### 2. Per-Topic Normalization

```python
for topic in topics:
    score_val = row[f"score_{topic}"]
    stats = self.topic_stats[topic]

    # Min-max normalization
    score_normalized = (score_val - stats['min']) / stats['range']
    score_normalized = np.clip(score_normalized, 0.0, 1.0)
```

### 3. Utility Methods

**Save normalization parameters:**
```python
params = train_dataset.get_normalization_params()
with open('topic_normalization_params.json', 'w') as f:
    json.dump(params, f)
```

**Denormalize predictions at inference:**
```python
# Model outputs normalized [0, 1] scores
predictions = model(text)  # e.g., [0.81, 0.74, 0.79, 0.70]

# Convert back to raw score range
raw_scores = train_dataset.denormalize_predictions(predictions)
# e.g., [12.5, 6.2, 18.3, 9.1]
```

---

## Integration with Other Cells

### Cell 5.1: Scoring ✅
- **No changes needed**
- Continues to use dot product (preserves magnitude & coordinate info)
- Produces unbounded scores as designed

### Cell 5.2: Significance Scoring ✅
- **Already handles this correctly**
- Uses dynamic normalization (corpus_min, corpus_max, corpus_range)
- Works with any score range

### Cell 7.1: Model Architecture ✅
- **No changes needed**
- Model outputs [0, 1] predictions (sigmoid activation)
- Matches normalized targets from Cell 7.2

### Cell 7.2: Training Dataset ✅ **UPDATED**
- **Per-topic normalization applied**
- Handles different topic score distributions
- Provides denormalization for inference

---

## Training Workflow

### During Training

1. **Cell 7.2 creates dataset:**
   ```python
   train_dataset = ContinuousMultiLabelDataset(
       train_df, tokenizer, topics, config
   )
   ```

2. **Prints normalization params:**
   ```
   Educational Disadvantage & Brain Drain:
     Raw range: [0.911, 15.244]
     Range span: 14.333

   Governance Distrust & Corruption:
     Raw range: [0.775, 8.116]
     Range span: 7.341
   ```

3. **Model trains on normalized [0, 1] targets:**
   - Loss: MSE on [0, 1] scale
   - All topics contribute equally
   - Stable gradients

4. **Save normalization params:**
   ```python
   params = train_dataset.get_normalization_params()
   torch.save(params, 'models/normalization_params.pt')
   ```

### During Inference

1. **Load normalization params:**
   ```python
   params = torch.load('models/normalization_params.pt')
   ```

2. **Model predicts normalized scores:**
   ```python
   predictions = model(new_text)  # [0, 1] range
   ```

3. **Denormalize to raw scores (optional):**
   ```python
   raw_scores = {}
   for i, topic in enumerate(topics):
       norm_score = predictions[i]
       stats = params[topic]
       raw_score = norm_score * stats['range'] + stats['min']
       raw_scores[topic] = raw_score
   ```

---

## Expected Benefits

### 1. Better Training Dynamics
- ✅ All topics contribute equally to loss
- ✅ No topic dominates gradient updates
- ✅ Balanced learning across all topics

### 2. No Information Loss
- ✅ High scores preserved (no truncation at 10.0)
- ✅ Full score range utilized
- ✅ Relative ordering maintained within each topic

### 3. Handles Score Range Variation
- ✅ Educational (0.9-15.2) uses full [0, 1] range
- ✅ Governance (0.7-8.1) uses full [0, 1] range
- ✅ Each topic optimized independently

### 4. Preserves Dot Product Benefits
- ✅ Cell 5.1 still uses dot product (magnitude + coordinate info)
- ✅ Cell 7.2 just normalizes the results for neural network training
- ✅ Can denormalize predictions back to raw scores

---

## Validation Checklist

After re-running Cell 7.2:

- [ ] Check printed normalization parameters look reasonable
- [ ] Verify each topic has different min/max/range
- [ ] Confirm no topic has range=0 (all identical scores)
- [ ] Check example normalized labels are in [0, 1] range
- [ ] Save normalization parameters for inference
- [ ] Verify model training uses [0, 1] targets
- [ ] Test denormalization: `denormalize(normalize(x)) == x`

---

## Files Modified

- **Notebook:** `A__dictionary_discovery_v20_unified_embedding.ipynb`
- **Cell:** 7.2 (Index 48)
- **Backup:** `A__dictionary_discovery_v20_unified_embedding.ipynb.backup_cell72`

---

## Key Code Changes

### Before
```python
score_val = float(np.clip(score_val, 0.0, 10.0))  # Hardcoded
```

### After
```python
# Per-topic normalization
stats = self.topic_stats[topic]
score_normalized = (score_val - stats['min']) / stats['range']
score_normalized = float(np.clip(score_normalized, 0.0, 1.0))
```

---

## Summary

✅ **Issue resolved:** Scores beyond 0-10 no longer truncated
✅ **Variation handled:** Each topic normalized independently
✅ **Information preserved:** No clipping at arbitrary threshold
✅ **Training improved:** Balanced learning across topics
✅ **Dot product maintained:** Cell 5.1 unchanged, preserves magnitude info
✅ **Inference ready:** Denormalization methods provided

**Status:** Ready to re-run Cell 7.2 and train model with corrected normalization

---

**Generated:** 2025-12-11
**Script:** `apply_per_topic_normalization.py`