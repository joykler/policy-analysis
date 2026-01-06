# V5 Problem Chunks - Detailed Term Analysis

## Chunk 34795144: Uncle Tom's Cabin (Racism Discussion)

### **Text Content** (from previous analysis)

**Key phrases**:
- "woord 'neger' discriminerend en racistisch"
- Discussion of abolitionists
- Historical racism and slavery

**Expected primary topic**: Social Fragmentation & Racism

---

### **V4 Performance** ❌

**Scores**:
1. Educational: 0.455 [#1] ❌ WRONG PRIMARY
2. (unknown #2)
3. (unknown #3)
4. (unknown #4)
5. Social Fragmentation: 0.382 [#5] ❌ CORRECT TOPIC TOO LOW

**Why V4 failed**:

**Social Fragmentation dictionary MISSING**:
- ❌ `neger` (word explicitly mentioned in chunk)
- ❌ `racistisch` (word explicitly mentioned in chunk)
- ❌ `discriminerend` (word explicitly mentioned in chunk)
- ❌ `abolitionisten` (concept discussed in chunk)

**Social Fragmentation dictionary HAD** (assumed):
- ✓ `racisme` (noun)
- ✓ `discriminatie` (noun)
- ✓ `slavernij` (noun)

**Problem**: Chunk uses ADJECTIVAL and VERB forms, V4 dictionary has only NOUNS.

**Educational dictionary triggered because**:
- Likely had: `geschiedenis`, `historisch` (contextual filters)
- Likely had: Generic terms that match "Uncle Tom's Cabin" as literature/educational content

---

### **V5 Improvements** ✓

**Social Fragmentation seed (relevant terms)**:
- ✓ `neger` (1.00, weight 0.90) - EXACT MATCH
- ✓ `racisme` (1.00, weight 1.00) - BASE NOUN
- ✓ `discriminatie` (1.00, weight 1.00) - BASE NOUN
- ✓ `abolitionisten` (1.00, weight 0.90) - EXACT MATCH
- ✓ `slavernij` (1.00, weight 0.95)
- ✓ `slavenhandel` (1.00, weight 0.95)

**Social Fragmentation SBERT-discovered**:
- ✓ `racistisch` (0.921, weight 0.80) - EXACT MATCH (adjective from `racisme`)
- ✓ `discriminerend` (0.891, weight 0.80) - EXACT MATCH (participle from `discriminatie`)
- ✓ `racistische` (0.923, weight 0.80)
- ✓ `discrimineren` (0.933, weight 0.80)

**Educational improvements**:
- Condensed seed (68 → 35 terms)
- Removed generic educational terms
- Still has contextual filters (as intended)

---

### **Expected V5 Scoring for Chunk 34795144**

**Cosine similarity boost calculation** (simplified):

**Social Fragmentation**:
- Exact matches: `neger` (0.90), `racistisch` (0.80), `discriminerend` (0.80), `abolitionisten` (0.90)
- Related terms: `racisme` (1.00), `discriminatie` (1.00), `slavernij` (0.95)
- **Weighted cosine score**: Estimated 0.48-0.52 (high match on critical terms)

**Educational**:
- Contextual matches: `geschiedenis` (0.70), `historisch` (0.70)
- Some slavery terms: `slavernijgeschiedenis` (0.80)
- **Weighted cosine score**: Estimated 0.35-0.40 (generic historical context only)

**Expected ranking**:
1. Social Fragmentation: 0.48-0.52 ✓ CORRECT
2. (Possibly Governance or Educational: 0.36-0.40)
3-5. Other topics

**Margin**: 0.08-0.16 (good separation)

**Confidence**: HIGH (margin > 0.05)

**Result**: ✓ LIKELY FIXED - Social Fragmentation should rank #1

---

## Chunk 195cdf4c: Parliamentary Abolition Debate

### **Text Content** (from previous analysis)

**Key phrases**:
- "parlementaire hervormingen"
- "constitutionele hervormingen"
- "kabinet-Thorbecke II"
- "afschaffing slavernij"
- Discussion of political reforms and abolition

**Expected primary topic**: Governance Distrust & Corruption

---

### **V4 Performance** ❌

**Scores**:
1. Educational: 0.457 [#1] ❌ WRONG PRIMARY
2. (unknown #2)
3. Governance: 0.327 [#3] ❌ CORRECT TOPIC TOO LOW

**Why V4 failed**:

**Governance dictionary MISSING**:
- ❌ `parlement` / `parlementaire`
- ❌ `kabinet`
- ❌ `constitutie` / `constitutionele`
- ❌ `hervormingen`
- ❌ Possibly: `wetgeving`, `debat`

**Governance dictionary HAD** (assumed):
- ✓ `corruptie` (1.00)
- ✓ `wantrouwen` (1.00)
- ✓ `gouverneur` (0.95)
- ✓ Generic colonial governance terms

**Problem**: V4 had colonial governance vocabulary but LACKED parliamentary/constitutional vocabulary.

**Educational triggered because**:
- Had: `geschiedenis`, `afschaffing`, historical terms
- Chunk discusses historical political event → matched as historical/educational

---

### **V5 Improvements** ✓

**Governance seed (relevant terms)**:
- ✓ `parlement` (1.00, weight 0.90) - BASE NOUN
- ✓ `kabinet` (1.00, weight 0.90) - EXACT MATCH
- ✓ `constitutie` (1.00, weight 0.90) - BASE NOUN
- ✓ `wetgeving` (1.00, weight 0.90)
- ✓ `afschaffing` (1.00, weight 0.90) - EXACT MATCH (higher weight than V4)
- ✓ `minister` (1.00, weight 0.90)

**Governance SBERT-discovered**:
- ✓ `parlementen` (0.762, weight 0.80) - Plural
- ✓ `kabinetten` (0.727, weight 0.80) - Plural
- ✓ `wetgevend` (0.711, weight 0.80) - Adjective
- ✓ `debat` (0.736, weight 0.80)
- ✓ `wet` (0.842, weight 0.80)

**Governance STILL MISSING**:
- ❌ `parlementaire` (adjective - used in chunk)
- ❌ `constitutionele` (adjective - used in chunk)
- ❌ `hervormingen` (noun - used in chunk)

---

### **Expected V5 Scoring for Chunk 195cdf4c**

**Cosine similarity boost calculation**:

**Governance**:
- Exact matches: `kabinet` (0.90), `afschaffing` (0.90)
- Base noun matches: `parlement` (0.90), `constitutie` (0.90)
- Related discovered: `debat` (0.80), `wetgevend` (0.80)
- **Missing exact matches**: `parlementaire`, `constitutionele`, `hervormingen` ⚠️
- **Weighted cosine score**: Estimated 0.42-0.48

**Educational**:
- Contextual: `geschiedenis` (0.70), `afschaffing` (if in Educational)
- Generic historical: `historisch` (0.70)
- **Weighted cosine score**: Estimated 0.36-0.40

**Social Fragmentation**:
- Context: `slavernij` (0.95), `afschaffing` (0.85)
- **Weighted cosine score**: Estimated 0.38-0.42

**Expected ranking** (OPTIMISTIC):
1. Governance: 0.42-0.48 ✓ CORRECT
2. Social Fragmentation: 0.38-0.42
3. Educational: 0.36-0.40

**Expected ranking** (PESSIMISTIC - if adjectives heavily weighted in embedding):
1. Educational: 0.40-0.44 ❌
2. Governance: 0.42-0.46 ⚠️ CORRECT but not #1
3. Social Fragmentation: 0.38-0.42

**Margin**: 0.02-0.06 (moderate separation)

**Confidence**: LOW to MEDIUM (margin borderline)

**Result**: ⚠️ PARTIALLY FIXED - Governance will score higher but might not rank #1

**Why**: Chunk text uses `parlementaire` and `constitutionele` (adjectives), but V5 only has `parlement` and `constitutie` (nouns). SBERT embedding similarity between noun and adjective forms might not be high enough to get strong cosine match.

---

## Term-Level Comparison Table

### **Social Fragmentation: Chunk 34795144 Terms**

| Term in Chunk | V4 Dictionary | V5 Seed | V5 Expansion | Weight | Match Quality |
|---------------|---------------|---------|--------------|--------|---------------|
| neger | ❌ MISSING | ✓ YES | 1.00 | 0.90 | EXACT |
| racistisch | ❌ MISSING | ❌ NO | 0.921 | 0.80 | EXACT (discovered) |
| discriminerend | ❌ MISSING | ❌ NO | 0.891 | 0.80 | EXACT (discovered) |
| abolitionisten | ❌ MISSING | ✓ YES | 1.00 | 0.90 | EXACT |
| racisme | ✓ YES | ✓ YES | 1.00 | 1.00 | BASE NOUN |
| discriminatie | ✓ YES | ✓ YES | 1.00 | 1.00 | BASE NOUN |
| slavernij | ✓ YES | ✓ YES | 1.00 | 0.95 | BASE NOUN |

**V4 Match Rate**: 3/7 terms (43%) - Only base nouns
**V5 Match Rate**: 7/7 terms (100%) - All forms (nouns + adjectives + discovered)

**Improvement**: +57 percentage points

---

### **Governance: Chunk 195cdf4c Terms**

| Term in Chunk | V4 Dictionary | V5 Seed | V5 Expansion | Weight | Match Quality |
|---------------|---------------|---------|--------------|--------|---------------|
| parlementaire | ❌ MISSING | ❌ NO | ❌ MISSING | - | NO MATCH |
| hervormingen | ❌ MISSING | ❌ NO | ❌ MISSING | - | NO MATCH |
| constitutionele | ❌ MISSING | ❌ NO | ❌ MISSING | - | NO MATCH |
| kabinet | ❌ MISSING | ✓ YES | 1.00 | 0.90 | EXACT |
| afschaffing | ? UNKNOWN | ✓ YES | 1.00 | 0.90 | EXACT |
| parlement | ❌ MISSING | ✓ YES | 1.00 | 0.90 | BASE NOUN (chunk uses adj) |
| constitutie | ❌ MISSING | ✓ YES | 1.00 | 0.90 | BASE NOUN (chunk uses adj) |
| debat | ❌ MISSING | ❌ NO | 0.736 | 0.80 | DISCOVERED |

**V4 Match Rate**: 0-1/8 terms (0-12%) - Almost nothing
**V5 Match Rate**: 5/8 terms (62%) - Base nouns + some discovered

**Improvement**: +50-62 percentage points

**Remaining gap**: 3/8 critical terms still missing (parlementaire, constitutionele, hervormingen)

---

## Conclusion: V5 Impact Assessment

### **Chunk 34795144 (Racism)** - LIKELY FIXED ✓

**V4 → V5 Improvement**:
- Match rate: 43% → 100% (+57 points)
- All critical racial discourse terms now present
- SBERT successfully found morphological variants

**Expected outcome**:
- Social Fragmentation: #5 → #1 (rank improvement: +4)
- Score improvement: 0.382 → 0.48-0.52 (+0.10-0.14)
- Confidence: Unknown → HIGH (margin >0.05)

**Conclusion**: ✓ This chunk should be FIXED in V5.

---

### **Chunk 195cdf4c (Parliamentary Debate)** - PARTIALLY FIXED ⚠️

**V4 → V5 Improvement**:
- Match rate: 0-12% → 62% (+50-62 points)
- Core political nouns now present
- Some discovered terms (debat, wetgevend)

**Remaining issues**:
- Missing 3/8 critical terms (parlementaire, constitutionele, hervormingen)
- Chunk uses ADJECTIVES, V5 has NOUNS
- SBERT didn't discover Dutch adjective forms

**Expected outcome**:
- Governance: #3 → #1-2 (rank improvement: +1-2)
- Score improvement: 0.327 → 0.42-0.48 (+0.09-0.15)
- **Risk**: Might still rank #2 if adjectives are heavily weighted in chunk embedding

**Conclusion**: ⚠️ This chunk is IMPROVED but might not be fully fixed without adding `parlementaire`, `constitutionele`, `hervormingen` to seed.

---

## Recommendation: V5.1 Governance Additions

If testing shows Chunk 195cdf4c still ranks Governance #2-3:

**Add to Governance seed**:
```python
GOVERNANCE_V5_1_ADDITIONS = [
    ('parlementaire', 0.90),
    ('constitutionele', 0.90),
    ('hervormingen', 0.85),
    ('hervorming', 0.85),
]
```

**Expected impact**:
- Match rate: 62% → 100% (+38 points)
- Governance score: 0.42-0.48 → 0.50-0.56 (+0.08-0.10)
- Should guarantee Governance ranks #1

**Decision point**: Test V5 first, create V5.1 only if empirical results show Governance still underperforming.
