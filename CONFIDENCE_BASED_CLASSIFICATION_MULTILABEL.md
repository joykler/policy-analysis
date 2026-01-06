# Multi-Label Confidence Classification (Corrected Approach)

## The Problem with Margin-Based Confidence

**Original flawed assumption:**
- High margin (top topic >> 2nd topic) = High confidence ❌
- Low margin (top ≈ 2nd topic) = Low confidence / Ambiguous ❌

**Why this is wrong for multi-label:**
- Multi-label texts SHOULD have multiple high scores (low margin)
- Margin-based confidence penalizes true multi-topic chunks
- Single-label bias in a multi-label problem

## Correct Multi-Label Confidence

**Confidence should mean:** "How confident are we that THIS SPECIFIC TOPIC is present/absent?"

Not: "How confident are we about THE primary topic?"

---

## Per-Topic Presence/Absence Classification

### Core Principle: Independent Binary Decisions

For each topic independently:
1. Score ≥ threshold → Topic is PRESENT
2. Score < threshold → Topic is ABSENT
3. Confidence = Distance from threshold

**Multiple topics can simultaneously be "high confidence present"** ✅

---

## Three-Level Threshold System

### Per-Topic Thresholds (Calibrated from Evaluation)

```python
# Calibrate from manual evaluation sample
TOPIC_THRESHOLDS = {
    'clearly_present': 70,      # Score ≥70 → Definitely present
    'likely_present': 50,        # Score 50-70 → Probably present
    'weak_signal': 30,           # Score 30-50 → Weak/unclear
    # Score <30 → Absent
}

def classify_topic_presence(score):
    """
    Classify whether a single topic is present in a chunk.

    Returns confidence level and presence status.
    """
    if score >= TOPIC_THRESHOLDS['clearly_present']:
        return {
            'present': True,
            'confidence': 'high',
            'confidence_score': min(1.0, (score - 70) / 50),  # 0.0 at 70, 1.0 at 120+
            'strength': 'strong'
        }

    elif score >= TOPIC_THRESHOLDS['likely_present']:
        return {
            'present': True,
            'confidence': 'medium',
            'confidence_score': (score - 50) / 20,  # 0.0 at 50, 1.0 at 70
            'strength': 'moderate'
        }

    elif score >= TOPIC_THRESHOLDS['weak_signal']:
        return {
            'present': True,
            'confidence': 'low',
            'confidence_score': (score - 30) / 20,  # 0.0 at 30, 1.0 at 50
            'strength': 'weak'
        }

    else:
        return {
            'present': False,
            'confidence': 'n/a',
            'confidence_score': 0.0,
            'strength': 'absent'
        }
```

---

## Multi-Label Classification Result

### Example: Chunk with Multiple Topics

```python
chunk_scores = {
    'Persistent_Poverty': 125.4,
    'Social_Fragmentation': 87.8,
    'Educational_Disadvantage': 52.1,
    'Governance_Distrust': 28.3
}

# Classify each topic independently
results = {}
for topic, score in chunk_scores.items():
    results[topic] = classify_topic_presence(score)

# Output:
{
    'Persistent_Poverty': {
        'present': True,
        'confidence': 'high',      # Score 125 >> 70
        'confidence_score': 0.90,
        'strength': 'strong'
    },
    'Social_Fragmentation': {
        'present': True,
        'confidence': 'high',      # Score 88 > 70
        'confidence_score': 0.36,
        'strength': 'strong'
    },
    'Educational_Disadvantage': {
        'present': True,
        'confidence': 'medium',    # Score 52 in 50-70 range
        'confidence_score': 0.10,
        'strength': 'moderate'
    },
    'Governance_Distrust': {
        'present': False,          # Score 28 < 30
        'confidence': 'n/a',
        'confidence_score': 0.0,
        'strength': 'absent'
    }
}

# This chunk is MULTI-LABEL: 3 topics present with varying strengths
# This is GOOD and EXPECTED, not "low confidence"!
```

---

## Chunk-Level Confidence Metrics

Even though we classify per-topic, we can still characterize overall chunk quality:

### 1. Max Score (Primary Relevance)
```python
max_score = max(chunk_scores.values())

# How relevant is this chunk to ANY of our topics?
if max_score >= 70:
    primary_relevance = "high"
elif max_score >= 50:
    primary_relevance = "medium"
else:
    primary_relevance = "low"
```

### 2. Number of Present Topics
```python
n_present = sum(1 for result in results.values() if result['present'])

# Multi-label complexity
if n_present == 0:
    complexity = "not_relevant"
elif n_present == 1:
    complexity = "single_topic"
elif n_present == 2:
    complexity = "dual_topic"
else:
    complexity = "multi_topic"
```

### 3. Score Spread (Differentiation Quality)
```python
score_std = np.std(list(chunk_scores.values()))
score_range = max(chunk_scores.values()) - min(chunk_scores.values())

# Can we clearly distinguish present from absent topics?
if score_range > 50 and score_std > 20:
    differentiation = "clear"  # Easy to distinguish topics
elif score_range > 30 or score_std > 15:
    differentiation = "moderate"
else:
    differentiation = "poor"  # All scores similar = ambiguous
```

### Combined Chunk Characterization
```python
def characterize_chunk(chunk_scores):
    """
    Characterize overall chunk quality and complexity.

    Does NOT use margin (that's single-label thinking).
    """
    max_score = max(chunk_scores.values())
    score_std = np.std(list(chunk_scores.values()))
    score_range = max(chunk_scores.values()) - min(chunk_scores.values())

    # Classify each topic
    topic_results = {
        topic: classify_topic_presence(score)
        for topic, score in chunk_scores.items()
    }

    # Count present topics
    n_present = sum(1 for r in topic_results.values() if r['present'])
    n_high_conf = sum(1 for r in topic_results.values()
                      if r['present'] and r['confidence'] == 'high')

    return {
        'max_score': max_score,
        'primary_relevance': (
            'high' if max_score >= 70
            else 'medium' if max_score >= 50
            else 'low'
        ),
        'n_topics_present': n_present,
        'n_high_confidence': n_high_conf,
        'complexity': (
            'not_relevant' if n_present == 0
            else 'single_topic' if n_present == 1
            else 'dual_topic' if n_present == 2
            else 'multi_topic'
        ),
        'differentiation': (
            'clear' if score_range > 50 and score_std > 20
            else 'moderate' if score_range > 30 or score_std > 15
            else 'poor'
        ),
        'topic_results': topic_results
    }
```

---

## Training Data Selection (Multi-Label)

### Use for Training Based on:

**1. High-Confidence Single-Topic Chunks**
```python
# Good for learning clear topic boundaries
if n_high_conf == 1 and differentiation == 'clear':
    use_case = "single_topic_training"
    priority = "high"
```

**2. High-Confidence Multi-Topic Chunks**
```python
# Good for learning topic co-occurrence patterns
if n_high_conf >= 2 and differentiation == 'clear':
    use_case = "multi_topic_training"
    priority = "high"
```

**3. Medium-Confidence Chunks**
```python
# Good for adding diversity, but review first
if n_present >= 1 and max_score >= 50:
    use_case = "supplemental_training"
    priority = "medium"
```

**4. Ambiguous Chunks**
```python
# Poor differentiation or all scores similar
if differentiation == 'poor' or (n_present > 0 and max_score < 50):
    use_case = "manual_review_needed"
    priority = "low"
```

**5. Not Relevant**
```python
# No topics present - useful as negative examples
if n_present == 0:
    use_case = "negative_examples"
    priority = "low"
```

---

## Implementation in Notebook

### Cell 37: Multi-Label Confidence Classification

```python
# ============================================================
# CELL 5.2: MULTI-LABEL CONFIDENCE CLASSIFICATION
# ============================================================

print(f"\n{'='*80}")
print("MULTI-LABEL CONFIDENCE CLASSIFICATION")
print(f"{'='*80}")

# Calibrated thresholds (from evaluation sample)
# Set once, don't change unless scoring system changes
TOPIC_THRESHOLDS = {
    'clearly_present': 70,   # Strong presence
    'likely_present': 50,     # Moderate presence
    'weak_signal': 30,        # Weak/unclear presence
    # <30 = Absent
}

def classify_topic_presence(score):
    """Classify single topic presence with confidence."""
    if score >= TOPIC_THRESHOLDS['clearly_present']:
        return {
            'present': True,
            'confidence': 'high',
            'confidence_score': min(1.0, (score - 70) / 50),
            'strength': 'strong'
        }
    elif score >= TOPIC_THRESHOLDS['likely_present']:
        return {
            'present': True,
            'confidence': 'medium',
            'confidence_score': (score - 50) / 20,
            'strength': 'moderate'
        }
    elif score >= TOPIC_THRESHOLDS['weak_signal']:
        return {
            'present': True,
            'confidence': 'low',
            'confidence_score': (score - 30) / 20,
            'strength': 'weak'
        }
    else:
        return {
            'present': False,
            'confidence': 'n/a',
            'confidence_score': 0.0,
            'strength': 'absent'
        }

def characterize_chunk(row, topic_cols):
    """
    Characterize chunk using multi-label approach.

    Returns per-topic classifications and overall chunk quality.
    """
    # Get scores for all topics
    chunk_scores = {col.replace('score_', ''): row[col] for col in topic_cols}

    # Classify each topic independently
    topic_results = {
        topic: classify_topic_presence(score)
        for topic, score in chunk_scores.items()
    }

    # Calculate chunk-level metrics
    max_score = max(chunk_scores.values())
    score_std = np.std(list(chunk_scores.values()))
    score_range = max(chunk_scores.values()) - min(chunk_scores.values())

    n_present = sum(1 for r in topic_results.values() if r['present'])
    n_high_conf = sum(1 for r in topic_results.values()
                      if r['present'] and r['confidence'] == 'high')
    n_medium_conf = sum(1 for r in topic_results.values()
                        if r['present'] and r['confidence'] == 'medium')

    # Overall characterization
    return {
        'max_score': max_score,
        'score_std': score_std,
        'score_range': score_range,
        'n_topics_present': n_present,
        'n_high_confidence': n_high_conf,
        'n_medium_confidence': n_medium_conf,
        'primary_relevance': (
            'high' if max_score >= 70
            else 'medium' if max_score >= 50
            else 'low' if max_score >= 30
            else 'not_relevant'
        ),
        'complexity': (
            'not_relevant' if n_present == 0
            else 'single_topic' if n_present == 1
            else 'dual_topic' if n_present == 2
            else 'multi_topic'
        ),
        'differentiation': (
            'clear' if score_range > 50 and score_std > 20
            else 'moderate' if score_range > 30 or score_std > 15
            else 'poor'
        ),
        'use_for_training': (
            n_present > 0 and max_score >= 50
        ),
        'priority': (
            'high' if n_high_conf >= 1 and score_range > 50
            else 'medium' if n_present >= 1 and max_score >= 50
            else 'low'
        ),
        'topic_results': topic_results
    }

# Apply to all chunks
print("\nClassifying chunks...")

topic_cols = [col for col in all_scores_df.columns if col.startswith('score_')]
topics = [col.replace('score_', '') for col in topic_cols]

characterizations = []
for idx, row in tqdm(all_scores_df.iterrows(), total=len(all_scores_df), desc="Classifying"):
    char = characterize_chunk(row, topic_cols)
    characterizations.append(char)

# Add chunk-level columns
all_scores_df['primary_relevance'] = [c['primary_relevance'] for c in characterizations]
all_scores_df['n_topics_present'] = [c['n_topics_present'] for c in characterizations]
all_scores_df['n_high_confidence'] = [c['n_high_confidence'] for c in characterizations]
all_scores_df['n_medium_confidence'] = [c['n_medium_confidence'] for c in characterizations]
all_scores_df['complexity'] = [c['complexity'] for c in characterizations]
all_scores_df['differentiation'] = [c['differentiation'] for c in characterizations]
all_scores_df['use_for_training'] = [c['use_for_training'] for c in characterizations]
all_scores_df['priority'] = [c['priority'] for c in characterizations]

# Add per-topic presence columns
for topic in topics:
    all_scores_df[f'{topic}_present'] = [
        c['topic_results'][topic]['present'] for c in characterizations
    ]
    all_scores_df[f'{topic}_confidence'] = [
        c['topic_results'][topic]['confidence'] for c in characterizations
    ]
    all_scores_df[f'{topic}_strength'] = [
        c['topic_results'][topic]['strength'] for c in characterizations
    ]

print(f"\n{'='*80}")
print("CLASSIFICATION RESULTS")
print(f"{'='*80}")

# Overall distribution
print(f"\nPrimary relevance distribution:")
print(all_scores_df['primary_relevance'].value_counts())

print(f"\nComplexity distribution:")
print(all_scores_df['complexity'].value_counts())

print(f"\nDifferentiation quality:")
print(all_scores_df['differentiation'].value_counts())

print(f"\nTraining priority:")
print(all_scores_df['priority'].value_counts())

# Per-topic presence
print(f"\n{'='*80}")
print("PER-TOPIC PRESENCE")
print(f"{'='*80}")

for topic in topics:
    n_present = all_scores_df[f'{topic}_present'].sum()
    n_high = (all_scores_df[f'{topic}_confidence'] == 'high').sum()
    n_medium = (all_scores_df[f'{topic}_confidence'] == 'medium').sum()
    n_low = (all_scores_df[f'{topic}_confidence'] == 'low').sum()

    print(f"\n{topic}:")
    print(f"  Present: {n_present} ({n_present/len(all_scores_df)*100:.1f}%)")
    print(f"    High confidence:   {n_high}")
    print(f"    Medium confidence: {n_medium}")
    print(f"    Low confidence:    {n_low}")

# Multi-label statistics
print(f"\n{'='*80}")
print("MULTI-LABEL STATISTICS")
print(f"{'='*80}")

multi_topic = all_scores_df['n_topics_present'] >= 2
print(f"\nMulti-topic chunks: {multi_topic.sum()} ({multi_topic.sum()/len(all_scores_df)*100:.1f}%)")

for n in range(0, len(topics)+1):
    count = (all_scores_df['n_topics_present'] == n).sum()
    pct = count / len(all_scores_df) * 100
    print(f"  {n} topics present: {count:5d} ({pct:5.1f}%)")

print(f"\n{'='*80}")
print("TRAINING DATA RECOMMENDATIONS")
print(f"{'='*80}")

high_priority = all_scores_df['priority'] == 'high'
medium_priority = all_scores_df['priority'] == 'medium'
low_priority = all_scores_df['priority'] == 'low'

print(f"\nHigh priority (clear single or multi-topic):")
print(f"  Count: {high_priority.sum()} ({high_priority.sum()/len(all_scores_df)*100:.1f}%)")
print(f"  Use for: Primary training data")

print(f"\nMedium priority (moderate confidence):")
print(f"  Count: {medium_priority.sum()} ({medium_priority.sum()/len(all_scores_df)*100:.1f}%)")
print(f"  Use for: Supplemental training after review")

print(f"\nLow priority (ambiguous or not relevant):")
print(f"  Count: {low_priority.sum()} ({low_priority.sum()/len(all_scores_df)*100:.1f}%)")
print(f"  Use for: Negative examples or manual review")
```

---

## Calibration from Evaluation Sample

### Step 1: Manual Multi-Label Annotation

For each chunk in sample, rate EACH topic independently (0-3):
```
Rating 0: Topic not present
Rating 1: Weak/peripheral mention
Rating 2: Moderate presence (secondary theme)
Rating 3: Strong presence (primary theme)
```

**Key: Rate ALL topics, allow multiple high ratings**

### Step 2: Find Optimal Threshold

```python
from sklearn.metrics import precision_recall_fscore_support

# For each topic, find threshold that best separates present (≥2) from absent (<2)
optimal_thresholds = {}

for topic in topics:
    best_f1 = 0
    best_threshold = 50

    for threshold in range(20, 100, 5):
        y_true = [1 if row[f'semantic_{topic}'] >= 2 else 0 for _, row in sample.iterrows()]
        y_pred = [1 if row[f'score_{topic}'] >= threshold else 0 for _, row in sample.iterrows()]

        _, _, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='binary')

        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold

    optimal_thresholds[topic] = {
        'threshold': best_threshold,
        'f1': best_f1
    }

    print(f"{topic}: threshold={best_threshold}, F1={best_f1:.2f}")

# If thresholds are similar across topics, use global threshold
thresholds_values = [t['threshold'] for t in optimal_thresholds.values()]
if max(thresholds_values) - min(thresholds_values) < 20:
    global_threshold = int(np.mean(thresholds_values))
    print(f"\nUsing global threshold: {global_threshold}")
```

### Step 3: Validate Multi-Label Performance

```python
# Apply thresholds to validation set
for topic in topics:
    threshold = optimal_thresholds[topic]['threshold']

    val_sample[f'{topic}_predicted'] = val_sample[f'score_{topic}'] >= threshold
    val_sample[f'{topic}_actual'] = val_sample[f'semantic_{topic}'] >= 2

    # Per-topic metrics
    precision, recall, f1, _ = precision_recall_fscore_support(
        val_sample[f'{topic}_actual'],
        val_sample[f'{topic}_predicted'],
        average='binary'
    )

    print(f"\n{topic}:")
    print(f"  Precision: {precision:.2f}")
    print(f"  Recall: {recall:.2f}")
    print(f"  F1: {f1:.2f}")

# Multi-label metrics (macro-averaged)
all_y_true = []
all_y_pred = []

for topic in topics:
    all_y_true.extend(val_sample[f'{topic}_actual'].tolist())
    all_y_pred.extend(val_sample[f'{topic}_predicted'].tolist())

macro_precision, macro_recall, macro_f1, _ = precision_recall_fscore_support(
    all_y_true, all_y_pred, average='macro'
)

print(f"\nMacro-averaged (multi-label):")
print(f"  Precision: {macro_precision:.2f}")
print(f"  Recall: {macro_recall:.2f}")
print(f"  F1: {macro_f1:.2f}")
```

---

## Key Differences from Margin-Based Approach

| Aspect | ❌ Margin-Based (Wrong) | ✅ Per-Topic Thresholds (Correct) |
|--------|------------------------|-----------------------------------|
| **Philosophy** | Single-label with "ambiguity" penalty | True multi-label independent classification |
| **Margin interpretation** | High margin = good | Margin irrelevant for multi-label |
| **Multi-topic chunks** | Penalized as "low confidence" | Correctly identified as multi-topic |
| **Confidence meaning** | "How clear is THE winner?" | "How confident per topic?" |
| **Training selection** | Biased toward single-topic | Balanced single + multi-topic |
| **Threshold type** | Relative (margin-based) | Absolute (per-topic score) |
| **Transferability** | Context-dependent | Corpus-independent |

---

## Summary

**For multi-label classification:**
1. ✅ Use **per-topic absolute thresholds** (50, 70, etc.)
2. ✅ Classify **each topic independently**
3. ✅ Allow **multiple topics** to be "high confidence present"
4. ❌ Don't use **margin** as confidence metric
5. ❌ Don't penalize **multi-topic chunks**

**Confidence means:** "How sure are we this specific topic is present/absent?"

**Not:** "How sure are we about which single topic wins?"
