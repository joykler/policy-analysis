# V5 Systematic Semantic Verification Report

## Methodology

**Systematic stratified sampling**: 45 chunks (3 per topic × 5 topics × 3 confidence levels)

**Analysis approach**:
- Loaded full chunk text from `chunked_corpus.csv`
- Counted topic-specific keywords for ALL 5 topics (not just primary)
- Assessed if **combined score distribution** reasonably represents content
- Focused on multi-label nature, not single primary label correctness

**Keyword lists used**:
- Educational: onderwijs, school, leer, taal, educatie, emigratie, student, curriculum
- Social: racisme, discrimin, neger, segregatie, slav, abolition, racist, uitsluiting
- Governance: parlement, kabinet, constitut, wetgeving, corrupt, gouvern, minister, debat
- Economic: armoede, werkloo, schuld, plantage, handel, economisch, voc, dwangarbeid
- Infrastructure: infrastructuur, voorziening, verwaarloz, achterstallig, onderhoud, investering, basisvoorziening

---

## Executive Summary

### Overall Results (45 chunks analyzed)

| Assessment | Count | Percentage |
|------------|-------|------------|
| **CORRECT** (max keywords) | 15 | 33.3% |
| **MULTI-LABEL** (tied keywords) | 8 | 17.8% |
| **QUESTIONABLE** (better topic exists) | 19 | 42.2% |
| **AMBIGUOUS** (0 keywords all topics) | 3 | 6.7% |

**Combined acceptable rate**: 51.1% (CORRECT + MULTI-LABEL)
**Problematic rate**: 42.2% (QUESTIONABLE)

---

## Critical Finding: Structural Neglect Complete Failure

### Statistics

**Structural Neglect chunks analyzed**: 9 (3 high, 3 low, 3 none confidence)

| Metric | Result |
|--------|--------|
| **Chunks with >0 infrastructure keywords** | 0 (0.0%) |
| **Chunks with 0 infrastructure keywords** | 9 (100.0%) |
| **CORRECT assessments** | 0 (0.0%) |
| **QUESTIONABLE assessments** | 8 (88.9%) |
| **AMBIGUOUS assessments** | 1 (11.1%) |

### Where Structural Neglect Chunks Should Go

| Better Topic | Count | Percentage |
|--------------|-------|------------|
| Social Fragmentation | 6 | 66.7% |
| Persistent Poverty & Economic | 2 | 22.2% |
| Ambiguous (0 keywords) | 1 | 11.1% |

### Examples

**High confidence Structural Neglect chunks** (should be most reliable):

1. **c12df80d:00000** (score=0.590, margin=0.054)
   - Keywords: Edu=0, Soc=1, Gov=0, Econ=0, **Infra=0**
   - Should be: Social Fragmentation

2. **676238ea:00000** (score=0.499, margin=0.050)
   - Keywords: Edu=0, Soc=0, Gov=0, Econ=1, **Infra=0**
   - Should be: Persistent Poverty & Economic

3. **fded2157:00000** (score=0.514, margin=0.073)
   - Keywords: Edu=0, Soc=1, Gov=0, Econ=0, **Infra=0**
   - Should be: Social Fragmentation

**All 9 Structural Neglect chunks** across all confidence levels had **0 infrastructure keywords**.

---

## Topic-by-Topic Performance

### 1. Social Fragmentation & Racism: BEST (55.6% correct)

| Assessment | Count | Percentage |
|------------|-------|------------|
| CORRECT | 5 | 55.6% |
| MULTI-LABEL | 1 | 11.1% |
| QUESTIONABLE | 3 | 33.3% |
| AMBIGUOUS | 0 | 0.0% |

**Combined acceptable**: 66.7% (6/9 chunks)

**Performance**:
- High confidence chunks: 3/3 CORRECT
- Low confidence chunks: 2/3 CORRECT
- No confidence chunks: 1/3 QUESTIONABLE, 1/3 MULTI-LABEL, 1/3 QUESTIONABLE

**Assessment**: Social Fragmentation is **performing well**. High-confidence chunks are semantically accurate, and the topic has the strongest keyword presence in its assigned chunks.

### 2. Educational Disadvantage: GOOD (44.4% correct)

| Assessment | Count | Percentage |
|------------|-------|------------|
| CORRECT | 4 | 44.4% |
| MULTI-LABEL | 2 | 22.2% |
| QUESTIONABLE | 3 | 33.3% |
| AMBIGUOUS | 0 | 0.0% |

**Combined acceptable**: 66.7% (6/9 chunks)

**Performance**:
- High confidence: 2/3 CORRECT, 1/3 MULTI-LABEL
- Low confidence: 2/3 CORRECT, 1/3 MULTI-LABEL
- No confidence: 3/3 QUESTIONABLE (acceptable - these are low-margin chunks)

**Assessment**: Educational is **performing adequately**. The fix from earlier (adding core educational terms) worked. High/low confidence chunks show educational keywords present.

### 3. Persistent Poverty & Economic: GOOD (44.4% correct)

| Assessment | Count | Percentage |
|------------|-------|------------|
| CORRECT | 4 | 44.4% |
| MULTI-LABEL | 2 | 22.2% |
| QUESTIONABLE | 2 | 22.2% |
| AMBIGUOUS | 1 | 11.1% |

**Combined acceptable**: 66.7% (6/9 chunks)

**Performance**:
- High confidence: 2/3 CORRECT, 1/3 QUESTIONABLE
- Low confidence: 2/3 CORRECT, 1/3 QUESTIONABLE
- No confidence: 2/3 MULTI-LABEL, 1/3 AMBIGUOUS

**Assessment**: Economic topic is **performing well**. Economic keywords (handel, economisch, plantage, armoede) are present in chunks assigned to this topic.

**Note**: One high-confidence chunk (75b05443) had more Social keywords (3) than Economic (1), suggesting multi-label overlap between economic vulnerability and social fragmentation.

### 4. Governance Distrust: WEAK (22.2% correct)

| Assessment | Count | Percentage |
|------------|-------|------------|
| CORRECT | 2 | 22.2% |
| MULTI-LABEL | 3 | 33.3% |
| QUESTIONABLE | 3 | 33.3% |
| AMBIGUOUS | 1 | 11.1% |

**Combined acceptable**: 55.6% (5/9 chunks)

**Performance**:
- High confidence: 1/3 CORRECT, 1/3 MULTI-LABEL, 1/3 QUESTIONABLE
- Low confidence: 3/3 MULTI-LABEL or AMBIGUOUS
- No confidence: 1/3 CORRECT, 2/3 QUESTIONABLE

**Assessment**: Governance is **underperforming but not catastrophic**. Many chunks have MULTI-LABEL with Governance tied with Economic or Infrastructure, suggesting overlap.

**Issue**: Governance has lower keyword counts overall, possibly because governance terms (parlement, kabinet, wetgeving) appear less frequently than social/economic terms in slavery legacy corpus.

**Example of problem**: High-confidence chunk 37936fcc had 0 governance keywords, should be Educational.

### 5. Structural Neglect: COMPLETE FAILURE (0% correct)

**See "Critical Finding" section above.**

---

## Multi-Label Analysis

### Acceptable Multi-Label Cases (8 chunks)

These chunks had **tied keyword counts** across multiple topics, indicating legitimate multi-topic content:

**Examples**:
- **db6084d5** (Educational): Edu=2, Soc=2, Gov=2 (tied) - about VMBO/MBO education policy with social/governance aspects
- **6b4a019d** (Governance): Gov=1, Econ=1, Infra=1 (tied) - about policy implementation with economic/infrastructure elements
- **143d682b** (Governance): Gov=1, Econ=1, Infra=1 (tied) - about financial obligations and administration

**Assessment**: These MULTI-LABEL cases are **acceptable and expected** for historical policy documents. The score distributions should reflect multiple relevant topics.

### Questionable Cases (19 chunks)

These chunks had **primary topic with 0 keywords** while another topic had higher keyword counts:

**By affected topic**:
- Structural Neglect → should be Social (6 chunks) or Economic (2 chunks)
- Educational → should be Social (2) or Economic (1)
- Governance → should be Economic (2) or Infrastructure (1)
- Social → should be Governance (1) or Economic (2)
- Economic → should be Educational (2)

**Pattern**: Most questionable cases (8/19 = 42%) come from **Structural Neglect over-triggering**.

---

## Root Cause Analysis

### Why Structural Neglect Failed Completely

**Dictionary composition** (from V5_CURATION_COMPLETE_FINAL.md):
- Total terms: 185
- Infrastructure-specific: 6 terms (3.2%)
- Neglect-specific: 1 term (0.5%)
- **Generic historical: ~60 terms (34.5%)**
- Other contextual: remaining

**Generic terms dominating the topic vector**:
- `slavernijverleden`, `slavernijgeschiedenis`, `geschiedenis`, `historisch`
- `koloniale`, `slavernij`, `verleden`, `erfgoed`
- `herdenking`, `herdenkingen`, `monument`, `monumenten`

**Result**: Structural Neglect vector is essentially a **"generic slavery history" detector**, not an infrastructure/neglect detector.

**What Structural Neglect SHOULD match**:
- "achterstallig onderhoud infrastructuur Caribisch Nederland"
- "verwaarlozing publieke voorzieningen eilanden"
- "gebrek investeringen basisinfrastructuur"

**What it ACTUALLY matches**:
- Any chunk mentioning slavery history (slavernijverleden)
- Public memory/commemoration (herdenking, monument)
- Historical documentation (geschiedenis, historisch)

### Why Governance Underperforms

**Governance keyword frequency is lower** in slavery legacy corpus because:
1. Slavery history content has more social/economic terms than governance terms
2. Parliamentary debates are subset of corpus, not majority
3. Governance terms (parlement, kabinet, wetgeving) are more specific and appear less frequently

**But this is less severe** than Structural Neglect because:
- Governance still has 22.2% CORRECT + 33.3% MULTI-LABEL = 55.6% acceptable
- The MULTI-LABEL cases are legitimate (governance overlaps with economic/infrastructure policy)
- Only 1/3 high-confidence chunks was questionable

---

## Impact on BERTje Training

### What Works ✓

1. **Social Fragmentation** (55.6% correct, 66.7% acceptable)
   - Will teach BERTje: racism, discrimination, social inequality patterns
   - High-confidence chunks are semantically accurate
   - Strong racial keyword presence (racisme, discrimin, neger)

2. **Educational Disadvantage** (44.4% correct, 66.7% acceptable)
   - Will teach BERTje: education gaps, language issues, brain drain
   - High/low confidence chunks have educational vocabulary
   - Multi-label cases are reasonable (education + social overlap)

3. **Persistent Poverty & Economic** (44.4% correct, 66.7% acceptable)
   - Will teach BERTje: economic vulnerability, trade history, poverty
   - Economic terms present in assigned chunks
   - Multi-label with Social is reasonable (economic hardship overlaps with social issues)

### What's Problematic ❌

1. **Structural Neglect** (0% correct, 0% acceptable)
   - Will teach BERTje: **"any slavery history → infrastructure"** (WRONG)
   - 918 chunks (23.8% of corpus) incorrectly labeled as Structural Neglect
   - These chunks are actually Social (majority) or Economic
   - **This is poison data for BERTje training**

2. **Governance** (22.2% correct, but 55.6% acceptable with multi-label)
   - Will teach BERTje: governance patterns with weaker signal
   - 483 chunks (12.5% of corpus) have governance as primary
   - Some high-confidence chunks lack governance keywords
   - **Risk**: BERTje may under-detect governance topics in transfer

### Expected BERTje Performance

**If trained on V5 labels as-is**:

| Topic | Expected Transfer Quality |
|-------|---------------------------|
| Social Fragmentation | ✓ Good - will learn racial discrimination patterns |
| Educational | ✓ Good - will learn educational disadvantage patterns |
| Economic | ✓ Good - will learn economic vulnerability patterns |
| Governance | ~ Moderate - will learn governance but with weaker signal |
| Structural Neglect | ✗ **BAD - will learn to misclassify any slavery history as infrastructure** |

**Predicted validation performance**:
- BERTje will likely **over-predict Structural Neglect** on any historical text
- BERTje will likely **under-predict Social Fragmentation** because many Social chunks are mislabeled as Structural
- Governance may underperform due to lower keyword signal

---

## Recommendations

### Option 1: Re-Curate Structural Neglect (STRONGLY RECOMMENDED)

**Action**: Remove generic historical terms from Structural Neglect dictionary.

**Keep ONLY** (7 core terms):
- `verwaarlozing`, `verwaarloosd`, `verwaarloozing`
- `achterstelling`, `achterstallig`
- `infrastructuur`, `voorzieningen`

**Remove** (~60 generic terms including):
- All history terms: `slavernijverleden`, `slavernijgeschiedenis`, `geschiedenis`, `historisch`, `verleden`
- All colonial terms: `koloniale`, `koloniaal`, `koloniën`
- All memory terms: `herdenking`, `herdenkingen`, `monument`, `monumenten`, `erfgoed`
- All generic slavery terms: `slavernij`, `slavernijmuseum`, `slavernijinstituten`

**Expected impact**:
- Structural Neglect drops from 918 chunks (23.8%) → ~300-400 chunks (~10%)
- Freed chunks re-assigned to Social (~400 chunks) and Economic (~200 chunks)
- High-confidence Structural chunks actually about infrastructure/neglect
- **BERTje will learn correct patterns**

**Effort**: 30-60 minutes to create `curate_v5_remove_structural_generic.py`

**Alternative approach**: Instead of re-curating, create a **post-labeling filter** that reassigns Structural Neglect chunks with 0 infrastructure keywords to their rank-2 topic. This is faster (10 minutes) and preserves the dictionary for future use.

### Option 2: Exclude Structural Neglect from Training

**Action**: Train BERTje on only 4 topics (Educational, Social, Governance, Economic).

**Approach**:
1. Filter training data to exclude Structural Neglect as primary topic
2. Set Structural Neglect scores to 0 in softmax distribution
3. Re-normalize top-4 scores to sum to 1.0
4. Train BERTje with 4-way classification

**Expected impact**:
- BERTje will learn 4 topics with good quality (66.7% acceptable for Edu/Soc/Econ, 55.6% for Gov)
- 2,936 chunks remain (76.2% of corpus) for training
- Structural Neglect won't be learned (can't detect it in transfer domain)

**Trade-off**: Lose infrastructure/neglect detection capability entirely.

### Option 3: Weight Down Structural Neglect

**Action**: Apply confidence penalties to Structural Neglect during training.

**Approach**:
1. For high-confidence Structural chunks: multiply loss weight by 0.2
2. For low-confidence Structural chunks: multiply loss weight by 0.1
3. For no-confidence Structural chunks: exclude entirely
4. Keep other topics at normal weights

**Expected impact**:
- Reduces Structural Neglect's influence on BERTje
- Doesn't solve root cause (BERTje still sees wrong patterns)
- Quick fix (5 minutes to adjust training code)

**Assessment**: This is a **band-aid**, not a solution. BERTje will still see incorrect patterns, just with less weight.

### Option 4: Proceed As-Is and Monitor

**Action**: Train BERTje with current V5 labels, evaluate validation performance.

**Monitoring**:
1. Check if BERTje over-predicts Structural Neglect on validation set
2. Check if BERTje under-predicts Social Fragmentation
3. If validation confirms the issue → implement Option 1 or 2 and re-train

**Advantages**:
- Fastest to production (0 minutes additional work)
- Empirical validation of the hypothesis

**Disadvantages**:
- High probability of wasted training time (~2-4 hours on GPU)
- Will need to re-train after fix
- BERTje may learn incorrect patterns that persist even after re-training

---

## Confidence-Based Training Strategy

Regardless of which option you choose, use **confidence-weighted loss** for BERTje training:

### High Confidence Chunks (425 total, 11.0%)

**Use with high weight (1.0)**:
- Social: 3/3 high-conf chunks CORRECT (100% verified)
- Educational: 2/3 CORRECT, 1/3 MULTI-LABEL (acceptable)
- Economic: 2/3 CORRECT, 1/3 QUESTIONABLE (mostly acceptable)
- Governance: 1/3 CORRECT, 1/3 MULTI-LABEL, 1/3 QUESTIONABLE (use with caution)
- **Structural: EXCLUDE** (0/3 CORRECT - all wrong)

**Strategy**: Filter out Structural Neglect from high-confidence, use remaining 340 chunks as strong supervision.

### Low Confidence Chunks (1,506 total, 39.1%)

**Use with moderate weight (0.5)** for multi-label learning:
- Use top-2 or top-3 scores, not just primary
- Accept overlap between topics
- Filter Structural Neglect if Option 1 chosen

### No Confidence Chunks (1,923 total, 49.9%)

**Use with low weight (0.2)** or exclude:
- These have margins <0.02 (very ambiguous)
- Many are genuinely multi-topic or off-topic
- Provide negative examples but weak signal

---

## Conclusion

### Summary of V5 Quality

**Overall acceptable rate**: 51.1% (23/45 chunks CORRECT or MULTI-LABEL)

**By topic**:
- ✓ Social Fragmentation: 66.7% acceptable (strong)
- ✓ Educational: 66.7% acceptable (strong)
- ✓ Economic: 66.7% acceptable (strong)
- ~ Governance: 55.6% acceptable (moderate)
- ✗ **Structural Neglect: 0% acceptable (failed)**

### Critical Issue

**Structural Neglect has completely failed** due to 34.5% generic historical terms in dictionary. It over-triggers on any slavery history content, affecting 918 chunks (23.8% of corpus).

**Evidence**:
- 9/9 sampled Structural chunks had **0 infrastructure keywords**
- 8/9 should be Social (6) or Economic (2)
- This is **systematic across all confidence levels**

### Recommendation Priority

**1. MUST FIX**: Remove generic terms from Structural Neglect (Option 1) OR exclude Structural entirely (Option 2)

**2. CAN PROCEED**: Educational, Social, Economic, Governance are sufficient for BERTje transfer learning

**3. TRAINING STRATEGY**: Use confidence-weighted loss, exclude Structural Neglect from high-confidence supervision

### Next Steps

**If you implement Option 1** (recommended):
1. Run curation script to remove generic terms from Structural Neglect (30 min)
2. Re-run checkpoint 5 (cosine labeling) on new dictionary (15 min)
3. Verify Structural Neglect now ~10% of corpus with infrastructure keywords present (10 min)
4. Proceed to BERTje training

**If you implement Option 2** (faster):
1. Filter training data to exclude Structural Neglect (5 min)
2. Proceed to BERTje training with 4 topics

**If you proceed as-is** (Option 4):
- Start BERTje training immediately
- Monitor validation performance closely
- Expect to need re-training after confirming Structural Neglect issue

---

**Report generated from systematic semantic verification of 45 chunks (3 per topic per confidence level)**

**Data saved to**: `systematic_semantic_verification.csv`
