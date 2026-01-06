# Confidence-Based Classification (Better than Percentile Thresholds)

## Problem with Percentile Thresholds

**Percentile thresholds are relative, not absolute:**
- Force a distribution: "Top 10% is good" even if all chunks are mediocre
- Not transferable across corpora
- Can't answer "Is this chunk actually relevant to slavery topics?"
- Only answer "Is this chunk more relevant than other chunks in this corpus?"

## Solution: Confidence-Based Absolute Thresholds

Use **score magnitude + margin** to measure absolute relevance and confidence.

---

## Key Metrics

### 1. Primary Score (Magnitude)
```python
primary_score = max(topic_scores)
```
**Interpretation:** How strongly does this chunk relate to ANY topic?
- High score (80+): Strong topic presence
- Medium score (50-80): Moderate topic presence
- Low score (30-50): Weak topic presence
- Very low (<30): Background/noise

### 2. Margin (Confidence)
```python
sorted_scores = np.sort(topic_scores)[::-1]
margin = sorted_scores[0] - sorted_scores[1]
```
**Interpretation:** How clear is the primary topic?
- High margin (30+): Single clear topic
- Medium margin (15-30): Primary topic with secondary presence
- Low margin (<15): Multi-topic or ambiguous

### 3. Relative Margin (Normalized Confidence)
```python
relative_margin = margin / primary_score if primary_score > 0 else 0
```
**Interpretation:** Confidence relative to score magnitude
- High (>0.30): 30%+ separation → Very confident
- Medium (0.15-0.30): 15-30% separation → Reasonably confident
- Low (<0.15): <15% separation → Ambiguous/multi-topic

---

## Classification Schema

### Four-Tier System (Absolute Thresholds)

```python
def classify_chunk(primary_score, margin):
    """
    Classify chunk using absolute thresholds.

    Thresholds calibrated from manual evaluation sample.
    Do NOT change unless scoring system changes.
    """
    relative_margin = margin / primary_score if primary_score > 0 else 0

    # Tier 1: High Confidence - Single Clear Topic
    if primary_score >= 80 and margin >= 30:
        return {
            'tier': 'high_confidence',
            'description': 'Single clear topic, strong presence',
            'use_case': 'Training data, auto-approve',
            'expected_accuracy': 0.90
        }

    # Tier 2: Medium Confidence - Clear Primary Topic
    elif primary_score >= 50 and margin >= 20:
        return {
            'tier': 'medium_confidence',
            'description': 'Clear primary topic, may have secondary',
            'use_case': 'Training data, batch review',
            'expected_accuracy': 0.75
        }

    # Tier 3: Low Confidence - Multi-topic or Weak
    elif primary_score >= 30 or (primary_score >= 20 and margin >= 10):
        return {
            'tier': 'low_confidence',
            'description': 'Multi-topic, ambiguous, or weak signals',
            'use_case': 'Individual review, edge cases',
            'expected_accuracy': 0.50
        }

    # Tier 4: Not Relevant
    else:
        return {
            'tier': 'not_relevant',
            'description': 'No clear topic presence',
            'use_case': 'Filter out, negative examples',
            'expected_accuracy': 0.10
        }
```

### Decision Matrix

| Primary Score | Margin | Tier | Interpretation |
|---------------|--------|------|----------------|
| 80+ | 30+ | High | Strong, clear single topic |
| 80+ | 15-30 | Medium | Strong primary, secondary present |
| 80+ | <15 | Low | Strong multi-topic |
| 50-80 | 20+ | Medium | Moderate, clear primary |
| 50-80 | 10-20 | Low | Moderate multi-topic |
| 50-80 | <10 | Low | Ambiguous |
| 30-50 | 15+ | Low | Weak but distinguishable |
| 30-50 | <15 | Not Relevant | Very weak/ambiguous |
| <30 | Any | Not Relevant | Background/noise |

---

## Calibration Process (One-Time)

### Step 1: Manual Evaluation Sample (25-50 chunks)

Rate each chunk:
- **Relevance:** Is ANY topic clearly present? (Yes/No)
- **Clarity:** Is there ONE clear primary topic? (Yes/Ambiguous/Multi-topic)

### Step 2: Plot Score vs Manual Rating

```python
import matplotlib.pyplot as plt

# Plot primary_score vs manual relevance
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Score distribution by relevance
relevant_scores = [row['primary_score'] for row in sample if row['manual_relevant'] == 'Yes']
not_relevant_scores = [row['primary_score'] for row in sample if row['manual_relevant'] == 'No']

axes[0].hist(not_relevant_scores, alpha=0.5, label='Not Relevant', bins=20)
axes[0].hist(relevant_scores, alpha=0.5, label='Relevant', bins=20)
axes[0].axvline(x=50, color='r', linestyle='--', label='Proposed threshold')
axes[0].set_xlabel('Primary Score')
axes[0].set_ylabel('Count')
axes[0].set_title('Score Distribution by Relevance')
axes[0].legend()

# Plot 2: Margin distribution by clarity
single_topic_margins = [row['margin'] for row in sample if row['manual_clarity'] == 'Single']
multi_topic_margins = [row['margin'] for row in sample if row['manual_clarity'] == 'Multi']

axes[1].hist(multi_topic_margins, alpha=0.5, label='Multi-topic', bins=20)
axes[1].hist(single_topic_margins, alpha=0.5, label='Single topic', bins=20)
axes[1].axvline(x=20, color='r', linestyle='--', label='Proposed threshold')
axes[1].set_xlabel('Margin')
axes[1].set_ylabel('Count')
axes[1].set_title('Margin Distribution by Clarity')
axes[1].legend()

plt.tight_layout()
plt.savefig('threshold_calibration.png')
```

### Step 3: Find Optimal Cut Points

```python
from sklearn.metrics import accuracy_score, f1_score

# Test different primary_score thresholds
best_score_threshold = None
best_accuracy = 0

for threshold in range(20, 100, 5):
    predicted = [1 if row['primary_score'] >= threshold else 0 for row in sample]
    actual = [1 if row['manual_relevant'] == 'Yes' else 0 for row in sample]

    accuracy = accuracy_score(actual, predicted)
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_score_threshold = threshold

print(f"Optimal primary_score threshold: {best_score_threshold} (accuracy: {best_accuracy:.2f})")

# Test different margin thresholds
best_margin_threshold = None
best_f1 = 0

relevant_sample = [row for row in sample if row['manual_relevant'] == 'Yes']

for threshold in range(5, 50, 5):
    predicted = [1 if row['margin'] >= threshold else 0 for row in relevant_sample]
    actual = [1 if row['manual_clarity'] == 'Single' else 0 for row in relevant_sample]

    f1 = f1_score(actual, predicted)
    if f1 > best_f1:
        best_f1 = f1
        best_margin_threshold = threshold

print(f"Optimal margin threshold: {best_margin_threshold} (F1: {best_f1:.2f})")
```

### Step 4: Validate Thresholds

```python
# Apply calibrated thresholds to validation set
def apply_thresholds(row, score_thresh, margin_thresh):
    if row['primary_score'] < score_thresh:
        return 'not_relevant'
    elif row['margin'] >= margin_thresh:
        return 'high_confidence'
    else:
        return 'low_confidence'

validation_sample['predicted_tier'] = validation_sample.apply(
    lambda row: apply_thresholds(row, best_score_threshold, best_margin_threshold),
    axis=1
)

# Compare to manual labels
print("\nConfusion Matrix:")
print(pd.crosstab(validation_sample['manual_tier'], validation_sample['predicted_tier']))
```

---

## Implementation in Notebook

### Cell Update: Confidence Classification

Replace percentile-based tier assignment with confidence-based:

```python
# ============================================================
# CONFIDENCE-BASED CLASSIFICATION (Absolute Thresholds)
# ============================================================

# Calibrated thresholds (from evaluation sample - DO NOT change without re-evaluation)
CONFIDENCE_THRESHOLDS = {
    'min_relevant_score': 50,       # Below this = not relevant
    'high_confidence_score': 80,    # Above this + margin = high confidence
    'min_single_topic_margin': 20,  # Below this = multi-topic or ambiguous
    'high_confidence_margin': 30    # Above this = very confident single topic
}

def classify_by_confidence(primary_score, margin):
    """
    Classify chunk using absolute confidence thresholds.

    These thresholds are FIXED based on evaluation sample.
    Only change if scoring system changes (model retrain, dictionary update, etc.)

    Args:
        primary_score: Highest topic score for chunk
        margin: Difference between top and 2nd topic scores

    Returns:
        dict with tier, confidence, and metadata
    """
    relative_margin = margin / primary_score if primary_score > 0 else 0

    # Not relevant: Low score
    if primary_score < CONFIDENCE_THRESHOLDS['min_relevant_score']:
        return {
            'confidence_tier': 'not_relevant',
            'confidence_score': 0.0,
            'single_topic': False,
            'use_for_training': False,
            'needs_review': False
        }

    # High confidence: High score + high margin
    elif (primary_score >= CONFIDENCE_THRESHOLDS['high_confidence_score'] and
          margin >= CONFIDENCE_THRESHOLDS['high_confidence_margin']):
        return {
            'confidence_tier': 'high',
            'confidence_score': 0.9,
            'single_topic': True,
            'use_for_training': True,
            'needs_review': False
        }

    # Medium confidence: Decent score + decent margin
    elif (primary_score >= CONFIDENCE_THRESHOLDS['min_relevant_score'] and
          margin >= CONFIDENCE_THRESHOLDS['min_single_topic_margin']):
        return {
            'confidence_tier': 'medium',
            'confidence_score': 0.7,
            'single_topic': True,
            'use_for_training': True,
            'needs_review': True  # Batch review recommended
        }

    # Low confidence: Relevant but ambiguous/multi-topic
    else:
        return {
            'confidence_tier': 'low',
            'confidence_score': 0.4,
            'single_topic': False,
            'use_for_training': True,  # Can use for multi-label training
            'needs_review': True
        }

# Apply to all scored chunks
print(f"\n{'='*60}")
print("APPLYING CONFIDENCE-BASED CLASSIFICATION")
print(f"{'='*60}")

confidence_results = []
for idx, row in all_scores_df.iterrows():
    classification = classify_by_confidence(row['max_score'], row['score_margin'])
    confidence_results.append(classification)

# Add to dataframe
for key in confidence_results[0].keys():
    all_scores_df[key] = [r[key] for r in confidence_results]

# Show distribution
print(f"\nConfidence tier distribution:")
print(all_scores_df['confidence_tier'].value_counts())

print(f"\nConfidence statistics:")
for tier in ['high', 'medium', 'low', 'not_relevant']:
    tier_df = all_scores_df[all_scores_df['confidence_tier'] == tier]
    if len(tier_df) > 0:
        print(f"\n  {tier.upper()}:")
        print(f"    Count: {len(tier_df)}")
        print(f"    Mean score: {tier_df['max_score'].mean():.2f}")
        print(f"    Mean margin: {tier_df['score_margin'].mean():.2f}")
        print(f"    Use for training: {tier_df['use_for_training'].sum()}")
```

---

## Benefits of Confidence-Based Approach

### 1. Absolute Relevance Measurement
- "This chunk IS relevant" vs "This chunk is MORE relevant than others"
- Transferable across corpora

### 2. No Forced Distribution
- If all chunks are relevant, all can be labeled high confidence
- If all chunks are noise, all can be labeled not relevant
- Distribution adapts to actual content quality

### 3. Multi-Topic Detection Built-In
- Low margin = multiple topics present
- High margin = single clear topic
- More informative than binary single/multi label

### 4. Simpler Maintenance
- Set thresholds once from evaluation
- No monthly recalibration needed
- Only update if scoring system changes

### 5. Interpretable
- Primary score = "How relevant?"
- Margin = "How confident/clear?"
- Easy to explain to stakeholders

---

## When to Update Thresholds

### DO Update When:
✅ Model retrained (scores might shift)
✅ Dictionary significantly updated (topic vectors change)
✅ Embedding model updated (all embeddings change)
✅ Evaluation shows thresholds are miscalibrated

### DON'T Update When:
❌ New corpus with different content
❌ Different mix of topics in data
❌ Seasonal variations in content
❌ "It's been a month"

### How to Decide:
```python
# Check if score distribution has shifted
def check_distribution_shift(old_scores, new_scores):
    """
    Compare score distributions to detect system changes.

    Returns True if thresholds need recalibration.
    """
    # Calculate KL divergence or similar metric
    from scipy.stats import ks_2samp

    # Test if distributions are significantly different
    statistic, pvalue = ks_2samp(old_scores, new_scores)

    if pvalue < 0.01:
        print(f"⚠️  Distribution shift detected (p={pvalue:.4f})")
        print(f"    Old mean: {np.mean(old_scores):.2f}")
        print(f"    New mean: {np.mean(new_scores):.2f}")
        print(f"    → Recommend re-evaluation and threshold recalibration")
        return True
    else:
        print(f"✓ Distribution stable (p={pvalue:.4f})")
        return False
```

---

## Example Usage

```python
# Score a new chunk
chunk_scores = {
    'topic1': 145.2,
    'topic2': 98.7,
    'topic3': 76.3,
    'topic4': 54.1
}

primary_score = max(chunk_scores.values())  # 145.2
sorted_scores = sorted(chunk_scores.values(), reverse=True)
margin = sorted_scores[0] - sorted_scores[1]  # 145.2 - 98.7 = 46.5

classification = classify_by_confidence(primary_score, margin)

print(f"Primary score: {primary_score:.1f}")
print(f"Margin: {margin:.1f}")
print(f"Classification: {classification['confidence_tier']}")
print(f"Single topic: {classification['single_topic']}")
print(f"Use for training: {classification['use_for_training']}")
print(f"Needs review: {classification['needs_review']}")

# Output:
# Primary score: 145.2
# Margin: 46.5
# Classification: high
# Single topic: True
# Use for training: True
# Needs review: False
```
