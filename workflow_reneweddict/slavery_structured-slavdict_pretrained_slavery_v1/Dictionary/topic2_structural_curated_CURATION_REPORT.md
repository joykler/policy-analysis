# Dictionary Curation Report

**Stage:** 1 (Domain Corpus)
**Corpus Size:** 1000 documents
**Date:** 2026-01-13 20:43:32

---

## Curation Statistics

### Phase 1: Automatic Removals

- Morphological Fragments: 0
- Low Cosine: 0
- Single Df: 0
- Encoding Errors: 0

### Phase 3: Overgeneralization Control

- High Frequency Lowered: 0
- High Frequency Removed: 0
- Generic Fragments Removed: 0

### Phase 4: Category Corrections

- Historical Recategorized: 0
- Overcategorized Lowered: 29
- Solutions Adjusted: 0

### Phase 5: Weight Calibration

- Df Dampened: 0
- Cosine Dampened: 0
- Category Adjusted: 0

---

## Final Dictionary Summary

**Total Terms:** 300

### Weight Distribution

| Weight Range | Count | Percentage |
|-------------|-------|------------|
| 0.50-0.59 | 0 | 0.0% |
| 0.60-0.69 | 31 | 10.3% |
| 0.70-0.79 | 0 | 0.0% |
| 0.80-0.89 | 241 | 80.3% |
| 0.90-0.95 | 0 | 0.0% |
| 0.96-1.00 | 28 | 9.3% |

### Category Distribution

| Category | Count | Percentage |
|----------|-------|------------|
| strongly_related | 212 | 70.7% |
| moderately_related | 31 | 10.3% |
| related_strong | 29 | 9.7% |
| core | 28 | 9.3% |

### Topic Distribution

| Topic | Count |
|-------|-------|
| Structural_Continuity_Neocolonial | 300 |

---

## Quality Checks

### Pyramid Structure

- Core problems (1.00): 0
- Strong problems (0.95): 0
- Related strong (0.85): 29

⚠️ Pyramid structure may need review

---

## Next Steps

1. Review Phase 2 flagged terms manually for semantic drift
2. Test curated dictionary on sample documents
3. Adjust thresholds based on score distribution
4. Train BERTJE model on domain corpus with curated dictionary
5. Proceed to Stage 2 curation for policy corpus
