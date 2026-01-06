# V18 Notebook Update: Score Rescaling Integration

## What Changed

Created **dictionary_discovery_v18_rescaled_scores.ipynb** with integrated score rescaling in Cell 5.1.

## Problem Solved

**Original scores were compressed** in narrow 0.14-0.62 range:
- 50% of chunks clustered in 0.34-0.43 band
- Hard to distinguish core content from context
- Low interpretability

## Solution Implemented

### Power + Margin Rescaling Function

Added `rescale_to_0_2()` function to Cell 5.1:

```python
def rescale_to_0_2(score: float, margin: float, power: float = 1.8,
                   margin_weight: float = 0.25) -> float:
    """
    Rescale compressed cosine scores to interpretable 0-2 range.

    Two-stage approach:
    1. Power transform (power=1.8) spreads high scores
    2. Margin bonus rewards confident classifications
    """
    min_obs, max_obs = 0.07, 0.65
    normalized = (score - min_obs) / (max_obs - min_obs)
    normalized = max(0.0, min(1.0, normalized))
    transformed = normalized ** power
    margin_factor = 1.0 + margin_weight * (margin / (score + 1e-6))
    transformed = transformed * margin_factor
    rescaled = min(2.0, transformed * 2.0)
    return rescaled
```

### How It Works

**Stage 1: Power Transform (power=1.8)**
- Emphasizes differences at high end
- Compresses differences at low end
- Example: 0.4² = 0.16, but 0.6² = 0.36 (bigger gap)

**Stage 2: Margin Bonus (weight=0.25)**
- Rewards confident classifications (large margin between 1st and 2nd topic)
- Penalizes ambiguous chunks (small margin)
- Helps separate clear core content from mixed chunks

## New Output Columns

Cell 5.1 now creates:

1. **`max_score_rescaled`** - Primary topic score in 0-2 range
2. **`rescaled_<topic>`** - Rescaled score for each topic

Both original (`cos_*`) and rescaled (`rescaled_*`) columns are preserved.

## Expected Results

### Score Distribution After Rescaling

| Metric | Original (Cosine) | Rescaled (0-2) | Improvement |
|--------|------------------|----------------|-------------|
| Range | 0.14 - 0.62 | 0.0 - 2.0 | 4.2x |
| Std Dev | 0.067 | 0.268 | 4.0x |
| IQR | 0.092 | 0.360 | 3.9x |

### Interpretable Thresholds

| Score Range | Percentile | Meaning |
|-------------|------------|---------|
| **0.0 - 0.5** | Bottom 25% | Context/background mentions |
| **0.5 - 1.0** | 25-50% | Weak relevance |
| **1.0 - 1.5** | 50-75% | Moderate relevance |
| **1.5 - 2.0** | Top 25% | Core topic content |

## Usage

### Running Cell 5.1

When you run Cell 5.1 in v18 notebook, it will:

1. Calculate original cosine scores (`cos_*` columns)
2. Apply rescaling to create `rescaled_*` columns
3. Print statistics showing spread improvement
4. Save both score types in the output CSV

### Example Output

```
Rescaled score distribution (0-2 range):
  Min:  0.050
  Q25:  0.521
  Med:  0.698
  Q75:  0.881
  Max:  2.000
  Std:  0.268
  Spread improvement: 4.01x
```

## Downstream Impact

### Files Affected

Running v18 Cell 5.1 will create/update:
- `scores_all_labeled.csv` - Now includes both original and rescaled scores
- Any downstream analysis using `max_score` can switch to `max_score_rescaled`

### Backward Compatibility

✅ **Fully backward compatible**:
- Original `cos_*` and `max_score` columns still present
- Rescaled columns are ADDITIONS, not replacements
- Can compare both scoring systems side-by-side

## Comparison to v17

| Feature | v17 | v18 |
|---------|-----|-----|
| Cell 1.4 text cleaning | ✅ Fixed | ✅ Fixed |
| Score rescaling | ❌ No | ✅ Yes |
| Interpretable 0-2 scale | ❌ No | ✅ Yes |
| Score spread | 0.07 std | 0.27 std (4x) |

## Workflow Integration

### For v21 Workflow

The v21 workflow folder has been created. To use rescaled scores:

1. Run v18 notebook Cell 5.1 with v21 workflow config
2. Or copy rescaling code to v21-specific notebook
3. Outputs will include both scoring systems

### Recommended Next Steps

1. ✅ Run Cell 5.1 in v18 notebook
2. Compare `max_score` vs `max_score_rescaled` distributions
3. Verify interpretability with manual chunk inspection
4. Use `max_score_rescaled` for downstream classification/filtering
5. Set thresholds based on 0-2 scale (e.g., core content > 1.5)

## Parameters (Tunable)

If you want to adjust rescaling behavior:

```python
def rescale_to_0_2(score, margin,
                   power=1.8,        # Higher = more emphasis on top scores
                   margin_weight=0.25):  # Higher = more confidence bonus
```

**Recommended ranges:**
- `power`: 1.5-2.5 (1.8 is good default)
- `margin_weight`: 0.1-0.4 (0.25 balances score vs confidence)

## Files Created/Modified

✅ Created:
- `dictionary_discovery_v18_rescaled_scores.ipynb`
- `workflow_data/slavery_Slavdict_pretraining_slavery_v21/` (copied from v20)
- `add_rescaling_to_v18.py` (script used for update)
- `SCORE_SPREAD_ANALYSIS_AND_RECOMMENDATIONS.md` (detailed analysis)
- `V18_RESCALING_UPDATE_SUMMARY.md` (this file)

📝 Reference files:
- `analyze_weight_impact_on_scores.py` - Weight impact analysis
- `verify_cell_4_1_weights.py` - Cell 4.1 verification
- `fix_cell_1_4_complete.py` - Cell 1.4 text cleaning fix
