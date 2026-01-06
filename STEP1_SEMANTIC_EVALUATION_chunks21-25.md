# STEP 1: SEMANTIC EVALUATION - CHUNKS 21-25 (NOISE TIER)
**Sample Type:** Noise Tier (cosine <0.25) - Lowest quality/most ambiguous
**Date:** 2025-12-03
**Expected:** High disagreement rate, very weak topic signals

---

## CHUNK 21: 71e10718:00725 - "SDG reporting methodology for development aid"

**Text summary:** Technical document about reporting methods for Sustainable Development Goals (SDGs) - 2030 horizon, measurement periods (2017-2020, 2021-2025, 2026-2030), indicator targets, annual reporting procedures, online results platform, budget documentation methodology, threshold rules for reporting deviations.

**Semantic Ratings:**

| Topic | Rating | Brief Rationale |
|-------|--------|----------------|
| Educational | 0/3 | Not discussed |
| Governance | 1/3 | **Weakly**: reporting procedures, budget documentation, government methodology - but this is TECHNICAL/ADMINISTRATIVE, not governance problems |
| Poverty | 1/3 | **Weakly**: context is development aid (poverty alleviation) but text is about REPORTING METHODOLOGY, not poverty itself |
| Racism | 0/3 | Not discussed |

**Primary topic:** NONE - Technical documentation, no clear topic fit
**Multi-topic?** No
**Slavery legacy:** None
**Difficulty:** 1 (Easy to read, but NOT RELEVANT to any topic)

**NOTE:** Cosine=Governance (0.21), BERTJE=Poverty (0.22) - **BOTH WRONG**, this shouldn't match any topic strongly

---

## CHUNK 22: ff22de3d:00663 - "COVID-19 financial accountability issues"

**Text summary:** Discusses COVID-19 subsidy accountability problems 2022-2023: LCCB annual report issues (€546M uncertainty), GGD extra costs (€511M uncertainty due to incorrect materiality thresholds), IC capacity subsidy problems (€382M uncertainty over FTE claims), accountant verification challenges.

**Semantic Ratings:**

| Topic | Rating | Brief Rationale |
|-------|--------|----------------|
| Educational | 0/3 | Not discussed |
| Governance | 2/3 | **Moderately present**: government financial oversight, accountability systems ("verantwoording"), control protocols, subsidy management - but focus is COVID-19 FINANCIAL ADMINISTRATION, not governance distrust/corruption |
| Poverty | 1/3 | **Weakly**: large sums of money (€546M, €511M) but about accounting, not economic vulnerability |
| Racism | 0/3 | Not discussed |

**Primary topic:** Governance (2/3) - but weak, technical financial administration
**Multi-topic?** No
**Slavery legacy:** None (COVID-19 financial management)
**Difficulty:** 2 (Medium - governance-adjacent but not core topic)

**NOTE:** Cosine=Governance (0.22), BERTJE=Poverty (0.21) - **DISAGREE**, Cosine marginally better

---

## CHUNK 23: 8e118753:00356 - "Comparing slave ships vs contract labor ships"

**Text summary:** Historical comparison of mortality on slave ships (50.9 deaths/1000/month, 1680-1807) vs Indian/Javanese contract labor ships post-1873 (7.1 deaths/1000/month). Describes British-Indian regulations improving conditions, better food/medicine, investigations into deaths, arrival health differences, plantation conditions post-slavery.

**Semantic Ratings:**

| Topic | Rating | Brief Rationale |
|-------|--------|----------------|
| Educational | 0/3 | Not discussed |
| Governance | 1/3 | **Weakly**: British-Indian regulations, government oversight, investigations |
| Poverty | 2/3 | **Moderately present**: economic conditions, labor systems, food provision, plantation economics, comparison of slavery vs contract labor as ECONOMIC SYSTEMS |
| Racism | 3/3 | **CENTRAL**: racial labor exploitation systems, comparison of enslaved Africans vs Asian contract workers, "epidemiologisch slachtveld", death rates by racial group, systemic dehumanization, though text notes improvements, core is RACIAL LABOR SYSTEMS |

**Primary topic:** Racism (3/3), secondary Poverty (2/3)
**Multi-topic?** Yes
**Slavery legacy:** Explicit (slavery vs post-slavery labor)
**Difficulty:** 2 (Medium - comparative historical analysis)

**NOTE:** Both predict Poverty - **BOTH PARTIALLY WRONG**, should be Racism primary

---

## CHUNK 24: 2c88535c:01409 - "Caribbean Netherlands policy complaints"

**Text summary:** Caribbean residents' complaints about Dutch policy post-2010 transition - lack of subsidies (housing, child benefits), no public transport between islands, immigration hassles, wrong investment priorities (nature/prisons vs poverty), cultural misunderstanding, imposed Dutch laws (euthanasia, gay marriage, abortion), tax collection, pension age increases, healthcare cuts.

**Semantic Ratings:**

| Topic | Rating | Brief Rationale |
|-------|--------|----------------|
| Educational | 0/3 | Not discussed |
| Governance | 3/3 | **CENTRAL**: policy complaints, Dutch government control, cultural imposition ("Nederland begrijpt de cultuur niet"), inappropriate laws, governance failures, "verkeerde keuzes", lack of local autonomy, policy-population disconnect |
| Poverty | 2/3 | **Moderately present**: lack of subsidies, high costs, unemployment, "armoedebestrijding", economic complaints about priorities |
| Racism | 1/3 | **Weakly**: implicit colonial attitude ("Nederland maakt de verkeerde keuzes"), cultural domination, but not explicitly racial |

**Primary topic:** Governance (3/3), secondary Poverty (2/3)
**Multi-topic?** Yes
**Slavery legacy:** Implicit (colonial governance legacy)
**Difficulty:** 2 (Medium - governance-poverty overlap)

**NOTE:** Cosine=Governance (0.25), BERTJE=Poverty (0.47) - **DISAGREE**, Cosine correct

---

## CHUNK 25: b2d7b49f:01739 - "20th century genocides catalog"

**Text summary:** Lists historical genocides - Australia indigenous (250K-750K → 31K by 1911), Namibia Herero/Nama (1904-1907, 80K → 15K), Armenian genocide (1-1.5M deaths, 1915-1923), 20th century genocides (Soviet Union, China, Nazi Europe, Guatemala Maya, Cambodia, Yugoslavia, etc.). Discusses genocide as "extreme form of reshaping humanity", US role in 20th century.

**Semantic Ratings:**

| Topic | Rating | Brief Rationale |
|-------|--------|----------------|
| Educational | 0/3 | Not discussed |
| Governance | 1/3 | **Weakly**: government perpetrated genocides, but focus is MASS ATROCITY, not governance systems |
| Poverty | 0/3 | Not discussed |
| Racism | 2/3 | **Moderately present**: racial/ethnic extermination (indigenous peoples, Armenians, Maya, etc.), "misdaden tegen de menselijkheid", genocide based on group identity - BUT this is CATALOG/LIST, not analysis of racism |

**Primary topic:** Racism (2/3) - but weak, historical catalog
**Multi-topic?** No (only Racism weakly present)
**Slavery legacy:** Tangential (mentions indigenous genocides, colonial context)
**Difficulty:** 2 (Medium - historical catalog, not deep analysis)

**NOTE:** Both predict Racism - **BOTH CORRECT** (best fit despite weak signal)

---

## SUMMARY: CHUNKS 21-25 (NOISE TIER)

### Disagreements:
- **Chunk 21:** Cosine=Governance (0.21), BERTJE=Poverty (0.22) → **BOTH WRONG** (technical doc, no topic)
- **Chunk 22:** Cosine=Governance (0.22), BERTJE=Poverty (0.21) → Cosine marginally better
- **Chunk 23:** Both=Poverty → **BOTH WRONG** (should be Racism primary)
- **Chunk 24:** Cosine=Governance ✅, BERTJE=Poverty ❌
- **Chunk 25:** Both=Racism ✅

### Key Observations:

1. **Very low scores = very weak content**
   - Chunk 21: Technical methodology (no real topic)
   - Chunks 22-25: Marginal relevance to topics

2. **Both methods struggle with noise**
   - Chunk 21: Neither should predict any topic strongly
   - Chunk 23: Both missed Racism, picked Poverty

3. **Cosine slightly better in noise tier**: 2 correct vs BERTJE 1 correct (excluding ties)

4. **Governance finally appears as primary!**
   - Chunk 24: First time in 25 chunks Governance is primary (3/3)
   - But only at cosine score 0.25 (noise tier)

5. **Score threshold insight:**
   - Cosine <0.25 = genuinely weak/irrelevant content
   - Both methods should probably use 0.25 as minimum threshold

---

## FINAL STATISTICS (All 25 Chunks)

### Topic Distribution:
- **Educational:** 7/25 primary (28%)
- **Racism:** 8/25 primary (32%) [including chunk 23]
- **Poverty:** 5/25 primary (20%)
- **Governance:** 1/25 primary (4%) - chunk 24 only!

### Agreement Rate by Tier:
| Tier | Agreement | Disagreements |
|------|-----------|---------------|
| Core (≥1.5) | 5/5 (100%) | 0 |
| Moderate (1.0-1.5) | 5/5 (100%) | 0 |
| Weak (0.5-1.0) | 3/5 (60%) | 2 |
| Context (0.25-0.5) | 3/5 (60%) | 2 |
| Noise (<0.25) | 2/5 (40%) | 3 |
| **TOTAL** | **18/25 (72%)** | **7 disagreements** |

**Pattern confirmed:** Lower cosine scores = more disagreements = genuinely ambiguous/weak content
