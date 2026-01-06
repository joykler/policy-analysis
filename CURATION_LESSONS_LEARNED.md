# Curation Lessons Learned - V5 Mistakes to Avoid

## Context

From V5 systematic semantic verification (45 chunks analyzed), we identified critical curation failures. This document summarizes mistakes to NEVER repeat.

---

## MISTAKE 1: Over-Filtering Core Problem Terms

### What Happened (Early V5 Attempts)

**Problem**: Initial curation removed ALL educational terms because they didn't match HISTORICAL_PATTERNS regex.

**Result**: Educational topic had only 39 generic historical terms with 0 actual educational content.

**User feedback**: "educational disadvantage looks way too insufficient now, almost no reference to the actual problem"

### Lesson Learned

**ALWAYS KEEP SEED TERMS** - Never filter out terms that came from the original seed dictionary (weight != 0.80).

**WHY**: Seed terms represent expert domain knowledge about what defines each topic. Filtering them breaks topic semantics.

**Rule**: `if weight != 0.80: keep_term = True` (regardless of other criteria)

---

## MISTAKE 2: Keeping Generic Historical Terms with High Weights

### What Happened (V5 Structural Neglect)

**Problem**: Structural Neglect dictionary included:
- 34.5% generic historical terms: `slavernijverleden`, `slavernijgeschiedenis`, `geschiedenis`, `historisch`
- Only 3.2% infrastructure-specific terms: `infrastructuur`, `voorzieningen`
- Only 0.5% neglect-specific terms: `verwaarlozing`

**Result**:
- 9/9 sampled chunks had **0 infrastructure keywords**
- 88.9% were semantically about Social/Economic, NOT infrastructure
- Structural Neglect over-triggered on ANY slavery history text
- 918 chunks (23.8% of corpus) mislabeled

**Root cause**: Generic terms like `geschiedenis`, `slavernijverleden` matched ANY historical text, not infrastructure-specific content.

### Lesson Learned

**LOWER WEIGHTS FOR GENERIC CONTEXT TERMS** - Terms that appear across all topics should have LOW weights (0.70-0.75), not high weights.

**Generic terms to watch**:
- Historical: `geschiedenis`, `historisch`, `historie`, `slavernijgeschiedenis`, `slavernijverleden`, `verleden`
- Colonial: `koloniale`, `koloniaal`, `koloniën`
- Slavery: `slavernij` (unless it's the topic focus like Social/Economic)
- Memory: `herdenking`, `monument`, `erfgoed`

**Rule**: If a term appears in >3 topics' expansions → assign weight 0.70-0.75 (context clue only)

---

## MISTAKE 3: Not Checking Semantic Specificity

### What Happened (V5 Governance)

**Problem**: Governance had lower keyword counts in chunks because governance vocabulary is less frequent than social/economic terms in slavery corpus.

**Result**: Governance underperformed (22.2% correct vs 55.6% for Social)

**Why it wasn't catastrophic**: At least governance terms (parlement, kabinet, wetgeving) were SPECIFIC to governance, so when they appeared, they correctly indicated governance content.

### Lesson Learned

**TOPIC-SPECIFIC > HIGH-FREQUENCY** - Better to have fewer specific terms than many generic terms.

**Example**:
- ✓ GOOD: `parlement` (specific, low frequency, correctly identifies governance)
- ✗ BAD: `slavernijverleden` (generic, high frequency, triggers on everything)

**Rule**: Prefer terms that uniquely identify a topic, even if they're rarer

---

## MISTAKE 4: Including Multi-Topic Terms Without Disambiguation

### What Happened (V5 Multi-Label Confusion)

**Problem**: Terms like `plantage`, `slavenhandel`, `slavernij` appear in multiple topics with similar weights.

**Result**: These terms correctly create multi-label cases, but can cause confusion if one topic has too many of them and too few specific terms.

**Example**:
- `plantage` appears in: Economic (plantage economy), Social (plantage society), Infrastructure (plantage geography)
- If Economic has `plantage` + specific terms (`handel`, `dwangarbeid`, `voc`) → good
- If Infrastructure has `plantage` + generic terms (`geschiedenis`, `verleden`) → bad (over-triggers)

### Lesson Learned

**BALANCE MULTI-TOPIC WITH SPECIFIC TERMS** - Each topic needs:
1. Core specific terms (unique to that topic)
2. Related multi-topic terms (shared but relevant)
3. Context terms (geography, time period)

**Rule**: Each topic should have at least 40-50% terms that are SPECIFIC to that topic (not shared)

---

## MISTAKE 5: Not Verifying Term Co-occurrence

### What Happened (V5 Structural Neglect)

**Problem**: We didn't check if infrastructure terms (`infrastructuur`, `voorziening`) actually co-occur with generic terms (`slavernijverleden`) in the corpus.

**Reality**: They DON'T co-occur frequently. Most slavery history texts don't mention infrastructure.

**Result**: Topic vector dominated by generic terms that appear everywhere, specific terms had no influence.

### Lesson Learned

**CHECK DOCUMENT FREQUENCY (df)** - High df for generic terms + low df for specific terms = problem

**Example from V7 expansion**:
- Social: `racisme` df=271, `discriminatie` df=247 (high df, but SPECIFIC to topic) ✓
- Educational: `onderwijs` df=194, `school` df=102 (high df, SPECIFIC) ✓
- Generic: `slavernij` df=753, `handel` df=249 (high df, GENERIC to multiple topics) → lower weight

**Rule**: If term has df > 200 AND appears in >2 topics → weight ≤ 0.80

---

## MISTAKE 6: Over-Inclusive Curation Philosophy

### What Happened (V5 First "Problem-First" Attempt)

**Problem**: Kept 863 terms by being too inclusive with discovered terms (any term with historical relevance).

**Result**: Too many contextual terms diluted topic specificity.

**Correction**: Switched to "keep all seeds + basic quality filter" → 1,185 terms → still had Structural Neglect issue.

### Lesson Learned

**QUALITY > QUANTITY** - Better to have 600 high-quality specific terms than 1,200 mixed-quality terms.

**Rule for discovered terms** (weight = 0.80):
- `cosine >= 0.70` (strong semantic similarity)
- `df >= 2` (appears in corpus)
- NOT a generic historical term (manual check)
- Contributes unique vocabulary not already covered by seeds

---

## MISTAKE 7: Not Doing Semantic Verification Early

### What Happened (V5 Process)

**Problem**: We ran full pipeline → created 3,854 labeled chunks → THEN discovered Structural Neglect failed completely.

**Cost**: Wasted 2-3 hours of analysis and testing.

**User correction**: "Remember always compare to actual semantic chunk reading"

### Lesson Learned

**VERIFY CURATION BEFORE FULL PIPELINE** - Do quick semantic checks:
1. Check if topic terms actually appear together in sample chunks
2. Count keyword co-occurrence in 10-20 random chunks
3. Verify high-weight terms are semantically coherent

**Rule**: After curation, before running checkpoint 5:
- Sample 5 chunks per topic from corpus
- Count how many contain the topic's core terms
- If <3/5 chunks have core terms → re-curate

---

## Summary: Curation Rules for V7

### ALWAYS DO:

1. ✓ **Keep ALL seed terms** (weight != 0.80) regardless of other criteria
2. ✓ **Assign low weights (0.70-0.75) to generic historical/geography/temporal terms**
3. ✓ **Prioritize topic-specific vocabulary** over high-frequency generic terms
4. ✓ **Balance each topic** with 40-50% unique specific terms
5. ✓ **Quality filter discovered terms**: cosine ≥0.70, df ≥2, not generic
6. ✓ **Verify semantics early**: Check keyword co-occurrence in sample chunks

### NEVER DO:

1. ✗ **Never filter out seed terms** (even if they seem generic)
2. ✗ **Never give high weights (>0.80) to generic historical terms** like `geschiedenis`, `slavernijverleden`
3. ✗ **Never rely only on statistics** without semantic verification
4. ✗ **Never over-include discovered terms** just to increase vocabulary size
5. ✗ **Never assume high cosine = good term** (check if it's topic-specific)

### Weight Assignment Rules:

- **1.00**: Critical core problem terms unique to topic (brain drain, racisme, armoede, corruptie)
- **0.95**: Core problem terms (emigratie, discriminatie, werkloosheid)
- **0.90**: Topic-specific vocabulary (onderwijs, parlement, handel)
- **0.85**: Extended specific terms (studenten, ministerie)
- **0.80**: Discovered terms (quality filtered)
- **0.75**: Geography context (curaçao, suriname)
- **0.70**: Generic historical/temporal context (geschiedenis, slavernijverleden, 1863)

### Generic Terms to Always Downweight (0.70-0.75):

- `geschiedenis`, `historisch`, `historie`, `history`, `historical`
- `slavernijgeschiedenis`, `slavernijverleden`, `slavernijgerelateerde`
- `koloniale`, `koloniaal`, `koloniën`, `koloniale`
- `verleden`, `vroeger`, `destijds`
- `herdenking`, `monument`, `erfgoed`, `slavernijmuseum`
- `slavernij` (unless Social/Economic focus), `plantage` (unless Economic focus)

**Exception**: Geography terms (curaçao, suriname, bonaire, aruba, caribisch nederland) get weight 0.75 (slightly higher than temporal because they're more specific).

---

## V7 Specific Concerns from Expansion Analysis

Looking at V7 expanded_candidates.csv:

**Good signs** ✓:
- All 4 topics have strong seed terms present
- Social has high-df specific terms: `racisme` df=271, `discriminatie` df=247
- Educational has high-df specific terms: `onderwijs` df=194, `school` df=102
- Governance has specific terms: `parlement`, `kabinet`, `constitutie`

**Watch out for** ⚠:
- `slavernijgeschiedenis` appears in all 4 topics (cosine 0.941) → must get weight 0.70
- `slavernij` appears in Social (cosine 1.0, df=753) and Economic (cosine 1.0, df=753) → weight 0.75-0.80 max
- `historie` appears in all topics (cosine 0.925) → weight 0.70
- `plantage` in Social (cosine 1.0, df=117) → OK for Social, but check if in Economic too

**Action items**:
1. Identify all terms that appear in >2 topics with high cosine
2. Force these to weight ≤ 0.75 (context only)
3. Keep topic-specific seeds at their original weights
4. Apply quality filter to discovered terms: cosine ≥0.70, df ≥2, not in generic list

