# Checkpoint 9: Complete Visualization Suite - User Guide

## Overview

Checkpoint 9 provides comprehensive visualizations for analyzing your policy dictionary and model performance. It consists of **three major visualization suites**:

1. **Cross-Topic Chunk Analysis** (Cells 9.3-9.5)
2. **Dictionary Term Visualization** (Cells 9.6-9.8)
3. **Model Performance Metrics** (Cell 9.9)

## Quick Start

```python
# 1. Set data source
CP9_SOURCE = None  # Or path to different workflow

# 2. Configure threshold
MIN_SCORE_THRESHOLD = 0.30  # Adjust as needed

# 3. Run all visualization cells
# Execute Cells 9.1 → 9.9

# 4. Open output files
# Visuals/cross_topic_space_2d.html
# Visuals/dictionary_terms_comparison_2d.html
# Visuals/training_metrics_performance.html
```

## Complete Cell Structure

```
Cell 74:  📌 CHECKPOINT 9: Visualizations (Header)

Cell 75:  🔧 CP9: Workflow Source Override
          └─ Set CP9_SOURCE to load from different workflow

Cell 76:  📚 CELL 9.1: Setup Visualization Libraries
          └─ Import matplotlib, seaborn, plotly, sklearn

Cell 77:  📊 CELL 9.2: Configuration & Data Loading
          ├─ Load cosine scores (required)
          ├─ Merge BERTJE predictions (if available)
          ├─ Load dictionary
          └─ Load training metrics

Cell 78:  🎯 CELL 9.3: Cross-Topic Semantic Space Preparation
          ├─ Calculate topic centroids
          ├─ PCA dimensionality reduction
          └─ Distance to centroids

Cell 79:  📈 CELL 9.4: 2D Cross-Topic Visualization
          └─ Output: cross_topic_space_2d.html

Cell 80:  📦 CELL 9.5: 3D Cross-Topic Visualization
          └─ Output: cross_topic_space_3d.html

Cell 81:  📖 CELL 9.6: Dictionary Embeddings Generation
          ├─ Load pre-training model
          ├─ Load post-training model
          └─ Generate embeddings for all terms

Cell 82:  📊 CELL 9.7: 2D Dictionary Visualization
          └─ Output: dictionary_terms_comparison_2d.html

Cell 83:  📦 CELL 9.8: 3D Dictionary with Shift Analysis
          └─ Output: dictionary_terms_shifts_3d.html

Cell 84:  📊 CELL 9.9: Training Metrics Visualization
          └─ Output: training_metrics_performance.html

Cell 85:  ✅ CHECKPOINT 9 COMPLETE (Marker)
```

## Visualization Suite 1: Cross-Topic Chunks

### Purpose
Show how **policy chunks** are distributed across topics and how they relate to topic centroids.

### What You See

**2D Visualization** (cross_topic_space_2d.html):
- **Points**: Policy chunks colored by primary topic
- **Stars**: Topic centroids (average position per topic)
- **Layout**: Single unified space showing all topics
- **Axes**: PC1 (x) vs PC2 (y) from PCA

**3D Visualization** (cross_topic_space_3d.html):
- **Points**: Same chunks in 3D space
- **Rotation**: Interactive exploration
- **Axes**: PC1, PC2, PC3
- **Better separation**: Topics may separate better in 3D

### Key Insights

✅ **Good Signs**:
- Tight clusters around centroids
- Clear separation between topics
- Few chunks between centroids
- High variance explained (>60%)

⚠️ **Warning Signs**:
- Overlapping centroids (topics too similar)
- Dispersed clouds (topics too broad)
- Many boundary chunks (multi-topic confusion)
- Low variance explained (<40%)

### Use Cases
1. Validate topic distinctiveness
2. Identify overlapping topics
3. Find multi-topic content
4. Detect outliers/noise
5. Compare dictionary versions

## Visualization Suite 2: Dictionary Terms

### Purpose
Show how **dictionary terms** (seeds + expanded) are positioned in semantic space, with pre/post training comparison.

### What You See

**2D Comparison** (dictionary_terms_comparison_2d.html):
```
┌────────────────────┬────────────────────┐
│  Pre-Training      │  Post-Training     │
│  ◆ Seed terms      │  ◆ Seed terms      │
│  ○ Expanded terms  │  ○ Expanded terms  │
└────────────────────┴────────────────────┘
```

**3D Shift Analysis** (dictionary_terms_shifts_3d.html):
- **Light circles**: Pre-training positions
- **Bold diamonds**: Post-training positions
- **Red arrows**: Shift vectors (significant changes)
- **Top shifters**: Terms that moved most

### Key Insights

**Tight Seed-Expanded Clustering**:
```
◆ (seed) with ○ ○ ○ (expanded) nearby
→ Good expansion quality
```

**Large Shifts**:
```
Pre: ◆ ────→ Post: ◆
→ Model learned new context for term
```

**Cross-Topic Terms**:
```
◆ positioned between two topic clusters
→ Genuinely multi-topic term
```

### Use Cases
1. Validate dictionary quality
2. Identify problematic expanded terms
3. Analyze training impact
4. Find topic overlaps
5. Detect mislabeled terms

## Visualization Suite 3: Model Performance

### Purpose
Show how well the BERTJE model learned to predict topic scores.

### What You See

**Performance Chart** (training_metrics_performance.html):
- **Bars**: Correlation (r) and MAE per topic
- **Green line**: Mean correlation across topics
- **Topics**: Performance varies by topic

### Key Metrics

**Correlation (r)**:
- **>0.70**: Excellent (strong agreement)
- **0.50-0.70**: Good (moderate agreement)
- **<0.50**: Poor (weak agreement)

**MAE (Mean Absolute Error)**:
- **<0.10**: Excellent (predictions very close)
- **0.10-0.20**: Good (reasonable accuracy)
- **>0.20**: Poor (large prediction errors)

### Use Cases
1. Validate model training success
2. Identify difficult topics
3. Compare model versions
4. Decide if more training needed

## Complete Workflow Example

```python
# =====================================
# SCENARIO: Analyze new dictionary v3
# =====================================

# --- STEP 1: Generate Visualizations ---
CP9_SOURCE = None  # Current workflow
MIN_SCORE_THRESHOLD = 0.30

# Run Cells 9.1-9.9
# ⏱️ ~5-10 minutes total

# --- STEP 2: Review Chunk Visualizations ---
# Open: cross_topic_space_2d.html

# Finding 1: "Poverty" and "Education" centroids very close
# Action: Investigate if topics should be merged or better distinguished

# Finding 2: ~150 chunks far from all centroids
# Action: Review outlier chunks, may need filtering

# --- STEP 3: Review Dictionary ---
# Open: dictionary_terms_comparison_2d.html

# Finding 1: In post-training, "onderwijs" cluster tighter
# Interpretation: Training improved topic coherence

# Finding 2: "discriminatie" term shifted significantly
# Open: dictionary_terms_shifts_3d.html to investigate

# Shift magnitude: 0.42 (large)
# Direction: From "Social Fragmentation" toward "Governance"
# Action: Review corpus usage of "discriminatie"

# --- STEP 4: Review Model Performance ---
# Open: training_metrics_performance.html

# Finding: "Governance" topic has r=0.45 (low)
# Interpretation: Model struggles with this topic
# Action: Add more distinctive seed terms for "Governance"

# --- STEP 5: Iterate ---
# Based on findings, update dictionary:
#   1. Add "bestuurscultuur", "overheidsoptreden" to Governance
#   2. Remove "discriminatie" (too ambiguous)
#   3. Consider merging "Poverty" and "Education"

# Re-run from Checkpoint 3
# Re-visualize with Checkpoint 9
# Compare results
```

## Configuration Guide

### Adjust Chunk Inclusion Threshold

```python
# Cell 9.2
MIN_SCORE_THRESHOLD = 0.30  # Default

# More inclusive (more chunks, potentially noisier)
MIN_SCORE_THRESHOLD = 0.20

# More conservative (fewer chunks, clearer patterns)
MIN_SCORE_THRESHOLD = 0.40
```

**Impact**:
- Lower → More chunks in visualization, broader patterns
- Higher → Fewer chunks, tighter clusters, clearer topics

### Load from Different Workflow

```python
# Cell 9.1
CP9_SOURCE = None  # Current workflow (default)

# Load from production model
CP9_SOURCE = "workflow_data/production_model_v1"

# Compare old dictionary
CP9_SOURCE = "workflow_data/baseline_dict_v0"
```

**Impact**:
- Can visualize any completed workflow
- Data loaded from `CP9_SOURCE`
- Visualizations saved to current workflow

### Customize Visualization Colors

```python
# Cell 9.4, 9.7
# Default: Plotly Set3 + Pastel
color_palette = px.colors.qualitative.Set3

# Use different palette
color_palette = px.colors.qualitative.Vivid
# Or: Bold, Pastel, Safe, Set1, Set2, Dark2, etc.
```

### Adjust PCA Components

```python
# Cell 9.3
PCA_COMPONENTS_2D = 2  # Fixed for 2D
PCA_COMPONENTS_3D = 3  # Fixed for 3D

# Generally don't change these
# But could increase 3D to 4+ for analysis
# (though can't visualize >3D)
```

## Output Files Summary

### Chunk Visualizations
| File | Type | Shows | When |
|------|------|-------|------|
| `cross_topic_space_2d.html` | 2D scatter | All chunks + centroids | Always |
| `cross_topic_space_3d.html` | 3D scatter | All chunks + centroids | Always |

### Dictionary Visualizations
| File | Type | Shows | When |
|------|------|-------|------|
| `dictionary_terms_comparison_2d.html` | 2D side-by-side | Pre vs post training | Both models available |
| `dictionary_terms_base_2d.html` | 2D single | Pre-training only | Only base model |
| `dictionary_terms_trained_2d.html` | 2D single | Post-training only | Only trained model |
| `dictionary_terms_shifts_3d.html` | 3D with arrows | Shift vectors | Both models available |
| `dictionary_terms_base_3d.html` | 3D single | Pre-training only | Only base model |
| `dictionary_terms_trained_3d.html` | 3D single | Post-training only | Only trained model |

### Performance Metrics
| File | Type | Shows | When |
|------|------|-------|------|
| `training_metrics_performance.html` | Bar chart | Correlation + MAE per topic | Training completed |
| `training_metrics_table.html` | Table | Summary statistics | Training completed |

## Troubleshooting

### Issue: "No topic score columns found"
**Fix**: Cell 9.2 now automatically loads cosine scores first ✅

### Issue: "Visualization libraries not available"
**Fix**:
```bash
pip install matplotlib seaborn plotly scikit-learn scipy
```

### Issue: "Too few high-confidence chunks"
**Fix**: Lower `MIN_SCORE_THRESHOLD` to 0.20 or 0.25

### Issue: "BERTJE model failed to load"
**Fix**: Ensure Checkpoint 7 completed successfully, or will use default GroNLP model

### Issue: Low PCA variance (<50%)
**Interpretation**: Topics are high-dimensional, visualization is rough approximation
**Action**: Rely more on score metrics, less on visual clustering

### Issue: Visualizations not updating
**Fix**:
1. Clear browser cache
2. Ensure cells executed in order
3. Check for error messages in cell outputs

## Interpretation Examples

### Example 1: Well-Separated Topics

**Observation in cross_topic_space_2d.html**:
```
⭐ Education    far from    ⭐ Governance
   • • •                      • • •
   • • •                      • • •
```

**Interpretation**: ✅ Topics are distinct and well-defined

**Action**: None needed, dictionary is working well

---

### Example 2: Overlapping Topics

**Observation**:
```
⭐ Poverty  ⭐ Education
   • • • • •
   • • • • •
```

**Interpretation**: ⚠️ Topics semantically overlap

**Action**:
1. Review if topics should be merged
2. Add more distinctive seed terms
3. Check if corpus genuinely conflates these topics

---

### Example 3: Large Dictionary Shift

**Observation in dictionary_terms_shifts_3d.html**:
```
Pre:  ◆ werkloosheid
         ↓ (large arrow)
Post:    ◆ werkloosheid
```

**Interpretation**: Training changed representation significantly

**Possible Reasons**:
1. ✅ Multi-topic term resolved to primary topic
2. ⚠️ Term was mislabeled in dictionary
3. ℹ️ Corpus uses term differently than expected

**Action**: Review corpus usage of this term

---

### Example 4: Poor Model Performance

**Observation in training_metrics_performance.html**:
```
Governance Distrust: r=0.42, MAE=0.25
```

**Interpretation**: ⚠️ Model struggles with this topic

**Possible Causes**:
1. Too few training examples
2. Topic too broad or ambiguous
3. Seed terms not distinctive
4. Topic genuinely difficult

**Action**:
1. Review training data distribution
2. Add more distinctive seed terms
3. Consider splitting into subtopics
4. Collect more examples if possible

## Best Practices

### 1. Run in Order
```
Always: Cell 9.1 → 9.2 → ... → 9.9
Don't skip cells or run out of order
```

### 2. Review All Three Suites
```
Chunks → Dictionary → Metrics
Each provides different insights
Together they tell complete story
```

### 3. Take Screenshots
```
Document findings with:
- Screenshots of visualizations
- Notes on patterns observed
- Action items for dictionary improvement
```

### 4. Iterate
```
Visualize → Identify issues → Revise dictionary → Re-run
Not a one-time analysis, but iterative refinement
```

### 5. Compare Over Time
```
Save visualizations with version numbers:
- cross_topic_space_2d_v1.html
- cross_topic_space_2d_v2.html
Track improvements across iterations
```

## Advanced Usage

### Compare Multiple Dictionaries

```python
# Dictionary v1
CP9_SOURCE = "workflow_data/dict_v1"
# Run Cells 9.6-9.8
# Save as: dict_v1_*.html

# Dictionary v2
CP9_SOURCE = "workflow_data/dict_v2"
# Run Cells 9.6-9.8
# Save as: dict_v2_*.html

# Open both in browser tabs
# Use browser: Window → Tile Windows Vertically
# Compare side-by-side
```

### Analyze Specific Topic

```python
# After Cell 9.3
# Filter to single topic
topic_of_interest = "Educational Disadvantage & Brain Drain"
df_single_topic = cross_topic_viz_data['df'][
    cross_topic_viz_data['df']['primary_topic'] == topic_of_interest
]

# Analyze this topic specifically
print(f"Chunks: {len(df_single_topic)}")
print(f"Avg distance to centroid: {df_single_topic['distance_to_centroid'].mean():.3f}")
print(f"Avg score margin: {df_single_topic['score_margin'].mean():.3f}")
```

### Export Data for External Analysis

```python
# After Cell 9.3
# Save chunk positions and metadata
cross_topic_viz_data['df'].to_csv('chunk_positions_2d.csv', index=False)

# After Cell 9.6
# Save dictionary embeddings
np.save('dict_embeddings_base.npy', dict_viz_data['base']['embeddings'])
np.save('dict_embeddings_trained.npy', dict_viz_data['trained']['embeddings'])

# Use in other tools (R, SPSS, custom scripts)
```

## Related Documentation

- **Detailed Guides**:
  - `CP9_CROSS_TOPIC_VISUALIZATION.md` - Chunk visualizations
  - `CP9_DICTIONARY_VISUALIZATION.md` - Dictionary visualizations
  - `CP9_UPDATE_SUMMARY.md` - What changed in v24.1

- **Quick References**:
  - `CP9_QUICK_REFERENCE.md` - Common use cases
  - `CHECKPOINT_9_OVERRIDE_UPDATE.md` - Override functionality

## Version Information

- **Notebook**: `A__dictionary_discovery_v24_unified_embedding.ipynb`
- **Version**: v24.1
- **Date**: 2025-12-22
- **Features**: Cross-topic chunks + Dictionary terms + Pre/Post comparison

## Summary

Checkpoint 9 provides **three complementary visualization suites** that together give you complete insight into:

1. **How your corpus chunks relate to topics** (cross-topic space)
2. **How your dictionary terms cluster and evolve** (with training)
3. **How well your model learned** (performance metrics)

Use all three together to:
- ✅ Validate dictionary quality
- ✅ Identify topic overlaps
- ✅ Evaluate training impact
- ✅ Guide dictionary refinement
- ✅ Make data-driven improvements

**Start exploring your visualizations now!** 🎉
