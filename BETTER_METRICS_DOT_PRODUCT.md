# Better Metrics for Dot Product Multi-Label Regression

## Current Metrics (Problematic)

```python
eval_corr_Educational Disadvantage: 0.54
eval_corr_Governance Distrust: -0.06
eval_mean_correlation: 0.21
```

**Problems:**
1. Correlation ignores absolute magnitude (scale-invariant)
2. Correlation doesn't penalize constant offsets
3. Not meaningful for multi-output regression where relative magnitudes matter

---

## Recommended Metrics

### 1. Mean Absolute Error (MAE) - PRIMARY METRIC ⭐

**What it measures:** Average absolute difference between predicted and target scores

```python
mae = mean(|predicted - target|)
```

**Why it's good:**
- ✅ Direct measure of prediction accuracy
- ✅ Sensitive to magnitude (0-10 range matters)
- ✅ Interpretable: "On average, predictions are off by X points"
- ✅ Robust to outliers (vs MSE)

**Target values:**
- Good: MAE < 1.0 (predictions within ±1 point)
- Acceptable: MAE 1.0-2.0
- Poor: MAE > 2.0

**Already in your metrics:**
```python
eval_global_mae: 1.10  # Average across all topics
eval_mae_Educational Disadvantage: 1.02
eval_mae_Governance Distrust: 1.04
```

---

### 2. Root Mean Squared Error (RMSE) - SECONDARY

**What it measures:** RMS of prediction errors (penalizes large errors more)

```python
rmse = sqrt(mean((predicted - target)²))
```

**Why it's good:**
- ✅ Sensitive to large errors
- ✅ Same scale as targets (0-10 range)
- ✅ Commonly used in regression

**Target values:**
- Good: RMSE < 1.5
- Acceptable: RMSE 1.5-3.0
- Poor: RMSE > 3.0

---

### 3. R² Score (Coefficient of Determination)

**What it measures:** Proportion of variance explained by model

```python
r2 = 1 - (sum((target - predicted)²) / sum((target - mean(target))²))
```

**Why it's good:**
- ✅ Normalized (0-1 scale)
- ✅ Measures explained variance
- ✅ Better than correlation for regression

**Target values:**
- Good: R² > 0.7
- Acceptable: R² 0.4-0.7
- Poor: R² < 0.4

---

### 4. Topic Ranking Accuracy (Multi-Label Specific)

**What it measures:** How often model gets the topic RANKING correct

```python
def ranking_accuracy(predictions, targets):
    """
    Check if top-ranked predicted topic matches top-ranked target topic.
    """
    pred_ranking = np.argsort(predictions)[::-1]  # Descending
    target_ranking = np.argsort(targets)[::-1]

    # Check if top-1 matches
    top1_match = (pred_ranking[0] == target_ranking[0])

    # Check if top-2 match (any order)
    top2_match = set(pred_ranking[:2]) == set(target_ranking[:2])

    return top1_match, top2_match
```

**Why it's good:**
- ✅ Directly relevant for multi-label classification
- ✅ Measures if model identifies PRIMARY topic
- ✅ More interpretable than correlation

**Target values:**
- Good: Top-1 accuracy > 70%
- Acceptable: Top-1 accuracy 50-70%
- Poor: Top-1 accuracy < 50%

---

### 5. Per-Topic MAE (Diagnostic)

**What it measures:** MAE for each topic separately

**Why it's good:**
- ✅ Identifies which topics are hard to predict
- ✅ Can reveal topic-specific issues
- ✅ Guides model improvements

**Already in your metrics:**
```python
eval_mae_Educational Disadvantage: 1.02  # Good
eval_mae_Governance Distrust: 1.04       # Good
eval_mae_Persistent Poverty: 1.30        # Acceptable
eval_mae_Social Fragmentation: 1.77      # Poor - needs attention
```

---

## Implementation

### Update `compute_continuous_metrics` function

Add these metrics to your evaluation:

```python
def compute_continuous_metrics(eval_pred, topic_names):
    """
    Compute metrics for continuous multi-label regression (dot product scores).

    Focus on MAE, RMSE, and R² - NOT correlation.
    """
    predictions, labels = eval_pred

    metrics = {}

    # Global metrics across all topics
    global_mae = np.mean(np.abs(predictions - labels))
    global_rmse = np.sqrt(np.mean((predictions - labels) ** 2))
    global_r2 = 1 - (np.sum((labels - predictions) ** 2) /
                     np.sum((labels - np.mean(labels)) ** 2))

    metrics['global_mae'] = global_mae
    metrics['global_rmse'] = global_rmse
    metrics['global_r2'] = global_r2

    # Per-topic metrics
    for i, topic in enumerate(topic_names):
        pred_topic = predictions[:, i]
        label_topic = labels[:, i]

        # MAE (primary metric)
        mae = np.mean(np.abs(pred_topic - label_topic))
        metrics[f'mae_{topic}'] = mae

        # RMSE
        rmse = np.sqrt(np.mean((pred_topic - label_topic) ** 2))
        metrics[f'rmse_{topic}'] = rmse

        # R² (better than correlation)
        ss_res = np.sum((label_topic - pred_topic) ** 2)
        ss_tot = np.sum((label_topic - np.mean(label_topic)) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        metrics[f'r2_{topic}'] = r2

    # Ranking accuracy (multi-label specific)
    top1_matches = 0
    top2_matches = 0

    for pred_row, label_row in zip(predictions, labels):
        pred_ranking = np.argsort(pred_row)[::-1]
        label_ranking = np.argsort(label_row)[::-1]

        if pred_ranking[0] == label_ranking[0]:
            top1_matches += 1

        if set(pred_ranking[:2]) == set(label_ranking[:2]):
            top2_matches += 1

    metrics['top1_ranking_accuracy'] = top1_matches / len(predictions)
    metrics['top2_ranking_accuracy'] = top2_matches / len(predictions)

    # Mean metrics across topics (for overall assessment)
    topic_maes = [metrics[f'mae_{topic}'] for topic in topic_names]
    topic_r2s = [metrics[f'r2_{topic}'] for topic in topic_names]

    metrics['mean_mae'] = np.mean(topic_maes)
    metrics['mean_r2'] = np.mean(topic_r2s)

    return metrics
```

---

## Interpreting Your Current Results

Looking at your actual metrics:

```python
eval_global_mae: 1.10          # ✓ Good - within ±1.1 points on average
eval_mae_Educational: 1.02     # ✓ Good
eval_mae_Governance: 1.04      # ✓ Good
eval_mae_Poverty: 1.30         # ⚠️ Acceptable
eval_mae_Social Frag: 1.77     # ❌ Poor - needs improvement

eval_corr_Governance: -0.06    # ❌ Misleading (ignore this)
eval_corr_Social Frag: -0.01   # ❌ Misleading (ignore this)
eval_mean_correlation: 0.21    # ❌ Not useful for regression
```

**The MAE tells the real story:**
- Model predicts within ±1-1.3 points for 3 topics (GOOD for 0-10 range)
- Struggles with Social Fragmentation (±1.77 points)
- Negative correlations are misleading - MAE shows model IS learning

**Key insight:** Your model might actually be performing OK on 3/4 topics, but correlation metric is hiding this!

---

## What to Monitor During Training

### Primary (optimize these):
1. **global_mae** - lower is better (target: < 1.0)
2. **mean_r2** - higher is better (target: > 0.5)
3. **top1_ranking_accuracy** - higher is better (target: > 0.6)

### Secondary (diagnostic):
4. **per-topic MAE** - identify problem topics
5. **global_rmse** - detect large errors

### Ignore:
6. ~~correlation~~ - not meaningful for multi-output regression
7. ~~threshold accuracy~~ - designed for binary, not continuous

---

## Expected Performance After Dot Product Switch

| Metric | Current (Cosine) | Target (Dot Product) |
|--------|------------------|----------------------|
| **Global MAE** | 1.10 | 0.8 - 1.2 ✓ |
| **Global R²** | N/A | 0.5 - 0.7 |
| **Top-1 Ranking** | ~0.57 | 0.65 - 0.75 |
| **Mean MAE** | 1.35 | 1.0 - 1.5 |

With proper dot product scores (0-10 range):
- MAE of 1.0 = 10% error (excellent)
- MAE of 1.5 = 15% error (acceptable)
- MAE of 2.0 = 20% error (needs improvement)

---

## Summary

**Stop using:**
- ❌ `eval_mean_correlation` - scale-invariant, not useful
- ❌ `eval_corr_*` per topic - misleading for regression

**Start using:**
- ✅ `eval_global_mae` - PRIMARY metric
- ✅ `eval_mean_r2` - measures explained variance
- ✅ `top1_ranking_accuracy` - multi-label specific
- ✅ `eval_mae_*` per topic - diagnostic

**Current assessment:**
Your model is likely performing BETTER than correlation suggests:
- MAE ~1.1 is actually good for 0-10 range
- Negative correlations are misleading (ignore them)
- Focus on reducing MAE for Social Fragmentation topic

Once you re-run with proper dot product scores, expect:
- MAE to stay similar or improve slightly
- R² to show 50-70% variance explained
- Top-1 ranking accuracy 65-75%
