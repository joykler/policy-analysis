# Checkpoint 9: Dictionary Visualization with Pre/Post Training Comparison

## Overview

Cells 9.6-9.8 visualize **dictionary terms** in the same semantic space framework as chunks, with the powerful addition of **pre-training vs post-training comparison**. This reveals how fine-tuning changes the model's representation of your curated terms.

## What It Shows

### 1. **Dictionary Terms in Semantic Space** (Cells 9.6-9.7)
- Each dictionary term plotted based on BERTJE embeddings
- **Seed terms**: Larger diamonds (manually curated)
- **Expanded terms**: Smaller circles (discovered by algorithm)
- **Topics**: Color-coded by assignment
- **Relationships**: Proximity = semantic similarity

### 2. **Training-Induced Shifts** (Cell 9.8)
- **Pre-training positions**: Base BERTJE embeddings (lighter, smaller)
- **Post-training positions**: Fine-tuned embeddings (bolder, larger)
- **Shift vectors**: Red arrows showing movement during training
- **Magnitude analysis**: Which terms changed most

## Cell Structure

```
Cell 9.6: Dictionary Embeddings Generation
  ├─ Load curated dictionary
  ├─ Load pre-training model (base BERTJE or saved base_encoder)
  ├─ Load post-training model (trained_encoder)
  ├─ Generate embeddings for all terms
  ├─ Apply PCA for dimensionality reduction
  └─ Prepare visualization data

Cell 9.7: 2D Dictionary Visualization
  ├─ Side-by-side comparison (if both models available)
  ├─ Seed terms: Diamonds with labels
  ├─ Expanded terms: Smaller circles
  ├─ Color by topic
  └─ Save: dictionary_terms_comparison_2d.html

Cell 9.8: 3D Dictionary with Shift Analysis
  ├─ Pre-training positions (light)
  ├─ Post-training positions (bold)
  ├─ Shift vectors (red arrows)
  ├─ Top shifters identified
  └─ Save: dictionary_terms_shifts_3d.html
```

## Cell 9.6: Embedding Generation

### What Happens

1. **Loads Dictionary**
   ```python
   dict_path = source_fs.folders.get('Dictionary') / 'Curated_dictionary.csv'
   df_dict = pd.read_csv(dict_path)
   ```

2. **Loads Models**
   - **Priority 1**: `Model_finetuning/trained_encoder/` (post-training)
   - **Priority 2**: `Model_finetuning/base_encoder/` (pre-training snapshot)
   - **Fallback**: `GroNLP/bert-base-dutch-cased` (default BERTJE)

3. **Generates Embeddings**
   ```python
   embeddings = get_embeddings(dict_terms, tokenizer, model)
   # Returns: (n_terms, 768) - BERTJE hidden size
   ```
   - Uses CLS token embedding (contextual representation)
   - Batch processing for efficiency

4. **PCA Projection**
   ```python
   # Separate PCA for dictionary terms (different from chunks)
   pca_2d = PCA(n_components=2)
   pca_3d = PCA(n_components=3)
   ```
   - Preserves relative distances
   - Enables visualization

### Key Variables Created

```python
dict_viz_data = {
    'df': df_dict,  # Dictionary with metadata
    'base': {  # Pre-training embeddings
        'embeddings': (n_terms, 768),
        'pca_2d': (n_terms, 2),
        'pca_3d': (n_terms, 3),
        'variance_2d': [PC1%, PC2%],
        'variance_3d': [PC1%, PC2%, PC3%],
    },
    'trained': {  # Post-training embeddings
        # ... same structure
    }
}
```

## Cell 9.7: 2D Visualization

### Layout Options

**Option A: Side-by-Side Comparison** (when both models available)
```
┌─────────────────────┬─────────────────────┐
│  Pre-Training       │  Post-Training      │
│  (Base BERTJE)      │  (Fine-tuned)       │
│                     │                     │
│  ◆ Seed terms       │  ◆ Seed terms       │
│  ○ Expanded terms   │  ○ Expanded terms   │
└─────────────────────┴─────────────────────┘
```

**Option B: Single View** (only one model available)
```
┌─────────────────────────────┐
│  Dictionary Terms           │
│  (Pre-training only)        │
│                             │
│  ◆ Seed terms               │
│  ○ Expanded terms           │
└─────────────────────────────┘
```

### Visual Elements

**Seed Terms** (manually curated):
- **Symbol**: Diamond (◆)
- **Size**: 12 pixels
- **Color**: By topic
- **Opacity**: 0.9 (solid)
- **Border**: Black, thick (2px)
- **Labels**: Term text (abbreviated to 15 chars)

**Expanded Terms** (algorithm-discovered):
- **Symbol**: Circle (○)
- **Size**: 6 pixels
- **Color**: By topic
- **Opacity**: 0.6 (semi-transparent)
- **Border**: Matching color (1px)
- **Labels**: None (would clutter)

**Hover Tooltip**:
```
Term: onderwijsachterstanden
Topic: Educational Disadvantage & Brain Drain
Type: Seed
Weight: 1.5
```

### Interpretation

**Patterns to Look For**:

1. **Tight Topic Clusters**
   ```
   ◆ ◆ ○ ○ ○  <- Well-defined topic
   ◆ ○ ◆ ○
   ```
   **Meaning**: Terms semantically coherent

2. **Overlapping Clusters**
   ```
   Topic A: ◆ ○ ○
              ◆ ○  <- Overlap zone
   Topic B:  ○ ◆ ○
   ```
   **Meaning**: Topics semantically related

3. **Isolated Terms**
   ```
   ◆ ...far... Topic cluster
   ```
   **Meaning**: Outlier or unique concept

4. **Seed-Expanded Alignment**
   ```
   ◆ (seed) surrounded by ○ ○ ○ (expanded)
   ```
   **Meaning**: Good expansion quality

### Pre vs Post Comparison

**What to Compare**:

| Aspect | Pre-Training | Post-Training | Insight |
|--------|-------------|---------------|---------|
| Cluster tightness | Dispersed | Tighter | Model learned topic structure |
| Topic separation | Overlapping | Separated | Better discrimination |
| Seed-expanded alignment | Weak | Strong | Expansion validated by data |
| Outliers | Many | Fewer | Terms integrated better |

## Cell 9.8: 3D Shift Analysis

### Visual Elements

**Pre-Training Positions** (starting points):
- **Symbol**: Small circles
- **Size**: 4 pixels
- **Color**: Topic color
- **Opacity**: 0.3 (very light)
- **Purpose**: Show where terms started

**Post-Training Positions** (ending points):
- **Symbol**: Diamonds (seed) or circles (expanded)
- **Size**: 8 pixels (larger than pre)
- **Color**: Topic color
- **Opacity**: 0.9 (solid)
- **Labels**: Term text for seeds
- **Purpose**: Show where terms ended up

**Shift Vectors** (movement during training):
- **Symbol**: Dashed red arrows
- **Width**: 2 pixels
- **Shown for**: Terms with above-median shift
- **Purpose**: Visualize learning

### Shift Magnitude

**Calculation**:
```python
shift = embedding_post - embedding_pre
shift_magnitude = ||shift||  # Euclidean norm
```

**Interpretation**:
- **Small shift (< 0.1)**: Term representation stable
- **Medium shift (0.1-0.3)**: Moderate refinement
- **Large shift (> 0.3)**: Significant change

**Why Terms Shift**:

1. **Topic Disambiguation**
   - Multi-topic term moves toward primary topic
   - Example: "achterstand" (disadvantage) moves toward Education cluster

2. **Context Learning**
   - Generic term becomes domain-specific
   - Example: "beleid" (policy) moves toward Governance cluster

3. **Co-occurrence Effects**
   - Term moves toward frequently co-occurring terms
   - Example: "discriminatie" closer to "racisme" cluster

4. **Noise Reduction**
   - Outlier term moves toward its assigned topic
   - Example: Misspelling or rare variant aligns with canonical form

### Top Shifters Analysis

**Cell 9.8 prints**:
```
Top 10 terms with largest shifts:
  multiculturalisme           : 0.456
  emancipatie                 : 0.423
  arbeidsdiscriminatie        : 0.398
  ...
```

**What This Reveals**:

**High Shift = High Learning Signal**
- Terms where training data provided strong signal
- Often multi-topic or ambiguous terms
- Model "decided" their primary meaning from context

**Low Shift = Already Well-Represented**
- Terms already aligned with topic from pre-training
- Very specific terms (e.g., "slavernijverleden")
- Model didn't need to move them much

### Interactive Exploration

**3D Interaction**:
1. **Rotate**: Click and drag to see from different angles
2. **Zoom**: Scroll to focus on specific clusters
3. **Pan**: Right-click drag to move view
4. **Hover**: See term details and shift magnitude
5. **Legend**: Click to hide/show topics

**Exploration Strategy**:
```python
# 1. Overview: Rotate to see overall structure
# 2. Focus: Zoom into topic clusters
# 3. Shifts: Look for red arrows (significant changes)
# 4. Outliers: Check terms far from clusters
# 5. Comparison: Toggle pre/post in legend
```

## Use Cases

### 1. **Validate Dictionary Quality**

**Check**: Do expanded terms cluster near their seed terms?

**Good Pattern**:
```
◆ (seed: onderwijs)
  ○ leerachterstanden
  ○ schooluitval       <- Clustered nearby
  ○ diplomakloof
```

**Bad Pattern**:
```
◆ (seed: onderwijs)
  ○ werkloosheid       <- Far away, wrong topic?
```

**Action**: Review mis-clustered expanded terms, possibly remove

### 2. **Identify Topic Overlap**

**Check**: Which topics have overlapping term clusters?

**Example Finding**:
```
"Poverty" terms overlap with "Education" terms
→ Natural co-occurrence in policy domain
→ Consider: Combined "Education-Poverty" topic?
```

### 3. **Evaluate Training Impact**

**Check**: Did fine-tuning improve topic separation?

**Metrics**:
```python
# Before training (pre)
topic_separation = avg_distance_between_topic_centroids
# After training (post)
topic_separation_trained = ...

if topic_separation_trained > topic_separation:
    print("✓ Training improved topic discrimination")
```

### 4. **Identify Problematic Terms**

**Check**: Which terms shifted dramatically?

**Large Shift Reasons**:
- ✓ Multi-topic term resolved to primary topic (good)
- ⚠️ Term was mislabeled in dictionary (bad)
- ⚠️ Training data had different usage than dictionary (investigate)

**Action**: Review top 10 shifters manually

### 5. **Compare Dictionary Versions**

**Workflow**:
```python
# Run 1: Old dictionary (v1)
CP9_SOURCE = "workflow_data/dict_v1"
# Run Cells 9.6-9.8, save as dict_v1_*.html

# Run 2: New dictionary (v2)
CP9_SOURCE = "workflow_data/dict_v2"
# Run Cells 9.6-9.8, save as dict_v2_*.html

# Compare side-by-side in browser
```

## Configuration

### Cell 9.6 Options

**Model Loading**:
```python
# Use specific base model
base_model_path = Path("path/to/base/bertje")

# Use specific trained model
trained_model_path = Path("path/to/trained/model")
```

**Embedding Batch Size**:
```python
batch_size = 32  # Adjust based on GPU memory
# Smaller = slower but less memory
# Larger = faster but more memory
```

### Cell 9.7 Options

**Label Abbreviation**:
```python
text=seed_df['term_text'].str[:15]  # Show first 15 chars
# Adjust to prevent overlap
```

**Marker Sizes**:
```python
# Seed terms
size=12  # Default, adjust for visibility

# Expanded terms
size=6  # Default, adjust for clutter
```

## Output Files

### dictionary_terms_comparison_2d.html
- **When**: Both pre and post models available
- **Shows**: Side-by-side 2D comparison
- **Size**: ~500KB - 1MB
- **Use**: Quick comparison, presentations

### dictionary_terms_base_2d.html
- **When**: Only pre-training model available
- **Shows**: Single 2D view
- **Size**: ~300KB
- **Use**: Baseline analysis

### dictionary_terms_trained_2d.html
- **When**: Only post-training model available
- **Shows**: Single 2D view
- **Size**: ~300KB
- **Use**: Current state analysis

### dictionary_terms_shifts_3d.html
- **When**: Both models available
- **Shows**: 3D with shift vectors
- **Size**: ~1MB - 2MB
- **Use**: Detailed shift analysis, exploration

### dictionary_terms_{base|trained}_3d.html
- **When**: Single model only
- **Shows**: 3D single view
- **Size**: ~500KB - 1MB
- **Use**: Spatial exploration

## Troubleshooting

### "Failed to load trained model"

**Cause**: Checkpoint 7 (SBERT training) not completed

**Solution**:
- Run Checkpoint 7 to train model
- Or only analyze pre-training embeddings

### "Failed to load base model"

**Cause**: Base model not saved during training

**Solution**:
- Re-run Checkpoint 7 (it should save base_encoder)
- Or will auto-load GroNLP/bert-base-dutch-cased

### "Out of memory during embedding"

**Cause**: Batch size too large for GPU

**Solution**:
```python
# Cell 9.6
batch_size = 16  # Reduce from default 32
```

### Shift vectors cluttered/hard to see

**Cause**: Too many significant shifts shown

**Solution**:
```python
# Cell 9.8
# Change threshold from median to higher percentile
significant_shifts = df_plot[
    df_plot['shift_magnitude'] > np.percentile(shift_magnitudes, 75)
]  # Top 25% instead of top 50%
```

## Best Practices

### 1. Run After Dictionary Curation
```
Checkpoint 3 (expand) → Curate → Checkpoint 9.6-9.8
```
Ensures you're visualizing the final curated dictionary

### 2. Compare Before/After Training
```
Before CP7: Save pre-training viz
After CP7: Generate post-training viz
Compare: See training impact
```

### 3. Document Findings
```
# Take screenshots of:
- Problematic overlaps
- Large shifts (unexpected)
- Well-separated clusters
- Outliers to review
```

### 4. Iterate Based on Insights
```
Visualize → Identify issues → Revise dictionary → Re-run
```

## Example Analysis Session

```python
# ========================================
# Session: Analyze dictionary after training
# ========================================

# 1. Generate embeddings
# Run Cell 9.6
# Output: Both pre and post embeddings available

# 2. View 2D comparison
# Run Cell 9.7
# Observation: "Poverty" and "Education" clusters overlap

# 3. View 3D shifts
# Run Cell 9.8
# Output: Top shifter: "onderwijs-armoede" (education-poverty)
#         Shift: 0.42 (large)
#         Direction: Moved from "Poverty" toward "Education"

# 4. Investigate top shifter
df_dict[df_dict['term_text'] == 'onderwijs-armoede']
# Output:
#   term: onderwijs-armoede
#   topic: Educational Disadvantage
#   type: Expanded
#   parent: onderwijsachterstanden

# 5. Interpretation
# Term was expanded from education seed
# But corpus has many poverty contexts for this term
# Model learned it's actually more poverty-related
# Shift shows model "correcting" dictionary assignment

# 6. Action
# Review term usage in corpus
# Consider: Move to "Poverty" topic OR keep in "Education" as multi-topic

# 7. Document
# Screenshot of shift vector
# Note in curation log
# Will monitor in next iteration
```

## Advanced: Understanding the Math

### Embedding Space

BERTJE creates 768-dimensional vector for each term:
```
embedding_term = [d1, d2, ..., d768]
```

Each dimension captures some aspect of meaning (learned from pre-training on Dutch text).

### Shift Vector

For each term:
```
shift = embedding_post - embedding_pre
shift_magnitude = sqrt(sum(shift^2))
shift_direction = shift / ||shift||
```

### Cosine Similarity

Terms close in embedding space (before PCA):
```
similarity = cos(angle) = (A · B) / (||A|| ||B||)
```
- 1.0 = identical
- 0.5 = moderately similar
- 0.0 = orthogonal (unrelated)
- -1.0 = opposite

### PCA Projection

Reduces 768D → 2D/3D while preserving distances:
```
PC1 = direction of maximum variance
PC2 = direction of max remaining variance (⊥ PC1)
PC3 = direction of max remaining variance (⊥ PC1, PC2)
```

Typical variance explained:
- 2D: 30-50% (rough approximation)
- 3D: 40-60% (better approximation)

## Related Documentation

- Chunk visualization: `CP9_CROSS_TOPIC_VISUALIZATION.md`
- Update summary: `CP9_UPDATE_SUMMARY.md`
- Quick reference: `CP9_QUICK_REFERENCE.md`

## Future Enhancements

Potential additions:

1. **Cluster Statistics**: Compute within-cluster cohesion
2. **Topic Boundaries**: Draw convex hulls around topics
3. **Shift Animation**: Animate pre→post transition
4. **Similarity Network**: Connect similar terms with edges
5. **Multi-Dictionary Comparison**: Compare multiple dictionary versions
6. **Automatic Quality Scoring**: Flag suspicious expanded terms
