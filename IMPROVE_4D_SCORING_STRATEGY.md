# Strategy: Improving 4D Dictionary Scoring for Better Score Spread

**Date**: 2025-11-27
**Goal**: Expand score ranges and reduce cross-contamination WITHOUT changing to 8D structure

---

## Diagnosis: Why v16 Scores Are Compressed

### Current v16 Score Ranges (PROBLEM)
```
Topic            Min     Max    Mean   Std
Educational:    0.004   0.637  0.281  0.082
Governance:    -0.031   0.553  0.293  0.091
Economic:       0.008   0.582  0.300  0.093
Racism:        -0.011   0.602  0.321  0.108
```

**Problems**:
1. **Max scores only 0.55-0.64** (should reach 0.7-0.9 for strong chunks)
2. **Means clustered 0.28-0.32** (insufficient differentiation)
3. **Narrow standard deviations** (0.08-0.11) show compressed distribution

### Root Cause Analysis (from v6 dictionary)

**1. Uniform Terms with High Weights Create Cross-Contamination**

```
Uniform terms (appear in all 4 topics):
- Geographic (weight 0.75): curaçao, bonaire, caribisch nederland, suriname, aruba, bes-eilanden
- Era markers (weight 0.70): 1863, geschiedenis, historisch, koloniaal, koloniale, slavernijverleden

Impact per topic:
- Educational:  12/45 terms (26.7%) are uniform
- Governance:   10/39 terms (25.6%) are uniform
- Economic:     13/39 terms (33.3%) are uniform
- Racism:       11/43 terms (25.6%) are uniform
```

**What this means**:
- If chunk mentions "curaçao" + "1863" + "slavernijverleden" → ALL 4 topics get boosted by ~0.75 + 0.70 + 0.70 = 2.15 units
- This creates a **baseline floor** that lifts all scores uniformly
- **Reduces differentiation** between topics
- **Compresses ranges** because differences come only from the remaining 70-75% of topic-specific terms

**2. Insufficient Weight Differentiation Within Topics**

```
Weight distribution (uniform across all terms):
- Core problems: 0.95-1.0   (very narrow range)
- Related:       0.85-0.9    (very narrow range)
- Historical:    0.8 exactly (no variation)
- Geographic:    0.75 exactly (no variation)
- Era markers:   0.7 exactly (no variation)
```

**Problem**: Most terms cluster at 0.85-1.0 weights. Insufficient differentiation between:
- Core problem terms (deserve 1.0)
- Strong related terms (deserve 0.8-0.9)
- Weak related terms (deserve 0.6-0.7)

**3. Topic-Specific Vocabulary Insufficient**

```
Core problem terms per topic:
- Educational:  8 terms  (brain drain, onderwijs-achterstand, schooluitval...)
- Governance:   7 terms  (corruptie, wantrouwen, patronage...)
- Economic:     5 terms  (armoede, werkloosheid...)
- Racism:      10 terms  (racisme, discriminatie, kleurisme...)
```

**Problem**: Only 5-10 core problem terms per topic. Need more **topic-specific vocabulary** that differentiates strong presence from weak presence.

---

## Solution Strategy: 4 Interventions

### Intervention 1: Reduce Uniform Term Weights (HIGH IMPACT)

**Rationale**: Geographic and era terms identify **scope** (Dutch Caribbean + slavery context), not **topic**. They should provide baseline presence, not dominate scores.

**Current weights**:
```csv
geography:   0.75
era_marker:  0.70
```

**Proposed v7 weights**:
```csv
geography:   0.50   (reduced from 0.75)
era_marker:  0.55   (reduced from 0.70)
```

**Expected impact**:
- Chunks mentioning "curaçao" + "1863" + "koloniale" get boost of ~0.50 + 0.55 + 0.55 = 1.60 (vs. 2.15 previously)
- **Reduces baseline floor** by ~0.55 units
- **Increases relative importance** of topic-specific terms
- **Should expand score ranges**: Strong topic chunks reach higher scores, weak chunks drop lower

**Implementation**:
```python
# In v7 dictionary, change all geography entries:
Educational Disadvantage & Brain Drain,curaçao,0.50,geography  # was 0.75
Educational Disadvantage & Brain Drain,bonaire,0.50,geography  # was 0.75
# ... etc for all geographic terms

# Change all era_marker entries:
Educational Disadvantage & Brain Drain,1863,0.55,era_marker  # was 0.70
Educational Disadvantage & Brain Drain,slavernijverleden,0.55,era_marker  # was 0.70
# ... etc for all era markers
```

---

### Intervention 2: Expand Weight Differentiation Within Topics (MEDIUM IMPACT)

**Rationale**: Create more granular differentiation between core, strong related, moderate related, and weak related terms.

**Current weight tiers** (5 tiers, narrow ranges):
```
1.0     Core problems
0.95    Core problems
0.9     Related
0.85    Related
0.8     Historical
```

**Proposed v7 weight tiers** (7 tiers, wider differentiation):
```
1.0     Core problems (absolutely central to topic)
0.90    Strong problems (clear problem vocabulary)
0.80    Related strong (domain vocabulary, strong association)
0.70    Related moderate (domain vocabulary, moderate association)
0.60    Related weak (peripheral terms, weak association)
0.55    Historical context (era markers)
0.50    Geographic context (geography markers)
```

**Example reclassification for Educational topic**:

```csv
# Current v6:
Educational Disadvantage & Brain Drain,brain drain,1.0,core_problem
Educational Disadvantage & Brain Drain,onderwijs-achterstand,1.0,core_problem
Educational Disadvantage & Brain Drain,emigratie,0.95,core_problem
Educational Disadvantage & Brain Drain,onderwijs,0.9,related
Educational Disadvantage & Brain Drain,papiamentu,0.9,related
Educational Disadvantage & Brain Drain,curriculum,0.85,related

# Proposed v7 (more differentiation):
Educational Disadvantage & Brain Drain,brain drain,1.0,core_problem           # unchanged (absolutely core)
Educational Disadvantage & Brain Drain,onderwijs-achterstand,1.0,core_problem # unchanged
Educational Disadvantage & Brain Drain,schooluitval,1.0,core_problem          # unchanged
Educational Disadvantage & Brain Drain,emigratie,0.95,strong_problem          # unchanged (strong but not absolute)
Educational Disadvantage & Brain Drain,onderwijsuitsluiting,0.95,strong_problem
Educational Disadvantage & Brain Drain,onderwijs,0.85,related_strong          # lowered from 0.9 (domain vocab, very relevant)
Educational Disadvantage & Brain Drain,school,0.85,related_strong
Educational Disadvantage & Brain Drain,papiamentu,0.80,related_strong         # lowered from 0.9 (relevant but also geographic)
Educational Disadvantage & Brain Drain,taal,0.80,related_strong
Educational Disadvantage & Brain Drain,curriculum,0.75,related_moderate       # lowered from 0.85 (relevant but generic)
Educational Disadvantage & Brain Drain,leerlingen,0.75,related_moderate
Educational Disadvantage & Brain Drain,studenten,0.70,related_moderate        # lowered from 0.85 (generic, not slavery-specific)
Educational Disadvantage & Brain Drain,emigreren,0.70,related_moderate
```

**Rationale for changes**:
- **1.0**: Only absolutely central problem terms (brain drain, onderwijsachterstand)
- **0.95**: Strong problem terms but not absolutely central (emigratie)
- **0.85**: Core domain vocabulary (onderwijs, school) - lowered slightly to differentiate from problems
- **0.80**: Relevant but also serve other functions (papiamentu is language but also geographic marker)
- **0.75**: Generic domain vocabulary (curriculum - could apply to education anywhere)
- **0.70**: Weak domain vocabulary (studenten - very generic)

**Expected impact**:
- Stronger differentiation between chunks with many core problem terms vs. chunks with only generic domain vocabulary
- **Score ranges expand** because weight spread is wider

---

### Intervention 3: Add Topic-Specific Problem Vocabulary (MEDIUM IMPACT)

**Rationale**: Expand dictionaries with more **topic-specific problem terms** to strengthen signal for strong chunks.

**Current vocabulary sizes**:
```
Educational:  45 terms (8 core_problem)
Governance:   39 terms (7 core_problem)
Economic:     39 terms (5 core_problem) ← WEAKEST
Racism:       43 terms (10 core_problem)
```

**Target vocabulary additions per topic**:

#### Educational (add ~10 terms)
```csv
Educational Disadvantage & Brain Drain,schoolachterstand,0.95,strong_problem
Educational Disadvantage & Brain Drain,onderwijskloof,0.95,strong_problem
Educational Disadvantage & Brain Drain,analfabetisme,0.90,strong_problem
Educational Disadvantage & Brain Drain,taalachterstand,0.90,strong_problem
Educational Disadvantage & Brain Drain,onderwijsongelijkheid,0.90,strong_problem
Educational Disadvantage & Brain Drain,voortijdig schoolverlaten,0.90,strong_problem
Educational Disadvantage & Brain Drain,kennismigratie,0.85,related_strong
Educational Disadvantage & Brain Drain,onderwijsachterstand,0.85,related_strong
Educational Disadvantage & Brain Drain,schoolprestaties,0.75,related_moderate
Educational Disadvantage & Brain Drain,onderwijssysteem,0.70,related_moderate
```

#### Governance (add ~10 terms)
```csv
Governance Distrust & Corruption,omkoping,0.95,strong_problem
Governance Distrust & Corruption,vriendjespolitiek,0.95,strong_problem
Governance Distrust & Corruption,machtsmisbruik,0.95,strong_problem
Governance Distrust & Corruption,bestuurlijke zwakte,0.90,strong_problem
Governance Distrust & Corruption,institutioneel wantrouwen,0.90,strong_problem
Governance Distrust & Corruption,gebrek aan transparantie,0.90,strong_problem
Governance Distrust & Corruption,democratisch tekort,0.90,strong_problem
Governance Distrust & Corruption,politieke afhankelijkheid,0.85,related_strong
Governance Distrust & Corruption,bestuurscultuur,0.75,related_moderate
Governance Distrust & Corruption,governance,0.70,related_moderate
```

#### Economic (add ~15 terms - PRIORITY, currently weakest)
```csv
Persistent Poverty & Economic Vulnerability,structurele armoede,0.95,strong_problem
Persistent Poverty & Economic Vulnerability,langdurige werkloosheid,0.95,strong_problem
Persistent Poverty & Economic Vulnerability,inkomensongelijkheid,0.95,strong_problem
Persistent Poverty & Economic Vulnerability,economische uitsluiting,0.95,strong_problem
Persistent Poverty & Economic Vulnerability,financiële kwetsbaarheid,0.90,strong_problem
Persistent Poverty & Economic Vulnerability,verborgen armoede,0.90,strong_problem
Persistent Poverty & Economic Vulnerability,minimuminkomens,0.85,related_strong
Persistent Poverty & Economic Vulnerability,arbeidsmarkt,0.80,related_strong
Persistent Poverty & Economic Vulnerability,economische structuur,0.80,related_strong
Persistent Poverty & Economic Vulnerability,inkomen,0.75,related_moderate
Persistent Poverty & Economic Vulnerability,werk,0.75,related_moderate
Persistent Poverty & Economic Vulnerability,banen,0.70,related_moderate
Persistent Poverty & Economic Vulnerability,economie,0.70,related_moderate
Persistent Poverty & Economic Vulnerability,financieel,0.70,related_moderate
Persistent Poverty & Economic Vulnerability,kosten,0.65,related_weak
```

#### Racism (add ~5 terms - already strongest)
```csv
Social Fragmentation & Racism,institutioneel racisme,0.95,strong_problem
Social Fragmentation & Racism,structureel racisme,0.95,strong_problem
Social Fragmentation & Racism,sociale ongelijkheid,0.90,strong_problem
Social Fragmentation & Racism,etnische discriminatie,0.90,strong_problem
Social Fragmentation & Racism,raciale hiërarchie,0.90,strong_problem
```

**Expected impact**:
- Chunks with strong problem presence score higher (more high-weight problem terms)
- Chunks with only generic vocabulary score lower
- **Economic topic improves** (currently worst performer in v16 evaluation)

---

### Intervention 4: Remove or Reduce Generic Shared Terms (LOW-MEDIUM IMPACT)

**Rationale**: Some terms appear across multiple topics because they're too generic, not because they're genuinely relevant to both.

**Terms to consider removing or reducing**:

```csv
# "plantage" appears in Economic AND Racism
# Decision: It's primarily historical economic structure, but also site of racial hierarchy
# Action: Keep in BOTH but reduce weight to 0.65 (was 0.90)

Persistent Poverty & Economic Vulnerability,plantage,0.65,related_weak  # was 0.90
Social Fragmentation & Racism,plantage,0.65,related_weak               # was 0.80

# "slavenhandel" appears in Economic AND Racism
# Decision: It's historical economic activity AND racial oppression
# Action: Keep in BOTH but reduce weight to 0.60

Persistent Poverty & Economic Vulnerability,slavenhandel,0.60,related_weak  # was 0.90
Social Fragmentation & Racism,slavenhandel,0.60,related_weak               # was 0.80

# "slavernij" appears in Economic AND Racism
# Decision: It's the historical system encompassing both
# Action: REMOVE from topic dictionaries (it's too broad for topic differentiation)
# Keep only in historical context if we later add Context_Era_Slavery dimension

# Remove these lines:
# Persistent Poverty & Economic Vulnerability,slavernij,0.8,historical
# Social Fragmentation & Racism,slavernij,0.8,historical

# "afschaffing" appears in Economic AND Racism
# Decision: Historical event, not problem vocabulary
# Action: Reduce weight significantly

Persistent Poverty & Economic Vulnerability,afschaffing,0.55,era_marker  # was 0.70, reclassify as era_marker
Social Fragmentation & Racism,afschaffing,0.55,era_marker               # was 0.85, reclassify as era_marker
```

**Rationale**:
- Terms like "slavernij" are too broad - they identify scope but don't differentiate topics
- Reduce their weights so they provide baseline context without dominating scores
- Focus dictionaries on **problem-specific vocabulary** that differentiates topics

**Expected impact**:
- Reduces cross-contamination between Economic and Racism topics
- Clearer topic differentiation

---

## Combined Expected Impact

### Score Range Predictions (v7 vs. v16)

**Current v16**:
```
Topic            Min     Max    Mean   Std
Educational:    0.004   0.637  0.281  0.082
Governance:    -0.031   0.553  0.293  0.091
Economic:       0.008   0.582  0.300  0.093
Racism:        -0.011   0.602  0.321  0.108
```

**Predicted v7 (after interventions)**:
```
Topic            Min     Max    Mean   Std    Improvement
Educational:    0.00    0.75   0.32   0.15   Max +0.11, Std +0.07
Governance:     0.00    0.72   0.30   0.14   Max +0.17, Std +0.05
Economic:       0.00    0.78   0.35   0.16   Max +0.20, Std +0.07
Racism:         0.00    0.80   0.36   0.17   Max +0.20, Std +0.06
```

**Why these predictions**:

1. **Max scores increase** (0.72-0.80 range):
   - Reduced uniform baseline → topic-specific terms have stronger relative impact
   - More high-weight problem vocabulary → chunks with many problem terms score higher
   - Better weight differentiation → strong chunks stand out more

2. **Std dev increases** (0.14-0.17 range):
   - Greater spread between strong chunks (0.7-0.8) and weak chunks (0.1-0.3)
   - Reduced uniform baseline → less compression around mean
   - Better differentiation → more variance in scores

3. **Means slightly increase** (0.30-0.36 range):
   - Adding problem vocabulary increases sensitivity to relevant chunks
   - But some chunks will drop (no longer boosted by high uniform weights)
   - Net effect: slight increase because improved vocabulary outweighs baseline reduction

### Confidence Classification Impact

**Current v16 distribution**:
```
High confidence (≥0.4, margin ≥0.05):  317 chunks (19.2%)
Low confidence  (≥0.2, margin ≥0.02):  861 chunks (52.1%)
None confidence (rest):                474 chunks (28.7%)
```

**Predicted v7 distribution**:
```
High confidence:  ~450 chunks (27%)   ← +133 chunks (+42%)
Low confidence:   ~750 chunks (45%)   ← -111 chunks (-13%)
None confidence:  ~450 chunks (27%)   ← -24 chunks (-5%)
```

**Why**:
- Expanded max scores (0.72-0.80) → more chunks reach 0.4 threshold
- Better differentiation → margins increase (easier to meet 0.05 requirement)
- More chunks become "trainable" with clear topic signals

### Pattern Quality Impact (72-chunk evaluation)

**Current v16 evaluation**:
```
Pattern quality:
- Excellent: 11.1%
- Good:      0.0%
- Fair:      13.9%
- Poor:      75.0%

Training sufficiency:
- Yes:       11.1%
- Marginal:  11.1%
- No:        77.8%
```

**Predicted v7 evaluation**:
```
Pattern quality:
- Excellent: 25%     ← +14%
- Good:      35%     ← +35%
- Fair:      25%     ← +11%
- Poor:      15%     ← -60%

Training sufficiency:
- Yes:       55%     ← +44%
- Marginal:  30%     ← +19%
- No:        15%     ← -63%
```

**Why**:
- Better score ranges → scores better match semantic judgment
- Reduced cross-contamination → topic differentiation clearer
- More problem vocabulary → strong topic presence scores higher

---

## Implementation Plan

### Phase 1: Create v7 Dictionary (4-6 hours)

**Step 1.1**: Apply weight reductions (30 min)
```python
# Script: adjust_uniform_weights_v7.py
# Change all geography entries: 0.75 → 0.50
# Change all era_marker entries: 0.70 → 0.55
```

**Step 1.2**: Expand weight tiers (1 hour)
```python
# Script: expand_weight_tiers_v7.py
# Reclassify existing terms using new 7-tier system
# Review each term's weight based on specificity/centrality
```

**Step 1.3**: Add topic-specific vocabulary (2-3 hours)
```python
# Script: add_problem_vocabulary_v7.py
# Add ~10 Educational terms
# Add ~10 Governance terms
# Add ~15 Economic terms (priority)
# Add ~5 Racism terms
```

**Step 1.4**: Remove/reduce generic shared terms (30 min)
```python
# Script: reduce_shared_terms_v7.py
# Remove "slavernij" from topic dictionaries
# Reduce "plantage", "slavenhandel" weights
# Reclassify "afschaffing" as era_marker
```

**Step 1.5**: Validate dictionary (30 min)
```python
# Script: validate_v7_dictionary.py
# Check: Total terms ~200-220 (vs. 166 in v6)
# Check: No duplicate terms except intentional geographic/era
# Check: Weight distribution follows 7-tier system
# Check: Each topic has 10-15 core/strong problem terms
```

**Output**: `problem_oriented_legacy_seed_v7_4topics.csv`

---

### Phase 2: Test on Evaluation Sample (2 hours)

**Step 2.1**: Score 72-chunk evaluation sample with v7
```python
# Script: score_eval_sample_v7.py
# Build topic vectors from v7 dictionary
# Score evaluation chunks
# Calculate score statistics
```

**Step 2.2**: Analyze score distributions
```python
# Check: Max scores reach 0.70-0.80?
# Check: Std dev increases to 0.14-0.17?
# Check: Score differentiation improved?
```

**Step 2.3**: Quick semantic check (manual)
- Review 20 chunks (5 per topic)
- Do high scores (>0.7) match strong topic presence?
- Do low scores (<0.3) match weak/absent topic presence?
- Do medium scores (0.4-0.6) match moderate presence?

**Decision point**: If score ranges expand and pattern quality improves → proceed to Phase 3. If not → iterate dictionary (adjust weights further).

---

### Phase 3: Full Corpus Scoring (3 hours)

**Step 3.1**: Score full slavery corpus with v7
```python
# Script: label_slavery_corpus_v7.py
# Score ~6,400 chunks with v7 dictionary
# Classify confidence levels
# Analyze distribution
```

**Step 3.2**: Compare v7 vs. v16 distributions
```
Metrics to compare:
- Score ranges (min, max, mean, std) per topic
- Confidence level distribution (high/low/none)
- Pattern type distribution (if using pattern classification)
- Number of chunks reaching 0.4 threshold
```

**Step 3.3**: Manual validation sample
- Select 100 chunks (25 per confidence level)
- Manual review: Do confidence classifications make sense?
- Check: Are high-confidence chunks genuinely strong on topic?

**Decision point**: If confidence distribution improves (more high-confidence, fewer none) → proceed to training. If not → iterate dictionary.

---

### Phase 4: Stratified Sampling & Training (Standard workflow)

Continue with standard v15 workflow:
1. Apply confidence-based stratified sampling
2. Train BERTje on slavery corpus
3. Use encoder to expand dictionary in policy space
4. Label policy corpus
5. Train final classifier
6. Apply to policy corpus
7. Thesis analysis

---

## Alternative: Multi-Topic High Confidence (If v7 Still Insufficient)

If v7 dictionary still results in many multi-topic moderate chunks classified as "none confidence", add this confidence category:

```python
# In confidence classification:

MULTI_TOPIC_HIGH = (
    (scores['Educational'] >= 0.35) AND
    (scores['Governance'] >= 0.35) AND
    (geographic_presence == True)  # Has Caribbean markers
)

OR

MULTI_TOPIC_HIGH = (
    (max_score >= 0.38) AND
    (2+ topics >= 0.32) AND
    (geographic_presence == True)
)

# Treat MULTI_TOPIC_HIGH same as single-topic HIGH in sampling
# → Include in 40% high-confidence pool
```

**Rationale**: Some chunks genuinely discuss multiple interconnected problems. These shouldn't be filtered as "noise" just because margin is low.

---

## Success Criteria (Before Proceeding to BERTje Training)

### Minimum Success (v7 dictionary adequate)
- [ ] Max scores reach ≥0.70 for at least one topic
- [ ] Std dev increases to ≥0.12 for all topics
- [ ] High confidence pool increases to ≥25% (from 19.2%)
- [ ] Manual review: ≥70% of high-confidence chunks genuinely strong on topic

### Optimal Success (v7 dictionary strong)
- [ ] Max scores reach 0.75-0.80 for all topics
- [ ] Std dev increases to ≥0.15 for all topics
- [ ] High confidence pool increases to ≥30%
- [ ] Pattern quality on evaluation sample: ≥60% Good/Excellent
- [ ] Training sufficiency on evaluation sample: ≥65% Yes

### If v7 Fails (Consider 8D or other alternatives)
- [ ] Max scores still <0.65 despite interventions
- [ ] Std dev doesn't increase (still <0.10)
- [ ] High confidence pool doesn't grow
- [ ] Pattern quality doesn't improve
- [ ] → Consider 8D hybrid approach OR different methodology entirely

---

## Timeline

**Total estimated time**: 11-17 hours

| Phase | Task | Time |
|-------|------|------|
| 1 | Create v7 dictionary | 4-6 hours |
| 2 | Test on evaluation sample | 2 hours |
| **Decision point** | Proceed or iterate? | 30 min |
| 3 | Full corpus scoring | 3 hours |
| 4 | Validation & comparison | 2 hours |
| **Decision point** | Proceed to training or iterate? | 30 min |

**Critical path**: Phase 2 decision point (6-8 hours). If evaluation sample doesn't show improvement, iterate dictionary before investing in full corpus scoring.

---

## Summary: Key Changes in v7

1. **Reduce uniform term weights**: Geography 0.75→0.50, Era markers 0.70→0.55
2. **Expand weight differentiation**: 5 tiers → 7 tiers (1.0, 0.95, 0.85, 0.80, 0.75, 0.70, 0.65...)
3. **Add problem vocabulary**: +40 terms (Educational +10, Governance +10, Economic +15, Racism +5)
4. **Reduce shared generic terms**: Lower "plantage", "slavenhandel", remove "slavernij" from topics

**Expected result**: Score ranges expand (max 0.72-0.80), better differentiation (std 0.14-0.17), more high-confidence chunks (27% vs. 19%), improved pattern quality (60%+ Good/Excellent).

**Risk mitigation**: Test on evaluation sample (72 chunks) before full corpus. Early decision point to iterate or proceed.

---

**Document by**: Claude (Sonnet 4.5)
**Date**: 2025-11-27
**Next step**: Implement Phase 1 (create v7 dictionary)
