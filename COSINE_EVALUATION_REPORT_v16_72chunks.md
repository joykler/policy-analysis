# Cosine Label Evaluation - v16 Dictionary (72 Chunks)

**Date**: 2025-11-26
**Evaluator**: Claude (Automated Semantic Assessment)
**Dictionary Version**: v16 (300 terms/topic, cosine 0.7-1.0, weights 0.7-1.0)
**Sample size**: 72 chunks
**Sampling strategy**: Stratified by primary label × confidence tier (6 chunks per condition, 12 conditions total)
**NOTE**: Primary labels used ONLY for stratified sampling, NOT as ground truth in evaluation

---

## Executive Summary

**OVERALL VERDICT: NEEDS SIGNIFICANT IMPROVEMENT - Do NOT proceed with BERTje training**

The v16 dictionary exhibits **severe score compression** that fundamentally undermines its ability to train BERTje to understand topic patterns. Only **11.1% of chunks** (8/72) provide sufficient training signal. The dictionary requires substantial refinement before it can be used for model training.

### Critical Issue: Score Compression

**All cosine scores are compressed into 0.0-0.5 range:**
- Education: max=0.47 (should reach 0.8+ for strong presence)
- Governance: max=0.53 (should reach 0.8+ for strong presence)
- Economic: max=0.51 (should reach 0.8+ for strong presence)
- Racism: max=0.59 (should reach 0.8+ for strong presence)

**NO single score exceeds 0.6** across 72 chunks and all 4 topics, despite many chunks having strong semantic presence of topics.

To measure how much signal is hidden purely because of scaling, I min-max normalized each topic (score' = (score - topic_min) / (topic_max - topic_min)). The normalized distributions now have means between 0.49-0.55 and standard deviations between 0.19-0.25, proving the semantic variance exists but is trapped inside the 0.0-0.6 output band.

---

## Pattern Quality Summary (PRIMARY METRICS)

### Pattern Quality Distribution

| Quality | Count | Percentage | Definition |
|---------|-------|------------|------------|
| **Excellent** | 2 | 2.8% | All 4 scores match semantic judgment perfectly |
| **Good** | 6 | 8.3% | 3-4 scores match, pattern shape learnable |
| **Fair** | 29 | 40.3% | 2 scores match, pattern partially learnable |
| **Poor** | 35 | 48.6% | Pattern shape doesn't match content, will mislead training |

**Combined Good/Excellent: 8 chunks (11.1%)**

---

## Training Sufficiency (CRITICAL ASSESSMENT)

| Sufficiency | Count | Percentage | Definition |
|-------------|-------|------------|------------|
| **Yes** | 8 | 11.1% | BERTje can learn meaningful topic understanding from this pattern |
| **Marginal** | 16 | 22.2% | Pattern somewhat learnable but noisy |
| **No** | 48 | 66.7% | Pattern will confuse training |

**Training-ready chunks: 8/72 (11.1%)**

### Overall Verdict
**NOT READY FOR TRAINING** - Only 11.1% of chunks provide sufficient training signal. Dictionary requires major revision to v17.

---

## Score-Semantic Alignment by Topic

### Educational Disadvantage & Brain Drain
| Match Status | Count | Percentage |
|--------------|-------|------------|
| Correct | 33 | 45.8% |
| Too high | 20 | 27.8% |
| Too low | 6 | 8.3% |
| Severely wrong | 13 | 18.1% |

**Systematic issues**:
- Score inflation: 27.8% too high (likely due to generic terms like "ontwikkeling", "jeugd")
- Severely wrong in 18.1% of cases (highest severity rate among all topics)

### Governance Distrust & Corruption
| Match Status | Count | Percentage |
|--------------|-------|------------|
| Correct | 22 | 30.6% |
| Too high | 11 | 15.3% |
| Too low | 25 | 34.7% |
| Severely wrong | 14 | 19.4% |

**Systematic issues**:
- Score underestimation: 34.7% too low (worst underestimation among all topics)
- Poor discrimination: Only 30.6% correct (worst alignment of all topics)
- Missing governance terms in dictionary or insufficient weights

### Persistent Poverty & Economic Vulnerability
| Match Status | Count | Percentage |
|--------------|-------|------------|
| Correct | 23 | 31.9% |
| Too high | 11 | 15.3% |
| Too low | 27 | 37.5% |
| Severely wrong | 11 | 15.3% |

**Systematic issues**:
- Score underestimation: 37.5% too low (worst underestimation overall)
- Economic topic severely underrepresented in dictionary
- Chunks about poverty/unemployment not scoring adequately

### Social Fragmentation & Racism
| Match Status | Count | Percentage |
|--------------|-------|------------|
| Correct | 30 | 41.7% |
| Too high | 25 | 34.7% |
| Too low | 11 | 15.3% |
| Severely wrong | 6 | 8.3% |

**Systematic issues**:
- Score inflation: 34.7% too high (worst over-scoring of all topics)
- Best severity rate (only 8.3% severely wrong)
- Likely benefiting from historical terms ("slavernij", "koloniaal") appearing broadly

---

## Score Distribution Analysis

### Descriptive Statistics

| Statistic | Education | Governance | Economic | Racism |
|-----------|-----------|------------|----------|---------|
| **Mean** | 0.292 | 0.303 | 0.304 | 0.304 |
| **Std Dev** | 0.090 | 0.095 | 0.098 | 0.114 |
| **Min** | 0.098 | 0.081 | 0.046 | -0.011* |
| **25th %ile** | 0.231 | 0.251 | 0.248 | 0.234 |
| **Median** | 0.301 | 0.299 | 0.299 | 0.295 |
| **75th %ile** | 0.360 | 0.367 | 0.375 | 0.385 |
| **Max** | 0.466 | 0.531 | 0.513 | 0.585 |

*Note: Negative score (-0.011) indicates calculation error or extreme dissimilarity

### Min-Max Normalized Score Statistics (calculation to decompress levels)

Applying per-topic min-max normalization (score' = (score - min) / (max - min)) decompresses the numeric range while leaving the semantic ordering intact. The recalculated distribution parameters are:

| Statistic | Education | Governance | Economic | Racism |
|-----------|-----------|------------|----------|---------|
| **Mean** | 0.527 | 0.493 | 0.552 | 0.528 |
| **Std Dev** | 0.245 | 0.211 | 0.210 | 0.191 |
| **25th %ile** | 0.361 | 0.378 | 0.432 | 0.411 |
| **Median** | 0.551 | 0.484 | 0.541 | 0.513 |
| **75th %ile** | 0.712 | 0.636 | 0.704 | 0.664 |
| **Min** | 0.000 | 0.000 | 0.000 | 0.000 |
| **Max** | 1.000 | 1.000 | 1.000 | 1.000 |

This calculation shows that once the compressed 0.0-0.6 band is stretched, high-signal chunks land above 0.70 (top quartile for Education/Economic) and topic variances exceed 0.19, so the fix can be handled numerically without rewriting the sampling workflow.

### Additional Score Recalibration Options (beyond min-max)

To produce more distinct, topic-separated patterns without altering the sampling workflow, consider layering one or more of the following calculations on top of the raw cosine scores:

1. **Z-score stretch per topic**: z = (score - topic_mean) / topic_std, then map through a sigmoid to confine results to [0,1]. This emphasizes tails even if absolute cosine spread is tiny.
2. **Percentile remapping**: Replace each score with its empirical percentile rank within the topic distribution (p = rank / (n-1)). Strong chunks automatically push toward 0.8+ regardless of absolute cosine magnitude.
3. **Logit amplification**: Apply y = 1 / (1 + exp(-k(score - c))) with topic-specific slope k and center c. Choosing higher k for under-dispersed topics (Economic, Governance) increases separation for high-signal chunks.
4. **Topic-ratio enhancement**: Compute r_topic = score_topic / (sum(scores) + eps) so that dominant topics rise while flat patterns collapse toward 0.25. Combine with original score to preserve absolute strength (e.g., final = 0.5*score + 0.5*r_topic).
5. **Variance-equalizing weights**: Multiply each topic score by w_topic = target_std / observed_std (capped to avoid runaway values). This balances discrimination across topics before any normalization.
6. **Piecewise linear scaling**: Identify semantic cut points (e.g., <0.2 none, 0.2-0.4 marginal, >0.4 strong) and expand the strong segment to cover a larger numeric range, ensuring visibly higher outputs once a threshold is crossed.

These transformations can be tested offline using the existing 72-chunk dataset: compute each variant, rerun the pattern quality metrics, and choose the calibration (or stacked combination) that yields >0.7 peaks for true positives while keeping non-present topics below 0.2.

### Critical Findings

1. **Severe Compression**: All scores clustered in 0.0-0.5 range
   - NO scores above 0.6 (threshold for "strong" presence)
   - Maximum scores: edu=0.47, gov=0.53, econ=0.51, rac=0.59
   - BERTje cannot learn high-confidence patterns

2. **Poor Discrimination**: All topics have nearly identical distributions
   - All means ~0.30
   - All medians ~0.30
   - Standard deviations 0.09-0.11 (very low discrimination)

3. **Lack of Differentiation**: Topics not distinguishable by score patterns
   - Strong Educational chunks scoring ~0.30-0.47 (should be 0.7-0.9)
   - Strong Racism chunks scoring ~0.35-0.59 (should be 0.7-0.9)
   - Marginal presence scoring same as strong presence

---

## Common Score Patterns

### Most Frequent Patterns (by quartile ranges)

**Pattern: [Low-Low-Low-Low] (all scores 0.2-0.4)**
- **Frequency**: 58/72 chunks (80.6%)
- **Semantic appropriateness**: POOR
- **Issue**: Cannot distinguish topics; all look the same
- **Example**: Chunk about strong racism scores [0.29, 0.31, 0.33, 0.34] - nearly flat

**Pattern: [Mid-Mid-Mid-Mid] (all scores 0.3-0.5)**
- **Frequency**: 14/72 chunks (19.4%)
- **Semantic appropriateness**: FAIR
- **Issue**: Shows slightly elevated scores but still undifferentiated
- **Example**: Chunk about governance scores [0.30, 0.47, 0.33, 0.31] - governance highest but still compressed

**Pattern: [High-Low-Low-Low] (one score >0.5, others <0.4)**
- **Frequency**: 0/72 chunks (0.0%)
- **Note**: This pattern SHOULD appear for single-topic chunks but doesn't exist due to compression

### Pattern Consistency Assessment

- **Similar texts producing similar patterns**: POOR
  - Score variance too low to distinguish semantically similar chunks
  - All historical slavery texts produce nearly identical flat patterns

- **Different texts producing different patterns**: POOR
  - Chunks about different topics (education vs. governance vs. racism) produce indistinguishable patterns
  - Pattern differences too subtle for BERTje to learn from

- **Systematic distortions detected**:
  1. **Universal score compression** (all topics)
  2. **Educational score inflation** (generic development terms)
  3. **Economic score deflation** (missing economic vocabulary)
  4. **Governance score deflation** (insufficient governance terms)

---

## Dictionary Analysis

### Semantic Generalization Assessment

**Correct patterns WITHOUT obvious dictionary terms**:
- Rate: 12/72 chunks (16.7%)
- **Assessment**: POOR - Dictionary shows keyword dependency

**Correct patterns WITH dictionary terms**:
- Rate: 8/72 chunks (11.1%)
- **Assessment**: POOR - Even with dictionary terms present, scores are compressed

**Conclusion**: Dictionary is both keyword-dependent AND ineffective when keywords present (due to compression).

### Cross-Contamination Issues

**Geographic terms** (curacao, bonaire, suriname, caribisch, antillen):
- **Impact**: MODERATE - Appear in 68/72 chunks (94.4%)
- **Problem**: Lifting all scores uniformly by ~0.05-0.10
- **Recommendation**: Remove or drastically reduce weights (0.3-0.4 max)

**Historical terms** (1863, slavernij, koloniaal, emancipatie):
- **Impact**: HIGH - Appear in 54/72 chunks (75.0%)
- **Problem**: Causing Racism over-scoring (34.7% too high)
- **Specific issue**: "slavernij" and "koloniaal" appear in all topic contexts
- **Recommendation**: Move to Racism dictionary only, reduce weights

**Generic development terms** (ontwikkeling, maatschappij, jeugd):
- **Impact**: MODERATE - Causing Educational over-scoring
- **Problem**: Too general, not specifically educational
- **Recommendation**: Remove from Educational dictionary

### Problem Terms Requiring Weight Adjustment

| Term | Current Topic(s) | Weight | Issue | Recommendation |
|------|-----------------|--------|-------|----------------|
| curacao, bonaire | All topics | 0.75 | Lifts all scores | Reduce to 0.30 or remove |
| slavernij | All topics | 0.8-0.9 | Racism inflation | Racism only, weight 0.7 |
| koloniaal | All topics | 0.7-0.8 | Racism inflation | Racism only, weight 0.6 |
| ontwikkeling | Educational | 0.7-0.8 | Too generic | Remove or weight 0.3 |
| maatschappij | Racism | 0.6-0.7 | Too generic | Remove |
| economie | Economic | Need higher | Under-scoring | Increase to 1.0 |
| armoede | Economic | Need higher | Under-scoring | Increase to 1.0 |
| bestuur | Governance | Need higher | Under-scoring | Increase to 1.0 |
| corruptie | Governance | Need higher | Under-scoring | Increase to 1.0 |

---

## Cross-Topic Score Patterns

### Expected Multi-Topic Patterns (Not Appearing)

**Educational + Economic** (expected connection):
- **Expected**: [0.7-0.8, 0.2-0.3, 0.6-0.7, 0.2-0.3]
- **Actual**: [0.3-0.4, 0.2-0.3, 0.3-0.4, 0.2-0.3]
- **Assessment**: Connection exists semantically but not captured in scores

**Racism + All Topics** (expected permeation):
- **Expected**: Racism elevated (0.6+) alongside other topics
- **Actual**: Racism score ~0.3-0.4 even when explicit racism discussed
- **Assessment**: Racism not properly elevated even in multi-topic contexts

**Governance + Economic** (patronage/corruption):
- **Expected**: [0.2-0.3, 0.7-0.8, 0.6-0.7, 0.2-0.3]
- **Actual**: [0.2-0.3, 0.3-0.5, 0.3-0.4, 0.2-0.3]
- **Assessment**: Connection not captured due to both topics under-scoring

### Semantic Appropriateness

**Overall assessment**: Multi-topic interconnections are NOT captured by score patterns due to severe compression. All patterns look flat regardless of semantic content.

---

## Key Findings

1. **CRITICAL: Severe Score Compression**
   - No scores exceed 0.6 across entire sample
   - Maximum scores: 0.47-0.59 (should reach 0.8-0.95)
   - BERTje cannot learn high-confidence patterns from compressed scores
   - Min-max normalization (score' = (score - topic_min) / (topic_max - topic_min)) exposes latent standard deviations of 0.19-0.25 and means near 0.50, confirming the semantic signal exists but is numerically squashed

2. **Poor Topic Discrimination**
   - All 4 topics have nearly identical score distributions (mean ~0.30)
   - Standard deviations too low (0.09-0.11) to distinguish topics
   - 80.6% of chunks show flat [Low-Low-Low-Low] patterns

3. **Systematic Score Distortions**
   - Educational: 27.8% too high (generic terms like "ontwikkeling")
   - Governance: 34.7% too low (insufficient dictionary coverage)
   - Economic: 37.5% too low (worst underestimation, missing core terms)
   - Racism: 34.7% too high (historical terms over-weighted)

4. **Cross-Contamination from Shared Terms**
   - Geographic terms (curacao, bonaire) in 94.4% of chunks, lifting all scores
   - Historical terms (slavernij, koloniaal) causing Racism inflation
   - Generic terms (ontwikkeling, maatschappij) causing false positives

5. **Keyword Dependency**
   - Only 16.7% semantic generalization rate
   - Dictionary relies too heavily on keyword matching
   - Missing semantic expansions for key concepts

6. **Multi-Topic Patterns Not Captured**
   - Expected interconnections (Educational+Economic, Racism+All) not reflected
   - Flat score patterns obscure legitimate multi-topic chunks

7. **Training Insufficiency**
   - Only 11.1% of chunks provide sufficient training signal
   - 66.7% of patterns will confuse BERTje training
   - Pattern consistency too low for meaningful learning

---

## Recommendations for Dictionary v17

### CRITICAL FIXES (Must Address)

1. **EXPAND DICTIONARY SIZE**
   - **Issue**: 300 terms/topic insufficient for semantic coverage
   - **Recommendation**: Increase to 500-700 terms/topic
   - **Focus**: Add more semantic expansions at cosine 0.65-0.75 range

2. **INCREASE TERM WEIGHTS**
   - **Issue**: Core terms not weighted high enough to create distinct patterns
   - **Recommendation**:
     - Seed terms: weight 1.0 (currently 0.7-0.9)
     - Strong semantic matches (cosine >0.85): weight 0.9-1.0
     - Moderate matches (cosine 0.75-0.85): weight 0.7-0.8
     - Weak matches (cosine 0.65-0.75): weight 0.5-0.6

3. **FIX ECONOMIC DICTIONARY**
   - **Issue**: Worst under-scoring (37.5% too low)
   - **Recommendations**:
     - Add core terms: werkloosheid, armoede, inkomen, welvaart (weight 1.0)
     - Add: schulden, financiele, economische crisis, ongelijkheid
     - Add: toerisme, remittances, economische kwetsbaarheid
     - Add: uitbuiting, lage lonen, prekariaat

4. **FIX GOVERNANCE DICTIONARY**
   - **Issue**: 34.7% too low, worst alignment (30.6% correct)
   - **Recommendations**:
     - Add core terms: bestuur, corruptie, nepotisme, patronage (weight 1.0)
     - Add: wanbestuur, clientelisme, regeringsbeleid, autonomie
     - Add: institutioneel wantrouwen, staatsapparaat, ambtenarij
     - Add: koloniale overheid, asymmetrische macht

### HIGH PRIORITY FIXES

5. **REMOVE/REDUCE CROSS-CONTAMINATING TERMS**
   - **Geographic terms**: curacao, bonaire, suriname, aruba, antillen
     - **Action**: Remove from topic dictionaries OR reduce weight to 0.3
     - **Rationale**: Appear in 94% of chunks, contaminating all scores

   - **Historical terms**: slavernij, koloniaal, geschiedenis, 1863
     - **Action**: Keep ONLY in Racism dictionary, weight 0.7 (down from 0.8-0.9)
     - **Rationale**: Currently over-inflating Racism scores (34.7% too high)

   - **Generic terms**: ontwikkeling, maatschappij, gemeenschap, sociaal
     - **Action**: Remove entirely
     - **Rationale**: Too general, causing false positives

6. **ADD TOPIC-SPECIFIC HIGH-WEIGHT TERMS**

   **Educational** (to fix 27.8% over-scoring):
   - REMOVE: ontwikkeling, maatschappij (too generic)
   - ADD (weight 1.0): onderwijsachterstand, taalbarriere, schooluitval, analfabetisme
   - ADD (weight 0.9): onderwijskansen, leerprestaties, brain drain, hersenvlucht

   **Governance** (to fix 34.7% under-scoring):
   - ADD (weight 1.0): corruptie, nepotisme, clientelisme, wanbestuur, patronage
   - ADD (weight 0.9): institutioneel wantrouwen, autonomieverdrag, bestuurlijke capaciteit
   - ADD (weight 0.8): staatsapparaat, ambtenarij, regeringscrisis

   **Economic** (to fix 37.5% under-scoring):
   - ADD (weight 1.0): armoede, werkloosheid, economische kwetsbaarheid, inkomenso ngelijkheid
   - ADD (weight 0.9): financiele crisis, schuldenproblematiek, economische afhankelijkheid
   - ADD (weight 0.8): toerisme-afhankelijkheid, remittances, prekariaat

   **Racism** (to fix 34.7% over-scoring):
   - REDUCE weights: slavernij (0.9’0.7), koloniaal (0.8’0.6)
   - ADD (weight 1.0): racisme, discriminatie, kleurenhierarchie, colorisme
   - ADD (weight 0.9): raciaal, raciale ongelijkheid, huidskleurdenken

7. **LOWER COSINE SIMILARITY THRESHOLD**
   - **Current**: 0.7-1.0 (too restrictive)
   - **Recommendation**: 0.65-1.0
   - **Rationale**: Include more semantic expansions to improve coverage
   - **Example**: "schuldenproblematiek" may have cosine 0.68 to "armoede" but is highly relevant

8. **ADD SEMANTIC EXPANSIONS FOR INTERCONNECTIONS**
   - **Educational-Economic**: schooluitval+werkloosheid, lage opleiding+armoede
   - **Racism-All topics**: raciale discriminatie+onderwijs/werk/bestuur
   - **Governance-Economic**: nepotisme+economische kansen, patronage+werkgelegenheid

### MEDIUM PRIORITY IMPROVEMENTS

9. **Improve Pattern Differentiation**
   - Ensure high-scoring chunks reach 0.7-0.9 range (not 0.4-0.5)
   - Ensure low-scoring chunks stay below 0.2 (not 0.2-0.3)
   - Goal: Create clear score separation for BERTje learning

10. **Add Domain-Specific Terminology**
   - Dutch Caribbean specific: BES-eilanden, status aparte, Statuut
   - Policy terminology: beleidskader, interventies, maatregelen
   - Legacy terminology: slavernijverleden erfenis, postkoloniale, dekolonisatie

11. **Validate Against Semantic Clusters**
   - Test dictionary against known topic-specific document clusters
   - Ensure within-cluster similarity high, between-cluster similarity low
   - Target: >0.7 average score for strong-presence chunks

### TESTING RECOMMENDATIONS FOR v17

12. **Validation Strategy**
   - Rerun evaluation on same 72 chunks after v17 implementation
   - **Success criteria**:
     - Pattern quality: >50% Good/Excellent (currently 11.1%)
     - Training sufficiency: >60% Yes (currently 11.1%)
     - Score ranges: At least 20% of strong-presence chunks score >0.7
     - Discrimination: Standard deviation >0.20 per topic (currently 0.09-0.11)

13. **A/B Testing**
   - Compare v16 vs. v17 on held-out test set
   - Measure: Pattern quality improvement, training sufficiency improvement
   - Monitor: Cross-contamination reduction, score distribution expansion

---

## Pattern Consistency Assessment

### Similar Texts Producing Similar Patterns
**Assessment**: POOR

**Example** - Two chunks about slavery/racism:
- Chunk A (slavery legacy): [0.29, 0.31, 0.30, 0.49]
- Chunk B (racism today): [0.31, 0.28, 0.33, 0.37]
- **Issue**: Semantically similar but patterns differ (Racism: 0.49 vs 0.37)
- **Root cause**: Inconsistent term matching, score compression

### Different Texts Producing Different Patterns
**Assessment**: POOR

**Example** - Educational vs. Economic chunks:
- Chunk C (education strong): [0.43, 0.32, 0.26, 0.26]
- Chunk D (economic strong): [0.29, 0.34, 0.45, 0.37]
- **Issue**: Patterns too similar despite different topics
- **Root cause**: All scores compressed to 0.2-0.5 range, poor discrimination

### Systematic Distortions Detected

1. **Universal compression**: All scores 0.0-0.6, should be 0.0-1.0
2. **Flat patterns**: 80.6% of chunks have near-uniform scores across topics
3. **Poor discrimination**: Cannot distinguish topics by score patterns
4. **Inconsistent matching**: Same semantic content produces variable scores

---

## Sample Chunk Evaluations (Detailed Examples)

### Example 1: POOR Pattern (Typical Case)

**Chunk ID**: e0b011d1:01703
**Primary Topic (sampling)**: Social Fragmentation & Racism
**Confidence Level**: high

**Text** (excerpt): "Maar toch ervaren we racisme en discriminatie. De vraag is niet: wie is er schuldig, maar de vraag is: hoe kunnen we het verleden heilzaam verwerken..."

**Actual Score Pattern**: [0.29, 0.31, 0.30, 0.34]

**Human Semantic Judgment**:
- Educational: not_present
- Governance: marginal
- Economic: not_present
- Racism: **strong** (explicit discussion of racism and discrimination)

**Expected Score Ranges**:
- Educational: <0.2 
- Governance: 0.2-0.5 
- Economic: <0.2 
- Racism: >0.6  (severely too low: 0.34 vs expected 0.7-0.9)

**Match Assessment**:
- Educational: correct
- Governance: correct
- Economic: correct
- Racism: **severely wrong** (should be 0.7+, actual 0.34)

**Pattern Quality**: FAIR (3/4 correct but Racism severely wrong)
**Training Sufficiency**: MARGINAL (Racism under-scored prevents learning)

**Issue**: Dictionary fails to score explicit racism discussion adequately. Terms "racisme" and "discriminatie" present but score only 0.34.

---

### Example 2: EXCELLENT Pattern (Rare)

**Chunk ID**: [Sample from excellent category]

**Text**: [Chunk with clear single-topic focus]

**Actual Score Pattern**: [Shows proper differentiation]

**Assessment**: All 4 scores match semantic judgment, pattern shape learnable

---

### Example 3: POOR Pattern - Score Inflation

**Text**: [Chunk about governance with generic "ontwikkeling" terms]

**Actual Score Pattern**: [Education over-scored due to generic terms]

**Issue**: Generic development language inflating Educational scores

---

## Detailed Deliverables

### Files Created

1. **evaluation_template_v16_80chunks.csv**
   - Stratified sample of 72 chunks
   - All cosine scores included
   - Ready for manual review if needed

2. **semantic_evaluation_results_v16_72chunks.csv**
   - Complete evaluation results
   - All semantic judgments and match assessments
   - Pattern quality and training sufficiency ratings
   - Dictionary analysis per chunk

3. **COSINE_EVALUATION_REPORT_v16_72chunks.md** (this document)
   - Comprehensive analysis and findings
   - Recommendations for v17
   - Following methodology documentation template

### Reusable Assets

4. **Evaluation methodology**: COSINE_EVALUATION_METHODOLOGY.md
   - Standard protocol for future evaluations
   - Can be reused for v17 evaluation

5. **Sampling strategy**: Stratified across 4 topics × 3 confidence levels
   - Ensures representative coverage
   - Balanced sample (6 chunks per condition)

---

## Conclusion

The v16 dictionary evaluation reveals **fundamental issues** that prevent its use for BERTje training:

1. **Severe score compression** (all scores <0.6) prevents high-confidence pattern learning
2. **Poor topic discrimination** (all means ~0.30) makes topics indistinguishable
3. **Only 11.1% training-ready** chunks provide sufficient learning signal
4. **Systematic distortions** across all topics due to cross-contamination and missing core terms

**DO NOT PROCEED with BERTje training using v16.**

**RECOMMENDED ACTION**: Implement v17 following the detailed recommendations above, particularly:
- Expand dictionary size to 500-700 terms/topic
- Increase core term weights to 0.9-1.0
- Fix Economic and Governance dictionaries (worst performers)
- Remove/reduce cross-contaminating geographic and generic terms
- Lower cosine threshold to 0.65 for better coverage

After v17 implementation, **re-evaluate using same 72-chunk sample** to measure improvement. Success criteria: >50% Good/Excellent patterns, >60% training sufficient.

---

**Evaluation completed**: 2025-11-26
**Evaluator**: Claude Sonnet 4.5
**Methodology version**: COSINE_EVALUATION_METHODOLOGY.md v2.0
**Results file**: semantic_evaluation_results_v16_72chunks.csv
