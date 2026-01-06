# Slavernij_Historisch Curation Report

**Topic**: Slavernij_Historisch (Historical Slavery)
**Date**: 2026-01-03
**Status**: ✅ Complete

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| **Initial terms** | 300 |
| **Seeds** | 48 |
| **Expanded** | 252 |
| **Final curated** | **212** |
| **Removed** | **40** (15.9% of expanded) |
| **Retention rate** | 84.1% |

---

## Phase 1: Automatic Removals

✅ **Result**: NO automatic removals needed

- Morphological fragments (len < 4): 0
- Extreme low cosine (<0.65): 0
- Single document frequency (expanded only): 0
- Zero df terms: 23 (intentional multi-word seed phrases - kept)

**Assessment**: Excellent expansion quality - all terms passed technical checks.

---

## Phases 2-6: Manual Curation Decisions

### Curation Actions Summary

| Action | Count | Description |
|--------|-------|-------------|
| **KEEP** | 175 | No changes needed |
| **RECATEGORIZE** | 34 | Category/weight changed |
| **REWEIGHT** | 3 | Weight adjusted within category |
| **REMOVE** | 40 | Excluded from dictionary |

---

## Key Curation Rules Applied

### Rule 1: Semantic Drift from "uitbuiting" Parent

**Problem**: Parent term "uitbuiting" (exploitation) generated 50 expansions, many were **orthographic matches** (uit-, uiting) rather than semantic matches.

**Action**: Removed 23 semantic drift terms

**Removed terms**:
- Orthographic: uit-, uiting, uitmaken, uitte, uitging, uittocht, uitputtende, uitgeloot, uitbraken, uitsprak, uitstaan, uitroepen, uitbarsten, uitgeputte, uitbarstingen
- Semantic drift: opheffing, voortzetting, afbreking, verwijdering, ontduiking, ontsporing, aanwas, bezetting

---

### Rule 2: Ultra-High Frequency Dampening (df > 300)

**Problem**: 3 terms with df > 300 risk dominating scores

| Term | df | Original | Decision |
|------|-------|----------|----------|
| **koloniale** | 524 | KERN 0.9 | ✅ KEEP as is (grammatical variant) |
| **slaven** | 479 | KERN 0.9 | 📝 CONTEXT 0.6 (too generic + low cosine 0.72) |
| **geschiedenis** | 316 | KERN 0.9 | 📝 CONTEXT 0.6 (too generic + low cosine 0.70) |

---

### Rule 3: Low Cosine (<0.72) + KERN 1.0

**Problem**: 11 terms at KERN 1.0 with low cosine (<0.72) don't meet strict KERN standards

**Actions**:
- **Removed (6)**: goederenhandel, smokkelhandel, staats-, staatkundig, slavengeld, negerhandel
  - Reasons: Generic trade terms, fragments, archaic/problematic terms
- **Downgraded to STERK 0.8 (2)**: slavenvervoer, eigendomsslavernij
  - Reasons: Relevant but low cosine
- **Reweighted to 0.9 (3)**: slavenopstanden, transatlantische, slavernijcomplex
  - Reasons: Valid terms, slightly lower confidence

---

### Rule 4: Low Cosine (<0.72) + KERN 0.9

**Problem**: 34 terms at KERN 0.9 with low cosine don't meet KERN threshold

**Actions**:
- **Removed (4)**: arbeid, economie, tuin, houder, eigenheid, eigenbelang
  - Reasons: Too generic or clear semantic drift
- **Downgraded to STERK 0.8 (30)**: Remaining low-cosine terms
  - Examples: slaveneigenaren, slavenopstand, plantagekoloniën, planter, suikerplantages, eigenaars, etc.
  - Reason: Relevant but don't meet KERN's unambiguous standard

---

### Rule 5: Additional Semantic Drift

**Removed (7)**:
- **vrouwenemancipatie**: Different type of emancipation (women's rights, not slavery)
- **schiedenis, geschiedenis-**: OCR errors/fragments
- **oorlogsschepen, marineschepen, zeilschepen**: Generic ships, not slave ships
- **roven**: Generic robbery, not historical plunder

---

### Rule 6: High df Geographic Terms

| Term | df | Original | Decision |
|------|-------|----------|----------|
| **koloniën** | 278 | KERN 0.9 | �� CONTEXT 0.6 (geographic marker) |

---

## Category Transitions

| From | To | Weight Change | Count | Rationale |
|------|--------|---------------|-------|-----------|
| KERN 0.9 | CONTEXT 0.6 | Downgrade | 3 | Ultra-high df + too generic |
| KERN 1.0 | KERN 0.9 | Minor adjustment | 3 | Valid but lower confidence |
| KERN 0.9 | STERK 0.8 | Downgrade | 29 | Low cosine, not unambiguous |
| KERN 1.0 | STERK 0.8 | Downgrade | 2 | Relevant but low cosine |

---

## Final Category Distribution

### Before Curation (Expanded Terms Only)

| Category | Count | % |
|----------|-------|---|
| KERN | 199 | 78.9% |
| STERK | 53 | 21.1% |
| **Total Expanded** | **252** | **100%** |

### After Curation (Final Dictionary)

| Category | Estimated Count | % | Note |
|----------|-----------------|---|------|
| KERN | ~170 | ~80% | Includes seeds + curated expanded |
| STERK | ~35 | ~16.5% | Original + downgraded from KERN |
| CONTEXT | ~7 | ~3.3% | New category for generic terms |
| **Total Final** | **~212** | **100%** | Estimate (seeds + curated expanded) |

---

## Quality Improvements

### Problems Addressed

1. ✅ **Semantic drift controlled**: Removed 30+ drift terms (principalmente from "uitbuiting" parent)
2. ✅ **Ultra-high frequency dampened**: Moved overly common terms to CONTEXT
3. ✅ **KERN standards enforced**: Only truly unambiguous terms remain in KERN
4. ✅ **Low-quality expansions removed**: 40 terms that didn't meet V10 standards
5. ✅ **Category fit validated**: 37 terms recategorized to better match their function

### Remaining Quality

- ✅ No morphological fragments
- ✅ No extreme low cosine (<0.65)
- ✅ No single-occurrence noise
- ✅ KERN category maintains high standards
- ✅ Semantic coherence improved
- ✅ Over-expanded parents cleaned

---

## Removal Breakdown by Reason

| Reason | Count |
|--------|-------|
| Semantic drift from uitbuiting (orthographic not semantic) | 23 |
| Semantic drift or OCR error | 7 |
| Too generic or semantic drift | 4 |
| Generic trade terms, not slavery-specific | 2 |
| Archaic/problematic terms | 2 |
| Fragments or too generic government terms | 2 |
| **Total** | **40** |

---

## Files Generated

1. **slavernij_historisch_manual_review.csv** - All 252 expanded terms with review priorities
2. **slavernij_historisch_curated.csv** - Full curation decisions with actions and notes
3. **slavernij_historisch_final.csv** - Clean final dictionary (212 terms, removals excluded)

---

## Key Insights for Remaining Topics

### Lessons Learned

1. **Over-expanded parents are common issue**
   - "uitbuiting" → 50 expansions (mostly drift)
   - **Action**: Apply stricter thresholds for high-expansion parents

2. **Low cosine + high category = red flag**
   - 64 terms flagged with cosine <0.75 + KERN
   - **Most were legitimate downgrades to STERK or removals**

3. **Ultra-high df terms need special attention**
   - Terms with df > 300 often too generic for KERN
   - **Move to CONTEXT or dampen weight**

4. **Orthographic similarity ≠ semantic similarity**
   - BERTJE finds spelling-similar terms (uit- from uitbuiting)
   - **Requires manual semantic validation**

5. **Context category is valuable**
   - Generic but relevant terms (slaven, geschiedenis, koloniën)
   - **Better than removing or keeping at high weight**

### Recommendations for Other Topics

1. **Priority review**: Low cosine + high category terms first
2. **Parent analysis**: Flag parents with >30 expansions for strict review
3. **High df dampening**: Automatic for df > 300
4. **Semantic drift detection**: Critical for morphologically-rich Dutch
5. **Use CONTEXT category**: For generic but discourse-relevant terms

---

## Next Steps

1. ✅ Slavernij_Historisch curated (212 terms)
2. ⏳ Apply same methodology to remaining 6 topics:
   - Koninkrijks_Macht (300 terms)
   - Raciale_Hierarchie (293 terms)
   - Arbeid_Afhankelijkheid (300 terms)
   - Doorwerking_Continuiteit (300 terms)
   - Erkenning_Verantwoordelijkheid (300 terms)
   - Kennis_Herinnering (300 terms)
3. ⏳ Cross-topic validation
4. ⏳ Final dictionary merge and quality report

---

## Curator Notes

**Slavernij_Historisch** was an ideal starting point:
- Clear topic boundaries (historical vs. contemporary)
- Mostly KERN/STERK (no BELEID/RISICO complexity)
- High-quality seed dictionary
- Clean expansion (no Phase 1 removals needed)

**Main challenge**: Semantic drift from Dutch morphology ("uit-" matching "uitbuiting")

**Solution**: Systematic rules-based curation with manual semantic validation for edge cases

**Outcome**: High-quality curated dictionary maintaining topic coherence while removing 15.9% noise

---

**Curated by**: Claude Sonnet 4.5
**Method**: V10 5-tier categorical curation methodology
**Tool**: Python pandas with systematic rule application
