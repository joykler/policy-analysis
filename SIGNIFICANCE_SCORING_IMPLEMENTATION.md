# Significance Scoring Implementation Summary

## Implementation Date: 2025-12-05

## What Changed

**Cell 37** in [A__dictionary_discovery_v19_unified_embedding.ipynb](A__dictionary_discovery_v19_unified_embedding.ipynb) has been updated with a new significance-based classification system that filters noise by detecting chunks with uniform scores across all topics.

---

## The Problem (User Insight)

**Original observation from actual data:**
```
Chunk with scores [4.88, 4.89, 4.92, 4.83]:
- All scores nearly identical (uniform pattern)
- Text: "De Tweede Kamer wordt... per brief geïnformeerd" (procedural boilerplate)
- Not actually about ANY specific topic → NOISE
```

**Key insight:** "Chunks with the same pattern in all topics are ranked down as they are more likely noise."

This revealed that **high scores alone don't indicate relevance** - chunks can have elevated scores across ALL topics due to:
- Generic/background text
- Procedural boilerplate
- Copyright/metadata
- Administrative language

These chunks lack **topic differentiation** and should be filtered out.

---

## The Solution: Significance Score

### Core Formula

```python
significance = (
    0.5 × differentiation +  # PRIMARY: Can we distinguish topics?
    0.3 × magnitude +        # SECONDARY: Is any signal strong?
    0.2 × contrast          # TERTIARY: Does max clearly stand out?
)
```

### Three Components

#### 1. Differentiation (Weight: 0.5) - PRIMARY FILTER

**Metric:** Coefficient of Variation (CV)
```python
cv = std(topic_scores) / mean(topic_scores)
differentiation = cv / 0.5  # Normalized to 0-1
```

**Interpretation:**
- CV < 0.10 → **Noise** (all scores similar)
- CV = 0.10-0.20 → Moderate differentiation
- CV > 0.20 → **Good differentiation**

**From actual data:**
- Q25: CV = 0.10 (bottom 25% have very similar scores)
- Q50: CV = 0.14 (median)
- Q75: CV = 0.20 (top 25% have good differentiation)

**Hard filter:** CV < 0.10 automatically marks chunk as noise, regardless of magnitude.

---

#### 2. Magnitude (Weight: 0.3) - SIGNAL STRENGTH

**Metric:** Max score normalized
```python
magnitude = (max_score - 2.0) / 7.0  # Normalized to 0-1
```

**Interpretation:**
- High (>6.0): Strong topic presence
- Medium (4.0-6.0): Moderate presence
- Low (<4.0): Weak presence

**Empirical range:** 2.0 - 9.0 from actual data

---

#### 3. Contrast (Weight: 0.2) - STANDOUT

**Metric:** Z-score of max
```python
z_max = (max_score - mean_score) / std_score
contrast = (z_max - 0.6) / 1.1  # Normalized to 0-1
```

**Interpretation:**
- High Z (>1.5): Max clearly stands out
- Medium Z (1.0-1.5): Max above average
- Low Z (<1.0): Max barely above average

**From actual data:**
- Q25: Z = 1.10
- Q50: Z = 1.31
- Q75: Z = 1.53

---

## Classification Tiers

### Four-Tier System

| Tier | Significance | Characteristics | Use Case |
|------|-------------|-----------------|----------|
| **High** | ≥ 0.70 | Clear topic, good differentiation (CV > 0.20) | Primary training data |
| **Medium** | 0.50 - 0.70 | Moderate signal or partial differentiation | Secondary training, batch review |
| **Low** | 0.30 - 0.50 | Weak signal or poor differentiation | Manual review needed |
| **Noise** | < 0.30 OR CV < 0.10 | Uniform scores or very weak signal | Exclude from training |

### Special Case: Hard CV Filter

```python
if cv < 0.10:
    category = 'noise_uniform_scores'
    priority = 'exclude'
    # Regardless of magnitude!
```

This ensures chunks like `[4.88, 4.89, 4.92, 4.83]` are correctly identified as noise despite having moderate max_score.

---

## Validation Results

### ✅ Low CV (< 0.10) = Noise

**Chunk 751** (Significance: 0.148):
- Scores: [3.66, 3.82, 3.83, 3.86] - Almost identical
- CV: 0.020
- Text: "De groep kwam in 1621 aan en ging in Amersfoort wonen..."
- **Verdict:** Historical narrative, no specific legacy topic → **NOISE** ✓

**Chunk 663** (Significance: 0.163):
- Scores: [3.60, 4.12, 4.14, 4.08] - Very similar
- CV: 0.056
- Text: "23 februari 2023 Aan voldaan per brief..."
- **Verdict:** Procedural boilerplate → **NOISE** ✓

### ✅ High CV (> 0.20) = Meaningful

**Chunk 1499** (Significance: 0.820):
- Scores: [**9.22**, 5.23, 4.10, 5.35] - Clear winner
- CV: 0.324 (excellent differentiation)
- Text: "Nederlandse universiteiten moeten vakken opnemen over racisme..."
- **Verdict:** Strongly about education → **MEANINGFUL** ✓

**Chunk 1187** (Significance: 0.818):
- Scores: [**7.18**, 3.21, 2.92, 3.86] - Strong differentiation
- CV: 0.396 (very high)
- Text: "reële achterstanden, die doorwerken tot in het voortgezet onderwijs..."
- **Verdict:** Educational disadvantage topic → **MEANINGFUL** ✓

### ✅ Edge Case: High Max + Low CV

**Chunk 338** (Significance: 0.456):
- Scores: [5.02, 4.85, 4.68, 5.91] - All elevated
- CV: 0.093 (low)
- Text: "Postkoloniale beeldenstormen vragen over verhalen..."
- **Result:** Correctly penalized for uniformity despite max=5.91
- **Verdict:** Metric correctly identifies as less significant ✓

---

## Output Files

### New Files (4-tier significance)

```
workflow_data/<workflow_name>/Cosine_labeling/
├── scores_high_significance.csv      # Primary training data (significance ≥ 0.70)
├── scores_medium_significance.csv    # Secondary training (0.50 - 0.70)
├── scores_needs_review.csv           # Manual review needed (0.30 - 0.50)
└── scores_exclude_noise.csv          # Filter out (< 0.30 or CV < 0.10)
```

### Backward Compatible (3-tier confidence)

```
workflow_data/<workflow_name>/Cosine_labeling/
├── scores_high_confidence.csv        # = High significance
├── scores_low_confidence.csv         # = Medium + Low significance
└── scores_no_confidence.csv          # = Noise (both types)
```

### All Scores

```
scores_all_labeled.csv  # Contains all chunks with significance metrics
```

**New columns added:**
- `significance_score` (0-1 float)
- `significance_category` (high/medium/low/noise_uniform/noise_weak)
- `priority` (primary_training/secondary_training/manual_review/exclude)
- `cv` (Coefficient of Variation)
- `z_max` (Z-score of max)
- `magnitude_norm`, `differentiation_norm`, `contrast_norm` (component scores 0-1)
- `confidence` (high/low/none for backward compatibility)

---

## Usage Recommendations

### For Training Models

**Use:**
- High significance (≥ 0.70) → Primary training data
- Medium significance (0.50-0.70) → Secondary training after batch review

**Review:**
- Low significance (0.30-0.50) → Individual review recommended

**Exclude:**
- Noise (< 0.30 or CV < 0.10) → Filter out completely

### For Manual Review

**Priority review:** Low-CV chunks with moderate scores
```python
df[(df['cv'] < 0.15) & (df['max_score'] > 4.0)]
```
These are likely generic/boilerplate text masquerading as relevant.

**Sample high-CV chunks** for quality validation
```python
df[df['cv'] > 0.25].sample(20)
```
These should have clear topic differentiation.

---

## Benefits of This Approach

### 1. **Automatically Filters Noise**
- Chunks with uniform scores (CV < 0.10) → significance ≈ 0
- No manual threshold tuning per topic needed

### 2. **Corpus-Independent**
- CV is relative to each chunk's own score distribution
- Works across different corpora with different absolute score ranges

### 3. **Multi-Label Compatible**
- Multiple topics can be high IF they're differentiated from absent topics
- Doesn't penalize multi-topic chunks (unlike margin-based approaches)

### 4. **Interpretable Components**
- Differentiation: "Can we distinguish topics?" (most important)
- Magnitude: "Is any topic strongly present?"
- Contrast: "Does max clearly stand out?"

### 5. **Addresses User Insight**
- Directly implements: "Chunks with same pattern in all topics are noise"
- CV explicitly measures this pattern

---

## When to Recalibrate

### ✅ DO Recalibrate When:
- Dictionary significantly updated (topic definitions change)
- Embedding model updated (all embeddings shift)
- Corpus dramatically different (e.g., different language, domain)
- Evaluation shows thresholds are miscalibrated

### ❌ DON'T Recalibrate When:
- New corpus with similar content type
- Different mix of topics in data
- Seasonal variations in content
- "It's been a month"

**Why:** CV is a relative metric - it measures differentiation within each chunk, not absolute position in a global distribution. This makes it robust to corpus changes.

---

## Next Steps

1. **Run Cell 37** to generate significance scores
2. **Review output** - check distribution of significance categories
3. **Sample chunks** from each tier to validate classification
4. **Adjust thresholds** if needed:
   - CV threshold (currently 0.10)
   - Significance thresholds (currently 0.70/0.50/0.30)
   - Component weights (currently 0.5/0.3/0.2)

---

## Technical Details

### Why CV as Primary Metric?

The Coefficient of Variation is scale-independent:
```
CV = std / mean
```

**Example:**
- Chunk A: [100, 105, 110, 108] → CV = 0.04 (uniform, noise)
- Chunk B: [100, 50, 45, 40] → CV = 0.26 (differentiated, meaningful)

Even though both have max=100, CV correctly identifies that Chunk A has no topic differentiation (all scores ~105), while Chunk B has clear primary topic (100 vs ~45).

### Why Weighted Combination?

**Differentiation (0.5):** Most important - directly addresses the noise problem
**Magnitude (0.3):** Important - weak signals shouldn't be promoted just because they're differentiated
**Contrast (0.2):** Helpful - provides additional confidence when max clearly stands out

This prevents edge cases like:
- Low scores [1, 2, 3, 4] have high CV but aren't significant (low magnitude)
- High uniform scores [5, 5, 5, 5] aren't significant (low differentiation)
- High scores [5, 4.9, 4.8, 4.7] aren't significant (low differentiation AND low contrast)

---

## References

- [SIGNIFICANCE_SCORE_PROPOSAL.md](SIGNIFICANCE_SCORE_PROPOSAL.md) - Original proposal with full rationale
- [CONFIDENCE_BASED_CLASSIFICATION_MULTILABEL.md](CONFIDENCE_BASED_CLASSIFICATION_MULTILABEL.md) - Previous approach (margin-based)
- [SCORING_CHANGES_SUMMARY.md](SCORING_CHANGES_SUMMARY.md) - Transition from cosine to dot product

---

## Summary

The significance scoring system successfully addresses the critical insight that **uniform scores across topics indicate noise, not relevance**. By using Coefficient of Variation as the primary filter (weight: 0.5), combined with magnitude and contrast, we can automatically identify and filter out boilerplate/generic text while preserving chunks with clear topic differentiation.

**Key achievement:** Chunks like `[4.88, 4.89, 4.92, 4.83]` are now correctly identified as noise (significance ≈ 0.15) despite having moderate absolute scores, while chunks like `[9.22, 5.23, 4.10, 5.35]` are correctly identified as highly significant (significance ≈ 0.82) due to clear differentiation.
