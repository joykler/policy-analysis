# V18 Complete: 5-Tier Quality Classification

## ✅ Cell 5.2 Updated with Noise Category

Cell 5.2 now provides **5-tier quality classification** instead of 4-tier, separating truly irrelevant chunks.

---

## New 5-Tier System

### Quality Tiers (0-2 Rescaled Score)

| Tier | Score Range | Meaning | Use Case |
|------|-------------|---------|----------|
| **Core** | 1.5 - 2.0 | High-quality topic content | High-quality training data, fine-tuning |
| **Moderate** | 1.0 - 1.5 | Clearly relevant | Standard training data, evaluation |
| **Weak** | 0.5 - 1.0 | Peripheral mentions | Background context, edge cases |
| **Context** | 0.25 - 0.5 | Background context only | Negative examples |
| **Noise** | 0 - 0.25 | Irrelevant/noise | **FILTER OUT** |

### Why 5 Tiers?

The previous 4-tier system lumped together:
- Background context (somewhat related but not useful)
- Complete noise (totally irrelevant)

The new **Noise tier (0-0.25)** separates truly irrelevant chunks that should be filtered out completely.

---

## Expected Output from Cell 5.2

### 1. Statistics Comparison
```
SCORE COMPARISON: ORIGINAL vs RESCALED
================================================================================
Metric               Original (Cosine)         Rescaled (0-2)            Improvement
--------------------------------------------------------------------------------
Std Dev              0.0668                    0.2679                    4.01x
```

### 2. Five-Tier Classification
```
Rescaled Classification (0-2 interpretable, 5 tiers):
  Core (1.5-2.0):        380 ( 25.0%)  ← High-quality topic content
  Moderate (1.0-1.5):    380 ( 25.0%)  ← Clearly relevant
  Weak (0.5-1.0):        380 ( 25.0%)  ← Peripheral mentions
  Context (0.25-0.5):    285 ( 18.8%)  ← Background context only
  Noise (0-0.25):         95 (  6.2%)  ← Irrelevant/noise
```

### 3. Sample Chunks from Each Tier

Shows 2 examples from each tier including **NOISE examples**:

```
NOISE EXAMPLES:

  Chunk ID: xyz789
  Primary topic: Governance Distrust & Corruption
  Original score: 0.0873 (margin: 0.0005)
  Rescaled score: 0.0124
  Text: Bijlage A: Lijst van geraadpleegde documenten.
        1. Reglement van Orde 2019
        2. Jaarverslag financiën 2020
        3. Correspondentie...

  Chunk ID: abc123
  Primary topic: Educational Disadvantage & Brain Drain
  Original score: 0.0697 (margin: 0.0003)
  Rescaled score: 0.0089
  Text: Inhoudsopgave
        1. Inleiding ..................... 3
        2. Methode ....................... 5
        3. Resultaten .................... 8
```

**Key insight**: Noise tier catches bibliographies, tables of contents, headers, etc.

### 4. Quality Distribution Summary
```
QUALITY DISTRIBUTION SUMMARY
================================================================================

Chunk Distribution by Quality Tier:
  Core        :  380 ( 25.0%) - Cumulative:  380 ( 25.0%)
  Moderate    :  380 ( 25.0%) - Cumulative:  760 ( 50.0%)
  Weak        :  380 ( 25.0%) - Cumulative: 1140 ( 75.0%)
  Context     :  285 ( 18.8%) - Cumulative: 1425 ( 93.8%)
  Noise       :   95 (  6.2%) - Cumulative: 1520 (100.0%)
```

### 5. Usage Recommendations
```
QUALITY TIER RECOMMENDATIONS
================================================================================

Recommended Use by Tier:
  CORE (380 chunks):
    → Use for: High-quality training data, model fine-tuning
    → Confidence: Very high - these are clearly on-topic

  MODERATE (380 chunks):
    → Use for: Standard training data, evaluation sets
    → Confidence: High - relevant but less central

  WEAK (380 chunks):
    → Use for: Background context, edge cases
    → Confidence: Medium - peripheral relevance
    → Consider: Manual review before use

  CONTEXT (285 chunks):
    → Use for: Negative examples (what's NOT core content)
    → Confidence: Low - mostly background/setup
    → Recommend: Exclude from training data

  NOISE (95 chunks):
    → Use for: Negative examples, noise detection
    → Confidence: Very low - likely irrelevant
    → Recommend: Filter out completely
```

### 6. Final Summary
```
✓ Classification complete: 1520 chunks scored and classified
✓ High-quality data (Core + Moderate): 760 chunks (50.0%)
✓ Should filter out (Context + Noise): 380 chunks (25.0%)
```

---

## How to Use the Output

### Filter High-Quality Chunks
```python
import pandas as pd

df = pd.read_csv('scores_all_labeled.csv')

# High-quality training data
high_quality = df[df['confidence_rescaled'].isin(['core', 'moderate'])]
print(f"High-quality chunks: {len(high_quality)}")

# Filter out noise
clean_data = df[~df['confidence_rescaled'].isin(['context', 'noise'])]
print(f"After filtering: {len(clean_data)}")
```

### Analyze What Gets Filtered
```python
# Check what's being classified as noise
noise_chunks = df[df['confidence_rescaled'] == 'noise']

print("Noise chunks sample:")
for _, row in noise_chunks.head(10).iterrows():
    print(f"\nScore: {row['max_score_rescaled']:.3f}")
    print(f"Text: {row['raw_text'][:150]}")
```

### Create Training Tiers
```python
# Different quality tiers for different purposes
training_tiers = {
    'premium': df[df['confidence_rescaled'] == 'core'],
    'standard': df[df['confidence_rescaled'] == 'moderate'],
    'background': df[df['confidence_rescaled'] == 'weak'],
    'negative_examples': df[df['confidence_rescaled'].isin(['context', 'noise'])]
}

for tier, data in training_tiers.items():
    print(f"{tier}: {len(data)} chunks")
```

---

## New Columns in Output CSV

Cell 5.2 creates:

1. **`confidence_original`** - Original 3-tier classification
   - Values: 'high', 'medium', 'low'

2. **`confidence_rescaled`** - New 5-tier classification
   - Values: 'core', 'moderate', 'weak', 'context', 'noise'

Both are included in the output CSV for comparison.

---

## Key Benefits of Noise Tier

### 1. **Clearer Filtering**
- Before: "Context" included both background info AND noise
- After: Clear separation between somewhat-related and truly irrelevant

### 2. **Better Training Data**
- Can confidently exclude noise tier (0-0.25)
- Context tier (0.25-0.5) might still have some value as negative examples
- Clear quality gradient

### 3. **Quality Validation**
- Easy to spot if scoring is working (noise should be obvious junk)
- Can manually verify noise samples to confirm threshold is correct
- Helps tune NOISE_THRESHOLD if needed

### 4. **Data Cleaning**
- Automatically identifies metadata, headers, TOCs, bibliographies
- Catches chunks that shouldn't have been in corpus
- Helps improve data preprocessing for future runs

---

## Threshold Tuning (Optional)

If you want to adjust the noise threshold:

```python
# In Cell 5.2, change:
NOISE_THRESHOLD = 0.25   # Default (bottom ~6%)

# More aggressive noise filtering:
NOISE_THRESHOLD = 0.35   # Filters bottom ~10-15%

# Less aggressive:
NOISE_THRESHOLD = 0.15   # Filters only bottom ~2-3%
```

Current 0.25 threshold is based on data analysis showing natural break in score distribution.

---

## Summary

**Cell 5.2 now provides:**
- ✅ 5-tier quality classification (core/moderate/weak/context/noise)
- ✅ Separate noise tier for truly irrelevant chunks (0-0.25)
- ✅ Sample chunks from ALL tiers including noise
- ✅ Usage recommendations for each tier
- ✅ Clear filtering guidance (filter out context + noise = bottom 25%)
- ✅ Both classification systems in output CSV

**Bottom ~6% of chunks** are now flagged as **noise** and should be filtered out completely!
