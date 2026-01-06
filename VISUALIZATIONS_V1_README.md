# Visualizations v1 - Standalone Notebook

## Overview

**A___Visualizations_v1.ipynb** is a standalone visualization notebook that can run independently from the main training workflow. It generates comprehensive visualizations for dictionary fitness, model performance, and topic coherence analysis.

---

## Key Features

- **Independent Workflow**: No dependencies on the main training notebook
- **Configurable Source**: Point to any completed workflow directory
- **Flexible Model Comparison**: Enable/disable models (base_cosine, pretrained_bertje, slavery_trained, policy_trained)
- **Metadata Filtering**: Filter by doc_type, year_range, doc_folder
- **34 Comprehensive Visualizations**: All CP9 visualizations from v26
- **Auto-Setup**: Automatically creates output directory (Visuals/)

---

## Quick Start

### 1. Set Source Workflow

In **Cell 1 (Configuration)**, set the source workflow path (where your Dictionary and Cosine scores are):

```python
SOURCE_WORKFLOW = "workflow_data/Policy_Slavdict_FT-slavery_slavery_v1"
```

Or use `None` to load from current directory:

```python
SOURCE_WORKFLOW = None
```

### 2. Set Model Paths (IMPORTANT)

**Set paths to Model_finetuning folders** - these can be from ANY workflow directory:

```python
MODEL_PATHS = {
    'pretrained_bertje': 'GroNLP/bert-base-dutch-cased',  # HuggingFace (automatic)
    'slavery_trained': 'workflow_Structureddict/slavery_structured-slavdict_pretrained_slavery_v1/Model_finetuning',
    'policy_trained': 'workflow_data/Policy_Slavdict_FT-slavery_slavery_v1/Model_finetuning'
}
```

**How it works**:
- Point to the `Model_finetuning/` folder (not the specific model subdirectory)
- The notebook automatically finds the best model inside (searches: `trained_encoder/`, `SBERTContinuousMultiLabel/`, `full_model/`)
- Models can be from different workflows than SOURCE_WORKFLOW

### 3. Configure Models to Compare

```python
COMPARE_MODELS = {
    'base_cosine': True,          # Dictionary-based cosine scores
    'pretrained_bertje': True,    # GroNLP/bert-base-dutch-cased
    'slavery_trained': False,     # Set True if you have this model
    'policy_trained': True        # Set True if you have this model
}
```

**Important**: If you enable `slavery_trained` or `policy_trained`, you MUST set the corresponding path in `MODEL_PATHS`.

### 4. Apply Metadata Filters (Optional)

```python
METADATA_FILTERS = {
    'doc_type': ['policy', 'report'],  # Or None for all
    'year_range': (2015, 2024),        # Or None for all
    'doc_folder': None                  # Or specific folder
}
```

### 5. Run All Cells

Execute all cells to generate visualizations. Outputs will be saved to `Visuals/` directory.

---

## Required Data Files

The notebook expects the following structure in the source workflow directory:

### Required Folders:
- `Dictionary/`
  - `Curated_dictionary.csv` - Dictionary terms with weights, categories
- `Cosine_labeling/`
  - `scores_all_labeled.csv` - Chunk scores from cosine similarity
- `Other_data/`
  - `chunked_corpus.csv` - Chunk metadata (doc_type, year, text)

### Optional Folders (in SOURCE_WORKFLOW):
- `BERTJE_predictions/`
  - `bertje_*_predictions_*.csv` - BERTJE predictions (for Section 6)

### Model Locations (can be ANYWHERE):
- **Policy-trained model**: Set `MODEL_PATHS['policy_trained']` to exact path
  - Example: `workflow_data/Policy_Slavdict_FT-slavery_slavery_v1/Model_finetuning/trained_encoder`
- **Slavery-trained model**: Set `MODEL_PATHS['slavery_trained']` to exact path
  - Example: `workflow_data/slavery_Slavdict_pretraining_slavery_v13/Model_finetuning/slavery_domain_encoder`
- **Training metrics** (optional): In policy-trained model's parent directory
  - Example: `workflow_data/.../Model_finetuning/training_metrics.json`

### Auto-Created:
- `Visuals/` - All visualization outputs (HTML, PNG, CSV)

---

## Notebook Structure

**Total Cells**: 36

### Setup Cells (0-2):
- **Cell 0**: Header & Documentation (Markdown)
- **Cell 1**: Configuration (Code)
- **Cell 2**: Filesystem Setup (Code)

### Visualization Cells (3-35):

**Section 1: Setup & Data Loading** (Cells 3-7)
- Source override configuration
- Visualization configuration variables
- Import libraries
- Load core data (dictionary, cosine scores, chunked corpus)
- Apply metadata filters

**Section 2: Model Embeddings Generation** (Cells 8-10)
- Load BERTJE models (pretrained, slavery-trained, policy-trained)
- Generate dictionary term embeddings
- Generate chunk embeddings (sampled)

**Section 3: Dictionary Fitness Visualizations** (Cells 11-15)
- Weight tier validation (boxplot)
- Expansion quality validation (2D scatter)
- Dictionary term clustering - 2D multi-model
- Dictionary term clustering - 3D exploration

**Section 4: Topic Coherence & Model Performance** (Cells 16-19)
- Cluster quality metrics table & chart
- Topic separation heatmap (confusion matrix)
- Training metrics visualization

**Section 5: Chunk Scoring Analysis** (Cells 20-27)
- PCA preparation
- Chunk clustering 2D - multi-model
- Chunk clustering 3D - exploration
- Chunk shift analysis - pre/post training
- Chunk shift vectors (top shifters)
- Score distribution by topic (violin plots)
- Multi-label distribution analysis

**Section 6: Score Distribution Analysis** (Cells 28-30)
- Cosine vs. BERTJE score comparison (scatter matrix)
- Score agreement analysis (correlation heatmap)

**Section 7: Thesis-Specific Visualizations** (Cells 31-33, optional)
- Temporal analysis - topics over time
- Document type analysis - topics by type

**Section 8: Summary & Export** (Cells 34-35)
- Visualization summary & inventory
- Export configuration snapshot

---

## Generated Outputs

All outputs are saved to `Visuals/` directory:

### Interactive Visualizations (HTML):
- `weight_tier_validation.html`
- `expansion_quality_2d.html`
- `dict_clustering_2d_multimodel.html`
- `dict_clustering_3d.html`
- `cluster_quality_metrics.html`
- `topic_separation_heatmap.html`
- `training_metrics.html`
- `chunk_clustering_2d_multimodel.html`
- `chunk_clustering_3d.html`
- `chunk_shift_before_after.html`
- `chunk_shift_vectors.html`
- `score_distribution_by_topic.html`
- `multilabel_distribution.html`
- `cosine_vs_bertje_comparison.html`
- `score_agreement_heatmap.html`
- `temporal_analysis_topics_over_time.html`
- `doctype_analysis_topics_by_type.html`

### Static Visualizations (PNG, if enabled):
- Same names as HTML files with `.png` extension

### Data Tables (CSV):
- `cluster_metrics_table.csv`
- `per_topic_tightness.csv`
- `chunk_shift_by_topic.csv`
- `score_statistics_by_topic.csv`
- `cosine_bertje_correlations.csv`
- `cosine_bertje_disagreements.csv`
- `temporal_topic_scores.csv`
- `doctype_topic_scores.csv`
- `visualization_inventory.csv`

### Configuration:
- `cp9_configuration.json` - Full configuration snapshot with timestamp

---

## Configuration Options

### Model Comparison

```python
COMPARE_MODELS = {
    'base_cosine': True,          # Always available (uses existing scores)
    'pretrained_bertje': True,    # Generates embeddings on-the-fly
    'slavery_trained': False,     # Requires model in Model_finetuning/slavery_domain_encoder
    'policy_trained': True        # Requires model in Model_finetuning/trained_encoder
}
```

**Note**: Setting a model to `True` requires either:
1. The model files exist in the source workflow
2. The model is available on HuggingFace (pretrained_bertje)

### Visualization Settings

```python
MIN_SCORE_THRESHOLD = 0.3        # Minimum score for "relevant" classification
TOP_N_SHIFTERS = 100             # How many top-shifting chunks to visualize
SAMPLE_SIZE_3D = 1000            # Max chunks for 3D plots (performance limit)
PCA_RANDOM_STATE = 42            # For reproducibility
FIGURE_DPI = 150                 # Figure resolution
```

### Output Settings

```python
SAVE_INTERACTIVE = True          # Save HTML plots (interactive, recommended)
SAVE_STATIC = False              # Save PNG/PDF for thesis (requires kaleido package)
SHOW_IN_NOTEBOOK = True          # Display plots inline in Jupyter
```

---

## Error Handling

The notebook uses a `VIZ_AVAILABLE` flag for graceful error handling:

- If critical data files are missing, `VIZ_AVAILABLE` is set to `False`
- Subsequent sections check this flag and skip with informative messages
- Optional sections (BERTJE comparison, training metrics) skip gracefully if data unavailable

---

## Performance Notes

### GPU Acceleration
- If CUDA-enabled GPU available, BERTJE embedding generation will use GPU
- CPU fallback is automatic
- Expected runtime (GPU): 20-30 minutes
- Expected runtime (CPU): 60-90 minutes

### Memory Requirements
- Full dataset: ~4-8 GB RAM
- Sampled (SAMPLE_SIZE_3D=1000): ~2-4 GB RAM
- Reduce `SAMPLE_SIZE_3D` if memory issues occur

### File Size
- Interactive HTML files: ~500 KB - 5 MB each
- Static PNG files: ~100 KB - 2 MB each
- Total output: ~50-200 MB depending on configuration

---

## Differences from Main Workflow (v26)

### What's the Same:
- All 34 CP9 visualizations identical
- Same analysis logic and calculations
- Same output format and quality

### What's Different:
- **Standalone**: No dependency on cells 1-72 of v26
- **Configurable Source**: Can point to any workflow directory
- **Simplified Setup**: Only 3 setup cells vs. full workflow
- **Independent Execution**: Can re-run visualizations without re-training models

---

## Use Cases

### 1. Re-visualize Existing Workflow
After completing a workflow run, generate visualizations without re-running training:

```python
SOURCE_WORKFLOW = "workflow_data/Policy_Slavdict_FT-slavery_slavery_v1"
```

### 2. Compare Different Workflows
Point to different workflow directories to compare results:

```python
# Run 1: Visualize workflow v1
SOURCE_WORKFLOW = "workflow_data/Policy_Slavdict_FT-slavery_slavery_v1"

# Run 2: Visualize workflow v2
SOURCE_WORKFLOW = "workflow_data/Policy_Slavdict_FT-slavery_slavery_v2"
```

### 3. Filtered Analysis
Apply different metadata filters without modifying source data:

```python
# Analyze only policies from 2020-2024
METADATA_FILTERS = {
    'doc_type': ['policy'],
    'year_range': (2020, 2024),
    'doc_folder': None
}
```

### 4. Thesis Preparation
Generate publication-ready static images:

```python
SAVE_INTERACTIVE = True   # For exploration
SAVE_STATIC = True        # For thesis inclusion
SHOW_IN_NOTEBOOK = True   # For review
```

---

## Troubleshooting

### Issue: "Source workflow directory not found"
**Solution**: Check `SOURCE_WORKFLOW` path in Cell 1. Use absolute path or path relative to notebook location.

### Issue: "Missing required folders"
**Solution**: Ensure source workflow has `Dictionary/`, `Cosine_labeling/`, and `Other_data/` folders.

### Issue: "No embedding models loaded"
**Solution**:
- Check `COMPARE_MODELS` configuration
- **IMPORTANT**: If `slavery_trained` or `policy_trained` are enabled, you MUST set their paths in `MODEL_PATHS`
- Set exact full paths: `MODEL_PATHS['policy_trained'] = 'workflow_data/.../Model_finetuning/trained_encoder'`
- For pretrained_bertje, ensure internet connection for HuggingFace download

### Issue: "policy_trained enabled but MODEL_PATHS['policy_trained'] is None"
**Solution**:
- In Cell 1, set the exact path to your policy-trained model:
  ```python
  MODEL_PATHS['policy_trained'] = 'workflow_data/Policy_Slavdict_FT-slavery_slavery_v1/Model_finetuning/trained_encoder'
  ```
- The path can be from ANY workflow, not just SOURCE_WORKFLOW

### Issue: "Out of memory"
**Solution**: Reduce `SAMPLE_SIZE_3D` from 1000 to 500 or 250

### Issue: "BERTJE comparison skipped"
**Solution**: This is expected if `BERTJE_predictions/` folder doesn't exist or is empty. This section is optional.

---

## Dependencies

### Required Python Packages:
```
pandas
numpy
pathlib (built-in)
json (built-in)
matplotlib
seaborn
plotly
scikit-learn
scipy
transformers  # For BERTJE models
torch         # For BERTJE models
tqdm          # For progress bars
```

### Optional Packages:
```
kaleido       # For static PNG/PDF export (if SAVE_STATIC = True)
```

### Installation:
```bash
pip install pandas numpy matplotlib seaborn plotly scikit-learn scipy transformers torch tqdm
pip install kaleido  # Optional, for static exports
```

---

## Thesis Integration

### Recommended Workflow:

1. **Exploration Phase**: Run with `SAVE_INTERACTIVE = True` to explore data
2. **Analysis Phase**: Review HTML visualizations, identify key findings
3. **Documentation Phase**: Enable `SAVE_STATIC = True` for thesis figures
4. **Selection**: Choose most relevant visualizations for thesis chapters

### Recommended Visualizations for Thesis:

**Chapter: Methodology**
- `dict_clustering_2d_multimodel.html` - Shows dictionary structure
- `weight_tier_validation.html` - Validates weighting methodology

**Chapter: Results - Dictionary Quality**
- `expansion_quality_2d.html` - Validates expansion approach
- `cluster_quality_metrics.html` - Quantitative validation

**Chapter: Results - Model Performance**
- `topic_separation_heatmap.html` - Topic confusion analysis
- `training_metrics.html` - Model convergence

**Chapter: Results - Document Analysis**
- `temporal_analysis_topics_over_time.html` - IDPAD decade trends
- `doctype_analysis_topics_by_type.html` - Document type patterns

**Chapter: Discussion**
- `chunk_shift_before_after.html` - Model learning visualization
- `cosine_vs_bertje_comparison.html` - Method validation

---

## Version History

### v1 (2026-01-04)
- Initial standalone visualization notebook
- All 34 CP9 visualizations from v26
- Independent filesystem configuration
- Flexible source workflow selection
- Comprehensive documentation

---

## Related Files

- **A__dictionary_discovery_v26_newdict.ipynb** - Main training workflow with integrated CP9
- **V26_CHECKPOINT9_PLAN.md** - Detailed implementation plan for all visualizations
- **V26_CP9_PROGRESS.md** - Implementation progress tracking
- **CHECKPOINT9_VISUALIZATION_CRITIQUE.md** - Critical assessment of visualizations

---

## Support

For questions or issues:
1. Check this README for configuration guidance
2. Review error messages in notebook output
3. Verify source workflow structure matches requirements
4. Check that all required data files exist

---

**Ready to visualize!** 🎨
