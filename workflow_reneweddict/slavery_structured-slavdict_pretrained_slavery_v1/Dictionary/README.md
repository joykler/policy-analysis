# Curated Slavery Legacy Dictionary - 7-Tier Framework
**Stage 1: Domain Corpus (Slavery Legacy Scholarship)**

## Overview

This directory contains the systematically curated dictionary for the 3-topic Slavery Legacy framework, processed through the 5-phase curation methodology defined in `A__DICTIONARY_CURATION_GUIDE.md`.

## Final Curated Dictionary

**File:** `SLAVERY_LEGACY_DICTIONARY_CURATED_7TIER.csv`

**Statistics:**
- Total terms: 782
- Topics: 3
- Framework: 7-tier semantic weights (1.00/0.95/0.85/0.75/0.70/0.55/0.50)
- Seed terms: 143 (original)
- Expanded terms: 639 (BERTJE nearest-neighbor)
- Removed during curation: 118 (13.1%)

**Weight Distribution:**
- 1.00 (core_problem): 173 terms (22.1%)
- 0.95 (strong_problem): 461 terms (59.0%)
- 0.85 (related_strong): 48 terms (6.1%)
- 0.75 (related_moderate): 79 terms (10.1%)
- 0.55 (era_context): 21 terms (2.7%)

## Topics

### 1. Historical_Slavery_Colonialism (296 terms)
Covers: Slavery institution + Colonial system + Scientific racism ideology

**Weight distribution:**
- 1.00: 105 terms (35.5%) - slavery, colonialism, scientific racism concepts
- 0.95: 113 terms (38.2%) - slave trade, colonial institutions, racial ideology
- 0.85: 31 terms (10.5%) - WIC/VOC, plantation structures, racial descriptors
- 0.75: 33 terms (11.1%) - actors, specific plantations, race theories
- 0.55: 14 terms (4.7%) - historical context markers

**Removal rate:** 1.3% (4 terms removed)
**Key removals:** Orthographic matches to `afschaffing` and `slaaf` with wrong meanings

### 2. Structural_Continuity_Neocolonial (283 terms)
Covers: Continuity mechanisms + Extraction economics + Brain drain + Structural patterns

**Weight distribution:**
- 1.00: 28 terms (9.9%) - continuity, legacy, structural pattern concepts
- 0.95: 212 terms (74.9%) - neocolonial, extraction, marginalization manifestations
- 0.85: 12 terms (4.2%) - intercolonial, ex-colonies, colonized people
- 0.75: 31 terms (11.0%) - inequality, poverty, dependency outcomes

**Removal rate:** 5.7% (17 terms removed)
**Key removals:** Construction terms (bouw*, constructie) with wrong semantic space

### 3. Contemporary_Manifestations (203 terms)
Covers: Racism + Systemic/institutional racism + Discrimination

**Weight distribution:**
- 1.00: 40 terms (19.7%) - racism, discrimination, exclusion concepts
- 0.95: 136 terms (67.0%) - systemic racism, anti-Black racism, racialization
- 0.85: 5 terms (2.5%) - affected groups, discrimination contexts
- 0.75: 15 terms (7.4%) - prejudice, stereotypes, anti-racism
- 0.55: 7 terms (3.4%) - temporal markers

**Removal rate:** 32.3% (97 terms removed)
**Key removals:** 34 orthographic matches from `uitsluiting` parent + 63 overgeneralizations

## Curation Process Applied

### Phase 1: Automatic Removal (Technical Errors)
- Removed morphological fragments, low cosine (<0.65), single df, encoding errors
- Contemporary topic: 63 removals (overgeneralization)
- Historical/Structural: 0 removals (clean expansions)

### Phase 2: Semantic Drift Detection (Manual Review)
- Flagged low cosine + high weight terms for manual review
- Historical: 8 flagged → 4 removed
- Structural: 22 flagged → 17 removed
- Contemporary: 38 flagged → 34 removed

### Phase 3: Overgeneralization Control
- Lowered weights for high-frequency terms (df > 300)
- Removed generic fragments
- Historical: 6 terms adjusted
- Structural: 6 terms adjusted

### Phase 4: Category Corrections
- Recategorized overcategorized terms (low cosine but high category)
- Historical: 35 terms recategorized
- Structural: 29 terms recategorized
- Contemporary: 39 terms recategorized

### Phase 5: Weight Calibration
- Applied semantic distance dampening
- Enforced category-specific weight ceilings
- Final adjustments for 7-tier framework consistency

## Files in This Directory

### Final Outputs
- `SLAVERY_LEGACY_DICTIONARY_CURATED_7TIER.csv` - Consolidated 3-topic curated dictionary
- `topic1_historical_FINAL_CURATED.csv` - Topic 1 only
- `topic2_structural_FINAL_CURATED.csv` - Topic 2 only
- `topic3_contemporary_FINAL_CURATED.csv` - Topic 3 only
- `COMPLETE_CURATION_SUMMARY.md` - Comprehensive curation report
- `README.md` - This file

### Source Files
- `expanded_candidates.csv` - Original BERTJE-expanded dictionary (900 terms)
- `topic1_historical_expanded.csv` - Topic 1 pre-curation
- `topic2_structural_expanded.csv` - Topic 2 pre-curation
- `topic3_contemporary_expanded.csv` - Topic 3 pre-curation

### Curation Phase Files (Intermediate)

**Topic 1:**
- `topic1_historical_curated_phase1.csv` - After automatic removal
- `topic1_historical_curated_phase2.csv` - After semantic drift flagging
- `topic1_historical_curated_phase2_flagged.txt` - Flagged terms for review
- `topic1_historical_curated_phase2_manual.csv` - After manual review
- `topic1_historical_curated_phase3.csv` - After overgeneralization control
- `topic1_historical_curated_phase4.csv` - After category corrections
- `topic1_historical_curated_phase5.csv` - After weight calibration
- `topic1_manual_review_decisions.csv` - Manual review decisions with rationales

**Topic 2:**
- `topic2_structural_curated_phase*.csv` - Same structure as Topic 1
- `topic2_manual_review_decisions.csv` - Manual review decisions

**Topic 3:**
- `topic3_contemporary_curated_phase*.csv` - Same structure as Topic 1
- `topic3_manual_review_decisions.csv` - Manual review decisions

### Reports
- `topic1_historical_curated_CURATION_REPORT.md` - Detailed Topic 1 report
- `topic2_structural_curated_CURATION_REPORT.md` - Detailed Topic 2 report
- `topic3_contemporary_curated_CURATION_REPORT.md` - Detailed Topic 3 report

## Usage

### Load the Curated Dictionary

```python
import pandas as pd

# Load full dictionary
dict_df = pd.read_csv('SLAVERY_LEGACY_DICTIONARY_CURATED_7TIER.csv')

# Filter by topic
historical = dict_df[dict_df['topic'] == 'Historical_Slavery_Colonialism']
structural = dict_df[dict_df['topic'] == 'Structural_Continuity_Neocolonial']
contemporary = dict_df[dict_df['topic'] == 'Contemporary_Manifestations']

# Create scoring dictionaries
scoring_dict = {}
for topic in dict_df['topic'].unique():
    topic_terms = dict_df[dict_df['topic'] == topic]
    scoring_dict[topic] = dict(zip(topic_terms['term'], topic_terms['weight']))
```

### Score a Document

```python
def score_document(text, topic_dict):
    """Score document for a topic using weighted dictionary"""
    text_lower = text.lower()
    score = 0.0
    matched_terms = []

    for term, weight in topic_dict.items():
        if term.lower() in text_lower:
            score += weight
            matched_terms.append((term, weight))

    return score, matched_terms

# Example
text = "Het rapport bespreekt de doorwerkingen van het koloniale slavernijverleden..."
hist_score, hist_matches = score_document(text, scoring_dict['Historical_Slavery_Colonialism'])
struct_score, struct_matches = score_document(text, scoring_dict['Structural_Continuity_Neocolonial'])
contemp_score, contemp_matches = score_document(text, scoring_dict['Contemporary_Manifestations'])
```

## Quality Validation

### Pyramid Structure: PASS
- Core (1.00): 173 terms (22.1%) - properly restricted
- Strong (0.95): 461 terms (59.0%) - largest tier for semantic richness
- Related strong (0.85): 48 terms (6.1%) - domain contexts
- Related moderate (0.75): 79 terms (10.1%) - actors/processes
- Era context (0.55): 21 terms (2.7%) - temporal markers

### Coverage: COMPLETE
All user framework elements covered:
- Historical: Slavery + Colonialism + Scientific racism
- Structural: Continuity + Extraction + Brain drain + Structural patterns
- Contemporary: Racism + Systemic racism + Discrimination

### Parent Quality: CONTROLLED
Problem parents identified and cleaned:
- `uitsluiting`: 36 flagged, 34 removed
- `structurele`: Construction terms removed
- `onderontwikkeling`: Opposite meanings removed

## Next Steps

### For BERTJE Training (Stage 1)
1. Use this curated dictionary for soft-label generation
2. Score domain corpus chunks with weighted scoring
3. Train BERTJE model on weighted labels
4. Validate on held-out domain texts

### For Policy Corpus (Stage 2)
1. Use Stage 1 trained BERTJE model
2. Expand this dictionary into policy corpus
3. Apply Stage 2 curation (more restrictive):
   - Remove purely historical terms
   - Remove domain jargon not in policy language
   - Require higher cosine thresholds (≥0.72)
4. Train final model on policy corpus

## Curation Methodology Reference

Full methodology documented in:
- `../../A__DICTIONARY_CURATION_GUIDE.md` - Complete 5-phase process
- `../../CURATION_WORKFLOW_INTEGRATION_GUIDE.md` - Integration into notebook
- `../../systematic_dictionary_curation_workflow.py` - Python implementation

## Version History

- **v1 (2026-01-13):** Initial systematic curation from BERTJE-expanded candidates
  - 900 input terms → 782 curated terms
  - 5-phase methodology applied
  - 7-tier framework implemented
  - Manual review of 68 flagged terms
  - 118 terms removed (13.1%)

## Contact

For questions about curation decisions, see:
- `COMPLETE_CURATION_SUMMARY.md` - Detailed rationales for all decisions
- `topic*_manual_review_decisions.csv` - Specific manual review rationales
- `topic*_curated_phase2_flagged.txt` - All flagged terms with context
