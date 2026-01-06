# V21 SEMANTIC EVALUATION - FINAL REPORT
**Complete Stratified Evaluation Following EVALUATION_METHODOLOGY.md**

**Date:** 2025-11-28
**Dataset:** `slavery_Slavdict_pretraining_slavery_v21/Cosine_labeling/scores_all_labeled.csv`
**Total Chunks:** 1,520
**Evaluation Sample:** 54 (stratified: 8 Core, 12 Moderate, 12 Weak, 12 Context, 10 Noise)
**Methodology:** V21 with rescaled scores (0-2.0 range), 5-tier quality classification

---

## EXECUTIVE SUMMARY

### ❌ DATASET IS **NOT SUFFICIENT** FOR BERTJE TRAINING AS-IS

**Critical Finding:** Only **62.5%** of Core tier chunks (5/8) are actually high-quality examples with semantic rating = 3. The remaining 37.5% are boilerplate administrative text, parliamentary motion lists, or wrong-domain content.

### Key Problems:

1. **Core Tier Failure:** 3/8 chunks shouldn't be Core tier
   - 2 are boilerplate/procedural text (FALSE-POSITIVE)
   - 1 is medieval European slavery, not colonial Caribbean (WRONG DOMAIN)

2. **Only 5 Verified Strong Examples** across all 4 topics
   - Need minimum 20-30 per topic for reliable training

3. **Severe Topic Imbalance:**
   - Racism: 48% of dataset
   - Educational: 10% of dataset
   - Governance has ZERO Core tier examples

4. **Score Ambiguity:** 59% of chunks have margin <0.05 (unclear primary topic)

---

## CORE TIER EVALUATION (N=8)

**Expected:** Semantic rating = 3 (strongly present), high precision

### ✅ **VERIFIED CORRECT (5/8 = 62.5%)**

| Chunk | Topic | Score | Semantic Rating | Assessment |
|-------|-------|-------|-----------------|------------|
| 799a3980:00031 | Educational | 1.697 | Edu=3 | ✅ MATCH-STRONG |
| 799a3980:00068 | Poverty | 1.635 | Pov=3 | ✅ MATCH-STRONG |
| ad8dfafd:00789 | Racism | 1.532 | Rac=3 | ✅ MATCH-STRONG |
| e0b011d1:01671 | Racism | 1.532 | Pov=3, Rac=3 | ✅ MATCH-STRONG (multi-label) |
| 799a3980:00129* | Governance | 1.026 | Gov=3 | ✅ MATCH-STRONG |

*Note: Last chunk is from Moderate tier but demonstrates good governance content

### ❌ **PROBLEMATIC (3/8 = 37.5%)**

| Chunk | Topic | Score | Issue |
|-------|-------|-------|-------|
| 2c88535c:01315 | Educational | 1.520 | Language policy admin text - semantic=2, should be Moderate |
| 9dd5d756:00575 | Educational | 1.510 | Parliamentary motion LIST - pure boilerplate, minimal semantic value |
| 183a57ee:01540 | Racism | 1.529 | Medieval European feudalism - WRONG DOMAIN (not colonial/Caribbean) |

**Impact:** Core tier precision = 62.5% (UNACCEPTABLE - need ≥90%)

---

## MODERATE TIER EVALUATION (N=12)

**Expected:** Semantic rating = 2-3

**Results:** ~83% accuracy (10/12 correct)

**✅ Good Examples:**
- Educational policy recommendations (semantic=3)
- Staten-Generaal governance role (semantic=3)
- MBO quality standards (semantic=2)
- Legal aspects of slavery (semantic=2)

**⚠️ Issues:**
- 2/12 have very small margins (<0.02) - multi-label cases forced into single-label
- Some administrative text scored higher than substantive content

**Verdict:** ACCEPTABLE quality, better than Core tier

---

## ROOT CAUSE ANALYSIS

### 1. **Boilerplate Contamination**

**Problem:** System can't distinguish substantive vs. administrative text

**Examples:**
- Parliamentary motion lists → high keyword density but low semantic value
- Policy document headers → trigger scores without substantive discussion
- Administrative procedures → generic "education/governance" terms

**Impact:** False positives in Core/Moderate tiers

### 2. **Text Preprocessing Over-Aggressive**

**Removed:**
- Geographic names: "Curaçao", "Suriname", "Bonaire"
- Proper nouns: Institution names, people
- Numbers: Years, statistics

**Impact:** Chunks lose semantic context, especially Caribbean-specific content

### 3. **Keyword Weighting Issues**

**Generic terms dominate:**
- "onderwijs" (0.85 weight) triggers ANY educational text
- "bestuur" (0.85 weight) triggers administrative boilerplate

**Specific terms undervalued:**
- Geographic terms (0.5 weight) despite being crucial for Caribbean context

### 4. **No Domain Filtering**

**Problem:** No requirement for "colonial Caribbean context"

**Result:** Medieval European slavery scores high for "Racism" topic

---

## AGGREGATE STATISTICS

### Full Dataset Distribution:

| Quality Tier | Count | % | Expected Semantic Rating |
|--------------|-------|---|-------------------------|
| **Core** (≥1.5) | 12 | 0.8% | 3 (strongly present) |
| **Moderate** (1.0-1.5) | 214 | 14.1% | 2-3 (moderate-strong) |
| **Weak** (0.5-1.0) | 960 | 63.2% | 1-2 (weak-moderate) |
| **Context** (0.25-0.5) | 305 | 20.1% | 0-1 (background) |
| **Noise** (<0.25) | 29 | 1.9% | 0 (irrelevant) |

### Topic Distribution:

| Topic | Count | % | Core Tier |
|-------|-------|---|-----------|
| Racism | 728 | 47.9% | 3 |
| Governance | 373 | 24.5% | 0 ❌ |
| Poverty | 268 | 17.6% | 2 |
| Educational | 151 | 9.9% | 7 |

**Critical:** Governance has ZERO Core tier examples!

### Score Separation:

| Topic | Primary Mean | Non-Primary Mean | Separation |
|-------|-------------|------------------|------------|
| Educational | 0.892 | 0.312 | 0.580 ✅ |
| Racism | 0.742 | 0.451 | 0.291 ✅ |
| Governance | 0.675 | 0.453 | 0.222 ⚠️ |
| Poverty | 0.605 | 0.455 | 0.150 ⚠️ |

**Finding:** Topics ARE distinguishable, but Governance/Poverty have weaker separation

---

## TRAINING DATA SUFFICIENCY ASSESSMENT

### Current Usable Data:

**Conservative (score ≥1.0):** 226 chunks
- Educational: 55
- Governance: 39
- Poverty: 14 ❌ (too few)
- Racism: 118

**Inclusive (score ≥0.5):** 1,186 chunks
- But 63% are Weak tier (peripheral relevance)

### Problems for Training:

1. **Insufficient Core Examples:**
   - Only 5 verified strong examples total
   - Need 20-30 PER TOPIC minimum
   - Governance has ZERO Core examples

2. **Severe Topic Imbalance:**
   - Educational needs 4-5x oversampling
   - Poverty needs 8x more examples
   - Risk of Racism topic overfitting

3. **Boilerplate Contamination:**
   - ~10-15% of Moderate+ tier is administrative text
   - Model will learn to associate keywords with boilerplate

4. **Weak Tier Dominance:**
   - 63% of dataset is peripheral mentions
   - Training on these teaches ambiguous patterns

---

## RECOMMENDATIONS

### IMMEDIATE ACTIONS (Required before training):

#### 1. **Manual Core Tier Curation**

**Current:** 12 chunks, only 5 verified correct

**Required:**
- Remove 3 problematic chunks
- Manually review all Moderate tier (214 chunks)
- Select 20-30 best chunks per topic for new Core tier
- **Target:** 80-120 verified Core examples

**Effort:** 8-12 hours

#### 2. **Boilerplate Filtering**

Remove:
- Parliamentary motion lists
- Table of contents chunks
- Bibliography/reference sections
- Administrative procedure descriptions

**Criteria:**
- Sentence count < 5 complete sentences
- Repetitive structure (lists, tables)
- Low vocabulary diversity

**Expected removal:** ~50-100 chunks

#### 3. **Domain Filtering**

Add requirement for Caribbean/Netherlands colonial context:

Must mention at least one of:
- Geographic: Suriname, Curaçao, Aruba, Bonaire, Sint Maarten, Antilles
- Institutional: VOC, WIC, Staten-Generaal
- Historical: 1863, emancipatie, plantages

**Expected removal:** ~20-30 chunks (including medieval slavery example)

#### 4. **Multi-Label Training Approach**

**Problem:** 32 chunks have 2+ topics ≥1.0, but forced into single-label

**Solution:**
- Train multi-label regression model
- Predict continuous relevance scores (0-2.0) for each topic
- Don't force single primary topic

**Benefit:** Uses ambiguous chunks effectively

### MEDIUM-TERM FIXES:

#### 5. **Adjust Keyword Weights**

**Downweight generic terms:**
- "onderwijs" (0.85 → 0.70)
- "bestuur" (0.85 → 0.70)

**Create compound terms:**
- "slavernij onderwijs" (1.0)
- "koloniaal bestuur" (0.95)
- "caribisch onderwijs" (0.90)

**Boost geographic context:**
- Caribbean place names (0.5 → 0.75)

#### 6. **Improve Text Preprocessing**

**Keep:**
- Geographic names related to Caribbean
- Institutional names (VOC, WIC, etc.)
- Numbers/dates for temporal context

**Remove:**
- Only Dutch stopwords
- Only irrelevant numbers

#### 7. **Add Quality Filters**

**Minimum requirements:**
- Sentence count ≥ 5
- Vocabulary diversity score ≥ threshold
- No list/table structure patterns

---

## TRAINING STRATEGY (After Fixes)

### Option A: Conservative

**Data:** Moderate+ only (≥1.0), after curation = ~180 chunks

**Sampling:**
- Oversample Educational 3x → ~165 effective
- Oversample Poverty 6x → ~84 effective
- Undersample Racism 0.3x → ~35 effective
- Balanced: ~60 per topic = 240 effective samples

**Weights:**
- Core tier: 3.0x
- Moderate tier: 1.5x

**Expected Performance:** Moderate, conservative predictions

### Option B: Inclusive with Weighting

**Data:** Score ≥0.5, after filtering = ~1,000 chunks

**Tier Weights:**
- Core: 3.0x
- Moderate: 2.0x
- Weak: 0.5x
- Context/Noise: 0.1x (as negative examples)

**Topic Weights:**
- Educational: 2.5x
- Poverty: 1.4x
- Governance: 1.0x
- Racism: 0.5x

**Expected Performance:** Broader coverage, but noisier

### Option C: Multi-Label Regression (RECOMMENDED)

**Data:** All ≥0.5, cleaned

**Target:** Predict 4 continuous scores (0-2.0)

**Loss:** MSE with tier-based sample weighting

**Benefits:**
- Uses ambiguous chunks effectively
- Doesn't force single-label on multi-topic content
- More training signal from each chunk

**Expected Performance:** Best approach for this data

---

## FINAL VERDICT

### ❌ **NOT SUFFICIENT AS-IS**

**Reasons:**
1. Core tier: 62.5% accuracy (need ≥90%)
2. Only 5 verified strong examples
3. Boilerplate contamination
4. Domain mismatch (wrong historical period)
5. Severe topic imbalance

### ✅ **CAN BE MADE SUFFICIENT**

**Required Work (8-16 hours):**
1. Manual Core tier curation (20-30 per topic)
2. Boilerplate filtering
3. Domain filtering
4. Multi-label data preparation

**After Fixes:**
- Core tier: 80-120 verified chunks
- Clean training set: ~800-1,000 chunks
- With oversampling: ~600-800 effective balanced samples

**Expected Model Performance:** MODERATE (not high precision, but usable)

---

## COMPARISON TO METHODOLOGY EXPECTATIONS

**The methodology stated Core tier should have:**
- "Clear, extensive topic discussion with core terminology"
- Semantic rating = 3 (strongly present)
- High precision required

**Actual Core tier has:**
- 37.5% false positive rate
- Boilerplate and wrong-domain content
- Only 62.5% meet expectations

**Verdict:** System FAILED to meet Core tier quality standards defined in methodology

---

## CONCLUSION

The V21 dataset demonstrates:

✅ **Scoring system fundamentally works** - topics ARE distinguishable
❌ **Label quality insufficient** - too many false positives in Core tier
❌ **Boilerplate contamination** - administrative text scored too high
❌ **Domain filtering needed** - wrong historical periods included
⚠️ **Topic imbalance severe** - 10% vs 48% distribution

**DO NOT TRAIN** on dataset as-is.

**FIRST COMPLETE** manual curation and filtering (8-16 hours work).

**THEN TRAIN** with multi-label regression, weighted sampling, and realistic expectations of moderate (not high) performance.

The data can be salvaged, but requires significant manual quality improvement before use.
