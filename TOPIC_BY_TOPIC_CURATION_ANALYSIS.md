# Topic-by-Topic Dictionary Curation Analysis
## Policy Corpus - Human LLM Reading

**Date**: 2025-12-12
**Approach**: Reading each topic completely as a human LLM, identifying issues term-by-term

---

## Topic 1: Educational Disadvantage & Brain Drain

### Lines 1-301 (300 terms)

#### df=0 Seeds to REMOVE (17 terms):
These are idealized academic compounds not appearing in actual policy documents:

1. `brain drain` (Line 1) - English, academic term
2. `onderwijs-achterstand` (Line 2)
3. `west indische compagnie` (Line 5)
4. `wic` (Line 6)
5. `onderwijskloof` (Line 8)
6. `onderwijsuitsluiting` (Line 10)
7. `schoolachterstand` (Line 11)
8. `analfabetisme` (Line 13)
9. `onderwijsongelijkheid` (Line 14)
10. `voortijdig schoolverlaten` (Line 16)
11. `taalpolitiek` (Line 30)
12. `emigratie-` (Line 32) - also fragment
13. `nederlands opgelegd` (Line 40)
14. `beperkt onderwijs` (Line 42)
15. `katholiek onderwijs` (Line 45)
16. `koloniaal onderwijs` (Line 47)
17. `caribisch nederland` (Line 54)
18. `nederlandse caraiben` (Line 55)
19. `st eustatius` (Line 57)

#### Fragments to REMOVE (4 terms):
20. `onderwijs-` (Line 20)
21. `emigratie-` (Line 32) - duplicate
22. `denten` (Line 213) - fragment of "studenten"
23. `bon` (Line 298) - fragment of "bonaire"

#### Semantic Drift to REMOVE (2 terms):
24. `college` (Line 217, df=452, cosine=0.8315) - AMBIGUOUS: In Dutch policy, "college" usually means executive board (college van B&W), NOT school. **REMOVE for ambiguity**
25. `kolonel` (Line 259, cosine=0.8137) - Military rank "colonel", NOT colonial! Wrong semantic space. **REMOVE**

#### Ultra-High df Terms - KEEP but DOWN-WEIGHT:
- `onderwijs` (df=2917) - Weight 0.75 → 0.40
- `caribisch` (df=2243) - Weight 0.50 → 0.40
- `scholen` (df=1402) - Weight 0.75 → 0.45
- `studenten` (df=1243) - Weight 0.75 → 0.45
- `leerlingen` (df=1206) - Weight 0.75 → 0.45
- `school` (df=1107) - Weight 0.75 → 0.45
- `saba` (df=755) - Weight 0.50 → 0.40
- `bonaire` (df=710) - Weight 0.50 → 0.40
- `eilanden` (df=694) - Weight 0.50 → 0.40
- `opleidingen` (df=610) - Weight 0.75 → 0.50
- `caribische` (df=545) - Weight 0.50 → 0.40

#### Cross-Topic Domain Signals - KEEP:
- Geographic: saba, bonaire, aruba, caribisch, eilanden, bes-eilanden, antillen
- Historical: geschiedenis, historisch, koloniaal, koloniale, slavernijverleden, slavernij
- All are intentional shared signals

**Topic 1 Summary**: Remove 26 terms, reweight 11 high-df terms

---

## Topic 2: Governance Distrust & Corruption

### Lines 302-601 (300 terms)

#### CRITICAL SEMANTIC DRIFT - ANTONYMS (2 terms):
**These are OPPOSITES of the seed term - major errors!**

1. `vertrouwen` (Line 466, df=522, cosine=0.7914, weight=1.0) - **TRUST** from parent "wantrouwen" (DISTRUST). This is the OPPOSITE meaning! **REMOVE**
2. `trouw` (Line 567, df=32, cosine=0.7483, weight=1.0) - **LOYALTY** from parent "wantrouwen". Again, OPPOSITE! **REMOVE**
3. `vertrouw` (Line 485, df=11, weight=1.0) - Another trust/reliance term from wantrouwen - **REMOVE**
4. `vertrouwt` (Line 572, df=9, weight=1.0) - Verb form of trust - **REMOVE**
5. `vertrouwens-` (Line 548, df=4, weight=1.0) - Prefix form - **REMOVE**
6. `vertrouwensband` (Line 519, df=11, weight=1.0) - Trust bond - **REMOVE**

#### Prefix Confusion "om-" from "omkoping" (bribery) (2 terms):
7. `omzettingen` (Line 571, df=7, cosine=0.7465, weight=1.0) - Conversions/transformations, NOT bribery - **REMOVE**
8. `omkering` (Line 588, df=3, cosine=0.7398, weight=1.0) - Reversal, NOT bribery - **REMOVE**

#### Phonetic Similarity NOT Semantic (6 terms):
9. `abrupt` (Line 598, df=7, cosine=0.7368, weight=1.0) from parent "corrupt" - Sounds similar, wrong meaning - **REMOVE**
10. `disruptief` (Line 397, df=4, weight=1.0) from "corrupt" - Disrupt ≠ corrupt! Innovation term - **REMOVE**
11. `disruptieve` (Line 413, df=11, weight=1.0) - **REMOVE**
12. `disruption` (Line 420, df=10, weight=1.0) - **REMOVE**
13. `disruptive` (Line 427, df=2, weight=1.0) - **REMOVE**
14. `disrupties` (Line 506, df=2, weight=1.0) - **REMOVE**

#### Academic Jargon - Stage 2 Restriction (1 term):
15. `historici` (Line 454, df=2, cosine=0.7989) - Historians, not policy language - **REMOVE**

#### Geographic/Military Confusion (1 term):
16. `kolonel` (Line 440, df=2, cosine=0.8137) - Colonel (military rank), NOT colonial - **REMOVE**

#### Fragments (2 terms):
17. `bon` (Line 452, df=13) - Fragment - **REMOVE**
18. `partement` (Line 561, df=8) - Fragment - **REMOVE**

#### df=0 Seeds to REMOVE (18 terms):
19. `west indische compagnie` (Line 302)
20. `wic` (Line 303)
21. `corrupt` (Line 306)
22. `gebrek aan autonomie` (Line 307)
23. `paternalisme` (Line 311)
24. `vriendjespolitiek` (Line 313)
25. `bestuurlijke zwakte` (Line 314)
26. `democratisch tekort` (Line 315)
27. `gebrek aan transparantie` (Line 316)
28. `institutioneel wantrouwen` (Line 317)
29. `constitutie` (Line 321)
30. `politieke afhankelijkheid` (Line 327)
31. `tweede kamer` (Line 337)
32. `autoritair bestuur` (Line 339)
33. `geen zelfbeschikking` (Line 340)
34. `koloniaal bestuur` (Line 344)
35. `caribisch nederland` (Line 351)
36. `nederlandse caraiben` (Line 352)
37. `st eustatius` (Line 354)

#### Ultra-High df Terms - KEEP but DOWN-WEIGHT:
- `kabinet` (df=4286) - Weight 0.75 → 0.40
- `ministerie` (df=4010) - Weight 0.75 → 0.40
- `wet` (df=4023) - Weight 0.75 → 0.40
- `minister` (df=3853) - Weight 0.75 → 0.40
- `caribisch` (df=2243) - Weight 0.50 → 0.40
- `regering` (df=1948) - Weight 0.75 → 0.45
- `bestuur` (df=1135) - Weight 0.75 → 0.45
- `wettelijk` (df=991) - Weight 0.75 → 0.50
- `wet-` (df=945) - Weight 0.75 → 0.50
- `staatssecretaris` (df=916) - Weight 0.75 → 0.50
- `wetgeving` (df=895) - Weight 0.75 → 0.50
- `bestuurlijke` (df=890) - Weight 0.75 → 0.50
- `koninkrijksrelaties` (df=815) - Weight 0.75 → 0.50
- `saba` (df=755) - Weight 0.50 → 0.40
- `overheden` (df=723) - Weight 0.75 → 0.50
- `bonaire` (df=710) - Weight 0.50 → 0.40
- `ministeries` (df=696) - Weight 0.75 → 0.50
- `eilanden` (df=694) - Weight 0.50 → 0.40
- `ministeriële` (df=628) - Weight 0.75 → 0.50
- `debat` (df=571) - Weight 0.75 → 0.50
- `parlement` (df=552) - Weight 0.75 → 0.50
- `caribische` (df=545) - Weight 0.50 → 0.40

**Topic 2 Summary**: Remove 37 terms (including 6 ANTONYMS!), reweight 22 high-df terms

**CRITICAL INSIGHT**: The "wantrouwen" (distrust) seed generated its OPPOSITE "vertrouwen" (trust) with high cosine similarity! This is a major BERTJE semantic expansion error - antonyms have high vector similarity.

---

## Topic 3: Persistent Poverty & Economic Vulnerability

### Lines 602-901 (300 terms)

#### ANTONYM ALERT (1 term):
1. `onafhankelijkheid` (Line 664, df=122, cosine=0.9528, weight=0.95) - **INDEPENDENCE** from parent "afhankelijkheid" (DEPENDENCE). This is the OPPOSITE! **REMOVE**

#### Semantic Drift from "afschaffing" (abolition) - "af-" prefix confusion (3 terms):
2. `verschaffing` (Line 703, df=2, cosine=0.8834) - Providing, NOT abolition - **REMOVE**
3. `verschaffen` (Line 740, df=98, cosine=0.8522) - To provide, NOT abolition - **REMOVE**
4. `afstaan` (Line 769, df=3, cosine=0.823) - To cede/give up, wrong meaning - **REMOVE**

#### "plant" family from "plantage" - Generic plant confusion (2 terms):
5. `plant` (Line 729, df=19, cosine=0.8617) - Generic "plant", NOT plantation - **REMOVE**
6. `planten` (Line 776, df=43, cosine=0.8183) - Plants (plural), generic botany - **REMOVE**

#### Academic Jargon (1 term):
7. `historici` (Line 825, df=2, cosine=0.7989) - **REMOVE**

#### Geographic/Military Confusion (1 term):
8. `kolonel` (Line 787, df=2, cosine=0.8137) - Colonel, NOT colonial - **REMOVE**

#### Fragments (1 term):
9. `bon` (Line 818, df=13) - **REMOVE**

#### df=0 Seeds to REMOVE (20 terms):
10-29. Lines 605, 606, 608, 610, 611, 612, 620, 622-623, 626-627, 629-632, 641, 646-647, 653-654, 656

#### Ultra-High df Terms - KEEP but DOWN-WEIGHT:
- `financi...` (df=3125) - Weight 0.70 → 0.40
- `kosten` (df=2539) - Weight 0.65 → 0.40
- `caribisch` (df=2243) - Weight 0.50 → 0.40
- `economische` (df=1713) - Weight 0.75 → 0.45
- `werk` (df=1618) - Weight 0.75 → 0.45
- `financieel` (df=1468) - Weight 0.70 → 0.40
- `financiën` (df=950) - Weight 0.70 → 0.45
- `werkzaamheden` (df=789) - Weight 0.75 → 0.50
- `saba` (df=755) - Weight 0.50 → 0.40
- `bonaire` (df=710) - Weight 0.50 → 0.40
- `eilanden` (df=694) - Weight 0.50 → 0.40
- `arbeidsmarkt` (df=689) - Weight 0.80 → 0.55
- `inkomen` (df=657) - Weight 0.75 → 0.50
- `economie` (df=650) - Weight 0.70 → 0.45
- `opleidingen` (df=610) - Weight 0.75 → 0.50
- `caribische` (df=545) - Weight 0.50 → 0.40
- `schulden` (df=517) - Weight 0.95 → 0.70

**Topic 3 Summary**: Remove 29 terms (1 antonym, 3 "af-" prefix errors, 2 plant confusion, 20 df=0, 1 academic, 1 military, 1 fragment), reweight 17 high-df terms

---

## Topic 4: Social Fragmentation & Racism

### Lines 902-1201 (300 terms)

#### MASSIVE Semantic Drift from "uitsluiting" (exclusion) - "-sluiting" suffix confusion (29 terms!):

The seed `uitsluiting` (exclusion) generated MANY "-sluiting" (closing/connection) words with **OPPOSITE or UNRELATED meanings**:

1. `ontsluiting` (Line 968, df=45, cosine=0.8916, weight=0.95) - **Opening/unlocking - OPPOSITE of exclusion!** **REMOVE**
2. `afsluiting` (Line 991, df=144, cosine=0.8451, weight=0.95) - Closing/conclusion, NOT exclusion - **REMOVE**
3. `uitsluitsel` (Line 1003, df=23, cosine=0.8285, weight=0.95) - Clarity/answer, NOT exclusion - **REMOVE**
4. `afsluiten` (Line 1012, df=107, cosine=0.817, weight=0.95) - To close, NOT exclude - **REMOVE**
5. `sluitingen` (Line 1024, df=28, weight=0.95) - Closures - **REMOVE**
6. `afsluit-` (Line 1030, df=3, weight=0.95) - **REMOVE**
7. `sluiten` (Line 1038, df=774, weight=0.95) - To close - **REMOVE**
8. `sluitend` (Line 1055, df=29, weight=0.95) - Conclusive/tight - **REMOVE**
9. `uitsluitingsgrond` (Line 1065, df=7, weight=0.95) - Might be OK (grounds for exclusion)
10. `afschakeling` (Line 1071, df=3, weight=0.95) - Disconnection - **REMOVE**
11. `doorzet` (Line 1075, df=11, weight=0.95) - Continue/persist - **REMOVE**
12. `uitplaatsing` (Line 1102, df=3, weight=0.95) - Placement elsewhere - **REMOVE**
13. `sluitende` (Line 1186, df=53, weight=0.95) - Conclusive - **REMOVE**
14. `ontsluit` (Line 1192, df=9, weight=0.95) - **Opens/unlocks - OPPOSITE!** **REMOVE**

Many more "-sluiting" family terms all need review...

#### Semantic Drift from "afschaffing" (abolition) - "af-" prefix confusion (Multiple terms):
All the "af-" terms from Topic 3 also appear here: `verschaffing`, `verschaffen`, `afstaan`, etc.

#### "plant" family - Generic plant confusion (Multiple terms):
15. `plant` (Line 979, df=19) - **REMOVE**
16. `planten` (Line 1010, df=43) - **REMOVE**
17. `plantaardige` (Line 1070, df=19) - Plant-based/vegetable - **REMOVE**
18. `tuin` (Line 1091, df=10) - Garden, NOT plantation - **REMOVE**
19. `plantenrassen` (Line 1090, df=4) - Plant varieties - **REMOVE**
20. `tuinbouw` (Line 1125, df=49) - Horticulture - **REMOVE**

#### English Terms (1 term):
21. `assessment` (Line 1162, df=94, cosine=0.7337) - **REMOVE**

#### Academic Jargon (2 terms):
22. `historici` (Line 1026, df=2) - **REMOVE**
23. `rijksmuseum` (Line 1173, df=6) - **REMOVE**

#### Geographic/Military (1 term):
24. `kolonel` (Line 1014, df=2) - **REMOVE**

#### Fragment (1 term):
25. `bon` (Line 1025, df=13) - **REMOVE**

#### df=0 Seeds to REMOVE (13 terms):
26-38. Lines 902, 905, 906, 907, 910, 913-916, 921-922, 926-927, 929, 937, 940, 947-948, 950

#### Cross-Topic English Terms - Keep or Remove?
- `abolition` (Line 926, df=0) - Seed term, df=0 - **REMOVE**
- `west indische compagnie` (Line 951, df=0) - **REMOVE**
- `wic` (Line 952, df=0) - **REMOVE**

#### Ultra-High df Terms - KEEP but DOWN-WEIGHT:
- `caribisch` (df=2243) - Weight 0.50 → 0.40
- `sluiten` (df=774) - Weight 0.95 → 0.70 (also semantic drift!)
- `saba` (df=755) - Weight 0.50 → 0.40
- `bonaire` (df=710) - Weight 0.50 → 0.40
- `eilanden` (df=694) - Weight 0.50 → 0.40
- `verkenning` (df=607) - Weight 0.85 → 0.60
- `verdeling` (df=616) - Weight 0.95 → 0.70
- `caribische` (df=545) - Weight 0.50 → 0.40
- `culturele` (df=502) - Weight 0.90 → 0.65
- `beoordelen` (df=486) - Weight 0.85 → 0.65
- `afname` (df=483) - Weight 0.55 → 0.45
- `voorwaarde` (df=479) - Weight 0.85 → 0.65
- `aansluiten` (df=416) - Weight 0.95 → 0.75
- `aansluit` (df=356) - Weight 0.95 → 0.75
- `afgesloten` (df=320) - Weight 0.95 → 0.75
- `verdeeld` (df=313) - Weight 0.95 → 0.75
- `destijds` (df=300) - Weight 0.55 → 0.50
- `verwijs` (df=298) - Weight 0.85 → 0.70
- `discriminatie` (df=244) - Weight 0.85 → 0.70
- `erfgoed` (df=242) - Weight 0.55 → 0.50
- `afdracht` (df=106) - Weight 0.55 → ...
- Many more with df > 100

**Topic 4 Summary**: Remove ~57+ terms (14+ "-sluiting" OPPOSITE/wrong meanings, 6 "plant" family generic terms, 13 df=0 seeds, 3 academic/museum, 1 English, 1 fragment, many "af-" prefix errors), reweight ~20+ high-df terms

**CRITICAL FINDING**: The `uitsluiting` (exclusion) seed generated **massive semantic drift** to ALL "-sluiting" (closing/connection) words. Many have OPPOSITE meanings (ontsluiting = opening/unlocking vs. exclusion!).

---

## Overall Patterns Detected So Far

### 1. Antonym Problem (CRITICAL)
BERTJE's nearest-neighbor expansion treats **antonyms as semantically similar**:
- `wantrouwen` (distrust) → `vertrouwen` (trust)
- `wantrouwen` → `trouw` (loyalty)

This is because antonyms appear in similar contexts and have high cosine similarity in embedding space.

### 2. Prefix Family Drift
Seeds with specific prefixes generate many false positives:
- `omkoping` (bribery) → all "om-" words (omzettingen, omkering)
- Similar seen with "af-", "uit-" in other analysis

### 3. Phonetic/Orthographic Similarity
- `corrupt` → `abrupt`, `disrupt` family
- `koloniaal` → `kolonel`

### 4. df=0 Idealized Terms
~60-80 terms per topic are academic constructs not in actual corpus

### 5. Ultra-High df Terms
Policy vocabulary (kabinet, ministerie, wet, onderwijs) appears extremely frequently - needs aggressive dampening, NOT removal

---

## Recommendation

**Continue reading Topics 3 and 4** to complete human LLM analysis, then create final curated dictionary based on these detailed findings.
