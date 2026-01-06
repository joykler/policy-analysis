# Checkpoint 9: Integration Analysis
## Comparing Existing Implementation vs. Enhanced Plan

---

## Existing Checkpoint 9 Structure (Cells 73-78)

### Cell 9.1: Library Setup
- Simple try/except import
- Sets `VIZ_AVAILABLE = True/False` flag
- **No model selection** - assumes single workflow

### Cell 9.2: Clustering Configuration
**Data Loading Pattern:**
```python
scores_path = fs.folders['Cosine_labeling'] / 'scores_all_labeled.csv'
df = pd.read_csv(scores_path)
topic_cols = [col for col in df.columns if col.startswith('score_')]
```

**Key Observations:**
- Uses `fs.folders[]` - filesystem manager from earlier checkpoints
- Loads from `'Cosine_labeling'` folder
- Looks for columns starting with `'score_'`
- **Issue**: Doesn't load BERTJE predictions (which have both cosine + BERTJE)
- **No model comparison capability**

### Cell 9.3: Clustering Per Topic
- Filters chunks by `MIN_SCORE_THRESHOLD`
- K-means clustering with `N_CLUSTERS = 5`
- PCA for 2D projection
- Stores results in `clustering_results` dict

**Tooltip Creation (Existing):**
```python
hover = (
    f"<b>File:</b> {file_name}<br>"
    f"<b>Chunk:</b> {chunk_id}<br>"
    f"<b>Cluster:</b> {cluster}<br>"
    f"<b>Score:</b> {score:.4f}<br>"
    f"<br><b>Text:</b><br>{snippet[:150]}"
)
```
- **Good**: Already has basic tooltips!
- **Limited**: Only shows file, chunk ID, cluster, score, text
- **Missing**: All topic scores, BERTJE comparison, confidence, etc.

### Cell 9.4: 2D Visualization
- Creates 2x2 subplot grid
- Plots chunks colored by cluster
- Saves to `fs.folders['Visuals'] / 'topic_clustering_2d.html'`

**Saving Pattern:**
```python
output_path = fs.folders['Visuals'] / 'filename.html'
fig.write_html(str(output_path))
```

### Cell 9.5: 3D Visualization
- Similar to 2D but with 3 PCA components
- One file per topic
- Naming: `topic_clustering_3d_{topic_name}.html`

### Cell 9.6: Training Metrics
- Loads from `fs.folders['Model_finetuning'] / 'training_metrics.json'`
- Creates simple bar chart
- **At end**: Calls `fs.save_config("checkpoint9_visuals")`

**Important**: This saves the checkpoint state!

---

## Key Differences: Existing vs. Enhanced Plan

| Aspect | Existing (v20) | Enhanced Plan | Integration Strategy |
|--------|----------------|---------------|---------------------|
| **Model Selection** | Single workflow only | Primary + Comparison | ✅ Add model selection while preserving `fs` pattern |
| **Data Loading** | `fs.folders['Cosine_labeling']` | Multiple sources | ✅ Extend loading to include BERTJE predictions |
| **Column Names** | `'score_'` prefix | `'cos_'` prefix | ⚠️ **CRITICAL**: Need to detect both patterns |
| **Tooltips** | Basic (file, chunk, score, text) | Rich (all scores, confidence, etc.) | ✅ Enhance existing tooltip structure |
| **Visualizations** | 3 types (2D, 3D, metrics) | 15+ types | ✅ Add new cells, preserve existing |
| **Saving** | `fs.save_config()` at end | Save per cell | ✅ Keep `fs.save_config()` pattern |
| **Filesystem** | Uses `fs.folders[]` dict | Uses `Path` objects | ✅ **Must use `fs.folders` to integrate properly** |

---

## Critical Integration Points

### 1. Filesystem Manager (`fs`)

The workflow uses a `fs` (FileSystem) object created in earlier checkpoints:

```python
fs.folders['Cosine_labeling']  # Returns Path object
fs.folders['Dictionary']
fs.folders['BERTJE_predictions']
fs.folders['Model_finetuning']
fs.folders['Visuals']
fs.save_config("checkpoint9_visuals")  # Saves checkpoint state
```

**Our code must:**
- ✅ Use `fs.folders[]` instead of constructing paths manually
- ✅ Call `fs.save_config()` at the end to save checkpoint
- ✅ Access `fs.workflow_name` for current workflow identification

### 2. Column Name Detection

**Existing**: Looks for `'score_'` prefix
**Reality**: Columns are named `'cos_'` (e.g., `'cos_Educational Disadvantage & Brain Drain'`)

**Solution**: Dual detection
```python
# Try cos_ first (actual column names)
topic_cols = [col for col in df.columns if col.startswith('cos_') and
              any(kw in col for kw in ['Educational', 'Governance', 'Poverty', 'Social'])]

# Fallback to score_ if none found
if len(topic_cols) == 0:
    topic_cols = [col for col in df.columns if col.startswith('score_')]
```

### 3. Data Loading Priority

**Enhanced loading order:**
1. **First try**: `BERTJE_predictions/bertje_continuous_predictions_full.csv` (has BOTH cosine + BERTJE)
2. **Fallback**: `Cosine_labeling/scores_all_labeled.csv` (cosine only)

```python
bertje_path = fs.folders.get('BERTJE_predictions', fs.folders['Cosine_labeling'].parent / 'BERTJE_predictions') / 'bertje_continuous_predictions_full.csv'

if bertje_path.exists():
    df = pd.read_csv(bertje_path)  # Has both cosine + BERTJE scores
else:
    df = pd.read_csv(fs.folders['Cosine_labeling'] / 'scores_all_labeled.csv')  # Cosine only
```

### 4. Model Comparison Integration

**Add at start of Cell 9.2:**
```python
# Configuration for model comparison
PRIMARY_WORKFLOW = fs.workflow_name  # Current workflow
COMPARISON_WORKFLOW = None  # Set to another workflow name to enable comparison
# Example: "slavery_Slavdict_pretraining_slavery_v13"

ENABLE_COMPARISON = (COMPARISON_WORKFLOW is not None)

if ENABLE_COMPARISON:
    # Load comparison data from other workflow
    comparison_path = Path("workflow_data") / COMPARISON_WORKFLOW
    # ... load comparison data
```

---

## Proposed Cell Structure (Enhanced but Integrated)

### Cell 9.0 (NEW): Configuration & Model Selection
- Model selection (primary + optional comparison)
- Global parameters
- Color scheme setup
- **Uses `fs` for filesystem access**

### Cell 9.1: Library Setup (KEEP AS IS)
- Already good
- Just ensure all needed libraries imported

### Cell 9.2: Data Loading (ENHANCE)
**Current**: Loads cosine scores only
**Enhanced**:
- Load BERTJE predictions (has both cosine + BERTJE)
- Detect column patterns (cos_ and score_)
- Load dictionary with seed/expanded detection
- Load training metrics
- **Optional**: Load comparison model data

### Cell 9.3: Clustering (ENHANCE)
**Current**: Basic clustering
**Enhanced**:
- Keep existing logic
- Add silhouette score calculation
- Store more metadata for tooltips
- Add comparison model clustering if enabled

### Cell 9.4: 2D Visualization (ENHANCE TOOLTIPS)
**Current**: Basic tooltips
**Enhanced**:
```python
hover = (
    f"<b>Chunk ID:</b> {chunk_id}<br>"
    f"<b>File:</b> {file_name}<br>"
    f"<b>Cluster:</b> {cluster} / {n_clusters}<br>"
    f"<b>Primary Topic Score:</b> {primary_score:.4f}<br>"
    f"<br><b>All Topic Scores:</b><br>"
    f"  Educational: {scores[0]:.3f}<br>"
    f"  Governance: {scores[1]:.3f}<br>"
    f"  Poverty: {scores[2]:.3f}<br>"
    f"  Social: {scores[3]:.3f}<br>"
    f"<br><b>BERTJE Score:</b> {bertje_score:.4f}<br>"
    f"<b>Agreement:</b> {agree_status}<br>"
    f"<br><b>Text Preview:</b><br>{snippet[:200]}"
)
```

### Cell 9.5: 3D Visualization (KEEP, ENHANCE TOOLTIPS)
- Same as above but for 3D

### Cell 9.6: Training Metrics (ENHANCE)
**Current**: Simple bar chart
**Enhanced**:
- Add per-topic correlation breakdown
- Add comparison vs. baseline if comparison enabled
- Show training progression if history available

### Cell 9.7 (NEW): Dictionary Composition
- Grouped bar chart: seed vs expanded per topic
- Rich tooltips with term details
- Model comparison if enabled

### Cell 9.8 (NEW): Dictionary Quality Distribution
- Box plot of cosine similarity per topic
- Separate seed vs expanded
- Shows quality thresholds

### Cell 9.9 (NEW): Dictionary 2D Clustering (PCA)
- Terms plotted in 2D space
- Color by topic
- Rich tooltips with term metadata

### Cell 9.10 (NEW): Score Comparison (Cosine vs BERTJE)
- 2x2 grid, one per topic
- Scatter: X=cosine, Y=BERTJE
- Diagonal line = perfect agreement
- Tooltips explain disagreements

### Cell 9.11 (NEW): Confusion Matrix
- Cosine primary topic vs BERTJE primary topic
- Heatmap with percentages
- Tooltips explain confusion patterns

### Cell 9.12 (NEW): Confidence vs Agreement
- Bar chart showing agreement rate by confidence bin
- Validates that high confidence → high agreement

### Cell 9.13 (NEW): Disagreement Flow (Sankey)
- Shows where methods disagree
- Flow thickness = disagreement count
- Tooltips with example chunks

### Cell 9.14 (NEW): Model Comparison Dashboard (if enabled)
- Only runs if ENABLE_COMPARISON = True
- Shows primary vs comparison metrics
- Improvement analysis

### Cell 9.15 (NEW): Summary & Export
- Generate markdown summary
- Export CSV with key metrics
- **Call `fs.save_config("checkpoint9_complete")`**

---

## Variable Naming Convention

**To avoid conflicts with existing workflow variables:**

| Purpose | Existing Var | Our Enhanced Var | Reason |
|---------|--------------|------------------|---------|
| Main dataframe | `df` | `df_viz` | Avoid overwriting |
| Topic columns | `topic_cols` | `topic_cols_viz` | Namespace separation |
| Dictionary | N/A | `df_dict_viz` | New addition |
| Clustering results | `clustering_results` | Keep same | Already good |
| Metrics | `metrics` | `training_metrics_viz` | More descriptive |
| Min threshold | `MIN_SCORE_THRESHOLD` | Keep or `MIN_SCORE_VIZ` | User choice |

---

## Integration Checklist

### Phase 1: Enhance Existing Cells (Non-Breaking)
- [ ] Cell 9.0 (NEW): Add configuration cell before 9.1
- [ ] Cell 9.2: Enhance data loading (load BERTJE predictions, detect col patterns)
- [ ] Cell 9.3: Add more clustering metadata
- [ ] Cell 9.4: Enhance tooltips (add all scores, BERTJE, confidence)
- [ ] Cell 9.5: Enhance tooltips (same as 9.4)
- [ ] Cell 9.6: Add per-topic metrics breakdown

### Phase 2: Add New Visualization Cells
- [ ] Cell 9.7: Dictionary composition
- [ ] Cell 9.8: Dictionary quality
- [ ] Cell 9.9: Dictionary clustering
- [ ] Cell 9.10: Score comparison (cosine vs BERTJE)
- [ ] Cell 9.11: Confusion matrix
- [ ] Cell 9.12: Confidence analysis
- [ ] Cell 9.13: Disagreement flows
- [ ] Cell 9.14: Model comparison (if enabled)
- [ ] Cell 9.15: Summary & export

### Phase 3: Testing & Validation
- [ ] Test with policy_v1 workflow (14k chunks)
- [ ] Test with comparison model
- [ ] Verify all visualizations save correctly
- [ ] Verify `fs.save_config()` works
- [ ] Check all tooltips render properly

---

## Code Template for Integration

### Enhanced Cell 9.2 (Data Loading)

```python
# ============================================================
# CELL 9.2: DATA LOADING & CONFIGURATION (ENHANCED)
# ============================================================

if VIZ_AVAILABLE:
    print(f"\n{'='*60}")
    print("DATA LOADING & CONFIGURATION")
    print(f"{'='*60}")

    # ========================================
    # CONFIGURATION
    # ========================================

    # Model comparison settings
    PRIMARY_WORKFLOW = fs.workflow_name
    COMPARISON_WORKFLOW = None  # Set to workflow name to enable, e.g., "slavery_Slavdict_pretraining_slavery_v13"
    ENABLE_COMPARISON = (COMPARISON_WORKFLOW is not None)

    # Clustering parameters
    N_CLUSTERS = 5
    MIN_SCORE_THRESHOLD = 0.30

    # Color scheme
    TOPIC_COLORS = {
        'Educational Disadvantage & Brain Drain': '#3498db',
        'Governance Distrust & Corruption': '#2ecc71',
        'Persistent Poverty & Economic Vulnerability': '#f39c12',
        'Social Fragmentation & Racism': '#e74c3c'
    }

    print(f"\nConfiguration:")
    print(f"  Primary workflow: {PRIMARY_WORKFLOW}")
    if ENABLE_COMPARISON:
        print(f"  Comparison workflow: {COMPARISON_WORKFLOW}")

    # ========================================
    # LOAD PRIMARY MODEL DATA
    # ========================================

    print(f"\nLoading primary model data...")

    # Try to load BERTJE predictions first (has both cosine + BERTJE scores)
    bertje_pred_path = fs.folders.get('BERTJE_predictions')
    if bertje_pred_path:
        bertje_full = bertje_pred_path / 'bertje_continuous_predictions_full.csv'
        if bertje_full.exists():
            df_viz = pd.read_csv(bertje_full)
            print(f"  ✓ Loaded {len(df_viz)} chunks (cosine + BERTJE scores)")
            HAS_BERTJE = True
        else:
            df_viz = pd.read_csv(fs.folders['Cosine_labeling'] / 'scores_all_labeled.csv')
            print(f"  ✓ Loaded {len(df_viz)} chunks (cosine scores only)")
            HAS_BERTJE = False
    else:
        df_viz = pd.read_csv(fs.folders['Cosine_labeling'] / 'scores_all_labeled.csv')
        print(f"  ✓ Loaded {len(df_viz)} chunks (cosine scores only)")
        HAS_BERTJE = False

    # Detect topic columns (try cos_ first, fallback to score_)
    topic_cols_viz = [col for col in df_viz.columns if col.startswith('cos_') and
                      any(kw in col for kw in ['Educational', 'Governance', 'Poverty', 'Social', 'Fragmentation'])]

    if len(topic_cols_viz) == 0:
        topic_cols_viz = [col for col in df_viz.columns if col.startswith('score_')]

    print(f"\n  Detected {len(topic_cols_viz)} topics:")
    for col in topic_cols_viz:
        topic_name = col.replace('cos_', '').replace('score_', '')
        print(f"    - {topic_name}")

    # Load dictionary
    dict_path = fs.folders.get('Dictionary')
    if dict_path:
        curated_dict = dict_path / 'Curated_dictionary.csv'
        if curated_dict.exists():
            df_dict_viz = pd.read_csv(curated_dict)
            print(f"  ✓ Loaded {len(df_dict_viz)} dictionary terms")

            if 'is_seed' in df_dict_viz.columns:
                n_seed = df_dict_viz['is_seed'].sum()
                print(f"    - Seed: {n_seed}, Expanded: {len(df_dict_viz) - n_seed}")
        else:
            df_dict_viz = None
    else:
        df_dict_viz = None

    # Load training metrics
    metrics_path = fs.folders['Model_finetuning'] / 'training_metrics.json'
    if metrics_path.exists():
        with open(metrics_path, 'r') as f:
            training_metrics_viz = json.load(f)
        final_eval = training_metrics_viz.get('final_eval', {})
        mean_corr = final_eval.get('eval_mean_correlation', 'N/A')
        print(f"  ✓ Training metrics loaded (mean r={mean_corr:.4f})")
    else:
        training_metrics_viz = None

    # ========================================
    # LOAD COMPARISON MODEL (if enabled)
    # ========================================

    df_viz_comparison = None
    df_dict_viz_comparison = None
    training_metrics_viz_comparison = None

    if ENABLE_COMPARISON:
        print(f"\nLoading comparison model data...")
        comparison_base = Path("workflow_data") / COMPARISON_WORKFLOW

        if comparison_base.exists():
            # Load comparison BERTJE predictions
            comp_bertje = comparison_base / "BERTJE_predictions" / "bertje_continuous_predictions_full.csv"
            if comp_bertje.exists():
                df_viz_comparison = pd.read_csv(comp_bertje)
                print(f"  ✓ Loaded {len(df_viz_comparison)} chunks from comparison model")

            # Load comparison dictionary
            comp_dict = comparison_base / "Dictionary" / "Curated_dictionary.csv"
            if comp_dict.exists():
                df_dict_viz_comparison = pd.read_csv(comp_dict)
                print(f"  ✓ Loaded {len(df_dict_viz_comparison)} dictionary terms from comparison")

            # Load comparison metrics
            comp_metrics = comparison_base / "Model_finetuning" / "training_metrics.json"
            if comp_metrics.exists():
                with open(comp_metrics, 'r') as f:
                    training_metrics_viz_comparison = json.load(f)
                comp_eval = training_metrics_viz_comparison.get('final_eval', {})
                comp_corr = comp_eval.get('eval_mean_correlation', 'N/A')
                print(f"  ✓ Comparison training metrics loaded (mean r={comp_corr:.4f})")
        else:
            print(f"  ⚠ Comparison workflow not found: {comparison_base}")
            ENABLE_COMPARISON = False

    print(f"\n✓ Data loading complete")

else:
    print("⚠ Skipping data loading - visualization libraries not available")
```

---

## Summary

**Key Integration Principles:**
1. ✅ **Use `fs.folders[]`** - Don't construct paths manually
2. ✅ **Detect column patterns** - Support both `'cos_'` and `'score_'` prefixes
3. ✅ **Load BERTJE predictions first** - Contains both score types
4. ✅ **Preserve existing cells** - Enhance, don't replace
5. ✅ **Add new cells after existing** - Extend functionality
6. ✅ **Call `fs.save_config()`** - Save checkpoint state at end
7. ✅ **Use `_viz` suffix** - Avoid variable name conflicts
8. ✅ **Rich tooltips** - Enhance existing hover structure

**Testing Priority:**
1. Cell 9.2 enhancement (data loading)
2. Cell 9.4 enhancement (tooltip upgrade)
3. New Cell 9.7 (dictionary composition)
4. New Cell 9.10 (score comparison)

This analysis provides the roadmap for proper integration!
