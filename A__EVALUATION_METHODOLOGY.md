# SEMANTIC EVALUATION METHODOLOGY
## Proper Multi-Label Assessment for Dictionary Cosine Labeling

**Version:** V21 (Updated for Rescaled Scores & Weight Differentiation)
**Date:** 2025-11-28

---

## CORE PRINCIPLE

**You must READ the full text semantically, not just search for keywords.**

Keyword matching misses:
- Context and meaning
- Paraphrasing and synonyms
- Implicit references
- Overall semantic theme
- Nuanced multi-topic content

---

## CRITICAL: UNDERSTANDING THE SCORING SYSTEM

### Two Score Systems in V21

The current system provides **two parallel scoring systems**:

#### 1. Original Cosine Scores (`cos_*` columns)
- Raw cosine similarity between chunk and topic vectors
- **Compressed range**: ~0.14 to 0.62 (narrow spread)
- **Legacy system**: Preserved for backward compatibility
- **Do NOT use for evaluation** - use rescaled scores instead

#### 2. Rescaled Scores (`rescaled_*` columns) **← USE THESE**
- Transformed using power function (1.8) + margin bonus
- **Interpretable range**: 0 to 2.0
- **Better spread**: 4x improvement over original cosine
- **Primary metric**: `max_score_rescaled` and `max_rescaled`

### Five-Tier Quality Classification

All chunks are classified into **5 quality tiers** based on `max_score_rescaled`:

| Tier | Score Range | Meaning | Use Case |
|------|-------------|---------|----------|
| **Core** | 1.5 - 2.0 | High-quality topic content | Premium training data |
| **Moderate** | 1.0 - 1.5 | Clearly relevant | Standard training data |
| **Weak** | 0.5 - 1.0 | Peripheral mentions | Background context |
| **Context** | 0.25 - 0.5 | Background only | Negative examples |
| **Noise** | 0 - 0.25 | Irrelevant/noise | **Filter out** |

### Keyword Weight System

**Not all keywords are equal.** The dictionary uses differentiated weights (0.5 - 1.0):

| Weight | Type | Examples |
|--------|------|----------|
| **1.0** | Core terms | "racisme", "discriminatie", "armoede", "werkloosheid" |
| **0.95** | Strong terms | "nepotisme", "structureel racisme", "segregatie" |
| **0.85** | Moderate terms | "onderwijs", "bestuur", "economisch", "plantages" |
| **0.75** | Supporting terms | "curriculum", "minister", "handel", "emancipatie" |
| **0.55** | Contextual terms | "geschiedenis", "historisch", "koloniaal", "slavernijverleden" |
| **0.5** | Geographic terms | "suriname", "curaçao", "bonaire", "caribisch nederland" |

**Impact on scoring:**
- Core terms (1.0) have 2x weight of geographic terms (0.5)
- Chunks with core terms score higher than chunks with only contextual terms
- SIF weighting also applied (rare terms boosted, common terms downweighted)

### Text Preprocessing

**IMPORTANT:** The system scores `text_for_scoring`, NOT `raw_text`.

**What you read (raw_text):**
```
"De economische situatie in Suriname blijft uitdagend. In 2023 was de werkloosheid hoog."
```

**What the system scores (text_for_scoring):**
```
"economische situatie uitdagend werkloosheid hoog"
```

**Removed during preprocessing:**
- Dutch stopwords ("de", "in", "was", "de")
- Numbers ("2023")
- Geographic names ("Suriname") - unless they're topic keywords
- English words (if detected)
- Non-word tokens

**NOT removed:**
- Stemming is disabled (original word forms preserved)

---

## STEP-BY-STEP EVALUATION PROTOCOL

### 1. Sample Selection

**Stratify by quality tier** (not old confidence levels):

Sample 3-5 chunks per tier × 4 topics = 60-80 samples:
- **Core tier** (12-20 samples): Expect very clear topic content
- **Moderate tier** (12-20 samples): Expect relevant but less central
- **Weak tier** (12-20 samples): Expect peripheral mentions
- **Context tier** (12-20 samples): Expect background/setup only
- **Noise tier** (12-20 samples): Expect truly irrelevant chunks

**Stratify across topics** to ensure each topic is evaluated.

### 2. For Each Chunk: READ FULLY

**Do not keyword search. Read the entire `raw_text` as a human would.**

Ask yourself:
1. What is this text actually about?
2. What are the main themes and subjects discussed?
3. Which of the 4 topics are genuinely present in the semantic content?

**Note:** You are reading `raw_text`, but the system scored `text_for_scoring`. Keep in mind that stopwords, numbers, and geographic names were removed before scoring.

### 3. Topic Definitions (for reference)

**Educational Disadvantage & Brain Drain:**
- Educational inequality, school quality, language barriers in education
- Educational migration (brain drain), emigration of educated people
- Teacher shortages, curriculum issues, literacy
- Educational achievement gaps, access to education

**Governance Distrust & Corruption:**
- Government corruption, nepotism, patronage systems
- Distrust in political institutions, governance failures
- Colonial/postcolonial governance structures, autonomy struggles
- Political control, administration problems, institutional issues

**Persistent Poverty & Economic Vulnerability:**
- Economic hardship, poverty, unemployment, debt
- Economic dependency, economic exploitation
- Plantation economies, trade systems, forced labor
- Economic vulnerability, financial insecurity

**Social Fragmentation & Racism:**
- Racial discrimination, racism, prejudice based on race/ethnicity
- Segregation, social exclusion, racial hierarchies
- Emancipation struggles, abolition movements
- Social legacy of slavery, identity and belonging issues

### 4. Rate Semantic Presence (0-3 scale)

For each of the 4 topics, rate its semantic presence:

| Rating | Meaning | When to Use |
|--------|---------|-------------|
| **0** | Not present | Topic not mentioned or discussed |
| **1** | Weakly present | Tangential mention, minor aspect |
| **2** | Moderately present | Clear discussion but not central theme |
| **3** | Strongly present | Central theme, extensively discussed |

**Important:** This is subjective human judgment based on full-text reading.

### 5. Compare to Rescaled Scores

**Use RESCALED scores, not original cosine scores.**

**Relevance thresholds:**
- **Core content**: rescaled score ≥ 1.5
- **Moderate content**: rescaled score ≥ 1.0
- **Weak content**: rescaled score ≥ 0.5
- **Noise**: rescaled score < 0.25

Compare:
- **System-detected topics:** Which topics have rescaled score ≥ 1.0?
- **Semantically-present topics:** Which topics you rated ≥ 2?
- **Overlap:** Do they match?

**Check primary_topic assignment:**
- `primary_topic_rescaled`: Which topic has highest rescaled score?
- Does this match your semantic assessment?

### 6. Quality Assessment

| Quality Label | Meaning | Updated Criteria |
|--------------|---------|------------------|
| **MATCH-STRONG** | Rescaled score ≥ 1.5 AND semantic rating = 3 | Perfect match, high quality |
| **MATCH-MODERATE** | Rescaled score 1.0-1.5 AND semantic rating = 2 | Good match, relevant content |
| **MATCH-WEAK** | Rescaled score 0.5-1.0 AND semantic rating = 1 | Correct weak signal detection |
| **CORRECT-NOISE** | Rescaled score < 0.25 AND semantic rating = 0 | Correctly filtered irrelevant |
| **MISMATCH-MISSING** | Semantic rating ≥ 2 BUT rescaled score < 1.0 | Dictionary gap, missed content |
| **FALSE-POSITIVE** | Rescaled score ≥ 1.5 BUT semantic rating ≤ 1 | Spurious high score |
| **TIER-MISMATCH** | Score tier doesn't match semantic strength | Classification issue |

**Multi-label assessment:**
- A chunk can be relevant to multiple topics
- Check if ALL semantically-present topics (rated ≥ 2) have rescaled scores ≥ 1.0
- Check if any topics with low semantic presence (rated 0-1) have high rescaled scores (≥ 1.5)

---

## EXAMPLE EVALUATION (UPDATED FOR V21)

### Sample Chunk from CSV:

**Chunk ID:** `1bc69fae:00001`

**Raw text (abbreviated):**
> "De ongelukkige contractarbeider Johannis Catheau schrijft in 1658 vanuit Barbados aan zijn ouders in Leiden dat hij 'als een slaef' is verkocht... Nu zullen sommigen zeggen: 'Zie je wel, die slavernij was echt niet alleen iets van Europeanen die Afrikanen tot slaaf maakten.' ...Maar het meer relevante verhaal is dat de Europeanen de slavernij in de Cariben en ook elders in de wereld al snel reserveerden voor mensen die níet wit waren. En daar is een woord voor: racisme."

**Rescaled scores:**
- Educational: 0.604
- Governance: 0.604
- Poverty: 0.446
- **Racism: 0.869** ✓ (highest)

**Primary topic (rescaled):** Social Fragmentation & Racism

**Quality tier:** Weak (score 0.869 in 0.5-1.0 range)

---

### Step 1: READ and understand

This text discusses:
- Historical slavery (contract labor vs chattel slavery)
- Racialization of slavery (Europeans reserved slavery for non-white people)
- Explicit mention of "racisme" as core concept
- Historical context of Caribbean slavery
- Commentary on how slavery became racially defined

### Step 2: Semantic ratings

- **Educational:** 0 (not discussed)
- **Governance:** 0 (not discussed, though colonial systems mentioned tangentially)
- **Poverty:** 1 (weak - mentions exploitation, labor systems, but not economic focus)
- **Racism:** 3 (strong - CENTRAL theme, explicitly names racism, discusses racial hierarchy)

### Step 3: Rescaled scores (from CSV)

- Educational: 0.604 (Weak tier)
- Governance: 0.604 (Weak tier)
- Poverty: 0.446 (Context tier)
- **Racism: 0.869** (Weak tier) ✓ (highest score)

### Step 4: Compare

- **System detected (≥ 1.0):** NONE (all scores below 1.0)
- **Semantic present (≥ 2):** Racism (rated 3)
- **Primary topic:** Racism ✓ (correct assignment)
- **Tier:** Weak (0.869)

### Step 5: Quality assessment

**Label:** TIER-MISMATCH / MISMATCH-MISSING

**Analysis:**
- ✅ Correct primary topic: Racism identified
- ❌ Score too low: Semantic rating = 3 (strongly present), but rescaled score = 0.869 (Weak tier)
- ❌ Should be Core tier (≥ 1.5): Text explicitly discusses racism, uses the word "racisme"
- ❌ Educational/Governance scores too high: Both 0.604 despite rating 0

**Possible reasons:**
1. **Text preprocessing removed key context**: "Europeanen", "Afrikanen", "Cariben" may have been removed as geographic/proper nouns
2. **Keyword weights**: "racisme" (1.0 weight) is present, but surrounding context removed
3. **SIF downweighting**: "racisme" might be common in corpus, reducing its impact
4. **Short text with high preprocessing loss**: Much content removed, reducing signal

**Recommendation:**
- Add compound terms: "raciale slavernij", "racialisering slavernij"
- Boost weight for explicit terminology combinations
- Review text preprocessing - may be removing too much relevant context

---

## QUALITY TIER INTERPRETATION

### Core Tier (1.5 - 2.0)
- **Expected:** Clear, extensive topic discussion with core terminology
- **Semantic rating:** Should mostly be 3 (strongly present)
- **Evaluation:** High precision required - false positives here are critical errors

### Moderate Tier (1.0 - 1.5)
- **Expected:** Clear topic relevance, moderate discussion
- **Semantic rating:** Should mostly be 2-3
- **Evaluation:** Standard quality - should reliably detect topic presence

### Weak Tier (0.5 - 1.0)
- **Expected:** Peripheral mentions, tangential relevance
- **Semantic rating:** Should mostly be 1-2
- **Evaluation:** Borderline cases - manual review recommended

### Context Tier (0.25 - 0.5)
- **Expected:** Background context, setup, introductions
- **Semantic rating:** Should mostly be 0-1
- **Evaluation:** Not suitable for training - use as negative examples

### Noise Tier (0 - 0.25)
- **Expected:** Completely irrelevant (tables of contents, bibliographies, boilerplate)
- **Semantic rating:** Should be 0 for all topics
- **Evaluation:** Should be filtered out completely - check for false negatives

---

## COMMON PITFALLS TO AVOID

### ❌ DON'T: Use Original Cosine Scores
```
Bad: "Educational scored 0.361, so it's above the 0.40 threshold"
```

### ✅ DO: Use Rescaled Scores
```
Good: "Educational rescaled score is 0.604 (Weak tier), below the 1.0 Moderate threshold"
```

### ❌ DON'T: Ignore Text Preprocessing
```
Bad: "This text mentions 'Suriname' multiple times, so Poverty should score high"
```

### ✅ DO: Consider What Was Actually Scored
```
Good: "Geographic terms like 'Suriname' (0.5 weight) were likely downweighted or removed,
so score is based on remaining economic/poverty terms"
```

### ❌ DON'T: Expect All Keywords Equal
```
Bad: "The text has both 'geschiedenis' and 'racisme', so they contribute equally"
```

### ✅ DO: Account for Weight Differences
```
Good: "'racisme' (1.0 weight) contributes 2x more than 'geschiedenis' (0.55 weight)"
```

### ❌ DON'T: Ignore Quality Tiers
```
Bad: "Score is 0.8, so it's relevant"
```

### ✅ DO: Interpret by Tier
```
Good: "Score is 0.8 (Weak tier) - peripheral relevance, needs manual review before use"
```

---

## REPORTING RESULTS

### Aggregate Metrics

**Overall Accuracy by Tier:**
```
Core tier accuracy = (MATCH-STRONG + MATCH-MODERATE) / Total Core chunks
Moderate tier accuracy = (MATCH-MODERATE + MATCH-STRONG) / Total Moderate chunks
Weak tier accuracy = (MATCH-WEAK + MATCH-MODERATE) / Total Weak chunks
Noise tier accuracy = (CORRECT-NOISE) / Total Noise chunks
```

**Precision and Recall:**
```
Precision (Core tier) = True Positives / (True Positives + False Positives)
  - TP: Chunks in Core tier with semantic rating = 3
  - FP: Chunks in Core tier with semantic rating ≤ 2

Recall (semantic rating 3) = True Positives / (TP + False Negatives)
  - TP: Chunks rated 3 that are in Core/Moderate tier
  - FN: Chunks rated 3 that are in Weak/Context/Noise tier
```

**Tier Mismatch Rate:**
```
TIER-MISMATCH = Chunks where quality tier doesn't align with semantic rating
Example: Semantic rating 3 but in Weak/Context tier (should be Core)
```

**False Positive Rate (Critical):**
```
FALSE-POSITIVE = Chunks in Core tier with semantic rating ≤ 1
This indicates serious scoring problems
```

**Missing Content Rate:**
```
MISMATCH-MISSING = Chunks with semantic rating ≥ 2 but rescaled score < 1.0
Indicates dictionary gaps or preprocessing issues
```

### Qualitative Insights

For each **MISMATCH-MISSING** case:
- What semantic content was present?
- Which keywords were in `text_for_scoring` vs `raw_text`?
- Why might the dictionary have missed it?
  - Missing keywords?
  - Keywords present but low weight (0.5-0.55)?
  - Text preprocessing removed key terms?
- What terms/concepts should be added or reweighted?

For each **FALSE-POSITIVE** case:
- Why did it score high despite no semantic content?
- Which keywords triggered the score?
- Are dictionary terms too generic? (e.g., "geschiedenis", "historisch")
- Are generic/contextual terms (0.5-0.55 weight) dominating the score?
- Should these terms be downweighted or removed?

For **TIER-MISMATCH** cases:
- Is the semantic rating accurate?
- Should this chunk be in a higher/lower tier?
- What would improve tier alignment?
  - Keyword additions?
  - Weight adjustments?
  - Threshold tuning?

### Analysis by Topic

Report separately for each of the 4 topics:
- Which topic has best Core tier precision?
- Which topic has most false positives?
- Which topic has most missing content?
- Which topics benefit from high-weight keywords (1.0)?
- Which topics suffer from over-reliance on contextual terms (0.5-0.55)?

### Noise Tier Analysis

**Critical validation:**
1. What proportion of Noise tier are truly irrelevant? (CORRECT-NOISE)
2. Are any high-quality chunks incorrectly in Noise tier? (FALSE-NEGATIVE check)
3. What types of content end up in Noise tier?
   - Table of contents
   - Bibliographies
   - Headers/footers
   - Generic policy boilerplate
   - Truly off-topic content
4. Should Noise threshold (0.25) be adjusted?

---

## REMEMBER: EVALUATION METHOD (V21 UPDATED)

✅ **Sample** by quality tier (Core/Moderate/Weak/Context/Noise)
✅ **Read** full `raw_text` semantically (no keyword matching)
✅ **Rate** all 4 topics independently (0-3 scale)
✅ **Compare** semantic ratings (≥2) vs. rescaled scores (≥1.0, not ≥0.40!)
✅ **Check** primary topic assignment against highest semantic rating
✅ **Understand** text preprocessing removes stopwords, numbers, geographic names
✅ **Account** for keyword weights (0.5-1.0 range, not equal)
✅ **Multi-label** approach - chunks can be relevant to 0-4 topics
✅ **Use** 5-tier quality classification (Core/Moderate/Weak/Context/Noise)

---

## VALIDATION CHECKLIST

Before finalizing evaluation:

- [ ] Did you use **rescaled scores**, not original cosine scores?
- [ ] Did you READ every chunk's `raw_text` fully, not just skim?
- [ ] Did you assess all 4 topics independently for each chunk?
- [ ] Did you ignore the `primary_topic_rescaled` label during initial assessment?
- [ ] Did you use the 0-3 semantic rating scale?
- [ ] Did you compare semantic (≥2) with rescaled scores (≥1.0)?
- [ ] Did you check quality tier alignment (Core chunks should have rating 3)?
- [ ] Did you check Noise tier chunks for false negatives?
- [ ] Did you note which keywords were likely removed during preprocessing?
- [ ] Did you consider keyword weight differences (1.0 vs 0.5)?
- [ ] Did you note specific examples of mismatches with explanations?
- [ ] Did you calculate accuracy by quality tier?
- [ ] Did you analyze tier mismatches (semantic rating vs actual tier)?

---

## KEY CHANGES FROM V12 TO V21

**What changed:**
1. ~~Use 0.40 threshold~~ → Use 1.0 threshold for rescaled scores
2. ~~3-tier confidence~~ → 5-tier quality classification
3. ~~All keywords equal~~ → Differentiated weights (0.5-1.0)
4. ~~Score 0.14-0.62 range~~ → Rescaled 0-2.0 range
5. ~~Assume full text scored~~ → Understand text preprocessing pipeline
6. ~~Original cosine primary~~ → Rescaled scores primary, cosine secondary

**What stayed the same:**
- Read full text semantically (not keyword search)
- Rate all 4 topics independently (0-3 scale)
- Multi-label assessment philosophy
- Topic definitions unchanged

---

**This methodology ensures accurate assessment of the V21 weighted, rescaled, multi-label dictionary-based topic classification system.**
