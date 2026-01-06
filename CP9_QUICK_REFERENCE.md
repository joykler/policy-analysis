# Checkpoint 9: Visualization Override - Quick Reference

## Quick Start

### Default Usage (Current Workflow)
```python
# Cell 75 - Leave as default
CP9_SOURCE = None
```
- Loads data from current workflow
- Saves visualizations to current workflow

### Load from Different Workflow
```python
# Cell 75 - Set source path
CP9_SOURCE = "workflow_data/Finetuned_Slavery-Slavery-policy_11.01.25_v1"
```
- Loads data from specified workflow
- Saves visualizations to current workflow

## Common Use Cases

### 1. Visualize Production Results
```python
CP9_SOURCE = "workflow_data/production_model_v1"
# Analyze production model without re-running training
```

### 2. Compare Model Versions
```python
# Run 1: Visualize baseline
CP9_SOURCE = "workflow_data/baseline_v1"
# Save as: baseline_*.html

# Run 2: Visualize new model
CP9_SOURCE = "workflow_data/improved_v2"
# Save as: improved_*.html
```

### 3. Generate Visualizations After Training
```python
# Just finished Checkpoint 8, want to re-generate visuals with different params
CP9_SOURCE = None  # Use current workflow
# Modify MIN_SCORE_THRESHOLD, N_CLUSTERS, etc. and re-run
```

## What Gets Loaded from Source

| Data Type | Folder | File | Required? |
|-----------|--------|------|-----------|
| BERTJE predictions | Bertje_labeling/ | bertje_labeled_corpus.csv | Optional |
| Cosine scores | Cosine_labeling/ | scores_all_labeled.csv | Required |
| Dictionary | Dictionary/ | Curated_dictionary.csv | Optional |
| Training metrics | Model_finetuning/ | training_metrics.json | Optional |

## What Gets Saved to Current Workflow

| Visualization | File | Description |
|---------------|------|-------------|
| 2D Clustering | Visuals/topic_clustering_2d.html | All topics in subplot grid |
| 3D Clustering | Visuals/topic_clustering_3d_*.html | One file per topic |
| Training Metrics | Visuals/training_metrics_performance.html | Bar chart of model performance |
| Metrics Table | Visuals/training_metrics_table.html | Summary table |

## Configuration Options (Cell 77)

```python
# Analysis Parameters
MIN_SCORE_THRESHOLD = 0.30  # Minimum score for high-confidence chunks
N_CLUSTERS = 5              # Number of K-means clusters per topic
PCA_COMPONENTS_2D = 2       # Components for 2D visualization
PCA_COMPONENTS_3D = 3       # Components for 3D visualization
```

**Adjust these to**:
- Change clustering granularity (N_CLUSTERS)
- Include more/fewer chunks (MIN_SCORE_THRESHOLD)
- Experiment with different visualizations

## Troubleshooting

### Error: "No scored data found"
**Solution**: Run Checkpoint 5 (Cosine Scoring) first, or set CP9_SOURCE to a workflow that has scores

### Error: "BERTJE predictions not available"
**Not an error**: Visualizations will work with cosine scores only
**To fix**: Run Checkpoint 8, or set CP9_SOURCE to workflow with BERTJE results

### Error: "No topics had enough chunks for clustering"
**Solution**: Lower MIN_SCORE_THRESHOLD in Cell 77
```python
MIN_SCORE_THRESHOLD = 0.20  # Lower threshold
```

### Visualization libraries not available
**Solution**: Install required packages
```bash
pip install matplotlib seaborn plotly scikit-learn scipy
```

## Tips & Best Practices

### 1. Organize Visualizations by Experiment
```python
# Experiment 1: Tight clustering
MIN_SCORE_THRESHOLD = 0.40
N_CLUSTERS = 3
# Run, then rename: mv topic_clustering_2d.html topic_clustering_2d_tight.html

# Experiment 2: Broad clustering
MIN_SCORE_THRESHOLD = 0.25
N_CLUSTERS = 7
# Run, then rename: mv topic_clustering_2d.html topic_clustering_2d_broad.html
```

### 2. Compare Dictionary Versions
```python
# Visualize with old dictionary
CP9_SOURCE = "workflow_data/dict_v1"

# Visualize with new dictionary
CP9_SOURCE = "workflow_data/dict_v2"

# Compare clustering patterns
```

### 3. Archive Important Visualizations
```bash
# Create archive folder
mkdir -p archive/visualizations/2025-12-22

# Copy important visuals
cp Visuals/*.html archive/visualizations/2025-12-22/
```

## Cell-by-Cell Execution

```python
# Cell 75: Set override (or leave as None)
CP9_SOURCE = None

# Cell 76: Load libraries (auto-runs)

# Cell 77: Configure & load data
# - Modify MIN_SCORE_THRESHOLD, N_CLUSTERS here if needed
# - Shows data loading status

# Cell 78: Clustering
# - Performs K-means and PCA
# - Can take 1-2 min for large datasets

# Cell 79: 2D visualization
# - Creates combined subplot view
# - Opens in browser if possible

# Cell 80: 3D visualization
# - Creates individual 3D plots per topic
# - Most interactive visualizations

# Cell 81: Training metrics
# - Only runs if CHECKPOINT 7 completed
# - Shows model performance
```

## Example Session

```python
# ======================================
# Session: Analyze baseline model
# ======================================

# 1. Set source to baseline model
CP9_SOURCE = "workflow_data/baseline_20251215"

# 2. Run Cells 76-81
# Results: Visuals/ folder contains baseline visualizations

# 3. Rename for archiving
!mv Visuals/topic_clustering_2d.html Visuals/baseline_2d.html
!mv Visuals/topic_clustering_3d_*.html Visuals/baseline_3d/

# ======================================
# Session: Analyze improved model
# ======================================

# 4. Set source to improved model
CP9_SOURCE = "workflow_data/improved_20251220"

# 5. Run Cells 76-81
# Results: New visualizations in Visuals/

# 6. Rename for archiving
!mv Visuals/topic_clustering_2d.html Visuals/improved_2d.html

# 7. Open both in browser tabs to compare side-by-side
```

## Keyboard Shortcuts (Jupyter)

- `Shift + Enter`: Run cell and move to next
- `Ctrl + Enter`: Run cell and stay
- `Alt + Enter`: Run cell and insert below
- `Esc, A`: Insert cell above
- `Esc, B`: Insert cell below
- `Esc, D, D`: Delete cell

## File Locations

```
workflow_data/
└── your_workflow_name/
    ├── Bertje_labeling/
    │   └── bertje_labeled_corpus.csv      ← Loaded by CP9
    ├── Cosine_labeling/
    │   └── scores_all_labeled.csv         ← Loaded by CP9
    ├── Dictionary/
    │   └── Curated_dictionary.csv         ← Loaded by CP9
    ├── Model_finetuning/
    │   └── training_metrics.json          ← Loaded by CP9
    └── Visuals/                           ← Output by CP9
        ├── topic_clustering_2d.html
        ├── topic_clustering_3d_*.html
        ├── training_metrics_performance.html
        └── training_metrics_table.html
```

## Next Steps After CP9

1. **Review Visualizations**: Open HTML files in browser
2. **Analyze Patterns**: Look for clustering quality, topic separation
3. **Validate Results**: Check if high-scoring chunks make semantic sense
4. **Document Findings**: Note any issues or insights
5. **Iterate if Needed**: Adjust dictionary, re-run earlier checkpoints
6. **Archive**: Save important visualizations with descriptive names

## Related Documentation

- Full guide: `CHECKPOINT_9_OVERRIDE_UPDATE.md`
- Workflow README: `README_V24.md` (or latest)
- Original analysis: Review of visualization checkpoint implementation
