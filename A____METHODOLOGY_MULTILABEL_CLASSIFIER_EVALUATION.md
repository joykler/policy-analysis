# METHODOLOGY: Multi-Label Classifier Evaluation Protocol
**Version:** 1.0
**Date:** 2025-12-03
**Purpose:** Reusable step-by-step methodology for evaluating multi-label text classifiers against semantic ground truth

---

## OVERVIEW

This methodology evaluates how well automated classifiers (neural models, dictionary-based, etc.) match human semantic judgment on multi-label text classification tasks.

**Key Principles:**
1. **Corpus-agnostic:** Works with any text corpus and topic framework
2. **Multi-label first:** Evaluates pattern matching, not just top-1 accuracy
3. **Token-efficient:** Designed for LLM evaluation with output limits
4. **Quality-stratified:** Samples across content quality spectrum

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

Example:
```csv
chunk_id,raw_text,bertje_topic1,bertje_topic2,bertje_topic3,cosine_topic1,cosine_topic2,cosine_topic3
abc123,"text here...",0.85,0.42,0.13,1.25,0.67,0.22
```

**3. Quality Scores (Optional)**

If available, include a column indicating content quality or confidence:
```
chunk_id,text,quality_score,classifier1_scores...
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

# Load predictions
df = pd.read_csv('predictions.csv')

# Identify columns
text_column = 'raw_text'  # or 'text', 'content', etc.
id_column = 'chunk_id'    # or 'id', 'doc_id', etc.

# List all classifiers and topics
classifiers = ['bertje', 'cosine']  # Adjust based on your data
topics = ['topic1', 'topic2', 'topic3', 'topic4']  # From framework

# Check data
print(f"Total chunks: {len(df)}")
print(f"Classifiers: {classifiers}")
print(f"Topics: {topics}")
```

---

#### STEP 0.2: Quality Stratification

**If quality scores available:**

```python
# Example: Using cosine max score as quality proxy
df['quality_score'] = df[[f'cosine_{topic}' for topic in topics]].max(axis=1)

# Define quality tiers
def assign_tier(score):
    if score >= 1.5: return 'Core'
    elif score >= 1.0: return 'Moderate'
    elif score >= 0.5: return 'Weak'
    elif score >= 0.25: return 'Context'
    else: return 'Noise'

df['tier'] = df['quality_score'].apply(assign_tier)

# Stratified sample: 5 per tier
sample = df.groupby('tier', group_keys=False).apply(
    lambda x: x.sample(min(5, len(x)), random_state=42)
)
```

**If no quality scores:**

```python
# Random sample
sample = df.sample(25, random_state=42)
```

---

#### STEP 0.3: Save Sample

```python
# Save stratified sample for evaluation
sample.to_csv('evaluation_sample.csv', index=False)

print(f"Sample size: {len(sample)}")
print(f"Tier distribution:\n{sample['tier'].value_counts()}")
```

**Output Example:**
```
Sample size: 25
Tier distribution:
Core        5
Moderate    5
Weak        5
Context     5
Noise       5
```

---

### PHASE 1: SEMANTIC EVALUATION (Ground Truth)

**Goal:** Rate each chunk on ALL topics independently (0-3 scale) WITHOUT looking at classifier predictions

**Token Management:** Split into multiple files to avoid output limits

**File Structure:**
- `STEP1_SEMANTIC_EVAL_chunks1-10.md` (first batch)
- `STEP1_SEMANTIC_EVAL_chunks11-20.md` (second batch)
- `STEP1_SEMANTIC_EVAL_chunks21-25.md` (final batch)
- `STEP1_COMPLETE_SUMMARY.md` (aggregated results)

---

#### STEP 1.1: Read Topic Framework

**Before starting evaluation, thoroughly read the topic framework document.**

For each topic, note:
- Core definition
- Key indicators
- Boundary cases (what's NOT included)

---

#### STEP 1.2: Semantic Rating Scale

**For EACH topic, rate 0-3:**

| Rating | Label | Definition | When to Use |
|--------|-------|------------|-------------|
| **0** | Absent | Topic not discussed | No mention or tangential only |
| **1** | Weak | Minor/contextual presence | Mentioned but not developed |
| **2** | Moderate | Clear secondary theme | Discussed but not central |
| **3** | Strong | Central/primary theme | Core focus of text |

**Critical Rules:**
1. **Rate ALL topics independently** - don't force a choice
2. **Read full text BEFORE rating** - don't rate based on keywords alone
3. **DO NOT look at classifier predictions** until Step 2
4. **Multiple topics can have rating ≥2** - multi-label is expected

---

#### STEP 1.3: Evaluation Template (Per Chunk)

```markdown
## CHUNK [N]: [chunk_id] - "[brief description]"

**Text summary:** [2-3 sentence summary of what text discusses]

**Semantic Ratings:**

| Topic | Rating | Brief Rationale |
|-------|--------|-----------------|
| [Topic 1] | [0-3] | [Why this rating?] |
| [Topic 2] | [0-3] | [Why this rating?] |
| [Topic 3] | [0-3] | [Why this rating?] |
| [Topic 4] | [0-3] | [Why this rating?] |

**Primary topic:** [Highest rated topic, or "TIE" if multiple topics = highest]
**Present topics (≥2):** [List all topics rated ≥2]
**Multi-topic?** [Yes/No - if ≥2 topics rated ≥2]
**Difficulty:** [1=Easy, 2=Medium, 3=Hard - subjective assessment]

**Notes:** [Any ambiguities, boundary cases, or interesting observations]

---
```

---

#### STEP 1.4: Batch Processing (Token Management)

**Process in batches of 10 chunks maximum per file.**

**Instructions for AI:**
```
Please evaluate chunks [N] through [M] using the semantic evaluation template.

For each chunk:
1. Read the full text from the dataset
2. Rate all [X] topics independently (0-3 scale)
3. Do NOT look at classifier predictions yet
4. Save results to: STEP1_SEMANTIC_EVAL_chunks[N]-[M].md

Then proceed to the next batch.
```

**After all batches complete:** Create summary file.

---

#### STEP 1.5: Create Summary File

After completing all batches, aggregate results:

**File:** `STEP1_COMPLETE_SUMMARY.md`

```markdown
# STEP 1 COMPLETE: SEMANTIC EVALUATION SUMMARY

## Semantic Ground Truth Results ([N] Chunks)

### Topic Distribution

| Topic | Primary (3/3) | Secondary (2/3) | Weak (1/3) | Absent (0/3) |
|-------|---------------|-----------------|------------|--------------|
| [Topic 1] | X/N (%) | X/N (%) | X/N (%) | X/N (%) |
| [Topic 2] | X/N (%) | X/N (%) | X/N (%) | X/N (%) |
| ... | ... | ... | ... | ... |

### Multi-Topic Analysis

- **Single-topic chunks:** X/N (%) - only 1 topic rated ≥2
- **Multi-topic chunks:** X/N (%) - 2+ topics rated ≥2
- **No clear topic:** X/N (%) - all topics rated <2

### Co-Occurrence Patterns

| Topic 1 | Topic 2 | Frequency | Notes |
|---------|---------|-----------|-------|
| [Topic A] | [Topic B] | X chunks | [Common pattern] |
| ... | ... | ... | ... |

### Quality Distribution

| Tier | N Chunks | Avg Topics Present | Multi-Topic % |
|------|----------|-------------------|---------------|
| Core | X | X.X | XX% |
| ... | ... | ... | ... |

---

## Files Created

1. STEP1_SEMANTIC_EVAL_chunks1-10.md
2. STEP1_SEMANTIC_EVAL_chunks11-20.md
3. ...
4. STEP1_COMPLETE_SUMMARY.md (this file)

**Ready for Step 2:** Classifier performance evaluation
```

---

### PHASE 2: MULTI-LABEL PATTERN EVALUATION

**Goal:** Compare each classifier's score patterns to semantic rating patterns

**Token Management:** One file per classifier (+ final comparison)

---

#### STEP 2.1: Per-Classifier Threshold Analysis

**For each classifier, determine optimal thresholds.**

**File:** `STEP2_[CLASSIFIER]_MULTILABEL_EVALUATION.md`

```markdown
# STEP 2: [CLASSIFIER NAME] Multi-Label Evaluation

## Methodology

Evaluating [CLASSIFIER] as multi-label classifier:
- **Semantic ground truth:** Present if rating ≥2
- **Classifier prediction:** Test multiple thresholds to find optimal

## Threshold Testing

### Fixed Threshold Analysis

Test thresholds: [0.3, 0.4, 0.5, 0.6, 0.7]

For each threshold, calculate:
- True Positives: Predicted present AND semantic ≥2
- False Positives: Predicted present BUT semantic <2
- False Negatives: Predicted absent BUT semantic ≥2
- True Negatives: Predicted absent AND semantic <2

| Threshold | TP | FP | FN | TN | Precision | Recall | F1 |
|-----------|----|----|----|----|-----------|--------|-----|
| 0.3 | X | X | X | X | 0.XX | 0.XX | 0.XX |
| 0.4 | X | X | X | X | 0.XX | 0.XX | 0.XX |
| **0.5** | X | X | X | X | **0.XX** | **0.XX** | **0.XX** |
| 0.6 | X | X | X | X | 0.XX | 0.XX | 0.XX |
| 0.7 | X | X | X | X | 0.XX | 0.XX | 0.XX |

**Optimal fixed threshold:** [X.X] (highest F1)
```

---

#### STEP 2.2: Adaptive Threshold Analysis

**Test if quality-stratified thresholds perform better.**

```markdown
## Adaptive Threshold Analysis

### Hypothesis
Content quality affects optimal threshold:
- High-quality content → Higher threshold (reduce FP)
- Low-quality content → Lower threshold (capture weak signals)

### Tested Strategy

| Quality Tier | Threshold | Rationale |
|--------------|-----------|-----------|
| Core/Moderate (≥1.0) | 0.65-0.75 | Strong signals, reduce false positives |
| Weak/Context (0.25-1.0) | 0.50 | Balanced threshold |
| Noise (<0.25) | 0.30-0.40 | Weak signals, capture presence |

### Results

| Chunk | Tier | Threshold Used | Predicted Present | Semantic Present | Match? |
|-------|------|----------------|-------------------|------------------|--------|
| 1 | Core | 0.70 | [Topics] | [Topics] | [✅/⚠️/❌] |
| ... | ... | ... | ... | ... | ... |

**Adaptive threshold performance:**
- Perfect matches: X/N (%)
- Partial matches: X/N (%)
- Complete misses: X/N (%)

**Comparison:**
- Fixed threshold (0.5): X/N (%) perfect matches
- Adaptive threshold: X/N (%) perfect matches
- **Improvement:** +X percentage points
```

---

#### STEP 2.3: Per-Topic Multi-Label Metrics

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
  - Chunk X: [Brief explanation]
  - Chunk Y: [Brief explanation]
- **False Negatives (present but not predicted):**
  - Chunk Z: [Brief explanation]

**Observations:** [Pattern in errors?]

---

### [Topic 2 Name]
[Repeat structure]

---

## Overall Multi-Label Performance

**Macro-averaged metrics:**
- Precision: (Topic1_P + Topic2_P + ... + TopicN_P) / N = 0.XX
- Recall: (Topic1_R + Topic2_R + ... + TopicN_R) / N = 0.XX
- F1: (Topic1_F1 + Topic2_F1 + ... + TopicN_F1) / N = **0.XX**

**Micro-averaged metrics:**
- Precision: Total_TP / (Total_TP + Total_FP) = 0.XX
- Recall: Total_TP / (Total_TP + Total_FN) = 0.XX
- F1: 0.XX
```

---

#### STEP 2.4: Ranking Correlation Analysis

```markdown
## Ranking Correlation Analysis

### Methodology

For each chunk, calculate Spearman correlation between:
- Semantic ratings [0, 1, 2, 3] for all topics
- Classifier scores [continuous] for all topics

**Spearman correlation** measures if relative ranking matches (not absolute values).

### Results by Quality Tier

| Tier | Mean Correlation | Std Dev | N Chunks |
|------|-----------------|---------|----------|
| Core (≥1.5) | 0.XX | 0.XX | X |
| Moderate (1.0-1.5) | 0.XX | 0.XX | X |
| Weak (0.5-1.0) | 0.XX | 0.XX | X |
| Context (0.25-0.5) | 0.XX | 0.XX | X |
| Noise (<0.25) | 0.XX | 0.XX | X |
| **Overall** | **0.XX** | **0.XX** | **N** |

### Example Cases

**High Correlation (>0.90):**
- Chunk X: Semantic [3,2,0,0], Scores [0.92,0.81,0.23,0.15] → Corr=0.95 ✅

**Medium Correlation (0.70-0.90):**
- Chunk Y: Semantic [2,2,1,0], Scores [0.67,0.63,0.42,0.18] → Corr=0.80 ⚠️

**Low Correlation (<0.70):**
- Chunk Z: Semantic [0,1,0,3], Scores [0.45,0.52,0.38,0.41] → Corr=0.40 ❌
- **Issue:** Ranking inverted (predicted Topic2 highest but semantic is Topic4)

### Correlation as Confidence Metric

| Correlation | Confidence Level | Recommendation |
|-------------|------------------|----------------|
| ≥0.85 | High | Auto-approve |
| 0.70-0.85 | Medium | Batch review |
| 0.50-0.70 | Low | Individual review |
| <0.50 | Very Low | Likely incorrect |
```

---

#### STEP 2.5: Classifier Summary

```markdown
## [CLASSIFIER NAME] Summary

### Strengths
- ✅ [Topic X]: Excellent performance (F1 0.XX)
- ✅ High-quality content: Mean correlation 0.XX
- ✅ [Other strength]

### Weaknesses
- ❌ [Topic Y]: Poor performance (F1 0.XX)
- ❌ Low-quality content: Mean correlation 0.XX
- ❌ [Other weakness]

### Recommended Configuration
- **Threshold strategy:** [Fixed/Adaptive]
- **Optimal thresholds:** [Values by tier]
- **Confidence calibration:** Use correlation >0.XX for high confidence
- **Expected performance:** Multi-label F1 = 0.XX

### Priority Improvements
1. [Specific issue] → [Recommended fix]
2. [Specific issue] → [Recommended fix]
```

---

### PHASE 3: COMPARATIVE ANALYSIS (If Multiple Classifiers)

**Goal:** Compare classifiers head-to-head

**File:** `STEP3_COMPARATIVE_ANALYSIS.md`

---

#### STEP 3.1: Head-to-Head Performance

```markdown
# STEP 3: Comparative Analysis

## Overall Performance Comparison

| Metric | [Classifier 1] | [Classifier 2] | Winner |
|--------|----------------|----------------|--------|
| **Multi-label F1 (macro)** | 0.XX | 0.XX | [Name] |
| Multi-label F1 (micro) | 0.XX | 0.XX | [Name] |
| Mean correlation | 0.XX | 0.XX | [Name] |
| Perfect pattern matches | X/N (%) | X/N (%) | [Name] |

## Per-Topic Comparison

| Topic | [Classifier 1] F1 | [Classifier 2] F1 | Best Method |
|-------|-------------------|-------------------|-------------|
| [Topic 1] | 0.XX | 0.XX | [Name] |
| [Topic 2] | 0.XX | 0.XX | [Name] |
| ... | ... | ... | ... |

## Disagreement Analysis

Chunks where classifiers disagree on primary topic:

| Chunk | Semantic Primary | [C1] Prediction | [C2] Prediction | Winner |
|-------|------------------|-----------------|-----------------|--------|
| X | [Topic] (rating 3) | [Topic A] ❌ | [Topic B] ✅ | C2 |
| Y | [Topic] (rating 3) | [Topic C] ✅ | [Topic D] ❌ | C1 |
| ... | ... | ... | ... | ... |

**Disagreement patterns:**
- [Pattern 1]: [Classifier X] better on [condition]
- [Pattern 2]: [Classifier Y] better on [condition]
```

---

#### STEP 3.2: Complementary Strengths Analysis

```markdown
## Complementary Strengths

### Where Classifiers Excel Differently

**[Classifier 1] Advantages:**
- [Topic/condition]: F1 0.XX vs 0.XX
- [Topic/condition]: F1 0.XX vs 0.XX

**[Classifier 2] Advantages:**
- [Topic/condition]: F1 0.XX vs 0.XX
- [Topic/condition]: F1 0.XX vs 0.XX

### Ensemble Potential

**Topic-specific routing:**
```python
def route_by_topic(text, scores_c1, scores_c2):
    # Use best classifier per topic
    routing = {
        'topic1': 'classifier1',  # Better F1
        'topic2': 'classifier2',  # Better F1
        'topic3': 'classifier1',
        'topic4': 'classifier2'
    }

    ensemble_scores = {}
    for topic, best_classifier in routing.items():
        if best_classifier == 'classifier1':
            ensemble_scores[topic] = scores_c1[topic]
        else:
            ensemble_scores[topic] = scores_c2[topic]

    return ensemble_scores
```

**Weighted averaging:**
```python
def weighted_ensemble(scores_c1, scores_c2, weights):
    # weights = {topic: (w1, w2), ...}
    ensemble = {}
    for topic in scores_c1.keys():
        w1, w2 = weights[topic]
        ensemble[topic] = w1 * scores_c1[topic] + w2 * scores_c2[topic]
    return ensemble
```

**Expected ensemble performance:** F1 = 0.XX (improvement of +X.XX over best single classifier)
```

---

### PHASE 4: FINAL RECOMMENDATIONS

**Goal:** Actionable recommendations for deployment

**File:** `STEP4_FINAL_RECOMMENDATIONS.md`

---

```markdown
# STEP 4: Final Recommendations and Deployment Guide

## Executive Summary

### Performance Summary

| Classifier | Multi-Label F1 | Ranking Correlation | Recommended Use |
|------------|----------------|---------------------|-----------------|
| [Name 1] | 0.XX | 0.XX | [Primary/Secondary/Ensemble] |
| [Name 2] | 0.XX | 0.XX | [Primary/Secondary/Ensemble] |

### Key Findings

1. **Multi-label vs single-label:** [Comparison - how much better is multi-label?]
2. **Quality stratification:** [How does performance vary by content quality?]
3. **Topic-specific patterns:** [Which topics are easiest/hardest?]
4. **Optimal thresholds:** [Fixed vs adaptive - which works better?]

---

## Production Configuration

### Recommended System Architecture

**Primary Classifier:** [Name]
- Multi-label F1: 0.XX
- Configuration: [Adaptive/fixed thresholds]

**Threshold Configuration:**

```python
THRESHOLDS = {
    'high_quality': {  # quality_score ≥ 1.0
        'topic1': 0.XX,
        'topic2': 0.XX,
        ...
    },
    'medium_quality': {  # 0.25 ≤ quality_score < 1.0
        'topic1': 0.XX,
        'topic2': 0.XX,
        ...
    },
    'low_quality': {  # quality_score < 0.25
        'topic1': 0.XX,
        'topic2': 0.XX,
        ...
    }
}
```

### Prediction Workflow

```python
def predict_topics(text, classifier, quality_score):
    # 1. Get scores for all topics
    scores = classifier.predict(text)

    # 2. Determine quality tier
    if quality_score >= 1.0:
        tier = 'high_quality'
    elif quality_score >= 0.25:
        tier = 'medium_quality'
    else:
        tier = 'low_quality'

    # 3. Apply adaptive thresholds
    thresholds = THRESHOLDS[tier]
    present_topics = []

    for topic, score in scores.items():
        if score >= thresholds[topic]:
            present_topics.append({
                'topic': topic,
                'score': score,
                'confidence': get_confidence(score, quality_score)
            })

    # 4. Calculate ranking correlation (for confidence)
    correlation = calculate_pattern_quality(scores)

    # 5. Return multi-label output
    return {
        'topics': sorted(present_topics, key=lambda x: x['score'], reverse=True),
        'quality_score': quality_score,
        'pattern_correlation': correlation,
        'confidence': determine_confidence(correlation, quality_score)
    }
```

---

## Confidence Calibration

### Confidence Levels

| Level | Criteria | Expected Accuracy | Action |
|-------|----------|-------------------|--------|
| **High** | Correlation ≥0.85 AND quality ≥1.0 | 90-95% | Auto-approve |
| **Medium** | Correlation ≥0.70 OR quality ≥0.5 | 75-85% | Batch review |
| **Low** | Correlation <0.70 AND quality <0.5 | 50-70% | Individual review |
| **Reject** | Quality <0.20 AND all scores <0.25 | N/A | Mark as non-relevant |

### Example Output

```json
{
  "chunk_id": "abc123",
  "topics": [
    {"topic": "topic1", "score": 0.87, "confidence": "high"},
    {"topic": "topic3", "score": 0.62, "confidence": "medium"}
  ],
  "quality_score": 1.23,
  "pattern_correlation": 0.91,
  "overall_confidence": "high",
  "recommendation": "auto_approve"
}
```

---

## Quality Assurance Workflow

### Human Review Strategy

**Auto-approve (70% of cases):**
- High confidence predictions
- Expected accuracy: 90-95%
- No human review needed

**Batch review (25% of cases):**
- Medium confidence predictions
- Group by topic for efficient review
- Domain expert reviews batches weekly

**Individual review (5% of cases):**
- Low confidence predictions
- Complex multi-topic cases
- Requires detailed examination

**Rejection zone (<1% of cases):**
- Very low quality content
- All topic scores below minimum threshold
- Mark as "not applicable" or "other"

---

## Improvement Priorities

### Short-term (Immediate Implementation)

**Priority 1: Implement Adaptive Thresholds** ⚠️ HIGH IMPACT
- Current: Fixed threshold (suboptimal)
- Target: Quality-based thresholds
- Expected improvement: +X% perfect matches

**Priority 2: Multi-label Output** ⚠️ HIGH IMPACT
- Current: [Single-label/other limitation]
- Target: Output all topics above threshold
- Expected improvement: Better reflects reality (X% of texts are multi-topic)

**Priority 3: Confidence Indicators** ⚠️ MEDIUM IMPACT
- Add correlation-based confidence scores
- Enable efficient human review prioritization

### Medium-term (Model/Dictionary Improvements)

**[Classifier-specific recommendations based on errors found]**

**Example:**
- [Topic X]: Low recall (F1 0.XX) → Need more training data/dictionary terms for [specific pattern]
- [Topic Y]: High false positives → Reduce weight on generic terms like [examples]

### Long-term (System Evolution)

1. **Expand evaluation sample** (25 → 100+ chunks for stable metrics)
2. **Ensemble system** (if multiple classifiers available)
3. **Active learning** (use low-confidence predictions for model improvement)
4. **Continuous evaluation** (monthly re-evaluation on new data)

---

## Deployment Checklist

- [ ] Configure adaptive thresholds for production environment
- [ ] Implement multi-label output format
- [ ] Set up confidence-based routing (auto-approve vs review)
- [ ] Create human review interface/workflow
- [ ] Train reviewers on topic framework and edge cases
- [ ] Deploy to [X%] of traffic (gradual rollout)
- [ ] Monitor precision/recall on reviewed samples
- [ ] Iterate on thresholds based on production data

---

## Monitoring Metrics

### Track These Metrics in Production

**Performance Metrics:**
- Multi-label F1 per topic (weekly)
- Ranking correlation distribution (daily)
- Confidence distribution (daily)

**Operational Metrics:**
- % auto-approved (target: 70%)
- % requiring review (target: 30%)
- Human review turnaround time
- Inter-rater agreement (between human reviewers)

**Quality Metrics:**
- Precision/recall on reviewed samples
- False positive rate per topic
- False negative rate per topic
- User feedback on incorrect predictions

---

## Files Created in This Evaluation

1. STEP1_SEMANTIC_EVAL_chunks[X]-[Y].md (ground truth by batch)
2. STEP1_COMPLETE_SUMMARY.md (semantic ground truth summary)
3. STEP2_[CLASSIFIER]_MULTILABEL_EVALUATION.md (per classifier)
4. STEP3_COMPARATIVE_ANALYSIS.md (if multiple classifiers)
5. STEP4_FINAL_RECOMMENDATIONS.md (this file)

## Methodology Document

See: **METHODOLOGY_MULTILABEL_CLASSIFIER_EVALUATION.md** for replication on new datasets
```

---

## TOKEN MANAGEMENT STRATEGIES

### Problem: LLM Output Token Limits

Evaluating 25+ chunks with detailed analysis can exceed output limits (typically 4000-8000 tokens per response).

### Solution: Batch Processing

**Strategy 1: Fixed Batch Sizes**
- Process 10 chunks per file
- Create multiple output files: `STEP1_SEMANTIC_EVAL_chunks1-10.md`, `chunks11-20.md`, etc.
- Final aggregation in summary file

**Strategy 2: Progressive Evaluation**
- Start with high-quality tier (most important)
- Evaluate lower tiers only if token budget allows
- Minimum viable: 15 chunks (3 per tier)

**Strategy 3: Condensed Format**
- For chunks with clear single topic, use one-line format:
  ```
  Chunk X: Topic1(3), Topic2(0), Topic3(0), Topic4(0) - [Brief note]
  ```
- Full template only for complex multi-topic cases

### File Size Guidelines

| File Type | Max Chunks | Approx Tokens |
|-----------|------------|---------------|
| Semantic evaluation | 10 | 3000-4000 |
| Classifier evaluation | 25 | 6000-8000 |
| Comparative analysis | All | 4000-6000 |
| Recommendations | All | 3000-4000 |

**Total evaluation:** 5-7 files for 25-50 chunk sample

---

## QUALITY CONTROL

### Inter-Evaluator Agreement (Optional)

If multiple evaluators available:

1. **Overlap sample:** 10% of chunks rated by 2+ evaluators
2. **Calculate Cohen's Kappa:** Agreement on ≥2 threshold (present/absent)
3. **Acceptable:** κ ≥ 0.70
4. **If low agreement:** Refine topic definitions, provide examples

### Common Evaluation Pitfalls

**❌ DON'T:**
- Rate based on keywords alone (read full context)
- Look at classifier predictions before rating (confirmation bias)
- Force single topic (multi-topic is expected)
- Assume 0 is default (actively decide 0 vs 1 vs 2 vs 3)

**✅ DO:**
- Read entire text before rating
- Consider topic definitions from framework
- Rate all topics independently
- Note ambiguities and difficult cases
- Take breaks (evaluation fatigue affects quality)

---

## ADAPTATION GUIDE

### For Different Topic Numbers

**3 topics:** Easier - use simpler confusion matrices
**5-6 topics:** Standard - follow methodology as written
**7+ topics:** Consider grouping related topics or hierarchical evaluation

### For Different Text Lengths

**Short texts (<100 words):**
- May have clearer single topics
- Less multi-topic complexity
- Can evaluate more per batch (15-20 chunks)

**Long texts (>500 words):**
- More likely multi-topic
- May need section-level evaluation
- Evaluate fewer per batch (5-8 chunks)

### For Different Languages

- Translate topic framework to target language
- Use native speaker evaluators
- Consider language-specific patterns (idioms, formal registers)

### For Domain-Specific Corpora

- Include domain glossary in topic framework
- Provide domain-specific examples
- May need domain expert evaluators

---

## REPLICATION INSTRUCTIONS

### To Use This Methodology on New Dataset:

1. **Prepare inputs:**
   - Create `TOPIC_FRAMEWORK.md` defining your topics
   - Prepare `predictions.csv` with classifier scores
   - (Optional) Calculate quality scores for stratification

2. **Run Phase 0 (Sampling):**
   - Execute code in Step 0.1-0.3
   - Generate `evaluation_sample.csv`

3. **Run Phase 1 (Semantic Evaluation):**
   - Read topic framework thoroughly
   - Evaluate in batches (10 chunks per file)
   - Create `STEP1_SEMANTIC_EVAL_chunks[X]-[Y].md` files
   - Aggregate in `STEP1_COMPLETE_SUMMARY.md`

4. **Run Phase 2 (Classifier Evaluation):**
   - For each classifier, create `STEP2_[NAME]_MULTILABEL_EVALUATION.md`
   - Test fixed and adaptive thresholds
   - Calculate per-topic metrics
   - Compute ranking correlations

5. **Run Phase 3 (Comparison):** (if multiple classifiers)
   - Create `STEP3_COMPARATIVE_ANALYSIS.md`
   - Head-to-head comparison
   - Identify complementary strengths

6. **Run Phase 4 (Recommendations):**
   - Create `STEP4_FINAL_RECOMMENDATIONS.md`
   - Production configuration
   - Deployment checklist

---

## APPENDIX: CODE TEMPLATES

### A. Stratified Sampling

```python
import pandas as pd
import numpy as np

def create_stratified_sample(df, quality_col, n_per_tier=5, random_state=42):
    """
    Create quality-stratified sample for evaluation.

    Args:
        df: DataFrame with predictions
        quality_col: Column name with quality scores
        n_per_tier: Number of samples per quality tier
        random_state: Random seed for reproducibility

    Returns:
        DataFrame with stratified sample
    """
    # Define tiers
    def assign_tier(score):
        if score >= 1.5: return 'Core'
        elif score >= 1.0: return 'Moderate'
        elif score >= 0.5: return 'Weak'
        elif score >= 0.25: return 'Context'
        else: return 'Noise'

    df['tier'] = df[quality_col].apply(assign_tier)

    # Stratified sample
    sample = df.groupby('tier', group_keys=False).apply(
        lambda x: x.sample(min(n_per_tier, len(x)), random_state=random_state)
    )

    return sample.sort_values('tier')
```

### B. Multi-Label Metrics Calculation

```python
from sklearn.metrics import precision_recall_fscore_support

def calculate_multilabel_metrics(semantic_ratings, predictions, threshold, topics):
    """
    Calculate per-topic precision, recall, F1 for multi-label classification.

    Args:
        semantic_ratings: Dict {chunk_id: {topic: rating_0_to_3}}
        predictions: Dict {chunk_id: {topic: score}}
        threshold: Float or Dict {topic: threshold}
        topics: List of topic names

    Returns:
        Dict {topic: {'precision': X, 'recall': X, 'f1': X}}
    """
    results = {}

    for topic in topics:
        y_true = []
        y_pred = []

        for chunk_id in semantic_ratings.keys():
            # Ground truth: present if rating ≥2
            y_true.append(1 if semantic_ratings[chunk_id][topic] >= 2 else 0)

            # Prediction: present if score ≥ threshold
            if isinstance(threshold, dict):
                thresh = threshold[topic]
            else:
                thresh = threshold

            y_pred.append(1 if predictions[chunk_id][topic] >= thresh else 0)

        # Calculate metrics
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true, y_pred, average='binary', zero_division=0
        )

        results[topic] = {
            'precision': precision,
            'recall': recall,
            'f1': f1
        }

    # Macro-averaged F1
    macro_f1 = np.mean([metrics['f1'] for metrics in results.values()])
    results['macro_avg'] = {'f1': macro_f1}

    return results
```

### C. Ranking Correlation

```python
from scipy.stats import spearmanr

def calculate_ranking_correlation(semantic_ratings, predictions, topics):
    """
    Calculate Spearman correlation between semantic ratings and classifier scores.

    Args:
        semantic_ratings: Dict {chunk_id: {topic: rating_0_to_3}}
        predictions: Dict {chunk_id: {topic: score}}
        topics: List of topic names

    Returns:
        Dict {chunk_id: correlation}
    """
    correlations = {}

    for chunk_id in semantic_ratings.keys():
        semantic_vector = [semantic_ratings[chunk_id][t] for t in topics]
        prediction_vector = [predictions[chunk_id][t] for t in topics]

        # Spearman correlation
        corr, _ = spearmanr(semantic_vector, prediction_vector)
        correlations[chunk_id] = corr if not np.isnan(corr) else 0.0

    return correlations
```

### D. Adaptive Threshold Optimization

```python
def optimize_adaptive_thresholds(semantic_ratings, predictions, quality_scores, topics):
    """
    Find optimal adaptive thresholds by quality tier.

    Args:
        semantic_ratings: Dict {chunk_id: {topic: rating_0_to_3}}
        predictions: Dict {chunk_id: {topic: score}}
        quality_scores: Dict {chunk_id: quality_score}
        topics: List of topic names

    Returns:
        Dict {tier: {topic: optimal_threshold}}
    """
    # Group chunks by tier
    tiers = {'high': [], 'medium': [], 'low': []}
    for chunk_id, score in quality_scores.items():
        if score >= 1.0:
            tiers['high'].append(chunk_id)
        elif score >= 0.25:
            tiers['medium'].append(chunk_id)
        else:
            tiers['low'].append(chunk_id)

    optimal_thresholds = {}

    for tier, chunk_ids in tiers.items():
        if not chunk_ids:
            continue

        tier_thresholds = {}

        for topic in topics:
            best_f1 = 0
            best_threshold = 0.5

            # Test thresholds from 0.2 to 0.8
            for threshold in np.arange(0.2, 0.85, 0.05):
                y_true = [1 if semantic_ratings[cid][topic] >= 2 else 0
                         for cid in chunk_ids]
                y_pred = [1 if predictions[cid][topic] >= threshold else 0
                         for cid in chunk_ids]

                _, _, f1, _ = precision_recall_fscore_support(
                    y_true, y_pred, average='binary', zero_division=0
                )

                if f1 > best_f1:
                    best_f1 = f1
                    best_threshold = threshold

            tier_thresholds[topic] = best_threshold

        optimal_thresholds[tier] = tier_thresholds

    return optimal_thresholds
```

---

## VERSION HISTORY

**v1.0 (2025-12-03)**
- Initial methodology document
- Based on Dutch Caribbean slavery legacy evaluation
- Validated on 25-chunk stratified sample
- Multi-label evaluation with adaptive thresholds
- Ranking correlation analysis

**Future versions:**
- Add support for hierarchical topics
- Include active learning workflow
- Add inter-rater agreement protocols
- Expand to multi-language evaluation

---

## LICENSE & CITATION

This methodology is released under [LICENSE TYPE].

**Citation:**
```
Multi-Label Classifier Evaluation Protocol v1.0 (2025)
Developed for Dutch Caribbean Slavery Legacy Project
```

**Acknowledgments:**
- Based on evaluation of BERTJE neural model and Cosine dictionary method
- Evaluated 25 stratified policy document chunks
- Achieved 0.81 multi-label F1 (BERTJE) vs 0.76 previous single-label accuracy

---

## CONTACT

For questions, improvements, or adaptations of this methodology:
[Contact information]

**Recommended Use Cases:**
- Multi-label text classification evaluation
- Policy document classification
- Topic modeling validation
- Classifier comparison studies
- Production deployment readiness assessment
