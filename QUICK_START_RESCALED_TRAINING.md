# Quick Start: BERTJE Training with Rescaled Scores

## What Changed?

The notebook now uses **rescaled scores (0-2 range)** instead of raw cosine scores (0-1 range) for all BERTJE training and predictions. This provides:
- 4x better score distribution
- Clear quality tiers (core/moderate/weak/context/noise)
- Better model training signal

## Quick Start Guide

### Step 1: Generate and Save Rescaled Scores

Run these cells in order:

1. **Cell 36**: Calculate rescaled scores
   - Transforms cosine scores to [0, 2] range
   - Creates `rescaled_<topic>` columns

2. **Cell 37**: Classify and save confidence files
   - **NEW**: Now saves files with rescaled scores
   - Creates 3-tier split: high (≥1.0), low (0.5-1.0), none (<0.5)
   - Saves: `scores_high_confidence.csv`, `scores_low_confidence.csv`, `scores_no_confidence.csv`

Expected output:
```
Rescaled 3-tier split:
  High (rescaled >= 1.0):  1234 (25.0%)
  Low (0.5 <= rescaled < 1.0): 2345 (47.5%)
  None (rescaled < 0.5):   1357 (27.5%)

Saved rescaled confidence files:
  High: .../Cosine_labeling/scores_high_confidence.csv
  Low:  .../Cosine_labeling/scores_low_confidence.csv
  None: .../Cosine_labeling/scores_no_confidence.csv
```

### Step 2: Prepare Training Data

Run these cells:

3. **Cell 41**: Load confidence files
   - Loads the rescaled confidence files from Step 1
   - All dataframes now contain `rescaled_<topic>` columns

4. **Cells 42-44**: Prepare training datasets
   - Creates labeled, pseudo-labeled, and unlabeled pools
   - All preserve `rescaled_<topic>` columns
   - Creates 4 training options

Expected output:
```
Option 1 (Labeled only):          1234 examples
Option 2 (Labeled + Pseudo):      3579 examples
Option 3 (Labeled + Unlabeled):   2234 examples
Option 4 (All):                   4579 examples
```

### Step 3: Train BERTJE Model

Run these cells:

5. **Cells 47-50**: Setup training environment
   - Cell 47: Load base model (BERTJE or pretrained)
   - Cell 48: Define `SBERTContinuousMultiLabel` class
   - Cell 49: Define data collator and metrics
   - Cell 50: Define `ContinuousMultiLabelDataset` class
     - **Uses `rescaled_<topic>` columns**
     - **Clips values to [0, 2]**

6. **Cells 52-54**: Load and prepare training data
   - Cell 52: Load train/val CSVs
   - Cell 53: Apply stratified sampling (optional)
   - Cell 54: Create torch datasets

7. **Cells 55-58**: Configure and run training
   - Cell 55: Instantiate model
   - Cell 56: Define training arguments
   - Cell 57: Create trainer
   - Cell 58: Train model

Expected output:
```
Training progress:
Epoch 1/3: train_loss=0.xxx, val_loss=0.xxx
Epoch 2/3: train_loss=0.xxx, val_loss=0.xxx
Epoch 3/3: train_loss=0.xxx, val_loss=0.xxx

Model learns to predict rescaled scores [0, 2]
```

8. **Cells 59-61**: Save trained model
   - Cell 59: Save model and metadata
   - Cell 60: Evaluate final performance
   - Cell 61: Save model components

### Step 4: Generate Predictions

Run these cells:

9. **Cell 65-66**: Load trained model
   - Cell 65: Setup prediction environment
   - Cell 66: Load saved model

10. **Cell 67**: Prepare corpus for prediction

11. **Cell 68**: Generate predictions
    - **Uses updated thresholds for [0, 2] range**
    - Ordinal thresholds: Low<0.6, Med=0.6-0.8, High≥0.8
    - Confidence thresholds: High≥0.8, Med≥0.6

Expected output:
```
Prediction shape: (N, num_topics)
Topics: ['topic1', 'topic2', ...]

Predictions use rescaled range [0, 2]
Confidence assignment uses rescaled thresholds
```

12. **Cell 69**: Save predictions

### Step 5: Visualize Results

13. **Cells 72-78**: Generate visualizations
    - Score distributions
    - Topic distributions
    - Training metrics
    - All use rescaled scores

## Key Differences from Previous Version

### What's New

| Component | Old Behavior | New Behavior |
|-----------|-------------|--------------|
| **Cell 37** | Only analysis/reporting | Now saves rescaled confidence files |
| **Cell 50** | Uses `rescaled_<topic>` | Same, but clarified in comments |
| **Cell 68** | Thresholds for [0, 1] | **Thresholds scaled 2x for [0, 2]** |
| **Confidence Files** | Contains cosine scores | **Contains rescaled scores** |

### Threshold Changes in Cell 68

| Threshold | Old (Cosine) | New (Rescaled) | Scaling |
|-----------|--------------|----------------|---------|
| Ordinal Low/Med | 0.30 | 0.60 | 2x |
| Ordinal Med/High | 0.40 | 0.80 | 2x |
| Confidence High | 0.40 | 0.80 | 2x |
| Confidence Med | 0.30 | 0.60 | 2x |
| Margin High | 0.10 | 0.20 | 2x |
| Margin Med | 0.05 | 0.10 | 2x |

## Troubleshooting

### "NameError: SBERTContinuousMultiLabel is not defined"

**Problem**: Trying to run Cell 66 before Cell 48

**Solution**: Run cells in order:
1. Cell 48 to define the class
2. Then Cell 66 to use it

OR: Run "Restart & Run All" to ensure proper order

### "KeyError: 'rescaled_<topic>'"

**Problem**: Training data doesn't have rescaled columns

**Solution**: Re-run Cell 37 to save confidence files with rescaled scores

### Predictions seem wrong

**Problem**: Model was trained on old cosine scores, predictions use rescaled thresholds

**Solution**: Retrain model (Cells 47-61) after running updated Cell 37

### Model predicts values outside [0, 2]

**Problem**: Model output not properly constrained

**Solution**: Check that:
1. Dataset clips values: `np.clip(cos_val, 0.0, 2.0)`
2. Model uses proper output activation
3. Training data has valid rescaled scores

## Validation Checklist

Before training, verify:

- [ ] Cell 37 ran successfully and saved confidence files
- [ ] Confidence files exist in `Cosine_labeling/` folder
- [ ] Files contain `rescaled_<topic>` columns (check with `pd.read_csv(...).columns`)
- [ ] Rescaled scores are in [0, 2] range (check `df['rescaled_*'].describe()`)

During training, verify:

- [ ] Dataset created successfully with correct label range
- [ ] Training loss decreases over epochs
- [ ] Validation loss tracks training loss reasonably

After training, verify:

- [ ] Predictions are in [0, 2] range
- [ ] Confidence distribution makes sense (not all "low" or all "high")
- [ ] High confidence predictions have high scores (≥0.8)

## Expected Distribution

With rescaled scores, expect:

### Training Data Split (3-tier)
- **High confidence** (≥1.0): ~15-30% of chunks
  - Core topics, clear matches
  - Used as labeled training data

- **Low confidence** (0.5-1.0): ~30-50% of chunks
  - Borderline relevance
  - Used as pseudo-labeled data

- **No confidence** (<0.5): ~30-50% of chunks
  - Weak/no signal
  - May use as unlabeled data or exclude

### Prediction Confidence
After training, predictions should show:
- **High confidence**: ~20-40% (score ≥0.8, good margin)
- **Medium confidence**: ~30-50% (score ≥0.6 or decent margin)
- **Low confidence**: ~20-30% (everything else)

## Next Steps

After completing training with rescaled scores:

1. **Evaluate Quality**
   - Compare high-confidence predictions with manual labels
   - Check if rescaled tiers match intuitive quality

2. **Iterate if Needed**
   - Adjust thresholds in Cell 37 if distribution is skewed
   - Retrain with different dataset options (Cell 52)

3. **Use Predictions**
   - Filter by confidence for downstream analysis
   - Use rescaled scores for ranking/sorting
   - Apply to new documents

## Files Modified

- `dictionary_discovery_v18_rescaled_scores.ipynb` - Main notebook (updated)
- `dictionary_discovery_v18_rescaled_scores_backup.ipynb` - Backup (pre-update)
- `update_notebook_for_rescaled_scores.py` - Update script
- `RESCALED_SCORES_README.md` - Detailed documentation
- `QUICK_START_RESCALED_TRAINING.md` - This file

## Support

For issues or questions:
1. Check [RESCALED_SCORES_README.md](RESCALED_SCORES_README.md) for detailed explanations
2. Review the troubleshooting section above
3. Verify cells were run in correct order
4. Check that Cell 37 was re-run after update to save rescaled files
