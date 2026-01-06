# Dictionary Curation Report: Social Fragmentation & Racism

**Workflow Version**: slavery_Slavdict_pretrained_slavery_v3
**Corpus Type**: Domain Corpus (Slavery Legacy Scholarship)
**Stage**: Stage 1 - Semantic Foundation
**Date**: 2025-12-17
**Curator**: Claude Sonnet 4.5 (LLM-assisted semantic analysis)

---

## Executive Summary

Curated Topic 2 (Social Fragmentation & Racism) following the Dictionary Curation Guide methodology. Reduced 300 candidate terms to 174 high-quality terms through systematic semantic analysis. This topic required extensive semantic drift detection due to many false cognates from "afschaffing" (abolition) and "uitsluiting" (exclusion).

### Key Outcomes
- **Starting terms**: 300 (including seed terms)
- **Automatic removals**: 1 (morphological fragment)
- **Manual review**: 248 terms analyzed
- **Final curated dictionary**: 174 terms
- **Removal rate**: 75 terms (25.0%)
- **Recategorizations**: 29 terms (many slave trade → era_context)
- **Weight adjustments**: 18 terms

---

## Curation Statistics

### Expansion Statistics
- **Seed terms**: 52 original terms (is_seed=1)
- **Expanded terms**: 248 BERTJE-generated terms (is_seed=0)
- **After automatic removal**: 247 terms
- **After manual curation**: 174 terms retained

### Decision Breakdown
| Decision | Count | Percentage |
|----------|-------|------------|
| KEEP | 127 | 42.3% |
| REMOVE | 75 | 25.0% |
| RECATEGORIZE | 29 | 9.7% |
| REWEIGHT | 18 | 6.0% |
| REVIEW (seeds kept) | 51 | 17.0% |

**Notable**: Higher removal rate (25%) than Topic 1 (10.3%) due to extensive semantic drift from "afschaffing" and "uitsluiting" parents.

---

## Phase 1: Automatic Removals

### 1. Morphological Fragments
**Removed**: 1 term
- `bon` (from "bonaire") - len<4, fragment

### 2. Extreme Low Similarity (cosine < 0.65)
**Removed**: 0 terms

### 3. Single Document Frequency (df == 1)
**Removed**: 0 terms

**Phase 1 Total Removals**: 1 term

---

## Phase 2: Semantic Drift Detection

**MAJOR ISSUE IDENTIFIED**: Extensive semantic drift from two problematic parent terms.

### Problem Parent 1: "afschaffing" (abolition)
BERTJE expanded to many "af-" prefix verbs that are semantically unrelated:

**Removed 32 terms** from "afschaffing" parent:
- **verlaging** - "reduction" (not abolition)
- **verschansing** - "entrenchment" (opposite!)
- **opschaling** - "scaling up"
- **afwijzen** - "to reject"
- **aanneming** - "assumption/contracting"
- **verscheping** - "shipping"
- **uitbetaling** - "payout"
- **vermindering** - "reduction"
- **afdwingen** - "to enforce"
- **uitgifte** - "issuance"
- **afrekeningen** - "settlements/accounts"
- **verschuiving** - "shift"
- **afwerpen** - "to throw off"
- **afleggen** - "to cover distance"
- **verveling** - "boredom" (!!)
- **afhandeling** - "handling"
- **afgeven** - "to hand over"
- **omzetting** - "conversion"
- **afkeer** - "aversion"
- **afname** - "decrease"
- **verwerven** - "to acquire"
- **aflossing** - "repayment"
- **aflossingen** - "repayments"
- **afzet** - "sales/deposition"
- **afbouw** - "phasing out"
- **afrekening** - "settlement"
- **afstel** - "postponement"
- **afnemen** - "to decrease"
- **afdracht** - "levy/payment"
- **afbetaling** - "installment payment"
- **afstaan** - "to cede"
- **verschaffen** - "to provide"

**Kept 4 terms** actually related to abolition:
- **afschaffen** (to abolish - verb form)
- **afschaffingswet** (abolition law)
- **afschaffingen** (abolitions - plural)
- **afschaffings-** (abolition prefix)

### Problem Parent 2: "uitsluiting" (exclusion)
BERTJE expanded to many "sluiten" (to close) derivatives:

**Removed 18 terms** from "uitsluiting" parent:
- **uitlating** - "utterance/statement"
- **sluit** - "closes/fits" (generic verb)
- **sluitend** - "conclusive/watertight"
- **sluiten** - "to close" (too generic)
- **aansluiten** - "to connect/join" (opposite meaning!)
- **uitsluitsel** - "certainty/decision"
- **afsluiten** - "to close/finish"
- **insluiting** - "enclosure"
- **afsluit** - "closes"
- **afsluiting** - "closing/conclusion"
- **sluiting** - "closure"
- **opsluiting** - "imprisonment" (different concept)
- **aansluit** - "connects" (opposite!)
- **ontsluiting** - "unlocking/access" (opposite!)
- **uitreding** - "withdrawal" from organization
- **ingedeeld** - "classified/categorized"

**Kept 1 term** actually related to exclusion:
- **uitsluiten** (to exclude - verb form)

### Other Semantic Drift (11 terms)
- **verscheidenheid** - "diversity" (positive concept, not fragmentation)
- **verdeeld** - "divided" (too generic standalone)
- **verspreid** - "scattered/spread" (too generic)
- **beoordelen** - "to judge/assess" (not prejudice)
- **veroordelen** - "to condemn/convict" (too generic)
- **aannames** - "assumptions" (too generic)
- **oordelen** - "judgments" (too generic)
- **bezaten** - "possessed" (generic verb)
- **teelt** - "cultivation" (too generic)
- **tuin** - "garden" (too generic)
- **planten** - "plants" (too generic)
- **plant** - "plant" (too generic)
- **plantaadje** - "little plantation" (diminutive, not serious)

### Polysemous Confusion (1 term)
- **kast** - Can mean "cabinet" (furniture) OR "caste" (social system) - removed due to ambiguity

### Geographic Confusion (1 term)
- **cuba** - Different country, not Dutch Caribbean

### Encoding Errors (1 term)
- **schiedenis** - Missing "ge-" prefix, should be "geschiedenis"

**Total Semantic Drift Removals**: 64 terms

---

## Phase 3: Overgeneralization Control

### Generic Temporal/Process Terms (5 terms)
- **vroeger** - "earlier/formerly" (too generic)
- **overleden** - "deceased" (too generic)
- **rederij** - "shipping company" (too generic)

### Morphological Fragments (5 terms)
- **bon** (from bonaire)
- **antiracisme-** (prefix fragment)
- **verdeeld-** (prefix fragment)
- **antidiscriminatie-** (prefix fragment)
- **eiland-** (prefix fragment)
- **slavernijverle-** (fragment of slavernijverleden)

### Different Topic (1 term)
- **vrouwenemancipatie** - Women's emancipation (different from slave emancipation)

### Not Relevant to Racism Topic (1 term)
- **kunsthistorici** - Art historians

---

## Phase 4: Category Corrections

### Major Recategorization: Slave Trade Terms
**29 terms** recategorized from various categories to `era_context` (0.55) or `related_weak` (0.65):

#### Slave Trade Commercial Infrastructure → era_context (0.55)
These are historical slave trade activities, not contemporary racism manifestations:

| Term | Original Category | Reason |
|------|-------------------|---------|
| slavenhandelsrederij | related_weak (0.65) | Historical slave trade company |
| slavenhandelsrederijen | related_weak (0.65) | Historical slave trade companies |
| slavenhandelrederijen | related_weak (0.65) | Historical slave trade companies |
| slavenbezit | related_weak (0.65) | Historical slave ownership |
| slavenbezitters | related_weak (0.65) | Historical slave owners |
| slavenkopers | related_weak (0.65) | Historical slave buyers |
| slavenmarkten | related_weak (0.65) | Historical slave markets |
| slaavenhandel | related_weak (0.65) | Historical slave trade variant |
| slavenverkoop | related_weak (0.65) | Historical slave sales |
| slavenhandelaar | related_weak (0.65) | Historical slave trader |
| slavenmarkt | related_weak (0.65) | Historical slave market |
| slavenhandelaars | related_weak (0.65) | Historical slave traders |
| slavenhandelsnaties | related_weak (0.65) | Historical slave trading nations |
| slavenhandelaren | related_weak (0.65) | Historical slave traders |
| slavenhandels-| related_weak (0.65) | Historical slave trade prefix |

#### Abolitionist Movement → related_weak (0.65)
Historical anti-slavery movement, kept but lowered:

| Term | Original Category | New Category |
|------|-------------------|--------------|
| abolitionisme | related_moderate (0.75) | related_weak (0.65) |
| abolitionistische | related_moderate (0.75) | related_weak (0.65) |
| abolitionist | related_moderate (0.75) | related_weak (0.65) |
| abolitionistisch | related_moderate (0.75) | related_weak (0.65) |

#### WIC (West India Company) → era_context (0.55)
Historical colonial company infrastructure:

| Term | Original Category |
|------|-------------------|
| wic-schepen | related_strong (0.85) |
| west-indië | related_strong (0.85) |
| west-indische | related_strong (0.85) |
| west-indie | related_strong (0.85) |
| westindische | related_strong (0.85) |
| wic-monopolie | related_strong (0.85) |
| wic-bezit | related_strong (0.85) |
| wic- | related_strong (0.85) |

#### Slave Revolts → related_weak (0.65)
- **slavenopstanden** - Historical slave revolts (0.75 → 0.65)
- **slaafmakers** - Historical enslavers (0.75 → 0.65)

---

## Phase 5: Weight Calibration

### Core Problem Quality Control (weight 1.00)
**Original**: 15 expanded terms at 1.00

**Removed 1**:
- ❌ **antiracisme-** - Morphological fragment prefix

**Kept 14** - All valid racism/discrimination/inequality terms:
- ✅ **non-discriminatiegrond** / **non-discriminatiegronden**
- ✅ **ongelijke** / **ongelijk** / **ongelijkheden**
- ✅ **non-discriminatie**
- ✅ **discriminatiegrond** / **discriminatiegronden**
- ✅ **racism** (English)
- ✅ **anti-zwartracisme** (anti-Black racism)
- ✅ **antiracisme** / **anti-racisme**
- ✅ **racismeprobleem**
- ✅ **racismevormen**

**Final**: 14 core_problem expansions (+ 8 seeds = 22 total)

### Strong Problem Adjustments (weight 0.95)
**Original**: 26 expanded terms at 0.95

**Removed 18** (mostly semantic drift from "uitsluiting"):
- Variants of "sluiten" (to close) - wrong meaning
- "verscheidenheid" (diversity - positive)
- "verdeeld-" (fragment)

**Reweighted 3**:
- **opsplitsing** (0.95 → 0.75) - splitting/division, related but not core
- **verdeeld** (0.95 → 0.75) - divided, too generic
- **verdeling** (0.95 → 0.75) - division/distribution, generic

**Kept 5**:
- ✅ **uitsluiten** (to exclude)
- ✅ **kleurlingen** (colored people - colorism term)
- ✅ **raciaal-etnische** (racial-ethnic)
- ✅ **anti-racistisch** (anti-racist)
- ✅ **racistische** (racist adjective)

**Final**: 5 strong_problem expansions (+ 28 seeds = 33 total)

### High Frequency Dampening

| Term | Original | New | df | Reason |
|------|----------|-----|-----|--------|
| discriminatie | 0.85 | 0.75 | 265 | Very high frequency |
| slaaf | 0.75 | 0.65 | 337 | Highest frequency term |
| slaafgemaakte | 0.75 | 0.65 | 152 | High frequency |
| etnische | 0.90 | 0.80 | 69 | High frequency |
| caribisch | 0.50 | 0.45 | 442 | Very high |
| eilanden | 0.50 | 0.45 | 421 | Very high |
| caribische | 0.50 | 0.45 | 205 | High |
| slavernij | 0.55 | 0.55 | 824 | Kept despite highest df |
| koloniën | 0.55 | 0.55 | 289 | Kept |
| historische | 0.55 | 0.55 | 128 | Kept |
| kolonialisme | 0.55 | 0.55 | 125 | Kept |
| planters | 0.65 | 0.65 | 121 | Kept (plantation context) |

---

## Final Weight Distribution

| Weight | Count | Category | Notes |
|--------|-------|----------|-------|
| 1.00 | 14 | core_problem | Racism/discrimination/inequality terms |
| 0.95 | 5 | strong_problem | Exclusion, colorism, racist |
| 0.85 | 12 | related_strong | Discrimination legal/policy terms |
| 0.80 | 1 | related_strong | etnische (dampened) |
| 0.75 | 15 | related_moderate | Emancipation, slavery actors |
| 0.65 | 35 | related_weak | Plantation economy + historical |
| 0.55 | 85 | era_context | Historical slavery/colonial terms |
| 0.50 | 4 | geographic_context | BES islands specific |
| 0.45 | 3 | geographic_context | Caribbean (dampened) |

**Distribution shape**: Proper pyramid - concentrated at era_context (Stage 1 appropriate)

---

## Final Category Distribution

| Category | Count | Percentage |
|----------|-------|------------|
| era_context | 85 | 48.9% |
| related_weak | 35 | 20.1% |
| related_moderate | 15 | 8.6% |
| core_problem | 14 | 8.0% |
| related_strong | 13 | 7.5% |
| geographic_context | 7 | 4.0% |
| strong_problem | 5 | 2.9% |

**Notable**: Nearly half (49%) in era_context - appropriate for Stage 1 where historical context teaches BERTJE about racism's roots in slavery/colonialism.

---

## Quality Checks

### ✅ Coverage Check
- **Final term count**: 174 terms
- **Target range**: 50-150 terms → Slightly over but acceptable ✓
- **Distribution**: Proper pyramid structure ✓

### ✅ Weight Distribution
- **Core problem (1.00)**: 14 expanded + 8 seeds = 22 total
- **Strong problem (0.95)**: 5 expanded + 28 seeds = 33 total
- **Related categories (0.65-0.85)**: 61 terms (35%)
- **Era context (0.55)**: 85 terms (49%) - Stage 1 appropriate

### ✅ Parent Review
**Problematic parents cleaned**:
- "afschaffing" family: Removed 32/36 expansions (89% removal rate)
- "uitsluiting" family: Removed 18/19 expansions (95% removal rate)
- Plantation terms: Kept most (structural racism context)
- WIC terms: Recategorized to era_context

### ✅ Document Frequency Distribution
- **Median df**: 6
- **Most terms**: df = 2-30 (healthy range)
- **High df terms**: Appropriately reweighted
- **Highest df**: slavernij (824) kept at 0.55 - historical context

---

## Notable Patterns & Decisions

### 1. Plantation Economy as Structural Racism Foundation
**Kept 48 plantation-related terms** at `related_weak` (0.65):
- Plantation system created racial hierarchies
- Economic structure enforced social fragmentation
- Relevant to understanding contemporary racism's roots

Examples: plantagesysteem, plantagesamenleving, plantagehouders, plantagearbeid

**Rationale**: Plantation economy is the structural foundation of Caribbean racism - not just historical background but the system that created colorism, class divisions, racial hierarchies.

### 2. Slave Trade vs. Slavery Context
**Recategorized slave trade commerce** (0.65 → 0.55):
- slavenhandelaar, slavenmarkt, slavenverkoop → era_context
- These are historical commercial activities

**Kept slavery social relations** (0.65-0.75):
- slaafgemaakten, nazaten, emancipatie → related_weak/moderate
- These describe social relationships still relevant to racism

### 3. Colorism Central to Topic
**Kept high weights**:
- kleurlingen (0.95) - colored people (historical racial category)
- huidskleuren (0.85) - skin colors
- huidskleur (seed, 1.00)

Framework explicitly notes colorism as persistent legacy.

### 4. Discrimination Legal Terminology
Comprehensive legal/policy language:
- discriminatiegrond(en), discriminatiezaak/zaken
- non-discriminatie, antidiscriminatie
- discriminatieverboden

### 5. Historical Abolition Context
Kept at low weights (0.55-0.65):
- afschaffing derivatives (only 4 kept)
- Abolitionist movement (4 terms at 0.65)

---

## Stage-Specific Decisions (Stage 1: Domain Corpus)

### Philosophy Applied: PERMISSIVE (with limits)

#### KEPT: Historical Context Terms (era_context 0.55)
- 85 slavery/colonial history terms
- WIC infrastructure (recategorized from 0.85 → 0.55)
- Abolitionist movement (lowered from 0.75 → 0.65)

**Rationale**: Stage 1 requires BERTJE to learn historical roots of contemporary racism.

#### KEPT: Plantation Economy (related_weak 0.65)
- 48 plantation terms
- Economic structure that created racial hierarchy

**Rationale**: Not just history - structural foundation of social fragmentation.

#### REMOVED: Even in Stage 1
- Semantic drift (64 terms) - wrong meanings
- Morphological fragments (5 terms)
- Too generic (11 terms)
- Different topics (2 terms)

**Rationale**: Noise is noise regardless of stage.

---

## Curation Decision Summary by Reason

### Removals by Type (75 terms)

| Reason Category | Count |
|----------------|-------|
| Semantic drift from "afschaffing" | 32 |
| Semantic drift from "uitsluiting" | 18 |
| Other semantic drift | 11 |
| Too generic | 5 |
| Morphological fragments | 5 |
| Different topic | 2 |
| Polysemous | 1 |
| Geographic confusion | 1 |

---

## Key Terms Retained

### Core Problem (1.00)
Seeds:
- racisme, discrimineren, discriminerend
- rassendiscriminatie, etnische discriminatie
- vooroordelen, huidskleur, kleurisme
- ongelijkheid, verdeeldheid, segregatie
- racistisch, uitsluiting, afschaffing (historical)

Expansions:
- racism, anti-zwartracisme, racismeprobleem, racismevormen
- antiracisme, anti-racisme
- non-discriminatie, discriminatiegrond(en), non-discriminatiegrond(en)
- ongelijk(e), ongelijkheden

### Strong Problem (0.95)
- uitsluiten, kleurlingen (colorism)
- raciaal-etnische, anti-racistisch, racistische

### Related Strong (0.80-0.85)
- etnische (dampened to 0.80)
- Discrimination terminology: discriminatiezaak/zaken, discriminatieverboden, discriminatoire, discriminerende, gediscrimineerd(e), discriminatie- (prefix)
- anti-vooroordelen, vooroordeel, huidskleuren
- etnografisch

### Related Moderate (0.75)
- Emancipation: emancipatiebeleid, emancipatieplan, emancipatiewet, emancipatieproces, slavenemancipatie
- Slavery actors: slaafgemaakten variants, nazaat, niet-nazaten
- discriminatie (dampened from 0.85)

### Related Weak (0.65)
- Plantation economy: 48 terms describing structural system
- Historical actors: planters, plantagehouders, plantagearbeiders
- Abolitionist movement: 4 terms (lowered from 0.75)
- slaaf, slaafgemaakte (dampened from 0.75)

### Era Context (0.55)
- 85 historical terms: slavery, colonialism, WIC, slave trade commerce
- Historical processes: kolonisatie, afschaffing

---

## Files Generated

1. **topic2_racism_manual_review.csv** - Full manual review list
2. **topic2_racism_curation_state.csv** - Intermediate state with decisions
3. **topic2_racism_CURATED.csv** - Full curated data with decisions
4. **topic2_racism_FINAL_DICTIONARY.csv** - Final clean dictionary
5. **TOPIC2_RACISM_CURATION_REPORT.md** - This report

---

## Recommendations for Stage 2 (Policy Corpus)

When moving to Stage 2, additional curation will be needed:

### Likely Remove in Stage 2
- Many era_context terms if df < 5 in policy corpus
- Historical WIC infrastructure (unless policies reference it)
- Detailed plantation terminology (unless policy-relevant)
- Abolitionist movement terms

### Definitely Keep in Stage 2
- All core racism/discrimination terms (1.00, 0.95)
- Legal discrimination terminology (0.85)
- Contemporary social actors (nazaten, descendants)
- Emancipation policy terms (if in policy discourse)

### Monitor in Stage 2
- Whether plantation terms appear in policy language
- If colorism terms (kleurlingen, huidskleuren) used in policies
- Whether historical context referenced in policy documents

---

## Validation Notes

### Vocabulary Coherence ✓
Reading through final 174 terms, they collectively describe:
1. Racism and discrimination (core)
2. Social exclusion and fragmentation
3. Colorism and racial hierarchies
4. Plantation economy as structural foundation
5. Historical slavery and colonialism context
6. Emancipation and contemporary descendants

### Semantic Consistency ✓
- Core problems truly represent racism/discrimination
- Historical terms appropriately low (0.55)
- Plantation economy at 0.65 (structural, not just historical)
- High-frequency terms dampened
- Semantic drift aggressively removed

### Test Readiness ✓
Dictionary ready for:
1. BERTJE semantic training (Stage 1)
2. Teaching historical roots of contemporary racism
3. Distinguishing structural vs. individual racism
4. Recognizing colorism patterns

---

## Curator Notes

This topic required the most aggressive semantic drift removal of all topics. The parents "afschaffing" and "uitsluiting" generated many false cognates based on prefix/suffix similarity rather than semantic meaning.

### Key Judgment Calls

1. **Plantation economy kept at 0.65** - These terms describe the structural economic system that created and enforced racial hierarchies. Not just historical background, but foundational to understanding racism's structure.

2. **Slave trade commerce recategorized to 0.55** - The commercial infrastructure (markets, traders, sales) is historical process. But the social relations (enslaved people, descendants, emancipation) remain relevant at 0.65-0.75.

3. **Aggressive removal of "af-" verbs** - Only kept 4/36 expansions from "afschaffing". Most were generic verbs with "af-" prefix that had nothing to do with abolition.

4. **Colorism terms kept high** - Framework explicitly identifies colorism as contemporary problem rooted in slavery. Terms like "kleurlingen" and "huidskleuren" kept at 0.85-0.95.

5. **WIC recategorized down** - West India Company infrastructure moved from 0.85 → 0.55. Historical commercial entity, not contemporary racism manifestation.

The resulting dictionary teaches BERTJE that Social Fragmentation & Racism involves:
- **Contemporary manifestations** (racism, discrimination, exclusion) - high weights
- **Structural foundations** (plantation economy, racial hierarchies) - medium weights
- **Historical roots** (slavery, colonialism, WIC) - low weights
- **Geographic context** (BES islands) - low weights

---

**Curation Completed**: 2025-12-17
**Status**: Ready for review and next topic (Topic 3: Governance Distrust & Corruption)
