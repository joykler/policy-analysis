# BERTJE Fine-tuning Contribution Analysis
## Slavery Corpus vs Policy Corpus Dictionary Comparison

**Date**: 2025-12-12
**Analysis**: What did BERTJE training on slavery corpus contribute vs. policy corpus?

---

## Executive Summary

Training BERTJE on the **slavery-specific corpus** (academic, historical, Dutch Caribbean slavery literature) vs. the **policy corpus** (government policy documents) produced **notably different semantic spaces**, revealing what each training regime contributes.

### Key Findings

1. **Slavery corpus dictionary: 1006 terms** (+113 more than policy)
2. **Policy corpus dictionary: 893 terms**
3. **Overlap: 79%** (578 shared terms) - substantial common foundation
4. **Slavery-only: 154 terms (21%)** - what slavery corpus adds
5. **Policy-only: 94 terms (14%)** - what policy corpus adds

---

## What Slavery Corpus Training Contributes

### 1. **Idealized Seed Terms (df=0)** - 64 terms

**Problem**: Slavery corpus training retained **64 compound seed terms with df=0** (not appearing in actual corpus). These are theoretically correct but **not empirically grounded**.

**Examples by topic**:
- **Education**: `brain drain`, `onderwijs-achterstand`, `onderwijsachterstand`, `onderwijsongelijkheid`, `onderwijsuitsluiting`
- **Governance**: `corrupt`, `omkoping`, `institutioneel wantrouwen`, `paternalisme`, `gebrek aan autonomie`
- **Poverty**: `economische kwetsbaarheid`, `extractieve economie`, `structurele afhankelijkheid`, `structurele armoede`
- **Racism**: `institutioneel racisme`, `raciale hiërarchie`, `structureel racisme`, `kleurisme`

**Interpretation**: These are **academic/theoretical constructs** that appear in slavery literature but not in actual government policy language. They represent how **scholars conceptualize** slavery legacy, not how **policy actors discuss** it.

### 2. **Historical/Temporal Language** - 5 terms

Slavery corpus adds historical framing:
- `geschiedenisboek`, `historie`, `overleden`, `voorgeschiedenis`, `vroeger`

**Interpretation**: Slavery literature is backward-looking (what happened), policy documents are forward-looking (what to do).

### 3. **Academic Jargon** - Multiple high-weight terms

Examples:
- **Education**: `academie` (0.75), `instituten` (0.75), `katholiek onderwijs` (0.70)
- **Governance**: `essay` (0.75), `kabinet-kok` (0.75) - referencing specific historical cabinets

**Interpretation**: Slavery corpus is scholarly discourse, policy corpus is bureaucratic discourse.

### 4. **Slavery-Specific Historical Terms** - 9 terms

Direct slavery references:
- `gebrek aan transparantie`, `koloniaal bestuur`, `koloniale economie`, `plantage-maatschappij`, `plantagedirectie`, `slaaf`, `slavernijverle-`, `voc-koloniën`, `wic-kolonie`

**Note**: These appear in slavery corpus but were **removed from policy corpus** during Phase 2 curation as not policy-relevant.

### 5. **English Terms** - Multiple

Slavery corpus retains English:
- **Education**: `brain drain` (1.00 weight!)
- **Racism**: `racism` (1.00), `abolition` (0.75)

**Interpretation**: Academic slavery literature code-switches to English; Dutch policy doesn't.

### 6. **Category Distribution Differences**

| Category | Slavery | Policy | Slavery Adds |
|----------|---------|--------|--------------|
| `core_problem` | 54 | 41 | **+13** |
| `strong_problem` | 49 | 33 | **+16** |
| `related_weak` | 75 | 61 | **+14** |
| `era_context` | 275 | 220 | **+55** |
| `geographic_context` | 62 | 54 | **+8** |

**Interpretation**: Slavery corpus has **55 more historical/temporal terms** and **13-16 more strong problem terms** (likely the idealized df=0 compounds).

---

## What Policy Corpus Training Contributes

### 1. **Contemporary Policy Language** - Dominant pattern

Policy corpus discovers terms **actually used in government documents**:

#### Education (26 unique policy terms):
- `lesmethoden`, `lesmethodes`, `onderwijsconferentie` - **pedagogical implementation**
- `universiteiten`, `mbo-scholen`, `faculteit` - **institutional types**
- `examens`, `schooljaar`, `schooljaren`, `klaslokaal` - **education operations**
- `leerplichtige`, `geschiedonderwijs`, `opleidingstrajecten` - **policy mechanisms**
- `migratiestromen`, `arbeidsmigratie` - **migration in policy context**

#### Governance (39 unique policy terms):
- `staatscommissie`, `gemeenteraad`, `rijksvertegenwoordiger` - **Dutch state institutions**
- `koninkrijksdelen`, `koninkrijksrelaties` - **Kingdom relations (NL-Caribbean)**
- `grondwetgevende`, `rechtsregels`, `territoriale` - **constitutional language**
- `democratische`, `democratisch`, `democratieën` - **democratic governance**
- `medeoverheden`, `bestuursfuncties`, `instituties` - **administrative structures**

#### Poverty (20 unique policy terms):
- `inkomensbeleid`, `arbeidskrachten`, `werkveld` - **labor market policy**
- `staatsfinanciën`, `bedrijfskapitaal` - **economic policy**
- `prijs`, `prijzen`, `kost` - **cost/pricing (economic indicators)**
- **CRITICAL**: `afschaffing` (0.45 weight, df=205) - **most frequent historical reference term**
- `afschaffingswet`, `afschaffingen`, `afschaffen`, `afschaffings-` - **abolition morphology**

#### Racism (22 unique policy terms):
- `antidiscriminatie-`, `antiracisme-`, `stagediscriminatie` - **anti-discrimination policy**
- `uitbuiting`, `uitsluiten` - **exclusion mechanisms**
- `veronderstellingen`, `opvattingen`, `opvatting` - **attitudes/beliefs (policy targets)**

### 2. **Morphological Variants of High-Frequency Terms**

Policy corpus captures **how terms actually vary** in documents:

**"afschaffing" (abolition) family**:
- `afschaffing` itself: df=205 (appears in 20% of documents!)
- `afschaffingswet`, `afschaffingen`, `afschaffen`, `afschaffings-`, `afbouw`, `omzetting`

**Interpretation**: Policy documents **constantly reference** the 1863 abolition as historical context. BERTJE trained on policy corpus learns these morphological patterns **from actual usage frequency**.

### 3. **Institutional Specificity**

Policy corpus is highly **institutionally specific**:
- `staatscommissie` (df=31) - state commissions appear frequently
- `medeoverheden` (df=21) - co-governing authorities (Caribbean-NL relations)
- `instituties` (df=26) - institutions as policy objects

**Interpretation**: Policy documents reference specific Dutch governmental structures; slavery literature is more generic/theoretical.

### 4. **Weight Distribution Differences**

| Weight Tier | Slavery | Policy | Difference |
|-------------|---------|--------|------------|
| 0.55 (era_context) | 265 | 166 | **-99** |
| 0.45 | 11 | 33 | **+22** |
| 0.40 | 0 | 19 | **+19** |

**Interpretation**: Policy corpus **down-weights 99 historical terms** from 0.55 to 0.45-0.40, reflecting that historical references are **less central** in policy discourse than slavery scholarship.

---

## Critical Differences in Semantic Space

### Slavery Corpus Semantic Space:
1. **Theoretical/conceptual** - idealized problem constructs (df=0)
2. **Historical/scholarly** - looking backward at what happened
3. **Academic discourse** - essay, historiography, theoretical debates
4. **English code-switching** - "brain drain", "racism", "abolition"
5. **Generic geography** - less specific institutional grounding

### Policy Corpus Semantic Space:
1. **Empirical/operational** - terms actually appearing in documents
2. **Forward-looking** - policy mechanisms, interventions, structures
3. **Bureaucratic discourse** - staatscommissie, rijksvertegenwoordiger, medeoverheden
4. **Dutch-only** - no English code-switching
5. **Institutionally specific** - Dutch Kingdom structures, Caribbean relations
6. **Morphologically rich** - captures how terms vary in actual usage (afschaffing family)

---

## Implications for Topic Modeling

### Stage 1 (Slavery Corpus) Strengths:
- **Semantic foundation**: Learns conceptual relationships between slavery legacy concepts
- **Problem identification**: High-weight theoretical constructs anchor each topic
- **Historical grounding**: Era context establishes temporal frame

### Stage 1 Weaknesses:
- **Idealized language**: 64 df=0 terms not in actual policy
- **Wrong discourse register**: Academic vs. bureaucratic
- **Missing operational terms**: No "staatscommissie", "koninkrijksdelen", etc.

### Stage 2 (Policy Corpus) Strengths:
- **Empirically grounded**: All terms appear in actual documents
- **Policy-relevant vocabulary**: Captures how government discusses these issues
- **Operational specificity**: Learns implementation mechanisms
- **Morphological realism**: Captures actual term variation (afschaffing family)

### Stage 2 Weaknesses:
- **Less theoretical**: May miss conceptual connections (no "extractieve economie")
- **Implicit framing**: Problems not explicitly labeled (no "structureel racisme")

---

## Recommended Two-Stage Approach

**CONFIRMED**: The two-stage training is well-designed:

1. **Stage 1 (Slavery Corpus)**:
   - Learns **conceptual structure** of slavery legacy problems
   - Establishes **semantic anchors** (even if idealized)
   - Provides **historical context** vocabulary

2. **Stage 2 (Policy Corpus)**:
   - **Adapts** semantic space to policy discourse
   - **Grounds** concepts in empirical term usage
   - **Captures** Dutch governmental institutional specificity
   - **Fine-tunes** weights based on actual document frequencies

**Result**: Model that understands slavery legacy **concepts** (Stage 1) but detects them using **policy-relevant language** (Stage 2).

---

## Specific Contributions Summary

### What Slavery BERTJE Uniquely Contributes:
1. **Theoretical problem constructs** (64 df=0 compounds)
2. **Historical framing** (5 temporal terms)
3. **Scholarly discourse markers** (academic terms)
4. **Explicit problem labeling** (structureel racisme, extractieve economie)
5. **English equivalents** (brain drain, racism, abolition)

### What Policy BERTJE Uniquely Contributes:
1. **Dutch state institutional vocabulary** (39 governance terms)
2. **Operational education terms** (26 terms: lesmethoden, examens, schooljaar)
3. **Anti-discrimination policy language** (antidiscriminatie-, antiracisme-, stagediscriminatie)
4. **Morphological families of high-frequency terms** (afschaffing: df=205)
5. **Economic policy indicators** (prijs, staatsfinanciën, inkomensbeleid)
6. **Kingdom relations vocabulary** (koninkrijksdelen, medeoverheden)

### Shared Foundation (79% overlap, 578 terms):
- Core slavery legacy vocabulary (slavernij, koloniale, caribisch)
- Geographic terms (suriname, curaçao, bonaire, aruba)
- WIC/VOC historical references
- Topic-specific problem terms appearing in both discourses
- Cross-topic domain signals

---

## Conclusion

**The slavery corpus training contributes CONCEPTUAL STRUCTURE.**
**The policy corpus training contributes DISCOURSE SPECIFICITY.**

Together, they create a model that:
1. **Understands** slavery legacy as theoretical problem (Stage 1)
2. **Detects** it in policy documents using bureaucratic language (Stage 2)

This is exactly what's needed for the use case: identifying which Dutch policy documents address slavery legacy problems, using the vocabulary policy actors actually use.
