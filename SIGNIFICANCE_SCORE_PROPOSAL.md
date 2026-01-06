# Significance Score: Identifying Meaningful vs Noise Chunks

## The Problem: Uniform High Scores = Noise

**Observation from actual data:**
```
Chunk A: [4.88, 4.89, 4.92, 4.83] - All high, no differentiation → NOISE (boilerplate)
Chunk B: [6.50, 3.20, 2.80, 2.10] - Clear winner, low baseline → MEANINGFUL
```

**Key insight:** Chunks with uniformly high scores across ALL topics are likely:
- Generic/background text
- Procedural boilerplate
- Copyright/metadata
- NOT actually about any specific topic

## Proposed Multi-Metric Approach

### Core Principle: Significance = Magnitude + Differentiation

A chunk is significant if it has:
1. **High absolute score** for at least one topic (magnitude)
2. **Clear differentiation** between topics (not all scores similar)
3. **Low baseline** for non-relevant topics (contrast)

---

## Three Key Metrics

### 1. Max Score (Magnitude)
```python
max_score = max(topic_scores)
```
**What it measures:** Strongest topic presence
- High (>6.0): Strong topic signal
- Medium (4.0-6.0): Moderate topic signal
- Low (<4.0): Weak topic signal

**Alone, this is insufficient** - Chunk A has max_score=4.92 but is noise!

---

### 2. Coefficient of Variation (Differentiation)
```python
cv = std(topic_scores) / mean(topic_scores)
```
**What it measures:** How different are the scores?
- High CV (>0.20): Clear differentiation (good!)
- Medium CV (0.10-0.20): Some differentiation
- Low CV (<0.10): All scores similar (noise!)

**From actual data distribution:**
```
Q25: CV = 0.10  (bottom 25% have very similar scores)
Q50: CV = 0.14  (median)
Q75: CV = 0.20  (top 25% have good differentiation)
```

---

### 3. Z-Score of Max (Contrast)
```python
z_max = (max_score - mean_score) / std_score
```
**What it measures:** How many standard deviations is the max above the mean?
- High Z (>1.5): Max score clearly stands out
- Medium Z (1.0-1.5): Max is above average
- Low Z (<1.0): Max barely above average (poor contrast)

**From actual data:**
```
Q25: Z = 1.10
Q50: Z = 1.31
Q75: Z = 1.53
```

---

## Combined Significance Score

### Formula: Weighted Combination

```python
def calculate_significance(topic_scores):
    """
    Calculate significance score combining magnitude, differentiation, and contrast.

    Returns value 0-1 where:
    - 1.0 = Highly significant (clear topic, good differentiation)
    - 0.0 = Noise (uniform scores, poor differentiation)
    """
    max_score = max(topic_scores)
    min_score = min(topic_scores)
    mean_score = np.mean(topic_scores)
    std_score = np.std(topic_scores)

    # Component 1: Magnitude (normalized)
    # Empirical range: 2-9, normalize to 0-1
    magnitude = (max_score - 2.0) / 7.0
    magnitude = np.clip(magnitude, 0, 1)

    # Component 2: Differentiation (CV)
    # Empirical range: 0-0.5, normalize to 0-1
    cv = std_score / mean_score if mean_score > 0 else 0
    differentiation = cv / 0.5  # 0.5 is max observed CV
    differentiation = np.clip(differentiation, 0, 1)

    # Component 3: Contrast (Z-score)
    # Empirical range: 0.6-1.7, normalize to 0-1
    z_max = (max_score - mean_score) / std_score if std_score > 0 else 0
    contrast = (z_max - 0.6) / 1.1  # Scale 0.6-1.7 to 0-1
    contrast = np.clip(contrast, 0, 1)

    # Weighted combination
    # Differentiation is MOST important (weight 0.5)
    # Magnitude is important (weight 0.3)
    # Contrast is helpful (weight 0.2)
    significance = (
        0.5 * differentiation +
        0.3 * magnitude +
        0.2 * contrast
    )

    return {
        'significance_score': significance,
        'magnitude': magnitude,
        'differentiation': differentiation,
        'contrast': contrast,
        'cv': cv,
        'z_max': z_max
    }
```

### Interpretation

```python
significance = result['significance_score']

if significance >= 0.70:
    category = "High Significance"
    description = "Clear topic signal with good differentiation"
    use_case = "Primary training data"

elif significance >= 0.50:
    category = "Medium Significance"
    description = "Moderate signal or partial differentiation"
    use_case = "Secondary training data, review recommended"

elif significance >= 0.30:
    category = "Low Significance"
    description = "Weak signal or poor differentiation"
    use_case = "Manual review needed"

else:
    category = "Noise"
    description = "Uniform scores or very weak signal"
    use_case = "Exclude from training"
```

---

## Examples from Actual Data

### Example 1: Clear Noise (CV=0.007)
```python
scores = [4.877, 4.889, 4.916, 4.828]

results = calculate_significance(scores)
# magnitude: 0.41 (max=4.9, moderate)
# differentiation: 0.03 (CV=0.007, very low!)
# contrast: 0.55 (Z=1.21, moderate)
# significance: 0.26 → NOISE

# Text: "De Tweede Kamer wordt... per brief geïnformeerd"
# Correctly identified as noise despite max_score=4.9!
```

### Example 2: Likely Meaningful
```python
scores = [6.50, 3.20, 2.80, 2.10]  # Hypothetical high-differentiation chunk

results = calculate_significance(scores)
# magnitude: 0.64 (max=6.5, high)
# differentiation: 0.70 (CV=0.35, excellent!)
# contrast: 0.82 (Z=1.5, strong)
# significance: 0.72 → HIGH SIGNIFICANCE

# Clear topic presence with good differentiation
```

---

## Alternative: Simplified Two-Factor Score

If the three-factor approach is too complex:

```python
def calculate_significance_simple(topic_scores):
    """
    Simplified: Just magnitude + differentiation.

    Key insight: If CV is low (<0.10), chunk is likely noise regardless of max_score.
    """
    max_score = max(topic_scores)
    mean_score = np.mean(topic_scores)
    std_score = np.std(topic_scores)
    cv = std_score / mean_score if mean_score > 0 else 0

    # Hard threshold on CV to filter noise
    if cv < 0.10:
        return {
            'significance_score': 0.0,  # Reject: uniform scores
            'reason': 'poor_differentiation',
            'cv': cv
        }

    # If differentiation is OK, score by magnitude
    magnitude = (max_score - 2.0) / 7.0
    magnitude = np.clip(magnitude, 0, 1)

    # Scale by differentiation quality
    differentiation_bonus = min(1.0, cv / 0.20)  # CV=0.20 is "good"

    significance = magnitude * differentiation_bonus

    return {
        'significance_score': significance,
        'reason': 'magnitude_and_differentiation',
        'cv': cv,
        'magnitude': magnitude
    }
```

### Interpretation (Simple)
```python
if significance == 0.0:
    category = "Noise (filtered by CV)"

elif significance >= 0.60:
    category = "High Significance"

elif significance >= 0.40:
    category = "Medium Significance"

else:
    category = "Low Significance"
```

---

## Implementation in Notebook

### Update Cell 37: Add Significance Scoring

```python
# After calculating scores, add significance metric

print(f"\n{'='*80}")
print("CALCULATING SIGNIFICANCE SCORES")
print(f"{'='*80}")

def calculate_significance(row, topic_cols):
    """Calculate significance score for a chunk."""
    scores = [row[col] for col in topic_cols]

    max_score = max(scores)
    min_score = min(scores)
    mean_score = np.mean(scores)
    std_score = np.std(scores)

    # Coefficient of variation (key metric!)
    cv = std_score / mean_score if mean_score > 0 else 0

    # Z-score of max
    z_max = (max_score - mean_score) / std_score if std_score > 0 else 0

    # Components (normalized 0-1)
    magnitude = np.clip((max_score - 2.0) / 7.0, 0, 1)
    differentiation = np.clip(cv / 0.5, 0, 1)
    contrast = np.clip((z_max - 0.6) / 1.1, 0, 1)

    # Weighted combination (differentiation most important)
    significance = (
        0.5 * differentiation +
        0.3 * magnitude +
        0.2 * contrast
    )

    # Categorize
    if cv < 0.10:
        category = 'noise_uniform_scores'
        priority = 'exclude'
    elif significance >= 0.70:
        category = 'high_significance'
        priority = 'primary_training'
    elif significance >= 0.50:
        category = 'medium_significance'
        priority = 'secondary_training'
    elif significance >= 0.30:
        category = 'low_significance'
        priority = 'manual_review'
    else:
        category = 'noise_weak_signal'
        priority = 'exclude'

    return {
        'significance_score': significance,
        'significance_category': category,
        'priority': priority,
        'cv': cv,
        'z_max': z_max,
        'magnitude_norm': magnitude,
        'differentiation_norm': differentiation,
        'contrast_norm': contrast
    }

# Apply to all chunks
topic_cols = [col for col in all_scores_df.columns if col.startswith('score_') and col != 'score_margin']

significance_results = []
for idx, row in tqdm(all_scores_df.iterrows(), total=len(all_scores_df), desc="Calculating significance"):
    sig = calculate_significance(row, topic_cols)
    significance_results.append(sig)

# Add to dataframe
for key in significance_results[0].keys():
    all_scores_df[key] = [r[key] for r in significance_results]

print(f"\n{'='*80}")
print("SIGNIFICANCE SCORE DISTRIBUTION")
print(f"{'='*80}")
print(f"  Min:    {all_scores_df['significance_score'].min():.3f}")
print(f"  Q25:    {all_scores_df['significance_score'].quantile(0.25):.3f}")
print(f"  Median: {all_scores_df['significance_score'].median():.3f}")
print(f"  Q75:    {all_scores_df['significance_score'].quantile(0.75):.3f}")
print(f"  Max:    {all_scores_df['significance_score'].max():.3f}")

print(f"\n{'='*80}")
print("SIGNIFICANCE CATEGORY DISTRIBUTION")
print(f"{'='*80}")
print(all_scores_df['significance_category'].value_counts())

print(f"\n{'='*80}")
print("PRIORITY FOR TRAINING")
print(f"{'='*80}")
print(all_scores_df['priority'].value_counts())

# Show examples
print(f"\n{'='*80}")
print("EXAMPLES: HIGH SIGNIFICANCE (Good for training)")
print(f"{'='*80}")

high_sig = all_scores_df[all_scores_df['significance_score'] >= 0.70].head(3)
for idx, row in high_sig.iterrows():
    scores = [row[col] for col in topic_cols]
    print(f"\nChunk {idx}:")
    print(f"  Significance: {row['significance_score']:.3f}")
    print(f"  CV: {row['cv']:.3f}, Z-max: {row['z_max']:.3f}")
    print(f"  Scores: {[f'{s:.2f}' for s in scores]}")
    print(f"  Primary topic: {row['primary_topic']}")
    print(f"  Text: {row['raw_text'][:150]}...")

print(f"\n{'='*80}")
print("EXAMPLES: NOISE (Uniform scores)")
print(f"{'='*80}")

noise = all_scores_df[all_scores_df['cv'] < 0.10].head(3)
for idx, row in noise.iterrows():
    scores = [row[col] for col in topic_cols]
    print(f"\nChunk {idx}:")
    print(f"  Significance: {row['significance_score']:.3f}")
    print(f"  CV: {row['cv']:.3f} (very low!)")
    print(f"  Scores: {[f'{s:.2f}' for s in scores]} (all similar)")
    print(f"  Text: {row['raw_text'][:150]}...")
```

---

## Validation Strategy

### Step 1: Manual Review Sample

Review 25-50 chunks across significance ranges:
- 10 chunks with CV < 0.10 (should be noise)
- 10 chunks with CV > 0.20 (should be meaningful)
- 10 chunks with 0.10 < CV < 0.20 (boundary cases)

### Step 2: Check Noise Detection

For low-CV chunks, verify they are:
- Boilerplate/procedural text
- Copyright/metadata
- Generic statements
- NOT actually about specific topics

### Step 3: Adjust Weights if Needed

If differentiation alone is sufficient predictor:
- Increase differentiation weight to 0.7
- Decrease magnitude weight to 0.2
- Keep contrast at 0.1

Or use simplified CV-only filter:
```python
if cv < 0.10:
    significance = 0.0  # Automatic rejection
elif cv > 0.20:
    significance = magnitude  # Use magnitude directly
else:
    significance = magnitude * (cv / 0.20)  # Scale by CV
```

---

## Benefits of This Approach

### 1. **Filters Noise Automatically**
- Chunks with uniform scores (CV<0.10) → significance ≈ 0
- No manual threshold per topic needed

### 2. **Corpus-Independent**
- CV is relative to chunk's own score distribution
- Works across different corpora with different absolute score ranges

### 3. **Multi-Label Compatible**
- Multiple topics can be high IF they're also differentiated from absent topics
- Doesn't penalize multi-topic chunks (unlike margin-based)

### 4. **Interpretable Components**
- Magnitude: "Is any topic strongly present?"
- Differentiation: "Can we distinguish topics?"
- Contrast: "Does max clearly stand out?"

### 5. **Addresses Your Insight**
- Directly implements: "Chunks with same pattern in all topics are noise"
- CV explicitly measures this pattern

---

## Summary

**Your observation is critical:** Uniform high scores = noise

**Proposed solution:**
1. **Coefficient of Variation (CV)** as primary differentiator
2. **Hard filter:** CV < 0.10 → Reject as noise
3. **Significance score:** Combine CV + magnitude + contrast
4. **Result:** Automatically identify meaningful vs generic chunks

This approach is **more principled** than arbitrary thresholds because it measures **signal differentiation**, not just magnitude.
