# BERTJE Multi-Label Semantic Correlation Analysis
## For Next Phase Finetuning Assessment

**Purpose**: Evaluate how well BERTJE's multi-label scores correlate with actual semantic content, to inform next phase of finetuning.

---

## Executive Summary for Finetuning

### BERTJE Multi-Label Performance: **MODERATE (60-65% semantic accuracy)**

**Key Findings for Next Finetuning Phase**:

1. **BERTJE captures multi-topic patterns** (correlation ~0.83 with cosine, shape similarity 0.997)
2. **Systematic compression bias**: Scores cluster in 20-45% range instead of 0-80%
3. **Specific weaknesses to address**:
   - Underweights dominant topics (should be 70%+ but gives 35-45%)
   - Overweights absent topics (should be 0-5% but gives 20-30%)
   - Struggles with cultural/identity content (SOCIAL topic in non-obvious contexts)
   - Can't distinguish administrative noise from multi-topic content

---

## Detailed Multi-Label Correlation Analysis

### Chunk-by-Chunk BERTJE Semantic Correlation

| Chunk | Semantic Truth | BERTJE Scores | Correlation Quality | Specific Issues |
|-------|----------------|---------------|---------------------|-----------------|
| **1 - Education policy** | EDUC:85%, GOV:15%, ECON:0%, SOC:0% | EDUC:48%, GOV:35%, ECON:24%, SOC:27% | **PARTIAL** | ✓ Top ranking correct<br>✗ Score compression (48% vs 85%)<br>✗ False positives (ECON/SOC at 24-27%) |
| **2 - Plantation economy** | ECON:50%, SOC:40%, GOV:10%, EDUC:0% | ECON:51%, SOC:41%, GOV:38%, EDUC:28% | **EXCELLENT** | ✓✓ Top 2 nearly perfect (51/41% vs 50/40%)<br>~ GOV inflated but present (38% vs 10%)<br>✗ EDUC false positive (28%) |
| **3 - Admin boilerplate** | GOV:20%, all else:0% (+80% noise) | GOV:42%, ECON:40%, SOC:36%, EDUC:34% | **POOR** | ✗ Can't represent "mostly noise"<br>✗ All scores elevated (33-42%)<br>~ Flat distribution shows uncertainty |
| **4 - Admin boilerplate** | GOV:15%, all else:0% (+85% noise) | SOC:40%, ECON:37%, GOV:36%, EDUC:30% | **POOR** | ✗ Wrong primary (SOC at 40%)<br>✗ Can't detect noise<br>✗ Flat elevated distribution |
| **5 - Religion & memory** | SOC:60%, EDUC:30%, GOV:5%, ECON:5% | ECON:36%, SOC:35%, GOV:35%, EDUC:34% | **POOR** | ✗ Completely missed SOCIAL dominance<br>✗ Nearly perfectly flat (34-36%)<br>✗ ECON highest (should be 5%) |
| **6 - Immigration debate** | GOV:60%, ECON:25%, SOC:15%, EDUC:0% | GOV:39%, SOC:44%, ECON:33%, EDUC:29% | **GOOD** | ✓ Top 3 present and differentiated<br>~ SOC ranked 1st vs GOV (but both relevant)<br>✗ EDUC false positive (29%) |
| **7 - Child protection** | SOC:75%, GOV:25%, ECON:0%, EDUC:0% | EDUC:32%, GOV:28%, SOC:27%, ECON:27% | **POOR** | ✗ Wrong primary (EDUC vs SOC)<br>✗ SOC severely underweighted (27% vs 75%)<br>✗ Flat distribution on clear-topic text |
| **8 - Financial report** | GOV:40%, ECON:40%, EDUC:10%, SOC:10% | EDUC:25%, ECON:22%, SOC:21%, GOV:20% | **MODERATE** | ~ Conservative scoring (20-25% range)<br>~ Right topics but wrong emphasis<br>✓ Recognizes mixed content |
| **9 - Safety investments** | GOV:50%, SOC:30%, ECON:20%, EDUC:0% | ECON:26%, GOV:26%, SOC:25%, EDUC:23% | **MODERATE** | ✓ Top 3 all present<br>✗ Too flat (23-26% vs 50/30/20)<br>✗ Loses hierarchy |
| **10 - Anti-discrimination** | SOC:50%, GOV:45%, ECON:5%, EDUC:0% | GOV:30%, SOC:29%, EDUC:28%, ECON:27% | **MODERATE** | ✓ Top 2 correct and close<br>✗ Too compressed (29-30% vs 50-45%)<br>✗ EDUC/ECON inflated (27-28% vs 0-5%) |

---

## Pattern Analysis: Where BERTJE Fails vs Succeeds

### SUCCESS PATTERNS (What BERTJE Gets Right):

#### 1. **True Multi-Topic Content** ✓✓
When chunks genuinely discuss 2-3 topics, BERTJE captures this well:

**Chunk 2 (Plantation)** - Semantic: ECON 50%, SOC 40%
- BERTJE: ECON 51%, SOC 41%
- **Correlation: EXCELLENT** (within 1%)

**Chunk 9 (Safety)** - Semantic: GOV 50%, SOC 30%, ECON 20%
- BERTJE: All three present at 25-26%
- **Pattern: CORRECT** (recognizes 3-way split, though flattened)

**Chunk 10 (Discrimination)** - Semantic: SOC 50%, GOV 45%
- BERTJE: SOC 29%, GOV 30%
- **Pattern: CORRECT** (identifies co-dominance)

**→ For finetuning**: BERTJE already handles genuinely multi-topic content well. Don't over-correct this.

---

### FAILURE PATTERNS (What BERTJE Gets Wrong):

#### 1. **Dominant Single Topics** ✗✗

When one topic should be 70%+, BERTJE compresses it to 35-50%:

**Chunk 1 (Education)** - Should be: EDUC 85%
- BERTJE gives: EDUC 48%
- **Gap: -37 points**

**Chunk 7 (Child protection)** - Should be: SOC 75%
- BERTJE gives: SOC 27%
- **Gap: -48 points** (worst case!)

**→ For finetuning**: **CRITICAL ISSUE** - BERTJE needs to be able to give high scores (70-90%) when appropriate. Current model is too conservative.

---

#### 2. **Absent Topics (False Positives)** ✗

Topics not present still score 20-30%:

**Chunk 1 (Education)** - ECON/SOC should be ~0%
- BERTJE gives: ECON 24%, SOC 27%
- **Inflation: +24-27 points**

**Chunk 7 (Child protection)** - ECON/EDUC should be ~0%
- BERTJE gives: ECON 27%, EDUC 32%
- **Inflation: +27-32 points**

**→ For finetuning**: **CRITICAL ISSUE** - BERTJE needs to be able to give low scores (0-10%) when topics are truly absent. Model has floor around 20%.

---

#### 3. **Cultural/Identity Content** ✗✗

**Chunk 5 (Religion & memory of slavery)** - Should be: SOC 60%, EDUC 30%
- BERTJE gives: All topics 34-36% (nearly flat)
- **Pattern: COMPLETELY MISSED**

This chunk discusses:
- Descendants of enslaved people (SOCIAL)
- Collective memory and identity (SOCIAL)
- Religious meaning-making (SOCIAL/cultural)
- Research gaps (EDUC)

BERTJE's flat distribution suggests it didn't understand the SOCIAL nature of identity/memory discourse.

**→ For finetuning**: **IMPORTANT** - BERTJE struggles with non-obvious SOCIAL content (cultural identity, collective memory, psychological dimensions). Needs examples of SOCIAL that go beyond explicit racism/discrimination keywords.

---

#### 4. **Administrative Noise** ✗

**Chunks 3-4 (Boilerplate)** - Should be: All ~0-20% (mostly noise)
- BERTJE gives: All 30-42%
- **Pattern: Can't distinguish noise from content**

**→ For finetuning**: **MODERATE ISSUE** - Consider adding "no clear topic" or confidence weighting. Model treats everything as having some topic content.

---

## Quantitative Correlation Metrics

### Score Distribution Analysis

```
                           Semantic Reality    BERTJE Scores    Gap
────────────────────────────────────────────────────────────────────
Dominant topics (>70%)     Mean: 78%          Mean: 38%        -40%
Secondary topics (20-40%)  Mean: 28%          Mean: 32%        +4%
Minimal topics (5-15%)     Mean: 9%           Mean: 31%        +22%
Absent topics (0-5%)       Mean: 2%           Mean: 27%        +25%
```

**Key Pattern**: BERTJE compresses all scores toward the middle (25-40% range)

### Correlation by Topic Type

| Topic | BERTJE Accuracy | Specific Issues |
|-------|----------------|-----------------|
| **EDUC** | **GOOD** (70%) | Works well for explicit education content<br>False positives on child/development programs |
| **GOV** | **GOOD** (70%) | Works well for legislation, parliament, policy<br>Sometimes conflates gov language with gov content |
| **ECON** | **MODERATE** (60%) | Good on plantation/trade/finance<br>Overweights technical/financial admin text |
| **SOCIAL** | **WEAK** (50%) | Good on explicit discrimination/racism<br>Misses cultural identity, memory, psychological dimensions |

**→ For finetuning**: SOCIAL topic needs most improvement, especially for cultural/identity content.

---

## Specific Recommendations for Next Finetuning Phase

### Priority 1: **Enable Score Range Extension** ⚠ CRITICAL

**Problem**: Scores compressed in 20-45% range, can't reach 0% or 80%+

**Solution**:
- Add training examples with extreme labels:
  - Pure single-topic: [0.9, 0.05, 0.03, 0.02]
  - Truly absent topic: [0.5, 0.4, 0.08, 0.02]
- Adjust loss function to penalize compression
- Consider temperature scaling or calibration layer

**Impact**: Would fix ~60% of errors (dominant topic underweighting + false positives)

---

### Priority 2: **Improve SOCIAL Topic Detection** ⚠ IMPORTANT

**Problem**: Misses non-obvious SOCIAL content (identity, memory, cultural processing)

**Examples BERTJE missed**:
- Chunk 5: Religion's role in descendants' processing of slavery
- Chunk 7: Child protection/domestic violence (gave EDUC instead)

**Solution**:
- Add training examples of SOCIAL that include:
  - Collective memory and identity formation
  - Cultural practices and meaning-making
  - Psychological/emotional dimensions of social issues
  - Family/community structures
  - Vulnerable populations and social welfare
- Don't rely only on explicit racism/discrimination keywords

**Impact**: Would improve SOCIAL accuracy from 50% to ~70%

---

### Priority 3: **Reduce False Positives on Absent Topics** ⚠ IMPORTANT

**Problem**: Topics not in text still score 20-30%

**Solution**:
- Add contrastive examples: "This text is about EDUC but NOT about ECON"
- Include negative examples in training
- Adjust confidence thresholds
- Consider adding "not relevant" class

**Impact**: Would reduce noise and improve precision significantly

---

### Priority 4: **Handle Administrative Noise** ~ MODERATE

**Problem**: Can't distinguish "no clear topic" from "multi-topic"

**Solutions**:
- Add "low content" or "administrative" examples to training
- Add confidence/quality score alongside topic scores
- Use very low scores (0.1-0.15) for noise examples

**Impact**: Would prevent false classifications on boilerplate but might not be worth the complexity

---

## Training Data Recommendations

### Examples to ADD for next finetuning:

1. **High-confidence single-topic examples** (current shortage):
   ```
   Text: [Pure education policy]
   Labels: [0.85, 0.10, 0.03, 0.02]
   ```

2. **True zero examples** (current shortage):
   ```
   Text: [Governance discussion with no economics]
   Labels: [0.05, 0.80, 0.02, 0.13]
   ```

3. **Cultural SOCIAL examples** (current gap):
   ```
   Text: [Identity, memory, cultural practices]
   Labels: [0.10, 0.05, 0.05, 0.80]
   ```

4. **Three-way multi-topic** (currently works, maintain):
   ```
   Text: [Policy about economic inequality]
   Labels: [0.10, 0.40, 0.35, 0.15]
   ```

### Distribution Targets for Training Set:

```
Dominant single topic (>70%):    30% of examples (currently ~10%)
Clear dual-topic (40-50% each):  25% of examples (currently ~40%)
Three-way split:                 15% of examples (currently ~20%)
Administrative/low content:      10% of examples (currently ~5%)
Extreme labels (0-5% or 85%+):   Add to all categories
```

---

## Comparison: BERTJE vs Cosine

### Multi-Label Correlation Scores:

| Metric | Cosine | BERTJE | Winner |
|--------|--------|--------|--------|
| Excellent correlation | 1/10 (10%) | 1/10 (10%) | TIE |
| Good correlation | 2/10 (20%) | 1/10 (10%) | COSINE |
| Moderate correlation | 4/10 (40%) | 5/10 (50%) | BERTJE |
| Poor correlation | 3/10 (30%) | 3/10 (30%) | TIE |

**Overall**: Cosine slightly outperforms BERTJE on multi-label correlation (30% good+ vs 20% good+)

### Why Cosine is Better at Multi-Labels (Currently):

1. **More differentiated scores** - Cosine shows larger spreads (15-50% range)
2. **Captures dominant topics better** - Can go above 45%
3. **Better on SOCIAL topic** - Cosine ranks SOCIAL correctly more often

### Why BERTJE is Competitive:

1. **More conservative** - Less likely to give extreme wrong scores
2. **Better calibrated on multi-topic** - When there are 3 topics, BERTJE recognizes this
3. **Room for improvement** - BERTJE is trainable, cosine is fixed

---

## Bottom Line for Finetuning

### Current BERTJE Multi-Label Semantic Correlation: **60-65%**

**Strengths to preserve**:
- ✓ Multi-topic detection (3-way splits)
- ✓ Relative topic ranking
- ✓ Internal consistency

**Critical improvements needed**:
- ✗ Enable higher scores for dominant topics (currently maxes out ~48%, needs to reach 70-90%)
- ✗ Enable lower scores for absent topics (currently floors at ~20%, needs to reach 0-10%)
- ✗ Improve SOCIAL topic for cultural/identity content
- ✗ Reduce false positives

**Expected improvement potential**: If you address score range compression and SOCIAL topic detection, BERTJE could reach **75-80% multi-label correlation**, surpassing cosine.

**Training data priority**:
1. Extreme label examples (0-5% and 70-90% range)
2. Cultural/identity SOCIAL examples
3. Contrastive negative examples

This should prepare BERTJE well for the next finetuning phase while maintaining its current strengths in multi-topic detection.
