# V5 vs V4 Dictionary Comparison Analysis

## Executive Summary

**V5 represents a MAJOR improvement over V4**:
- Condensed seed dictionary: 377 → 188 terms (-50%)
- Critical missing vocabulary ADDED to seed
- Better expansion quality with SBERT finding morphological variants
- Governance and Social Fragmentation now have the missing political and racial terms

---

## Seed Dictionary Changes

### **Size Reduction: 377 → 188 terms (-50%)**

**V4 Seed (377 terms)**:
- Social Fragmentation: 110 terms
- Governance: 107 terms
- Educational: 68 terms
- Persistent Poverty: 86 terms
- Structural Neglect: 69 terms (assumed based on total)

**V5 Seed (188 terms)**:
- Social Fragmentation: 46 terms (-58%)
- Governance: 41 terms (-62%)
- Educational: 35 terms (-49%)
- Persistent Poverty: 36 terms (-58%)
- Structural Neglect: 30 terms (-57%)

**Strategy**: Condensed to core semantic anchors (weight ≥0.85-0.90), removed morphological variants, let SBERT expansion find related terms.

### **Weight Distribution Improvement**

**V4 Seed Weights**:
```
Weight   Count   %
0.70-0.80:  ~120   32%
0.85:       ~75    20%
0.90-1.00:  ~180   48%
```

**V5 Seed Weights**:
```
Weight   Count   %
0.70:      10     5%
0.75:       6     3%
0.80:       2     1%
0.85:      55    29%
0.90:      69    37%
0.95:      33    18%
1.00:      13     7%
```

**Improvement**: V5 has 91% terms at weight ≥0.85 vs V4's ~68%. Higher quality seed with core concepts prioritized.

---

## Critical Terms Added to V5 Seed

### **Social Fragmentation & Racism**

**ADDED (present in v5 seed)**:
- `neger` (0.90) - Historical racial slur discussed in documents
- `slavenhandel` (0.95) - Slave trade as racial commerce
- `abolitionisten` (0.90) - Abolition movement (racial liberation)

**STILL MISSING from seed** (but SBERT might find):
- `racistisch` - Adjectival form of racisme
- `discriminerend` - Present participle of discriminatie

### **Governance Distrust & Corruption**

**ADDED (present in v5 seed)**:
- `parlement` (0.90) - Parliament
- `kabinet` (0.90) - Cabinet
- `constitutie` (0.90) - Constitution
- `wetgeving` (0.90) - Legislation

**Expected SBERT expansions**:
- `parlementaire`, `hervormingen`, `debat` - SBERT should find from seed terms

---

## Expansion Quality Comparison

### **V5 Social Fragmentation Expansion (top 50)**

**Critical terms SUCCESSFULLY expanded**:

**Seed terms (weight from seed)**:
1. `discriminatie` (1.00, weight 1.00) - SEED
2. `slavernijverleden` (1.00, weight 0.90) - SEED
3. `slavernij` (1.00, weight 0.95) - SEED
4. `racisme` (1.00, weight 1.00) - SEED
5. `segregatie` (1.00, weight 0.95) - SEED
6. `afschaffing` (1.00, weight 0.85) - SEED
7. `slavenhandel` (1.00, weight 0.95) - SEED ✓ **NEW**
8. `abolitionisten` (1.00, weight 0.90) - SEED ✓ **NEW**
9. `neger` (1.00, weight 0.90) - SEED ✓ **NEW**

**SBERT discovered morphological variants** (weight 0.80):
- `racistische` (0.923, weight 0.80) - DISCOVERED from `racisme`
- `racistisch` (0.921, weight 0.80) - DISCOVERED from `racisme` ✓
- `discrimineren` (0.933, weight 0.80) - DISCOVERED from `discriminatie`
- `discriminerend` (0.891, weight 0.80) - DISCOVERED from `discriminatie` ✓
- `discriminerende` (0.870, weight 0.80)
- `discriminatiezaken` (0.873, weight 0.80)
- `gediscrimineerd` (0.852, weight 0.80)
- `abolitionists` (0.924, weight 0.80) - English variant
- `abolitionistisch` (0.858, weight 0.80)
- `slavenhandelaren` (0.892, weight 0.80)
- `slavenhouder` (0.891, weight 0.80) - Singular form

**Result**: The condensed seed strategy WORKED perfectly. SBERT found `racistisch` and `discriminerend` (the missing adjectives) automatically from the core nouns `racisme` and `discriminatie`.

---

### **V5 Governance Expansion (top 50)**

**Seed terms (weight from seed)**:
1. `corruptie` (1.00, weight 1.00) - SEED
2. `wantrouwen` (1.00, weight 1.00) - SEED
3. `minister` (1.00, weight 0.90) - SEED
4. `monopolie` (1.00, weight 0.95) - SEED
5. `afschaffing` (1.00, weight 0.90) - SEED ✓ **Higher weight for political act**
6. `constitutie` (1.00, weight 0.90) - SEED ✓ **NEW**
7. `kabinet` (1.00, weight 0.90) - SEED ✓ **NEW**
8. `parlement` (1.00, weight 0.90) - SEED ✓ **NEW**
9. `wetgeving` (1.00, weight 0.90) - SEED ✓ **NEW**

**SBERT discovered political variants** (weight 0.80):
- `parlementen` (0.762, weight 0.80) - Plural
- `kabinetten` (0.727, weight 0.80) - Plural
- `wetgevend` (0.711, weight 0.80) - Adjectival form ✓
- `debat` (0.736, weight 0.80) - Political debates ✓
- `wet` (0.842, weight 0.80) - Law (related to wetgeving)

**MISSING**:
- `hervormingen` / `hervorming` - NOT found in expansion
- `parlementaire` - NOT found in expansion (only plural `parlementen`)
- `constitutionele` - NOT found in expansion

**Partial success**: SBERT found some political vocabulary but missed key adjectival forms like `parlementaire` and `constitutionele`. These might need to be added to seed.

---

### **V5 Educational Expansion (top 50)**

**Still contains contextual filters** (as intended):
- `geschiedenis` (1.00, weight 0.70) - Historical filter
- `slavernijverleden` (1.00, weight 0.90) - Slavery period filter
- `destijds` (1.00, weight 0.75) - Temporal filter
- `historisch` (1.00, weight 0.70) - Historical filter

**Educational-specific terms**:
- `schooluitval` (1.00, weight 0.90) - SEED
- `onderwijskwaliteit` (1.00, weight 0.90) - SEED
- `emigratie` (1.00, weight 0.95) - Brain drain SEED

**Observation**: Educational still has many historical/slavery compound terms in expansion:
- `slavernijgeschiedenis` (0.941)
- `slavernijgeschiedenissen` (0.927)
- `slavernijverhaal` (0.872)
- `slavernijgerelateerde` (0.799)
- `slavernijdebat` (0.763)

**These are DISCOVERED terms** (weight 0.80), not seed terms. SBERT is finding them from the combination of:
- `slavernij` / `slavernijverleden` (contextual filter)
- `geschiedenis` (contextual filter)
- Educational-specific seed terms

**Question**: Do these historical slavery compounds belong in Educational? They might trigger on any historical slavery discussion rather than actual educational content.

---

## Key Improvements in V5

### **1. SBERT Morphological Variant Discovery Works**

**Proof**:
- Seed: `racisme` (noun) → SBERT found: `racistisch`, `racistische` (adjectives)
- Seed: `discriminatie` (noun) → SBERT found: `discriminerend`, `discrimineren` (verb/participle)
- Seed: `wetgeving` (noun) → SBERT found: `wetgevend` (adjective)

**This validates the condensed seed strategy**: Don't manually enumerate variants, let SBERT find them.

### **2. Critical Missing Terms Now Present**

**V4 problems FIXED in V5**:

**Problem: Chunk 34795144 (Uncle Tom's Cabin racism)** - Educational ranked #1, Social Fragmentation ranked #5

**V4 Social Fragmentation** lacked:
- `neger` (slur discussed in chunk) ❌
- `racistisch` (adjective used in chunk) ❌
- `discriminerend` (participle used in chunk) ❌
- `abolitionisten` (discussed in chunk) ❌

**V5 Social Fragmentation** now has:
- `neger` (1.00, weight 0.90) ✓ SEED
- `racistisch` (0.921, weight 0.80) ✓ DISCOVERED
- `discriminerend` (0.891, weight 0.80) ✓ DISCOVERED
- `abolitionisten` (1.00, weight 0.90) ✓ SEED

**Expected impact**: Social Fragmentation should now rank #1-2 instead of #5.

---

**Problem: Chunk 195cdf4c (Parliamentary abolition debate)** - Educational ranked #1, Governance ranked #3

**V4 Governance** lacked:
- `parlement` / `parlementaire` ❌
- `kabinet` ❌
- `constitutie` / `constitutionele` ❌
- `wetgeving` ❌
- `hervormingen` ❌

**V5 Governance** now has:
- `parlement` (1.00, weight 0.90) ✓ SEED
- `kabinet` (1.00, weight 0.90) ✓ SEED
- `constitutie` (1.00, weight 0.90) ✓ SEED
- `wetgeving` (1.00, weight 0.90) ✓ SEED
- `debat` (0.736, weight 0.80) ✓ DISCOVERED
- `wetgevend` (0.711, weight 0.80) ✓ DISCOVERED

**Still missing**:
- `parlementaire` (adjectival form) ⚠️
- `constitutionele` (adjectival form) ⚠️
- `hervormingen` (reforms) ⚠️

**Expected impact**: Governance should score higher, but might still be sub-optimal without `parlementaire` and `hervormingen`.

---

### **3. Weight Distribution More Focused**

**V5 Expansion Weight Distribution**:

**Social Fragmentation**:
- Weight 1.00: 11 terms (core seed concepts)
- Weight 0.95: 2 terms
- Weight 0.90: 4 terms
- Weight 0.85: 2 terms
- Weight 0.80: 281 terms (DISCOVERED)

**Governance**:
- Weight 1.00: 13 terms (core seed concepts)
- Weight 0.95: 3 terms
- Weight 0.90: 9 terms ✓ **More high-weight seeds than V4**
- Weight 0.85: 2 terms
- Weight 0.80: 273 terms (DISCOVERED)

**Improvement**: V5 has MORE high-weight (0.90+) terms in seed, providing stronger semantic anchors for scoring.

---

## Remaining Issues

### **1. Missing Adjectival Forms in Governance**

**Problem**: Chunk 195cdf4c uses `parlementaire` and `constitutionele`, but V5 expansion only has:
- `parlement` (noun) ✓
- `parlementen` (plural) ✓
- `constitutie` (noun) ✓

**Missing**:
- `parlementaire` (adjectival "parliamentary")
- `constitutionele` (adjectival "constitutional")
- `hervormingen` (reforms - noun)

**Why SBERT didn't find them**:
- Dutch adjectives from nouns (`parlement` → `parlementaire`) may have lower cosine similarity than English equivalents
- SBERT k=50 nearest neighbors might not include these if other slavery/governance terms are closer

**Recommendation**: Add to seed:
```
Governance seed additions:
- parlementaire (0.90)
- constitutionele (0.90)
- hervormingen (0.85)
- hervorming (0.85)
```

### **2. Educational Still Has Generic Historical Compounds**

**Observation**: V5 Educational expansion includes:
- `slavernijgeschiedenis` (0.941)
- `slavernijdebat` (0.763)
- `slavernijonderzoek` (0.763)
- `slavernijcomplex` (0.738)

**These are DISCOVERED** (weight 0.80), not seed. SBERT is combining:
- Contextual filter: `slavernijverleden`
- Contextual filter: `geschiedenis`
- Educational seeds: `schooluitval`, `onderwijskwaliteit`

**Question**: Should `slavernijdebat` be in Educational or Governance? Should `slavernijgeschiedenis` trigger Educational scoring?

**Recommendation**: During curation, carefully review these compounds to ensure they're truly educational-specific, not just historical/political content about slavery.

---

## Curation Quality (If Available)

Let me check if V5 has a curated dictionary...

---

## Summary: V5 Improvements Over V4

### **Definite Improvements** ✓

1. **Condensed seed (188 vs 377 terms)**: Higher quality, focused on core concepts
2. **Critical racial terms added to Social Fragmentation**: `neger`, `slavenhandel`, `abolitionisten`
3. **Critical political terms added to Governance**: `parlement`, `kabinet`, `constitutie`, `wetgeving`
4. **SBERT morphological discovery validated**: Found `racistisch`, `discriminerend`, `wetgevend` from base nouns
5. **Weight distribution improved**: 91% of seed terms at weight ≥0.85 (vs ~68% in V4)
6. **Better semantic anchors**: More high-weight (0.90+) terms provide stronger topic signals

### **Partial Improvements** ⚠️

1. **Governance political vocabulary**: Has core nouns (`parlement`, `kabinet`) but missing key adjectives (`parlementaire`, `constitutionele`, `hervormingen`)
2. **Educational historical compounds**: Still has many `slavernij*` compounds in expansion, needs careful curation

### **Expected Impact on Problem Chunks**

**Chunk 34795144 (Uncle Tom's Cabin racism)**:
- V4: Social Fragmentation rank #5 (0.382)
- V5 expected: Social Fragmentation rank #1-2 (estimated 0.45-0.50)
- Reason: Added `neger`, `abolitionisten` to seed; SBERT found `racistisch`, `discriminerend`

**Chunk 195cdf4c (Parliamentary abolition debate)**:
- V4: Governance rank #3 (0.327)
- V5 expected: Governance rank #1-2 (estimated 0.42-0.46)
- Reason: Added `parlement`, `kabinet`, `wetgeving`, `afschaffing` to seed
- **BUT**: Still missing `parlementaire`, `hervormingen` might limit improvement

### **Next Steps**

1. **Check if V5 has curated dictionary** - compare curation quality to V4
2. **Test on same 14 sample chunks** - validate expected ranking improvements
3. **Consider final seed refinements**:
   - Add `parlementaire`, `constitutionele`, `hervormingen` to Governance seed
   - Possibly add `racistisch`, `discriminerend` explicitly to Social (instead of relying on SBERT)
4. **Careful Educational curation** - review `slavernij*` compounds during curation

---

## Conclusion

**V5 represents a strategic improvement over V4**:
- Smaller, higher-quality seed dictionary
- Critical missing vocabulary addressed
- SBERT expansion strategy validated
- Expected to fix the cosine labeling problems identified in V4

**The condensed seed + SBERT expansion approach is working as intended**.
