# Dictionary Curation Report

**Stage:** 1 (Domain Corpus)
**Corpus Size:** 1000 documents
**Date:** 2026-01-13 20:46:02

---

## Curation Statistics

### Phase 1: Automatic Removals

- Morphological Fragments: 1
- Low Cosine: 62
- Single Df: 0
- Encoding Errors: 0

### Phase 3: Overgeneralization Control

- High Frequency Lowered: 1
- High Frequency Removed: 0
- Generic Fragments Removed: 0

### Phase 4: Category Corrections

- Historical Recategorized: 0
- Overcategorized Lowered: 39
- Solutions Adjusted: 0

### Phase 5: Weight Calibration

- Df Dampened: 0
- Cosine Dampened: 0
- Category Adjusted: 0

---

## Final Dictionary Summary

**Total Terms:** 237

### Weight Distribution

| Weight Range | Count | Percentage |
|-------------|-------|------------|
| 0.50-0.59 | 7 | 3.0% |
| 0.60-0.69 | 15 | 6.3% |
| 0.70-0.79 | 1 | 0.4% |
| 0.80-0.89 | 174 | 73.4% |
| 0.90-0.95 | 0 | 0.0% |
| 0.96-1.00 | 40 | 16.9% |

### Category Distribution

| Category | Count | Percentage |
|----------|-------|------------|
| strongly_related | 136 | 57.4% |
| core | 40 | 16.9% |
| related_strong | 39 | 16.5% |
| moderately_related | 15 | 6.3% |
| context | 7 | 3.0% |

### Topic Distribution

| Topic | Count |
|-------|-------|
| Contemporary_Manifestations | 237 |

---

## Quality Checks

### Pyramid Structure

- Core problems (1.00): 0
- Strong problems (0.95): 0
- Related strong (0.85): 39

⚠️ Pyramid structure may need review

---

## Next Steps

1. Review Phase 2 flagged terms manually for semantic drift
2. Test curated dictionary on sample documents
3. Adjust thresholds based on score distribution
4. Train BERTJE model on domain corpus with curated dictionary
5. Proceed to Stage 2 curation for policy corpus
