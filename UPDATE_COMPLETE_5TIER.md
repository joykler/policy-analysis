# BERTJE Training Update: 5-Tier Rescaled Scores - COMPLETE

## Date
2025-11-29

## Status
✅ **COMPLETE** - All notebook cells updated for 5-tier rescaled score system

## What Was Changed

### Cell 37: Score Classification & File Saving
**Status**: ✅ Updated

**Changes**:
- Added 5-tier classification using rescaled scores
- Saves 5 separate confidence files:
  - `scores_core_confidence.csv` (1.5-2.0)
  - `scores_moderate_confidence.csv` (1.0-1.5)
  - `scores_weak_confidence.csv` (0.5-1.0)
  - `scores_context_confidence.csv` (0.25-0.5)
  - `scores_noise_confidence.csv` (0-0.25)
- Also saves 3-tier compatibility files:
  - `scores_high_confidence.csv` (Core + Moderate)
  - `scores_low_confidence.csv` (Weak)
  - `scores_no_confidence.csv` (Context + Noise)
- All files contain `rescaled_<topic>` columns

### Cell 50: Dataset Class
**Status**: ✅ Updated

**Changes**:
- Updated comments to clarify use of rescaled scores [0, 2]
- Dataset class already correctly extracts `rescaled_<topic>` columns
- Clips values to [0.0, 2.0] range

### Cell 68: Prediction Thresholds
**Status**: ✅ Updated

**Changes**:

#### Ordinal Classification (5 levels)
```python
def score_to_ordinal(score):
    if score < 0.25:
        return 0  # Noise
    elif score < 0.50:
        return 1  # Context
    elif score < 1.00:
        return 2  # Weak
    elif score < 1.50:
        return 3  # Moderate
    else:
        return 4  # Core
```

#### Confidence Assignment (5 tiers)
```python
def assign_confidence(row):
    score = row['bertje_primary_score']
    margin = row['bertje_margin']

    if score >= 1.50 and margin > 0.30:
        return 'core'
    elif score >= 1.00 and margin > 0.20:
        return 'moderate'
    elif score >= 0.50 and margin > 0.10:
        return 'weak'
    elif score >= 0.25 or margin > 0.05:
        return 'context'
    else:
        return 'noise'
```

## 5-Tier Score Ranges

| Tier | Score Range | Margin Threshold | Interpretation |
|------|-------------|------------------|----------------|
| Core | 1.5 - 2.0 | > 0.30 | Perfect match, gold standard |
| Moderate | 1.0 - 1.5 | > 0.20 | Good quality, clear relevance |
| Weak | 0.5 - 1.0 | > 0.10 | Borderline, some connection |
| Context | 0.25 - 0.5 | > 0.05 | Weak signal, contextual |
| Noise | 0.0 - 0.25 | any | No meaningful signal |

## Files Created/Updated

### Modified
- `dictionary_discovery_v18_rescaled_scores.ipynb` - Main notebook with 5-tier updates

### Backups
- `dictionary_discovery_v18_rescaled_scores_backup.ipynb` - Initial backup (3-tier)
- `dictionary_discovery_v18_rescaled_scores_backup_5tier.ipynb` - Pre-5tier backup

### Scripts
- `update_notebook_for_rescaled_scores.py` - Initial 3-tier update script
- `update_notebook_for_5tier_rescaled.py` - 5-tier update script

### Documentation
- `RESCALED_SCORES_5TIER_README.md` - Comprehensive 5-tier guide
- `RESCALED_SCORES_README.md` - Original rescaled scores guide
- `QUICK_START_RESCALED_TRAINING.md` - Step-by-step workflow
- `RESCALED_SCORES_UPDATE_SUMMARY.md` - Technical summary
- `RESCALED_SCORES_VISUAL_GUIDE.md` - Visual diagrams
- `UPDATE_COMPLETE_5TIER.md` - This file

## Verification Results

All changes verified:

✅ Cell 37 has 5-tier file saving logic
✅ Cell 37 includes 3-tier compatibility files
✅ Cell 50 clarifies rescaled score usage
✅ Cell 68 has 5-tier ordinal classification (0-4)
✅ Cell 68 has 5-tier confidence assignment (core/moderate/weak/context/noise)

## Next Steps for User

### 1. Run Cell 37 to Generate Files
```
Execute Cell 37 in the notebook
↓
Generates 9 CSV files:
- 5 tier-specific files (core, moderate, weak, context, noise)
- 3 compatibility files (high, low, none)
- 1 combined file (all)
```

### 2. Choose Training Strategy

**Option A: Standard Quality (Recommended)**
```python
# Use high confidence file (Core + Moderate)
df_labeled = pd.read_csv('scores_high_confidence.csv')
```

**Option B: Granular Control**
```python
# Select specific tiers
core_df = pd.read_csv('scores_core_confidence.csv')
moderate_df = pd.read_csv('scores_moderate_confidence.csv')
df_labeled = pd.concat([core_df, moderate_df])
```

**Option C: Include Borderline**
```python
# Add weak tier for more data
high_df = pd.read_csv('scores_high_confidence.csv')
weak_df = pd.read_csv('scores_weak_confidence.csv')
df_labeled = pd.concat([high_df, weak_df])
```

### 3. Train Model
Run Cells 47-61 with chosen training data

### 4. Generate 5-Tier Predictions
Run Cells 66-69 to get predictions with 5-tier confidence

### 5. Analyze Results
```python
# Check prediction distribution
predictions['bertje_confidence'].value_counts()

# Expected:
# core        10-20%
# moderate    20-30%
# weak        30-40%
# context     10-20%
# noise        5-15%
```

## Training Data Recommendations

### By Use Case

**High Precision Needed** (e.g., final analysis):
- Use: Core only
- Data: 10-15% of corpus
- Quality: Highest
- Coverage: Limited

**Balanced Approach** (recommended):
- Use: Core + Moderate (high confidence file)
- Data: 25-40% of corpus
- Quality: Good
- Coverage: Moderate

**Maximum Coverage** (e.g., exploration):
- Use: Core + Moderate + Weak
- Data: 60-80% of corpus
- Quality: Variable
- Coverage: Comprehensive

**Semi-Supervised**:
- Labeled: Core + Moderate
- Pseudo: Weak (with reduced weight)
- Data: All relevant chunks
- Quality: Mixed, weighted appropriately

## Expected Performance

### With Core + Moderate Training

| Metric | Expected Value |
|--------|---------------|
| Training accuracy | 85-95% |
| Validation accuracy | 80-90% |
| Core prediction accuracy | 90-95% |
| Moderate prediction accuracy | 80-90% |
| Weak prediction accuracy | 60-80% |

### Prediction Distribution

After training on high confidence data (Core + Moderate):

| Tier | Training % | Prediction % | Notes |
|------|-----------|--------------|-------|
| Core | 15% | 10-20% | Model is conservative |
| Moderate | 20% | 20-30% | Most confident predictions |
| Weak | 35% | 30-40% | Largest group |
| Context | 20% | 10-20% | Model learns to exclude |
| Noise | 10% | 5-15% | Clear exclusion |

## Troubleshooting

### Issue: Files not found
**Solution**: Run Cell 37 first to generate confidence files

### Issue: KeyError on rescaled columns
**Solution**: Ensure Cell 37 completed successfully and files contain `rescaled_<topic>` columns

### Issue: Predictions all one tier
**Solution**:
- Check training data diversity
- Verify thresholds in Cell 68
- Ensure model trained on rescaled scores

### Issue: Want to use 3-tier instead
**Solution**: Use compatibility files:
- `scores_high_confidence.csv`
- `scores_low_confidence.csv`
- `scores_no_confidence.csv`

## Key Differences: 3-Tier vs 5-Tier

### File Structure
**3-Tier**: 3 files (high, low, none)
**5-Tier**: 5 files (core, moderate, weak, context, noise) + 3 compatibility files

### Prediction Granularity
**3-Tier**: Basic classification (high/medium/low confidence)
**5-Tier**: Detailed classification (core/moderate/weak/context/noise)

### Training Flexibility
**3-Tier**: Use predefined groups
**5-Tier**: Mix and match any combination of tiers

### Analysis Depth
**3-Tier**: Basic quality assessment
**5-Tier**: Detailed quality profiling

## Summary

The notebook now supports a complete 5-tier rescaled score system:

✅ **Cell 36**: Calculates rescaled scores [0, 2]
✅ **Cell 37**: Saves 5-tier + 3-tier compatibility files
✅ **Cell 50**: Uses rescaled scores in dataset
✅ **Cell 68**: Generates 5-tier predictions

All components are consistent and use the [0, 2] rescaled range throughout.

**Recommendation**: Start with Core + Moderate (high confidence file) for training, analyze 5-tier prediction distribution, then iterate based on results.

---

## Quick Reference

### Score Ranges
- Core: 1.5-2.0
- Moderate: 1.0-1.5
- Weak: 0.5-1.0
- Context: 0.25-0.5
- Noise: 0-0.25

### Files to Use for Training
- **Standard**: `scores_high_confidence.csv` (Core + Moderate)
- **Granular**: Individual tier files as needed
- **Legacy**: Any 3-tier file for backward compatibility

### Cells to Run
1. Cell 37 → Generate files
2. Cells 41-44 → Load & prepare training data
3. Cells 47-61 → Train model
4. Cells 66-69 → Generate predictions

### Expected Timeline
- File generation (Cell 37): 1-5 minutes
- Training (Cells 47-61): 10-60 minutes depending on data size
- Predictions (Cells 66-69): 5-15 minutes

---

For detailed information, see:
- [RESCALED_SCORES_5TIER_README.md](RESCALED_SCORES_5TIER_README.md) - Complete 5-tier guide
- [QUICK_START_RESCALED_TRAINING.md](QUICK_START_RESCALED_TRAINING.md) - Step-by-step workflow
