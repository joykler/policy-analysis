# Cross-Encoder Weight Fix - Summary

## Date: 2025-12-15

## Problem Identified

The cross-encoder implementation in v24 was using SIF (Smooth Inverse Frequency) weighting, which caused **extreme weight inflation**:

### Before Fix:
```
Weight range: 79.135 - 997.586
Average weight: 660.598
```

### Root Cause:
1. **Dictionary terms are extremely rare** in the corpus (most appear 0-1 times)
2. **SIF formula amplifies rare terms**: `weight = 1 / (0.001 + probability)`
3. For rare terms: `weight = 1 / (0.001 + 0.0000024) = 997.59`
4. **Cross-encoder doesn't need corpus-based weights** - it learns term importance through attention

### Impact:
- Score explosion after multiplying cross-encoder logits (-1 to +1) by weights (997)
- Final scores: -997 to +997 (uninterpretable)
- Training instability
- All chunks scoring < 0.5 despite having relevant content

---

## Changes Applied

### 1. Config Update (Cell 5)

**Scoring Section:**
```python
"scoring": {
    "use_sif": False,  # Changed from True
    # Disabled for cross-encoder - model learns term importance
}
```

**Weights Section:**
```python
"weights": {
    "default_core_weight": 1.0,        # Unchanged
    "default_discovered_weight": 0.7,  # Changed from 0.8
    "weighting_scheme": "seed_only",   # Changed from "multiplicative"
    # Cross-encoder only needs seed weights
}
```

### 2. Function Update (Cell 32)

Added new case to `hybrid_weight()` function:

```python
def hybrid_weight(term: str, seed_weight: float) -> float:
    '''Combine seed dictionary weight with corpus-based SIF weight.'''

    # For cross-encoder: use seed weights only (model learns term importance)
    if weighting_scheme == "seed_only":
        return seed_weight

    # Legacy weighting schemes (for bi-encoder compatibility)
    sif_w = sif_weight(term)
    # ... rest of function ...
```

---

## Expected Results

### After Fix:
```
Weight range: 0.7 - 1.0
Average weight: ~0.85

Weight distribution:
  - Core seed terms (manually curated): 1.0
  - Discovered terms (expanded): 0.7
```

### Score Interpretation:
```
Cross-encoder scores after training:
  -1.0 to -0.5  = Definitely not relevant
  -0.5 to  0.0  = Probably not relevant
   0.0 to +0.5  = Weakly relevant
  +0.5 to +0.8  = Moderately relevant (high confidence)
  +0.8 to +1.0  = Highly relevant (very high confidence)
```

---

## Why This Works for Cross-Encoder

### Cross-Encoder Architecture:
```
Input: [CLS] chunk_text [SEP] term [SEP]
        ↓
    Full cross-attention between chunk and term
        ↓
    Binary relevance classifier
        ↓
    Logit: -1 (irrelevant) to +1 (relevant)
```

### Key Differences from Bi-Encoder:

| Aspect | Bi-Encoder | Cross-Encoder |
|--------|------------|---------------|
| **Interaction** | None (separate encoding) | Full attention |
| **Needs SIF?** | Yes (no term-level learning) | No (learns per-term) |
| **Weights** | Corpus-based helpful | Seed preference only |
| **Score Scale** | 0-200+ (arbitrary) | -1 to +1 (calibrated) |

### Why Seed Weights Still Matter:
- **Core terms (1.0)**: Manually curated, domain expert knowledge
- **Discovered terms (0.7)**: Automatically expanded, less certain
- **Gives slight preference** to expert-curated terms during aggregation
- **Doesn't overwhelm** the cross-encoder's learned attention

---

## Next Steps

### 1. Re-run Checkpoint 4 & 5:
```python
# Checkpoint 4: Build weighted topic vectors
# Expected output:
#   Weight range: 0.700 - 1.000
#   Avg weight: 0.850

# Checkpoint 5: Score chunks
# Expected output:
#   Score range: -0.8 to +0.9 (after training)
#   Interpretable thresholds work correctly
```

### 2. Train Cross-Encoder (Checkpoint 6-7):
- Use high-significance chunks as training data
- Model will learn which terms are important
- Should see confident predictions (scores > 0.5) after training

### 3. Validate Results:
- Compare to human labels
- Check precision/recall improvements
- Verify interpretable score thresholds

---

## Backward Compatibility

The changes maintain **backward compatibility** with bi-encoder approaches:

```python
# To use bi-encoder with SIF (old method):
CONFIG = {
    "scoring": {"use_sif": True},
    "weights": {"weighting_scheme": "multiplicative"}
}

# Cross-encoder will use the legacy code path
# All old weighting schemes still work
```

---

## Technical Notes

### SIF Formula (for reference):
```python
def sif_weight(term):
    probability = term_frequency / total_corpus_frequency
    a = 1e-3  # smoothing parameter
    return 1.0 / (a + probability)
```

**Why it causes inflation:**
- Common terms (p=0.1): weight = 1/(0.001 + 0.1) = 9.9
- Rare terms (p=0.000001): weight = 1/(0.001 + 0.000001) = 999

**Why it's wrong for cross-encoder:**
- Corpus mismatch: Dictionary terms from different domain
- Redundant: Cross-encoder learns term importance via attention
- Unstable: Extreme weights cause gradient explosion

---

## Files Modified

1. **A__dictionary_discovery_v24_policy_crossencoder.ipynb**
   - Cell 5: CONFIG (scoring and weights sections)
   - Cell 32: hybrid_weight function

2. **Generated files** (temporary):
   - update_notebook_weights.py (can be deleted)

---

## Verification

Run this code to verify the fix works:

```python
import json
from pathlib import Path

# After re-running Checkpoint 4
topic_meta_path = Path("workflow_data/.../Other_data/topic_terms_meta.json")
with open(topic_meta_path) as f:
    meta = json.load(f)

print("Weighting scheme:", meta['weighting_scheme'])
print("Use SIF:", meta['use_sif'])

# Load weighted terms
topic_terms_path = Path("workflow_data/.../Other_data/topic_terms_weighted.json")
with open(topic_terms_path) as f:
    terms = json.load(f)

for topic, term_weights in terms.items():
    weights = [w for _, w in term_weights]
    print(f"\n{topic}:")
    print(f"  Range: {min(weights):.2f} - {max(weights):.2f}")
    print(f"  Avg: {sum(weights)/len(weights):.2f}")

# Expected output:
# Weighting scheme: seed_only
# Use SIF: False
# Range: 0.70 - 1.00
# Avg: 0.85
```

---

## Summary

✅ **Fixed extreme weight inflation** (997 → 1.0)
✅ **Disabled redundant SIF weighting** for cross-encoder
✅ **Maintained seed weight preferences** (core=1.0, discovered=0.7)
✅ **Preserved bi-encoder compatibility**
✅ **Enables interpretable scoring** after training

The cross-encoder can now learn term importance through its attention mechanism without interference from corpus-based weights that were causing score explosion.
