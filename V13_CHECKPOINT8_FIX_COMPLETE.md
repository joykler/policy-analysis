# V13 Checkpoint 8 Fix - Complete

## Issue
Checkpoint 8 was still using V12's ordinal classification code:
- Loading `SBERTMultiOrdinal` model
- Predicting ordinal classes (0=Low, 1=Med, 2=High)
- Outputting only ordinal predictions

This would fail when trying to load V13's continuous regression model.

## Changes Made

### Cell 60 (8.2): Load Continuous Model

**Before (V12 ordinal):**
```python
bertje_model = SBERTMultiOrdinal(
    model_name=model_config['model_name'],
    num_topics=model_config['num_topics'],
    num_classes=model_config['num_classes']  # 3 classes
)
model_weights_path = model_dir / 'pytorch_model.bin'
```

**After (V13 continuous):**
```python
bertje_model = SBERTContinuousMultiLabel(
    model_name=metadata['model_name'],
    num_topics=metadata['num_topics']  # No num_classes - continuous!
)
model_save_path = model_dir / 'continuous_regression_model'
metadata_path = model_dir / 'continuous_model_metadata.json'
```

**Key differences:**
- Uses `SBERTContinuousMultiLabel` instead of `SBERTMultiOrdinal`
- Loads from `continuous_regression_model/` folder
- Uses `continuous_model_metadata.json` instead of `model_config.json`
- No `num_classes` parameter (continuous output, not classification)

### Cell 62 (8.4): Predict Continuous Scores

**Before (V12 ordinal):**
```python
def predict_bert_multitopic(texts, batch_size=32):
    # Apply softmax per topic
    probs = torch.softmax(logits, dim=-1)  # [batch, num_topics, num_classes]

    # Get predicted class (0,1,2)
    topic_scores, topic_preds = torch.max(probs, dim=-1)
    return topic_preds, topic_scores  # ordinal classes + confidence
```

**After (V13 continuous):**
```python
def predict_continuous_multitopic(texts, batch_size=32):
    # Get continuous scores (already sigmoid'd in model)
    scores = outputs.logits  # [batch, num_topics] - values in [0, 1]

    return scores  # continuous scores directly
```

**Key differences:**
- No softmax (output is already continuous [0, 1])
- No argmax (no classes to predict)
- Returns continuous scores directly

**Output columns created:**
```python
# PRIMARY: Continuous scores
corpus_for_bert[f'bertje_{topic}_score'] = topic_scores[:, i]

# COMPATIBILITY: Ordinal classes derived from scores
def score_to_ordinal(score):
    if score < 0.30: return 0  # Low
    elif score < 0.40: return 1  # Med
    else: return 2  # High

corpus_for_bert[f'bertje_{topic}_class'] = score.apply(score_to_ordinal)
```

**Confidence assignment updated:**
```python
def assign_confidence(row):
    score = row['bertje_primary_score']  # Continuous score
    margin = row['bertje_margin']

    # High: score >= 0.4 AND good margin
    if score >= 0.40 and margin > 0.10:
        return 'high'
    # Medium: score >= 0.3 OR decent margin
    elif score >= 0.30 or margin > 0.05:
        return 'medium'
    # Low: everything else
    else:
        return 'low'
```

### Cell 63 (8.5): Summary with Continuous Scores

**Before (V12 ordinal):**
```python
print("Ordinal class distribution:")
class_dist = corpus_for_bert['bertje_primary_class'].value_counts()
# Only showed class counts
```

**After (V13 continuous):**
```python
print("Continuous score statistics (primary topic):")
print(corpus_for_bert['bertje_primary_score'].describe())

print("Score distribution by percentile:")
for p in [10, 25, 50, 75, 90, 95, 99]:
    val = corpus_for_bert['bertje_primary_score'].quantile(p/100)
    print(f"  {p}th percentile: {val:.3f}")

# Also show ordinal for reference
print("Ordinal class distribution (for reference):")
class_dist = corpus_for_bert['bertje_primary_class'].value_counts()
```

**Additional outputs:**
```python
# Save score-threshold filtered files
for threshold in [0.3, 0.4, 0.5]:
    above_threshold = corpus_for_bert[corpus_for_bert['bertje_primary_score'] >= threshold]
    threshold_path = output_folder / f'bertje_continuous_predictions_score_gte_{int(threshold*100)}.csv'
    above_threshold.to_csv(threshold_path, index=False)
```

## Output Changes

### Column Naming

**V12 (ordinal):**
- `bertje_<topic>_class`: Ordinal class 0/1/2
- `bertje_<topic>_score`: Softmax probability of predicted class
- `bertje_primary_class`: Primary topic's ordinal class

**V13 (continuous):**
- `bertje_<topic>_score`: **Continuous relevance score [0, 1]** (PRIMARY)
- `bertje_<topic>_class`: Ordinal class derived from score (COMPATIBILITY)
- `bertje_primary_score`: **Continuous score of primary topic** (PRIMARY)
- `bertje_primary_class`: Ordinal class for reference

### Files Saved

**V12 outputs:**
```
BERTJE_predictions/
  bertje_predictions_full.csv
  bertje_predictions_high_confidence.csv
```

**V13 outputs:**
```
BERTJE_predictions/
  bertje_continuous_predictions_full.csv
  bertje_continuous_predictions_high_confidence.csv
  bertje_continuous_predictions_score_gte_30.csv  (NEW)
  bertje_continuous_predictions_score_gte_40.csv  (NEW)
  bertje_continuous_predictions_score_gte_50.csv  (NEW)
```

## Why This Matters

### V12 Problem
When predicting on new chunks, V12 would:
1. Predict ordinal class: Low/Med/High
2. Lose fine-grained information
3. Chunks with scores 0.29 and 0.31 both labeled "Low" or "Med"

### V13 Solution
When predicting on new chunks, V13:
1. Predicts continuous score: 0.29 vs 0.31
2. Preserves fine-grained differences
3. Allows flexible thresholding (users can choose cutoffs)
4. Still provides ordinal classes for backward compatibility

## Example Predictions

### V12 Ordinal Output
```
chunk_id        | bertje_Educational_class | bertje_Educational_score
----------------|--------------------------|-------------------------
chunk_001       | 1 (Med)                  | 0.72 (confidence)
chunk_002       | 0 (Low)                  | 0.85 (confidence)
chunk_003       | 2 (High)                 | 0.68 (confidence)
```
**Problem:** No way to distinguish 0.31 from 0.39 (both "Med")

### V13 Continuous Output
```
chunk_id        | bertje_Educational_score | bertje_Educational_class
----------------|--------------------------|-------------------------
chunk_001       | 0.35                     | 1 (Med) - for reference
chunk_002       | 0.22                     | 0 (Low)
chunk_003       | 0.47                     | 2 (High)
```
**Benefit:**
- Primary: Use continuous scores for ranking, filtering
- Compatibility: Ordinal classes available if needed
- Flexibility: Users can choose their own thresholds

## Verification

To verify Checkpoint 8 works correctly:

1. Run Checkpoint 7 to train continuous model
2. Check that these files exist:
   - `workflow_data/.../Model_finetuning/continuous_regression_model/`
   - `workflow_data/.../Model_finetuning/continuous_model_metadata.json`
3. Run Checkpoint 8 cells 60-63
4. Verify outputs:
   - `bertje_<topic>_score` has continuous values in [0, 1]
   - `bertje_<topic>_class` has ordinal values 0/1/2
   - Score-threshold filtered files created

## Status

✓ Checkpoint 8 fully updated for continuous regression
✓ Loads SBERTContinuousMultiLabel model
✓ Predicts continuous scores
✓ Provides ordinal classes for compatibility
✓ Creates score-threshold filtered outputs
✓ Shows continuous score statistics

V13 Checkpoint 8 is now complete and consistent with Checkpoint 7's continuous regression approach.
