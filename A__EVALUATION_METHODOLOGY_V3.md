# SEMANTIC EVALUATION METHODOLOGY V3
## Multi-Label Assessment for Dictionary Cosine Labeling
## Based on Actual Score Distributions from slavery_Slavdict_pretrained_slavery_v3

**Version:** V3.0 (Updated 2025-12-22)
**Data Source:** workflow_data/slavery_Slavdict_pretrained_slavery_v3/
**Scoring System:** Cosine similarity with SIF weighting (0-10 scale)

---

## CRITICAL UPDATE: ACTUAL SCORE DISTRIBUTIONS

### ⚠️ Major Change from Previous Versions

**Previous methodology (V21)** assumed:
- Score range: 0.0 - 2.0 (rescaled)
- Thresholds: Core ≥1.5, Moderate ≥1.0, Weak ≥0.5
- Equal keyword weights

**ACTUAL scoring system (V3)** uses:
- **Score range: ~1.0 - 9.5** (raw cosine scores, NOT 0-2 scale)
- **Topic-specific baselines** (Educational: 4.0, Racism: 5.1)
- **Differentiated keyword weights** (0.5 - 1.0)
- **SIF term weighting** (rare terms boosted, common terms downweighted)

**THIS METHODOLOGY IS BASED ON EMPIRICAL DISTRIBUTIONS, NOT THEORETICAL RANGES.**

---

## CORE PRINCIPLE

**You must READ the full text semantically, not just search for keywords.**

Keyword matching misses:
- Context and meaning
- Paraphrasing and synonyms
- Implicit references
- Overall semantic theme
- Nuanced multi-topic content

**Multi-label philosophy**: Evaluate whether the score pattern [edu, gov, econ, racism] accurately represents the semantic content's topic profile. Topics are interconnected; chunks can belong to multiple topics.

---

## UNDERSTANDING THE SCORING SYSTEM

### Actual Score Distributions (N=2,840 labeled chunks)

**Individual Topic Scores:**

| Topic | Min | Q1 (25%) | Median (50%) | Q3 (75%) | Max | Mean | Std Dev |
|-------|-----|----------|--------------|----------|-----|------|---------|
| **Educational Disadvantage** | 1.131 | 3.184 | 3.895 | 4.658 | 9.106 | 3.996 | 1.151 |
| **Governance Distrust** | 1.249 | 3.734 | 4.384 | 5.092 | 9.453 | 4.415 | 1.020 |
| **Persistent Poverty** | 1.397 | 3.746 | 4.498 | 5.258 | 9.051 | 4.539 | 1.102 |
| **Social Fragmentation & Racism** | 1.190 | 4.249 | 5.117 | 5.965 | 8.991 | 5.099 | 1.221 |

**Key Observations:**
1. **Racism scores highest baseline** (mean 5.1) - dataset is skewed toward racism/social topics (58.4% of chunks)
2. **Educational scores lowest baseline** (mean 4.0) - only 11.2% of chunks
3. **All topics have similar spread** (std dev ~1.0-1.2)
4. **Minimum scores all >1.0** - even unrelated chunks get baseline scores

### Max Score Distribution (Primary Topic Assignment)

The **max_score** (highest score across 4 topics) is used for primary topic assignment:

| Percentile | Score | Interpretation |
|------------|-------|----------------|
| **P10** (bottom 10%) | 4.118 | Weak signal - borderline noise |
| **P25** (Q1) | 4.752 | Low significance threshold |
| **P50** (Median) | 5.477 | Moderate significance threshold |
| **P75** (Q3) | 6.189 | High significance threshold |
| **P90** (top 10%) | 6.842 | Very high significance |
| **Maximum** | 9.453 | Exceptional signal strength |

### Confidence Tier Distribution

Based on manual labels in the dataset:

| Confidence Category | Count | Percentage | Max Score Range |
|-------------------|-------|-----------|-----------------|
| **No confidence** | 1,370 | 48.2% | 1.8 - 6.5 (broad) |
| **Low confidence** | 908 | 32.0% | 4.7 - 7.6 (mid-range) |
| **High confidence** | 562 | 19.8% | 6.3 - 9.5 (upper) |

### Significance Category Distribution

| Significance Category | Count | Percentage | Typical Max Score |
|-------------------|-------|-----------|-------------------|
| **Noise - Weak Signal** | 840 | 29.6% | < 4.7 |
| **Low Significance** | 364 | 12.8% | 4.7 - 5.5 |
| **Medium Significance** | 544 | 19.2% | 5.5 - 6.2 |
| **High Significance** | 562 | 19.8% | > 6.2 |
| **Noise - Uniform Scores** | 530 | 18.7% | All topics similar |

---

## UPDATED SCORE INTERPRETATION THRESHOLDS

### Individual Topic Score Interpretation

**For each topic independently, use these empirical thresholds:**

| Score Range | Semantic Presence | Interpretation | Percentile |
|-------------|------------------|----------------|------------|
| **< 3.5** | Not present | Below topic baseline, likely irrelevant | < 25% |
| **3.5 - 4.5** | Weakly present | Near baseline, tangential mention | 25% - 50% |
| **4.5 - 5.5** | Moderately present | Clear relevance, moderate discussion | 50% - 75% |
| **5.5 - 6.5** | Strongly present | High relevance, central discussion | 75% - 90% |
| **> 6.5** | Very strongly present | Exceptional relevance, primary focus | > 90% |

**⚠️ TOPIC-SPECIFIC ADJUSTMENTS:**

Because topics have different baselines, adjust interpretation:

**Educational Disadvantage** (baseline 4.0):
- Not present: < 3.2
- Weak: 3.2 - 4.0
- Moderate: 4.0 - 4.7
- Strong: 4.7 - 6.0
- Very strong: > 6.0

**Social Fragmentation & Racism** (baseline 5.1):
- Not present: < 4.2
- Weak: 4.2 - 5.1
- Moderate: 5.1 - 6.0
- Strong: 6.0 - 7.0
- Very strong: > 7.0

**Governance Distrust & Poverty** (baseline 4.4-4.5):
- Use the general thresholds above (3.5/4.5/5.5/6.5)

### Max Score (Primary Topic) Interpretation

**Use percentile-based thresholds for overall chunk quality:**

| Max Score | Quality Tier | Interpretation | Use Case |
|-----------|-------------|----------------|----------|
| **< 4.7** | Noise/Weak | Bottom 25%, very weak signal | Filter out or use as negative examples |
| **4.7 - 5.5** | Low Significance | Q1 to Median, peripheral relevance | Borderline training data |
| **5.5 - 6.2** | Medium Significance | Median to Q3, clear relevance | Standard training data |
| **6.2 - 7.0** | High Significance | Q3 to P90, strong relevance | Quality training data |
| **> 7.0** | Very High Significance | Top 10%, exceptional quality | Premium training data |

### Margin Score Interpretation

**Margin = (max_score - second_highest_score)**

The margin indicates topic discrimination strength:

| Margin | Interpretation | Multi-label Pattern |
|--------|---------------|---------------------|
| **< 0.3** | Uniform scores | Multi-topic chunk or noise |
| **0.3 - 0.6** | Low discrimination | 2-3 relevant topics |
| **0.6 - 1.0** | Moderate discrimination | Clear primary topic + 1 secondary |
| **> 1.0** | High discrimination | Single dominant topic |

**Median margin: 0.617** (most chunks have moderate discrimination)
**Max margin: 4.279** (rare, extreme single-topic focus)

---

## KEYWORD WEIGHT SYSTEM

**Not all keywords are equal.** The dictionary uses differentiated weights:

| Weight | Type | Examples |
|--------|------|----------|
| **1.0** | Core problem terms | "racisme", "discriminatie", "armoede", "werkloosheid", "corruptie" |
| **0.95** | Strong problem terms | "nepotisme", "structureel racisme", "segregatie", "sociale uitsluiting" |
| **0.85** | Domain terms | "onderwijs", "bestuur", "economisch", "plantages", "slavernij" |
| **0.75** | Supporting terms | "curriculum", "minister", "handel", "emancipatie", "koloniaal" |
| **0.55** | Contextual terms | "geschiedenis", "historisch", "erfenis", "slavernijverleden" |
| **0.5** | Geographic terms | "suriname", "curaçao", "bonaire", "caribisch nederland" |

**Impact on scoring:**
- Core terms (1.0) have **2x weight** of geographic terms (0.5)
- Chunks with multiple core terms score significantly higher
- SIF weighting also applied (rare terms boosted, common terms downweighted)
- Geographic/historical terms appear in all topics → create baseline noise

---

## TEXT PREPROCESSING PIPELINE

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
- Dutch stopwords ("de", "in", "was", "blijft")
- Numbers ("2023")
- Geographic names ("Suriname") - unless they're topic keywords
- Common function words
- Punctuation

**Preserved:**
- Original word forms (NO stemming)
- Domain-specific terms
- Compound words
- Topic keywords (even if geographic/historical)

---

## STEP-BY-STEP EVALUATION PROTOCOL

### 1. Sample Selection Strategy

**Stratify by BOTH quality tier AND topic:**

Sample 10-15 chunks per combination = 200-300 total samples:

**By max score percentile** (5 tiers × 50-75 chunks):
- Bottom 25% (max < 4.7): 50-75 chunks
- Q1-Median (4.7-5.5): 50-75 chunks
- Median-Q3 (5.5-6.2): 50-75 chunks
- Q3-P90 (6.2-7.0): 50-75 chunks
- Top 10% (max > 7.0): 50-75 chunks

**By primary topic** (4 topics, ensure balanced coverage):
- Educational: 50-75 chunks
- Governance: 50-75 chunks
- Poverty: 50-75 chunks
- Racism: 50-75 chunks

**By margin** (3 categories):
- Low margin (< 0.4): Multi-topic chunks
- Medium margin (0.4-1.0): Standard chunks
- High margin (> 1.0): Single-topic chunks

**Optional stratification:**
- Manual confidence labels (if available)
- Significance categories
- Bertje model predictions (if available)

### 2. For Each Chunk: READ FULLY

**Do not keyword search. Read the entire `raw_text` as a human would.**

Ask yourself:
1. What is this text actually about?
2. What are the main themes and subjects discussed?
3. Which of the 4 topics are genuinely present in the semantic content?
4. How central vs. peripheral is each topic?

**Note:** You are reading `raw_text`, but the system scored `text_for_scoring`. Keep in mind that stopwords, numbers, and some geographic names were removed before scoring.

### 3. Topic Definitions (Reference)

**Educational Disadvantage & Brain Drain:**
- Educational inequality, school quality, language barriers in education
- Educational migration (brain drain), emigration of educated people
- Teacher shortages, curriculum issues, literacy, dropout
- Educational achievement gaps, access to education
- Colonial education system, Dutch language imposition

**Governance Distrust & Corruption:**
- Government corruption, nepotism, patronage systems
- Distrust in political institutions, governance failures
- Colonial/postcolonial governance structures, autonomy struggles
- Political control, administration problems, institutional issues
- Legal system, rule of law, access to justice

**Persistent Poverty & Economic Vulnerability:**
- Economic hardship, poverty, unemployment, debt
- Economic dependency, economic exploitation
- Plantation economies, trade systems, forced labor
- Economic vulnerability, financial insecurity, informal economy
- Wealth inequality, lack of economic opportunities

**Social Fragmentation & Racism:**
- Racial discrimination, racism, prejudice based on race/ethnicity
- Segregation, social exclusion, racial hierarchies, colorism
- Emancipation struggles, abolition movements
- Social legacy of slavery, identity and belonging issues
- Intra-community racism, social fragmentation

**See [A__TOPIC_FRAMEWORK_CONTEXT.md](A__TOPIC_FRAMEWORK_CONTEXT.md) for detailed historical context.**

### 4. Rate Semantic Presence (0-4 scale)

For each of the 4 topics, rate its semantic presence:

| Rating | Meaning | When to Use |
|--------|---------|-------------|
| **0** | Not present | Topic not mentioned or discussed at all |
| **1** | Weakly present | Tangential mention, very minor aspect |
| **2** | Moderately present | Clear discussion but not central theme |
| **3** | Strongly present | Central theme, extensively discussed |
| **4** | Very strongly present | Dominant theme, exceptional focus |

**Important:** This is subjective human judgment based on full-text reading, considering the historical context and topic interconnections.

### 5. Compare to Actual Scores

**Map your semantic ratings to expected score ranges:**

| Semantic Rating | Expected Score (General) | Educational | Racism |
|----------------|-------------------------|-------------|--------|
| **0** Not present | < 3.5 | < 3.2 | < 4.2 |
| **1** Weak | 3.5 - 4.5 | 3.2 - 4.0 | 4.2 - 5.1 |
| **2** Moderate | 4.5 - 5.5 | 4.0 - 4.7 | 5.1 - 6.0 |
| **3** Strong | 5.5 - 6.5 | 4.7 - 6.0 | 6.0 - 7.0 |
| **4** Very strong | > 6.5 | > 6.0 | > 7.0 |

**Compare:**
- **System-detected topics:** Which topics have scores ≥ 5.5 (moderate threshold)?
- **Semantically-present topics:** Which topics you rated ≥ 2?
- **Overlap:** Do they match?

**Check primary_topic assignment:**
- Which topic has the highest score?
- Does this match your semantic assessment?
- Is the margin (difference to 2nd place) appropriate?

### 6. Quality Assessment Framework

**Pattern-Level Assessment:**

| Quality Label | Meaning | Criteria |
|--------------|---------|----------|
| **EXCELLENT-PATTERN** | All 4 scores match semantic ratings | All scores within expected ranges |
| **GOOD-PATTERN** | 3/4 scores match, pattern shape correct | Minor deviations, overall learnable |
| **FAIR-PATTERN** | 2/4 scores match, pattern partially correct | Noticeable issues but still usable |
| **POOR-PATTERN** | Pattern shape doesn't match content | Will mislead training |

**Individual Topic Assessment:**

| Quality Label | Meaning | Criteria |
|--------------|---------|----------|
| **MATCH** | Score aligns with semantic rating | Score in expected range for rating |
| **MINOR-DEVIATION** | Score slightly off (±0.5 points) | Close to expected range |
| **MODERATE-MISMATCH** | Score moderately off (±1.0 points) | Outside expected range |
| **SEVERE-MISMATCH** | Score severely wrong (±2.0+ points) | Completely wrong signal |

**Direction-Specific Labels:**

| Quality Label | Meaning | Example |
|--------------|---------|---------|
| **UNDER-SCORED** | Score too low for semantic presence | Rating 3 (strong) but score 4.2 (weak) |
| **OVER-SCORED** | Score too high for semantic presence | Rating 0 (absent) but score 6.5 (strong) |
| **FALSE-POSITIVE** | High score (>6.5) but not present | Dictionary keywords in wrong context |
| **FALSE-NEGATIVE** | Low score (<4.5) but strongly present | Missing relevant keywords |

**Multi-label Specific:**

| Quality Label | Meaning | Criteria |
|--------------|---------|----------|
| **MULTI-TOPIC-CORRECT** | Multiple high scores, all appropriate | 2+ topics rated ≥2, all score ≥5.5 |
| **MULTI-TOPIC-PARTIAL** | Some topics captured, some missed | Mixed performance on multi-topic content |
| **MULTI-TOPIC-CONFUSED** | Wrong topics score high | Irrelevant topics score higher than relevant |
| **SINGLE-TOPIC-CORRECT** | Only 1 high score, appropriate | 1 topic rated ≥2, margin >1.0 |
| **UNIFORM-NOISE** | All scores similar and low | All scores 3.5-4.5, no clear topic |

---

## EVALUATION EXAMPLES (UPDATED FOR V3)

### Example 1: Strong Single-Topic Match

**Chunk ID:** `abc123:00042`

**Raw text (abbreviated):**
> "Het onderwijssysteem op de BES-eilanden kampt met structurele problemen. De taalbarrière tussen Papiamentu en Nederlands vormt een grote hindernis. Veel jongeren verlaten het eiland voor hoger onderwijs in Nederland en keren niet terug - een vorm van brain drain."

**Actual Scores:**
- Educational: **7.2**
- Governance: 4.1
- Poverty: 3.8
- Racism: 4.5

**Max score:** 7.2 (Educational)
**Margin:** 3.1 (very high discrimination)
**Significance tier:** Very High (top 10%)

---

**Step 1: Semantic Reading**

This text discusses:
- Educational system problems (structural)
- Language barriers in education (Papiamentu vs Dutch)
- Brain drain (educated youth leaving)
- Educational challenges specific to BES islands

**Step 2: Semantic Ratings**

- **Educational:** 4 (very strongly present - primary focus, multiple aspects)
- **Governance:** 0 (not discussed)
- **Poverty:** 1 (weakly present - implied economic consequences of brain drain)
- **Racism:** 1 (weakly present - colonial language imposition is implicit racist legacy)

**Step 3: Expected Score Ranges** (using Educational-adjusted thresholds)

- Educational: Rating 4 → expect > 6.0
- Governance: Rating 0 → expect < 3.5
- Poverty: Rating 1 → expect 3.5-4.5
- Racism: Rating 1 → expect 4.2-5.1

**Step 4: Compare to Actual Scores**

| Topic | Actual | Rating | Expected | Assessment |
|-------|--------|--------|----------|------------|
| Educational | 7.2 | 4 | > 6.0 | ✅ MATCH (excellent) |
| Governance | 4.1 | 0 | < 3.5 | ⚠️ MINOR-DEVIATION (slightly high) |
| Poverty | 3.8 | 1 | 3.5-4.5 | ✅ MATCH |
| Racism | 4.5 | 1 | 4.2-5.1 | ✅ MATCH |

**Step 5: Pattern Assessment**

```
Score pattern:      [Very High --- Low -- VeryLow -- Low]
                    [7.2,     4.1,  3.8,  4.5]

Semantic pattern:   [Very Strong - Absent - Weak - Weak]
                    [4,          0,      1,    1]

Pattern shape: EXCELLENT-PATTERN
- Educational clearly dominant (7.2 >> all others)
- Margin 3.1 indicates strong single-topic focus (correct)
- Secondary scores appropriately low/weak
- Governance slightly elevated (4.1 vs expected <3.5) but not problematic
```

**Overall Quality:** **EXCELLENT-PATTERN**

**Training Sufficiency:** **Yes** - BERTje can clearly learn:
- "onderwijssysteem", "taalbarrière", "brain drain" → very high Educational score (7.2)
- Absence of governance/poverty content → low scores
- Pattern [7.2, 4.1, 3.8, 4.5] is highly informative

**Dictionary Analysis:**
- "onderwijssysteem" - compound of "onderwijs" (0.85 weight)
- "taalbarrière" - matches "taalbarrières" (0.95 weight, Educational dict)
- "papiamentu" (0.85 weight, Educational dict)
- "brain drain" - English term, semantic similarity working
- High score achieved through multiple relevant terms, not single keyword

---

### Example 2: Multi-Topic Chunk

**Chunk ID:** `def456:00089`

**Raw text (abbreviated):**
> "Racisme op de arbeidsmarkt blijft een groot probleem. Mensen met een donkere huidskleur hebben minder kans op werk, zelfs met dezelfde kwalificaties. Dit leidt tot hogere werkloosheid en armoede binnen de Afro-Caribische gemeenschap."

**Actual Scores:**
- Educational: 3.2
- Governance: 3.9
- Poverty: **6.8**
- Racism: **7.1**

**Max score:** 7.1 (Racism)
**Margin:** 0.3 (low discrimination - multi-topic)
**Significance tier:** Very High

---

**Step 1: Semantic Reading**

This text discusses:
- Racism in labor market
- Employment discrimination based on skin color
- Economic consequences (unemployment, poverty)
- Afro-Caribbean community impacts

**Step 2: Semantic Ratings**

- **Educational:** 0 (not discussed)
- **Governance:** 0 (not discussed - though policy solutions implied)
- **Poverty:** 3 (strongly present - unemployment and poverty explicitly mentioned)
- **Racism:** 4 (very strongly present - primary focus, explicit racism discussion)

**Step 3: Expected Score Ranges**

- Educational: Rating 0 → expect < 3.2
- Governance: Rating 0 → expect < 3.5
- Poverty: Rating 3 → expect 5.5-6.5
- Racism: Rating 4 → expect > 7.0

**Step 4: Compare to Actual Scores**

| Topic | Actual | Rating | Expected | Assessment |
|-------|--------|--------|----------|------------|
| Educational | 3.2 | 0 | < 3.2 | ✅ MATCH (at boundary) |
| Governance | 3.9 | 0 | < 3.5 | ⚠️ MINOR-DEVIATION (slightly high) |
| Poverty | 6.8 | 3 | 5.5-6.5 | ✅ MATCH (upper range) |
| Racism | 7.1 | 4 | > 7.0 | ✅ MATCH |

**Step 5: Pattern Assessment**

```
Score pattern:      [VeryLow -- Low -- High ---- VeryHigh]
                    [3.2,    3.9,  6.8,   7.1]

Semantic pattern:   [Absent - Absent - Strong - Very Strong]
                    [0,       0,       3,       4]

Pattern shape: EXCELLENT-PATTERN (Multi-topic)
- Racism and Poverty both high (7.1, 6.8) - correct!
- Low margin (0.3) appropriately indicates multi-topic content
- Educational and Governance appropriately low
- Pattern correctly captures "racism → economic consequences" connection
```

**Overall Quality:** **EXCELLENT-PATTERN** + **MULTI-TOPIC-CORRECT**

**Training Sufficiency:** **Yes** - BERTje learns:
- Racism-Poverty interconnection (both score >6.5)
- Low margin signals multi-topic chunk
- Pattern [3.2, 3.9, 6.8, 7.1] shows topic co-occurrence

**Topic Interconnection:** This is an IDEAL multi-topic chunk - demonstrates that racism (employment discrimination) directly causes economic vulnerability (unemployment, poverty). The scoring system correctly captures both topics as strongly present with low margin.

---

### Example 3: False Positive (Dictionary Overfitting)

**Chunk ID:** `ghi789:00134`

**Raw text (abbreviated):**
> "De circulaire van 1863 betrof administratieve procedures voor het ministerie van Koloniën. Diverse geografische gebieden, waaronder Suriname en de Nederlandse Antillen, vielen onder deze regelgeving."

**Translation:** "The 1863 circular concerned administrative procedures for the Ministry of Colonies. Various geographic areas, including Suriname and the Dutch Antilles, fell under this regulation."

**Actual Scores:**
- Educational: 4.8
- Governance: **6.2**
- Poverty: 4.1
- Racism: 5.3

**Max score:** 6.2 (Governance)
**Margin:** 0.9
**Significance tier:** High (Q3)

---

**Step 1: Semantic Reading**

This text discusses:
- Administrative circular from 1863
- Colonial ministry procedures
- Geographic coverage (Suriname, Antilles)
- Bureaucratic/regulatory content

**This is likely a table of contents entry or document header - NO substantive topic content.**

**Step 2: Semantic Ratings**

- **Educational:** 0 (not discussed)
- **Governance:** 1 (weakly present - administrative mention, but no substantive content)
- **Poverty:** 0 (not discussed)
- **Racism:** 0 (not discussed - "1863" is emancipation year but no content about slavery/racism)

**Step 3: Expected Score Ranges**

- Educational: Rating 0 → expect < 3.2
- Governance: Rating 1 → expect 3.5-4.5
- Poverty: Rating 0 → expect < 3.5
- Racism: Rating 0 → expect < 4.2

**Step 4: Compare to Actual Scores**

| Topic | Actual | Rating | Expected | Assessment |
|-------|--------|--------|----------|------------|
| Educational | 4.8 | 0 | < 3.2 | ❌ SEVERE-MISMATCH (over-scored) |
| Governance | 6.2 | 1 | 3.5-4.5 | ❌ SEVERE-MISMATCH (over-scored) |
| Poverty | 4.1 | 0 | < 3.5 | ❌ MODERATE-MISMATCH (over-scored) |
| Racism | 5.3 | 0 | < 4.2 | ❌ SEVERE-MISMATCH (over-scored) |

**Step 5: Pattern Assessment**

```
Score pattern:      [Medium -- High ---- Low -- Medium]
                    [4.8,   6.2,    4.1,  5.3]

Semantic pattern:   [Absent - Weak - Absent - Absent]
                    [0,       1,     0,       0]

Pattern shape: POOR-PATTERN (False positive)
- ALL scores too high for content
- Governance score 6.2 (High tier) for table-of-contents entry
- Max score 6.2 places this in "High Significance" tier - WRONG
- This chunk should be in "Noise" tier (max < 4.7)
```

**Overall Quality:** **POOR-PATTERN** + **FALSE-POSITIVE**

**Training Sufficiency:** **No** - This will mislead training:
- BERTje learns that administrative headers = high Governance score
- Pattern [4.8, 6.2, 4.1, 5.3] suggests multi-topic substantive content
- Actually just keyword-triggered noise

**Dictionary Overfitting Analysis:**

**Likely triggers:**
- "1863" (0.75 weight, in ALL topic dicts) - emancipation year
- "koloniën" (0.85 weight, Governance/Educational dicts)
- "Suriname" (0.5 weight, ALL dicts)
- "Antillen" (0.5 weight, ALL dicts)
- "ministerie" (0.85 weight, Governance dict)

**Problem:** Generic historical/geographic terms create false signal without substantive content.

**After preprocessing** (`text_for_scoring`):
```
"circulaire 1863 administratieve procedures ministerie koloniën geografische suriname antillen regelgeving"
```

High density of low-weight cross-topic keywords (0.5-0.85 range) → inflated scores.

**Recommendation:**
- Downweight generic terms: "1863" (→ 0.4), "koloniën" (→ 0.6)
- Add "circulaire" to stopwords (administrative boilerplate)
- Consider content-length penalty (very short texts)
- Add context requirements: "ministerie" should co-occur with substantive governance terms

---

## COMMON PITFALLS TO AVOID

### ❌ DON'T: Use Old Thresholds

```
Bad: "Educational scored 0.82 which is high, so it's strongly present"
```
**Wrong scale!** V21 used 0-2 range. V3 uses 1-10 range.

### ✅ DO: Use V3 Empirical Thresholds

```
Good: "Educational scored 7.2, which is >6.0 (very strong for Educational topic),
      placing it in the top 10% of Educational scores"
```

### ❌ DON'T: Ignore Topic Baselines

```
Bad: "Racism scored 5.1 and Educational scored 5.1, so they're equally present"
```
**Wrong!** Racism baseline is 5.1 (median), but Educational baseline is 4.0 (median 3.9).

### ✅ DO: Adjust for Topic-Specific Baselines

```
Good: "Racism scored 5.1 (at baseline/median, weak presence) but Educational scored 5.1
      (well above 3.9 median, strong presence for this topic)"
```

### ❌ DON'T: Ignore Text Preprocessing

```
Bad: "This text mentions 'Suriname' 5 times, so scores should be very high"
```

### ✅ DO: Consider What Was Actually Scored

```
Good: "Geographic terms like 'Suriname' (0.5 weight) contribute minimally.
      Score driven by substantive terms: 'werkloosheid' (1.0), 'armoede' (1.0)"
```

### ❌ DON'T: Expect All Keywords Equal

```
Bad: "The text has 'geschiedenis' and 'racisme', so both contribute equally"
```

### ✅ DO: Account for Weight Differences

```
Good: "'racisme' (1.0 weight) contributes 2x more than 'geschiedenis' (0.55 weight),
      plus SIF weighting boosts rare terms"
```

### ❌ DON'T: Treat Margin as Binary

```
Bad: "Margin is 0.3, so this is clearly multi-topic"
```

### ✅ DO: Interpret Margin in Context

```
Good: "Margin 0.3 is below median (0.6), suggesting multi-topic content.
      Confirm by checking if 2+ topics score >5.5"
```

---

## AGGREGATE ANALYSIS & REPORTING

### Pattern Quality Metrics (PRIMARY)

Calculate overall pattern quality distribution:

```
Pattern Quality:
- EXCELLENT-PATTERN: X chunks (Y%) - all 4 scores match semantic ratings
- GOOD-PATTERN: X chunks (Y%) - 3/4 scores match, shape correct
- FAIR-PATTERN: X chunks (Y%) - 2/4 scores match, partially usable
- POOR-PATTERN: X chunks (Y%) - pattern misleading
```

### Training Sufficiency (CRITICAL)

```
Training Sufficiency:
- Yes (BERTje can learn): X chunks (Y%)
- Marginal (somewhat learnable): X chunks (Y%)
- No (will confuse training): X chunks (Y%)
```

**Threshold for training readiness:** ≥80% "Yes", <5% "No"

### Score-Semantic Alignment by Topic

For each topic independently:

```
Educational Disadvantage & Brain Drain:
- MATCH: X% (scores align with semantic ratings)
- MINOR-DEVIATION: X% (±0.5 points)
- MODERATE-MISMATCH: X% (±1.0 points)
- SEVERE-MISMATCH: X% (±2.0+ points)

Direction breakdown:
- UNDER-SCORED: X% (score too low for content)
- OVER-SCORED: X% (score too high for content)

Systematic issues: [description]
```

Repeat for all 4 topics.

### Multi-Topic Assessment

```
Multi-Topic Chunks (margin <0.6):
- MULTI-TOPIC-CORRECT: X chunks - multiple relevant topics all captured
- MULTI-TOPIC-PARTIAL: X chunks - some captured, some missed
- MULTI-TOPIC-CONFUSED: X chunks - wrong topics scored high

Single-Topic Chunks (margin >1.0):
- SINGLE-TOPIC-CORRECT: X chunks - clear dominant topic
- SINGLE-TOPIC-WRONG: X chunks - wrong topic dominant
```

### False Positive Analysis (CRITICAL)

```
False Positives (high score but not present):
- Total: X chunks (Y%)
- By topic:
  - Educational: X (most common triggers: [keywords])
  - Governance: X (most common triggers: [keywords])
  - Poverty: X (most common triggers: [keywords])
  - Racism: X (most common triggers: [keywords])

Common patterns:
- Generic historical terms (1863, koloniaal): X chunks
- Geographic terms (suriname, curaçao): X chunks
- Administrative boilerplate (circulaire, ministerie): X chunks
- Table of contents / headers: X chunks
```

### False Negative Analysis (CRITICAL)

```
False Negatives (low score but strongly present):
- Total: X chunks (Y%)
- By topic:
  - Educational: X (missing keywords: [concepts])
  - Governance: X (missing keywords: [concepts])
  - Poverty: X (missing keywords: [concepts])
  - Racism: X (missing keywords: [concepts])

Common patterns:
- Paraphrasing / euphemisms: X chunks
- Implicit references (no explicit keywords): X chunks
- Domain-specific terminology not in dict: X chunks
- Policy language avoiding direct terminology: X chunks
```

### Score Distribution Validation

Compare your sample to overall population:

```
Sample Score Distribution vs. Population:

Max Score Distribution:
- Sample P25: X.XX vs. Population P25: 4.752
- Sample P50: X.XX vs. Population P50: 5.477
- Sample P75: X.XX vs. Population P75: 6.189

Margin Distribution:
- Sample median: X.XX vs. Population median: 0.617

Assessment: Sample is [representative / skewed toward high/low scores]
```

### Topic Baseline Validation

```
Topic Score Means (Sample vs. Population):

Educational:
- Sample mean: X.XX vs. Population: 3.996
- Sample median: X.XX vs. Population: 3.895

Governance:
- Sample mean: X.XX vs. Population: 4.415
- Sample median: X.XX vs. Population: 4.384

Poverty:
- Sample mean: X.XX vs. Population: 4.539
- Sample median: X.XX vs. Population: 4.498

Racism:
- Sample mean: X.XX vs. Population: 5.099
- Sample median: X.XX vs. Population: 5.117

Assessment: Sample distributions [match / differ from] population
```

---

## QUALITATIVE ANALYSIS

### For Each POOR-PATTERN Case

Document:
1. **Chunk text** (full raw_text)
2. **Actual score pattern** [edu, gov, econ, racism]
3. **Semantic ratings** [0-4 scale for each topic]
4. **Specific mismatch**: Which scores are wrong and by how much?
5. **Likely cause**:
   - Dictionary keywords found in `text_for_scoring`
   - Keyword weights involved
   - Generic cross-topic terms (1863, koloniaal, suriname)?
   - Administrative boilerplate?
   - Missing relevant keywords?
   - Paraphrasing/euphemisms not captured?
6. **Impact on training**: How will this mislead BERTje?
7. **Recommendation**: Specific dictionary changes (add/remove/reweight terms)

### For Each FALSE-POSITIVE Case

Special attention to high-scoring noise:

1. **Score and tier**: What score? Which significance tier?
2. **Content type**: Table of contents? Header? Boilerplate? Bibliography?
3. **Trigger keywords**: Which dictionary terms inflated the score?
4. **Keyword weights**: Are they too high (0.85-1.0 when should be 0.5-0.7)?
5. **Cross-contamination**: Are generic terms (geographic, historical) the problem?
6. **Recommendation**:
   - Downweight generic terms?
   - Add to stopwords?
   - Require co-occurrence with substantive terms?
   - Add content-length penalty?

### For Each FALSE-NEGATIVE Case

Special attention to missed content:

1. **Semantic strength**: How strong was the topic presence (rating 3-4)?
2. **Actual score**: How low did it score?
3. **Missing keywords**: What concepts/terms were present but not in dictionary?
4. **Language pattern**: Paraphrasing? Euphemism? Policy jargon?
5. **Recommendation**:
   - Add missing keywords with appropriate weights
   - Add semantic expansions
   - Add domain-specific policy terminology

### Cross-Topic Pattern Analysis

Identify common multi-topic patterns:

```
Pattern: High Educational + High Poverty [edu >5.5, pov >5.5]
- Frequency: X chunks
- Semantic appropriateness: [YES/PARTIAL/NO]
- Example chunks: [list IDs]
- Assessment: [This is expected - educational disadvantage → poverty]

Pattern: High Racism + High Governance [racism >6.0, gov >6.0]
- Frequency: X chunks
- Semantic appropriateness: [YES/PARTIAL/NO]
- Example chunks: [list IDs]
- Assessment: [Less common but valid - discriminatory governance policies]
```

Common expected multi-topic combinations:
- Educational + Poverty (educational disadvantage → economic vulnerability)
- Racism + All topics (racism permeates all domains)
- Governance + Poverty (corruption/patronage → economic inequality)
- Educational + Governance (language policy, colonial education system)

---

## REMEMBER: EVALUATION METHOD (V3 UPDATED)

✅ **Use V3 score ranges** (1.0 - 9.5, NOT 0-2.0)
✅ **Adjust for topic baselines** (Educational 4.0, Racism 5.1)
✅ **Sample** by max score percentile AND primary topic
✅ **Read** full `raw_text` semantically (no keyword matching)
✅ **Rate** all 4 topics independently (0-4 scale)
✅ **Compare** semantic ratings to empirical score thresholds
✅ **Check** pattern shape [edu, gov, econ, racism] as unified vector
✅ **Understand** text preprocessing removes stopwords, numbers, some geographic names
✅ **Account** for keyword weights (0.5-1.0 range, NOT equal)
✅ **Consider** SIF weighting (rare terms boosted, common downweighted)
✅ **Multi-label** approach - chunks can be relevant to 0-4 topics
✅ **Assess** margin for multi-topic vs. single-topic discrimination
✅ **Ask** "Can BERTje learn from this pattern?"

---

## VALIDATION CHECKLIST

Before finalizing evaluation:

- [ ] Did you use **V3 score ranges** (1-9.5), not V21 ranges (0-2)?
- [ ] Did you adjust thresholds for **topic-specific baselines**?
- [ ] Did you READ every chunk's `raw_text` fully, not just skim?
- [ ] Did you assess all 4 topics independently for each chunk?
- [ ] Did you use the 0-4 semantic rating scale?
- [ ] Did you compare semantic ratings (≥2) with score thresholds (Educational ≥4.7, Racism ≥6.0)?
- [ ] Did you evaluate **pattern shape** [edu, gov, econ, racism] as a whole?
- [ ] Did you check margin for multi-topic interpretation?
- [ ] Did you identify false positives (high scores for noise/boilerplate)?
- [ ] Did you identify false negatives (low scores for strong content)?
- [ ] Did you note which keywords were likely removed during preprocessing?
- [ ] Did you consider keyword weight differences (1.0 vs 0.5)?
- [ ] Did you document specific examples of mismatches with explanations?
- [ ] Did you calculate pattern quality distribution?
- [ ] Did you assess training sufficiency (≥80% "Yes")?

---

## KEY CHANGES FROM V21 TO V3

**What changed:**

1. ~~Score range 0-2.0~~ → **Score range 1.0-9.5** (actual empirical data)
2. ~~Equal topic baselines~~ → **Topic-specific baselines** (Educational 4.0, Racism 5.1)
3. ~~5-tier quality (Core/Moderate/Weak/Context/Noise)~~ → **Percentile-based tiers** (P25/P50/P75/P90)
4. ~~Threshold 1.5/1.0/0.5~~ → **Threshold 6.5/5.5/4.5/3.5** (adjusted per topic)
5. ~~Semantic rating 0-3~~ → **Semantic rating 0-4** (added "very strong")
6. ~~Assumed rescaling applied~~ → **Raw cosine scores** (no rescaling in V3)
7. Added **margin score** interpretation for multi-topic detection
8. Added **false positive analysis** for boilerplate/noise
9. Added **score distribution validation** against population
10. Added **V3 data source** (slavery_Slavdict_pretrained_slavery_v3)

**What stayed the same:**

- Read full text semantically (not keyword search)
- Multi-label assessment philosophy
- Pattern shape evaluation [edu, gov, econ, racism]
- Topic definitions unchanged
- Training sufficiency as critical metric
- Topic interconnections acknowledged
- Dictionary weight awareness (0.5-1.0)

---

## DATA SOURCE SPECIFICATIONS

**Workflow:** slavery_Slavdict_pretrained_slavery_v3
**Created:** 2025-12-22
**Corpus:** Slavery-related historical documents (books, reports)
**Chunks:** 85,087 total, 2,840 with manual labels
**Dictionary:** ~300 terms per topic, SIF-weighted
**Scoring:** Cosine similarity with SIF weighting, no rescaling

**Files:**
- `workflow_data/slavery_Slavdict_pretrained_slavery_v3/Cosine_labeling/scores_all_labeled.csv` (2,840 rows)
- `workflow_data/slavery_Slavdict_pretrained_slavery_v3/Bertje_labeling/bertje_labeling_summary.json` (statistics)
- `workflow_data/slavery_Slavdict_pretrained_slavery_v3/config/config_checkpoint5_scoring_20251222_174354.json` (config)

**See also:**
- [A__TOPIC_FRAMEWORK_CONTEXT.md](A__TOPIC_FRAMEWORK_CONTEXT.md) - Historical context for 4 topics
- [COSINE_EVALUATION_METHODOLOGY.md](COSINE_EVALUATION_METHODOLOGY.md) - Alternative pattern-based methodology

---

**This methodology ensures accurate assessment of the V3 dictionary-based multi-label topic classification system using empirically-derived score distributions from 2,840 labeled chunks.**

**Last updated:** 2025-12-22
**Version:** 3.0
**Author:** Based on workflow data analysis for Cedric Joy Berkelouw's Dutch Caribbean slavery legacy research (EUR master's thesis)
