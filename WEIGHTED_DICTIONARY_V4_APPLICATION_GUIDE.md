# Weighted Dictionary v4 - Application Guide for Slavery Legacy Topics

## Overview

This document explains how the 7-tier weighting system has been applied to the **5-topic Dutch Slavery Legacy dictionary** (177 terms) for use in the v24 unified embedding notebook.

**Created File**: [`dutch_slavery_legacy_5topics_seed_v4_weighted.csv`](dutch_slavery_legacy_5topics_seed_v4_weighted.csv)

---

## Weight Distribution Summary

| Weight | Category | Count | % of Total | Purpose |
|--------|----------|-------|------------|---------|
| **1.00** | `core_problem` | 17 | 9.6% | Central concepts |
| **0.95** | `strong_problem` | 28 | 15.8% | Clear manifestations |
| **0.85** | `related_strong` | 25 | 14.1% | Domain manifestations |
| **0.80** | `related_strong_specific` | 22 | 12.4% | Specialized context |
| **0.75** | `related_moderate` | 20 | 11.3% | Actors/processes |
| **0.70** | `related_moderate_weak` | 15 | 8.5% | Broader context |
| **0.65** | `related_weak` | 3 | 1.7% | Weak contextual clues |
| **0.55** | `era_context` | 15 | 8.5% | Temporal markers |
| **0.50** | `geographic_context` | 32 | 18.1% | Spatial markers |
| **TOTAL** | | **177** | **100%** | |

---

## Topic-by-Topic Analysis

### 1. Colonial Systems (35 terms)

**Weight Range**: 0.50 - 1.00

**Core Concepts (1.00)** - 3 terms:
- `kolonialisme`, `koloniaal`, `kolonie`

**Strong Manifestations (0.95)** - 3 terms:
- `wic`, `west-indische compagnie`, `dekolonisatie`

**Related Strong (0.85)** - Institutional structures - 5 terms:
- `plantage`, `plantages`, `plantagekolonie`, `gouverneur`, `koloniaal bestuur`

**Related Strong Specific (0.80)** - Economic systems - 4 terms:
- `exploitatie`, `handel`, `handelsmonopolie`, `plantagehouders`

**Related Moderate (0.75)** - Actors - 4 terms:
- `gekoloniseerden`, `handelaren`, `compagnie`, `westindische`

**Related Moderate Weak (0.70)** - General admin - 1 term:
- `bestuur`

**Era Context (0.55)** - Temporal marker - 1 term:
- `koloniale periode`

**Geographic Context (0.50)** - Place markers - 14 terms:
- Caribbean territories: Suriname, Paramaribo, Curaçao, Aruba, Bonaire, Antillen, etc.

**Rationale**: Colonial Systems has the heaviest geographic context (14 terms) because the system operated in specific territories. Institutional terms like "plantage" and "gouverneur" get high weights (0.85) as they are defining features of colonial administration.

---

### 2. Historical Slavery (41 terms)

**Weight Range**: 0.50 - 1.00

**Core Concepts (1.00)** - 3 terms:
- `slavernij`, `slavernijverleden`, `slavenhandel`

**Strong Manifestations (0.95)** - 6 terms:
- `slaafgemaakte`, `slaafgemaakten`, `slaven`, `dwangarbeid`, `slavenhouders`, `slavenhandelaren`

**Related Strong (0.85)** - Conditions & resistance - 7 terms:
- `ketenen`, `zweep`, `verzet`, `slavenopstand`, `marrons`, `marronage`, `middenpassage`

**Related Strong Specific (0.80)** - Infrastructure - 3 terms:
- `slavenschepen`, `verkoop`, `vrijkopen`

**Related Moderate (0.75)** - Labor context - 1 term:
- `arbeid`

**Related Moderate Weak (0.70)** - Historical endpoints - 2 terms:
- `afschaffing`, `1863`

**Related Weak (0.65)** - Geographic scope - 3 terms:
- `atlantisch`, `atlantische`, `trans-atlantisch`

**Era Context (0.55)** - Temporal markers - 9 terms:
- `eeuw`, `achttiende eeuw`, `negentiende eeuw`, `zeventiende eeuw`, `destijds`, `toenmalig`, `voormalig`, `historisch`, `geschiedenis`

**Geographic Context (0.50)** - Place markers - 7 terms:
- Caribbean territories: Suriname, Curaçao, Aruba, Antillen, etc.

**Rationale**: Historical Slavery has the most temporal markers (9 terms at 0.55) to distinguish historical discussion from contemporary issues. Terms like "slaafgemaakte" (preferred modern term) and "slaven" both get 0.95 to capture both contemporary and historical language. Resistance terms (marrons, verzet) get 0.85 as they're defining features of the slavery experience.

---

### 3. Modern Racism & Discrimination (35 terms)

**Weight Range**: 0.50 - 1.00

**Core Concepts (1.00)** - 4 terms:
- `racisme`, `discriminatie`, `structureel`, `structurele`

**Strong Manifestations (0.95)** - 6 terms:
- `uitsluiting`, `uitbuiting`, `segregatie`, `ongelijkheid`, `alledaags racisme`, `microagressie`

**Related Strong (0.85)** - Mechanisms - 3 terms:
- `stereotypering`, `vooroordelen`, `achterstand`

**Related Strong Specific (0.80)** - Identity & experience - 6 terms:
- `raciale`, `etnisch`, `zwarte`, `kleur`, `huidskleur`, `gemarginaliseerde`

**Related Moderate (0.75)** - Experiences & solutions - 5 terms:
- `veilig voelen`, `meldingsbereidheid`, `gelijkwaardig burgerschap`, `inclusie`, `gemeenschappen`

**Related Moderate Weak (0.70)** - Response mechanisms - 3 terms:
- `antiracisme`, `activisme`, `belangenorganisaties`

**Era Context (0.55)** - Contemporary markers - 5 terms:
- `hedendaags`, `actueel`, `tegenwoordig`, `huidig`, `hedendaagse`

**Geographic Context (0.50)** - Ethnic/origin markers - 3 terms:
- `Antilliaans`, `Surinaams`, `Caribisch`

**Rationale**: "Structureel/structurele" get 1.00 (core) because structural racism is central to understanding modern manifestations of slavery's legacy. Contemporary temporal markers (0.55) help distinguish present-day discrimination from historical slavery. Identity terms (0.80) are weighted high as they're central to experiencing discrimination but not the problem itself.

---

### 4. Heritage & Memory (28 terms)

**Weight Range**: 0.50 - 1.00

**Core Concepts (1.00)** - 4 terms:
- `keti koti`, `slavernijherdenking`, `slavernijgeschiedenis`, `slavernijverleden`

**Strong Manifestations (0.95)** - 5 terms:
- `eerste juli`, `1 juli`, `nationale herdenking`, `herdenking`, `slavernijmonument`

**Related Strong (0.85)** - Memorialization - 5 terms:
- `monument`, `erfgoed`, `slavernijmuseum`, `gedenken`, `ceremonie`

**Related Strong Specific (0.80)** - Education & awareness - 4 terms:
- `geschiedenisonderwijs`, `bewustwording`, `bewustzijn`, `tentoonstelling`

**Related Moderate (0.75)** - Institutions & content - 4 terms:
- `museum`, `verhalen`, `getuigenissen`, `erkenning`

**Related Moderate Weak (0.70)** - Community - 2 terms:
- `nazaten`, `diaspora`

**Geographic Context (0.50)** - Place markers - 4 terms:
- `Suriname`, `Curaçao`, `Antillen`, `Caribisch`

**Rationale**: "Keti Koti" (Chains Broken - July 1st celebration) gets 1.00 as it's the defining memorial event. Specific dates ("eerste juli", "1 juli") get 0.95 as they're strong signals of heritage discussion. Education terms (0.80) are weighted high as they're mechanisms for memory preservation but not the memory itself.

---

### 5. Policy & Reparations (38 terms)

**Weight Range**: 0.50 - 1.00

**Core Concepts (1.00)** - 3 terms:
- `herstelbetalingen`, `reparaties`, `herstelbeleid`

**Strong Manifestations (0.95)** - 8 terms:
- `compensatie`, `schadevergoeding`, `restitutie`, `excuses`, `verontschuldiging`, `schulderkenning`, `eerherstel`, `rechtsherstel`

**Related Strong (0.85)** - Legislative action - 5 terms:
- `wetgeving`, `wetsvoorstel`, `wet`, `grondwet`, `motie`

**Related Strong Specific (0.80)** - Policy process - 5 terms:
- `kamerstukken`, `kamerdebat`, `parlementair`, `beleidsnota`, `maatregelen`

**Related Moderate (0.75)** - Governance & research - 6 terms:
- `commissie`, `rapport`, `aanbevelingen`, `onderzoek`, `adviesraad`, `besluit`

**Related Moderate Weak (0.70)** - Actors & general process - 7 terms:
- `minister`, `staatssecretaris`, `regering`, `kabinet`, `rijksoverheid`, `debat`, `beleid`

**Geographic Context (0.50)** - Place markers - 4 terms:
- `Suriname`, `Curaçao`, `Antillen`, `Caribisch Nederland`

**Rationale**: Reparations-specific terms get highest weights (1.00, 0.95) as they're the core policy response. Legislative terms (0.85) are weighted high as they're concrete actions. Generic policy terms like "beleid" and political actors like "minister" get lower weights (0.70) as they appear in many policy contexts.

---

## Strategic Weighting Decisions

### 1. Geographic Markers (0.50)

**All geographic terms get 0.50** across all topics:
- Suriname, Curaçao, Aruba, Bonaire, Antillen, Caribisch, etc.

**Why?**
- These are **context clues** not problem indicators
- Help BERTJE focus on **Dutch slavery legacy** vs. other slavery contexts (US, Brazil, etc.)
- Prevent false positives from generic Caribbean/Suriname mentions
- Work synergistically: Low-weight geography alone = not relevant; High-weight problem + geography = highly relevant

### 2. Temporal Markers (0.55)

**Historical markers** (Historical Slavery):
- `historisch`, `eeuw`, `zeventiende eeuw`, `destijds`, `toenmalig`

**Contemporary markers** (Modern Racism):
- `hedendaags`, `actueel`, `tegenwoordig`, `huidig`

**Why?**
- Distinguish **historical discussion** from **contemporary manifestations**
- Prevent "slavernij" + "historisch" from drowning out "discriminatie" + "hedendaags"
- Enable BERTJE to understand temporal context without being keyword-dependent

### 3. Cross-Topic Overlaps

Some terms appear in multiple topics with **same weights**:

**Geographic overlap**:
- Suriname, Curaçao, Antillen, Caribisch → all 0.50 across all topics

**Heritage overlap**:
- `slavernijverleden` → 1.00 in both Historical Slavery AND Heritage & Memory
  - In Historical: Core concept of what happened
  - In Heritage: Core concept of what we remember

**Why allow overlap?**
- Reflects real semantic ambiguity
- BERTJE learns that terms can activate multiple topics
- Matches how humans discuss these issues (concepts are interconnected)

### 4. Preferred vs. Legacy Terminology

**Both weighted equally**:
- `slaafgemaakte` (modern preferred) = 0.95
- `slaven` (historical/legacy term) = 0.95

**Why?**
- Historical texts use "slaven"
- Contemporary texts use "slaafgemaakte"
- Both are equally valid signals of the topic
- BERTJE needs to recognize both to work across time periods

---

## How Weights Work in Practice

### Formula (Multiplicative Hybrid)

```python
seed_weight = from dictionary (0.50-1.00)
sif_weight = 1.0 / (a + term_freq/total_freq)  # Smooth Inverse Frequency
final_weight = seed_weight × sif_weight

topic_vector = sum(term_vector × final_weight) / sum(final_weight)
```

### Example Scenarios

**Scenario 1: Core concept, common word**
- Term: `slavernij`
- Seed weight: 1.00 (core)
- SIF weight: ~0.20 (very common in corpus)
- Final weight: 1.00 × 0.20 = **0.20**
- **Effect**: Important but common → moderate influence

**Scenario 2: Strong manifestation, rare word**
- Term: `microagressie`
- Seed weight: 0.95 (strong manifestation)
- SIF weight: ~0.90 (rare in corpus)
- Final weight: 0.95 × 0.90 = **0.855**
- **Effect**: Important and rare → very high influence

**Scenario 3: Geographic marker, moderate frequency**
- Term: `Suriname`
- Seed weight: 0.50 (geographic context)
- SIF weight: ~0.60 (moderately common)
- Final weight: 0.50 × 0.60 = **0.30**
- **Effect**: Context clue → low influence alone

**Scenario 4: Temporal marker, very common**
- Term: `historisch`
- Seed weight: 0.55 (era context)
- SIF weight: ~0.15 (very common)
- Final weight: 0.55 × 0.15 = **0.0825**
- **Effect**: Generic marker → very low influence

**Key Insight**: The hybrid system ensures that:
- **Rare important terms** dominate topic vectors (high seed × high SIF)
- **Common important terms** have moderate influence (high seed × low SIF)
- **Generic markers** provide context without overwhelming (low seed × variable SIF)

---

## Integration with v24 Notebook

### Update Configuration

In your notebook's CONFIG section, update the dictionary path:

```python
CONFIG = {
    "paths": {
        "dictionary_excel": r"C:\Users\Home\policy-analysis\dutch_slavery_legacy_5topics_seed_v4_weighted.csv",
        # ... other paths ...
    },
    "weights": {
        "default_core_weight": 1.0,         # For seed terms without explicit weight
        "default_discovered_weight": 0.80,   # For BERTJE-expanded terms
        "weighting_scheme": "multiplicative",
    },
    # ... rest of config ...
}
```

### Expected Behavior

1. **Dictionary Loading** (Checkpoint 0):
   - Should show: "Found weight column in seed dictionary"
   - Should preserve 177 terms with weights 0.50-1.00

2. **BERTJE Expansion** (Checkpoint 3):
   - Expanded terms inherit parent weight
   - New discovered terms get `default_discovered_weight` = 0.80

3. **Vector Building** (Checkpoint 4):
   - Should show: "BUILDING TOPIC VECTORS WITH HYBRID WEIGHTS"
   - Should show weight statistics per topic
   - Topic vectors will differ from SIF-only version

4. **Cosine Scoring** (Checkpoint 5):
   - Chunks with rare important terms → higher scores
   - Chunks with only common/generic terms → lower scores
   - Geographic/temporal markers provide context without dominating

---

## Validation Checklist

After integration, verify:

- [ ] Dictionary loaded with 177 terms
- [ ] Weight column preserved in seed dictionary
- [ ] Weight distribution matches expected (17 core, 28 strong, etc.)
- [ ] Expanded dictionary preserves parent weights
- [ ] Vector building uses hybrid weights (not just SIF)
- [ ] Console shows "Avg seed weight" and "Avg combined weight" per topic
- [ ] Topic vectors are semantically meaningful (inspect top terms)

---

## Topic-Specific Guidance

### For Historical Corpus (Stage 1)

**More permissive on**:
- Temporal markers (0.55) - historical context is expected
- Geographic markers (0.50) - territories are central
- Institutional terms (0.85) - colonial structures matter

**Configuration**:
```python
"default_core_weight": 1.0,
"default_discovered_weight": 0.75,  # Cautious with new historical terms
```

### For Policy Corpus (Stage 2)

**More restrictive on**:
- Temporal markers - focus on contemporary
- Geographic markers - unless discussing specific territories
- Generic policy terms (0.70) - "beleid" alone isn't enough

**Configuration**:
```python
"default_core_weight": 0.95,        # Slightly lower core weight
"default_discovered_weight": 0.85,  # More trust in policy vocabulary
```

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Terms** | 177 |
| **Topics** | 5 |
| **Weight Tiers** | 9 (1.00 to 0.50) |
| **Categories** | 9 distinct |
| **Avg Terms per Topic** | 35.4 |
| **Core Concepts** | 17 (9.6%) |
| **Strong Signals** | 45 (25.4%) |
| **Context Markers** | 47 (26.6%) |
| **Most Weighted Topic** | Historical Slavery (41 terms) |
| **Least Weighted Topic** | Heritage & Memory (28 terms) |

---

## Key Takeaways

1. **Weights reflect semantic importance** not just frequency
2. **Low weights are strategic** - they provide context without dominating
3. **Geographic/temporal markers** (0.50-0.55) prevent false positives
4. **Core concepts** (1.00) get modulated by corpus frequency (SIF)
5. **Hybrid system** balances expert knowledge with statistical patterns
6. **Overlap is intentional** - concepts are interconnected
7. **Both old and new terminology** weighted equally for temporal coverage

This weighted dictionary transforms your seed terms into a **nuanced semantic blueprint** that teaches BERTJE not just what words to look for, but **how much each word matters** in context.
