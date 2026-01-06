# Workflow Interaction Analysis: v16 Selection Strategy vs. Transfer Problems

**Date**: 2025-11-27
**Analysis of**: How v16's confidence-based selection strategy interacts with domain transfer challenges

---

## Executive Summary

**Critical Finding**: The current confidence classification system (0.4 threshold + margin requirements) systematically filters out exactly the type of chunks needed for policy corpus transfer: **implicit multi-topic patterns**.

**Key Numbers**:
- **266 chunks (16% of "none confidence")** score moderately across multiple topics (2+ topics >0.3)
- These chunks fail the margin requirement (<0.05) despite having reasonable relevance
- Current sampling heavily downsamples these chunks (50% removal in "none confidence" category)
- Yet these are precisely the **implicit patterns** likely to appear in policy documents

**Recommendation**: The 8-dimensional restructure could enable separate confidence criteria that capture implicit patterns WITHOUT requiring high single-topic dominance.

---

## Current v16 Confidence Classification System

### The Thresholds (from v15 workflow)

```python
HIGH_CONFIDENCE:
  max_score >= 0.40 AND margin >= 0.05

LOW_CONFIDENCE:
  max_score >= 0.20 AND margin >= 0.02

NONE_CONFIDENCE:
  Everything else
```

### Actual v16 Distribution

```
Total chunks: 1,652

Confidence breakdown:
- High:  317 chunks (19.2%)
- Low:   861 chunks (52.1%)
- None:  474 chunks (28.7%)
```

### Statistical Properties

| Confidence | Mean max_score | Std max_score | Mean margin | Std margin |
|-----------|----------------|---------------|-------------|------------|
| High      | 0.462         | 0.040         | 0.100       | 0.038      |
| Low       | 0.352         | 0.067         | 0.058       | 0.035      |
| None      | 0.322         | 0.096         | 0.012       | 0.009      |

**Key observation**: "None confidence" has **very low margins** (mean=0.012) but reasonable max_scores (mean=0.322). These are chunks where multiple topics score similarly.

---

## Score Compression Problem Impact

### Per-Topic Score Ranges (v16)

| Topic        | Min    | Max   | Mean  | Std   |
|--------------|--------|-------|-------|-------|
| Educational  | 0.004  | 0.637 | 0.281 | 0.082 |
| Governance   | -0.031 | 0.553 | 0.293 | 0.091 |
| Economic     | 0.008  | 0.582 | 0.300 | 0.093 |
| Racism       | -0.011 | 0.602 | 0.321 | 0.108 |

**Problems**:
1. **Maximum scores barely exceed 0.6** (Educational: 0.637, Racism: 0.602)
2. **No chunks reach 0.7+** despite v16 evaluation report showing chunks with "strong topic presence"
3. **Score compression limits high-confidence pool**: Only 19.2% of chunks reach >=0.4 threshold

**Implication**: Dictionary doesn't create sufficient differentiation. If truly strong chunks scored 0.7-0.9, margin requirements would be easier to meet.

---

## The Implicit Pattern Problem

### Definition

**Implicit patterns**: Chunks discussing slavery-rooted problems without explicit historical vocabulary.

Example characteristics:
- Multiple problem dimensions present (Educational + Economic)
- Clear Caribbean geographic context
- Contemporary problem vocabulary (onderwijs, werkloosheid)
- **LOW or ABSENT slavery/historical vocabulary** (slavernij, 1863, koloniaal)

### Why Current System Filters Them Out

**Margin requirement assumes single-topic dominance**:
- High confidence needs 0.05+ margin (1st - 2nd topic difference)
- But implicit multi-topic chunks have **small margins by nature**

**Example from v16 data** (chunk #1182):
```
Confidence: NONE (filtered to 50% sampling weight)
Max score: 0.395 (Economic)
Margin: 0.010

All 4 scores:
  Educational: 0.370
  Governance:  0.376
  Economic:    0.395
  Racism:      0.385
```

**Why this happened**: Chunk discusses institutional engagement with slavery research (affects all 4 topics). Cross-contamination from shared geographic/historical terms lifts all scores. Small differences between topics → fails margin requirement → classified "none confidence" → heavily downsampled.

**But**: This could be exactly the type of chunk pattern appearing in policy documents (multi-topic, moderate scores, implicit historical connection).

### Scale of the Problem

**266 chunks (16% of "none confidence", 16% of total corpus)** have:
- 2+ topics scoring >0.30
- Moderate relevance across multiple dimensions
- Failed margin requirements

**Current treatment**: Downsampled to 20% representation (from 28.7% to 20% after stratified sampling).

---

## Domain Transfer Challenge

### The Two Corpora

**Training corpus** (slavery history books/articles):
- **Explicit slavery vocabulary**: slavernij, slavenhandel, 1863, afschaffing, etc.
- **Explicit causal linking**: "onderwijs problemen door koloniaal systeem"
- **Historical framing**: Discusses problems in historical context

**Target corpus** (IDPAD-era policy documents 2015-2024):
- **Minimal slavery vocabulary**: May acknowledge history in introduction, but not throughout
- **Implicit patterns**: Discusses educational problems without saying "caused by slavery"
- **Contemporary framing**: Focuses on current issues, solutions

### What BERTje Needs to Learn

**NOT**: "Find chunks that say 'slavery caused X'"
**INSTEAD**: "Recognize problem patterns that match slavery-rooted signatures"

Example pattern BERTje should learn:
- **Educational problem** (dropout, taalbarrière, onderwijs-achterstand)
- **+ Caribbean context** (Bonaire, Papiamentu, Caribisch Nederland)
- **+ Structural/systemic framing** (not individual failure)
- **= High relevance** (even without "slavernij" mentioned)

### Current System's Mismatch

**Training corpus selection favors**:
- Single-topic dominance (high margin requirement)
- Explicit vocabulary (reaches 0.4+ threshold via historical terms)

**Policy corpus reality**:
- Multi-topic overlap (economic + educational problems intertwined)
- Implicit vocabulary (contemporary problem terms without historical markers)

**Result**: Training on wrong pattern distribution for transfer task.

---

## How Current Stratified Sampling Interacts

### v15 Sampling Strategy

```python
"apply_confidence_sampling": True

Effect:
- High confidence: Oversample (with replacement if needed)
- Low confidence: Sample normally
- None confidence: Downsample to 50%

Result:
- Original: High=24.6%, Low=44.3%, None=31.1%
- After:    High=40%,   Low=40%,   None=20%
```

### v16 Numbers

```
Original:
- High:  317 (19.2%)
- Low:   861 (52.1%)
- None:  474 (28.7%)

After stratified sampling (estimated for ~5000 chunks):
- High:  ~2000 (40%) - oversampled
- Low:   ~2000 (40%) - slightly downsampled
- None:  ~1000 (20%) - heavily downsampled from 28.7% to 20%
```

### Why This Creates Transfer Problems

**1. Oversampling explicit patterns**:
- "High confidence" chunks likely have strong historical vocabulary
- These patterns are LESS representative of policy corpus
- BERTje learns to rely on explicit markers

**2. Undersampling implicit patterns**:
- "None confidence" includes 266 multi-topic moderate chunks
- These are MORE representative of policy corpus patterns
- BERTje sees fewer examples of implicit patterns

**3. Margin requirement bias**:
- Selects for single-topic dominance
- Policy documents often discuss interconnected problems (Educational + Economic)
- BERTje trained on single-topic examples, applied to multi-topic reality

---

## Why 8D Approach Could Help

### The Core Insight

**Current 4D**: Educational, Governance, Economic, Racism (integrated topic + scope)
- Cross-contamination from shared geographic/historical terms
- Margin requirements favor single-topic chunks
- Multi-topic patterns filtered as "noise"

**Proposed 8D**: 4 problem dimensions + 4 context dimensions
- Problems: Educational, Governance, Economic, Racism
- Contexts: Era_Slavery, Era_Modern, Geo_Caribbean, Geo_Dutch
- Separate scoring, composable via multiplication

### Advantage 1: Separate Confidence Criteria for Implicit Patterns

**Example high-confidence implicit pattern** (8D scoring):
```python
Problem_Educational:   0.65  # Strong education vocabulary
Problem_Economic:      0.55  # Strong economic vocabulary
Geo_Caribbean:         0.75  # Clear geographic markers
Era_Modern:            0.70  # Contemporary framing
Era_Slavery:           0.15  # EXPLICITLY LOW on slavery terms

# Composite relevance (multiply dimensions):
Educational_relevance = 0.65 * 0.75 * (0.70 + 0.30*0.15) = 0.37
Economic_relevance    = 0.55 * 0.75 * (0.70 + 0.30*0.15) = 0.31

# Confidence classification (8D approach):
IF (Problem_score >= 0.6) AND
   (Geo_Caribbean >= 0.7) AND
   (Era_Modern >= 0.6) AND
   (Era_Slavery < 0.3):
    → HIGH_CONFIDENCE_IMPLICIT
```

**This chunk would be**:
- **4D system**: "none confidence" (multi-topic moderate scores, low margin)
- **8D system**: "high confidence implicit" (strong problem + context, explicitly modern)

### Advantage 2: Reducing Cross-Contamination

**Current problem**: Geographic terms (curaçao, bonaire) appear in most chunks → lift all 4 topic scores → reduce differentiation

**8D solution**: Geographic terms score only `Geo_Caribbean` dimension
- Educational score based purely on education vocabulary
- Governance score based purely on governance vocabulary
- Cross-contamination eliminated
- Better topic differentiation

**Expected effect**: Score ranges expand (some chunks 0.1-0.2, strong chunks 0.7-0.9) because topics aren't artificially lifted by shared scope terms.

### Advantage 3: Composable Relevance Gradients

**4D problem**: How do you score a chunk about "education AND economic problems in Bonaire"?
- Current: Lift both Educational and Economic scores via shared terms
- Result: Moderate scores on both (0.35, 0.38), fails margin requirement

**8D solution**:
```
Problem_Educational: 0.70
Problem_Economic:    0.65
Geo_Caribbean:       0.80
Era_Modern:          0.75

Educational_relevance = 0.70 * 0.80 * 0.75 = 0.42
Economic_relevance    = 0.65 * 0.80 * 0.75 = 0.39
```

**Result**: Natural relevance gradient through multiplication. Both topics have good composite scores, but Educational slightly higher. No artificial margin requirement needed.

### Advantage 4: Training on Implicit Patterns

**Current workflow** (with 8D):
1. Train BERTje on slavery corpus (learns problem patterns WITH Era_Slavery high)
2. Use encoder to expand dictionaries in policy corpus space
3. **Cosine label policy chunks with 8D scoring**
4. **Select training data using implicit confidence criteria**:
   - High Problem_X score
   - High Geo_Caribbean score
   - High Era_Modern score
   - **Low Era_Slavery score** ← KEY DIFFERENCE
5. Train classifier on policy-labeled chunks

**Effect**: BERTje learns to recognize problem signatures in contemporary framing, not just historical framing.

---

## Potential Disadvantages of 8D (Critical Analysis)

### 1. Interpretation Layer Complexity

**Problem**: Research question asks about 4 integrated topics (Educational, etc.), not 8 separate dimensions.

**Implication**: Need interpretation rules to translate 8D scores back to 4-topic framework:
```python
Educational_relevance = (
    Problem_Educational *
    Geo_Caribbean *
    (Era_Modern + 0.3 * Era_Slavery)
)
```

**Risk**: If interpretation rules are wrong, final analysis is wrong. Adds complexity without ground truth validation.

**Mitigation**: Could validate interpretation rules on evaluation sample before applying to full corpus.

### 2. Training Signal Assumptions

**Assumption**: BERTje trained on 8 independent dimensions can learn problem patterns separately from context.

**Risk**: What if problem patterns are NOT separable from context? E.g., "educational disadvantage" discussed differently in Caribbean vs. Dutch context, differently in historical vs. modern framing.

**Current 4D**: Learns integrated pattern (how educational disadvantage is discussed in Caribbean slavery context)
**Proposed 8D**: Learns separate patterns (educational vocabulary, Caribbean vocabulary), assumes they combine

**Mitigation**: Two-stage transfer (train on slavery corpus first, then policy corpus) might help BERTje learn both explicit and implicit integrated patterns.

### 3. Dictionary Curation Becomes 2x Work

**Current**: Curate 4 dictionaries (Educational, Governance, Economic, Racism)

**8D**: Curate 8 dictionaries:
- 4 problem dictionaries (should be "pure" problem vocabulary)
- 4 context dictionaries (geographic, temporal, etc.)

**Challenge**: How do you decide if "plantage-economie" goes in Economic or Era_Slavery? It's both.

**Risk**: Arbitrary splitting of inherently integrated terms reduces signal quality.

### 4. Still Requires Dictionary Improvement

**8D doesn't solve fundamental issue**: Current dictionary has score compression (max 0.6) even WITH 4D integrated approach.

**Why 8D might not fix this**:
- Score compression could be due to insufficient vocabulary coverage
- Or weights not properly calibrated
- Or chunks genuinely having moderate relevance (not everything is 0.9)

**8D could help**: By separating geographic terms from problem terms, problem scores might expand range (not lifted by uniform geographic presence).

**But**: Need to test whether 8D actually improves score ranges or just redistributes the same compression.

---

## Concrete Recommendations

### Option 1: Improve Current 4D System (Lower-Risk)

**Changes to confidence classification**:
```python
# Add multi-topic high confidence category
MULTI_TOPIC_HIGH_CONFIDENCE:
  max_score >= 0.35 AND
  2+ topics >= 0.30 AND
  margin < 0.05 AND
  geographic_presence == True  # Has Caribbean markers
```

**Effect**: Capture implicit multi-topic patterns without restructuring entire system.

**Stratified sampling adjustment**:
- Don't downsample multi-topic chunks
- Sample them equally to single-topic high-confidence

**Dictionary improvements** (regardless of 4D vs 8D):
1. Reduce weights on geographic terms (0.75 → 0.50) to reduce cross-contamination
2. Increase weights on core problem terms (1.0 → 1.0) - already maxed
3. Add more topic-specific vocabulary, especially Economic and Governance
4. Test whether score ranges expand

### Option 2: Implement 8D System (Higher-Risk, Higher-Reward)

**Phase 1: Test 8D scoring on evaluation sample**
1. Create 8 separate dictionaries from current v6 seed
2. Score 72-chunk evaluation sample with 8D
3. Compare score ranges: Do problem dimensions now reach 0.7-0.9?
4. Test interpretation rules: Do composite scores match semantic judgment?
5. If successful → proceed; if not → stay with improved 4D

**Phase 2: Implement 8D confidence criteria**
```python
# Explicit pattern high confidence
EXPLICIT_HIGH:
  Problem_X >= 0.6 AND
  Geo_Caribbean >= 0.7 AND
  Era_Slavery >= 0.5

# Implicit pattern high confidence
IMPLICIT_HIGH:
  Problem_X >= 0.6 AND
  Geo_Caribbean >= 0.7 AND
  Era_Modern >= 0.6 AND
  Era_Slavery < 0.3

# Both are "high confidence" for training
```

**Phase 3: Modified stratified sampling**
- Oversample both explicit and implicit high confidence
- Downsample only chunks that fail ALL confidence criteria

**Phase 4: Validation**
- After BERTje training, test on held-out policy documents
- Check: Does model recognize implicit patterns?
- Compare to 4D baseline

### Option 3: Hybrid Approach (Recommended)

**Use 4D for thesis analysis, but 8D internally for training selection**:

1. **Keep 4D topic framework for research questions** (Educational, Governance, Economic, Racism)
2. **Use 8D scoring internally during training data selection**:
   - Identify implicit vs. explicit patterns
   - Sample both types for training
   - BERTje learns broader pattern distribution
3. **BERTje classifier outputs 4D predictions** (not 8D)
4. **Report results in 4D framework** (matches research questions)

**Advantage**: Gets benefit of 8D's better training selection without complexity of 8D interpretation layer in final analysis.

---

## Specific Actionable Next Steps

### Immediate (Can do now with v16 data)

1. **Quantify implicit pattern filtering**:
   - How many chunks in "none confidence" have strong problem vocabulary but low historical vocabulary?
   - Manual review 10-20 examples: Are these actually valuable patterns?

2. **Test alternative confidence criteria on v16**:
   - Reclassify using multi-topic allowance
   - How does training distribution change?
   - Would this capture more implicit patterns?

### Short-term (Dictionary iteration)

3. **v17 dictionary experiment: Reduce geographic weights**:
   - Lower curaçao, bonaire, etc. from 0.75 to 0.50
   - Test on evaluation sample: Do score ranges expand?
   - Does cross-contamination reduce?

4. **Compare 4D vs 8D scoring on evaluation sample**:
   - Create 8D dictionaries
   - Score same 72 chunks with both approaches
   - Measure: score ranges, topic differentiation, pattern quality
   - Decision point: Which approach better captures implicit patterns?

### Medium-term (Training strategy)

5. **Implement implicit pattern sampling** (whether 4D or 8D):
   - Define criteria for implicit high confidence
   - Modify stratified sampling to include them
   - Train BERTje with balanced explicit + implicit examples

6. **Validate transfer performance**:
   - Test trained BERTje on policy documents
   - Check: Does it recognize problems without explicit slavery vocabulary?
   - Compare: 4D baseline vs. improved selection strategy

---

## Conclusion

**The core problem**: Current confidence classification systematically filters out implicit multi-topic patterns, which are exactly the patterns likely to appear in policy documents.

**Why it happens**:
- Margin requirements assume single-topic dominance
- Score compression limits high-confidence pool
- Cross-contamination creates uniform moderate scores
- Stratified sampling downsamples ambiguous chunks

**How 8D could help**:
- Separate confidence criteria for implicit patterns
- Reduced cross-contamination (geographic terms separate from problem terms)
- Composable relevance through dimension multiplication
- Training on pattern distribution matching policy corpus reality

**Critical questions before 8D implementation**:
1. Does 8D actually expand score ranges? (Test on evaluation sample)
2. Are problem patterns separable from context? (Theoretical assumption)
3. Is interpretation layer complexity worth the benefit? (Cost-benefit)
4. Could simpler 4D improvements achieve similar results? (Alternative)

**Recommended approach**: Test 8D scoring on evaluation sample (72 chunks) first. If score ranges expand and pattern quality improves, proceed with 8D training selection. If not, improve 4D system with multi-topic confidence criteria.

---

**Analysis by**: Claude (Sonnet 4.5)
**Date**: 2025-11-27
**Based on**: v16 scores data (1,652 chunks), v15 workflow notebook, PROJECT_CONTEXT_MASTER.md
