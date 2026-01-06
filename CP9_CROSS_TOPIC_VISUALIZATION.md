# Checkpoint 9: Cross-Topic Semantic Space Visualization

## Overview

Checkpoint 9 has been redesigned to visualize **cross-topic relationships** rather than per-topic clustering. This approach shows how chunks are distributed across the semantic space defined by all topics simultaneously, revealing the relationships between topics and how chunks coordinate with topic centroids.

## Key Concept: Semantic Space Representation

### Previous Approach (Per-Topic Clustering)
- ❌ Each topic visualized separately
- ❌ No cross-topic comparison
- ❌ Can't see topic relationships
- ❌ Can't see multi-topic chunks

### New Approach (Cross-Topic Space)
- ✅ All chunks in single unified space
- ✅ Topics shown as centroids (stars)
- ✅ Chunks colored by primary topic
- ✅ Distances to centroids visible
- ✅ Topic relationships revealed
- ✅ Multi-topic patterns visible

## What the Visualization Shows

### 1. **Chunk Distribution**
Each point represents a chunk, positioned based on its scores across ALL topics:
- **Position**: Determined by topic score profile (via PCA)
- **Color**: Primary topic (highest score)
- **Proximity to centroid**: How "typical" the chunk is for its topic
- **Proximity to other centroids**: Multi-topic relevance

### 2. **Topic Centroids** (Red Stars)
Each topic's centroid shows the "center" of that topic in semantic space:
- **Position**: Average of all chunks assigned to that topic
- **Distance between centroids**: Topic similarity/distinctiveness
- **Cluster tightness**: How well-defined the topic is

### 3. **Inter-Topic Relationships**
The spatial arrangement reveals:
- **Topic overlap**: Centroids close together = semantically related topics
- **Topic separation**: Centroids far apart = distinct topics
- **Boundary chunks**: Points between centroids = multi-topic content
- **Outliers**: Points far from all centroids = unusual/noise

## Checkpoint 9 Structure

```
Cell 74:  CHECKPOINT 9: Visualizations (Header)
Cell 75:  CP9: Workflow Source Override
Cell 76:  CELL 9.1: Setup Visualization Libraries
Cell 77:  CELL 9.2: Configuration & Data Loading
Cell 78:  CELL 9.3: Cross-Topic Semantic Space Preparation ⭐ NEW
Cell 79:  CELL 9.4: 2D Cross-Topic Visualization ⭐ NEW
Cell 80:  CELL 9.5: 3D Cross-Topic Visualization ⭐ NEW
Cell 81:  CELL 9.6: Training Metrics Visualization
Cell 82:  CHECKPOINT 9 COMPLETE
```

## Cell 9.3: Cross-Topic Space Preparation

### What It Does

1. **Creates Feature Matrix**
   ```python
   X = df_viz[topic_cols_cosine_viz].values  # shape: (n_chunks, n_topics)
   ```
   Each chunk = vector of scores across all topics

2. **Assigns Primary Topics**
   ```python
   primary_topic_idx = df_viz[topic_cols_cosine_viz].values.argmax(axis=1)
   ```
   Primary topic = topic with highest score

3. **Calculates Confidence Metrics**
   - `score_margin`: Difference between 1st and 2nd highest scores
   - `score_cv`: Coefficient of variation (spread of scores)

4. **Filters High-Confidence Chunks**
   ```python
   high_conf_mask = (df_viz['primary_score'] >= MIN_SCORE_THRESHOLD)
   ```
   Only includes chunks with clear topic assignment

5. **Calculates Topic Centroids**
   ```python
   centroid = X_high_conf[topic_mask].mean(axis=0)
   ```
   Centroid = mean position of all chunks in that topic

6. **Dimensionality Reduction (PCA)**
   - Reduces from n_topics dimensions to 2D/3D
   - Preserves maximum variance
   - Enables visualization of high-dimensional space

7. **Distance to Centroids**
   ```python
   dist = np.linalg.norm(chunk_vec - centroid_vec)
   ```
   Measures how "typical" each chunk is for its topic

### Output
- `cross_topic_viz_data`: Dictionary with all visualization data
  - `df`: DataFrame with PCA coordinates, distances, topics
  - `centroids_pca_2d/3d`: Topic centroid positions
  - `pca_2d/3d`: PCA models
  - `scaler`: Feature scaler
  - `explained_variance`: How much variance PCA preserves

## Cell 9.4: 2D Visualization

### Features

**Chunk Markers**:
- **Color**: By primary topic
- **Size**: 6 pixels
- **Opacity**: 0.6 (semi-transparent to show density)
- **Hover**: Rich tooltip with:
  - Chunk ID and file
  - Primary topic and score
  - Margin to 2nd topic
  - Distance to centroid
  - All topic scores
  - BERTJE comparison (if available)
  - Text preview

**Topic Centroids**:
- **Symbol**: Red stars
- **Size**: 20 pixels (large, visible)
- **Labels**: Topic names above stars
- **Hover**: Topic name and chunk count

**Axes**:
- **X-axis**: PC1 (1st principal component)
- **Y-axis**: PC2 (2nd principal component)
- **Grid**: Light gray, with zero lines
- **Variance**: Shown in axis labels (e.g., "PC1 (45.2% variance)")

### Interpretation Guide

**Patterns to Look For**:

1. **Well-Separated Centroids** = Distinct topics
   ```
   Topic A ⭐ ... far apart ... ⭐ Topic B
   ```

2. **Overlapping Centroids** = Related/confused topics
   ```
   Topic C ⭐⭐ Topic D (very close)
   ```

3. **Tight Clusters** = Well-defined topics
   ```
   ⭐ with many points nearby
   ```

4. **Dispersed Clouds** = Broad/unclear topics
   ```
   ⭐ with points scattered far away
   ```

5. **Boundary Regions** = Multi-topic content
   ```
   Points between two centroids
   ```

6. **Outliers** = Noise or unique content
   ```
   Points far from all centroids
   ```

## Cell 9.5: 3D Visualization

### Advantages of 3D

- **More variance captured**: Typically 60-80% vs 40-60% in 2D
- **Better separation**: Topics may separate better in 3rd dimension
- **Richer exploration**: Rotate to see different perspectives
- **Hidden patterns**: Some relationships only visible in 3D

### Interaction

- **Rotate**: Click and drag
- **Zoom**: Scroll wheel
- **Pan**: Right-click and drag
- **Hover**: Tooltips show chunk details
- **Legend**: Click to hide/show topics

### When to Use 3D vs 2D

**Use 2D when**:
- Quick overview needed
- Presenting to stakeholders
- Publishing in reports
- 2D captures most variance (>60%)

**Use 3D when**:
- Detailed exploration
- 2D shows overlapping centroids
- 3rd PC adds significant variance (>10%)
- Interactive analysis session

## Configuration Parameters

```python
# Cell 9.2
MIN_SCORE_THRESHOLD = 0.30  # Minimum score to include chunk
```

**Effect**: Lower = more chunks, but more noise

**Recommendations**:
- **0.20**: Inclusive, shows broader patterns
- **0.30**: Balanced (default)
- **0.40**: Conservative, clearest topics only
- **0.50**: Very strict, only highest confidence

## Interpreting Results

### High-Quality Topics

✅ **Indicators**:
- Tight cluster around centroid
- Clear separation from other topics
- Low average distance to centroid
- High margin scores (>0.15)

Example:
```
Topic: Educational Disadvantage & Brain Drain
  Chunks: 450
  Avg distance to centroid: 0.12
  Avg margin: 0.25

Interpretation: Well-defined topic with clear semantic profile
```

### Problematic Topics

⚠️ **Indicators**:
- Dispersed cloud (no clear cluster)
- Centroid overlaps with another topic
- High average distance to centroid
- Low margin scores (<0.10)

Example:
```
Topic: Governance Distrust & Corruption
  Chunks: 120
  Avg distance to centroid: 0.35
  Avg margin: 0.08
  Centroid very close to "Social Fragmentation" centroid

Interpretation: May need better seed terms or topic is too broad
```

### Multi-Topic Content

📍 **Pattern**: Chunks positioned between multiple centroids

**Interpretation**:
- Chunk discusses multiple topics
- Natural topic overlap (e.g., poverty + education)
- May need separate combined topic

**Action**:
- Review specific chunks (use hover tooltip)
- Consider if topics should be merged
- Check if chunks need manual categorization

## Comparison with BERTJE

When BERTJE predictions available, hover tooltips show:
- **Cosine primary topic**: From dictionary-based scoring
- **BERTJE primary topic**: From trained model
- **Agreement**: ✓ or ✗

### Agreement Patterns

**High Agreement** (✓ on most chunks):
- Both methods find same semantic structure
- Validates dictionary quality
- Model learned well

**Low Agreement** (✗ on many chunks):
- Methods capture different aspects
- Dictionary may need refinement
- Model may need more training
- Topics may have different granularity

## Troubleshooting

### Issue: All chunks in one cluster

**Cause**: MIN_SCORE_THRESHOLD too high

**Solution**: Lower threshold to 0.20 or 0.25

### Issue: No clear separation between topics

**Causes**:
1. Topics are genuinely similar (semantic overlap)
2. Dictionary seeds are too similar
3. Not enough distinctive terms per topic

**Solutions**:
1. Review topic definitions - can any be merged?
2. Add more distinctive seed terms
3. Check expanded dictionary for cross-topic terms

### Issue: Many outliers far from all centroids

**Causes**:
1. Chunks don't fit any topic (noise)
2. Missing topic in dictionary
3. Generic administrative text

**Solutions**:
1. Review outlier chunks (hover to see text)
2. Consider adding new topic if pattern emerges
3. May need "Administrative" or "Other" topic

### Issue: Low PCA variance explained (<50% in 3D)

**Cause**: Topics are very high-dimensional and complex

**Interpretation**:
- Visualization is rough approximation
- Use caution in interpreting distances
- Rely more on score-based metrics
- Consider UMAP instead of PCA (future enhancement)

## Best Practices

### 1. Start with 2D, Then Explore 3D
```python
# Run Cell 9.4 first
# Review overall structure
# Then run Cell 9.5 for detailed exploration
```

### 2. Use Hover Tooltips Extensively
- Click on boundary chunks to see multi-topic content
- Check outliers to identify noise vs. missing topics
- Verify centroid positions make semantic sense

### 3. Compare with Score Distributions
```python
# Before visualization, check score stats
df_viz[topic_cols_cosine_viz].describe()
```
- Helps set appropriate MIN_SCORE_THRESHOLD
- Shows if topics are balanced

### 4. Iterate on Dictionary
```
1. Run visualization
2. Identify problems (overlap, outliers, etc.)
3. Revise dictionary (add seeds, adjust weights)
4. Re-run from Checkpoint 3
5. Compare new visualization
```

### 5. Document Findings
- Take screenshots of key patterns
- Note problematic topic pairs
- List chunks that should be reviewed manually
- Track changes across dictionary iterations

## Example Analysis Workflow

```python
# ========================================
# Step 1: Run visualization with default threshold
# ========================================
MIN_SCORE_THRESHOLD = 0.30
# Run Cells 9.3-9.5

# Observation: "Poverty" and "Education" centroids very close

# ========================================
# Step 2: Examine boundary chunks
# ========================================
# Hover on chunks between centroids
# Find: Many chunks about "school funding gaps"

# ========================================
# Step 3: Check score distributions
# ========================================
poverty_edu_mask = (
    (df_viz['score_Persistent Poverty & Economic Vulnerability'] > 0.25) &
    (df_viz['score_Educational Disadvantage & Brain Drain'] > 0.25)
)
print(f"Multi-topic chunks: {poverty_edu_mask.sum()}")

# Output: Multi-topic chunks: 145 (10.2% of total)

# ========================================
# Decision: Topics are related but distinct
# ========================================
# Keep separate topics
# Add specific seed terms to increase separation
# Add "school funding" seeds to Education topic
# Add "employment barriers" seeds to Poverty topic
```

## Output Files

| File | Description | Size |
|------|-------------|------|
| `cross_topic_space_2d.html` | Interactive 2D visualization | ~500KB - 2MB |
| `cross_topic_space_3d.html` | Interactive 3D visualization | ~1MB - 3MB |
| `training_metrics_*.html` | Model performance charts | ~100KB |

### Opening Visualizations

```bash
# Windows
start Visuals/cross_topic_space_2d.html

# Mac/Linux
open Visuals/cross_topic_space_2d.html
```

Or drag HTML file into browser.

## Advanced: Understanding the Math

### Feature Space
Each chunk is represented as a vector in n-dimensional space (n = number of topics):
```
chunk_i = [score_topic1, score_topic2, ..., score_topicN]
```

### Centroid Calculation
Topic centroid = mean of all chunk vectors assigned to that topic:
```
centroid_topic = mean([chunk_i for chunk_i in chunks where primary_topic == topic])
```

### PCA Projection
PCA finds orthogonal axes that maximize variance:
```
PC1 = direction of maximum variance
PC2 = direction of maximum remaining variance (orthogonal to PC1)
PC3 = direction of maximum remaining variance (orthogonal to PC1, PC2)
```

### Distance Metric
Euclidean distance in original feature space:
```
distance = sqrt(sum((chunk_i - centroid_topic)^2))
```

## Future Enhancements

Potential improvements to consider:

1. **UMAP instead of PCA**: Better preserves local structure
2. **t-SNE**: Alternative dimensionality reduction
3. **Hierarchical clustering**: Show topic hierarchies
4. **Temporal animation**: If chunks have dates, show evolution
5. **Convex hulls**: Draw boundaries around topic clusters
6. **Voronoi diagram**: Show topic territories
7. **Network graph**: Connect related chunks
8. **Heatmap overlay**: Show score intensities

## Related Documentation

- Quick reference: `CP9_QUICK_REFERENCE.md`
- Update log: `CHECKPOINT_9_OVERRIDE_UPDATE.md`
- Main README: `README_V24.md`
