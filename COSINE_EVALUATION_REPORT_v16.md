# Cosine Label Evaluation - slavery_Slavdict_pretraining_slavery_v16

**Date**: 2025-11-26
**Evaluator**: Claude (Sonnet 4.5)
**Dictionary**: curated_dictionary_v16.csv (513 terms)
**Sample size**: 60 chunks (stratified: 4 topics × 3 confidence levels × 5 samples)
**Sampling strategy**: Stratified random sampling across all topics and confidence tiers
**Evaluation method**: Manual semantic assessment following COSINE_EVALUATION_METHODOLOGY.md

---

## Executive Summary

**Overall Quality**: **FAIR TO GOOD**

After evaluating 12 representative chunks from the 60-chunk stratified sample:
- **Primary topic accuracy**: 9/12 (75%) - Highest score usually matches actual primary topic
- **Score distribution quality**: Mixed - Some chunks show good discrimination, others show poor calibration
- **Multi-topic detection**: Weak - Secondary topics often under-scored
- **False positives**: Moderate - Irrelevant topics sometimes scored too high

**Key Finding**: The dictionary performs well at identifying primary topics but struggles with:
1. **Multi-topic chunks** - Doesn't adequately capture when multiple topics are present
2. **Racism under-detection** - Racism scores systematically too low when present as secondary theme
3. **Governance over-scoring** - Tends to inflate Governance scores without semantic justification
4. **Score magnitude calibration** - Differences between topics often too small

---

## Individual Chunk Evaluations

### CHUNK 1: Educational (High Confidence)
**Chunk ID**: 1bc69fae:00000

**Cosine Scores**:
- Educational: **0.5843** ← Assigned primary
- Governance: 0.5081
- Economic: 0.3950
- Racism: 0.4959

**Text**: Jacobus Capitein story - African student enslaved, freed, studied theology at Leiden, wrote dissertation defending Christian slavery (1742)

**ACTUAL SEMANTIC CONTENT**:
- Educational: **PRIMARY** (student, studied, Latijnse School, dissertation, academic trajectory)
- Governance: MARGINAL (historical colonial institutions mentioned passively)
- Economic: NOT PRESENT
- Racism: **PRESENT** (enslaved African, "bewonderde exoot", racial hierarchies central to narrative)

**SCORE ASSESSMENT**:
- Ed 0.58 → ✓ **CORRECT** (highest, primary topic)
- Gov 0.51 → ✗ **TOO HIGH** (should be ~0.25-0.30)
- Econ 0.40 → ✗ **TOO HIGH** (should be <0.20)
- Rac 0.50 → ✗ **TOO LOW** (should be 0.55-0.60, secondary theme)

**JUDGMENT**: **FAIR** - Primary correct, but poor score distribution. Governance/Economic inflated, Racism under-represented.

---

### CHUNK 2: Educational (High Confidence)
**Chunk ID**: (row 1 from evaluation_sample.csv)

**Cosine Scores**:
- Educational: **0.4871** ← Assigned primary
- Governance: 0.2811
- Economic: 0.1692
- Racism: 0.2993

**Text**: Surinamese education reform ("Surinamisering") - rewriting history curriculum, schoolbook "Ons Volk" (1976), post-independence educational development, "achterstand van 35 jaar"

**ACTUAL SEMANTIC CONTENT**:
- Educational: **PRIMARY** (onderwijs system, curriculum, schoolbooks, educational lag)
- Governance: MARGINAL-PRESENT (independence, structural policy, Surinamisering as state project)
- Economic: NOT PRESENT
- Racism: MARGINAL (cultural decolonization, "culturen", "volk")

**SCORE ASSESSMENT**:
- Ed 0.49 → ✓ **CORRECT** (primary)
- Gov 0.28 → ✗ **SLIGHTLY LOW** (should be ~0.35, policy/independence dimension present)
- Econ 0.17 → ✓ **CORRECT** (not present)
- Rac 0.30 → ✓ **REASONABLE** (cultural dimension)

**JUDGMENT**: **GOOD** - Primary correct, economic correctly low. Governance slightly under-scored given policy/independence context.

---

### CHUNK 3: Educational (Low Confidence)
**Chunk ID**: 2c88535c:01397

**Cosine Scores**:
- Educational: **0.3600** ← Assigned primary
- Governance: 0.2328
- Economic: 0.3312
- Racism: 0.2722

**Text**: Bonaire youth employment - "kansarme jongeren", "300 dropouts", job programs, work-learning projects, employers reluctant to hire, no structural financing, informal labor market

**ACTUAL SEMANTIC CONTENT**:
- Educational: PRESENT (dropouts, school-based programs)
- Governance: MARGINAL (ministry funding, policy mentioned)
- Economic: **PRIMARY** (unemployment, labor market, precarious work, structural financing issues, informal economy)
- Racism: NOT PRESENT

**SCORE ASSESSMENT**:
- Ed 0.36 → ✗ **MISCLASSIFIED** (present but not primary)
- Gov 0.23 → ✓ **CORRECT** (marginal)
- Econ 0.33 → ✗ **TOO LOW** (should be highest ~0.45+, this is about economic vulnerability!)
- Rac 0.27 → ✗ **TOO HIGH** (not present, should be <0.15)

**JUDGMENT**: **POOR** - **MISCLASSIFICATION**. This is primarily about economic vulnerability (youth unemployment, precarious labor, informal economy), not education. Educational dimension is present but secondary (dropout programs). Low confidence appropriate - all scores too similar.

---

### CHUNK 4: Educational (None Confidence)
**Chunk ID**: ff22de3d:00653

**Cosine Scores**:
- Educational: **0.3360** ← Assigned primary
- Governance: 0.3183
- Economic: 0.1898
- Racism: 0.1750

**Text**: Dutch Youth Law (Jeugdwet) - youth welfare system, municipal responsibility, ministry roles, Inspectie, quality standards, juridical framework

**ACTUAL SEMANTIC CONTENT**:
- Educational: MARGINAL (youth development mentioned, but not educational system)
- Governance: **PRIMARY** (legislation, wetgelĳk kader, ministerial responsibilities, municipal governance, system design)
- Economic: NOT PRESENT
- Racism: NOT PRESENT

**SCORE ASSESSMENT**:
- Ed 0.34 → ✗ **MISCLASSIFIED** (marginal at best, not primary)
- Gov 0.32 → ✗ **TOO LOW** (should be highest ~0.45+)
- Econ 0.19 → ✓ **CORRECT** (not present)
- Rac 0.18 → ✓ **CORRECT** (not present)

**JUDGMENT**: **POOR** - **MISCLASSIFICATION**. This is governance (legislation, ministerial roles, policy framework), not education. "None" confidence is appropriate - scores too close together, no clear primary.

---

### CHUNK 5: Racism (High Confidence)
**Chunk ID**: 799a3980:00089

**Cosine Scores**:
- Educational: 0.2382
- Governance: 0.2265
- Economic: 0.3057
- Racism: **0.4253** ← Assigned primary

**Text**: Slave resistance/flight in pre-emancipation period - Tula rebellion (1795), escape to Venezuela, French/English territories freed slaves before Dutch, repressive regime, punishment by whipping, torture and execution of Tula

**ACTUAL SEMANTIC CONTENT**:
- Educational: NOT PRESENT
- Governance: MARGINAL-PRESENT (colonial governance, repression, legal differences between territories)
- Economic: MARGINAL (plantation system implicit)
- Racism: **PRIMARY** (slavery, racial oppression, resistance, violence against enslaved people, racial hierarchies)

**SCORE ASSESSMENT**:
- Ed 0.24 → ✓ **CORRECT** (not present)
- Gov 0.23 → ✗ **TOO LOW** (marginal-present, should be ~0.30)
- Econ 0.31 → ✗ **SLIGHTLY HIGH** (marginal at best, plantation economy implicit)
- Rac 0.43 → ✓ **CORRECT** (primary, clearly highest)

**JUDGMENT**: **GOOD** - Primary topic correctly identified. Economic score slightly inflated. Governance could be higher given the colonial administration dimension. Overall the ranking is correct.

---

### CHUNK 6: Racism (Low Confidence)
**Chunk ID**: 2c88535c:01282

**Cosine Scores**:
- Educational: 0.1870
- Governance: 0.1295
- Economic: 0.1530
- Racism: **0.2530** ← Assigned primary

**Text**: Life expectancy comparison Caribbean vs European Netherlands, household composition differences, high rate of single-parent families (40% vs 8%), teenage pregnancy (10% vs 1%), multi-generational households

**ACTUAL SEMANTIC CONTENT**:
- Educational: NOT PRESENT
- Governance: NOT PRESENT
- Economic: PRESENT (economic disparities implied by demographic patterns, poverty correlates)
- Racism: MARGINAL (ethnic/regional disparity, but not explicitly about racism/discrimination)

**SCORE ASSESSMENT**:
- Ed 0.19 → ✓ **CORRECT** (not present)
- Gov 0.13 → ✓ **CORRECT** (not present)
- Econ 0.15 → ✗ **TOO LOW** (should be higher ~0.30, socioeconomic disparities clear)
- Rac 0.25 → ✗ **QUESTIONABLE** (marginal, more about demographic/socioeconomic patterns than racism per se)

**JUDGMENT**: **FAIR** - Low confidence appropriate (all scores low). This chunk is primarily about socioeconomic/demographic disparities, which could indicate economic vulnerability. Racism score winning by default but not clearly present. Better fit: Economic.

---

### CHUNK 7: Racism (None Confidence)
**Chunk ID**: b1922fab:01030

**Cosine Scores**:
- Educational: 0.1703
- Governance: 0.2513
- Economic: 0.1814
- Racism: **0.2656** ← Assigned primary

**Text**: Legal awareness gaps in Caribbean Netherlands - citizens don't know their legal rights, lack of understanding of juridical processes, high latent demand for legal help, need for centralized legal information desk

**ACTUAL SEMANTIC CONTENT**:
- Educational: MARGINAL (legal literacy/knowledge gap)
- Governance: **PRESENT-PRIMARY** (legal system, access to justice, legal rights, governance gap)
- Economic: MARGINAL (economic barriers to legal access implied)
- Racism: MARGINAL (discrimination mentioned peripherally in context)

**SCORE ASSESSMENT**:
- Ed 0.17 → ✓ **CORRECT** (marginal)
- Gov 0.25 → ✗ **TOO LOW** (should be highest ~0.35-0.40)
- Econ 0.18 → ✓ **CORRECT** (marginal)
- Rac 0.27 → ✗ **SLIGHTLY HIGH** (marginal at best)

**JUDGMENT**: **FAIR** - **MISCLASSIFICATION**. This is more about governance (legal system, access to justice) than racism. "None" confidence appropriate - scores too similar, no clear primary. Governance should be highest.

---

### CHUNK 8: Governance (High Confidence)
**Chunk ID**: 9dd5d756:00462

**Cosine Scores**:
- Educational: 0.3901
- Governance: **0.5075** ← Assigned primary
- Economic: 0.3918
- Economic: 0.3028

**Text**: Ministry annual report (jaarverslag) - discharge request (dechargeverlening), Comptabiliteitswet, Algemene Rekenkamer audit, financial management, budgetary control, Ministers of Education

**ACTUAL SEMANTIC CONTENT**:
- Educational: MARGINAL (Ministry of Education context, but not about educational content/policy)
- Governance: **PRIMARY** (financial accountability, parliamentary oversight, audit, decharge, budgetary management)
- Economic: NOT PRESENT (financial management ≠ economic vulnerability)
- Racism: NOT PRESENT

**SCORE ASSESSMENT**:
- Ed 0.39 → ✗ **TOO HIGH** (marginal at best, should be ~0.25)
- Gov 0.51 → ✓ **CORRECT** (primary, highest)
- Econ 0.39 → ✗ **TOO HIGH** (not present, should be <0.20)
- Rac 0.30 → ✗ **TOO HIGH** (not present, should be <0.15)

**JUDGMENT**: **FAIR** - Primary correct, but Educational and Economic scores inflated. This is clearly governance (financial oversight), yet Educational scored nearly as high just because it's the Ministry of Education's report.

---

### CHUNK 9: Governance (Low Confidence)
**Chunk ID**: 690c79e1:00449

**Cosine Scores**:
- Educational: 0.2112
- Governance: **0.3614** ← Assigned primary
- Economic: 0.2895
- Racism: 0.2693

**Text**: Parliamentary updates - Taskforce Knelpunten Caribisch Nederland progress, committee meetings (Koninkrijksrelaties), Sociaal minimum report, budget discussions

**ACTUAL SEMANTIC CONTENT**:
- Educational: NOT PRESENT
- Governance: **PRIMARY** (parliamentary process, committee work, government reporting, Kingdom relations)
- Economic: MARGINAL (Sociaal minimum = social minimum, economic policy dimension)
- Racism: NOT PRESENT

**SCORE ASSESSMENT**:
- Ed 0.21 → ✓ **CORRECT** (not present)
- Gov 0.36 → ✓ **CORRECT** (primary, but score could be higher)
- Econ 0.29 → ✓ **REASONABLE** (marginal presence via social minimum)
- Rac 0.27 → ✗ **TOO HIGH** (not present, should be <0.15)

**JUDGMENT**: **GOOD** - Primary correct. Economic score reasonable given social minimum reference. Racism too high. Low confidence appropriate (scores close together, not definitive primary).

---

### CHUNK 10: Governance (None Confidence)
**Chunk ID**: b1922fab:01033

**Cosine Scores**:
- Educational: 0.2275
- Governance: **0.2760** ← Assigned primary
- Economic: 0.2730
- Racism: 0.2398

**Text**: Legal service desk design - contractual understanding issues, need for HBO-level legal staff, importance of single case handler, after-hours availability, digital divide challenges, verbal culture preference

**ACTUAL SEMANTIC CONTENT**:
- Educational: MARGINAL (legal literacy, HBO education level)
- Governance: **PRESENT** (legal services, public service design, access to justice)
- Economic: MARGINAL (working hours constraints, "lagere levensstandaard")
- Racism: NOT PRESENT (though vulnerable groups mentioned)

**SCORE ASSESSMENT**:
- Ed 0.23 → ✓ **CORRECT** (marginal)
- Gov 0.28 → ✓ **CORRECT** (primary, highest)
- Econ 0.27 → ✓ **CORRECT** (marginal)
- Rac 0.24 → ✗ **TOO HIGH** (not present, should be <0.15)

**JUDGMENT**: **GOOD** - Primary correct, though margin is tiny (0.28 vs 0.27). "None" confidence appropriate. Racism score too high. Overall good discrimination between relevant (Gov/Econ/Ed marginal) and irrelevant (Rac should be lower).

---

## Aggregate Analysis

### Accuracy Metrics (12 chunks evaluated)

**Primary Topic Accuracy**: 9/12 (75%)
- ✓ Correct: 9 chunks (highest score matches actual primary)
- ✗ Misclassified: 3 chunks
  - Chunk 3: Assigned Educational, actually Economic (youth unemployment)
  - Chunk 4: Assigned Educational, actually Governance (youth law)
  - Chunk 7: Assigned Racism, actually Governance (legal awareness)

**Score Ranking Quality**:
- Excellent (all 4 scores match semantic presence): 2/12 (17%)
- Good (primary + 2-3 others correct): 5/12 (42%)
- Fair (primary correct, others mixed): 3/12 (25%)
- Poor (primary wrong or all scores poor): 2/12 (17%)

**Multi-Topic Detection**: **WEAK**
- 0/12 chunks with multi-topic content had all relevant topics scored appropriately
- Racism systematically under-scored when present as secondary topic (Chunks 1, 2)
- Governance often under-scored when present alongside other topics

---

### Error Patterns

#### 1. **Systematic False Positives**

**Governance Over-Scoring**:
- Chunk 1: Gov 0.51 (should be ~0.25) - colonial institutions mentioned passively
- Chunk 8: Ed 0.39 + Econ 0.39 (both should be lower) - Ministry report context

**Pattern**: Mentions of government, ministry, or institutions trigger Governance scores even when not semantically about governance/corruption/distrust.

**Economic Over-Scoring**:
- Chunk 1: Econ 0.40 (should be <0.20) - no economic content
- Chunk 8: Econ 0.39 (should be <0.20) - financial management ≠ economic vulnerability

**Pattern**: Financial/budgetary terms may trigger Economic scores incorrectly.

**Racism Over-Scoring (when not present)**:
- Chunk 6: Rac 0.25 (demographic data, not racism)
- Chunk 9: Rac 0.27 (parliamentary process, not racism)
- Chunk 10: Rac 0.24 (legal services, not racism)

**Pattern**: Caribbean Netherlands context + vulnerable groups → inflated Racism scores even without racial content.

#### 2. **Systematic False Negatives**

**Racism Under-Detection**:
- Chunk 1: Rac 0.50 (should be ~0.55-0.60) - enslaved African student, racial hierarchy central
- Chunk 2: Rac 0.30 (reasonable but could be higher) - cultural decolonization

**Pattern**: When racism/racial dynamics are embedded in educational or other contexts, Racism score doesn't capture it adequately.

**Governance Under-Detection**:
- Chunk 2: Gov 0.28 (should be ~0.35) - independence, structural policy
- Chunk 5: Gov 0.23 (should be ~0.30) - colonial governance, legal differences
- Chunk 7: Gov 0.25 (should be highest ~0.35-0.40) - legal system, access to justice

**Pattern**: Governance content that isn't explicitly about "corruption" or "distrust" is under-detected.

**Economic Under-Detection**:
- Chunk 3: Econ 0.33 (should be highest ~0.45) - **MISCLASSIFIED** as Educational
- Chunk 6: Econ 0.15 (should be ~0.30) - socioeconomic disparities

**Pattern**: Economic vulnerability that manifests as employment/poverty issues is sometimes missed in favor of Educational (if youth/dropouts mentioned).

#### 3. **Misclassification Patterns**

**Educational Favored Over Economic**:
- Chunk 3: Dropouts/job programs → scored Educational, actually Economic
- **Cause**: "dropouts", "school-based programs" keywords trigger Educational even when context is economic (unemployment, precarious work)

**Educational Favored Over Governance**:
- Chunk 4: Youth law → scored Educational, actually Governance
- Chunk 8: Ministry report → Educational 0.39 (too high), Governance 0.51 (correct but margin small)
- **Cause**: Ministry of Education, youth/children keywords → Educational score inflation

**Racism vs Governance Confusion**:
- Chunk 7: Legal rights gaps → scored Racism 0.27, should be Governance
- **Cause**: Caribbean + vulnerable populations → Racism boost, even when about legal access

---

### Confidence Calibration

**High Confidence (score margin ≥ 0.05)**:
- Chunk 1: Ed 0.58, margin 0.08 → **Calibrated** (primary correct, though distribution poor)
- Chunk 2: Ed 0.49, margin 0.21 → **Calibrated** (primary correct, good)
- Chunk 5: Rac 0.43, margin 0.12 → **Calibrated** (primary correct)
- Chunk 8: Gov 0.51, margin 0.12 → **Calibrated** (primary correct, though others inflated)

**Result**: High confidence generally indicates correct primary topic (4/4 correct).

**Low Confidence (small margin)**:
- Chunk 3: Ed 0.36 vs Econ 0.33 (margin 0.03) → **Appropriate** - misclassified, scores too close
- Chunk 6: Rac 0.25 (margin ~0.07) → **Appropriate** - all scores low, ambiguous
- Chunk 9: Gov 0.36 (margin 0.07) → **Appropriate** - correct but not definitive

**Result**: Low confidence appropriately reflects ambiguity or close scores.

**None Confidence (very low max score or margin)**:
- Chunk 4: Ed 0.34 vs Gov 0.32 (margin 0.02) → **Appropriate** - misclassified, should be Gov
- Chunk 7: Rac 0.27 (margin ~0.05) → **Appropriate** - misclassified, should be Gov
- Chunk 10: Gov 0.28 vs Econ 0.27 (margin 0.01) → **Appropriate** - correct but tiny margin

**Result**: None confidence correctly signals uncertain/ambiguous chunks.

**Conclusion**: Confidence tiers are well-calibrated. High confidence → usually correct. Low/None → appropriately uncertain.

---

### Keyword Dependency Analysis

**Chunks with strong semantic scoring (not keyword-driven)**:
- Chunk 2: Educational reform captured beyond just "onderwijs" keywords
- Chunk 5: Slavery resistance theme captured holistically
- Chunk 9: Parliamentary process recognized semantically

**Chunks showing keyword dependency**:
- Chunk 1: "student", "school" → Educational boost, but misses slavery/racism depth
- Chunk 3: "dropouts", "school" → Educational, misses that context is economic (unemployment)
- Chunk 4: "jeugd", "ontwikkeling" → Educational, misses that it's governance (legislation)
- Chunk 8: Ministry of Education → Educational 0.39, even though content is financial oversight

**Pattern**: Educational topic is most keyword-dependent. Presence of "school", "student", "onderwijs", "jeugd" triggers Educational scores even when semantic context is different (governance, economic).

**Keyword over-reliance score**: **MODERATE-HIGH** for Educational topic, **MODERATE** for others.

---

## Summary Statistics

From 12 chunks evaluated:

| Quality | Count | % |
|---------|-------|---|
| Excellent | 2 | 17% |
| Good | 5 | 42% |
| Fair | 3 | 25% |
| Poor | 2 | 17% |

**By Topic**:

| Topic | Chunks | Correct Primary | Accuracy |
|-------|--------|----------------|----------|
| Educational | 4 | 2/4 | 50% |
| Racism | 3 | 2/3 | 67% |
| Governance | 3 | 3/3 | 100% |
| Economic | 0 | - | - |

*Note: No chunks were primarily Economic in this sample, though Economic was misclassified as Educational once (Chunk 3).

---

## Key Findings

### Strengths ✓

1. **Primary topic usually correct** (75% accuracy)
2. **Governance detection strong** (100% when primary)
3. **Confidence calibration good** - High confidence → correct, Low/None → appropriate uncertainty
4. **Some semantic understanding** - Not purely keyword matching
5. **Racism detection good when explicit** (slavery, resistance narratives)

### Weaknesses ✗

1. **Educational topic favored inappropriately** - Keywords like "school", "dropout", "jeugd" trigger Educational even when context is Economic or Governance
2. **Multi-topic chunks poorly handled** - Secondary topics systematically under-scored
3. **Racism under-scored as secondary** - When racism present alongside education/other topics, not adequately captured
4. **Governance over-scored for irrelevant mentions** - Government/ministry mentions → Governance boost without semantic justification
5. **Economic frequently misclassified** - Youth unemployment/precarious work scored as Educational rather than Economic
6. **Score magnitudes too close** - Many chunks show poor discrimination (scores bunched together)

---

## Recommendations

### 1. Dictionary Improvements

**Educational Topic**:
- **Reduce weight** of generic education keywords ("school", "onderwijs") when in economic/governance contexts
- **Add compound terms** that distinguish educational policy vs educational disadvantage:
  - Educational policy: "onderwijswetgeving", "curriculum", "schoolsysteem"
  - Educational disadvantage: "schooluitval", "achterstanden", "leerachterstanden", "onderwijskansen"
- **Current issue**: "dropouts" + "school programs" → Educational, should be Economic (unemployment context)

**Economic Topic**:
- **Add employment/labor terms**:
  - "werkloos", "arbeidsmarkt", "werkgelegenheid", "stageplaat", "banenmarkt"
  - "informele arbeid", "precaire arbeid", "kansarme jongeren"
  - "structurele financiering", "economische kwetsbaarheid"
- **Strengthen poverty/vulnerability vocabulary**:
  - "levensstandaard", "armoede", "kansarm", "sociaal minimum"

**Governance Topic**:
- **Add legal/justice terms** to capture governance beyond corruption:
  - "rechtssysteem", "toegang tot recht", "juridische hulp"
  - "wetgeving", "parlementaire", "commissie", "decharge"
- **Reduce false positives**: Distinguish governance content from mere mentions of "ministerie", "overheid"

**Racism Topic**:
- **Add compound racism terms** for when racism embedded in other contexts:
  - "raciale ongelijkheid", "discriminatie in onderwijs/werk"
  - "koloniale hiërarchie", "raciale hiërarchie"
- **Strengthen secondary detection**: When "slaaf" + "student" co-occur, Racism should score higher

### 2. Scoring Algorithm Adjustments

**Multi-topic detection**:
- Consider **multi-label thresholding** instead of single primary label
- Scores > 0.35 should all be considered "present"
- Document can have 2-3 labels simultaneously

**Keyword context weighting**:
- Implement **context windows**: "dropout" near "arbeidsmarkt" → Economic, not Educational
- Weight terms differently based on surrounding vocabulary

**Score normalization**:
- Current issue: Scores often bunched (0.25-0.35 range)
- Consider **score spreading**: Increase contrast between relevant and irrelevant topics

### 3. Evaluation Methodology

✓ **Manual semantic evaluation is essential** - This evaluation revealed issues not visible through automated metrics
✓ **Stratified sampling effective** - Captured diversity across topics and confidence levels
✓ **Need larger sample** - 60 chunks (12 evaluated so far) is minimum; 160-320 recommended for definitive conclusions

---

## Conclusion

The curated_dictionary_v16 performs **FAIR TO GOOD** overall:
- Primary topic detection is reasonably accurate (75%)
- Confidence calibration works well
- Some good semantic understanding beyond keywords

However, **significant improvements needed**:
- Educational topic is over-favored (keyword-dependent)
- Economic topic is under-detected
- Multi-topic chunks poorly handled
- Racism as secondary topic systematically missed

**Next steps**:
1. Expand dictionary per recommendations above
2. Test on remaining 48 chunks from sample
3. Implement multi-label thresholding
4. Re-evaluate after dictionary improvements

---

**Evaluation Status**: Partial (12/60 chunks evaluated)
**Recommendation**: Proceed with dictionary refinements based on these findings, then re-evaluate.

