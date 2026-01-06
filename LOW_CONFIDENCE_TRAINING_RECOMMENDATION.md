# Should You Feed BERTJE Low Confidence Cosine Chunks?

## Quick Answer: **YES, but SELECTIVELY**

Low/none confidence chunks represent **84.3% of your data** (3,249 out of 3,854 chunks). Excluding them entirely would severely limit your training data and miss important patterns.

---

## What Low/None Confidence Chunks Actually Represent

### Distribution:
- **None confidence**: 1,556 chunks (40.4%) - Margin < 0.025
- **Low confidence**: 1,693 chunks (43.9%) - Margin 0.025-0.050
- **High confidence**: 605 chunks (15.7%) - Margin > 0.050

### Key Characteristics:

| Confidence | Avg Margin | Avg Max Score | Score Std | Agreement with BERTJE |
|-----------|-----------|---------------|-----------|----------------------|
| **High** | 0.095 | 0.462 | 0.071 | 97.0% |
| **Low** | 0.043 | 0.376 | 0.047 | 85.1% |
| **None** | 0.009 | 0.356 | 0.036 | **51.2%** |

### What This Means:

**Low confidence (margin 0.025-0.050)**:
- Score std: 0.047 (moderate differentiation)
- Scores like: EDUC:0.30, GOV:0.37, ECON:0.42, SOC:0.40
- **These are genuinely multi-topic chunks** (2-3 topics present)
- BERTJE agrees 85% of the time
- **VALUABLE for training** - teach multi-topic patterns

**None confidence (margin < 0.025)**:
- Score std: 0.036 (very flat)
- Scores like: EDUC:0.35, GOV:0.35, ECON:0.40, SOC:0.38
- **Mix of**:
  - True multi-topic (3-4 topics equally present)
  - Administrative noise (no clear topic)
  - Ambiguous content
- BERTJE only agrees 51% - these are genuinely hard
- **MIXED VALUE for training** - some useful, some noise

---

## Current Problem: You're Only Training on 15.7% of Data

If you exclude low/none confidence, you only train on **605 high-confidence chunks**.

### Issues with High-Only Training:

1. **Severe sample size reduction** (3,854 → 605 = -84%)
2. **Selection bias** - Only learning single-topic chunks
3. **Won't learn multi-topic patterns** (most policy documents are multi-topic!)
4. **BERTJE's main weakness** (score compression) likely CAUSED by this

### Why BERTJE Compresses Scores:

Looking at your current training data distribution:
- High confidence (clear single topic): 15.7% of training data
- Low confidence (2-3 topics): 43.9% of training data
- None confidence (flat/ambiguous): 40.4% of training data

**BERTJE learned**: "Most chunks have multiple topics with similar scores"
**Result**: Model defaults to giving everything 25-40% scores (compressed distribution)

This is actually **correct behavior** given the training distribution!

---

## Recommendations for Training Data Selection

### STRATEGY 1: **Stratified Sampling by Confidence** ✓ RECOMMENDED

Include ALL confidence levels but weight them appropriately:

```python
# Recommended training data composition
training_data = {
    'high_confidence': 40%,      # Up from 15.7% (oversample)
    'low_confidence': 40%,       # Down from 43.9%
    'none_confidence': 20%       # Down from 40.4% (undersample)
}
```

**Rationale**:
- **High confidence** (40%): Teach clear single-topic patterns, enable high scores (70-90%)
- **Low confidence** (40%): Teach genuine multi-topic patterns (needed for policy docs!)
- **None confidence** (20%): Teach extreme multi-topic and low-confidence scoring

**Benefits**:
- Maintains sample size
- Teaches both single-topic and multi-topic patterns
- Reduces compression bias (more high-confidence examples)
- Still learns multi-topic detection (low-confidence examples)

---

### STRATEGY 2: **Selective Filtering of None Confidence** ✓ ALSO GOOD

Keep all high + low, but filter none confidence:

```python
# Include based on BERTJE agreement
include_if = {
    'high_confidence': 'all',           # 605 chunks (100%)
    'low_confidence': 'all',            # 1,693 chunks (100%)
    'none_confidence': 'bertje_agrees'  # ~800 chunks (51% of 1,556)
}

# Total: 605 + 1,693 + 800 = 3,098 chunks (80% of original)
```

**Rationale**:
- High + low gives you good coverage (60% of data)
- From none confidence, only include chunks where BERTJE agrees with cosine
  - Agreement suggests there IS signal despite flat scores
  - Disagreement suggests pure noise or mislabeling

**Benefits**:
- Removes likely noise (none confidence + disagreement)
- Keeps genuinely difficult multi-topic cases (none confidence + agreement)
- Still teaches multi-topic patterns

---

### STRATEGY 3: **Augment with Manual Labels** (If Resources Allow)

For none confidence chunks (40% of data):
1. Manually review random sample (100-200 chunks)
2. Identify patterns:
   - True multi-topic (keep with adjusted labels)
   - Administrative noise (exclude or label differently)
   - Mislabeled (relabel)
3. Use patterns to filter/relabel rest

**Most valuable for**: Understanding what "none confidence" actually contains in your specific corpus

---

## Specific Recommendations for Your Case

### Given Your Goal: **Reduce BERTJE Score Compression**

**Root cause identified**: Training data is 84% low/none confidence (flat scores)

**Solution**: **OVERSAMPLE high confidence, UNDERSAMPLE none confidence**

### Recommended Training Mix:

```
Current distribution:
- High:  605 (15.7%)
- Low:  1,693 (43.9%)
- None: 1,556 (40.4%)

Recommended distribution:
- High:  1,500 (40%) ← Oversample by 2.5x (with augmentation or repeat)
- Low:   1,500 (40%) ← Slight undersample
- None:    750 (20%) ← Heavy undersample, only BERTJE-agrees

Total: 3,750 chunks (97% of original data)
```

### How to Oversample High Confidence:

Since you only have 605 high-confidence chunks, you can:

1. **Repeat high-confidence examples** in training (simple but effective)
2. **Augment high-confidence examples**:
   - Paraphrase (if you have resources)
   - Add noise/variations
   - Use back-translation
3. **Lower the threshold slightly**: Include "upper medium" (margin 0.045-0.050) as "high"

---

## What This Will Fix

### Current BERTJE Problems (from analysis):

1. **Score compression** (scores in 20-45% range)
   - **Cause**: 84% of training data has flat scores
   - **Fix**: Increase high-confidence examples from 16% to 40%

2. **Can't give high scores** (maxes at ~48%)
   - **Cause**: Rarely sees examples with 70-90% labels
   - **Fix**: High-confidence chunks have clear dominance to learn from

3. **Can't give low scores** (floors at ~20%)
   - **Cause**: All training examples have all topics present to some degree
   - **Fix**: High-confidence chunks show some topics can be near-zero

### What You'll Preserve:

- Multi-topic detection (keep 40% low confidence)
- Handling ambiguous chunks (keep 20% none confidence)
- Realistic policy document patterns

---

## Implementation Steps

### Step 1: Analyze Your Current Training Data
```python
# Check what you're currently using
current_training = df[df['used_for_training'] == True]
conf_dist = current_training['confidence_level'].value_counts()
print(conf_dist)
```

### Step 2: Create Stratified Sample
```python
# Recommended composition
high_conf = df[df['confidence_level'] == 'high']
low_conf = df[df['confidence_level'] == 'low']
none_conf = df[df['confidence_level'] == 'none']

# Sample none confidence where BERTJE agrees
none_conf_agree = none_conf[none_conf['primary_topic'] == none_conf['bertje_primary_topic']]

# Oversample high (repeat 2.5x)
high_sample = pd.concat([high_conf] * 3, ignore_index=True).sample(n=1500, random_state=42)

# Sample low
low_sample = low_conf.sample(n=1500, random_state=42)

# Sample none (only agreements)
none_sample = none_conf_agree.sample(n=min(750, len(none_conf_agree)), random_state=42)

# Combine
training_data = pd.concat([high_sample, low_sample, none_sample])
```

### Step 3: Verify Distribution
```python
# Check final distribution
print("Training data composition:")
print(f"High confidence: {len(high_sample)} ({len(high_sample)/len(training_data)*100:.1f}%)")
print(f"Low confidence: {len(low_sample)} ({len(low_sample)/len(training_data)*100:.1f}%)")
print(f"None confidence: {len(none_sample)} ({len(none_sample)/len(training_data)*100:.1f}%)")
```

---

## Expected Improvements

### With Stratified Training (40% high, 40% low, 20% none):

**Score compression** → Should improve significantly
- High scores will reach 60-70% (vs current 35-48%)
- Low scores will reach 5-15% (vs current 20-30%)

**Multi-topic detection** → Should maintain or improve
- 60% of training still has multi-topic examples
- Model learns BOTH single and multi-topic patterns

**Overall accuracy** → Should improve from 60-65% to 70-75%

---

## Final Recommendation

### **YES, include low confidence chunks** ✓

They represent **genuine multi-topic content** that policy documents naturally contain.

### **SELECTIVELY include none confidence chunks** ~

Only include where BERTJE agrees (51% of none-confidence chunks). These are genuinely difficult multi-topic cases worth learning from.

### **OVERSAMPLE high confidence chunks** ✓✓ CRITICAL

Current 16% → Target 40% of training data. This will fix the score compression problem.

### Training Data Recipe:
```
✓ High confidence: 1,500 examples (40%) - oversample existing 605
✓ Low confidence:  1,500 examples (40%) - from existing 1,693
~ None confidence:   750 examples (20%) - only where BERTJE agrees
─────────────────────────────────────────────────────────────
  Total:          3,750 examples (97% of original corpus)
```

This balanced approach will teach BERTJE to:
1. Give high scores when appropriate (from high-confidence examples)
2. Give low scores when appropriate (from high-confidence counter-examples)
3. Detect multi-topic content (from low-confidence examples)
4. Handle ambiguous cases (from none-confidence examples)

The current score compression problem is likely **caused by** excluding or underweighting high-confidence examples, so increasing their proportion is the key fix.
