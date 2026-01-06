# Rescaled Scores: BERTJE Training Integration

## Overview

The dictionary discovery workflow has been updated to use **rescaled scores** (0-2 range) instead of raw cosine scores (0-1 range) throughout the BERTJE training and prediction pipeline. This provides 4x better score distribution and more interpretable quality tiers.

## Score Transformation

### Rescaling Function

```python
def rescale_cosine_score(cosine_score):
    """
    Transform cosine score to [0, 2] range with improved spread.

    Process:
    1. Shift: cosine - 0.5 (center around 0)
    2. Stretch: multiply by 4 (spread out distribution)
    3. Scale to [0, 2]: multiply by 2
    4. Clip: ensure final range is [0, 2]

    Returns:
        float: Rescaled score in [0.0, 2.0] range
    """
    shifted = cosine_score - 0.5
    stretched = shifted * 4.0
    rescaled = min(2.0, stretched * 2.0)
    return rescaled
```

### Score Distribution Comparison

| Metric | Original (Cosine) | Rescaled (0-2) | Improvement |
|--------|-------------------|----------------|-------------|
| Range  | [0.0, 1.0]        | [0.0, 2.0]     | 2x wider    |
| Spread (Std) | ~0.05-0.10   | ~0.20-0.40     | 4x better   |
| Interpretability | Low (compressed) | High (clear tiers) | Much better |

## Confidence Tier Systems

### 5-Tier System (Analysis & Reporting)

Used for detailed analysis and quality assessment:

| Tier | Score Range | Interpretation | Typical Use |
|------|-------------|----------------|-------------|
| **Core** | 1.5 - 2.0 | Highest quality, clear topic match | Gold standard training data |
| **Moderate** | 1.0 - 1.5 | Good quality, reliable match | Standard training data |
| **Weak** | 0.5 - 1.0 | Borderline relevance | Pseudo-labeling candidate |
| **Context** | 0.25 - 0.5 | Weak signal, contextual mention | Consider for unlabeled pool |
| **Noise** | 0.0 - 0.25 | No meaningful signal | Exclude from training |

### 3-Tier System (Training)

Used for actual BERTJE model training (mapped from 5-tier):

| Tier | Score Range | Composition | Training Use |
|------|-------------|-------------|--------------|
| **High** | rescaled >= 1.0 | Core + Moderate | Labeled training data |
| **Low** | 0.5 <= rescaled < 1.0 | Weak | Pseudo-labeled data |
| **None** | rescaled < 0.5 | Context + Noise | Unlabeled/excluded |

### Mapping Logic

```python
# Create 3-tier confidence from rescaled scores
all_scores_df['confidence_3tier'] = pd.cut(
    all_scores_df['max_score_rescaled'],
    bins=[0, 0.5, 1.0, 2.0],
    labels=['none', 'low', 'high'],
    include_lowest=True
)

# Split for training
high_df = all_scores_df[all_scores_df['confidence_3tier'] == 'high']   # rescaled >= 1.0
low_df = all_scores_df[all_scores_df['confidence_3tier'] == 'low']     # 0.5 <= rescaled < 1.0
none_df = all_scores_df[all_scores_df['confidence_3tier'] == 'none']   # rescaled < 0.5
```

## Updated Notebook Cells

### Cell 36: Score Calculation
- Calculates rescaled scores for all chunks
- Creates `rescaled_<topic>` columns for each topic
- Creates `max_score_rescaled` column for max score across topics

### Cell 37: Confidence Classification & File Saving
- **5-tier classification**: For analysis and reporting
- **3-tier classification**: For training data splits
- **Saves files**: `scores_high_confidence.csv`, `scores_low_confidence.csv`, `scores_no_confidence.csv`
- All files contain rescaled scores in `rescaled_<topic>` columns

### Cell 50: Dataset Class
```python
class ContinuousMultiLabelDataset(Dataset):
    """
    Dataset for continuous multi-label regression.
    Uses rescaled scores [0, 2] - NO discretization!
    """

    def __init__(self, dataframe, tokenizer, topics, config):
        # Extract continuous rescaled scores directly
        for topic in topics:
            cos_val = row.get(f"rescaled_{topic}", 0.0)
            cos_val = float(np.clip(cos_val, 0.0, 2.0))  # Clip to [0, 2]
            label_vec.append(cos_val)
```

### Cell 68: Prediction Thresholds

All thresholds scaled 2x for rescaled [0, 2] range:

#### Ordinal Classification
```python
def score_to_ordinal(score):
    """Convert continuous rescaled score to ordinal class"""
    if score < 0.60:      # Was 0.30 for cosine
        return 0  # Low
    elif score < 0.80:    # Was 0.40 for cosine
        return 1  # Med
    else:
        return 2  # High
```

#### Confidence Assignment
```python
def assign_confidence(row):
    """Assign confidence based on rescaled score + margin"""
    score = row['bertje_primary_score']
    margin = row['bertje_margin']

    # High confidence: score >= 0.8 AND good margin
    if score >= 0.80 and margin > 0.20:  # Was 0.40 and 0.10
        return 'high'
    # Medium confidence: score >= 0.6 OR decent margin
    elif score >= 0.60 or margin > 0.10:  # Was 0.30 and 0.05
        return 'medium'
    # Low confidence: everything else
    else:
        return 'low'
```

## Workflow Steps

### 1. Generate Rescaled Scores
Run **Cell 36** to:
- Calculate cosine scores for all chunks
- Apply rescaling transformation
- Create `rescaled_<topic>` columns

### 2. Classify & Save Confidence Files
Run **Cell 37** to:
- Apply 5-tier rescaled classification (analysis)
- Apply 3-tier classification (training)
- Save `scores_high_confidence.csv` (rescaled >= 1.0)
- Save `scores_low_confidence.csv` (0.5 <= rescaled < 1.0)
- Save `scores_no_confidence.csv` (rescaled < 0.5)
- Save `scores_all_labeled.csv` (all scores)

### 3. Prepare Training Data
Run **Cells 41-44** to:
- Load confidence files (now contain rescaled scores)
- Create training data options (labeled, pseudo, unlabeled)
- All dataframes preserve `rescaled_<topic>` columns

### 4. Train BERTJE Model
Run **Cells 47-60** to:
- Dataset class extracts `rescaled_<topic>` values [0, 2]
- Model learns to predict rescaled scores [0, 2]
- Loss function: MSE on rescaled range
- Model outputs: Continuous scores [0, 2]

### 5. Generate Predictions
Run **Cells 66-69** to:
- Model predicts rescaled scores [0, 2]
- Apply rescaled thresholds for ordinal classification
- Apply rescaled thresholds for confidence assignment
- Save predictions with rescaled scores

## Benefits of Rescaled Scores

### 1. Better Distribution
- **Original**: 80%+ of scores compressed in 0.4-0.6 range
- **Rescaled**: Scores spread across 0.5-1.5 range (4x better)

### 2. Interpretable Tiers
- **Original**: Hard to distinguish "good" vs "great" (both ~0.5)
- **Rescaled**: Clear tiers (core=1.5-2.0, moderate=1.0-1.5, weak=0.5-1.0)

### 3. Better Training Signal
- **Original**: Compressed scores → model has trouble learning distinctions
- **Rescaled**: Wider range → model can learn finer distinctions

### 4. Consistent Thresholds
- **Original**: Thresholds like 0.4 are arbitrary
- **Rescaled**: Thresholds like 1.0 are meaningful (50% of range)

## Data Column Reference

### Score Columns in DataFrames

After running Cell 36 and 37, dataframes contain:

```python
# Original cosine scores (still present for reference)
'cos_<topic>'              # Original cosine similarity [0, 1]
'max_score'                # Max cosine across topics
'primary_topic'            # Topic with max cosine score

# Rescaled scores (used for training)
'rescaled_<topic>'         # Rescaled score [0, 2]
'max_score_rescaled'       # Max rescaled across topics
'primary_topic_rescaled'   # Topic with max rescaled score

# Confidence classifications
'confidence'               # Original 3-tier (from config thresholds)
'confidence_rescaled'      # New 5-tier (core/moderate/weak/context/noise)
'confidence_3tier'         # New 3-tier for training (high/low/none)
```

### Training Data Structure

Confidence CSV files contain all columns including:
- Text data: `text`, `raw_text`, `chunk_id`, etc.
- Cosine scores: `cos_<topic>` for each topic
- **Rescaled scores**: `rescaled_<topic>` for each topic ← **USED FOR TRAINING**
- Metadata: `max_score`, `primary_topic`, `confidence_3tier`, etc.

## Troubleshooting

### Issue: Model predicts values outside [0, 2]
- Check dataset clipping: `np.clip(cos_val, 0.0, 2.0)`
- Check model output activation (should be sigmoid scaled to [0, 2])

### Issue: Training doesn't improve
- Verify `rescaled_<topic>` columns exist in training data
- Check label extraction in dataset class
- Verify loss function uses correct range

### Issue: Predictions don't match expected tiers
- Verify thresholds are scaled 2x (0.8 instead of 0.4, etc.)
- Check that model was trained on rescaled scores
- Ensure prediction code uses rescaled column names

## Version History

- **v18**: Initial rescaled scores implementation
  - Added rescaling transformation in Cell 36
  - Dataset class updated to use `rescaled_<topic>` columns
  - Prediction thresholds NOT yet updated

- **v18 (Updated)**: Complete rescaled integration
  - Cell 37: Added 3-tier classification and file saving
  - Cell 50: Clarified rescaled score usage
  - Cell 68: Updated all thresholds for [0, 2] range
  - All components now use rescaled scores consistently

## References

- Original notebook: `dictionary_discovery_v18_rescaled_scores.ipynb`
- Update script: `update_notebook_for_rescaled_scores.py`
- Backup: `dictionary_discovery_v18_rescaled_scores_backup.ipynb`
