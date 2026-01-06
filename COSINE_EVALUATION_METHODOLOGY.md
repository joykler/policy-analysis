# Cosine Label Evaluation Methodology

## Overview
This document describes the proper method for evaluating cosine labeling quality through manual semantic assessment for the Dutch Caribbean slavery legacy research project.

**Research Context**: This evaluation assesses dictionary-based topic modeling that links contemporary developmental challenges in the Dutch Caribbean (Bonaire, St. Eustatius, Saba) to historical slavery legacies during the UN International Decade for People of African Descent (IDPAD, 2015-2024).

**See also**:
- [A__TOPIC_FRAMEWORK_CONTEXT.md](A__TOPIC_FRAMEWORK_CONTEXT.md) for detailed historical rationale behind the 4-topic framework
- [A__EVALUATION_METHODOLOGY.md](A__EVALUATION_METHODOLOGY.md) for V21 semantic evaluation protocol
- [workflow_data/policy_Slavdict_ft-slavery_slavery_v1/Cosine_labeling/POLICY_CORPUS_EVALUATION_REPORT.md](workflow_data/policy_Slavdict_ft-slavery_slavery_v1/Cosine_labeling/POLICY_CORPUS_EVALUATION_REPORT.md) for completed policy corpus evaluation (2025-12-03)

---

## Core Principle

**DO NOT use keyword matching or automated metrics as primary evaluation.**

**DO NOT evaluate "which topic is correct" - there is no single correct topic.**

Instead: **Evaluate whether the multi-label score pattern [edu, gov, econ, racism] accurately represents the semantic content's topic profile.**

**Training goal**: These multi-label scores train BERTje to understand topic patterns. The question is: **Can BERTje learn meaningful topic understanding from these score patterns?** Scores don't need to be perfect, just sufficient to teach the shape and understanding of topics.

---

## Understanding the 4 Topics

Before evaluating, understand what each topic represents (see [TOPIC_FRAMEWORK_CONTEXT.md](TOPIC_FRAMEWORK_CONTEXT.md) for full details):

### Topic 1: Educational Disadvantage & Brain Drain
**Contemporary problems**: Poor outcomes, dropout, language barriers (Dutch vs. Papiamentu), brain drain, educational racism
**Slavery legacy**: Educational exclusion, colonial language imposition, underdevelopment as extraction economy

### Topic 2: Social Fragmentation & Racism
**Contemporary problems**: Racism, colorism, social hierarchies based on skin color, intra-community discrimination
**Slavery legacy**: Racial hierarchy system, divide-and-rule, identity destruction, scientific racism

### Topic 3: Governance Distrust & Corruption
**Contemporary problems**: Low trust in government, corruption, patronage/clientelism, weak rule of law, asymmetric power with Netherlands
**Slavery legacy**: Colonial governance for extraction, denial of agency, patronage survival strategies, legal oppression

### Topic 4: Persistent Poverty & Economic Vulnerability
**Contemporary problems**: High poverty, unemployment, dependency on tourism/remittances, economic precarity
**Slavery legacy**: Extractive economy, zero wealth transfer post-emancipation, continued labor exploitation, no reparations

**Critical insight**: Topics are **interconnected** - racism shapes economic outcomes; governance affects education; educational disadvantage leads to poverty. Chunks may legitimately belong to multiple topics.

---

## Step-by-Step Process

### 1. Stratified Sampling

**Objective**: Get representative sample across all conditions

**Sampling dimensions**:
- ✅ **All 4 topics** (Educational, Racism, Governance, Economic)
- ✅ **All confidence tiers** (high/medium/low/no confidence)
- ✅ **Balanced distribution** (equal representation)

**Method**:
```python
# For each topic
for topic in topics:
    for tier in ['high', 'medium', 'low', 'no']:
        # Sample N chunks (e.g., 10-20)
        sample = chunks[(chunks['primary_label'] == topic) &
                       (chunks['confidence_tier'] == tier)]
        sampled_chunks.extend(sample.sample(n=N))
```

**CRITICAL NOTE**: Primary labels are ONLY used for stratified sampling to ensure coverage - they are NOT ground truth and must be completely ignored during evaluation! The multi-label score vector is what matters.

---

### 2. Blind Semantic Assessment

**For each sampled chunk, evaluator must**:

#### A. Read the chunk text
- Understand the full semantic meaning
- Identify what topics are actually discussed
- Note the main focus and secondary themes

#### B. Examine ALL cosine scores as a multi-label vector
- Look at the complete score profile across all 4 topics: [edu, gov, econ, racism]
- **IGNORE which was assigned as primary label** (primary is just sampling shorthand, NOT ground truth)
- The 4-dimensional score vector is what BERTje learns from

#### C. Assess multi-label score pattern accuracy

**CRITICAL**: You are NOT evaluating "which topic is correct" - you are evaluating whether the **score pattern** (the shape of [edu, gov, econ, racism]) accurately represents the semantic content.

Ask these questions:

**Score pattern assessment**:
- ✅ Does the **score combination** accurately reflect topic presence/emphasis in the text?
- ✅ Are high scores (>0.6) given to topics that are clearly present?
- ✅ Are medium scores (0.3-0.6) given to topics that are marginally present?
- ✅ Are low scores (<0.3) given to topics that are not present?
- ❌ Does any score significantly misrepresent that topic's presence?

**Relative magnitude assessment**:
- ✅ Do score differences reflect semantic emphasis differences?
  - Example: Chunk mainly about education (0.75) with economic mention (0.45) - difference reflects emphasis
- ❌ Are scores inverted relative to actual emphasis?
  - Example: Chunk mainly about education but econ=0.8, edu=0.4 (wrong emphasis)
- ⚠️ Are scores too flat (all similar)? Indicates poor discrimination
- ⚠️ Are scores too extreme (0.95 or 0.05)? May indicate overconfidence

**Pattern consistency (critical for BERTje training)**:
- Do similar texts produce similar score patterns?
- Do semantically different texts produce different score patterns?
- Can BERTje learn meaningful distinctions from these score patterns?

---

### 3. Semantic Judgments & Score Pattern Evaluation

For each chunk, record:

**Step 1: Identify semantic topic presence (human/LLM judgment)**:
```
Educational Disadvantage & Brain Drain:         [ ] Not present  [ ] Marginal  [x] Present  [ ] Strong
Governance Distrust & Corruption:               [ ] Not present  [x] Marginal  [ ] Present  [ ] Strong
Persistent Poverty & Economic Vulnerability:    [x] Not present  [ ] Marginal  [ ] Present  [ ] Strong
Social Fragmentation & Racism:                  [ ] Not present  [ ] Marginal  [ ] Present  [x] Strong
```

**Step 2: Map expected score ranges for each judgment**:
- Not present → expect score < 0.2
- Marginal → expect score 0.2-0.5
- Present → expect score 0.4-0.7
- Strong → expect score > 0.6

**Step 3: Evaluate actual cosine score pattern**:
```
Chunk text: [...]

Actual score pattern: [edu=0.45, gov=0.32, econ=0.12, racism=0.78]

Human semantic judgment: [edu=Present, gov=Marginal, econ=Not_present, racism=Strong]

Assessment per topic:
- Educational:  0.45 → Present (human) → ✗ Too low (should be 0.5-0.7 range)
- Governance:   0.32 → Marginal (human) → ✓ Correct range
- Economic:     0.12 → Not present (human) → ✓ Correct, appropriately low
- Racism:       0.78 → Strong (human) → ✓ Correct, appropriately high
```

**Step 4: Evaluate score pattern shape**:
```
Pattern shape: Low-Medium-VeryLow-High [0.45, 0.32, 0.12, 0.78]
Semantic shape: Present-Marginal-Absent-Strong

Pattern quality: GOOD - shape generally matches, but Educational slightly under-scored
Training sufficiency: YES - BERTje can learn "strong racism + educational presence" pattern
```

**Overall score pattern judgment**:
- [ ] Excellent - all 4 scores match semantic presence, pattern shape is perfect
- [x] Good - 3/4 scores match well, pattern shape is learnable, minor issues won't harm training
- [ ] Fair - 2/4 scores match, pattern shape partially correct, may confuse training
- [ ] Poor - pattern shape doesn't match content, will mislead training

**Notes**: Educational score 0.45 slightly low for "Present" judgment (expect 0.5-0.7), but overall pattern of [moderate edu + strong racism + low econ/gov] is correct and learnable.

---

### 4. Dictionary Awareness & Keyword Analysis (Secondary)

**Dictionary v16 consists of**:
- **300 terms per topic** (1200 terms total)
- **Cosine similarity range**: 0.7-1.0 to seed terms
- **Weighted terms**: 0.7-1.0 weights based on relevance and frequency
- **Mix of**: Exact seed terms (cosine=1.0), semantically similar expansions (cosine=0.7-0.95), domain terms (geographic names, historical dates)

**AFTER semantic assessment**, analyze dictionary influence:

**Check for dictionary term presence**:
- Which dictionary terms appear in the text?
- Are they high-weight terms (0.9-1.0) or lower-weight terms (0.7-0.8)?
- Are they exact seeds (cosine=1.0) or expanded candidates?
- Do dictionary terms explain the scores?

**Assess scoring mechanism**:
- ✅ **Semantic scoring**: High scores without exact dictionary keywords (good! shows generalization)
- ✅ **Balanced**: Mix of dictionary terms and related concepts
- ⚠️ **Keyword-driven**: High scores only when dictionary terms present
- ❌ **Keyword-dependent**: Zero scores without dictionary matches (bad! shows overfitting)
- ❌ **Cross-domain false positives**: Generic terms (e.g., "1863", "koloniaal") appearing in wrong-topic chunks

**Document**:
```
Dictionary terms found: "onderwijs" (3×, w=0.9), "achterstand" (1×, not in dict), "caribisch" (2×, w=0.75)
Assessment: Scores likely driven by semantic similarity, not just keyword matching.
Evidence: Related concepts ("leerlingen", "school") also contribute despite "leerlingen" being lower-weight (0.85).
Concern: Historical term "1863" appears but with Governance context, not Educational - may cause cross-topic confusion.
```

**Common dictionary terms across topics** (check for cross-contamination):
- Geographic: "curaçao", "bonaire", "suriname", "aruba", "antillen" (appear in all topics, weight=0.75)
- Historical: "1863", "koloniale", "geschiedenis", "slavernijverleden" (appear in all topics, weight=0.7-0.8)
- These terms should score moderately across topics; very high scores may indicate dictionary overfitting

---

### 5. Output Format

**Evaluation record per chunk**:

```csv
chunk_id, chunk_text,
score_education, score_governance, score_economic, score_racism,
human_education, human_governance, human_economic, human_racism,
match_education, match_governance, match_economic, match_racism,
pattern_quality, training_sufficiency,
assessment_notes,
dict_terms_found, keyword_analysis
```

**Fields**:
- `chunk_id`: Unique identifier
- `chunk_text`: Full text of chunk
- `score_*`: Actual cosine scores from dictionary (0-1)
- `human_*`: Human/LLM semantic judgment (not_present | marginal | present | strong)
- `match_*`: Does score match human judgment? (correct | too_high | too_low | severely_wrong)
- `pattern_quality`: Overall score pattern assessment (excellent | good | fair | poor)
- `training_sufficiency`: Can BERTje learn from this pattern? (yes | marginal | no)
- `assessment_notes`: Free-text explanation of pattern shape and learnability
- `dict_terms_found`: List of dictionary terms found in text with weights
- `keyword_analysis`: Assessment of dictionary influence on score pattern

---

### 6. Aggregate Analysis

**After evaluating sample, compute**:

**Pattern quality metrics** (PRIMARY METRICS):
- % Excellent patterns: All 4 scores match semantic judgment perfectly
- % Good patterns: 3-4 scores match, pattern shape learnable
- % Fair patterns: 2 scores match, pattern partially learnable
- % Poor patterns: Pattern shape doesn't match, will mislead training

**Training sufficiency** (CRITICAL QUESTION):
- % Yes: BERTje can learn meaningful topic understanding from this pattern
- % Marginal: Pattern somewhat learnable but noisy
- % No: Pattern will confuse training

**Score-semantic alignment per topic**:
- Educational: X% correct match, Y% too high, Z% too low
- Governance: X% correct match, Y% too high, Z% too low
- Economic: X% correct match, Y% too high, Z% too low
- Racism: X% correct match, Y% too high, Z% too low

**Pattern consistency**:
- Do similar texts produce similar score patterns? (assess variance)
- Do different texts produce different score patterns? (assess discrimination)
- Are there systematic pattern distortions? (e.g., always under-scoring Economic)

**Cross-topic score patterns**:
- Common patterns: [High-High-Low-Low], [High-Low-High-Low], etc.
- Do these patterns make semantic sense?
- Are interconnected topics scoring together appropriately?

**Dictionary influence on patterns**:
- Semantic generalization rate: % correct patterns WITHOUT dictionary terms
- Dictionary overfitting rate: % incorrect patterns WITH dictionary terms
- Cross-contamination: Do shared terms (geographic, historical) distort patterns?

---

## Key Principles

### ✅ DO
1. **Read the full text** before looking at scores
2. **Judge semantic content independently** - ignore assigned primary label completely
3. **Evaluate the complete 4-score pattern** [edu, gov, econ, racism] as a vector
4. **Assess pattern shape** - does the score pattern shape match the semantic content shape?
5. **Ask "Can BERTje learn from this?"** - focus on training sufficiency, not perfection
6. **Expect multi-topic patterns** - interconnected high scores are often correct
7. **Document pattern reasoning** - explain why pattern is/isn't learnable

### ❌ DON'T
1. **Don't look at primary labels** - they're sampling shortcuts, NOT ground truth
2. **Don't ask "which topic is correct"** - there's no single answer, evaluate the full pattern
3. **Don't rely on keyword matching** for primary evaluation
4. **Don't ignore context** (read full chunk, not snippets)
5. **Don't evaluate topics independently** - assess pattern as a whole
6. **Don't require perfection** - "good enough to learn from" is sufficient
7. **Don't skip pattern shape documentation** (BERTje learns from shapes!)

---

## Evaluating Topic Interconnections

**Critical context**: These 4 topics are **fundamentally interconnected** due to their shared roots in slavery/colonialism. This is NOT a weakness - it reflects reality!

### Expected Patterns in Multi-Topic Chunks

**Educational ↔ Economic**: Strong connection expected
- Educational disadvantage → limited job opportunities → poverty
- Example: "Dropouts struggle to find work" should score high on BOTH topics

**Racism ↔ All Topics**: Racism permeates all domains
- Racism in education, governance, economic systems
- Example: "Discrimination in hiring" should score high on BOTH Racism AND Economic

**Governance ↔ Economic**: Patronage/corruption affects economic opportunity
- Example: "Nepotism in government contracts" should score high on BOTH topics

**Educational ↔ Governance**: Colonial education system, language policy
- Example: "Dutch-language requirements exclude local population" touches BOTH topics

### Evaluation Questions for Multi-Topic Chunks

1. **Are legitimate multi-topic chunks captured?**
   - ✅ Good: Chunk about educational racism scores high on BOTH Educational and Racism
   - ❌ Bad: Same chunk scores high only on Educational, low on Racism

2. **Are scores proportional to emphasis?**
   - ✅ Good: Chunk primarily about education (0.8) with mention of economic impact (0.4)
   - ❌ Bad: Equal mention of both topics but scores are 0.8 vs 0.15

3. **Do interconnections make semantic sense?**
   - ✅ Good: Educational + Economic high scores (known strong connection)
   - ⚠️ Investigate: Educational + Governance high scores (less common but can occur with language policy)

---

## Why This Method?

### Single-label classification metrics fail because:
- **There IS no single correct topic** - these topics are inherently multi-dimensional
- No ground truth labels exist (this IS the labeling process)
- Primary labels are just sampling shortcuts, not answers
- Asking "is this Educational or Economic?" misses that it can be BOTH
- **BERTje is NOT trained on classification** - it learns from multi-label score patterns

### Keyword matching fails because:
- Topics can be discussed without using specific terms (especially in policy language)
- Dictionary terms may appear in off-topic contexts (e.g., "1863" in governance vs. educational context)
- Semantic similarity ≠ keyword overlap
- Dictionary is training input, not evaluation ground truth
- **Dutch Caribbean context**: Some policy texts use euphemisms or avoid explicit mention of slavery legacy

### Automated metrics fail because:
- Inter-annotator agreement requires multiple humans
- Semantic nuance requires understanding of historical context
- Cannot assess whether pattern shape is "learnable" by BERTje
- **Interconnected topics**: Cannot evaluate topics in isolation
- Pattern consistency requires human judgment across multiple examples

### Manual semantic pattern assessment succeeds because:
- Humans understand semantic content AND historical context
- Can judge whether **score pattern shape** matches **content shape**
- Can assess all 4 scores as a unified pattern, not independently
- Can evaluate training sufficiency: "Can BERTje learn from this pattern?"
- Can detect systematic pattern distortions across samples
- Can recognize topic interconnections as appropriate, not errors
- **Focuses on the right question**: Not "which topic?" but "does pattern represent content?"

---

## Sample Size Guidelines

**Minimum for each topic × tier combination**: 10 chunks
- 4 topics × 4 tiers = 16 conditions
- 10 chunks per condition = **160 chunks minimum**

**Recommended**: 20 chunks per condition = **320 chunks**

**For quick assessment**: 5 chunks per condition = **80 chunks**

---

## Example Evaluation

**Chunk**: "De onderwijskansen op Curaçao blijven achter bij het Europees Nederland. Vooral de taalbarrière tussen Papiaments en Nederlands speelt een grote rol."

**Translation**: "Educational opportunities in Curaçao lag behind European Netherlands. Especially the language barrier between Papiamentu and Dutch plays a major role."

**Actual Score Pattern**: [edu=0.82, gov=0.23, econ=0.31, racism=0.28]

---

**Step 1: Human Semantic Judgment** (read text, ignore scores):
- Educational: **Strong** (primary focus on educational disadvantage and language barriers in education)
- Governance: **Not present** (no governance content)
- Economic: **Marginal** (implied economic consequences of educational lag, but not explicit)
- Racism: **Marginal** (language imposition is colonial/racist legacy, but not explicit racism discussion)

**Step 2: Expected Score Ranges**:
- Educational: Strong → expect > 0.6
- Governance: Not present → expect < 0.2
- Economic: Marginal → expect 0.2-0.5
- Racism: Marginal → expect 0.2-0.5

**Step 3: Evaluate Actual Pattern**:
```
Topic        | Score | Human      | Expected Range | Match?
-------------|-------|------------|----------------|--------
Educational  | 0.82  | Strong     | >0.6           | ✓ Correct
Governance   | 0.23  | Not present| <0.2           | ✗ Slightly high (marginal range)
Economic     | 0.31  | Marginal   | 0.2-0.5        | ✓ Correct
Racism       | 0.28  | Marginal   | 0.2-0.5        | ✓ Correct
```

**Step 4: Evaluate Pattern Shape**:
```
Score pattern shape:    [High -------- Low -- Medium -- Medium]
                        [0.82, 0.23, 0.31, 0.28]

Semantic content shape: [Strong ------- Absent - Marginal - Marginal]

Pattern assessment: EXCELLENT
- Shape matches semantic content very well
- Educational clearly dominant (0.82 >> others)
- Economic and Racism appropriately moderate (0.31, 0.28)
- Governance appropriately low (0.23, though could be even lower)
- Relative magnitudes reflect actual topic emphasis
```

**Overall Pattern Quality**: **Excellent** (all 4 scores match semantic judgment well)

**Training Sufficiency**: **Yes** - BERTje can clearly learn:
- "Educational disadvantage + language barriers" → high Educational score
- Implied economic/racist dimensions → moderate scores
- Absent governance → low score
- Pattern shape [0.82, 0.23, 0.31, 0.28] is highly informative and learnable

**Dictionary Analysis**:
- "onderwijskansen" - Not exact dict match → shows semantic generalization (positive!)
- "taalbarrière" related to "taalbarrières" (w=0.8), "taal" (w=0.9) → semantic expansion working
- "papiaments" (w=0.9) in Educational dict → appropriate domain term
- "Curaçao" (w=0.75) in all dicts → not distorting pattern, appropriate context
- High Educational score despite non-exact matches demonstrates good semantic understanding

---

## Documentation Template

Use this template for each evaluation session:

```markdown
# Cosine Label Evaluation - [Dataset Name]

**Date**: YYYY-MM-DD
**Evaluator**: [Name/LLM]
**Dictionary Version**: v16 (300 terms/topic, cosine 0.7-1.0, weights 0.7-1.0)
**Sample size**: [N chunks]
**Sampling strategy**: [e.g., Stratified by primary label × confidence tier - NOTE: primary labels used only for sampling, not evaluation]

## Pattern Quality Summary (PRIMARY METRICS)
- Excellent patterns: X chunks (Y%) - all 4 scores match semantic judgment perfectly
- Good patterns: X chunks (Y%) - 3-4 scores match, pattern shape learnable
- Fair patterns: X chunks (Y%) - 2 scores match, pattern partially learnable
- Poor patterns: X chunks (Y%) - pattern shape doesn't match content

## Training Sufficiency (CRITICAL ASSESSMENT)
- Yes (BERTje can learn): X chunks (Y%)
- Marginal (somewhat learnable): X chunks (Y%)
- No (will confuse training): X chunks (Y%)

**Overall verdict**: [Ready for training / Needs dictionary refinement / Major issues]

## Score-Semantic Alignment by Topic
**Educational**:
- Correct: X% | Too high: Y% | Too low: Z%
- Systematic issues: [description]

**Governance**:
- Correct: X% | Too high: Y% | Too low: Z%
- Systematic issues: [description]

**Economic**:
- Correct: X% | Too high: Y% | Too low: Z%
- Systematic issues: [description]

**Racism**:
- Correct: X% | Too high: Y% | Too low: Z%
- Systematic issues: [description]

## Common Score Patterns
List most frequent patterns and assess semantic appropriateness:
- [High-High-Low-Low]: X chunks - [Educational+Racism focus, appropriate for...]
- [High-Low-High-Low]: X chunks - [Educational+Economic, appropriate for...]
- [description of whether patterns make semantic sense]

## Dictionary Analysis
**Semantic Generalization** (correct patterns WITHOUT dictionary terms):
- Rate: X/Y chunks (Z%)
- Assessment: [Excellent/Good/Poor] - [dictionary shows semantic understanding vs. keyword dependency]

**Cross-Contamination Issues**:
- Geographic terms (curaçao, bonaire, etc.): [causing problems? which topics?]
- Historical terms (1863, koloniale, etc.): [causing problems? which topics?]
- Problem terms requiring weight adjustment: [list]

## Pattern Consistency Assessment
- Similar texts producing similar patterns: [Yes/Somewhat/No] - [examples]
- Different texts producing different patterns: [Yes/Somewhat/No] - [examples]
- Systematic distortions detected: [list any recurring issues]

## Key Findings
[Bullet points of main observations about pattern quality and training sufficiency]

## Recommendations for Dictionary v17
1. [Specific term additions/removals to improve pattern quality]
2. [Weight adjustments for better discrimination]
3. [Cross-topic term handling strategies]
4. [Suggestions to improve pattern learnability]

## Detailed Evaluations
[Per-chunk pattern assessments - see output format above]
```

---

## Change Log

**Version 2.0** - 2025-11-26
- **MAJOR CONCEPTUAL SHIFT**: Reframed from single-label classification evaluation to multi-label **score pattern evaluation**
- Emphasized that primary labels are sampling shortcuts, NOT ground truth
- Reframed core question from "which topic is correct?" to "does score pattern shape match content shape?"
- Added **training sufficiency** as critical evaluation metric: "Can BERTje learn from this pattern?"
- Updated all assessment criteria to focus on 4-score pattern as unified vector [edu, gov, econ, racism]
- Added pattern shape visualization and comparison in examples
- Updated output format to include pattern_quality and training_sufficiency fields
- Completely rewrote aggregate analysis section to focus on pattern metrics, not classification accuracy
- Updated Key Principles: added "evaluate pattern as whole", "ask if learnable", "don't require perfection"
- Rewrote example evaluation to demonstrate pattern-based assessment methodology
- Added research context and link to TOPIC_FRAMEWORK_CONTEXT.md
- Added dictionary v16 specifications (300 terms/topic, cosine/weight ranges)
- Enhanced documentation template with pattern quality and training sufficiency sections

**Version 1.0** - 2025-11-19
- Initial methodology document
- Standard semantic assessment protocol (classification-focused)

---

**Purpose**: Standard methodology for multi-label cosine score pattern quality assessment in Dutch Caribbean slavery legacy research project. Evaluates whether dictionary-based score patterns are sufficient to train BERTje to understand topic semantics.
