# V7 Dictionary Creation Summary

**Date**: 2025-11-27
**Status**: ✓ Created and ready for testing

---

## Files Created

### 1. **problem_oriented_legacy_seed_v7_4topics.csv**
- **204 terms** (vs. 166 in v6, +38 terms)
- Improved weight differentiation
- Reduced cross-contamination from uniform terms

### 2. **dictionary_discovery_v17_improved_weights.ipynb**
- Updated workflow notebook configured for v7 dictionary
- All v16 references updated to v17
- Workflow data path: `workflow_data/slavery_Slavdict_pretraining_slavery_v17/`

### 3. **Supporting Scripts**
- `create_v7_dictionary.py` - Dictionary creation script
- `update_notebook_to_v17.py` - Notebook configuration updater
- `test_v7_scoring_quick.py` - Quick scoring test (requires sentence-transformers)

---

## Key Improvements in v7

### 1. Reduced Uniform Term Weights (Highest Impact)

**Problem**: Geographic and era marker terms appeared in all topics at high weights, creating cross-contamination.

**Solution**:
```
Geography:   0.75 → 0.50  (-0.25)
Era markers: 0.70 → 0.55  (-0.15)
```

**Terms affected**:
- Geographic (6 terms): curaçao, bonaire, aruba, suriname, caribisch nederland, bes-eilanden, antillen
- Era markers (8 terms): 1863, geschiedenis, historisch, koloniaal, koloniale, slavernijverleden, afschaffing, verleden

**Expected impact**: Reduces uniform baseline by ~0.55 units, allowing topic-specific terms to dominate scores.

### 2. Expanded Weight Tiers (Medium Impact)

**v6 weight tiers** (5 tiers):
```
1.0   - Core problems
0.95  - Core problems
0.9   - Related
0.85  - Related
0.8   - Historical
```

**v7 weight tiers** (7 tiers):
```
1.0   - Core problems (absolutely central)
0.95  - Strong problems (clear problem vocabulary)
0.85  - Related strong (domain vocabulary, strong)
0.75  - Related moderate (domain vocabulary, moderate)
0.70  - Related moderate (domain vocabulary, weak)
0.65  - Related weak (peripheral terms)
0.55  - Era context (historical/temporal markers)
0.50  - Geographic context (geographic markers)
```

**Expected impact**: Stronger differentiation between chunks with core problem terms vs. generic domain vocabulary.

### 3. Added Problem-Specific Vocabulary (Medium Impact)

**Educational (+10 terms)**:
- Strong problems: schoolachterstand, onderwijskloof, analfabetisme, taalachterstand, onderwijsongelijkheid, voortijdig schoolverlaten
- Related: kennismigratie, onderwijsachterstand, schoolprestaties, onderwijssysteem

**Governance (+10 terms)**:
- Strong problems: omkoping, vriendjespolitiek, machtsmisbruik, bestuurlijke zwakte, institutioneel wantrouwen, gebrek aan transparantie, democratisch tekort
- Related: politieke afhankelijkheid, bestuurscultuur, governance

**Economic (+15 terms - PRIORITY)**:
- Strong problems: structurele armoede, langdurige werkloosheid, inkomensongelijkheid, economische uitsluiting, financiële kwetsbaarheid, verborgen armoede
- Related: minimuminkomens, arbeidsmarkt, economische structuur, inkomen, werk, banen, economie, financieel, kosten

**Racism (+5 terms)**:
- Strong problems: institutioneel racisme, structureel racisme, sociale ongelijkheid, etnische discriminatie, raciale hiërarchie

**Expected impact**: More vocabulary → stronger signal for relevant chunks → higher max scores.

### 4. Removed/Reduced Generic Shared Terms (Low Impact)

**Removed entirely**:
- `slavernij` from Economic and Racism topics (too generic, doesn't differentiate topics)

**Reduced weights**:
- `plantage`: 0.90 → 0.65 (appears in Economic AND Racism, too generic)
- `slavenhandel`: 0.90 → 0.65 (appears in Economic AND Racism, too generic)
- `afschaffing`: reclassified as era_context 0.55 (was 0.70-0.85, historical event not problem)

**Expected impact**: Clearer topic differentiation, reduced false cross-topic signals.

---

## Per-Topic Statistics

### Educational Disadvantage & Brain Drain
- **55 terms** (was 45, +10)
- Categories:
  - related_strong: 15
  - era_context: 11
  - strong_problem: 10
  - related_moderate: 9
  - geographic_context: 6
  - core_problem: 4
- Weight range: 0.50 - 1.00

### Governance Distrust & Corruption
- **49 terms** (was 39, +10)
- Categories:
  - strong_problem: 12
  - related_strong: 12
  - era_context: 10
  - related_moderate: 9
  - geographic_context: 4
  - core_problem: 2
- Weight range: 0.50 - 1.00

### Persistent Poverty & Economic Vulnerability
- **53 terms** (was 39, +14)
- Categories:
  - related_strong: 13
  - era_context: 10
  - related_moderate: 10
  - strong_problem: 9
  - geographic_context: 6
  - related_weak: 3
  - core_problem: 2
- Weight range: 0.50 - 1.00

### Social Fragmentation & Racism
- **47 terms** (was 43, +4)
- Categories:
  - strong_problem: 11
  - related_strong: 10
  - era_context: 10
  - related_moderate: 6
  - core_problem: 4
  - geographic_context: 4
  - related_weak: 2
- Weight range: 0.50 - 1.00

---

## Expected Improvements vs. v16

### Score Ranges
```
                v16 Current    v7 Predicted    Improvement
Max scores:     0.55-0.64      0.72-0.80       +0.17-0.20
Std dev:        0.08-0.11      0.14-0.17       +0.06-0.07
Mean:           0.28-0.32      0.30-0.36       +0.02-0.04
```

### Confidence Distribution
```
                v16 Current    v7 Predicted    Change
High (≥0.4):    317 (19%)      450 (27%)       +133 (+42%)
Low (≥0.2):     861 (52%)      750 (45%)       -111 (-13%)
None:           474 (29%)      450 (27%)       -24 (-5%)
```

### Pattern Quality (72-chunk evaluation)
```
                v16 Current    v7 Predicted
Good+:          11%            60%            (+49%)
Trainable:      11%            55%            (+44%)
```

---

## Success Criteria for v17

### Minimum Viable Success
- [ ] Max scores reach ≥0.70 for at least one topic
- [ ] Std dev increases to ≥0.12 for all topics
- [ ] High confidence pool increases to ≥25% (from 19.2%)
- [ ] Manual review: ≥70% of high-confidence chunks genuinely strong on topic

### Optimal Success
- [ ] Max scores reach 0.75-0.80 for all topics
- [ ] Std dev increases to ≥0.15 for all topics
- [ ] High confidence pool increases to ≥30%
- [ ] Pattern quality on evaluation sample: ≥60% Good/Excellent
- [ ] Training sufficiency on evaluation sample: ≥65% Yes

### If v17 Fails
- [ ] Max scores still <0.65 despite interventions
- [ ] Std dev doesn't increase (still <0.10)
- [ ] High confidence pool doesn't grow
- [ ] → Consider 8D hybrid approach OR different methodology

---

## Next Steps

### Immediate: Test v17 Workflow

**Option 1: Full workflow (recommended)**
1. Open `dictionary_discovery_v17_improved_weights.ipynb` in Jupyter
2. Run all cells from start
3. Monitor score distributions at CHECKPOINT 5
4. Compare to v16 baseline

**Option 2: Quick test on evaluation sample**
1. Ensure `sentence-transformers` is installed: `pip install sentence-transformers`
2. Run: `python test_v7_scoring_quick.py`
3. Review comparison output
4. If improvements shown → proceed to full workflow

### After Testing: Validate Results

**Score Analysis**:
1. Check max scores per topic (target: 0.72-0.80)
2. Check std dev per topic (target: 0.14-0.17)
3. Check confidence distribution (target: 27% high)
4. Compare to v16 results

**Manual Validation**:
1. Sample 20 high-confidence chunks (5 per topic)
2. Verify scores match semantic judgment
3. Check: Are high scores (>0.7) genuinely strong on topic?
4. Check: Are low scores (<0.3) genuinely weak/absent?

### If Success Criteria Met: Proceed

1. Label full slavery corpus with v17
2. Train BERTje on v17-labeled data
3. Expand dictionary in policy space
4. Label policy corpus
5. Train final classifier
6. Apply to policy documents
7. Thesis analysis

### If Criteria Not Met: Iterate

**If max scores still <0.70**:
- Further reduce geographic/era weights (0.50 → 0.40, 0.55 → 0.45)
- Add more core problem vocabulary
- Consider removing more generic shared terms

**If std dev doesn't increase**:
- Expand weight differentiation further (e.g., add 0.60 tier for weak related)
- Review term classifications (are core terms truly core?)
- Consider different embedding model

**If confidence doesn't improve**:
- Adjust confidence thresholds (lower to 0.35 for high confidence)
- Add multi-topic high confidence category
- Reconsider margin requirements

**If fundamental issues persist**:
- Consider 8D hybrid approach (see [HYBRID_8D_APPROACH_DETAILED.md](HYBRID_8D_APPROACH_DETAILED.md))
- Or alternative methodology entirely

---

## Supporting Documentation

- **[IMPROVE_4D_SCORING_STRATEGY.md](IMPROVE_4D_SCORING_STRATEGY.md)** - Detailed rationale and implementation plan
- **[WORKFLOW_INTERACTION_ANALYSIS_v16.md](WORKFLOW_INTERACTION_ANALYSIS_v16.md)** - Problem diagnosis from v16
- **[HYBRID_8D_APPROACH_DETAILED.md](HYBRID_8D_APPROACH_DETAILED.md)** - Alternative 8D approach if v17 fails
- **[PROJECT_CONTEXT_MASTER.md](PROJECT_CONTEXT_MASTER.md)** - Overall research context

---

## Changelog

**v7 (2025-11-27)**:
- Created 204-term dictionary (+38 from v6)
- Reduced geography weights 0.75 → 0.50
- Reduced era marker weights 0.70 → 0.55
- Expanded weight tiers 5 → 7
- Added 40 problem-specific terms
- Removed "slavernij" from topics
- Reduced "plantage", "slavenhandel" weights
- Created v17 workflow notebook

**v6 (baseline)**:
- 166 terms
- 4 topics with integrated geography/era markers
- 5 weight tiers
- Used in v16 workflow (achieved 11% training sufficiency)

---

**Status**: Ready for testing
**Estimated time to test**: 2-3 hours (full workflow) or 30 min (quick test)
**Decision point**: After testing, proceed to full corpus or iterate dictionary
