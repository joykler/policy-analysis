# METHODOLOGY: Multi-Label Classifier Evaluation Protocol (Dot Product Edition)
**Version:** 2.0 (Dot Product Adaptation)
**Date:** 2025-12-05
**Purpose:** Reusable step-by-step methodology for evaluating multi-label text classifiers with unnormalized dot product scoring

---

## CHANGELOG FROM V1.0

**Major Changes for Dot Product Scoring:**
1. **Score ranges:** Updated from 0-1 cosine (0.07-0.65 compressed) to 0-200+ dot product
2. **Thresholds:** All hardcoded thresholds replaced with percentile-based adaptive thresholds
3. **Quality tiers:** Updated from fixed 0-2 rescaled ranges to dynamic percentile-based classification
4. **Normalization:** Removed assumptions about normalized embeddings
5. **Distribution analysis:** Added checks for score distribution to ensure proper scoring system

---

## OVERVIEW

This methodology evaluates how well automated classifiers (neural models, dictionary-based, etc.) match human semantic judgment on multi-label text classification tasks.

**Key Principles:**
1. **Corpus-agnostic:** Works with any text corpus and topic framework
2. **Multi-label first:** Evaluates pattern matching, not just top-1 accuracy
3. **Token-efficient:** Designed for LLM evaluation with output limits
4. **Quality-stratified:** Samples across content quality spectrum
5. **⭐ Score-agnostic:** Works with any scoring system (cosine, dot product, model logits)

**Input Requirements:**
1. Dataset with predictions from 1+ classifiers
2. Topic framework document (defines what each topic means)
3. Quality scores (optional but recommended for stratification)

**Output:**
- Semantic ground truth ratings for sample
- Per-topic precision/recall/F1 for each classifier
- Ranking correlation analysis
- Adaptive threshold recommendations

---

## PREREQUISITES

### Required Input Files

**1. Topic Framework Document** (`TOPIC_FRAMEWORK.md`)
```markdown
# Topic Framework: [Project Name]

## Topic 1: [Name]
**Definition:** [What this topic covers]
**Key indicators:** [Words, concepts, themes]
**Examples:** [Sample texts]

## Topic 2: [Name]
...
```

**2. Predictions Dataset** (CSV format)

Minimum required columns:
```
chunk_id,text,classifier1_topic1_score,classifier1_topic2_score,...,classifier2_topic1_score,...
```

Example with dot product scores:
```csv
chunk_id,raw_text,bertje_topic1,bertje_topic2,bertje_topic3,score_topic1,score_topic2,score_topic3,max_score,score_margin
abc123,"text here...",87.5,42.3,13.2,125.4,67.8,22.1,125.4,57.6
def456,"other text...",145.2,98.7,76.3,156.3,112.4,88.9,156.3,43.9
```

**Key Differences from V1.0:**
- Score values are now in wider ranges (e.g., 0-200 instead of 0-1)
- Include `max_score` and `score_margin` for confidence assessment
- No rescaled columns needed

**3. Quality Scores (Optional)**

If available, include a column indicating content quality or confidence:
```
chunk_id,text,max_score,score_margin,classifier1_scores...
```

This enables quality-stratified sampling.

---

## STEP-BY-STEP PROTOCOL

### PHASE 0: SETUP AND SAMPLING

**Goal:** Create stratified sample for evaluation (minimize tokens, maximize coverage)

**Recommended Sample Size:**
- Minimum: 25 chunks (5 per quality tier)
- Recommended: 50 chunks (10 per quality tier)
- Maximum for single session: 100 chunks (requires multiple files)

---

#### STEP 0.1: Load and Inspect Data

```python
import pandas as pd
import numpy as np

# Load predictions
df = pd.read_csv('predictions.csv')

# Identify columns
text_column = 'raw_text'  # or 'text', 'content', etc.
id_column = 'chunk_id'    # or 'id', 'doc_id', etc.

# List all classifiers and topics
classifiers = ['bertje', 'score']  # Adjust based on your data
topics = ['topic1', 'topic2', 'topic3', 'topic4']  # From framework

# Check data
print(f"Total chunks: {len(df)}")
print(f"Classifiers: {classifiers}")
print(f"Topics: {topics}")

# ⭐ NEW: Check score distribution to verify scoring system
for classifier in classifiers:
    score_cols = [f'{classifier}_{topic}' for topic in topics]
    if all(col in df.columns for col in score_cols):
        scores = df[score_cols].values.flatten()
        print(f"\n{classifier} score distribution:")
        print(f"  Min:    {scores.min():.2f}")
        print(f"  Q25:    {np.percentile(scores, 25):.2f}")
        print(f"  Median: {np.percentile(scores, 50):.2f}")
        print(f"  Q75:    {np.percentile(scores, 75):.2f}")
        print(f"  Max:    {scores.max():.2f}")
        print(f"  Std:    {scores.std():.2f}")

        # Sanity check: if max < 2.0, likely still using old cosine/rescaled system
        if scores.max() < 2.0:
            print(f"  ⚠️  WARNING: Scores seem compressed (max < 2.0)")
            print(f"      This might indicate old cosine similarity system")
            print(f"      Expected dot product range: 0-200+")
```

---

#### STEP 0.2: Quality Stratification (Adaptive)

**⭐ NEW: Use percentile-based tiers instead of hardcoded thresholds**

```python
# Calculate quality score (use max score across topics if not provided)
if 'max_score' not in df.columns:
    score_cols = [f'score_{topic}' for topic in topics]
    df['max_score'] = df[score_cols].max(axis=1)

# ⭐ NEW: Calculate percentile-based quality thresholds
p90 = df['max_score'].quantile(0.90)
p75 = df['max_score'].quantile(0.75)
p50 = df['max_score'].quantile(0.50)
p25 = df['max_score'].quantile(0.25)
p10 = df['max_score'].quantile(0.10)

print(f"\nQuality score percentiles:")
print(f"  P90 (top 10%):    {p90:.2f}")
print(f"  P75 (top 25%):    {p75:.2f}")
print(f"  P50 (median):     {p50:.2f}")
print(f"  P25 (bottom 75%): {p25:.2f}")
print(f"  P10 (bottom 90%): {p10:.2f}")

# Define quality tiers using percentiles
def assign_tier(score):
    """Percentile-based tier assignment (adapts to score distribution)"""
    if score >= p90:
        return 'Core'      # Top 10%
    elif score >= p75:
        return 'Moderate'  # 75-90th percentile
    elif score >= p50:
        return 'Weak'      # 50-75th percentile
    elif score >= p25:
        return 'Context'   # 25-50th percentile
    else:
        return 'Noise'     # Bottom 25%

df['tier'] = df['max_score'].apply(assign_tier)

print(f"\nTier distribution:")
print(df['tier'].value_counts().sort_index())

# Stratified sample: n per tier
n_per_tier = 5  # Or 10 for 50-chunk sample
sample = df.groupby('tier', group_keys=False).apply(
    lambda x: x.sample(min(n_per_tier, len(x)), random_state=42)
)

print(f"\nSample tier distribution:")
print(sample['tier'].value_counts().sort_index())
```

**Key Changes from V1.0:**
- ❌ OLD: Fixed thresholds (1.5, 1.0, 0.5, 0.25, 0.0) for rescaled 0-2 range
- ✅ NEW: Percentile-based thresholds (P90, P75, P50, P25) adapt to any range
- Works with cosine (0-1), rescaled (0-2), AND dot product (0-200+)

---

#### STEP 0.3: Save Sample with Metadata

```python
# ⭐ NEW: Include scoring metadata in sample
sample_metadata = {
    'scoring_system': 'dot_product',  # or 'cosine', 'rescaled'
    'score_range': {
        'min': float(sample['max_score'].min()),
        'max': float(sample['max_score'].max()),
        'median': float(sample['max_score'].median())
    },
    'percentile_thresholds': {
        'p90': float(p90),
        'p75': float(p75),
        'p50': float(p50),
        'p25': float(p25),
        'p10': float(p10)
    },
    'topics': topics,
    'classifiers': classifiers,
    'sample_size': len(sample),
    'date': pd.Timestamp.now().isoformat()
}

# Save sample
sample.to_csv('evaluation_sample.csv', index=False)

# Save metadata
import json
with open('evaluation_sample_metadata.json', 'w') as f:
    json.dump(sample_metadata, f, indent=2)

print(f"\n✓ Saved evaluation_sample.csv ({len(sample)} chunks)")
print(f"✓ Saved evaluation_sample_metadata.json")
```

**Output Example:**
```
✓ Saved evaluation_sample.csv (25 chunks)
✓ Saved evaluation_sample_metadata.json

Sample tier distribution:
Core        5
Moderate    5
Weak        5
Context     5
Noise       5
```

---

### PHASE 1: SEMANTIC EVALUATION (Ground Truth)

**Goal:** Rate each chunk on ALL topics independently (0-3 scale) WITHOUT looking at classifier predictions

**⚠️ NO CHANGES from V1.0 - semantic rating is score-independent!**

The semantic evaluation process is identical regardless of scoring system:
- Still use 0-3 rating scale (Absent/Weak/Moderate/Strong)
- Still rate all topics independently
- Still don't look at classifier predictions
- Still batch into 10-chunk files

See V1.0 methodology sections 1.1-1.5 for complete instructions.

**Quick Reference:**

| Rating | Label | Definition | When to Use |
|--------|-------|------------|-------------|
| **0** | Absent | Topic not discussed | No mention or tangential only |
| **1** | Weak | Minor/contextual presence | Mentioned but not developed |
| **2** | Moderate | Clear secondary theme | Discussed but not central |
| **3** | Strong | Central/primary theme | Core focus of text |

---

### PHASE 2: MULTI-LABEL PATTERN EVALUATION

**Goal:** Compare each classifier's score patterns to semantic rating patterns

**⭐ MAJOR CHANGES: Adaptive threshold calculation**

---

#### STEP 2.1: Per-Classifier Threshold Analysis (Adaptive)

**For each classifier, determine optimal thresholds based on actual score distribution.**

**File:** `STEP2_[CLASSIFIER]_MULTILABEL_EVALUATION.md`

```markdown
# STEP 2: [CLASSIFIER NAME] Multi-Label Evaluation

## Score Distribution Analysis

### Step 1: Understand Score Range

**Score statistics across all [N] evaluation chunks:**

| Statistic | Value | Notes |
|-----------|-------|-------|
| Minimum | X.XX | Lowest score observed |
| Q25 | X.XX | 25th percentile |
| Median | X.XX | 50th percentile |
| Q75 | X.XX | 75th percentile |
| Maximum | X.XX | Highest score observed |
| Std Dev | X.XX | Spread of scores |
| Range | X.XX | Max - Min |

⭐ **Score range type detected:** [0-1 cosine / 0-2 rescaled / 0-200+ dot product]

### Step 2: Calculate Percentile-Based Test Thresholds

Instead of testing fixed thresholds (0.3, 0.4, 0.5...), test percentile-based thresholds:

```python
# Generate candidate thresholds from score distribution
scores_flat = df[[f'{classifier}_{topic}' for topic in topics]].values.flatten()

candidate_thresholds = {
    'p90': np.percentile(scores_flat, 90),  # Top 10%
    'p80': np.percentile(scores_flat, 80),  # Top 20%
    'p75': np.percentile(scores_flat, 75),  # Top 25%
    'p70': np.percentile(scores_flat, 70),  # Top 30%
    'p60': np.percentile(scores_flat, 60),  # Top 40%
    'p50': np.percentile(scores_flat, 50),  # Median
    'p40': np.percentile(scores_flat, 40),  # Top 60%
    'p30': np.percentile(scores_flat, 30),  # Top 70%
}

print("Candidate thresholds (percentile-based):")
for name, value in candidate_thresholds.items():
    print(f"  {name}: {value:.2f}")
```

**Example output:**
```
Candidate thresholds (percentile-based):
  p90: 142.56
  p80: 118.34
  p75: 98.23
  p70: 87.45
  p60: 67.89
  p50: 56.78
  p40: 45.12
  p30: 34.56
```

## Threshold Testing Results

For each percentile threshold, calculate:
- True Positives: Predicted present (score ≥ thresh) AND semantic ≥2
- False Positives: Predicted present BUT semantic <2
- False Negatives: Predicted absent BUT semantic ≥2
- True Negatives: Predicted absent AND semantic <2

| Threshold | Value | TP | FP | FN | TN | Precision | Recall | F1 |
|-----------|-------|----|----|----|----|-----------|--------|-----|
| P90 | XXX.X | X | X | X | X | 0.XX | 0.XX | 0.XX |
| P80 | XXX.X | X | X | X | X | 0.XX | 0.XX | 0.XX |
| **P75** | **XXX.X** | **X** | **X** | **X** | **X** | **0.XX** | **0.XX** | **0.XX** |
| P70 | XXX.X | X | X | X | X | 0.XX | 0.XX | 0.XX |
| P60 | XXX.X | X | X | X | X | 0.XX | 0.XX | 0.XX |
| P50 | XXX.X | X | X | X | X | 0.XX | 0.XX | 0.XX |
| P40 | XXX.X | X | X | X | X | 0.XX | 0.XX | 0.XX |
| P30 | XXX.X | X | X | X | X | 0.XX | 0.XX | 0.XX |

**Optimal global threshold:** P[XX] = XXX.X (highest F1)

**Observations:**
- Higher thresholds (P80-P90): High precision, low recall (misses weak signals)
- Lower thresholds (P30-P40): High recall, low precision (too many false positives)
- **Sweet spot:** Around P[60-75] typically balances precision and recall
```

**Key Changes from V1.0:**
- ❌ OLD: Test fixed thresholds [0.3, 0.4, 0.5, 0.6, 0.7]
- ✅ NEW: Test percentile-based thresholds [P30, P40, P50, P60, P70, P75, P80, P90]
- Thresholds adapt to actual score distribution
- Works with any scoring system

---

#### STEP 2.2: Adaptive Threshold Analysis (Quality-Stratified)

```markdown
## Adaptive Threshold Analysis

### Hypothesis
Content quality affects optimal threshold:
- High-quality content (P90+): Can use stricter threshold (reduce FP)
- Medium-quality content (P50-P90): Use balanced threshold
- Low-quality content (<P50): May need lenient threshold (capture weak signals)

### Calculate Tier-Specific Thresholds

For each quality tier, find optimal threshold:

```python
tier_thresholds = {}

for tier in ['Core', 'Moderate', 'Weak', 'Context', 'Noise']:
    tier_chunks = sample[sample['tier'] == tier]

    if len(tier_chunks) == 0:
        continue

    # Get scores for this tier
    tier_scores = []
    for _, row in tier_chunks.iterrows():
        for topic in topics:
            tier_scores.append(row[f'{classifier}_{topic}'])

    # Calculate percentiles for this tier
    tier_p90 = np.percentile(tier_scores, 90)
    tier_p75 = np.percentile(tier_scores, 75)
    tier_p60 = np.percentile(tier_scores, 60)
    tier_p50 = np.percentile(tier_scores, 50)

    # Test thresholds for this tier
    best_f1 = 0
    best_threshold = tier_p60

    for threshold in [tier_p90, tier_p75, tier_p60, tier_p50]:
        # Calculate F1 for this tier+threshold combo
        # [implementation details]

        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold

    tier_thresholds[tier] = {
        'threshold': best_threshold,
        'f1': best_f1,
        'percentile': find_percentile(best_threshold, tier_scores)
    }

print("Tier-specific optimal thresholds:")
for tier, info in tier_thresholds.items():
    print(f"  {tier}: {info['threshold']:.2f} (P{info['percentile']:.0f}, F1={info['f1']:.2f})")
```

**Example output:**
```
Tier-specific optimal thresholds:
  Core:     156.3 (P75, F1=0.87)
  Moderate: 112.4 (P70, F1=0.82)
  Weak:     78.9 (P65, F1=0.76)
  Context:  45.6 (P60, F1=0.68)
  Noise:    23.1 (P50, F1=0.52)
```

### Adaptive vs Fixed Threshold Comparison

| Chunk | Tier | Fixed (P60) | Adaptive (Tier-specific) | Semantic Present | Better Method |
|-------|------|-------------|--------------------------|------------------|---------------|
| 1 | Core | [Topics] | [Topics] | [Topics] | [Adaptive/Fixed/Tie] |
| 2 | Moderate | [Topics] | [Topics] | [Topics] | [Adaptive/Fixed/Tie] |
| ... | ... | ... | ... | ... | ... |

**Results:**
- Fixed threshold (P60): X/N (XX%) perfect matches
- Adaptive threshold: X/N (XX%) perfect matches
- **Improvement:** +X percentage points

**Conclusion:**
- ✅ Use adaptive thresholds if improvement ≥5%
- ⚠️ Use fixed threshold if improvement <5% (simpler system)
```

**Key Changes from V1.0:**
- ❌ OLD: Fixed tier thresholds (0.65-0.75, 0.50, 0.30-0.40)
- ✅ NEW: Calculate optimal threshold per tier from actual data
- More robust across different scoring systems

---

#### STEP 2.3: Per-Topic Multi-Label Metrics (Unchanged Structure)

The confusion matrix and metrics calculation remains the same as V1.0:

```markdown
## Per-Topic Performance

Using optimal thresholds (adaptive):

### [Topic 1 Name]

**Confusion Matrix:**

|              | Predicted Present | Predicted Absent |
|--------------|------------------|------------------|
| **Semantic Present (≥2)** | TP: X | FN: X |
| **Semantic Absent (<2)** | FP: X | TN: X |

**Metrics:**
- Precision: TP/(TP+FP) = X/Y = 0.XX
- Recall: TP/(TP+FN) = X/Y = 0.XX
- F1: 2×(P×R)/(P+R) = 0.XX

**Error Analysis:**
- **False Positives (predicted but not present):**
  - Chunk X: Score XXX.X (threshold XXX.X), Semantic rating 0-1
  - [Brief explanation - why did classifier predict this?]

- **False Negatives (present but not predicted):**
  - Chunk Y: Score XXX.X (threshold XXX.X), Semantic rating 2-3
  - [Brief explanation - why did classifier miss this?]

**Observations:** [Pattern in errors?]
```

**⭐ NEW: Include actual score values in error analysis to help diagnose threshold issues**

---

#### STEP 2.4: Ranking Correlation Analysis (Minor Updates)

```markdown
## Ranking Correlation Analysis

### Methodology

For each chunk, calculate Spearman correlation between:
- Semantic ratings [0, 1, 2, 3] for all topics
- Classifier scores [continuous, any range] for all topics

**Spearman correlation** measures if relative ranking matches (not absolute values).
✅ **Score-independent:** Works with any scoring system (0-1, 0-2, 0-200+)

### Results by Quality Tier

| Tier | Mean Correlation | Std Dev | N Chunks | Score Range |
|------|-----------------|---------|----------|-------------|
| Core (P90+) | 0.XX | 0.XX | X | XXX-XXX |
| Moderate (P75-P90) | 0.XX | 0.XX | X | XXX-XXX |
| Weak (P50-P75) | 0.XX | 0.XX | X | XXX-XXX |
| Context (P25-P50) | 0.XX | 0.XX | X | XXX-XXX |
| Noise (<P25) | 0.XX | 0.XX | X | XXX-XXX |
| **Overall** | **0.XX** | **0.XX** | **N** | **XXX-XXX** |

⭐ **NEW: Include score range** to show distribution by tier

### Example Cases

**High Correlation (>0.90):**
- Chunk X: Semantic [3,2,0,0], Scores [145.2,98.7,12.3,8.5] → Corr=0.95 ✅
  - Rankings match perfectly: Both have Topic1 > Topic2 > Topic3 > Topic4

**Medium Correlation (0.70-0.90):**
- Chunk Y: Semantic [2,2,1,0], Scores [89.4,87.1,42.3,15.8] → Corr=0.80 ⚠️
  - Close tie between top 2 topics (scores 89.4 vs 87.1)
  - Semantic also has tie (both rated 2)

**Low Correlation (<0.70):**
- Chunk Z: Semantic [0,1,0,3], Scores [67.8,76.2,45.1,52.3] → Corr=0.40 ❌
  - **Issue:** Predicted Topic2 highest (76.2) but semantic is Topic4 (3)
  - Ranking completely inverted

### Correlation as Confidence Metric

| Correlation | Confidence Level | Recommendation | Expected Accuracy |
|-------------|------------------|----------------|-------------------|
| ≥0.85 | High | Auto-approve | 90-95% |
| 0.70-0.85 | Medium | Batch review | 75-85% |
| 0.50-0.70 | Low | Individual review | 50-70% |
| <0.50 | Very Low | Likely incorrect | <50% |

✅ **Score-independent:** These correlation bands work regardless of absolute score values
```

**Key Changes from V1.0:**
- ✅ Added score range column to show distribution
- ✅ Emphasized that correlation is score-independent
- ✅ Examples now show wider score ranges (dot product)

---

#### STEP 2.5: Classifier Summary (Updated Recommendations)

```markdown
## [CLASSIFIER NAME] Summary

### Score Distribution Profile

- **Scoring system:** [Dot product / Cosine / Rescaled]
- **Score range:** [Min] to [Max]
- **Spread:** Std dev = [XX.X]
- **Quality tiers well-separated:** [Yes/No - can distinguish quality levels?]

### Strengths
- ✅ [Topic X]: Excellent performance (F1 0.XX)
- ✅ High-quality content: Mean correlation 0.XX
- ✅ Wide score range: Good discrimination (std = XX.X)
- ✅ [Other strength]

### Weaknesses
- ❌ [Topic Y]: Poor performance (F1 0.XX)
- ❌ Low-quality content: Mean correlation 0.XX
- ❌ [Compressed scores in tier Z]: Limited discrimination
- ❌ [Other weakness]

### Recommended Configuration

**Threshold Strategy:** [Fixed/Adaptive]

**If Fixed:**
```python
THRESHOLD = XXX.X  # P[XX] percentile
```

**If Adaptive:**
```python
THRESHOLDS = {
    'Core': XXX.X,      # P[XX] for high-quality
    'Moderate': XXX.X,  # P[XX] for medium-quality
    'Weak': XXX.X,      # P[XX] for low-quality
    'Context': XXX.X,   # P[XX] for very low-quality
    'Noise': XXX.X      # P[XX] for noise
}

def get_threshold(quality_score, percentile_map):
    \"\"\"Get appropriate threshold based on chunk quality\"\"\"
    if quality_score >= P90:
        return THRESHOLDS['Core']
    elif quality_score >= P75:
        return THRESHOLDS['Moderate']
    elif quality_score >= P50:
        return THRESHOLDS['Weak']
    elif quality_score >= P25:
        return THRESHOLDS['Context']
    else:
        return THRESHOLDS['Noise']
```

**Confidence calibration:** Use correlation >0.XX for high confidence

**Expected performance:** Multi-label F1 = 0.XX

### Priority Improvements
1. [Specific issue] → [Recommended fix]
2. If using old cosine system → Migrate to dot product for better discrimination
3. If scores compressed → Check embedding normalization
```

**Key Changes from V1.0:**
- ✅ Added score distribution profile section
- ✅ Threshold recommendations now show actual values (not just 0.X)
- ✅ Include percentile information for reproducibility
- ✅ Add diagnostic for compressed scores

---

### PHASE 3: COMPARATIVE ANALYSIS (Minimal Changes)

**Goal:** Compare classifiers head-to-head

The comparative analysis structure is mostly unchanged from V1.0, with minor additions:

```markdown
# STEP 3: Comparative Analysis

## Score Distribution Comparison

⭐ **NEW: Compare scoring systems directly**

| Classifier | Scoring System | Score Range | Std Dev | Separation Quality |
|------------|----------------|-------------|---------|-------------------|
| [Name 1] | [Type] | [Min-Max] | [XX.X] | [Good/Fair/Poor] |
| [Name 2] | [Type] | [Min-Max] | [XX.X] | [Good/Fair/Poor] |

**Separation quality:** Can the scoring system distinguish between quality tiers?
- Good: P90-P10 > 3× std dev
- Fair: P90-P10 > 2× std dev
- Poor: P90-P10 < 2× std dev

## Overall Performance Comparison

[Rest of section unchanged from V1.0]
```

---

### PHASE 4: FINAL RECOMMENDATIONS (Updated for Dot Product)

```markdown
# STEP 4: Final Recommendations and Deployment Guide

## Executive Summary

### Performance Summary

| Classifier | Scoring System | Multi-Label F1 | Ranking Correlation | Recommended Use |
|------------|----------------|----------------|---------------------|-----------------|
| [Name 1] | [Dot/Cosine] | 0.XX | 0.XX | [Primary/Secondary/Ensemble] |
| [Name 2] | [Dot/Cosine] | 0.XX | 0.XX | [Primary/Secondary/Ensemble] |

### Key Findings

1. **Scoring system impact:** [How does dot product vs cosine affect performance?]
2. **Multi-label vs single-label:** [Comparison]
3. **Quality stratification:** [Performance variation]
4. **Optimal thresholds:** [Percentile-based results]

---

## Production Configuration

### Recommended System Architecture

**Primary Classifier:** [Name]
- Multi-label F1: 0.XX
- Scoring system: [Dot product / Cosine]
- Configuration: [Adaptive/fixed percentile thresholds]

### Threshold Configuration (Percentile-Based)

⭐ **NEW: Store thresholds as percentiles for reproducibility**

```python
# Configuration
PERCENTILE_THRESHOLDS = {
    'Core': 'P75',      # Top 25% for high-quality content
    'Moderate': 'P70',  # Top 30% for medium-quality
    'Weak': 'P65',      # Top 35% for low-quality
    'Context': 'P60',   # Top 40% for context
    'Noise': 'P50'      # Median for noise
}

# At runtime, calculate actual thresholds from current data
def calculate_thresholds(scores, percentile_map):
    \"\"\"
    Calculate actual threshold values from percentile definitions.
    This adapts to score distribution changes over time.
    \"\"\"
    thresholds = {}
    for tier, percentile_name in percentile_map.items():
        # Extract percentile number (e.g., 'P75' -> 75)
        percentile = int(percentile_name[1:])
        thresholds[tier] = np.percentile(scores, percentile)
    return thresholds

# Example for initial deployment (calculated from evaluation sample)
DEPLOYED_THRESHOLDS = {
    'Core': 156.3,      # P75 on 2025-12-05 data
    'Moderate': 112.4,  # P70
    'Weak': 78.9,       # P65
    'Context': 45.6,    # P60
    'Noise': 23.1       # P50
}

# Recalculate monthly as score distribution changes
```

### Prediction Workflow

```python
def predict_topics(text, classifier, quality_percentile_map,
                   percentile_values_current_month):
    \"\"\"
    Predict topics using adaptive percentile-based thresholds.

    Args:
        text: Input text
        classifier: Model/dictionary scorer
        quality_percentile_map: Quality tier definitions (e.g., P90, P75, ...)
        percentile_values_current_month: Dict mapping quality_score to percentiles
    \"\"\"
    # 1. Get scores for all topics
    scores = classifier.predict(text)

    # 2. Calculate quality score (max across topics)
    quality_score = max(scores.values())

    # 3. Determine quality tier using current month's percentiles
    if quality_score >= percentile_values_current_month['P90']:
        tier = 'Core'
    elif quality_score >= percentile_values_current_month['P75']:
        tier = 'Moderate'
    elif quality_score >= percentile_values_current_month['P50']:
        tier = 'Weak'
    elif quality_score >= percentile_values_current_month['P25']:
        tier = 'Context'
    else:
        tier = 'Noise'

    # 4. Apply adaptive threshold for this tier
    threshold = DEPLOYED_THRESHOLDS[tier]
    present_topics = []

    for topic, score in scores.items():
        if score >= threshold:
            # Calculate confidence based on how far above threshold
            margin_above_threshold = score - threshold
            tier_range = (percentile_values_current_month[f'P{90}'] -
                         percentile_values_current_month[f'P{10}'])
            confidence_score = min(1.0, margin_above_threshold / (0.2 * tier_range))

            present_topics.append({
                'topic': topic,
                'score': score,
                'confidence': confidence_score
            })

    # 5. Calculate ranking correlation (for overall confidence)
    correlation = calculate_pattern_quality(scores)

    # 6. Return multi-label output
    return {
        'topics': sorted(present_topics, key=lambda x: x['score'], reverse=True),
        'quality_score': quality_score,
        'quality_tier': tier,
        'pattern_correlation': correlation,
        'confidence': determine_confidence(correlation, quality_score)
    }
```

---

## Threshold Maintenance

⭐ **NEW: Regular recalibration protocol**

### Monthly Recalibration

```python
def recalibrate_thresholds(new_data_this_month):
    \"\"\"
    Recalculate thresholds monthly as score distribution shifts.
    \"\"\"
    # Get all scores from this month
    all_scores = []
    for row in new_data_this_month:
        for topic in topics:
            all_scores.append(row[f'score_{topic}'])

    # Recalculate percentiles
    new_percentiles = {
        'P90': np.percentile(all_scores, 90),
        'P80': np.percentile(all_scores, 80),
        'P75': np.percentile(all_scores, 75),
        'P70': np.percentile(all_scores, 70),
        'P60': np.percentile(all_scores, 60),
        'P50': np.percentile(all_scores, 50),
        'P40': np.percentile(all_scores, 40),
        'P30': np.percentile(all_scores, 30),
        'P25': np.percentile(all_scores, 25),
        'P10': np.percentile(all_scores, 10)
    }

    # Recalculate deployed thresholds
    new_thresholds = {
        'Core': new_percentiles['P75'],
        'Moderate': new_percentiles['P70'],
        'Weak': new_percentiles['P65'],
        'Context': new_percentiles['P60'],
        'Noise': new_percentiles['P50']
    }

    # Compare to previous month
    print("Threshold drift analysis:")
    for tier, new_thresh in new_thresholds.items():
        old_thresh = DEPLOYED_THRESHOLDS[tier]
        drift = (new_thresh - old_thresh) / old_thresh * 100
        print(f"  {tier}: {old_thresh:.2f} → {new_thresh:.2f} ({drift:+.1f}%)")

    # Update if drift > 10%
    max_drift = max(abs((new - old) / old * 100)
                    for new, old in zip(new_thresholds.values(),
                                       DEPLOYED_THRESHOLDS.values()))

    if max_drift > 10:
        print(f"⚠️  Large drift detected ({max_drift:.1f}%), updating thresholds")
        return new_thresholds
    else:
        print(f"✓ Drift within tolerance ({max_drift:.1f}%), keeping current thresholds")
        return DEPLOYED_THRESHOLDS
```

---

## Confidence Calibration

[Mostly unchanged from V1.0, minor updates:]

### Confidence Levels

| Level | Criteria | Expected Accuracy | Action |
|-------|----------|-------------------|--------|
| **High** | Correlation ≥0.85 AND quality ≥P75 | 90-95% | Auto-approve |
| **Medium** | Correlation ≥0.70 OR quality ≥P50 | 75-85% | Batch review |
| **Low** | Correlation <0.70 AND quality <P50 | 50-70% | Individual review |
| **Reject** | Quality <P10 AND all scores <P25 | N/A | Mark as non-relevant |

⭐ **NEW: Quality thresholds use percentiles instead of fixed values**

---

## Monitoring Metrics

### Track These Metrics in Production

**Performance Metrics:**
- Multi-label F1 per topic (weekly)
- Ranking correlation distribution (daily)
- Confidence distribution (daily)

**Score Distribution Metrics:** ⭐ NEW
- P10, P25, P50, P75, P90 (daily)
- Standard deviation (daily)
- Alert if P90-P10 < 2×std (poor separation)

**Threshold Drift Metrics:** ⭐ NEW
- Monthly percentile recalculation
- Alert if drift > 10% from deployed thresholds
- Trigger re-evaluation if drift > 20%

**Operational Metrics:**
- % auto-approved (target: 70%)
- % requiring review (target: 30%)
- Human review turnaround time
- Inter-rater agreement

**Quality Metrics:**
- Precision/recall on reviewed samples
- False positive rate per topic
- False negative rate per topic
- User feedback on incorrect predictions

---

## Deployment Checklist

- [ ] ✓ Calculate initial percentile thresholds from evaluation data
- [ ] ✓ Verify score distribution shows good separation (P90-P10 > 2×std)
- [ ] ✓ If using dot product, confirm embeddings are unnormalized
- [ ] ✓ Configure adaptive thresholds for production environment
- [ ] ✓ Implement monthly recalibration workflow
- [ ] ✓ Set up confidence-based routing (auto-approve vs review)
- [ ] ✓ Create human review interface/workflow
- [ ] ✓ Deploy to [X%] of traffic (gradual rollout)
- [ ] ✓ Monitor percentile drift (alert if >10%)
- [ ] ✓ Re-evaluate if major changes to scoring system

---

## Troubleshooting

### Compressed Scores (Poor Discrimination)

**Symptoms:**
- P90-P10 < 2×std
- All scores in narrow range (e.g., 0.07-0.65 instead of 0-200)
- Unable to distinguish quality tiers

**Diagnosis:**
```python
scores = df[score_cols].values.flatten()
p90_p10_range = np.percentile(scores, 90) - np.percentile(scores, 10)
std = scores.std()

print(f"P90-P10 range: {p90_p10_range:.2f}")
print(f"Std dev: {std:.2f}")
print(f"Ratio: {p90_p10_range / std:.2f} (should be >2.0)")

if p90_p10_range / std < 2.0:
    print("⚠️  WARNING: Compressed score distribution")
```

**Solutions:**
1. **If using cosine similarity:** Switch to dot product scoring
2. **If embeddings normalized:** Use `normalize_embeddings=False`
3. **If dictionary-based:** Increase weight differences between terms
4. **If model-based:** Check if output layer is squashing scores

### Threshold Drift Over Time

**Symptoms:**
- Monthly recalibration shows >10% drift
- Performance degrading month-over-month

**Diagnosis:**
```python
# Compare percentiles month-over-month
for month in ['2025-12', '2025-11', '2025-10']:
    month_data = df[df['month'] == month]
    month_scores = month_data[score_cols].values.flatten()

    print(f"{month}:")
    for p in [10, 25, 50, 75, 90]:
        print(f"  P{p}: {np.percentile(month_scores, p):.2f}")
```

**Solutions:**
1. Implement monthly recalibration (see above)
2. If drift consistent in one direction, investigate data distribution changes
3. If drift erratic, may need more frequent recalibration or larger sample

---

## Files Created in This Evaluation

1. evaluation_sample.csv (stratified sample)
2. evaluation_sample_metadata.json ⭐ NEW (scoring system info)
3. STEP1_SEMANTIC_EVAL_chunks[X]-[Y].md (ground truth by batch)
4. STEP1_COMPLETE_SUMMARY.md (semantic ground truth summary)
5. STEP2_[CLASSIFIER]_MULTILABEL_EVALUATION.md (per classifier)
6. STEP3_COMPARATIVE_ANALYSIS.md (if multiple classifiers)
7. STEP4_FINAL_RECOMMENDATIONS.md (this file)

## Methodology Document

See: **METHODOLOGY_MULTILABEL_CLASSIFIER_EVALUATION_DOT_PRODUCT.md** (this document) for replication on new datasets with any scoring system.
```

---

## APPENDIX: CODE TEMPLATES

### A. Percentile-Based Stratified Sampling

```python
import pandas as pd
import numpy as np

def create_percentile_stratified_sample(df, score_col, n_per_tier=5, random_state=42):
    """
    Create quality-stratified sample using percentiles (adapts to any score range).

    Args:
        df: DataFrame with predictions
        score_col: Column name with quality scores (any range)
        n_per_tier: Number of samples per quality tier
        random_state: Random seed for reproducibility

    Returns:
        DataFrame with stratified sample + metadata dict
    """
    # Calculate percentiles
    p90 = df[score_col].quantile(0.90)
    p75 = df[score_col].quantile(0.75)
    p50 = df[score_col].quantile(0.50)
    p25 = df[score_col].quantile(0.25)

    # Define tiers using percentiles (adapts to any score distribution)
    def assign_tier(score):
        if score >= p90:
            return 'Core'
        elif score >= p75:
            return 'Moderate'
        elif score >= p50:
            return 'Weak'
        elif score >= p25:
            return 'Context'
        else:
            return 'Noise'

    df['tier'] = df[score_col].apply(assign_tier)

    # Stratified sample
    sample = df.groupby('tier', group_keys=False).apply(
        lambda x: x.sample(min(n_per_tier, len(x)), random_state=random_state)
    )

    # Metadata
    metadata = {
        'score_range': {
            'min': float(df[score_col].min()),
            'max': float(df[score_col].max()),
            'median': float(df[score_col].median())
        },
        'percentile_thresholds': {
            'p90': float(p90),
            'p75': float(p75),
            'p50': float(p50),
            'p25': float(p25)
        },
        'sample_size': len(sample),
        'tier_distribution': sample['tier'].value_counts().to_dict()
    }

    return sample.sort_values('tier'), metadata
```

### B. Adaptive Threshold Optimization (Percentile-Based)

```python
def optimize_percentile_thresholds(semantic_ratings, predictions, quality_scores, topics):
    """
    Find optimal percentile-based thresholds by quality tier.
    Works with any score range.

    Args:
        semantic_ratings: Dict {chunk_id: {topic: rating_0_to_3}}
        predictions: Dict {chunk_id: {topic: score (any range)}}
        quality_scores: Dict {chunk_id: quality_score}
        topics: List of topic names

    Returns:
        Dict {tier: {topic: {'percentile': P[X], 'value': float, 'f1': float}}}
    """
    # Calculate quality percentiles for tier definition
    all_quality_scores = list(quality_scores.values())
    p90 = np.percentile(all_quality_scores, 90)
    p75 = np.percentile(all_quality_scores, 75)
    p50 = np.percentile(all_quality_scores, 50)
    p25 = np.percentile(all_quality_scores, 25)

    # Group chunks by tier
    tiers = {'Core': [], 'Moderate': [], 'Weak': [], 'Context': [], 'Noise': []}
    for chunk_id, score in quality_scores.items():
        if score >= p90:
            tiers['Core'].append(chunk_id)
        elif score >= p75:
            tiers['Moderate'].append(chunk_id)
        elif score >= p50:
            tiers['Weak'].append(chunk_id)
        elif score >= p25:
            tiers['Context'].append(chunk_id)
        else:
            tiers['Noise'].append(chunk_id)

    optimal_thresholds = {}

    for tier, chunk_ids in tiers.items():
        if not chunk_ids:
            continue

        tier_thresholds = {}

        for topic in topics:
            # Collect all scores for this topic in this tier
            tier_topic_scores = [predictions[cid][topic] for cid in chunk_ids]

            # Calculate percentiles for this tier+topic
            percentiles = {
                'P90': np.percentile(tier_topic_scores, 90),
                'P80': np.percentile(tier_topic_scores, 80),
                'P75': np.percentile(tier_topic_scores, 75),
                'P70': np.percentile(tier_topic_scores, 70),
                'P65': np.percentile(tier_topic_scores, 65),
                'P60': np.percentile(tier_topic_scores, 60),
                'P50': np.percentile(tier_topic_scores, 50),
            }

            best_f1 = 0
            best_percentile_name = 'P60'
            best_threshold_value = percentiles['P60']

            # Test each percentile
            for percentile_name, threshold_value in percentiles.items():
                y_true = [1 if semantic_ratings[cid][topic] >= 2 else 0
                         for cid in chunk_ids]
                y_pred = [1 if predictions[cid][topic] >= threshold_value else 0
                         for cid in chunk_ids]

                from sklearn.metrics import precision_recall_fscore_support
                _, _, f1, _ = precision_recall_fscore_support(
                    y_true, y_pred, average='binary', zero_division=0
                )

                if f1 > best_f1:
                    best_f1 = f1
                    best_percentile_name = percentile_name
                    best_threshold_value = threshold_value

            tier_thresholds[topic] = {
                'percentile': best_percentile_name,
                'value': best_threshold_value,
                'f1': best_f1
            }

        optimal_thresholds[tier] = tier_thresholds

    return optimal_thresholds
```

### C. Multi-Label Metrics (Score-Independent)

```python
from sklearn.metrics import precision_recall_fscore_support

def calculate_multilabel_metrics(semantic_ratings, predictions, threshold_map, topics):
    """
    Calculate per-topic precision, recall, F1 for multi-label classification.
    Works with any score range - just provide appropriate thresholds.

    Args:
        semantic_ratings: Dict {chunk_id: {topic: rating_0_to_3}}
        predictions: Dict {chunk_id: {topic: score (any range)}}
        threshold_map: Float or Dict {topic: threshold} or Dict {tier: {topic: threshold}}
        topics: List of topic names

    Returns:
        Dict {topic: {'precision': X, 'recall': X, 'f1': X, 'threshold_used': X}}
    """
    results = {}

    for topic in topics:
        y_true = []
        y_pred = []
        thresholds_used = []

        for chunk_id in semantic_ratings.keys():
            # Ground truth: present if rating ≥2
            y_true.append(1 if semantic_ratings[chunk_id][topic] >= 2 else 0)

            # Determine threshold (supports multiple formats)
            if isinstance(threshold_map, (int, float)):
                # Global fixed threshold
                thresh = threshold_map
            elif isinstance(threshold_map, dict) and topic in threshold_map:
                # Per-topic threshold
                if isinstance(threshold_map[topic], (int, float)):
                    thresh = threshold_map[topic]
                else:
                    # Adaptive threshold - need quality tier
                    # (assuming quality_tier is in semantic_ratings or predictions)
                    quality_tier = predictions[chunk_id].get('_tier', 'Moderate')
                    thresh = threshold_map[quality_tier][topic]
            else:
                raise ValueError("Invalid threshold_map format")

            # Prediction: present if score ≥ threshold
            y_pred.append(1 if predictions[chunk_id][topic] >= thresh else 0)
            thresholds_used.append(thresh)

        # Calculate metrics
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true, y_pred, average='binary', zero_division=0
        )

        results[topic] = {
            'precision': float(precision),
            'recall': float(recall),
            'f1': float(f1),
            'threshold_used': {
                'mean': float(np.mean(thresholds_used)),
                'range': (float(np.min(thresholds_used)), float(np.max(thresholds_used)))
            }
        }

    # Macro-averaged F1
    macro_f1 = np.mean([metrics['f1'] for metrics in results.values()])
    results['macro_avg'] = {'f1': float(macro_f1)}

    return results
```

### D. Score Distribution Diagnostics

```python
def diagnose_score_distribution(df, score_cols, quality_col):
    """
    Diagnose score distribution to detect compression or other issues.

    Args:
        df: DataFrame with scores
        score_cols: List of score column names
        quality_col: Quality score column name

    Returns:
        Dict with diagnostic info
    """
    # Flatten all scores
    all_scores = df[score_cols].values.flatten()

    # Calculate statistics
    p10 = np.percentile(all_scores, 10)
    p25 = np.percentile(all_scores, 25)
    p50 = np.percentile(all_scores, 50)
    p75 = np.percentile(all_scores, 75)
    p90 = np.percentile(all_scores, 90)
    std = all_scores.std()

    # Calculate separation quality
    range_p90_p10 = p90 - p10
    separation_ratio = range_p90_p10 / std if std > 0 else 0

    # Detect scoring system type
    if p90 < 2.0:
        if p90 < 1.0:
            system_type = "cosine (0-1 range)"
        else:
            system_type = "rescaled (0-2 range)"
    else:
        system_type = "dot product (wide range)"

    # Quality assessment
    if separation_ratio >= 3.0:
        quality = "Good"
    elif separation_ratio >= 2.0:
        quality = "Fair"
    else:
        quality = "Poor (compressed)"

    diagnostics = {
        'system_type': system_type,
        'percentiles': {
            'p10': float(p10),
            'p25': float(p25),
            'p50': float(p50),
            'p75': float(p75),
            'p90': float(p90)
        },
        'statistics': {
            'min': float(all_scores.min()),
            'max': float(all_scores.max()),
            'mean': float(all_scores.mean()),
            'std': float(std),
            'range': float(all_scores.max() - all_scores.min())
        },
        'separation': {
            'p90_p10_range': float(range_p90_p10),
            'std': float(std),
            'ratio': float(separation_ratio),
            'quality': quality
        },
        'warnings': []
    }

    # Generate warnings
    if separation_ratio < 2.0:
        diagnostics['warnings'].append(
            "Compressed score distribution - consider switching to dot product scoring"
        )

    if p90 < 1.0 and system_type == "cosine (0-1 range)":
        diagnostics['warnings'].append(
            "Using cosine similarity - limited discrimination. "
            "Consider dot product for 10-100x wider range"
        )

    if std / np.mean(all_scores) < 0.2:
        diagnostics['warnings'].append(
            "Low coefficient of variation - scores too similar"
        )

    return diagnostics
```

---

## VERSION HISTORY

**v2.0 (2025-12-05) - Dot Product Adaptation**
- ✅ Replaced all fixed thresholds with percentile-based adaptive thresholds
- ✅ Added score distribution diagnostics
- ✅ Updated quality stratification to use percentiles
- ✅ Added monthly recalibration protocol
- ✅ Made methodology score-range agnostic (0-1, 0-2, 0-200+)
- ✅ Added troubleshooting section for compressed scores
- ✅ Updated code templates for adaptive thresholds

**v1.0 (2025-12-03)**
- Initial methodology document
- Based on Dutch Caribbean slavery legacy evaluation
- Validated on 25-chunk stratified sample with cosine/rescaled scores
- Multi-label evaluation with fixed adaptive thresholds
- Ranking correlation analysis

**Future versions:**
- Add support for hierarchical topics
- Include active learning workflow
- Add inter-rater agreement protocols
- Expand to multi-language evaluation
- Add cross-corpus evaluation protocols

---

## LICENSE & CITATION

This methodology is released under [LICENSE TYPE].

**Citation:**
```
Multi-Label Classifier Evaluation Protocol v2.0 - Dot Product Edition (2025)
Developed for Dutch Caribbean Slavery Legacy Project
Adapted for unnormalized dot product scoring systems
```

**Acknowledgments:**
- Based on v1.0 evaluation of BERTJE neural model and Cosine dictionary method
- v2.0 adapted for dot product scoring with unnormalized embeddings
- Evaluated on policy document chunks with both scoring systems
- Achieved robust performance across 0-1 cosine and 0-200 dot product ranges

---

## CONTACT

For questions, improvements, or adaptations of this methodology:
[Contact information]

**Recommended Use Cases:**
- Multi-label text classification evaluation
- Policy document classification
- Topic modeling validation
- Classifier comparison studies (different scoring systems)
- Migration from cosine to dot product scoring
- Production deployment readiness assessment
- Score distribution diagnostics
