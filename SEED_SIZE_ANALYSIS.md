# Seed Dictionary Size Analysis: Small vs Large

## The Question

**Current trajectory**: 377 → 440 terms (+17%)
**Your concern**: Is this too large? Should we use a condensed seed and let corpus expansion do the work?

**Answer**: YES - you're right. A smaller, higher-quality seed is likely better.

## Why Smaller is Better

### 1. **Seed Purpose: Semantic Anchors, Not Exhaustive Coverage**

The seed dictionary's job is to:
- ✅ Define the **core semantic space** of each topic
- ✅ Provide **high-quality anchor terms** for SBERT expansion
- ❌ NOT enumerate every possible term

**Current problem**: 440 terms is approaching exhaustive enumeration
- 110 terms for Social Fragmentation & Racism
- 107 terms for Governance
- This defeats the purpose of "expansion"

### 2. **SBERT Expansion Will Find Variants**

**Example from your workflow**:

**Seed term**: `racisme` (1.00)
**SBERT finds** (k=50 nearest):
- racistisch (0.95 cosine)
- discriminerend (0.92 cosine)
- discriminatie (0.91 cosine)
- vooroordelen (0.88 cosine)
- ... and 45 more related terms

**If you manually add all variants to seed**:
- `racisme` (1.00)
- `racistisch` (0.95)
- `discriminerend` (0.95)
- `discriminatie` (1.00)
- `discrimineren` (0.90)

**Problem**: You're doing SBERT's job manually
- Wastes effort on predictable morphological variants
- SBERT would find these automatically from `racisme` alone

### 3. **Weight Differentiation Gets Diluted**

**With large seed (current)**:
- 110 Social Fragmentation terms with weights 0.70-1.00
- During expansion: 110 × 50 neighbors = 5,500 candidates
- After aggregation (top 300): Most are discovered terms (weight 0.80)
- **Result**: Seed weights barely matter because discovered terms dominate

**With small seed (proposed)**:
- 25 Social Fragmentation core terms with weights 0.85-1.00
- During expansion: 25 × 50 neighbors = 1,250 candidates
- After aggregation (top 300): Mix of high-weight seeds + discovered terms
- **Result**: Seed weights have meaningful influence

### 4. **Curation Becomes Harder**

**Current workflow**:
1. Seed: 440 terms
2. Expansion: 440 × 50 = 22,000 raw candidates
3. Aggregation: Top 300 per topic = 1,500 candidates
4. Curation: Review 1,500 → ~400-600 final

**With smaller seed**:
1. Seed: 150-200 terms
2. Expansion: 150 × 50 = 7,500 raw candidates
3. Aggregation: Top 300 per topic = 1,500 candidates
4. Curation: Review 1,500 → ~400-600 final

**Advantage**: Smaller seed means less noise in expansion, easier curation

### 5. **Semantic Purity: Core Concepts Only**

**Large seed includes**:
- Core concepts: `slavernij`, `racisme`, `parlement`
- Morphological variants: `slavernijverleden`, `racistisch`, `parlementaire`
- Contextual combinations: `slavernijgeschiedenis`, `politiek debat`
- Administrative terms: `taalbeleid`, `wetgeving`

**Small seed should include**:
- ✅ Core concepts ONLY: `slavernij`, `racisme`, `parlement`
- ❌ NOT variants: SBERT finds these
- ❌ NOT combinations: SBERT finds these
- ❌ NOT administrative: Too generic, expansion should filter

---

## Proposed: Condensed Seed Dictionary

### **Target Size**: ~150-200 total terms (60% reduction)

**Per topic**: ~30-40 core terms instead of 70-110

### **Selection Criteria**

Keep only terms that are:

1. **Core semantic anchors** (NOT derivations)
   - ✅ `racisme` (NOT `racistisch`, `racisten`, `antiracisme`)
   - ✅ `slavernij` (NOT `slavernijverleden`, `slavernijperiode`, `slavernijgeschiedenis`)
   - ✅ `discriminatie` (NOT `discriminerend`, `discrimineren`)

2. **Conceptually distinct** (NOT morphological variants)
   - ✅ `racisme`, `discriminatie`, `uitsluiting` (different concepts)
   - ❌ `racisme`, `racistisch`, `racisten` (same concept, different forms)

3. **High semantic weight** (core to topic, NOT peripheral)
   - ✅ Keep: Weight 0.90-1.00 terms
   - ⚠️ Review: Weight 0.85 terms (keep if truly distinct)
   - ❌ Remove: Weight 0.70-0.80 terms (let expansion find these)

4. **Specific to topic** (NOT shared contextual filters)
   - ✅ Keep contextual filters in ALL topics (temporal/geographic)
   - ✅ Remove topic-specific low-weight terms
   - ✅ Focus on what makes each topic UNIQUE

---

## Condensed Seed: Topic-by-Topic

### **Social Fragmentation & Racism** (110 → 35 terms)

**KEEP (Core concepts, weight ≥ 0.90)**:
```
Core racial concepts (weight 1.00):
- racisme
- discriminatie
- kleur-hiërarchie
- raciale hiërarchie
- erfenis van slavernij

High-weight racial systems (0.90-0.95):
- slavernij
- segregatie
- kleurisme
- uitsluiting
- vooroordelen
- stereotypering
- plantage-maatschappij
- kastensysteem
- slavenhouders
- slaafgemaakten
- blanke privilege

Racial categorization (0.90-0.95):
- kleurscheidslijn
- sociale stratificatie
- huidskleur

Ideology (0.90+):
- structureel racisme
- institutioneel racisme
- doorwerking kleurdenken

NEW critical terms (0.90-0.95):
- slavenhandel (slave trade - racial commerce)
- neger (historical racial slur in documents)
- abolitionisten (racial liberation movement)
```

**REMOVE (Variants/derivatives that SBERT will find)**:
- ❌ `racistisch` (adjective of racisme)
- ❌ `discriminerend` (participle of discriminatie)
- ❌ `discrimineren` (verb of discriminatie)
- ❌ `uitsluiten` (verb of uitsluiting)
- ❌ `marginalisering` (similar to uitsluiting)
- ❌ `slavernijverleden` (slavernij + verleden - compound SBERT finds)
- ❌ `slavenhouder`, `slaveneigenaar` (singular/variants of slavenhouders)
- ❌ `vrijgemaakten`, `manumissie` (low weight 0.80-0.85, expansion finds)
- ❌ `kleurvooroordelen` (compound of kleur + vooroordelen)
- ❌ All 0.70-0.80 weight terms

**Rationale**: Keep 35 core distinct concepts, SBERT finds 300+ related terms

---

### **Governance Distrust & Corruption** (107 → 35 terms)

**KEEP (Core concepts, weight ≥ 0.90)**:
```
Core governance (1.00):
- corruptie
- wantrouwen

Colonial governance (0.90-0.95):
- gouverneur
- koloniaal bestuur
- koloniale overheid

NEW Parliamentary (0.90-0.95):
- parlement
- constitutie
- kabinet
- minister
- wetgeving
- afschaffing (political act)
- afschaffingsdebat

Power/control (0.90+):
- monopolie
- machtsmisbruik
- uitbuiting
- onderdrukking
- dwang
- willekeur
```

**REMOVE (Variants/combinations)**:
- ❌ `parlementaire`, `wetgevend`, `wetgever` (derivatives)
- ❌ `constitutionele`, `grondwet` (variants of constitutie)
- ❌ `hervormingen`, `hervorming` (generic, SBERT finds)
- ❌ `debat`, `politiek debat` (too generic, SBERT finds in context)
- ❌ `bestuur`, `bestuurlijk`, `bestuursorgaan` (governance duplicates)
- ❌ `regering`, `ministerraad` (cabinet duplicates)
- ❌ All colonial governance compounds (SBERT finds from koloniale + bestuur)

**Rationale**: 35 core political/governance concepts, expansion finds administrative variants

---

### **Educational Disadvantage & Brain Drain** (68 → 30 terms)

**KEEP (Core concepts, weight ≥ 0.90)**:
```
Core educational disadvantage (1.00):
- onderwijs-achterstand
- brain drain

Educational access (0.90-0.95):
- schooluitval
- onderwijskwaliteit
- onderwijsuitsluiting
- alfabetisering verbod
- beperkt onderwijs
- toegang tot onderwijs

Colonial education (0.90-0.95):
- koloniaal onderwijs
- koloniaal onderwijssysteem
- eurocentrisch curriculum
- taalonderdrukking
- moedertaal verbod
- Papiaments verbod
- Nederlandse taal opgelegd
- religieus monopolie

Brain drain (0.90-0.95):
- emigratie
- vertrek geschoolden
- niet terugkeren
```

**REMOVE (Low weight, variants, generic)**:
- ❌ `leerprestaties`, `analfabetisme`, `opleidingsniveau` (0.80-0.85, SBERT finds)
- ❌ `onderwijsdeelname`, `studie-uitval` (variants of schooluitval)
- ❌ `taal-barrière`, `taalachterstand` (0.85-0.95 but SBERT finds from taalonderdrukking)
- ❌ `katholiek onderwijs`, `missie-onderwijs` (specific of religieus monopolie)
- ❌ `koloniale canon`, `culturele dominantie` (SBERT finds from eurocentrisch)
- ❌ `lerarentekort`, `studeren in Nederland` (0.80, SBERT finds)
- ❌ `Papiaments`, `Papiamentu` (language names, not educational concepts)
- ❌ All generic historical/geographic terms (covered by contextual filters)

**Rationale**: 30 distinct educational concepts, SBERT expands to language/access variants

---

### **Persistent Poverty & Economic Vulnerability** (86 → 30 terms)

**KEEP (Core concepts, weight ≥ 0.90)**:
```
Core poverty (1.00):
- armoede
- werkloosheid

Economic vulnerability (0.90-0.95):
- schuld
- economische kwetsbaarheid
- afhankelijkheid
- economische crisis

Colonial economy (0.90-0.95):
- plantage-economie
- extractie
- monocultuur
- koloniale exploitatie
- slavernij-economie
- dwangarbeid
- handelsmonopolie

NEW trade (0.90-0.95):
- slavenhandel (if not in Social Fragmentation)
- handel
- wic
- exporteconomie
```

**REMOVE (Low weight, generic, derivatives)**:
- ❌ `inkomensongelijkheid`, `lage lonen`, `bestaanszekerheid` (0.85, SBERT finds)
- ❌ `koopkracht`, `levensonderhoud`, `sociale zekerheid` (0.75-0.80, too generic)
- ❌ `plantage`, `suikerplantages` (SBERT finds from plantage-economie)
- ❌ `slavenarbeid`, `exporteconomie` (SBERT finds from slavernij-economie/extractie)
- ❌ `compagnie`, `grondstoffen` (too generic)
- ❌ All structural/legacy terms (covered by contextual filters)

**Rationale**: 30 core economic concepts, SBERT finds poverty/trade variants

---

### **Structural Neglect & Infrastructure Gaps** (69 → 30 terms)

**KEEP (Core concepts, weight ≥ 0.90)**:
```
Core neglect (1.00):
- verwaarlozing
- achterstallig onderhoud

Infrastructure (0.90-0.95):
- infrastructuur
- publieke voorzieningen
- basisvoorzieningen

Colonial under-investment (0.90-0.95):
- koloniale onderinvestering
- extractieve economie
- gebrek aan investeringen
- beperkte ontwikkeling
```

**REMOVE (Low weight, generic)**:
- ❌ Most 0.70-0.85 terms (let SBERT find)
- ❌ Generic service terms (SBERT finds from publieke voorzieningen)
- ❌ Specific infrastructure (water, roads, etc. - too narrow)

**Rationale**: 30 core infrastructure/neglect concepts

---

## Summary: Condensed Seed Dictionary

### **Proposed Size**:
- **Social Fragmentation**: 110 → 35 (-68%)
- **Governance**: 107 → 35 (-67%)
- **Educational**: 68 → 30 (-56%)
- **Persistent Poverty**: 86 → 30 (-65%)
- **Structural Neglect**: 69 → 30 (-57%)
- **TOTAL**: 440 → 160 (-64%)

### **What We Remove**:
1. ❌ Morphological variants (adjectives, verbs, plurals)
2. ❌ Compound terms SBERT will find (slavernijverleden = slavernij + verleden)
3. ❌ Low-weight terms (0.70-0.80) - expansion handles these
4. ❌ Administrative/generic terms
5. ❌ Redundant similar concepts

### **What We Keep**:
1. ✅ Core semantic anchors (weight ≥ 0.90)
2. ✅ Conceptually distinct terms (not variants)
3. ✅ Contextual filters in ALL topics (temporal/geographic)
4. ✅ Topic-unique high-value terms
5. ✅ NEW critical missing terms (neger, parlementaire, kabinet, slavenhandel)

---

## Expected Benefits

### 1. **Better Expansion Quality**
- Fewer noisy seed terms = cleaner nearest-neighbor results
- High-weight seeds dominate = better semantic coherence
- SBERT finds natural variants = more corpus-grounded

### 2. **Stronger Weight Differentiation**
- 160 seed terms × 50 neighbors = 8,000 candidates
- Top 300 per topic = 1,500 total
- **Seed terms: ~10-15% of candidates** (vs ~30% now)
- Discovered terms more prominent, seed weights more meaningful

### 3. **Easier Curation**
- Smaller expansion = less noise to filter
- Core seeds are clear anchors = easier to evaluate relevance
- More consistent quality

### 4. **Fixes Core Issues**

**Chunk 34795144** (Uncle Tom's Cabin):
- Small seed with `racisme` (1.00), `slavernij` (0.95), `neger` (0.90), `abolitionisten` (0.90)
- SBERT finds: `racistisch`, `discriminerend`, `zwarte`, `afrikanen`
- **Result**: Social Fragmentation still captures racism, but through expansion not enumeration

**Chunk 195cdf4c** (Parliamentary debate):
- Small seed with `parlement` (0.90), `kabinet` (0.90), `constitutie` (0.90), `afschaffing` (0.90)
- SBERT finds: `parlementaire`, `hervormingen`, `wetgeving`, `debat`
- **Result**: Governance captures political content through core anchors + expansion

---

## Recommendation

### **Create a condensed seed dictionary**:

1. **Keep ONLY weight ≥ 0.90 terms** (+ select 0.85 if truly distinct)
2. **Remove all morphological variants**
3. **Remove compounds SBERT will find**
4. **Add 5-10 critical missing terms per topic** (neger, parlement, kabinet, slavenhandel)
5. **Target: 30-40 terms per topic = 150-200 total**

### **Trust SBERT expansion to**:
- Find morphological variants (racisme → racistisch)
- Find semantic neighbors (racisme → discriminatie)
- Find contextual uses (slavernij → slavernijverleden)
- Fill out the 300 candidates per topic

### **Benefits**:
- Semantically purer seed
- Better weight differentiation
- Easier curation
- Same or better final dictionary quality

**Bottom line**: You're right - **smaller, focused seed > large, exhaustive seed**.

