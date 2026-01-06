# Cell 9.17: Multi-Model Chunk Shift Analysis

## Summary

Cell 9.17 (Chunk Shift Analysis) has been updated to compare **all available models** instead of just pretrained vs policy_trained.

---

## What Changed

### Before (2-Model Comparison)
- Compared only: `pretrained_bertje` vs `policy_trained`
- Single before/after visualization
- One set of shift statistics

### After (Multi-Model Comparison)
- Compares ALL available models (2, 3, or more)
- Multi-panel visualization showing all models side-by-side
- Pairwise shift analysis for all model combinations
- Combined statistics table

---

## New Features

### 1. Multi-Panel Distribution Comparison
Shows all models' chunk distributions in one visualization:
- **2 models**: 1×2 layout
- **3 models**: 1×3 layout
- **4+ models**: 2×n grid layout

**Output**: `chunk_distribution_multimodel_comparison.html`

### 2. Pairwise Shift Analysis
For each pair of models:
- Calculates shift vectors (how chunks move in embedding space)
- Generates before/after visualization
- Computes shift statistics by topic

**With 3 models** (pretrained, slavery, policy), creates:
- `chunk_shift_pretrained_bertje_to_slavery_trained.html`
- `chunk_shift_pretrained_bertje_to_policy_trained.html`
- `chunk_shift_slavery_trained_to_policy_trained.html`

### 3. Combined Statistics Table
All pairwise shifts in one CSV for comparison.

**Output**: `chunk_shift_stats_combined.csv`

**Columns**:
- `pair`: Model pair name
- `from_model`: Source model
- `to_model`: Target model
- `topic`: Primary topic
- `n_chunks`: Number of chunks
- `mean_shift`: Average shift magnitude
- `median_shift`: Median shift
- `max_shift`: Maximum shift

---

## Example with 3 Models

### Input Models:
1. **pretrained_bertje** (base)
2. **slavery_trained** (domain-adapted)
3. **policy_trained** (finetuned)

### Outputs Generated:

**Multi-Panel Comparison**:
```
chunk_distribution_multimodel_comparison.html
├─ Panel 1: pretrained_bertje (baseline distribution)
├─ Panel 2: slavery_trained (after domain adaptation)
└─ Panel 3: policy_trained (after finetuning)
```

**Pairwise Shift Visualizations**:
```
chunk_shift_pretrained_bertje_to_slavery_trained.html
  → Shows: Impact of domain adaptation

chunk_shift_pretrained_bertje_to_policy_trained.html
  → Shows: Combined impact of adaptation + finetuning

chunk_shift_slavery_trained_to_policy_trained.html
  → Shows: Impact of finetuning alone (on already adapted model)
```

**Combined Statistics**:
```csv
pair,from_model,to_model,topic,mean_shift,median_shift
pretrained_bertje_to_slavery_trained,pretrained_bertje,slavery_trained,Topic1,0.234,0.221
pretrained_bertje_to_slavery_trained,pretrained_bertje,slavery_trained,Topic2,0.189,0.176
pretrained_bertje_to_policy_trained,pretrained_bertje,policy_trained,Topic1,0.312,0.298
...
```

---

## Interpretation Guide

### Multi-Panel Comparison

**What to look for**:
- **Cluster tightness**: Are topics more separated in later models?
- **Cluster overlap**: Does training reduce topic confusion?
- **Distribution shape**: Do chunks spread differently across models?

**Example**:
```
pretrained_bertje:     [Topics overlap significantly]
slavery_trained:       [Topics start separating]
policy_trained:        [Clear topic clusters]
```
**Interpretation**: Progressive improvement in topic separation.

---

### Pairwise Shift Analysis

**Shift Magnitude Interpretation**:
- **Low shift (0.1-0.2)**: Conservative changes, subtle refinement
- **Moderate shift (0.2-0.4)**: Significant repositioning
- **High shift (>0.4)**: Major structural changes

**By Model Pair**:

#### pretrained → slavery
**Expected**: Moderate shifts
- Domain adaptation repositions chunks to reflect slavery legacy semantics
- Topics related to slavery should shift more than others

**Example**:
```
Educational_Disadvantage:  mean_shift = 0.287 (high)
Economic_Vulnerability:    mean_shift = 0.245 (moderate)
Governance_Distrust:       mean_shift = 0.198 (low)
```
**Interpretation**: Model learned more about education/economy aspects of slavery.

#### slavery → policy
**Expected**: Lower shifts
- Finetuning on policy corpus (already domain-adapted)
- Refinement rather than restructuring

**Example**:
```
Mean shift = 0.156 (low)
```
**Interpretation**: Policy finetuning made subtle adjustments.

#### pretrained → policy
**Expected**: Highest shifts (combined effect)
- Total transformation from base to specialized model

**Example**:
```
Mean shift = 0.334 (high)
```
**Interpretation**: Full model adaptation journey.

---

## Analysis Workflow

### Step 1: View Multi-Panel Comparison
Open: `chunk_distribution_multimodel_comparison.html`

**Questions to ask**:
1. Do clusters get tighter across models?
2. Does topic separation improve?
3. Are there visual differences in distributions?

### Step 2: Analyze Pairwise Shifts
Open each pairwise shift visualization.

**For each pair, check**:
1. Mean shift magnitude (overall impact)
2. Which topics shifted most (selective learning)
3. Visual before/after differences

### Step 3: Examine Statistics Table
Load: `chunk_shift_stats_combined.csv`

```python
import pandas as pd

df = pd.read_csv('Visuals/chunk_shift_stats_combined.csv')

# Compare mean shifts by pair
shift_summary = df.groupby(['from_model', 'to_model'])['mean_shift'].mean()
print(shift_summary)

# Which topics shifted most?
top_shifters = df.nlargest(10, 'mean_shift')[['from_model', 'to_model', 'topic', 'mean_shift']]
print(top_shifters)
```

---

## Thesis Integration

### Methodology Chapter

**Figure: Multi-Model Progression**
- Show: `chunk_distribution_multimodel_comparison.html`
- Caption: "Chunk embedding distributions across model stages: baseline (pretrained), domain-adapted (slavery), and finetuned (policy). Progressive clustering indicates improved topic coherence."

### Results Chapter

**Section: Model Training Impact**

**Figure 1: Domain Adaptation**
- Show: `chunk_shift_pretrained_bertje_to_slavery_trained.html`
- Caption: "Chunk repositioning after domain adaptation (mean shift = 0.234). Educational disadvantage chunks showed largest shifts, reflecting domain-specific learning."

**Figure 2: Finetuning Impact**
- Show: `chunk_shift_slavery_trained_to_policy_trained.html`
- Caption: "Refinement from finetuning (mean shift = 0.156). Smaller shifts indicate conservative adjustment on already adapted model."

**Table: Shift Statistics by Model Pair**
```
Model Pair                    | Mean Shift | Interpretation
------------------------------|------------|------------------
pretrained → slavery          | 0.234      | Domain learning
slavery → policy              | 0.156      | Finetuning
pretrained → policy (total)   | 0.334      | Full transformation
```

### Discussion Chapter

**Analysis**: "The progressive shift pattern (pretrained → slavery: 0.234; slavery → policy: 0.156) suggests that domain adaptation had a larger structural impact than subsequent finetuning. This validates the two-stage training approach..."

---

## Benefits of Multi-Model Approach

### 1. Complete Training Journey
See full progression:
- Base → Domain-adapted → Finetuned
- Understand impact of each stage
- Identify where most learning happened

### 2. Comparative Analysis
- Which model stage had biggest impact?
- Which topics were most affected by each stage?
- Quantitative evidence for training decisions

### 3. Model Selection Insights
- If slavery → policy shifts are minimal: finetuning added little
- If pretrained → slavery shifts are large: domain adaptation crucial
- Evidence-based selection of model for thesis

### 4. Validation of Approach
- Progressive improvement validates training strategy
- Large shifts without collapse show stable learning
- Topic-specific shifts show targeted learning

---

## Troubleshooting

### Issue: Only shows 2 models
**Check**:
1. Cell 7 (Chunk Embeddings) - are all models enabled?
2. `chunk_pca_2d.keys()` - which models have chunk embeddings?
3. May need to regenerate chunk embeddings for all models

### Issue: No pairwise visualizations generated
**Check**: Console output for errors during pairwise analysis

### Issue: Shifts seem too large (>1.0)
**Interpretation**: This is PCA space distance, not cosine distance. Large shifts are possible if model completely restructures embedding space.

### Issue: Negative shifts?
**Note**: Shift magnitude is always positive (Euclidean distance). If you see negative values, check the data column.

---

## Technical Notes

### PCA Space Comparison
- Each model has its own embedding space
- PCA projection is model-specific
- Shifts measured in post-PCA 2D space (for visualization)
- Different PCA spaces mean shifts are **relative**, not absolute

### Statistical Validity
- Shifts measure relative repositioning
- Mean shift = average movement across chunks
- Topic-level analysis shows selective learning
- Use for comparative analysis, not absolute metrics

---

## Summary

| Aspect | Before | After |
|--------|--------|-------|
| Models compared | 2 (pretrained vs policy) | All available (2, 3, or more) |
| Visualizations | 1 before/after | Multi-panel + all pairwise |
| Statistics | One shift metric | All pairwise shifts by topic |
| Output files | 1 HTML | 1 multi-panel + n pairwise + 1 CSV |
| Analysis depth | Basic comparison | Complete training journey |

---

*Updated: 2026-01-05*
*Cell: 9.17 (Chunk Shift Analysis)*
*Feature: Multi-model pairwise comparison*
