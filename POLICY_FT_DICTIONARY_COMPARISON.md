# Policy Fine-tuned Dictionary Comparison

## Overview

This analysis compares the **Policy_Slavdict_FT-slavery_slavery_v1** expanded dictionary against:
1. Previous slavery-only dictionaries (v9)
2. Manual seed dictionaries
3. The intended slavery legacy topics

---

## Dictionary Characteristics

### Policy-Based FT Dictionary (NEW)
- **Source Corpus**: Policy documents (parliamentary proceedings, government reports)
- **Encoder**: Fine-tuned on slavery historical corpus
- **Structure**: 1,200 terms (300 per topic)
- **Topics**: 4 contemporary legacy problems
- **Key Feature**: Domain transfer - slavery encoder applied to policy language

### Slavery-Based v9 Dictionary (PREVIOUS)
- **Source Corpus**: Historical slavery texts
- **Encoder**: Pre-trained on slavery corpus
- **Structure**: 1,200 terms (300 per topic)
- **Topics**: Same 4 legacy problems
- **Key Feature**: Direct extraction from slavery discourse

### Manual Seed Dictionary
- **Source**: Hand-curated by domain experts
- **Structure**: 167 terms total (39-45 per topic)
- **Purpose**: High-precision anchor terms
- **Key Feature**: Weighted by relevance category

---

## Topic-by-Topic Comparison

### 1. Educational Disadvantage & Brain Drain

#### Overlap Statistics
- **Policy terms**: 300
- **Slavery terms**: 300
- **Seed terms**: 45
- **Policy-Slavery overlap**: 124 terms (41.3%)

#### Unique Policy Contributions
High-weight terms ONLY in policy dictionary:
- `onderwijsachterstand` (education disadvantage) - df=2, weight=1.00
- `taalbarri�re` (language barrier) - df=2, weight=0.95
- `taalonderwijs` (language education) - df=4, weight=0.90
- `schoolse` (school-related) - df=11, weight=0.90

#### Unique Slavery Contributions
- `emigratie` (emigration) - df=4, weight=0.95
- `papiamentu` (Papiamentu language) - df=6, weight=0.90

#### Document Frequency Profile (Policy Dictionary)
- Terms appearing 10+ times: 116/300 (38.7%)
- Terms appearing 50+ times: 40/300 (13.3%)
- Terms appearing 100+ times: 30/300 (10.0%)

**Most frequent**: `onderwijs` (education, df=1,486)

#### Assessment
The policy dictionary captures **contemporary policy language** about education:
- Uses exact policy terminology (`onderwijsachterstand`)
- Includes bureaucratic/administrative language
- More grounded in actual policy discourse (higher df for core terms)
- Missing some historical/cultural terms (`emigratie`, `papiamentu`)

---

### 2. Governance Distrust & Corruption

#### Overlap Statistics
- **Policy-Slavery overlap**: 127 terms (42.3%)

#### Unique Policy Contributions
- `zelfbeschikking` (self-determination) - df=8, weight=0.90

#### Unique Slavery Contributions
High-weight terms missing from policy:
- `wantrouwen` (distrust) - **df=10, weight=1.00** ⚠️ Core concept!
- `nepotisme` (nepotism) - df=2, weight=0.95
- `patronage` (patronage) - df=3, weight=0.95
- `constitutie` (constitution) - df=7, weight=0.90

#### Document Frequency Profile
- Terms appearing 10+ times: 145/300 (48.3%)
- Terms appearing 50+ times: 75/300 (25.0%)
- Terms appearing 100+ times: 47/300 (15.7%)

**Most frequent**: `kamer` (chamber/parliament, df=11,648)

#### Assessment
**Critical gap**: The policy dictionary **misses "wantrouwen" (distrust)** - a core concept in the topic name!
- Policy dictionary focuses on institutional terms (`ministerie`, `kabinet`, `regering`)
- Slavery dictionary captures the **affective/psychological dimensions** (`wantrouwen`, `nepotisme`)
- Policy corpus may not explicitly discuss "distrust" as a framing

---

### 3. Persistent Poverty & Economic Vulnerability

#### Overlap Statistics
- **Policy-Slavery overlap**: 110 terms (36.7%) - **lowest overlap**

#### Unique Policy Contributions
- `armoedecijfers` (poverty statistics) - df=3, weight=0.90

#### Unique Slavery Contributions
- `slavenhandel` (slave trade) - df=249, weight=0.90

#### Document Frequency Profile
- Terms appearing 10+ times: 122/300 (40.7%)
- Terms appearing 50+ times: 53/300 (17.7%)
- Terms appearing 100+ times: 34/300 (11.3%)

**Most frequent**: `financi�le` (financial, df=2,656), `economische` (economic, df=1,343)

#### Assessment
- Policy dictionary emphasizes **contemporary economic administration** (`financi�le`, `economische`)
- Missing explicit historical linkages (`slavenhandel` only in slavery dict)
- Focus on measurement (`armoedecijfers`) vs. causal mechanisms

---

### 4. Social Fragmentation & Racism

#### Overlap Statistics
- **Policy-Slavery overlap**: 109 terms (36.3%) - **lowest overlap**

#### Unique Policy Contributions
- Very few high-weight unique terms

#### Unique Slavery Contributions
**Major gap** - many core racism terms missing from policy:
- `neger` (n-word) - **df=17, weight=1.00**
- `racistisch` (racist) - **df=21, weight=0.95**
- `racist` (racist) - df=2, weight=0.95
- `raciale` (racial) - **df=28, weight=0.90**
- `raciaal` (racial) - df=5, weight=0.90
- `rassendiscriminatie` (racial discrimination) - df=4, weight=0.90
- `verdeeldheid` (division/fragmentation) - df=5, weight=0.95
- `huidskleur` (skin color) - **df=33, weight=0.90**
- `discrimineren` (to discriminate) - df=12, weight=0.90

#### Document Frequency Profile
- Terms appearing 10+ times: 155/300 (51.7%) - **highest**
- Most frequent: `caribisch` (Caribbean, df=1,202)

#### Assessment
**Critical vocabulary gap**: The policy dictionary is **missing explicit racism terminology**!
- Policy discourse may avoid direct terms like `neger`, `racist`, `huidskleur`
- Focuses on institutional/geographic terms (`caribisch`, `bonaire`, `cura�ao`)
- **Euphemistic language**: Policy may discuss racism through proxy terms

---

## Key Findings

### 1. Domain Transfer Success
✅ **Successfully captures policy language**: Terms like `onderwijsachterstand`, `taalbarri�re`, `armoedecijfers` show the encoder learned policy-specific vocabulary

✅ **High document frequency**: Many terms appear 10+ times, indicating they're grounded in actual policy discourse, not noise

### 2. Critical Gaps

⚠️ **Missing affective/psychological terms**:
- `wantrouwen` (distrust) - core to "Governance Distrust"
- `verdeeldheid` (fragmentation) - core to "Social Fragmentation"

⚠️ **Missing explicit racism vocabulary**:
- `racist`, `racistisch`, `raciale`, `raciaal`
- `neger`, `huidskleur`
- `rassendiscriminatie`

⚠️ **Missing historical linkage terms**:
- `slavenhandel` (despite being in seed dictionary)

### 3. Vocabulary Euphemization

The policy dictionary shows signs of **institutional euphemization**:
- Focuses on administrative/bureaucratic language
- Avoids explicit terms for sensitive topics (racism, distrust)
- Uses geographic/institutional proxies (`caribisch`, `ministerie`)

This reflects how **policy language differs from academic/historical discourse about the same problems**.

### 4. Complementarity Pattern

**Low overlap (36-42%)** suggests the two dictionaries are **complementary**:
- **Policy dict**: Contemporary administrative/institutional language
- **Slavery dict**: Explicit problem framing, historical causation, affective dimensions

---

## Semantic Quality Examples

### Strong Policy Terms
1. `onderwijsachterstand` - Exact term used in policy documents for education gaps
2. `lerarentekort` - Teacher shortage, specific policy concern
3. `armoedecijfers` - Poverty statistics, measurement focus
4. `zelfbeschikking` - Self-determination, constitutional language

### Missing Critical Terms
1. `wantrouwen` (distrust) - **Core concept not captured**
2. `nepotisme` (nepotism) - Specific governance problem
3. `neger` - Historical slur still discussed in legacy contexts
4. `rassendiscriminatie` - Explicit framing of racial discrimination
5. `verdeeldheid` - Social division/fragmentation

### Noise/Weak Terms
Based on low df but moderate cosine:
- Many geographic terms with moderate-low cosine (0.6-0.7)
- Generic administrative terms (`kamer`, `wet`) with low cosine

---

## Recommendations

### For Classification Tasks

**Option 1: Merged Dictionary** (Recommended for comprehensive coverage)
- Combine policy + slavery dictionaries
- Use union of terms to capture both administrative and explicit problem language
- Weight policy terms higher when scoring policy documents
- Weight slavery terms higher when detecting historical causation

**Option 2: Hierarchical Approach**
- Use policy dictionary for **first-pass identification** (what policies discuss)
- Use slavery dictionary for **causal attribution** (why these problems exist)
- Flag documents that use policy language but lack historical framing

### For Dictionary Refinement

**Add missing core terms manually**:
1. `wantrouwen` → Governance topic
2. `verdeeldheid` → Social Fragmentation topic
3. Explicit racism terms → Social Fragmentation topic
4. `slavenhandel` → Economic Vulnerability topic

**Investigate low-df high-weight terms**:
- `onderwijsachterstand` (df=2) - might be too rare despite being perfect term
- Consider lowering weight threshold for policy-specific jargon

### For Future Iterations

**Create domain-specific encoders**:
- Fine-tune separate encoders for policy vs. historical texts
- Use ensemble predictions to capture different discourse styles
- Experiment with weighted combinations based on document source

---

## Conclusion

The Policy_Slavdict_FT-slavery_slavery_v1 dictionary successfully captures **contemporary policy language** about slavery legacy problems, but exhibits **vocabulary euphemization** typical of official discourse.

**Key insight**: Policy documents discuss these problems using **institutional and administrative language** rather than explicit problem framing. The low overlap with slavery-based dictionaries (36-42%) reflects genuine differences in discourse style, not encoder failure.

**Actionable**: For comprehensive topic identification in policy documents, a **merged dictionary** combining both policy and slavery vocabularies will provide the most robust coverage, capturing both how policy discusses these issues AND the underlying problems being addressed.

The missing "distrust" and racism terminology is particularly concerning for classification accuracy - these represent **semantic blind spots** where the policy corpus may not explicitly name the problems it's trying to address.
