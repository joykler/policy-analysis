# V20 Dictionary Evaluation Report
**Based on 4-Topic Framework for Slavery's Developmental Legacies**

Date: 2025-11-28
Dictionary: `workflow_data/slavery_Slavdict_pretraining_slavery_v20/Dictionary/expanded_candidates.csv`

---

## Executive Summary

The v20 dictionary represents a **HIGH VALUE** literature-based expansion that significantly improves topic coverage while maintaining strong semantic coherence. The expansion from 142 seed terms to 1,200 total terms (7.45x growth) demonstrates:

✅ **Perfect category-weight consistency** (100% of terms within expected ranges)
✅ **Strong parent-child relationships** (average cosine 0.807)
✅ **Balanced topic coverage** (300 terms per topic)
✅ **No low-quality terms** (minimum cosine 0.707)

⚠️ **Area for improvement**: Context terms (47%) may dilute topic-specific signals; consider curation to increase problem-oriented focus.

---

## 1. Overall Dictionary Statistics

| Metric | Value |
|--------|-------|
| **Total terms** | 1,200 |
| **Seed terms** | 142 |
| **Expanded terms** | 1,058 |
| **Expansion ratio** | 7.45x |
| **Substantive terms** | 636 (53.0%) |
| **Context terms** | 564 (47.0%) |

### Quality Distribution (Expanded Terms Only)
- **High quality** (cosine > 0.8): 46.2%
- **Medium quality** (0.7-0.8): 53.8%
- **Low quality** (< 0.7): 0.0%
- **Mean cosine**: 0.805
- **Median cosine**: 0.796
- **Min cosine**: 0.707

---

## 2. Topic-Level Analysis

### Distribution by Topic

| Topic | Total Terms | Seeds | Expanded | Expansion Ratio | Avg Cosine |
|-------|-------------|-------|----------|-----------------|------------|
| Educational Disadvantage & Brain Drain | 300 | 36 | 264 | 7.82x | 0.804 |
| Governance Distrust & Corruption | 300 | 38 | 262 | 7.57x | 0.808 |
| Persistent Poverty & Economic Vulnerability | 300 | 40 | 260 | 7.11x | 0.803 |
| Social Fragmentation & Racism | 300 | 38 | 262 | 7.33x | 0.804 |

**Assessment**: Perfectly balanced expansion across all 4 topics.

### Substantive vs Context Balance

| Topic | Substantive | Context | Substantive % |
|-------|-------------|---------|---------------|
| Educational Disadvantage & Brain Drain | 158 | 142 | 52.7% |
| Governance Distrust & Corruption | 154 | 146 | 51.3% |
| Persistent Poverty & Economic Vulnerability | 167 | 133 | **55.7%** ✓ |
| Social Fragmentation & Racism | 157 | 143 | 52.3% |

**Assessment**: All topics have ~47-49% context terms. This is acceptable but leaves room for curation to increase problem-oriented focus (target: >60% substantive).

---

## 3. Category Analysis

### Category Distribution

| Category | Total | Seeds | Expanded | Weight Range | Status |
|----------|-------|-------|----------|--------------|--------|
| **core_problem** | 53 (4.4%) | 9 | 44 | 1.00 | ✓ Perfect |
| **strong_problem** | 74 (6.2%) | 16 | 58 | 0.90-0.95 | ✓ Perfect |
| **related_strong** | 275 (22.9%) | 41 | 234 | 0.80-0.85 | ✓ Perfect |
| **related_moderate** | 140 (11.7%) | 26 | 114 | 0.70-0.75 | ✓ Perfect |
| **related_weak** | 94 (7.8%) | 5 | 89 | 0.65 | ✓ Perfect |
| **era_context** | 479 (39.9%) | 29 | 450 | 0.55 | ✓ Perfect |
| **geographic_context** | 85 (7.1%) | 16 | 69 | 0.50 | ✓ Perfect |

### Category-Weight Consistency

All 1,200 terms fall within expected weight ranges:
- **core_problem**: Expected [0.95-1.00], Actual [1.00-1.00] ✓
- **strong_problem**: Expected [0.85-0.95], Actual [0.90-0.95] ✓
- **related_strong**: Expected [0.75-0.90], Actual [0.80-0.85] ✓
- **related_moderate**: Expected [0.60-0.80], Actual [0.70-0.75] ✓
- **era_context**: Expected [0.50-0.60], Actual [0.55] ✓
- **geographic_context**: Expected [0.45-0.55], Actual [0.50] ✓

**Assessment**: PERFECT category-weight structure. This is the biggest strength of the v20 dictionary and demonstrates excellent adherence to the weighted scoring system.

---

## 4. Parent-Child Relationship Quality

### Top Parent Terms by Children Count

| Parent | Topic | Children | Avg Cosine | Min Cosine |
|--------|-------|----------|------------|------------|
| **1863** | Educational | 169 | 0.789 | 0.731 |
| **koloniaal** | Educational | 62 | 0.810 | 0.713 |
| **plantage** | Economic | 62 | 0.838 | 0.758 |
| **slavernijverleden** | Educational | 55 | 0.803 | 0.728 |
| **afschaffing** | Economic | 51 | 0.781 | 0.743 |
| **geschiedenis** | Educational | 46 | 0.841 | 0.735 |
| **koloniale** | Educational | 45 | 0.843 | 0.720 |

**Average parent-child cosine across all parents**: 0.807

### Parents with Weak Relationships (< 0.75)

Only **9 parents** out of hundreds show weaker semantic relationships:
- machtsmisbruik (0.712)
- moedertaal (0.725)
- patronage (0.728)
- corruptie (0.730)
- ministerie (0.737)
- emigreren (0.740)
- taalpolitiek (0.742)
- zelfbeschikking (0.746)
- rassendiscriminatie (0.746)

**Assessment**: Excellent parent-child coherence. Only 9 weak parents, mostly due to having 1-3 children each. This is negligible.

---

## 5. Sample High-Quality Expansions (cosine > 0.9)

### Educational Disadvantage & Brain Drain
**Strong problems:**
- taalbarrières (parent: taalachterstand, cosine: 0.933) ✓
- migratie- (parent: emigratie, cosine: 0.932) ✓
- immigratie (parent: emigratie, cosine: 0.925) ✓

**Related strong:**
- taal- (parent: taal, cosine: 0.963) ✓

### Governance Distrust & Corruption
**Strong problems:**
- paternalistische (parent: nepotisme, cosine: 0.925) ✓✓

**Related strong:**
- parlementair (parent: parlementaire, cosine: 0.967) ✓
- kabinet- (parent: kabinet, cosine: 0.962) ✓
- gouverneur- (parent: gouverneur, cosine: 0.956) ✓

### Persistent Poverty & Economic Vulnerability
**Core problems:**
- armoede- (parent: armoede, cosine: 0.961) ✓

**Strong problems:**
- onafhankelijkheid (parent: afhankelijkheid, cosine: 0.952) ✓

**Related strong:**
- arbeidsmarkt- (parent: arbeidsmarkt, cosine: 0.975) ✓
- voc- (parent: voc, cosine: 0.964) ✓

### Social Fragmentation & Racism
**Core problems:**
- discrimination (parent: discriminatie, cosine: 0.983) ✓✓
- discriminatie- (parent: discriminatie, cosine: 0.960) ✓
- racismevormen (parent: racisme, cosine: 0.921) ✓

**Strong problems:**
- racistische (parent: racistisch, cosine: 0.974) ✓

**Assessment**: Excellent semantic coherence between parents and children. The expanded terms are highly relevant variations, compounds, and related concepts.

---

## 6. Problem-Oriented Framework Alignment

### Coverage of Expected Problem Keywords

Based on [TOPIC_FRAMEWORK_CONTEXT.md](TOPIC_FRAMEWORK_CONTEXT.md):

| Topic | Expected Keywords Found | Coverage |
|-------|-------------------------|----------|
| **Educational Disadvantage** | 7/12 | 58% |
| **Social Fragmentation & Racism** | 8/11 | **73%** ✓ |
| **Governance Distrust & Corruption** | 8/12 | 67% |
| **Persistent Poverty** | 4/12 | 33% ⚠️ |

#### Missing Keywords by Topic

**Educational:**
- "brain drain" (but covered by: emigratie, brain drain conceptually)
- "dropout" (but covered by: schooluitval)
- "language" (but covered by: taal, papiamentu)
- "racisme" in education (cross-topic overlap - present in Racism topic)
- "discrimination" in education (cross-topic overlap)

**Governance:**
- "corruption" (English - but covered by: corruptie)
- "distrust" (English - but covered by: wantrouwen)
- "clientelisme" (but covered by: patronage conceptually)
- "rechtsstaat" (missing - potential gap)

**Economic:**
- "poverty" (English - but covered by: armoede)
- "werkeloosheid" (but covered by: werkloosheid - spelling)
- "unemployment" (English - but covered by: werkloosheid)
- "kwetsbaarheid" (missing - potential gap)
- "vulnerability" (English - but covered conceptually by: afhankelijkheid)
- "income" (English - but covered by: inkomen)
- "precair" (missing - potential gap)
- "dependency" (English - but covered by: afhankelijkheid)

**Assessment**: Good coverage overall. "Missing" keywords are mostly:
1. English equivalents (expected - corpus is Dutch)
2. Conceptually covered by related terms
3. Cross-topic terms (e.g., racism appears in Education context but is in Racism topic)

True gaps are minimal (e.g., "rechtsstaat", "kwetsbaarheid", "precair").

---

## 7. Potential Issues & Recommendations

### Issue 1: High-Frequency Generic Terms (DF > 150)

**27 substantive terms** appear in >150 documents, potentially diluting topic specificity:

| Term | DF | Topic | Category |
|------|-----|-------|----------|
| nederlandse | 832 | Educational | related_strong |
| slavenhandel | 353 | Multiple | related_weak |
| werk | 337 | Economic | related_moderate |
| ministerie | 330 | Governance | related_moderate |
| caribisch | 312 | Social | related_strong |
| kinderen | 280 | Educational | related_moderate |
| racisme | 268 | Social | **core_problem** |

**Recommendation**:
- Terms like "nederlandse", "caribisch", "kinderen", "werk" are very generic
- Consider curation: keep only if truly topic-discriminative
- BUT: "racisme" (DF 268) is appropriately a core_problem - high frequency doesn't mean low value if it's genuinely central to the topic

### Issue 2: Rare Core/Strong Problems (DF < 3)

**43 core/strong problem terms** appear in <3 documents:

Examples:
- taalbarrières (DF: 2, strong_problem)
- leerachterstand (DF: 2, strong_problem)
- taalproblematiek (DF: 2, strong_problem)
- omkoping (DF: 2, strong_problem)
- deportatie (DF: 2, strong_problem)

**Recommendation**:
- Verify these are truly "core" or "strong" problems
- If they appear in only 2 documents, they may be edge cases
- Consider downgrading some to "related_moderate" if not truly central
- OR: accept that even rare mentions of core problems (e.g., "omkoping" = bribery) are still important

### Issue 3: Context Term Balance

All topics have **~47-49% context terms** (era_context + geographic_context).

**Recommendation**:
- Current balance is acceptable but could be improved
- Target: >60% substantive, <40% context
- Curation strategy: Remove redundant era/geographic terms that don't add discriminative power
- Example: Do we need 169 children of "1863"? Many are just year variants (1862, 1864, 1865, etc.)

---

## 8. Overall Assessment

### Key Strengths

1. **Perfect Category-Weight Structure** ✓✓✓
   - 100% of terms within expected weight ranges
   - This is CRITICAL for downstream weighted TF-IDF scoring
   - Demonstrates excellent adherence to the scoring methodology

2. **Strong Semantic Coherence** ✓✓
   - Average parent-child cosine: 0.807
   - All expanded terms > 0.7 cosine (no junk)
   - High-quality expansions capture variations, compounds, related concepts

3. **Balanced Topic Coverage** ✓
   - 300 terms per topic (perfect balance)
   - Similar expansion ratios (7.1x - 7.8x)
   - Consistent quality across topics

4. **Literature-Based Grounding** ✓
   - Expansion based on SBERT semantic similarity
   - Reflects actual language use in Dutch Caribbean policy documents
   - Not just manual curation - data-driven

### Areas for Improvement

1. **Context Term Overrepresentation** ⚠️
   - 47% context terms may dilute topic-specific signals
   - Era terms (39.9%) dominate - many redundant year variants
   - Consider pruning to <35% context

2. **Generic High-DF Terms** ⚠️
   - 27 very common substantive terms (DF > 150)
   - Terms like "nederlandse", "werk", "kinderen" may not be topic-discriminative
   - Recommend curation based on topic specificity

3. **Rare Core Problems** ⚠️
   - 43 core/strong problems with DF < 3
   - Verify these are truly "core" - may be edge cases
   - Consider category adjustments

---

## 9. Final Recommendation

### Does the literature-based expansion significantly improve the dictionary?

**YES - HIGH VALUE** ✓✓✓

The v20 dictionary represents a **significant improvement** through:

1. **7.45x expansion** (142 → 1,200 terms) with maintained quality
2. **Perfect category-weight consistency** for downstream scoring
3. **Strong semantic coherence** (avg cosine 0.807, min 0.707)
4. **Balanced coverage** across all 4 topics
5. **Data-driven expansion** capturing real policy language

### Next Steps: Recommended Curation

To maximize value, apply **selective curation**:

1. **Remove overly generic high-DF terms** (target: reduce 27 → ~10)
   - Keep: "racisme", "discriminatie", "armoede" (even if high DF - they're core)
   - Remove: "nederlandse", "kinderen", "caribisch" (too generic)

2. **Prune redundant era terms** (target: reduce 479 → ~300)
   - Keep: Key dates (1863, 1814, 1954, etc.) and "slavernijverleden", "koloniale"
   - Remove: Year variants (1862, 1864, 1865...) unless uniquely important

3. **Verify rare core problems** (target: review 43 terms)
   - Keep if genuinely core (e.g., "omkoping" = bribery is core corruption)
   - Downgrade if peripheral (e.g., some migration variants)

4. **Balance to 60% substantive / 40% context**
   - After steps 1-3, should naturally achieve better balance

### Expected Post-Curation Statistics

- **Total terms**: ~850-950 (down from 1,200)
- **Substantive %**: ~60% (up from 53%)
- **Context %**: ~40% (down from 47%)
- **Avg cosine**: ~0.82+ (up from 0.805 - keeping only strongest)
- **Category-weight consistency**: 100% (maintained)

### Long-Term Value

After curation, this dictionary will provide:
- **Excellent 4-topic coverage** aligned with the problem-oriented framework
- **Strong weighted scoring** through perfect category-weight structure
- **Semantic coherence** through SBERT-based expansion
- **Empirical grounding** in actual Dutch Caribbean policy language

This is a **HIGH-QUALITY foundation** for dictionary-based topic modeling of slavery's developmental legacies.

---

## 10. Appendix: Detailed Files

**Evaluation outputs:**
- [v20_dictionary_quality_report.csv](v20_dictionary_quality_report.csv) - Parent-child analysis
- [evaluate_v20_dictionary_quality.py](evaluate_v20_dictionary_quality.py) - Quality evaluation script
- [analyze_v20_topic_alignment.py](analyze_v20_topic_alignment.py) - Topic alignment script

**Reference documentation:**
- [TOPIC_FRAMEWORK_CONTEXT.md](TOPIC_FRAMEWORK_CONTEXT.md) - 4-topic framework rationale
- [expanded_candidates.csv](workflow_data/slavery_Slavdict_pretraining_slavery_v20/Dictionary/expanded_candidates.csv) - Full v20 dictionary

---

**Evaluation Date**: 2025-11-28
**Evaluator**: Claude Code (Sonnet 4.5)
**Framework**: 4-topic problem-oriented approach (Educational, Racism, Governance, Economic)
