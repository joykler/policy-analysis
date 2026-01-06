# Iteration 1 Dictionary Re-Curation - COMPLETE

**Date:** 2025-11-14
**Objective:** Curate dictionary for Iteration 1 training focused on HISTORICAL CAUSES & STRUCTURES of slavery

---

## Summary

Successfully re-curated the dictionary file according to updated criteria that clearly distinguish between:
- **HISTORICAL CAUSES/STRUCTURES** (KEPT for Iteration 1)
- **CONTEMPORARY OUTCOMES** (REMOVED, saved for Iteration 2)

---

## Files Generated

All files located in: `c:\Users\Home\policy-analysis\workflow_data\slavery_Slavdict_pretraining_slavery_v2\Dictionary\`

1. **curated_dictionary.csv** (371 terms)
   - Clean dictionary for Iteration 1 BERTje training
   - Focused on historical causes and structures
   - 25.3% retention rate from candidates

2. **CURATION_SUMMARY.md**
   - Full statistical breakdown
   - Retention rates by topic
   - Terms kept/removed by category
   - High-value terms per topic
   - Explicit rationale for racial ideology terms

3. **CURATION_VERIFICATION.md**
   - Spot checks of curation decisions
   - Examples from each category
   - Quality assurance checks

4. **curate_iteration1_dictionary.py**
   - Reusable curation script
   - Rule-based regex patterns
   - Semantic categorization logic

---

## Key Statistics

### Overall
- **Total candidates:** 1,469 terms
- **Terms KEPT:** 371 (25.3%)
- **Terms REMOVED:** 1,098 (74.7%)

### Retention by Topic
- Social Fragmentation & Racism: 34.0% (highest - due to racial ideology terms)
- Persistent Poverty & Economic Vulnerability: 29.7%
- Educational Disadvantage & Brain Drain: 21.9%
- Structural Neglect & Infrastructure Gaps: 20.3%
- Governance Distrust & Corruption: 20.0%

### Terms Kept by Category
- **Historical slavery core:** 202 terms (slavernij, slavenhandel, plantages, etc.)
- **Colonial structures:** 71 terms (koloniale, gouverneur, etc.)
- **Caribbean localization:** 45 terms (curaçao, papiamento, surinaamse, etc.)
- **Racial ideology (FOUNDATIONAL):** 31 terms (racisme, discriminatie, raciale, etc.)
- **Academic/historical analysis:** 18 terms (slavernijonderzoek, historisch, etc.)
- **Historical context:** 4 terms

### Terms Removed by Category
- **Not clearly historical/structural:** 1,053 terms (conservative default)
- **Economic outcomes:** 21 terms (armoede, werkloosheid, schuld, etc.)
- **Migration flows:** 17 terms (emigratie, immigratie, migratie, etc.)
- **Educational outcomes:** 4 terms (schooluitval, lerarentekort, etc.)
- **Contemporary governance:** 2 terms (corruptie, nepotisme)
- **Contemporary social problems:** 1 term

---

## Critical Decision: Racial Ideology Terms

### Why Racisme/Discriminatie Are KEPT

**These are NOT contemporary outcomes - they are FOUNDATIONAL CAUSES:**

1. **Ideological Foundation**
   - Racial ideology was THE causal system that justified and enabled slavery
   - Without racial theories, the slavery system could not have been sustained

2. **Historical Structures**
   - Rassenleer (racial theory), rassentheorie were formal knowledge systems in colonial period
   - These were documented, taught, and institutionalized

3. **Training Objective**
   - Iteration 1 teaches BERTje about CAUSES and STRUCTURES
   - Racial ideology was the central cause
   - Contemporary manifestations of racism will be addressed in Iteration 2 as OUTCOMES

4. **Terms Kept (31 total)**
   - racisme, discriminatie, huidskleur, racistische, racistisch
   - arbeidsdiscriminatie, rassendiscriminatie
   - discriminerend, discriminatiezaken, antidiscriminatie
   - raciale, raciaal, etnisch, etnische

---

## Contemporary Terms Saved for Iteration 2

These represent OUTCOMES and CONTEMPORARY MANIFESTATIONS:

### Economic Outcomes (21 terms)
armoede, werkloosheid, schuld, armoedesituatie, armoedeproblematiek, jeugdwerkloosheid, armoedebestrijding, schulden, armoedegrens, armoedebeleid, schuldrestant, werkloosheidscijfers, werkloosheidspercentage

### Educational Outcomes (4 terms)
schooluitval, lerarentekort, taalbarrières, leerachterstanden

### Migration Flows (17 terms)
emigratie, immigratie, migratie, immigranten, migranten, migratiediscours, immigratiedienst, migratieachtergrond, asielmigranten, migrantenachtergrond, arbeidsmigranten, migratiestromen

### Contemporary Governance (2 terms)
corruptie, nepotisme (as current problems, not colonial structures)

---

## Sample High-Value Terms (by cosine similarity)

### Social Fragmentation & Racism (Top 10)
1. racisme (1.0000, df=271) - FOUNDATIONAL
2. discriminatie (1.0000, df=247) - FOUNDATIONAL
3. slavernij (1.0000, df=753)
4. slavernijverleden (1.0000, df=257)
5. huidskleur (1.0000, df=33) - FOUNDATIONAL
6. curaçao (0.9780, df=223)
7. slavernijgeschiedenis (0.9405, df=23)
8. slavernijgeschiedenissen (0.9271, df=2)
9. racistische (0.9234, df=37) - FOUNDATIONAL
10. racistisch (0.9210, df=21) - FOUNDATIONAL

### Persistent Poverty & Economic Vulnerability (Top 10)
1. slavenarbeid (1.0000, df=19) - Historical structure
2. slavernijverleden (1.0000, df=257)
3. curaçao (0.9780, df=223)
4. slavernijgeschiedenis (0.9405, df=23)
5. slavenverzet (0.8479, df=4) - Historical resistance
6. slavernij (0.8413, df=753)
7. koloniale (0.8200, df=503)
8. plantagesector (0.8064, df=9) - Economic structure

Note: Contemporary poverty terms (armoede, werkloosheid) were correctly REMOVED

### Governance Distrust & Corruption (Top 10)
1. gouverneur (1.0000, df=62) - Colonial governance structure
2. slavernijverleden (1.0000, df=257)
3. curaçao (0.9780, df=223)
4. slavernijgeschiedenis (0.9405, df=23)
5. gouverneurschap (0.9090, df=2) - Colonial governance
6. koloniaal (0.8552, df=70)
7. koloniale (0.8481, df=503)

Note: Contemporary corruption terms (corruptie, nepotisme) were correctly REMOVED

---

## Validation Checks

### Expected KEEP Terms - Verified
- Racial ideology: racisme, discriminatie, raciale, etnisch ✓
- Historical slavery: slavernij, slavenhandel, slavenarbeid, plantages, koloniale ✓
- Caribbean localization: curaçao, surinaamse, papiamento, caribisch ✓
- Bridge terms: slavernijverleden, slavernijgeschiedenis, postkoloniale ✓

### Expected REMOVE Terms - Verified
- Economic outcomes: armoede, werkloosheid, schuld ✓
- Educational outcomes: schooluitval, lerarentekort ✓
- Migration flows: emigratie, immigratie, migratie ✓
- Contemporary governance: corruptie, nepotisme ✓

---

## Next Steps

1. **Use for Training**
   - Input: `curated_dictionary.csv` (371 terms)
   - Objective: Train BERTje on historical causes/structures of slavery
   - Focus: Dutch Caribbean context with colonial and racial ideology terms

2. **Prepare Iteration 2**
   - Review removed terms (1,098) for potential Iteration 2 dictionary
   - Focus on contemporary outcomes and manifestations
   - Will include: economic impacts, educational outcomes, migration patterns

3. **Quality Review**
   - Manually review "Not clearly historical/structural" category (1,053 terms)
   - Check for false negatives (historical terms incorrectly removed)
   - Domain expert validation of racial ideology categorization

4. **Training Configuration**
   - Ensure workflow_process uses curated_dictionary.csv
   - Verify topic-term associations are preserved
   - Monitor cosine similarity thresholds in training

---

## Methodology

### Curation Approach
- **Rule-based:** Regex patterns for each category
- **Semantic:** Context-aware categorization logic
- **Conservative:** Default to removal if unclear
- **Explicit:** Clear rationale for each decision category

### Pattern Categories
1. Historical slavery core (slavernij, slaven*, plantage*)
2. Colonial structures (koloni*, gouverneur, etc.)
3. Caribbean localization (curaçao, papiamento, caribisch)
4. Racial ideology (racisme, discriminatie, racial*, etnisch)
5. Bridge terms (slavernijverleden, postkolonial*)
6. Academic/historical (historisch, geschied*, archief)

### Removal Patterns
1. Economic outcomes (armoede, werkloosheid, schuld)
2. Educational outcomes (schooluitval, leerachterstanden)
3. Contemporary governance (corruptie, nepotisme)
4. Migration flows (emigratie, immigratie, migratie)
5. Generic contemporary problems

---

## Files Location

**Directory:** `c:\Users\Home\policy-analysis\workflow_data\slavery_Slavdict_pretraining_slavery_v2\Dictionary\`

```
Dictionary/
├── expanded_candidates.csv          (1,469 terms - original)
├── curated_dictionary.csv           (371 terms - FOR TRAINING)
├── CURATION_SUMMARY.md              (Full statistics)
├── CURATION_VERIFICATION.md         (Validation checks)
└── [previous versions if any]
```

**Script:** `c:\Users\Home\policy-analysis\curate_iteration1_dictionary.py`

---

## Impact on Training

### What BERTje Will Learn (Iteration 1)
- Historical slavery system and structures
- Colonial governance and institutions
- Dutch Caribbean geographic/linguistic context
- **Racial ideology as FOUNDATIONAL CAUSE**
- Plantation economy structures
- Historical documentation and analysis terms

### What Is Deferred (Iteration 2)
- Contemporary economic outcomes (poverty, unemployment)
- Educational disparities and challenges
- Migration patterns and flows
- Current governance problems
- Contemporary social problems

### Why This Matters
- **Causal Understanding:** BERTje learns the ROOT CAUSES before outcomes
- **Historical Accuracy:** Focuses on period-appropriate terminology
- **Domain Specificity:** Strong Caribbean localization
- **Ideological Foundations:** Properly positions racism as CAUSE, not just outcome

---

## Success Criteria

✓ Clear separation between historical causes and contemporary outcomes
✓ Racial ideology terms retained as foundational (not outcomes)
✓ Contemporary terms (armoede, werkloosheid, emigratie) correctly removed
✓ Historical slavery and colonial terms consistently kept
✓ Caribbean localization preserved
✓ 25.3% retention rate appropriate for focused training
✓ Explicit documentation of all decisions
✓ Reusable, transparent curation methodology

**Status: COMPLETE AND READY FOR ITERATION 1 TRAINING**
