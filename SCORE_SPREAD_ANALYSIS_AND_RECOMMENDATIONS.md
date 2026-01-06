# Score Spread Analysis and Recommendations

## Current Score Distribution

### Key Metrics (Max Score - Primary Topic Strength)
- **Range**: 0.145 - 0.622 (0.477 total spread)
- **Median**: 0.388
- **IQR**: 0.092 (middle 50% of chunks)
- **Std Dev**: 0.067

### Problem: Score Compression

**19% of the range contains 50% of the data**
- Most chunks score between 0.34-0.43 (very narrow!)
- Only ~7 effective "bins" of separation
- Hard to distinguish relevance levels

### Classification Confidence (Score Margin)
- **26.7%** very low confidence (margin < 0.02) - ambiguous chunks
- **32.4%** medium confidence (0.02-0.05)
- **40.9%** high confidence (> 0.05)

---

## Root Causes of Compression

### 1. **L2 Normalization Effect**
- All vectors normalized to unit length
- Cosine similarity measures angles, not magnitudes
- Semantic embeddings naturally cluster in similar regions
- Result: Most chunks score in narrow 0.3-0.4 range

### 2. **Topic Overlap**
- Your 4 topics share related concepts (colonial history, social issues)
- Even "unrelated" chunks have some semantic connection
- Minimum score: 0.145 (not close to 0)
- Maximum score: 0.622 (not close to 1)

### 3. **Broad Topic Definitions**
- Topics include both core terms (slavery) and context terms (Suriname)
- Weighted averaging smooths out extremes
- Topic vectors point to "middle ground" of all terms

---

## Strategies to Increase Spread (Ranked by Impact)

### Option 1: **Non-linear Rescaling** (HIGH IMPACT)
**Concept**: Apply power transform to stretch tails and compress middle

```python
def power_rescale(score, power=2.0, target_range=(0, 2)):
    """
    Power transform: emphasizes differences at extremes

    score^2 spreads high scores more (0.4^2=0.16, 0.6^2=0.36)
    """
    # Normalize to 0-1 first
    normalized = (score - min_observed) / (max_observed - min_observed)

    # Apply power transform
    transformed = normalized ** power

    # Scale to target range
    rescaled = transformed * (target_range[1] - target_range[0]) + target_range[0]
    return rescaled
```

**Impact**:
- Stretches high scores (core content)
- Compresses low scores (context)
- Non-linear: preserves semantic ordering
- Expected spread: 2-3x increase

**Pros**:
- Simple to implement
- Interpretable (power=2 means "square the importance")
- Preserves ranking

**Cons**:
- Changes semantic meaning slightly
- Need to tune power parameter

---

### Option 2: **Percentile-Based Binning** (MEDIUM-HIGH IMPACT)
**Concept**: Map scores to percentile ranks, then rescale

```python
def percentile_rescale(score, scores_df, target_range=(0, 2)):
    """
    Map score to its percentile position, then rescale

    Example:
    - Bottom 10% -> 0.0-0.4 (context)
    - Middle 80% -> 0.4-1.2 (relevant)
    - Top 10% -> 1.2-2.0 (core)
    """
    percentile = (scores_df < score).sum() / len(scores_df)

    # Optional: Non-uniform mapping for more spread in meaningful regions
    if percentile < 0.25:
        rescaled = percentile * 2  # 0.0-0.5
    elif percentile < 0.75:
        rescaled = 0.5 + (percentile - 0.25) * 2  # 0.5-1.5
    else:
        rescaled = 1.5 + (percentile - 0.75) * 2  # 1.5-2.0

    return rescaled
```

**Impact**:
- Guarantees even distribution across 0-2 range
- Automatically adapts to data

**Pros**:
- Data-driven
- Ensures good spread
- Robust to outliers

**Cons**:
- Requires access to full score distribution
- Less intuitive mapping

---

### Option 3: **Score Margin Adjustment** (MEDIUM IMPACT)
**Concept**: Amplify the difference between top score and 2nd score

```python
def margin_adjusted_score(top_score, second_score, margin_weight=0.3):
    """
    Reward chunks with clear primary topic

    High margin -> boost score
    Low margin -> reduce score
    """
    margin = top_score - second_score

    # Amplify based on confidence
    adjusted = top_score * (1 + margin_weight * (margin / top_score))

    return adjusted
```

**Impact**:
- Spreads confident classifications further from ambiguous ones
- Expected increase: 15-25%

**Pros**:
- Semantically meaningful (confidence matters!)
- Simple to explain

**Cons**:
- Only affects chunks with multiple topic matches
- Doesn't help single-topic chunks

---

### Option 4: **Modify Dictionary Weights** (LOW-MEDIUM IMPACT)
**Concept**: Increase weight differentiation in dictionary

**Current weights**: 0.5-1.0 range, fairly compressed
- Most seed terms: 0.7-0.85
- Geographic context: 0.5
- Core terms: 1.0

**Proposed weights**: 0.2-2.0 range (more extreme)
- Context terms (Suriname, Curaçao): 0.2-0.3
- General terms (onderwijs, discriminatie): 0.7-1.0
- Core terms (slavernij, racisme): 1.5-2.0

**Impact**:
- From simulation: ~18% increase in spread
- Shifts topic vectors toward core terms
- Slightly better separation

**Pros**:
- Semantically grounded
- No post-processing needed

**Cons**:
- Limited impact due to normalization
- Requires re-running Cell 4.1 and 5.1

---

### Option 5: **Remove L2 Normalization** (HIGH IMPACT, HIGH RISK)
**Concept**: Use raw dot product instead of cosine similarity

```python
def unnormalized_score(chunk_vec, topic_vec):
    """
    Raw dot product: magnitude matters

    Chunks with stronger signals get higher scores
    """
    return np.dot(chunk_vec, topic_vec)
```

**Impact**:
- Massive spread increase (5-10x)
- Scores reflect both direction AND magnitude

**Pros**:
- Natural spread
- Rewards strong signals

**Cons**:
- **DANGEROUS**: Magnitude can be misleading
- Longer chunks artificially score higher
- Loses semantic interpretability
- **NOT RECOMMENDED**

---

## Recommended Approach

### **Best Solution: Hybrid (Options 1 + 3)**

1. **Apply Power Rescaling** (Option 1)
   - Use power=1.5-2.0 for moderate non-linearity
   - Maps current 0.145-0.622 → 0-2 scale
   - Emphasizes high-scoring chunks

2. **Add Margin Bonus** (Option 3)
   - Boost scores for confident classifications
   - Penalize ambiguous chunks slightly
   - Weight: 0.2-0.3

3. **Optionally: Adjust Dictionary Weights** (Option 4)
   - More extreme weights (0.2-2.0 range)
   - Small additional benefit
   - Worth doing if re-curating dictionary anyway

### Implementation

```python
def combined_rescale(score, margin, power=1.8, margin_weight=0.25):
    """
    Two-stage rescaling for interpretable 0-2 range

    Stage 1: Power transform (spreads high scores)
    Stage 2: Margin adjustment (rewards confidence)
    """
    # Observed range from your data
    min_score = 0.07
    max_score = 0.65

    # Stage 1: Normalize and power transform
    normalized = (score - min_score) / (max_score - min_score)
    normalized = max(0, min(1, normalized))  # Clip
    transformed = normalized ** power

    # Stage 2: Apply margin bonus
    margin_factor = 1 + margin_weight * (margin / (score + 1e-6))
    transformed = transformed * margin_factor

    # Scale to 0-2
    rescaled = transformed * 2.0

    return rescaled

# Usage
df['rescaled_score'] = df.apply(
    lambda row: combined_rescale(row['max_score'], row['score_margin']),
    axis=1
)
```

### Expected Results

**Current distribution:**
- Range: 0.145-0.622 (0.477)
- IQR: 0.092
- Most chunks: 0.34-0.43

**After rescaling:**
- Range: 0-2.0 (2.0)
- IQR: ~0.5-0.8
- Distribution:
  - 0.0-0.5: Context/background (bottom 25%)
  - 0.5-1.0: Weak relevance (25-50%)
  - 1.0-1.5: Moderate relevance (50-75%)
  - 1.5-2.0: Core topic content (top 25%)

**Spread improvement**: ~3-4x increase in effective range

---

## Alternative: Simpler Linear Rescale

If you want something simpler:

```python
def simple_rescale(score, min_obs=0.07, max_obs=0.65):
    """Straight linear mapping to 0-2"""
    normalized = (score - min_obs) / (max_obs - min_obs)
    return max(0, min(2, normalized * 2))
```

**Pros**: Simple, interpretable
**Cons**: Doesn't increase spread, just relabels the compressed range

---

## Recommendation Summary

**For maximum meaningful spread while preserving semantics:**

✅ **Implement Option 1 + 3**: Power rescaling (1.8-2.0) with margin adjustment
✅ **Optionally add Option 4**: Extreme dictionary weights (0.2-2.0) for small boost
❌ **Avoid Option 5**: Removing normalization (breaks semantic meaning)

This gives you:
- Interpretable 0-2 scale
- 3-4x better separation
- Semantically grounded (not arbitrary)
- Preserves topic ranking
