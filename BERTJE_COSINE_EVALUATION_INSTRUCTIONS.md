# BERTJE + COSINE DUAL-SCORING EVALUATION PROTOCOL
## Instructions for Evaluating 10-Chunk Samples

**Version:** 1.0
**Date:** 2025-12-02
**Purpose:** Evaluate BERTJE-labeled dataset with both BERTJE predictions and cosine rescaled scores

---

## CRITICAL CONTEXT: What You're Evaluating

This is a **dual-scoring system**:
1. **BERTJE predictions**: Supervised neural model trained on labeled corpus chunks
2. **Cosine rescaled scores**: Dictionary-based semantic similarity (0-2.0 range)

**Your job**: Determine which method (or both) correctly identifies topic presence and strength by **reading the full text semantically**.

**Research context**: The 4 topics represent **structural legacies of slavery** in Dutch Caribbean policy:
- Educational Disadvantage & Brain Drain
- Social Fragmentation & Racism
- Governance Distrust & Corruption
- Persistent Poverty & Economic Vulnerability

These are **interconnected** (not isolated categories). Texts often address multiple topics. Historical connections may be **implicit** (contemporary language without explicit slavery mentions).

---

## SAMPLE SELECTION: 10 Chunks Per Sample Type

You will evaluate **10 carefully selected chunks** based on the sampling strategy provided by the user. Common sampling strategies:

### Strategy A: Agreement vs. Disagreement
- 3 chunks: Both agree (same top topic), both correct
- 3 chunks: Both agree, both wrong
- 2 chunks: Disagree, BERTJE correct
- 2 chunks: Disagree, Cosine correct

### Strategy B: BERTJE Confidence Levels
- 3 chunks: High BERTJE confidence (≥0.8)
- 4 chunks: Medium BERTJE confidence (0.4-0.8)
- 3 chunks: Low BERTJE confidence (<0.4)

### Strategy C: Cosine Quality Tiers
- 2 chunks: Core tier (rescaled ≥1.5)
- 3 chunks: Moderate tier (rescaled 1.0-1.5)
- 3 chunks: Weak tier (rescaled 0.5-1.0)
- 2 chunks: Context/Noise tier (rescaled <0.5)

### Strategy D: Multi-Topic Focus
- 5 chunks: Likely multi-topic (multiple scores ≥1.0)
- 5 chunks: Likely single-topic (one dominant score)

**User will specify which strategy to use.**

---

## STEP-BY-STEP EVALUATION PROCESS

### STEP 1: Receive Sample Data

User will provide a CSV or table with these columns:
- `chunk_id`: Unique identifier
- `raw_text`: Full text to evaluate
- `text_for_scoring`: Preprocessed text (what cosine scored)
- `bertje_topic_1` through `bertje_topic_4`: BERTJE predictions (topic names)
- `bertje_score_1` through `bertje_score_4`: BERTJE confidence scores
- `rescaled_Educational`, `rescaled_Governance`, `rescaled_Poverty`, `rescaled_Racism`: Cosine scores
- `primary_topic_rescaled`: Cosine's top-1 prediction
- `max_score_rescaled`: Cosine's highest score
- `quality_tier`: Core/Moderate/Weak/Context/Noise

**You will receive 10 chunks.**

---

### STEP 2: For Each Chunk - Semantic Evaluation (MOST IMPORTANT)

**DO NOT look at BERTJE or cosine predictions yet.**

Read the `raw_text` fully and answer these questions:

#### A. Overall Understanding
1. **What is this text about?** (1-2 sentence summary in your own words)
2. **Slavery legacy connection**:
   - Explicit (directly mentions slavery/colonialism)
   - Implicit (discusses contemporary problems rooted in slavery without naming it)
   - None (unrelated to slavery legacies)
3. **Reparative justice measure discussed?** (Yes/No, which one: Cessation/Restitution/Rehabilitation/Compensation/Satisfaction)

#### B. Rate Each Topic (0-3 Scale) - DO ALL 4 INDEPENDENTLY

**Educational Disadvantage & Brain Drain:**
- **Rating (0-3)**: ___
- **Rationale**: Why this rating? What specific content supports it?
- **Key evidence**: Quote 1-2 phrases that indicate presence/absence

**Governance Distrust & Corruption:**
- **Rating (0-3)**: ___
- **Rationale**: Why this rating? What specific content supports it?
- **Key evidence**: Quote 1-2 phrases that indicate presence/absence

**Persistent Poverty & Economic Vulnerability:**
- **Rating (0-3)**: ___
- **Rationale**: Why this rating? What specific content supports it?
- **Key evidence**: Quote 1-2 phrases that indicate presence/absence

**Social Fragmentation & Racism:**
- **Rating (0-3)**: ___
- **Rationale**: Why this rating? What specific content supports it?
- **Key evidence**: Quote 1-2 phrases that indicate presence/absence

**Rating scale:**
- **0** = Not present (topic not mentioned or discussed)
- **1** = Weakly present (tangential mention, minor aspect, setup/context only)
- **2** = Moderately present (clear discussion, secondary theme)
- **3** = Strongly present (central theme, extensively discussed)

#### C. Multi-Topic Assessment
- **How many topics rated ≥2?** ___
- **Is this multi-topic content?** Yes/No
- **Intersectionality?** (e.g., "racism in education", "corruption affecting economy") - describe if present

#### D. Primary Topic (Your Assessment)
- **Which single topic is MOST central?** ___
- **Confidence in this assessment**: High/Medium/Low
- **Why this topic over others?** (brief explanation)

---

### STEP 3: Compare to BERTJE Predictions

**Now look at BERTJE's predictions.**

Record:
- **BERTJE top-1 topic**: ___ (score: ___)
- **BERTJE all topics with scores ≥0.3**: List all (topic: score)
- **BERTJE confidence interpretation**: High (≥0.7) / Medium (0.4-0.7) / Low (<0.4)

#### Evaluate BERTJE Performance:

**Top-1 Accuracy:**
- ✅ CORRECT: BERTJE top-1 matches your primary topic assessment
- ❌ WRONG: BERTJE top-1 is different from your assessment
- ⚠️ ACCEPTABLE: BERTJE picked topic you rated 2-3, just not the highest

**Multi-Label Coverage:**
For each topic you rated ≥2:
- Did BERTJE predict it (score ≥0.3)? ✅/❌
- Overall: Did BERTJE detect all semantically present topics? ✅/❌

**False Positives:**
For each topic BERTJE scored ≥0.5:
- Did you rate it ≥1? If not, this is a false positive
- List false positives: ___

**Intensity Alignment:**
For topics you rated 3 (strongly present):
- BERTJE score should be high (≥0.7) - is it? ✅/❌
For topics you rated 0 (not present):
- BERTJE score should be low (<0.3) - is it? ✅/❌

#### BERTJE Quality Label:
Choose the most appropriate:
- **MATCH-STRONG**: Top-1 correct, high confidence (≥0.7), semantic rating = 3
- **MATCH-MODERATE**: Top-1 correct, confidence and rating align reasonably
- **MATCH-WEAK**: Detected topic weakly (low confidence, rating 1-2)
- **WRONG-TOPIC**: Top-1 is incorrect (predicted A, should be B)
- **FALSE-POSITIVE**: High confidence (≥0.7) for topic rated 0-1
- **MISSING-TOPIC**: Topic rated ≥2 but BERTJE score <0.3

#### Hypothesis: Why Did BERTJE Predict This?
- Which words/phrases in the text likely triggered BERTJE's prediction?
- Is this a spurious correlation BERTJE learned? (e.g., "Suriname" → Poverty)
- Did BERTJE learn a valid pattern?
- Did training data quality affect this?

---

### STEP 4: Compare to Cosine Scores

**Now look at cosine rescaled scores.**

Record:
- **Cosine top-1 topic** (from `primary_topic_rescaled`): ___ (score: ___)
- **Cosine quality tier**: Core/Moderate/Weak/Context/Noise
- **Cosine all topics with rescaled score ≥1.0**: List all (topic: score)

#### Evaluate Cosine Performance:

**Top-1 Accuracy:**
- ✅ CORRECT: Cosine top-1 matches your primary topic assessment
- ❌ WRONG: Cosine top-1 is different from your assessment
- ⚠️ ACCEPTABLE: Cosine picked topic you rated 2-3, just not the highest

**Multi-Label Coverage:**
For each topic you rated ≥2:
- Did cosine detect it (rescaled score ≥1.0)? ✅/❌
- Overall: Did cosine detect all semantically present topics? ✅/❌

**False Positives:**
For each topic cosine scored ≥1.5:
- Did you rate it ≥2? If not, this is a false positive
- List false positives: ___

**Tier Alignment:**
- Your highest semantic rating (0-3): ___
- Expected tier: Rating 3 → Core (≥1.5), Rating 2 → Moderate (≥1.0), Rating 1 → Weak (0.5-1.0), Rating 0 → Noise (<0.5)
- Actual tier: ___
- Alignment? ✅/❌

#### Cosine Quality Label:
Choose the most appropriate:
- **MATCH-STRONG**: Top-1 correct, Core tier, semantic rating = 3
- **MATCH-MODERATE**: Top-1 correct, Moderate tier, rating 2-3
- **MATCH-WEAK**: Detected topic weakly (Weak tier, rating 1-2)
- **WRONG-TOPIC**: Top-1 is incorrect
- **FALSE-POSITIVE**: Core tier (≥1.5) for topic rated 0-1
- **MISSING-TOPIC**: Topic rated ≥2 but rescaled score <1.0
- **TIER-MISMATCH**: Correct topic but wrong tier (e.g., rating 3 but Weak tier)

#### Hypothesis: Why Did Cosine Score This Way?
- Look at `text_for_scoring`: Which keywords are present?
- Are dictionary terms present but with low weights (0.5-0.55)?
- Were key terms removed during preprocessing? (compare `raw_text` vs `text_for_scoring`)
- Are there missing dictionary terms that should be added?
- Are generic terms (e.g., "geschiedenis", "historisch") dominating the score?

---

### STEP 5: BERTJE vs. Cosine Comparison

#### Agreement Analysis:
- **Same top-1 topic?** ✅/❌
- **If same**: Did both get it correct? ✅/❌
- **If different**: Which method was correct? BERTJE / Cosine / Neither / Both acceptable

#### Multi-Label Coverage Comparison:
- **BERTJE detected ___ / ___ semantically present topics**
- **Cosine detected ___ / ___ semantically present topics**
- **Which method has better multi-label recall?** BERTJE / Cosine / Tie

#### Intensity Correlation:
- For the primary topic, do BERTJE confidence and cosine rescaled score both align with semantic rating? ✅/❌
- Example: Semantic rating = 3, BERTJE = 0.9, Cosine = 1.8 → Both align ✅
- Example: Semantic rating = 3, BERTJE = 0.3, Cosine = 0.7 → Neither aligns ❌

#### Divergence Analysis (if they disagree):
**Root cause of disagreement** (choose primary reason):
- BERTJE learned spurious correlation (explain)
- Cosine missing key dictionary terms (list missing terms)
- BERTJE generalizes better (handles paraphrasing/synonyms)
- Cosine captures rare domain-specific terms BERTJE never saw
- Text preprocessing artifact (cosine scored different text)
- Implicit language (BERTJE handles better / Cosine handles better)
- Multi-topic confusion (one method confused overlapping topics)
- Other (explain)

**Winner for this chunk:** BERTJE / Cosine / Tie / Neither

---

### STEP 6: Special Assessments

#### Historical-Structural Understanding:
- **Does this chunk require understanding implicit slavery legacies?** Yes/No
- **If yes**: Did BERTJE capture it? ✅/❌
- **If yes**: Did Cosine capture it? ✅/❌
- **Explanation**: How is the slavery legacy implicit in this text?

#### Intersectionality:
- **Does this chunk discuss overlapping topics?** Yes/No (e.g., racism in education)
- **If yes**: Did BERTJE capture the intersection? ✅/❌
- **If yes**: Did Cosine capture the intersection? ✅/❌

#### Difficulty Rating:
Rate how challenging this chunk is to classify:
- **Easy** (1): Clear single topic, explicit language
- **Medium** (2): Some ambiguity, but primary topic clear
- **Hard** (3): Multi-topic, implicit language, requires deep context
- **Very Hard** (4): Ambiguous even with full context, expert disagreement likely

---

### STEP 7: Document Key Findings for This Chunk

For each chunk, create a summary:

```markdown
## Chunk [ID]: [Brief Description]

**Semantic Assessment:**
- Primary topic: [Topic] (rating: X/3)
- Other topics present: [List topics rated ≥2]
- Multi-topic? Yes/No
- Slavery legacy: Explicit/Implicit/None
- Difficulty: [1-4]

**BERTJE Performance:**
- Top-1 prediction: [Topic] (confidence: X.XX)
- Quality label: [Label]
- Correct? ✅/❌
- Multi-label recall: X/X topics detected
- Key issue: [Brief description if wrong]

**Cosine Performance:**
- Top-1 prediction: [Topic] (score: X.XX)
- Quality tier: [Tier]
- Quality label: [Label]
- Correct? ✅/❌
- Multi-label recall: X/X topics detected
- Key issue: [Brief description if wrong]

**Comparison:**
- Agreement? ✅/❌
- Winner: BERTJE/Cosine/Tie/Neither
- Root cause of divergence: [Brief explanation]

**Recommendations:**
- For BERTJE: [Specific suggestion]
- For Cosine: [Specific suggestion, e.g., "Add keyword 'X' with weight 0.9"]

**Notable quotes:** "[Key phrase from text that illustrates the main point]"
```

---

## STEP 8: Aggregate Analysis Across 10 Chunks

After evaluating all 10 chunks, calculate:

### Overall Accuracy:
```
BERTJE top-1 accuracy: ___/10 correct
Cosine top-1 accuracy: ___/10 correct
Agreement rate: ___/10 same top-1 prediction
Both correct when agree: ___/[agreements]
```

### Per-Topic Performance:
For each of the 4 topics:
```
[Topic Name]:
- Semantic prevalence: X chunks rated ≥2
- BERTJE detected: X/X (recall)
- Cosine detected: X/X (recall)
- BERTJE false positives: X chunks
- Cosine false positives: X chunks
```

### Multi-Label Performance:
```
Chunks with multiple topics (≥2 topics rated ≥2): ___/10
BERTJE avg multi-label recall: ___% (detected topics / present topics)
Cosine avg multi-label recall: ___%
```

### Intensity Alignment:
```
BERTJE confidence correlates with semantic rating: ___/10 chunks
Cosine tier correlates with semantic rating: ___/10 chunks
```

### Quality Label Distribution:

**BERTJE:**
- MATCH-STRONG: ___
- MATCH-MODERATE: ___
- MATCH-WEAK: ___
- WRONG-TOPIC: ___
- FALSE-POSITIVE: ___
- MISSING-TOPIC: ___

**Cosine:**
- MATCH-STRONG: ___
- MATCH-MODERATE: ___
- MATCH-WEAK: ___
- WRONG-TOPIC: ___
- FALSE-POSITIVE: ___
- MISSING-TOPIC: ___
- TIER-MISMATCH: ___

### Divergence Patterns:
When BERTJE and Cosine disagreed (list all):
- Winner: BERTJE (X times), Cosine (X times), Neither (X times)
- Common root causes:
  1. [Most frequent cause] (X occurrences)
  2. [Second most frequent] (X occurrences)
  3. [Third most frequent] (X occurrences)

### Historical-Structural Understanding:
```
Chunks requiring implicit slavery legacy understanding: ___/10
BERTJE correctly handled: ___
Cosine correctly handled: ___
Neither captured: ___
```

### Difficulty Analysis:
```
Easy chunks (1): ___ → BERTJE accuracy: ___%, Cosine accuracy: ___%
Medium chunks (2): ___ → BERTJE accuracy: ___%, Cosine accuracy: ___%
Hard chunks (3): ___ → BERTJE accuracy: ___%, Cosine accuracy: ___%
Very hard chunks (4): ___ → BERTJE accuracy: ___%, Cosine accuracy: ___%
```

---

## STEP 9: Key Insights and Recommendations

### Summary of Findings:
Write 3-5 paragraphs summarizing:
1. **Overall performance**: Which method performs better? By how much?
2. **Complementary strengths**: Where does BERTJE excel? Where does Cosine excel?
3. **Common failure modes**: What mistakes does each method make?
4. **Multi-topic handling**: How well do they handle intersectionality?
5. **Historical context**: Do they capture implicit slavery legacies?

### Top 3 BERTJE Issues:
1. [Issue] - Found in X/10 chunks
   - **Example**: Chunk [ID]
   - **Root cause**: [Explanation]
   - **Recommendation**: [Specific action, e.g., "Add more training data for Education topic with implicit references"]

2. [Issue] - Found in X/10 chunks
   - **Example**: Chunk [ID]
   - **Root cause**: [Explanation]
   - **Recommendation**: [Specific action]

3. [Issue] - Found in X/10 chunks
   - **Example**: Chunk [ID]
   - **Root cause**: [Explanation]
   - **Recommendation**: [Specific action]

### Top 3 Cosine Issues:
1. [Issue] - Found in X/10 chunks
   - **Example**: Chunk [ID]
   - **Root cause**: [Explanation]
   - **Recommendation**: [Specific action, e.g., "Add keywords: 'schooluitval', 'onderwijsmigratie' with weight 0.95"]

2. [Issue] - Found in X/10 chunks
   - **Example**: Chunk [ID]
   - **Root cause**: [Explanation]
   - **Recommendation**: [Specific action]

3. [Issue] - Found in X/10 chunks
   - **Example**: Chunk [ID]
   - **Root cause**: [Explanation]
   - **Recommendation**: [Specific action]

### Dictionary Improvements (Specific):
List concrete keyword additions/changes:
```
ADD to Educational topic:
- "schooluitval" (weight: 1.0) - direct term for dropout
- "onderwijsmigratie" (weight: 0.95) - educational migration/brain drain

ADJUST weights:
- "geschiedenis": 0.55 → 0.45 (too generic, causing false positives)
- "racisme": keep at 1.0 (performs well)

REMOVE:
- [term]: causing too many false positives, not useful
```

### BERTJE Training Recommendations:
```
1. Add more training examples for: [specific topic/pattern]
2. Rebalance training data: [which topic is underrepresented]
3. Consider data augmentation for: [edge cases]
4. Review training labels for: [specific pattern where BERTJE consistently wrong]
```

### Hybrid Approach Suggestions:
```
When to trust BERTJE:
- [Situation/pattern where BERTJE outperforms]

When to trust Cosine:
- [Situation/pattern where Cosine outperforms]

Ensemble strategy:
- [How to combine both methods, e.g., "Use BERTJE for primary topic, Cosine for multi-label detection"]

Conflict resolution:
- [How to handle disagreements, e.g., "When both confident but disagree, default to Cosine for Education/Racism, BERTJE for Governance/Poverty"]
```

---

## CRITICAL REMINDERS

### ✅ DO:
- Read EVERY `raw_text` fully before looking at predictions
- Rate all 4 topics independently (0-3 scale)
- Treat BERTJE and Cosine as BOTH potentially wrong (semantic evaluation is ground truth)
- Document specific evidence (quote phrases) for your ratings
- Consider multi-topic presence (chunks can be 2-3 topics)
- Think about implicit slavery legacies (contemporary language without explicit mentions)
- Note intersectionality (racism in education, corruption in economy)
- Provide SPECIFIC, ACTIONABLE recommendations (exact keywords to add, not vague suggestions)
- Check if `text_for_scoring` differs significantly from `raw_text` (preprocessing impact)

### ❌ DON'T:
- Keyword search instead of full semantic reading
- Assume BERTJE is "ground truth" just because it's a neural model
- Use original cosine scores (use RESCALED scores only)
- Ignore multi-topic content (only evaluate top-1)
- Rate topics based on explicit keywords only (miss implicit content)
- Give vague recommendations like "improve dictionary" (be specific)
- Forget to compare BERTJE confidence intensity with semantic rating
- Ignore the 4-topic framework context (these are slavery legacy topics, not neutral categories)

---

## OUTPUT FORMAT

Provide your evaluation in this structure:

```markdown
# BERTJE + COSINE EVALUATION REPORT
## Sample: [Description of sample type, e.g., "High disagreement cases"]
**Date**: [Date]
**Evaluator**: Claude
**Chunks evaluated**: 10

---

## CHUNK-BY-CHUNK ANALYSIS

### Chunk 1: [ID] - [Brief description]
[Full Step 7 summary]

### Chunk 2: [ID] - [Brief description]
[Full Step 7 summary]

[...continue for all 10 chunks...]

---

## AGGREGATE ANALYSIS (Step 8 results)
[All metrics from Step 8]

---

## KEY INSIGHTS AND RECOMMENDATIONS (Step 9)
[All sections from Step 9]

---

## APPENDIX: Evaluation Methodology
- Semantic evaluation conducted before viewing predictions
- 0-3 rating scale applied independently to all 4 topics
- Multi-label assessment performed
- Intersectionality and implicit slavery legacies considered
- BERTJE confidence thresholds: High ≥0.7, Medium 0.4-0.7, Low <0.4
- Cosine relevance threshold: ≥1.0 for moderate presence
- Cosine quality tiers: Core ≥1.5, Moderate 1.0-1.5, Weak 0.5-1.0, Noise <0.25
```

---

## FINAL NOTE: Context Limitations

You (Claude) can handle approximately **10 chunks** in a single evaluation session while maintaining detailed analysis. If more chunks need evaluation:

1. **Batch approach**: Evaluate in sets of 10, then aggregate across batches
2. **Focused sampling**: Select 10 most informative chunks (divergence cases, edge cases, etc.)
3. **Iterative refinement**: Use findings from first 10 to inform selection of next 10

**Never attempt 50+ chunks in one session** - you will lose analytical depth and make superficial assessments.

---

**This protocol ensures rigorous, detailed evaluation within your context window constraints while providing actionable insights for both BERTJE and dictionary-based cosine methods.**
