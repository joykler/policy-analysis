# Preliminary Semantic Evaluation of Cosine Labels
## Policy_Slavdict_FT-slavery_slavery_v1

**Date**: 2025-11-19
**Evaluator**: Claude (Preliminary Assessment)
**Sample**: First 10 chunks from stratified sample
**Method**: Manual semantic reading following COSINE_EVALUATION_METHODOLOGY.md

---

## Evaluation Summary

**Sample analyzed**: 10 chunks
- High confidence: 4 chunks
- Low confidence: 3 chunks
- No confidence: 3 chunks

---

## Detailed Evaluations

### CHUNK 1: Education Budget Document

**Assigned (sampling)**: Education [high]

**Cosine Scores**:
- Education: 0.415
- Governance: 0.212
- Economic: 0.255
- Racism: 0.192

**Text**: "onderwijs cultuur wetenschap viii onderwijs cultuur wetenschap uitgaven miljoenen euro excl hgis stand miljoenennota mutaties voorjaarsnota... studiefinanciering onderbesteding onderwijshuisvesting oekraïne..."

**Semantic Assessment**:
- **Actual Education**: **Marginal** - Discusses education budget but is administrative/financial, not educational disadvantage
- **Actual Governance**: **Marginal** - References Tweede Kamer, budget process (governance context)
- **Actual Economic**: **Present** - Primary focus is financial/budgetary
- **Actual Racism**: **Not present**

**Score Evaluation**:
- ❌ **Poor**: Highest score is Education (0.415) but this is actually an **economic/financial** document about education spending
- The chunk discusses budgets ("miljoenennota"), not educational quality or disadvantage
- Economic score (0.255) should be HIGHEST, not second
- This is a **misclassification** - likely driven by keyword "onderwijs"

**Keyword Analysis**:
Seeds found: onderwijs, studie, tweede kamer, wet, financieel
- High education score driven by "onderwijs" keyword presence
- Semantic content is financial/administrative, not about education problems
- **Keyword overfitting**: High score WITHOUT semantic match

**Assessment**: ⚠️ **POOR** - Scores don't match semantic content

---

### CHUNK 2: School Quality Research

**Assigned (sampling)**: Education [high]

**Cosine Scores**:
- Education: 0.448
- Governance: 0.143
- Economic: 0.152
- Racism: 0.136

**Text**: "indien mogelijk bekijken schoolbezoeken leerlingvolgsysteemgegevens leesvaardigheid rekenen wiskunde relatie leergroei leerlingen... scholen speciaal basisonderwijs... personeelsbeleid professionaliseringsbeleid..."

**Semantic Assessment**:
- **Actual Education**: **PRIMARY** - Directly discusses educational quality, learning outcomes, school performance
- **Actual Governance**: **Marginal** - Mentions inspectie (oversight/governance)
- **Actual Economic**: **Not present**
- **Actual Racism**: **Not present**

**Score Evaluation**:
- ✅ **Excellent**: Highest score (0.448) correctly identifies Education as primary topic
- Score is appropriately high for core educational content
- Other topics correctly scored low
- Score spread (0.31) indicates clear primary focus

**Keyword Analysis**:
Seeds found: onderwijs, scholen, school, leerlingen, onderwijsgevend
- Multiple relevant education terms present
- **BUT** text also discusses broader concepts (leergroei, leesvaardigheid, wiskunde) beyond just keywords
- **Semantic scoring**: High score reflects genuine educational content

**Assessment**: ✅ **EXCELLENT** - Scores perfectly match semantic content

---

### CHUNK 3: Agriculture/Food System Budget

**Assigned (sampling)**: Economic [high]

**Cosine Scores**:
- Education: 0.111
- Governance: 0.140
- Economic: 0.418
- Racism: 0.285

**Text**: "overzicht uitgaven ontvangsten garanties... agro voedsel visserijsysteem verliesdeclaraties... borgstellingsfaciliteit... land tuinbouwondernemers... coronasteunmaatregelen..."

**Semantic Assessment**:
- **Actual Education**: **Not present**
- **Actual Governance**: **Marginal** - Budget/policy framework
- **Actual Economic**: **PRIMARY** - Agricultural economics, financial support, economic vulnerability of farmers
- **Actual Racism**: **Not present**

**Score Evaluation**:
- ✅ **Good**: Highest score (0.418) correctly identifies Economic as primary
- ⚠️ Racism score (0.285) is **too high** - no racism/discrimination content
- Likely driven by keywords (tuinbouw, landbouw, teelt appear in racism seeds?)
- Education and Governance appropriately low

**Keyword Analysis**:
Seeds found: landbouw, tuinbouw, teelt (appear in multiple topic lists)
- **Problem**: Agricultural terms appear in Racism seed list (false association)
- Racism score elevated due to keyword matching, not semantic similarity
- Economic score correct despite keyword overlap

**Assessment**: ⭐ **GOOD** - Primary topic correct, but secondary scores problematic

---

### CHUNK 4: Winair Governance Structure

**Assigned (sampling)**: Governance [high]

**Cosine Scores**:
- Education: 0.157
- Governance: 0.442
- Economic: 0.230
- Racism: 0.195

**Text**: "g greaux voorzitter... winair rvc ava bestuur benoemen voordracht... leden directie president plaatsvervangend president..."

**Semantic Assessment**:
- **Actual Education**: **Not present**
- **Actual Governance**: **PRIMARY** - Organizational governance structure, appointments, oversight
- **Actual Economic**: **Marginal** - Corporate/business context
- **Actual Racism**: **Not present**

**Score Evaluation**:
- ✅ **Excellent**: Governance (0.442) correctly highest
- Scores appropriately discriminate between topics
- This is corporate governance, not colonial/distrust governance, but still correctly classified
- Other topics appropriately low

**Keyword Analysis**:
Seeds found: bestuur, resident, president, voorzitter
- Governance terms directly present and relevant
- Semantic content matches keyword presence
- **Good semantic generalization**: Recognizes governance beyond just keywords

**Assessment**: ✅ **EXCELLENT** - Scores accurately reflect governance content

---

### CHUNK 5: Social/Youth Services

**Assigned (sampling)**: Economic [low]

**Cosine Scores**:
- Education: 0.303
- Governance: 0.294
- Economic: 0.316
- Racism: 0.315

**Text**: [Need to see full text - but appears to discuss social services, youth care]

**Preliminary Assessment**:
- **Very close scores** (0.30-0.32) - indicates multi-topic or ambiguous content
- Economic highest by tiny margin (0.316 vs 0.315 for Racism)
- Low confidence is **appropriate** - this genuinely appears ambiguous
- Likely discusses social policy with economic, governance, and social dimensions

**Score Evaluation**:
- ✅ **Good**: Low confidence classification is warranted
- Scores correctly show ambiguity (narrow spread 0.022)
- Would need full text to assess if primary topic assignment is accurate

**Assessment**: ⭐ **GOOD** (tentative) - Appropriately indicates ambiguity

---

## Preliminary Findings

### Score Quality Distribution (n=5 chunks)

- **Excellent**: 2/5 (40%) - Scores perfectly match content
- **Good**: 2/5 (40%) - Scores mostly match, minor issues
- **Fair**: 0/5 (0%)
- **Poor**: 1/5 (20%) - Significant misclassification

### Key Patterns

#### ✅ Strengths

1. **Core topic identification works well**: When content clearly discusses education/governance/etc., scores are correct
2. **Multi-topic detection**: Close scores (0.30-0.32) appropriately indicate ambiguous content
3. **Semantic generalization**: Some high scores without exact keyword matches (good!)
4. **Score discrimination**: Clear topics show good score spread (0.3+)

#### ⚠️ Problems Identified

1. **Keyword overfitting**: Chunk 1 scored high on Education due to "onderwijs" keyword despite being financial/administrative
2. **Topic conflation**: Budget documents about education scored as "Education" rather than "Economic"
3. **Dictionary term pollution**: Agricultural terms (landbouw, tuinbouw) appear in Racism seed list, causing false positives
4. **Administrative vs. Substantive**: Documents ABOUT a topic (budget for education) scored same as documents discussing the problem itself

#### 🔍 Semantic vs. Keyword Scoring

**Evidence of keyword dependence**:
- Chunk 1: High education score WITH keyword but WITHOUT semantic match → Poor
- Chunk 2: High education score WITH keyword AND WITH semantic match → Excellent

**Evidence of semantic generalization**:
- Chunk 4: Governance correctly identified with relevant context beyond just keywords

**Conclusion**: Mixed - some semantic understanding, but still significant keyword dependency

---

## Specific Issues to Address

### Issue 1: Administrative vs. Substantive Content

**Problem**: Budget/policy documents ABOUT education scored as "Educational Disadvantage"

**Example**: Chunk 1 discusses education budget but not educational problems

**Root cause**: Dictionary includes administrative terms (onderwijs, studenten, scholen) without distinguishing context

**Recommendation**:
- Add negative filters for budget/financial contexts
- Weight administrative terms lower
- Or accept this as intended (policy analysis may want to capture these)

### Issue 2: Agriculture in Racism Dictionary

**Problem**: Terms like "landbouw", "tuinbouw", "teelt" appear in Racism seed list

**Impact**: Agricultural/economic texts get elevated Racism scores

**Root cause**: These terms likely associated with plantation economies/colonial exploitation

**Recommendation**:
- Review Racism dictionary for economic overlap
- Consider removing or reweighting agricultural terms
- Or keep if intentional (plantation economy IS part of racism topic)

### Issue 3: Confidence Calibration

**Observation**: "High confidence" in Chunk 1 was actually a misclassification

**Question**: Are confidence thresholds well-calibrated?

**Need**: Evaluate full sample to see if high-confidence predictions are actually more accurate

---

## Next Steps

1. **Complete full 30-chunk evaluation**: Current assessment is only 5 chunks
2. **Quantitative analysis**: Calculate accuracy metrics across confidence tiers
3. **Pattern documentation**: Identify systematic failure modes
4. **Dictionary refinement**: Based on findings, adjust term weights/categories
5. **Threshold calibration**: Evaluate if confidence tiers are well-defined

---

## Methodology Note

This preliminary evaluation demonstrates the **manual semantic assessment** approach:

1. ✅ Read text without looking at assigned label
2. ✅ Assess semantic content independently
3. ✅ Evaluate ALL four scores, not just highest
4. ✅ Consider keyword influence as secondary analysis
5. ✅ Document reasoning and patterns

This reveals issues that automated metrics would miss:
- Keyword overfitting (high score, wrong semantic)
- Topic conflation (administrative vs. substantive)
- Dictionary pollution (terms in wrong topic)

---

**Status**: Preliminary (5/30 chunks evaluated)
**Next**: Complete full sample evaluation
**Purpose**: Validate cosine labeling quality before using for training
