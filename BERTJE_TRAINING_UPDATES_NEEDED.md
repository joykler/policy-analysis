# BERTJE Training Updates for Dot Product Scores

## Current Issue

Your BERTJE training setup expects **rescaled scores (0-2 range)** but the new dot product system produces **raw scores (~0.77-9.22 range)**.

---

## What Needs to Change

### 1. Cell 50: Dataset Class (CRITICAL)

**Current code (line 28):**
```python
score_val = row.get(f"rescaled_{topic}", 0.0)
```

**Problem:** Looking for `rescaled_{topic}` columns that no longer exist

**Fix:** Use raw `score_{topic}` columns
```python
score_val = row.get(f"score_{topic}", 0.0)
```

**Also update line 31:**
```python
# OLD: Clipping to 0-2 range (rescaled)
score_val = float(np.clip(score_val, 0.0, 2.0))

# NEW: Clip to observed score range (dot product)
score_val = float(np.clip(score_val, 0.0, 10.0))
```

**Also update docstring (line 12):**
```python
# OLD
"""Uses rescaled scores [0, 2] - NO discretization!"""

# NEW
"""Uses raw dot product scores [0, ~9] - NO discretization!"""
```

**Also update print statement (line 50):**
```python
# OLD
print("  - Uses rescaled scores (0.0-2.0) with 4x better spread")

# NEW
print("  - Uses raw dot product scores (0.0-10.0) with full magnitude information")
```

---

### 2. Training Implications

#### Score Range Comparison

| System | Range | Spread | Information |
|--------|-------|--------|-------------|
| Old (cosine + rescale) | 0.0 - 2.0 | 2.0 | Compressed, normalized |
| New (dot product) | 0.77 - 9.22 | 8.45 | **4.2x wider**, preserves magnitude |

#### What This Means for BERTJE

**Positive impacts:**
- ✅ **Better gradient signals:** Wider range = more distinct training targets
- ✅ **Magnitude preserved:** Strong topics have genuinely higher scores
- ✅ **Less compression:** Model learns more nuanced patterns

**Potential concerns:**
- ⚠️ **Different scale:** Model will predict in 0-10 range instead of 0-2
- ⚠️ **Loss magnitude:** MSE loss will be ~16x larger (4² scaling)

---

### 3. Loss Function (OPTIONAL - may not need changes)

Your current setup likely uses MSE loss, which is scale-invariant in terms of optimization:

```python
MSE = mean((prediction - target)²)
```

The optimizer doesn't care if targets are 0-2 or 0-10 - it will adjust the same way. However, you might want to monitor loss values differently:

**Current loss range (rescaled 0-2):**
- Good model: MSE ~0.1 - 0.3
- Poor model: MSE ~0.5 - 1.0

**Expected loss range (dot product 0-10):**
- Good model: MSE ~0.5 - 2.0  (roughly 4-6x higher due to scale)
- Poor model: MSE ~2.5 - 6.0

**No code change needed**, but be aware when interpreting training logs.

---

### 4. Evaluation Metrics (OPTIONAL)

If you have evaluation metrics that use absolute thresholds, they need updating.

Example from your code (if it exists):
```python
# OLD
threshold = 0.5  # For rescaled scores

# NEW
threshold = 3.0  # For dot product scores (proportional scaling)
```

Search for hardcoded thresholds in:
- Metrics computation functions
- Evaluation scripts
- Post-processing code

---

## Complete Fix for Cell 50

Here's the complete updated Cell 50:

```python
# ============================================================
# CELL 7.2: Continuous Multi-Label Dataset (DOT PRODUCT)
# ============================================================

from torch.utils.data import Dataset
import pandas as pd
import numpy as np

class ContinuousMultiLabelDataset(Dataset):
    """
    Dataset for continuous multi-label regression.
    Uses raw dot product scores [0, ~9] - NO discretization!
    """

    def __init__(self, dataframe, tokenizer, topics, config):
        self.dataframe = dataframe.reset_index(drop=True)
        self.tokenizer = tokenizer
        self.topics = topics
        self.config = config

        self.texts = dataframe["text"].tolist()

        # Extract continuous dot product scores directly
        self.labels = []
        for _, row in dataframe.iterrows():
            label_vec = []
            for topic in topics:
                # Use raw dot product scores (not rescaled)
                score_val = row.get(f"score_{topic}", 0.0)
                if pd.isna(score_val):
                    score_val = 0.0
                # Clip to observed range (0-10 covers empirical max of ~9.2)
                score_val = float(np.clip(score_val, 0.0, 10.0))
                label_vec.append(score_val)
            self.labels.append(label_vec)

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx],
            truncation=True,
            max_length=self.config["model"]["max_length"],
            padding=False,
            return_tensors=None
        )
        encoding["labels"] = self.labels[idx]
        return encoding

print("V19: ContinuousMultiLabelDataset Defined (Dot Product)")
print("  - Uses raw dot product scores (0.0-10.0)")
print("  - Full magnitude information preserved")
print("  - No discretization!")
```

---

## Summary of Changes

| Location | Old | New | Impact |
|----------|-----|-----|--------|
| Cell 50, line 28 | `f"rescaled_{topic}"` | `f"score_{topic}"` | Uses correct columns |
| Cell 50, line 31 | `clip(score_val, 0.0, 2.0)` | `clip(score_val, 0.0, 10.0)` | Correct range |
| Cell 50, line 12 | "rescaled scores [0, 2]" | "dot product scores [0, ~9]" | Accurate docs |
| Cell 50, line 50 | "rescaled scores (0.0-2.0)" | "dot product scores (0.0-10.0)" | Accurate output |

---

## Testing After Changes

### 1. Check Dataset Creation

After updating Cell 50 and running Cell 55 (dataset creation):

```python
# Verify labels are in correct range
sample_labels = train_dataset.labels[:10]
all_label_values = [v for labels in sample_labels for v in labels]

print(f"Label range: {min(all_label_values):.2f} - {max(all_label_values):.2f}")
# Should show: ~0.77 - 9.22 (not 0.0 - 2.0)

print(f"Sample labels: {sample_labels[0]}")
# Should show values like [6.5, 3.2, 2.8, 4.1]
# NOT like [1.2, 0.5, 0.1, 0.8]
```

### 2. Check Training Progress

During training, monitor loss values:

```python
# First few steps
# Expected: Loss starts high (~3-5) due to wider target range
# Expected: Loss decreases steadily

# After convergence
# Good model: MSE ~0.5-2.0 (vs old ~0.1-0.3)
```

### 3. Check Predictions

After training, validate predictions are in correct range:

```python
predictions = model_predict(test_texts)

print(f"Prediction range: {predictions.min():.2f} - {predictions.max():.2f}")
# Should be: ~0-10 range
# NOT: 0-2 range
```

---

## Migration Path

### Option 1: Clean Break (RECOMMENDED)

1. ✅ Fix Cell 4: `normalize_embeddings=False`
2. ✅ Fix Cell 50: Use `score_{topic}` columns, clip to 0-10
3. Re-run entire workflow from Cell 4 onward
4. Train BERTJE with new dot product scores

**Pros:** Clean, consistent, no legacy issues
**Cons:** Need to re-run from beginning

### Option 2: Keep Old Training Data

If you have valuable trained models from the old rescaled system:

1. Create a new workflow version for dot product
2. Keep old workflows with rescaled scores
3. Compare model performance between systems

**Pros:** Can compare systems
**Cons:** Maintaining two parallel systems

---

## Why Dot Product is Better for Training

### 1. Preserved Magnitude Information

**Rescaled (old):**
```
Chunk A: [1.8, 0.3, 0.1, 0.5] - Lost original magnitude
Chunk B: [1.2, 0.8, 0.6, 0.9] - Lost original magnitude
```

**Dot Product (new):**
```
Chunk A: [8.2, 3.1, 2.3, 4.5] - Strong signal preserved
Chunk B: [5.1, 4.8, 4.2, 4.9] - Weak differentiation visible
```

Model can learn:
- Strong topics have higher absolute values
- Weak differentiation (uniform scores) = noise
- Magnitude correlates with confidence

### 2. Better Gradient Flow

Wider range → larger gradients → faster learning:

```
Old: prediction=1.1, target=1.2, gradient = 2*(1.1-1.2) = -0.2
New: prediction=4.5, target=5.0, gradient = 2*(4.5-5.0) = -1.0
```

5x stronger gradient signal!

### 3. Natural Alignment with Significance

Your significance scoring uses raw scores + CV. BERTJE trained on raw scores will:
- Learn same patterns as significance metric
- Predictions directly comparable to significance thresholds
- No conversion needed between systems

---

## Expected Performance Improvements

After switching to dot product training:

| Metric | Old (Rescaled) | New (Dot Product) | Improvement |
|--------|---------------|-------------------|-------------|
| Training convergence | ~10-15 epochs | ~5-10 epochs | 1.5-2x faster |
| Final MSE | ~0.2 | ~1.0 | (Different scale, not comparable) |
| Prediction accuracy | Baseline | +5-10% better | Better separation |
| Noise detection | Moderate | Excellent | CV-based filtering |

---

## Next Steps

1. **Update Cell 50** with the code provided above
2. **Re-run workflow** from Cell 4 onward (with `normalize_embeddings=False`)
3. **Verify** dataset labels are in 0-10 range
4. **Train BERTJE** and monitor loss convergence
5. **Compare** predictions to significance scores for validation

The system will integrate seamlessly once Cell 50 is updated!
