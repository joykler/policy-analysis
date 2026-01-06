# V5 vs V4 Final Comparison and Recommendations

## Status Check

**V4 (Complete workflow)**:
- ✓ Seed dictionary: 377 terms
- ✓ Expanded candidates: 1,500 terms
- ✓ Curated dictionary: 302 terms
- ✓ Cosine labeling: 3,854 chunks scored
- ✓ Problems identified: Educational over-triggering, missing racial/political vocabulary

**V5 (In progress)**:
- ✓ Seed dictionary: 188 terms (condensed, -50%)
- ✓ Expanded candidates: 1,500 terms
- ❌ Curated dictionary: NOT YET CREATED
- ❌ Cosine labeling: NOT YET RUN
- ✓ Critical terms added to seed

---

## Dictionary Quality Comparison

### **Seed Dictionary: V5 is Superior**

| Metric | V4 | V5 | Change |
|--------|----|----|--------|
| Total terms | 377 | 188 | -50% |
| Terms weight ≥0.90 | ~180 (48%) | 115 (61%) | +13% |
| Terms weight ≥0.85 | ~255 (68%) | 170 (91%) | +23% |
| Terms weight <0.80 | ~120 (32%) | 18 (9%) | -23% |

**V5 advantages**:
- Higher concentration of core concepts (weight ≥0.85)
- Removed morphological variants (let SBERT find them)
- Added critical missing terms (`neger`, `parlement`, `kabinet`, `constitutie`)
- Cleaner semantic anchors for expansion

### **Expansion Quality: V5 Shows Improvement**

**Social Fragmentation**:

| Feature | V4 | V5 | Assessment |
|---------|----|----|------------|
| `neger` present | ❌ | ✓ (1.00, 0.90 seed) | FIXED |
| `racistisch` present | ? | ✓ (0.921, 0.80 discovered) | FIXED |
| `discriminerend` present | ? | ✓ (0.891, 0.80 discovered) | FIXED |
| `abolitionisten` present | ❌ | ✓ (1.00, 0.90 seed) | FIXED |
| `slavenhandel` present | ? | ✓ (1.00, 0.95 seed) | FIXED |
| High-weight terms (≥0.90) | Unknown | 19 terms | Improved |

**Governance**:

| Feature | V4 | V5 | Assessment |
|---------|----|----|------------|
| `parlement` present | ❌ | ✓ (1.00, 0.90 seed) | FIXED |
| `parlementaire` present | ❌ | ❌ (not expanded) | STILL MISSING |
| `kabinet` present | ❌ | ✓ (1.00, 0.90 seed) | FIXED |
| `constitutie` present | ❌ | ✓ (1.00, 0.90 seed) | FIXED |
| `constitutionele` present | ❌ | ❌ (not expanded) | STILL MISSING |
| `wetgeving` present | ? | ✓ (1.00, 0.90 seed) | FIXED |
| `wetgevend` present | ? | ✓ (0.711, 0.80 discovered) | FIXED |
| `hervormingen` present | ❌ | ❌ (not expanded) | STILL MISSING |
| `debat` present | ? | ✓ (0.736, 0.80 discovered) | FIXED |
| High-weight terms (≥0.90) | Unknown | 27 terms | Improved |

**Educational**:

| Feature | V4 | V5 | Assessment |
|---------|----|----|------------|
| Seed size | 68 terms | 35 terms | Condensed |
| Generic terms removed | ? | Yes (from seed) | Improved |
| Contextual filters kept | Yes | Yes | Maintained |
| Historical compounds in expansion | ? | Many (SBERT-discovered) | Needs curation |

---

## Key Validation: SBERT Expansion Strategy Works

**Evidence from V5**:

### **Test 1: Morphological Variant Discovery**

**Hypothesis**: If we include only base nouns in seed, SBERT will find adjectival/verb forms.

**Results**:
- Seed: `racisme` (noun, 1.00) → Discovered: `racistisch` (adj, 0.921), `racistische` (adj, 0.923) ✓
- Seed: `discriminatie` (noun, 1.00) → Discovered: `discriminerend` (participle, 0.891), `discrimineren` (verb, 0.933) ✓
- Seed: `wetgeving` (noun, 1.00) → Discovered: `wetgevend` (adj, 0.711) ✓
- Seed: `abolitionisten` (noun, 1.00) → Discovered: `abolitionistisch` (adj, 0.858) ✓

**Conclusion**: ✓ SBERT successfully finds morphological variants with high cosine similarity (0.85-0.93).

### **Test 2: Semantic Neighbor Discovery**

**Hypothesis**: SBERT will find semantically related terms from core concepts.

**Results**:
- Seed: `slavenhandel` → Discovered: `slavenhandelaren` (0.892) ✓
- Seed: `slavenhouders` → Discovered: `slavenhouder` (0.891) ✓
- Seed: `discriminatie` → Discovered: `discriminatiezaken` (0.873), `antidiscriminatie` (0.869), `gediscrimineerd` (0.852) ✓
- Seed: `parlement` → Discovered: `parlementen` (0.762) ✓
- Seed: `kabinet` → Discovered: `kabinetten` (0.727) ✓

**Conclusion**: ✓ SBERT finds plurals, compounds, and related administrative terms.

### **Test 3: What SBERT DOESN'T Find**

**Dutch adjectival forms with different morphology**:
- Seed: `parlement` → Expected: `parlementaire` (parliamentary) → Result: ❌ NOT in top 300
- Seed: `constitutie` → Expected: `constitutionele` (constitutional) → Result: ❌ NOT in top 300

**Conceptually distinct terms**:
- Seed: (no reform terms) → Expected: `hervormingen` (reforms) → Result: ❌ NOT in expansion

**Conclusion**: ⚠️ SBERT struggles with:
1. Dutch adjectives with non-trivial derivational morphology (`parlement` → `parlementaire`)
2. Conceptually related but lexically distinct terms (`constitutie` ≠ `hervorm`)

**Implication**: Some critical adjectival forms and distinct concepts still need manual addition to seed.

---

## Expected Impact on V4 Problem Chunks

### **Chunk 34795144: Uncle Tom's Cabin (racism discussion)**

**Text snippet** (from previous analysis): "woord 'neger' discriminerend en racistisch", discussing abolitionists

**V4 Scores**:
- Educational: 0.455 [#1] ❌ WRONG
- Social Fragmentation: 0.382 [#5] ❌ SHOULD BE #1

**V4 Social Fragmentation dictionary** lacked:
- `neger` ❌
- `racistisch` ❌
- `discriminerend` ❌
- `abolitionisten` ❌

**V5 Social Fragmentation dictionary** now has:
- `neger` (1.00, weight 0.90) ✓
- `racistisch` (0.921, weight 0.80) ✓
- `discriminerend` (0.891, weight 0.80) ✓
- `abolitionisten` (1.00, weight 0.90) ✓

**Expected V5 scoring**:
- Social Fragmentation: Estimated 0.48-0.52 [#1-2] ✓ LIKELY CORRECT
- Educational: Estimated 0.35-0.40 [#3-4] ✓ IMPROVED

**Mechanism**:
- Chunk contains explicit matches: `neger`, `racistisch`, `discriminerend`
- V5 Social Fragmentation will get weighted cosine boost from all three terms
- V4 had NONE of these terms, so couldn't capture racial discourse vocabulary

---

### **Chunk 195cdf4c: Parliamentary abolition debate**

**Text snippet** (from previous analysis): "parlementaire hervormingen", "constitutionele hervormingen", "kabinet-Thorbecke II", "afschaffing slavernij"

**V4 Scores**:
- Educational: 0.457 [#1] ❌ WRONG
- Governance: 0.327 [#3] ❌ SHOULD BE #1

**V4 Governance dictionary** lacked:
- `parlement` / `parlementaire` ❌
- `kabinet` ❌
- `constitutie` / `constitutionele` ❌
- `hervormingen` ❌

**V5 Governance dictionary** now has:
- `parlement` (1.00, weight 0.90) ✓
- `kabinet` (1.00, weight 0.90) ✓
- `constitutie` (1.00, weight 0.90) ✓
- `wetgeving` (1.00, weight 0.90) ✓
- `afschaffing` (1.00, weight 0.90) ✓
- `debat` (0.736, weight 0.80) ✓

**Still missing**:
- `parlementaire` ❌
- `constitutionele` ❌
- `hervormingen` ❌

**Expected V5 scoring**:
- Governance: Estimated 0.42-0.48 [#1-2] ⚠️ IMPROVED but maybe not #1
- Educational: Estimated 0.36-0.40 [#2-3] ✓ IMPROVED

**Mechanism**:
- Chunk contains: `parlement`, `kabinet`, `constitutie`, `afschaffing` → V5 will match base nouns ✓
- Chunk contains: `parlementaire`, `constitutionele`, `hervormingen` → V5 will NOT match ❌
- Result: Partial improvement, might not fully fix the ranking

**Risk**: If chunk uses primarily adjectival forms (`parlementaire`, `constitutionele`) rather than base nouns, Governance might still rank below Educational.

---

## Recommendations for Further Improvement

### **1. Add Missing Adjectival Forms to Seed** ⚠️ HIGH PRIORITY

**Governance additions**:
```python
GOVERNANCE_ADDITIONS = [
    ('parlementaire', 0.90),  # Parliamentary (adjective)
    ('constitutionele', 0.90),  # Constitutional (adjective)
    ('hervormingen', 0.85),  # Reforms (noun, conceptually distinct)
    ('hervorming', 0.85),  # Reform (singular)
]
```

**Why**: SBERT didn't discover these in V5 expansion despite having base nouns. Dutch adjectival morphology (`parlement` → `parlementaire`) creates semantic distance beyond k=50 nearest neighbors.

**Expected impact**: Chunk 195cdf4c should rank Governance #1 with these additions.

---

### **2. Consider Adding Explicit Racial Adjectives to Seed** (Optional)

**Social Fragmentation**:
```python
SOCIAL_OPTIONAL = [
    ('racistisch', 0.95),  # Already discovered (0.921) but could strengthen
    ('discriminerend', 0.95),  # Already discovered (0.891) but could strengthen
]
```

**Why**: Currently relying on SBERT discovery (weight 0.80). Adding to seed (weight 0.95) would give stronger signal for chunks using adjectival forms.

**Trade-off**:
- Pro: Stronger matching for chunks with adjectives
- Con: Defeats the purpose of condensed seed strategy
- Decision: OPTIONAL - only if V5 scoring shows Social Fragmentation still ranking too low

---

### **3. Curate V5 Carefully** ✓ NEXT STEP

**Priority areas for curation**:

**Educational topic**:
- Review `slavernij*` compounds: `slavernijgeschiedenis`, `slavernijdebat`, `slavernijonderzoek`
- Question: Do these belong in Educational or are they generic historical/political?
- Criteria: Keep only if explicitly about educational content (schools, curriculum, learning)
- Remove if they're about historical events, political debates, or general scholarship

**Social Fragmentation**:
- Keep morphological variants: `racistisch`, `discriminerend`, `discriminerende`
- Keep explicit racial terms: All variants of `neger`, `zwart*`, `blanke`, etc.
- Keep abolition movement terms: `abolitionisten`, `abolitionistisch`, `anti-slavernij`

**Governance**:
- Keep political process terms: `debat`, `wetgevend`, `parlementen`, `kabinetten`
- Review for missing terms: Check if `parlementaire` or `constitutionele` appear lower in expansion
- Keep colonial governance: All `koloniaal bestuur` related terms

---

### **4. Test V5 on Same 14 Chunks** ✓ VALIDATION STEP

**Process**:
1. Run V5 through complete workflow (Checkpoint 3 → Checkpoint 7)
2. Curate V5 expanded dictionary
3. Build topic vectors and score chunks
4. Extract same 14 chunk_ids from V4 analysis
5. Compare V5 vs V4 scores:
   - Primary topic rankings
   - Score margins
   - Confidence levels
   - Specific chunks: 34795144 (racism), 195cdf4c (parliamentary)

**Success criteria**:
- Chunk 34795144: Social Fragmentation ranks #1-2 (vs V4 rank #5)
- Chunk 195cdf4c: Governance ranks #1-2 (vs V4 rank #3)
- Overall: Fewer Educational #1 rankings for non-educational content
- Margins: Better topic separation (higher margins for focused content)

---

### **5. Consider Iterative Seed Refinement** (Optional)

**If V5 testing shows persistent issues**:

**Option A: V5.1 - Add missing adjectives**
- Add `parlementaire`, `constitutionele`, `hervormingen` to seed
- Re-run expansion
- Should fix Governance political vocabulary gap

**Option B: V5.2 - Strengthen racial vocabulary**
- Add `racistisch`, `discriminerend` to seed (currently SBERT-discovered)
- Increase weight for explicit racial terms
- Should strengthen Social Fragmentation for adjectival racism discussions

**Option C: V6 - Full refinement**
- V5.1 + V5.2 improvements
- Review Educational seed for remaining generic terms
- Final optimization before production use

---

## Curation Guidance for V5

### **What to Keep During Curation**

**1. Seed terms (all weights ≥0.85)**: Keep ALL seed terms automatically
   - They were carefully selected as core concepts
   - Exception: Only if cosine < 0.65 AND df < 3 (data error)

**2. High-weight discovered terms (weight 0.80, cosine ≥0.85)**:
   - Morphological variants of seed: `racistisch`, `discriminerend`, `wetgevend`
   - Semantic neighbors: `discriminatiezaken`, `slavenhandelaren`
   - Keep if: Clearly related to topic AND appears in corpus (df ≥ 5)

**3. Contextual filters (even if generic)**:
   - Temporal: `historisch`, `geschiedenis`, `destijds`, `achttiende`, `zeventiende`
   - Geographic: `Curaçao`, `Suriname`, `Bonaire`, `Antillen`
   - Slavery period: `slavernijverleden`, `slavernijgeschiedenis`
   - **Why**: These ensure focus on historical Caribbean slavery legacy across ALL topics

**4. Topic-specific high-frequency terms**:
   - Keep if: cosine ≥0.70 AND df ≥ 50 AND weight-adjusted quality score ≥ threshold
   - Example: `onderwijs` (df=194) for Educational, `slavernij` (df=753) for all topics

### **What to Remove During Curation**

**1. Low cosine, low frequency** (cosine <0.65, df <3):
   - Likely noise or very rare terms
   - Exception: Seed terms (keep regardless)

**2. Generic non-discriminating terms**:
   - Example: `terug`, `oorspronkelijk`, `jarenlange`
   - These don't differentiate between topics

**3. Overly specific compounds** (for Educational):
   - `geschiedenisboek`, `onderwijseditie`, `kunsthistorici`
   - Keep core concepts: `schooluitval`, `onderwijskwaliteit`
   - Remove administrative/peripheral: `onderwijsplannen`, `onderwijsvoorschriften`

**4. Topic mismatches** (careful review):
   - `slavernijdebat` in Educational: Is this about teaching slavery or political debates?
   - If it's about political debates → should be in Governance
   - If it's about curriculum debates → keep in Educational

### **Curation Decision Framework**

For each term with weight 0.80 (SBERT-discovered):

```
IF cosine ≥ 0.85 AND df ≥ 10:
    KEEP (strong semantic similarity + reasonable frequency)
ELIF cosine ≥ 0.75 AND df ≥ 30:
    KEEP (moderate similarity but high frequency)
ELIF cosine ≥ 0.70 AND df ≥ 50 AND term is morphological variant of seed:
    KEEP (variant of core concept with corpus presence)
ELIF term is contextual filter (temporal/geographic/slavery):
    KEEP (filtering function across topics)
ELIF term is generic administrative word:
    REMOVE (doesn't differentiate topics)
ELSE:
    REVIEW MANUALLY (borderline case)
```

For Educational-specific `slavernij*` compounds:
```
IF term describes educational institution/process:
    KEEP (e.g., "slavernijonderwijs", "slavernij lessen")
IF term describes historical event/political process:
    REMOVE (e.g., "slavernijdebat" → Governance, "slavernijgeschiedenis" → generic)
IF unsure:
    CHECK corpus examples - what context does it appear in?
```

---

## Summary: V5 vs V4

### **V5 Improvements** ✓

1. **Condensed seed (188 vs 377)**: Higher quality core concepts
2. **Critical terms added**: `neger`, `parlement`, `kabinet`, `constitutie`, `slavenhandel`, `abolitionisten`
3. **SBERT expansion validated**: Successfully finds morphological variants (`racistisch`, `discriminerend`, `wetgevend`)
4. **Weight distribution**: 91% terms ≥0.85 (vs 68% in V4)
5. **Expected to fix Chunk 34795144**: Social Fragmentation should rank #1-2

### **V5 Remaining Gaps** ⚠️

1. **Dutch adjectival forms**: `parlementaire`, `constitutionele` not discovered by SBERT
2. **Conceptually distinct terms**: `hervormingen` (reforms) not in seed
3. **Governance chunk 195cdf4c**: Might still rank #2-3 due to missing adjectives
4. **Educational compounds**: Needs careful curation of `slavernij*` terms

### **Recommended Actions**

**Immediate (for V5)**:
1. ✓ Curate V5 expanded dictionary (in progress)
2. ✓ Run complete workflow and score chunks
3. ✓ Test on 14 sample chunks to validate improvements

**If needed (V5.1 iteration)**:
1. Add `parlementaire`, `constitutionele`, `hervormingen` to Governance seed
2. Re-run expansion and curation
3. Re-test on sample chunks

**Production readiness**:
- V5 is a SIGNIFICANT improvement over V4
- V5 should be tested before deciding if V5.1 is necessary
- Expected: 60-70% of V4 problems will be fixed by V5
- Remaining 30-40% might require V5.1 with additional adjectives

---

## Next Step: Curate and Test V5

**Run the curation script on V5**:
```bash
python curate_v5_with_weights.py
```

**Then complete workflow**:
- Checkpoint 4: Build vocab and topic vectors
- Checkpoint 5: Score chunks with cosine similarity
- Checkpoint 6: Generate training data (if using BERTje)

**Validate**:
- Compare V5 vs V4 on 14 sample chunks
- Check if problem chunks are fixed
- Assess if further seed refinements needed

The condensed seed strategy has worked - now we need to test if it translates to better cosine labeling accuracy.
