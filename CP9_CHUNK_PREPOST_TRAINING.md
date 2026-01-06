# Checkpoint 9: Chunk Pre/Post Training Comparison

## Overview

Cells 9.3A, 9.4A, and 9.4B now provide **pre/post training comparison for corpus chunks**, showing how fine-tuning changed the model's understanding of policy text.

## New Cells

### Cell 9.3A: Generate Chunk Embeddings (Pre/Post)
**Purpose**: Generate BERTJE embeddings for chunks before and after training

**Two Modes**:

1. **BERTJE Embeddings Mode** (default, preferred)
   - Uses actual BERTJE model embeddings (768-dimensional)
   - More comprehensive semantic representation
   - Shows true model learning

2. **Topic Scores Mode** (fallback)
   - Uses cosine scores vs BERTJE predictions
   - Faster, no GPU needed
   - Topic-specific view

**Configuration**:
```python
USE_BERTJE_EMBEDDINGS = True  # Set to False for topic scores mode
MAX_CHUNKS_FOR_EMBEDDING = 5000  # Limit for speed
```

### Cell 9.4A: 2D Pre/Post Comparison
**Purpose**: Side-by-side visualization showing clustering before and after training

**Layout**:
```
┌─────────────────────┬─────────────────────┐
│  Pre-Training       │  Post-Training      │
│  (Before finetuning)│  (After finetuning) │
│  • • • •           │  • • • •           │
│  • • • •           │  • • • •           │
└─────────────────────┴─────────────────────┘
```

**What to Look For**:
- Tighter clusters in post-training → Better topic learning
- Better separation → Improved discrimination
- Changed positions → Model refined understanding

### Cell 9.4B: 3D Shift Vectors
**Purpose**: Interactive 3D showing how chunks moved during training

**Visual Elements**:
- **Light circles**: Pre-training positions
- **Bold circles**: Post-training positions
- **Red dashed arrows**: Significant shifts (top 10%)
- **Interactive**: Rotate to explore from all angles

## How It Works

### Embedding Generation

**Pre-Training Embeddings**:
```python
# Load base model (before fine-tuning)
model_base = AutoModel.from_pretrained('base_encoder')

# Generate embeddings
embeddings_pre = model_base(chunk_texts)
# Shape: (n_chunks, 768)
```

**Post-Training Embeddings**:
```python
# Load trained model (after fine-tuning)
model_trained = AutoModel.from_pretrained('trained_encoder')

# Generate embeddings
embeddings_post = model_trained(chunk_texts)
# Shape: (n_chunks, 768)
```

### Shift Calculation

For each chunk:
```python
shift = embedding_post - embedding_pre
shift_magnitude = ||shift||  # Euclidean distance
```

**Interpretation**:
- **Small shift (<0.1)**: Chunk representation stable
- **Medium shift (0.1-0.3)**: Moderate refinement
- **Large shift (>0.3)**: Significant learning

## Use Cases

### 1. Validate Training Success

**Check**: Did training improve clustering?

**Good Signs**:
- Tighter clusters in post-training
- Better separation between topics
- More chunks close to topic centroids

**Bad Signs**:
- Dispersed clusters in post-training
- Topics more overlapped
- Many chunks moving to "wrong" topic

### 2. Identify Challenging Content

**Check**: Which chunks shifted most?

**Large Shifts Indicate**:
- Multi-topic chunks resolved
- Model learned context
- Previously ambiguous → now clear

**Example**:
```python
# After Cell 9.3A
top_shifters = chunk_embeddings_data['df'].nlargest(10, 'shift_magnitude')
for _, row in top_shifters.iterrows():
    print(f"{row['raw_text'][:100]}: shift={row['shift_magnitude']:.3f}")
```

### 3. Compare Training Approaches

**Workflow**:
```python
# Training Run 1: Baseline
CP9_SOURCE = "workflow_data/baseline_training"
# Run Cells 9.3A-9.4B
# Save as: chunks_shifts_baseline.html

# Training Run 2: Improved
CP9_SOURCE = "workflow_data/improved_training"
# Run Cells 9.3A-9.4B
# Save as: chunks_shifts_improved.html

# Compare: Which shows better clustering?
```

### 4. Analyze Topic-Specific Learning

**Check**: Did some topics learn better than others?

```python
# After Cell 9.3A
for topic in chunk_embeddings_data['df']['primary_topic'].unique():
    topic_df = chunk_embeddings_data['df'][
        chunk_embeddings_data['df']['primary_topic'] == topic
    ]
    avg_shift = topic_df['shift_magnitude'].mean()
    print(f"{topic}: avg shift = {avg_shift:.3f}")
```

**Interpretation**:
- High avg shift → Topic learned a lot (or was confused before)
- Low avg shift → Topic was already well-represented

## Configuration Options

### Embedding Mode Selection

```python
# Cell 9.3A
USE_BERTJE_EMBEDDINGS = True  # Full BERTJE embeddings

# OR

USE_BERTJE_EMBEDDINGS = False  # Topic scores only
```

**When to use embeddings**:
- ✅ Have GPU available
- ✅ Want comprehensive view
- ✅ Willing to wait (~5-10 min)

**When to use scores**:
- ✅ No GPU available
- ✅ Quick analysis needed
- ✅ Topic-specific focus

### Sampling Size

```python
# Cell 9.3A
MAX_CHUNKS_FOR_EMBEDDING = 5000  # Default

# For faster execution
MAX_CHUNKS_FOR_EMBEDDING = 1000

# For comprehensive analysis
MAX_CHUNKS_FOR_EMBEDDING = 10000
```

### Shift Vector Threshold

```python
# Cell 9.4B
shift_threshold = np.percentile(df_chunks['shift_magnitude'], 90)  # Top 10%

# Show more arrows (top 20%)
shift_threshold = np.percentile(df_chunks['shift_magnitude'], 80)

# Show fewer arrows (top 5%)
shift_threshold = np.percentile(df_chunks['shift_magnitude'], 95)
```

## Output Files

| File | Shows | When |
|------|-------|------|
| `chunks_prepost_comparison_2d.html` | Side-by-side 2D | Both models available |
| `chunks_shifts_3d.html` | 3D with shift vectors | Both models available |

## Interpretation Guide

### Pattern 1: Convergence

**Observation**:
```
Pre:  • • • • • (dispersed)
Post: • • • (tight cluster)
```

**Meaning**: Training brought similar chunks together

**Good**: Topics becoming more coherent

### Pattern 2: Separation

**Observation**:
```
Pre:  Topic A ••• Topic B (overlapping)
Post: Topic A •••    ••• Topic B (separated)
```

**Meaning**: Training learned to distinguish topics

**Good**: Better topic discrimination

### Pattern 3: Migration

**Observation**:
```
Pre:  Topic A: • • • ← • (this chunk)
Post: Topic B:         • → • • • (moved here)
```

**Meaning**: Chunk reassigned to different topic

**Investigate**: Why did it move? Was original label wrong?

### Pattern 4: Stability

**Observation**:
```
Pre:  • • •
Post: • • • (same positions)
```

**Meaning**: Chunks already well-represented

**Good**: Pre-training captured these well

## Troubleshooting

### "Failed to load base/trained model"

**Cause**: Checkpoint 7 not completed or models not saved

**Solution**:
```python
# Re-run Checkpoint 7, ensure it saves:
# - base_encoder/ (pre-training snapshot)
# - trained_encoder/ (fine-tuned model)
```

### "Out of memory during embedding"

**Cause**: Too many chunks or batch size too large

**Solution**:
```python
# Cell 9.3A - Reduce batch size
batch_size=16  # Change from 32

# OR reduce sample size
MAX_CHUNKS_FOR_EMBEDDING = 2000
```

### "Switching to topic scores mode"

**Cause**: BERTJE models not available

**Impact**: Will use cosine vs BERTJE scores instead

**Action**: Still works, just different semantic space

### Shift vectors too cluttered

**Cause**: Showing too many arrows

**Solution**:
```python
# Cell 9.4B
# Show only top 5% instead of top 10%
shift_threshold = np.percentile(df_chunks['shift_magnitude'], 95)

# Or limit absolute number
if len(significant_shifts) > 100:
    significant_shifts = significant_shifts.nlargest(100, 'shift_magnitude')
```

## Performance Notes

### Cell 9.3A Runtime

**Embeddings Mode**:
- 1000 chunks: ~2-3 minutes
- 5000 chunks: ~10-15 minutes
- 10000 chunks: ~25-30 minutes

**Scores Mode**:
- All chunks: ~5-10 seconds

### Memory Requirements

**Embeddings Mode**:
- RAM: ~2-4 GB
- GPU: 4-8 GB (if available)
- Without GPU: Slower but works on CPU

**Scores Mode**:
- RAM: ~500 MB
- No GPU needed

## Advanced Analysis

### Statistical Comparison

```python
# After Cell 9.3A
import scipy.stats as stats

# Test if shifts are significant
t_stat, p_value = stats.ttest_1samp(
    chunk_embeddings_data['df']['shift_magnitude'],
    0
)

print(f"Mean shift: {chunk_embeddings_data['df']['shift_magnitude'].mean():.3f}")
print(f"p-value: {p_value:.4f}")

if p_value < 0.05:
    print("✓ Shifts are statistically significant")
else:
    print("⚠ Shifts may be due to random variation")
```

### Topic-Wise Shift Analysis

```python
# Compare shift magnitude across topics
import matplotlib.pyplot as plt
import seaborn as sns

df_shifts = chunk_embeddings_data['df']

plt.figure(figsize=(12, 6))
sns.boxplot(data=df_shifts, x='primary_topic', y='shift_magnitude')
plt.xticks(rotation=45, ha='right')
plt.title('Shift Magnitude Distribution by Topic')
plt.tight_layout()
plt.savefig('shift_distribution_by_topic.png')
plt.show()
```

### Export Shift Data

```python
# Save for external analysis
chunk_embeddings_data['df'][['chunk_uid', 'primary_topic', 'shift_magnitude', 'shift_x', 'shift_y', 'shift_z']].to_csv(
    'chunk_shifts.csv',
    index=False
)

print("Shift data saved to chunk_shifts.csv")
```

## Complete Example Workflow

```python
# ========================================
# Analyze how training affected chunks
# ========================================

# Step 1: Generate embeddings
# Run Cell 9.3A
# Output: 5000 chunks embedded (pre and post)
#         Mean shift: 0.234
#         Max shift: 0.876

# Step 2: View 2D comparison
# Run Cell 9.4A
# Observation:
#   - Pre-training: Topics somewhat overlapping
#   - Post-training: Clear separation emerged
#   - "Education" cluster much tighter

# Step 3: Explore 3D shifts
# Run Cell 9.4B
# Finding: 500 shift vectors shown
# Top shifter: Chunk about "school funding disparities"
#   - Pre: Near "Poverty" cluster
#   - Post: Moved to "Education" cluster
#   - Shift: 0.876

# Step 4: Investigate top shifter
chunk_id = top_shifter_chunk_uid
chunk_text = df_viz[df_viz['chunk_uid'] == chunk_id]['raw_text'].iloc[0]
print(chunk_text)

# Output: "...tekorten in onderwijsfinanciering leiden tot
#          grotere verschillen in leerkansen..."
# Translation: "...shortages in education funding lead to
#               larger differences in learning opportunities..."

# Step 5: Interpretation
# This chunk discusses BOTH poverty and education
# Pre-training: Classified as "Poverty" (economic focus)
# Post-training: Reclassified as "Education" (learning focus)
# Shift: Model learned from corpus that education context dominates

# Step 6: Validation
# Check BERTJE prediction for this chunk
bertje_topic = df_viz[df_viz['chunk_uid'] == chunk_id]['bertje_primary_topic'].iloc[0]
print(f"BERTJE agrees: {bertje_topic}")
# Output: BERTJE agrees: Educational Disadvantage & Brain Drain

# Step 7: Conclusion
# Training successfully refined understanding of this chunk
# Moved from economic frame to educational frame
# Aligns with domain expert judgment
```

## Summary

**Cells 9.3A, 9.4A, 9.4B** provide comprehensive pre/post training analysis for chunks:

✅ **Generate embeddings** (BERTJE or scores)
✅ **2D comparison** (side-by-side)
✅ **3D shift visualization** (with arrows)
✅ **Shift statistics** (magnitude, direction)
✅ **Topic-wise analysis** (which topics learned most)

**Use to**:
- Validate training success
- Identify challenging content
- Compare training approaches
- Understand model learning
- Guide further refinement

**Complements** dictionary visualization (Cells 9.6-9.8) for complete picture of training impact!
