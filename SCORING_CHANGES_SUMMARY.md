# Scoring System Changes - Summary

## Date: 2025-12-04

## Overview
Replaced the compressed cosine similarity + complex rescaling system with a simpler, more expressive **dot product** scoring approach.

## Problems with Old System

### 1. Normalized Embeddings
- Used `normalize_embeddings=True` in SBERT
- All vectors forced to unit length (norm = 1.0)
- Embeddings sit on hypersphere surface

### 2. Cosine Similarity Compression
```python
# Old formula
cosine = dot(a, b) / (||a|| × ||b||)
```
- Division by norms cancels out magnitude information
- Scores compressed to narrow range (0.07-0.65)
- Poor discrimination between relevance levels

### 3. Complex Rescaling Required
- 3-stage transformation needed:
  1. Normalize to 0-1 based on observed min/max
  2. Power transform (^1.8) to spread high scores
  3. Margin bonus to reward confident classifications
- Artificial, hard to interpret
- Parameters tuned to specific dataset

## New System

### 1. Unnormalized Embeddings
```python
def st_embed(texts: list, batch_size: int = 256) -> np.ndarray:
    return st_model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=False,
        normalize_embeddings=False  # ← Changed from True
    )
```
- Embeddings retain natural magnitude
- Higher magnitude = stronger semantic content

### 2. Dot Product Similarity
```python
def similarity_score(a: np.ndarray, b: np.ndarray) -> float:
    """Dot product - magnitude matters."""
    return float(np.dot(a, b))
```
- No normalization division
- Preserves magnitude information
- Natural, wide score range (typically 0-200+)

### 3. No Rescaling Needed
- Use raw dot product scores directly
- Percentile-based confidence thresholds
- Automatically adapts to score distribution

## Changes Made

### Cell 4 (st_embed function)
**Before:**
```python
normalize_embeddings=True
```

**After:**
```python
normalize_embeddings=False
```

### Cell 36 (Chunk Scoring)
**Before:**
```python
def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))

# ... complex rescaling with rescale_to_0_2 function
row[f'cos_{topic}'] = cosine(dv, tv)
```

**After:**
```python
def similarity_score(a: np.ndarray, b: np.ndarray) -> float:
    """Dot product - magnitude matters when embeddings are unnormalized."""
    return float(np.dot(a, b))

# No rescaling - use raw scores
row[f'score_{topic}'] = similarity_score(dv, tv)
```

**Removed:**
- Entire `rescale_to_0_2()` function (109 lines)
- All rescaling logic and rescaled_* columns
- Complex comparison statistics

### Cell 37 (Confidence Classification)
**Before:**
- Fixed thresholds based on rescaled 0-2 range
- 5-tier system: 0-0.25, 0.25-0.5, 0.5-1.0, 1.0-1.5, 1.5-2.0
- Compared original vs rescaled scores

**After:**
- Percentile-based thresholds (adapts to distribution)
- 5-tier system based on quantiles:
  - CORE: Top 10% (P90+) with high margin (P75+)
  - MODERATE: Above median (P50+) with decent margin (P25+)
  - WEAK: Above bottom quartile (P25+)
  - CONTEXT: Above noise threshold
  - NOISE: Very low scores
- No comparison needed (only one scoring system)

### Cells 44, 50, 52, 75, 76
- Replaced all `cos_` column references with `score_`
- Removed all `rescaled_` column references
- Updated to work with single score set

## Expected Benefits

### 1. Wider Natural Range
- **Old:** 0.07-0.65 (0.58 range)
- **New:** ~5-200 (195+ range, ~340x wider)

### 2. Better Discrimination
- Natural spread without artificial transforms
- Standard deviation likely 10-20x higher
- Easier to distinguish relevance levels

### 3. Meaningful Scores
- Scores reflect weighted topic vector magnitudes
- Higher weights → proportionally higher scores
- Direct relationship between dictionary weights and chunk scores

### 4. Simpler, More Interpretable
- No complex transformations
- Percentile-based thresholds are self-documenting
- Easier to explain and debug

### 5. More Robust
- Adapts to different corpora automatically
- No hardcoded min/max from specific dataset
- Percentiles adjust to actual distribution

## How to Use

### Running the Updated Notebook

1. **Start from Cell 4** (already has `normalize_embeddings=False`)
2. **Run through Cell 27** to generate unnormalized embeddings
3. **Run Cell 36** to score chunks with dot product
4. **Run Cell 37** to classify by confidence

### Checking Results

After running Cell 36, check the score distribution:
```python
print(all_scores_df['max_score'].describe())
```

You should see:
- **Min:** Near 0 (empty/irrelevant chunks)
- **Max:** 100-300+ (highly relevant chunks)
- **Std:** 20-50+ (good spread)
- **Range:** Much wider than 0.07-0.65

### Adjusting Confidence Thresholds

Cell 37 uses percentile-based thresholds. If you want to adjust:

```python
# Current defaults:
p90 = all_scores_df['max_score'].quantile(0.90)  # Top 10% = CORE
p50 = all_scores_df['max_score'].quantile(0.50)  # Above median = MODERATE

# To be more/less strict:
p95 = all_scores_df['max_score'].quantile(0.95)  # More strict (top 5%)
p80 = all_scores_df['max_score'].quantile(0.80)  # Less strict (top 20%)
```

## Compatibility Notes

### Output Files
The notebook still creates the same output files:
- `scores_all_labeled.csv`
- `scores_high_confidence.csv` (3-tier)
- `scores_low_confidence.csv` (3-tier)
- `scores_no_confidence.csv` (3-tier)
- `scores_core_confidence.csv` (5-tier)
- `scores_moderate_confidence.csv` (5-tier)
- `scores_weak_confidence.csv` (5-tier)
- `scores_context_confidence.csv` (5-tier)
- `scores_noise_confidence.csv` (5-tier)

### Column Names
- **Old:** `cos_Topic_Name`, `max_score_rescaled`, `rescaled_Topic_Name`
- **New:** `score_Topic_Name`, `max_score` (no rescaled versions)

### Downstream Code
Any code that loads these CSVs and references `cos_*` or `rescaled_*` columns will need updating to use `score_*` columns instead.

## Backup
A backup of the original notebook was saved to:
`A__dictionary_discovery_v19_unified_embedding.ipynb.backup`

## Testing Checklist

- [ ] Run Cell 4 - verify `normalize_embeddings=False`
- [ ] Run Cells up to 27 - generate unnormalized embeddings
- [ ] Run Cell 36 - check score distribution is wide (not 0.07-0.65)
- [ ] Run Cell 37 - verify confidence tiers make sense
- [ ] Check output CSVs have `score_*` columns (not `cos_*`)
- [ ] Verify high-quality chunks are in CORE/MODERATE tiers
- [ ] Verify noise/irrelevant chunks are in NOISE tier

## Questions?

If the new scores seem wrong:
1. Check embedding norms: `print([np.linalg.norm(e) for e in embeddings[:5]])`
   - Should vary (not all ~1.0)
2. Check score range: `print(all_scores_df['max_score'].min(), all_scores_df['max_score'].max())`
   - Should be wide (not 0.07-0.65)
3. Check topic vector norms: `print({topic: np.linalg.norm(vec) for topic, vec in topic2vec.items()})`
   - Should vary based on weights
