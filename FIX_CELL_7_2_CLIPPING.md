# Fix for Cell 7.2: Score Clipping Issue

**Problem:** Cell 7.2 clips scores to 0-10 range, but Cell 5.1 produces unbounded dot product scores (0-200+)

**Location:** Cell 7.2 (Index 48) in `A__dictionary_discovery_v20_unified_embedding.ipynb`

---

## Current Code (INCORRECT)

```python
class ContinuousMultiLabelDataset(Dataset):
    """
    Dataset for continuous multi-label regression.
    Uses raw dot product scores [0, ~9] - NO discretization!  # <- COMMENT IS WRONG
    """

    def __init__(self, dataframe, tokenizer, topics, config):
        # ...

        # Extract continuous dot product scores directly
        self.labels = []
        for _, row in dataframe.iterrows():
            label_vec = []
            for topic in topics:
                score_val = row.get(f"score_{topic}", 0.0)
                if pd.isna(score_val):
                    score_val = 0.0
                score_val = float(np.clip(score_val, 0.0, 10.0))  # <- PROBLEM!
                label_vec.append(score_val)
            self.labels.append(label_vec)
```

**Problem:**
- Clipping to 10.0 truncates valid high scores
- Cell 5.1 produces scores that can exceed 10 (up to 200+)
- This artificially compresses the high-score range

---

## Solution Options

### Option A: Use Dynamic Normalization (RECOMMENDED)

Normalize to 0-1 range using corpus statistics (same approach as Cell 5.2):

```python
class ContinuousMultiLabelDataset(Dataset):
    """
    Dataset for continuous multi-label regression.
    Normalizes raw dot product scores to [0, 1] range dynamically.
    """

    def __init__(self, dataframe, tokenizer, topics, config):
        self.dataframe = dataframe.reset_index(drop=True)
        self.tokenizer = tokenizer
        self.topics = topics
        self.config = config

        self.texts = dataframe["raw_text"].tolist()

        # Calculate corpus statistics for normalization
        score_cols = [f"score_{topic}" for topic in topics]
        all_scores = dataframe[score_cols].values
        corpus_min = float(all_scores.min())
        corpus_max = float(all_scores.max())
        corpus_range = corpus_max - corpus_min

        print(f"Score normalization: [{corpus_min:.2f}, {corpus_max:.2f}] -> [0.0, 1.0]")

        # Extract and normalize continuous dot product scores
        self.labels = []
        for _, row in dataframe.iterrows():
            label_vec = []
            for topic in topics:
                score_val = row.get(f"score_{topic}", corpus_min)  # Default to min, not 0
                if pd.isna(score_val):
                    score_val = corpus_min

                # Normalize to [0, 1] using corpus statistics
                if corpus_range > 0:
                    score_normalized = (score_val - corpus_min) / corpus_range
                else:
                    score_normalized = 0.0

                score_normalized = float(np.clip(score_normalized, 0.0, 1.0))
                label_vec.append(score_normalized)

            self.labels.append(label_vec)
```

**Advantages:**
- Works with ANY score range (positive, negative, unbounded)
- Consistent with Cell 5.2's significance scoring
- No information loss from clipping
- Model learns meaningful 0-1 targets

---

### Option B: Use Percentile-Based Normalization

Normalize based on percentiles (more robust to outliers):

```python
# Calculate percentile-based bounds (before the loop)
p99 = float(all_scores.quantile(0.99))  # 99th percentile as upper bound
p01 = float(all_scores.quantile(0.01))  # 1st percentile as lower bound
score_range = p99 - p01

print(f"Score normalization: P01={p01:.2f}, P99={p99:.2f}")

# In the loop:
score_normalized = (score_val - p01) / score_range
score_normalized = float(np.clip(score_normalized, 0.0, 1.0))
```

**Advantages:**
- Robust to extreme outliers
- Clips only top 1% and bottom 1%

---

### Option C: Remove Clipping (Keep Raw Scores)

If the model can handle unbounded targets:

```python
score_val = float(score_val)  # No clipping at all
```

**Disadvantages:**
- MSE loss will be sensitive to large scores
- Harder for model to learn (unbounded targets)
- Not recommended unless using specialized loss function

---

## Recommended Fix

**Use Option A (Dynamic Normalization)** to match Cell 5.2's approach:

1. Calculate corpus_min, corpus_max, corpus_range from training data
2. Normalize all scores to [0, 1]
3. Model learns to predict normalized scores
4. When making predictions, denormalize if needed: `score = pred * corpus_range + corpus_min`

---

## Additional Fix: Update Comment

Change the docstring to reflect the actual score range:

```python
class ContinuousMultiLabelDataset(Dataset):
    """
    Dataset for continuous multi-label regression.
    Normalizes raw dot product scores (unbounded) to [0, 1] range.

    Uses dynamic normalization based on corpus statistics:
        normalized = (raw_score - corpus_min) / (corpus_max - corpus_min)
    """
```

---

## Implementation

I can create a script to update Cell 7.2 with the recommended fix. Would you like me to:

1. Apply Option A (dynamic normalization to 0-1)?
2. Apply Option B (percentile-based normalization)?
3. Just remove the clipping and keep raw scores?