# Dictionary Curation Report

**Stage:** 1 (Domain Corpus)
**Corpus Size:** 1000 documents
**Date:** 2026-01-13 20:39:44

---

## Curation Statistics

### Phase 1: Automatic Removals

- Morphological Fragments: 0
- Low Cosine: 0
- Single Df: 0
- Encoding Errors: 0

### Phase 3: Overgeneralization Control

- High Frequency Lowered: 6
- High Frequency Removed: 0
- Generic Fragments Removed: 0

### Phase 4: Category Corrections

- Historical Recategorized: 0
- Overcategorized Lowered: 35
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
| 0.50-0.59 | 14 | 4.7% |
| 0.60-0.69 | 34 | 11.3% |
| 0.70-0.79 | 1 | 0.3% |
| 0.80-0.89 | 151 | 50.3% |
| 0.90-0.95 | 0 | 0.0% |
| 0.96-1.00 | 100 | 33.3% |

### Category Distribution

| Category | Count | Percentage |
|----------|-------|------------|
| strongly_related | 113 | 37.7% |
| core | 105 | 35.0% |
| related_strong | 35 | 11.7% |
| moderately_related | 33 | 11.0% |
| context | 14 | 4.7% |

### Topic Distribution

| Topic | Count |
|-------|-------|
| Historical_Slavery_Colonialism | 300 |

---

## Quality Checks

### Pyramid Structure

- Core problems (1.00): 0
- Strong problems (0.95): 0
- Related strong (0.85): 35

⚠️ Pyramid structure may need review

---

## Next Steps

1. Review Phase 2 flagged terms manually for semantic drift
2. Test curated dictionary on sample documents
3. Adjust thresholds based on score distribution
4. Train BERTJE model on domain corpus with curated dictionary
5. Proceed to Stage 2 curation for policy corpus
