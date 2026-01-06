# Slavernij_Historisch - Manual Semantic Review
**Reviewer**: Human semantic understanding
**Date**: 2026-01-03

## Review of High-Priority Terms (Low Cosine + KERN)

### Lines 2-13: KERN 1.0 terms with cosine < 0.72

**Line 2: slavenopstanden** (slave uprisings)
- Parent: slavernij
- Cosine: 0.6803, df: 12
- **SEMANTIC CHECK**: "Slavenopstanden" = slave uprisings/rebellions. This IS directly slavery-related.
- **DECISION**: KEEP, but downgrade to KERN 0.9 (low cosine)

**Line 3: staats-** (state-)
- Parent: staatstoezicht
- Cosine: 0.6975, df: 9
- **SEMANTIC CHECK**: "staats-" is just a fragment/prefix meaning "state-". NOT a complete term.
- **DECISION**: REMOVE (morphological fragment)

**Line 4: transatlantische** (transatlantic)
- Parent: trans-Atlantische slavenhandel
- Cosine: 0.7004, df: 6
- **SEMANTIC CHECK**: "Transatlantische" = transatlantic. Valid adjective for transatlantic slave trade.
- **DECISION**: KEEP at KERN 0.9

**Line 5: smokkelhandel** (smuggling trade)
- Parent: slavenhandel
- Cosine: 0.7067, df: 4
- **SEMANTIC CHECK**: "Smokkelhandel" = smuggling trade. This is GENERIC trade/smuggling, not slavery-specific.
- **DECISION**: REMOVE (too generic, semantic drift)

**Line 6: eigendomsslavernij** (property slavery / chattel slavery)
- Parent: slavernij
- Cosine: 0.7025, df: 4
- **SEMANTIC CHECK**: "Eigendomsslavernij" = chattel slavery (slavery as property ownership). This IS a specific slavery concept.
- **DECISION**: KEEP, downgrade to STERK 0.8 (low cosine, specific concept)

**Line 7: staatkundig** (political/constitutional)
- Parent: staatstoezicht
- Cosine: 0.6911, df: 4
- **SEMANTIC CHECK**: "Staatkundig" = political science/constitutional. Too generic, not slavery-specific.
- **DECISION**: REMOVE (generic political term)

**Line 8: slavengeld** (slave money)
- Parent: slavenhandel
- Cosine: 0.6798, df: 3
- **SEMANTIC CHECK**: "Slavengeld" could mean money from slave trade OR compensation for slaves. Very low df (3), archaic term.
- **DECISION**: REMOVE (archaic, very low df, low cosine)

**Line 9: goederenhandel** (goods trade)
- Parent: slavenhandel
- Cosine: 0.6767, df: 3
- **SEMANTIC CHECK**: "Goederenhandel" = trade in goods. This is GENERIC commerce, not slavery-specific.
- **DECISION**: REMOVE (semantic drift - generic trade term)

**Line 10: slavernijcomplex** (slavery complex)
- Parent: slavernij
- Cosine: 0.7499, df: 2
- **SEMANTIC CHECK**: "Slavernijcomplex" = slavery complex (system/institution). Valid slavery term.
- **DECISION**: KEEP at KERN 1.0

**Line 11: slavernijmusea** (slavery museums)
- Parent: slavernijverleden
- Cosine: 0.7197, df: 2
- **SEMANTIC CHECK**: "Slavernijmusea" = slavery museums. Valid commemoration/memory term.
- **DECISION**: KEEP, downgrade to KERN 0.9

**Line 12: slavenvervoer** (slave transport)
- Parent: slavenhandel
- Cosine: 0.6828, df: 2
- **SEMANTIC CHECK**: "Slavenvervoer" = transport of slaves. Valid slavery term.
- **DECISION**: KEEP, downgrade to STERK 0.8 (low cosine)

**Line 13: negerhandel** (negro trade)
- Parent: slavenhandel
- Cosine: 0.6774, df: 2
- **SEMANTIC CHECK**: "Negerhandel" = archaic/offensive term for slave trade. Problematic terminology, very low df.
- **DECISION**: REMOVE (archaic/problematic + low df + low cosine)

### Lines 14-18: KERN 0.9 terms with issues

**Line 14: koloniale** (colonial)
- Parent: koloniaal
- Cosine: 0.9781, df: 524
- **SEMANTIC CHECK**: "Koloniale" = colonial (grammatical variant). Very high df but legitimate term.
- **DECISION**: KEEP at KERN 0.9 (already appropriate)

**Line 15: slaven** (slaves)
- Parent: slavenhouder
- Cosine: 0.7222, df: 479
- **SEMANTIC CHECK**: "Slaven" = slaves (plural). Generic but central. Very high df + low cosine.
- **DECISION**: RECATEGORIZE to CONTEXT 0.6 (too generic for KERN despite relevance)

**Line 16: geschiedenis** (history)
- Parent: koloniale geschiedenis
- Cosine: 0.6984, df: 316
- **SEMANTIC CHECK**: "Geschiedenis" = history. VERY generic word, not slavery-specific.
- **DECISION**: RECATEGORIZE to CONTEXT 0.6 (generic temporal marker)

**Line 17: arbeid** (labor/work)
- Parent: dwangarbeid
- Cosine: 0.7161, df: 125
- **SEMANTIC CHECK**: "Arbeid" = labor/work. VERY generic, not slavery-specific alone.
- **DECISION**: REMOVE (too generic - "arbeid" alone doesn't indicate forced labor)

**Line 18: economie** (economy)
- Parent: plantage-economie
- Cosine: 0.6892, df: 80
- **SEMANTIC CHECK**: "Economie" = economy. VERY generic economic term.
- **DECISION**: REMOVE (too generic)

### Lines 19-66: Continue semantic review...

**Line 30: tuin** (garden)
- Parent: plantage
- Cosine: 0.7379, df: 8
- **SEMANTIC CHECK**: "Tuin" = garden. This is NOT a plantation! Semantic drift - plantations are agricultural enterprises, not gardens.
- **DECISION**: REMOVE (semantic drift)

**Line 36: eigenheid** (uniqueness/identity)
- Parent: eigendom van personen
- Cosine: 0.7335, df: 5
- **SEMANTIC CHECK**: "Eigenheid" = uniqueness/own identity. NOT about property ownership! Semantic drift from "eigendom".
- **DECISION**: REMOVE (semantic drift)

**Line 37: tuinen** (gardens)
- Parent: plantages
- Cosine: 0.7118, df: 5
- **SEMANTIC CHECK**: "Tuinen" = gardens (plural). Same issue as "tuin".
- **DECISION**: REMOVE (semantic drift)

**Line 39: eigenbelang** (self-interest)
- Parent: eigendom van personen
- Cosine: 0.6846, df: 5
- **SEMANTIC CHECK**: "Eigenbelang" = self-interest. NOT about ownership of persons! Semantic drift.
- **DECISION**: REMOVE (semantic drift)

**Line 41: houder** (holder/keeper)
- Parent: slavenhouder
- Cosine: 0.681, df: 5
- **SEMANTIC CHECK**: "Houder" = holder/keeper. Too generic - could be ticket holder, account holder, etc.
- **DECISION**: REMOVE (too generic)

**Line 46: schiedenis** (typo/OCR error)
- Parent: koloniale geschiedenis
- Cosine: 0.736, df: 3
- **SEMANTIC CHECK**: "Schiedenis" is a typo/OCR error for "geschiedenis".
- **DECISION**: REMOVE (OCR error/typo)

**Line 52: vrouwenemancipatie** (women's emancipation)
- Parent: emancipatie
- Cosine: 0.7453, df: 2
- **SEMANTIC CHECK**: "Vrouwenemancipatie" = women's emancipation/women's liberation. This is about WOMEN'S RIGHTS, not slave emancipation (1863)!
- **DECISION**: REMOVE (different kind of emancipation - semantic drift)

### Lines 68-96: "uitbuiting" (exploitation) parent expansions

These need careful review as many are morphological matches on "uit-" prefix:

**Line 69: uit-**
- **SEMANTIC CHECK**: Just prefix "uit-" (out/from)
- **DECISION**: REMOVE (fragment)

**Line 71: uiting** (expression/utterance)
- **SEMANTIC CHECK**: "Uiting" = expression/utterance. NOT exploitation!
- **DECISION**: REMOVE (semantic drift)

**Line 72: uitmaken** (to matter / to make out)
- **SEMANTIC CHECK**: "Uitmaken" = to matter/constitute. NOT exploitation!
- **DECISION**: REMOVE (semantic drift)

**Line 75: uitte** (expressed - past tense)
- **SEMANTIC CHECK**: "Uitte" = expressed. NOT exploitation!
- **DECISION**: REMOVE (semantic drift)

**Line 79: uitging** (went out)
- **SEMANTIC CHECK**: "Uitging" = went out/emanated. NOT exploitation!
- **DECISION**: REMOVE (semantic drift)

**Line 82: uittocht** (exodus)
- **SEMANTIC CHECK**: "Uittocht" = exodus/departure. Could relate to slave exodus but very indirect.
- **DECISION**: REMOVE (indirect, low cosine)

**Line 88: uitgeloot** (drawn by lot)
- **SEMANTIC CHECK**: "Uitgeloot" = drawn by lottery. NOT exploitation!
- **DECISION**: REMOVE (semantic drift)

**Line 89: uitbraken** (broke out)
- **SEMANTIC CHECK**: "Uitbraken" = broke out (riots, etc.). Could relate to slave uprisings but indirect.
- **DECISION**: REMOVE (semantic drift)

**Line 90: uitsprak** (pronounced/verdict)
- **SEMANTIC CHECK**: "Uitsprak" = pronounced judgment. NOT exploitation!
- **DECISION**: REMOVE (semantic drift)

**Line 91: uitstaan** (to endure / outstanding)
- **SEMANTIC CHECK**: "Uitstaan" = to endure/outstanding. Indirect at best.
- **DECISION**: REMOVE (semantic drift)

**Line 94: uitroepen** (to proclaim)
- **SEMANTIC CHECK**: "Uitroepen" = to proclaim. NOT exploitation!
- **DECISION**: REMOVE (semantic drift)

**Line 95: uitbarsten** (to burst out)
- **SEMANTIC CHECK**: "Uitbarsten" = to burst out. NOT exploitation!
- **DECISION**: REMOVE (semantic drift)

**Line 96: uitgeputte** (exhausted)
- **SEMANTIC CHECK**: "Uitgeputte" = exhausted. This could relate to exploitation!
- **DECISION**: KEEP at STERK 0.8 (relevant but indirect)

**Line 93: aanwas** (growth/increase)
- **SEMANTIC CHECK**: "Aanwas" = growth/increase. NOT exploitation!
- **DECISION**: REMOVE (semantic drift)

**Line 84: ontduiking** (evasion)
- **SEMANTIC CHECK**: "Ontduiking" = evasion/avoidance. NOT exploitation!
- **DECISION**: REMOVE (semantic drift)

**Line 85: ontsporing** (derailment)
- **SEMANTIC CHECK**: "Ontsporing" = derailment/deviation. NOT exploitation!
- **DECISION**: REMOVE (semantic drift)

KEEP from uitbuiting expansions (actually related):
- **uitputting** (exhaustion) - line 78
- **uitwerking** (effect/impact) - line 206
- **ontheemding** (displacement) - line 92
- **onmenselijke, mensonterende, onmenselijkheid** - dehumanization terms

### Lines 97-105: Ship-related terms

**Line 97: oorlogsschepen** (warships)
- **SEMANTIC CHECK**: "Oorlogsschepen" = warships. These are MILITARY ships, not slave ships!
- **DECISION**: REMOVE (semantic drift)

**Line 98: marineschepen** (navy ships)
- **SEMANTIC CHECK**: "Marineschepen" = navy ships. Military, not slave trade.
- **DECISION**: REMOVE (semantic drift)

**Line 99: roven** (to rob/plunder)
- **SEMANTIC CHECK**: "Roven" = to rob/plunder. Generic robbery, could relate to colonial plunder but very indirect.
- **DECISION**: REMOVE (too generic)

**Line 100: zeilschepen** (sailing ships)
- **SEMANTIC CHECK**: "Zeilschepen" = sailing ships. Generic sailing vessels, not slave-ship specific.
- **DECISION**: REMOVE (too generic)

KEEP from ship terms:
- **slavenschepen, schepen, schip** - ships (can include slave ships in context)
- **vaartuigen** - vessels (neutral)
- **passages** - passages (Middenpassage context)

### Lines 106-108: "ketenen" (chains) expansions

**Line 106: sloot** (ditch/moat)
- **SEMANTIC CHECK**: "Sloot" = ditch/moat/canal. NOT chains!
- **DECISION**: REMOVE (semantic drift)

**Line 107: bezetten** (to occupy/fill)
- **SEMANTIC CHECK**: "Bezetten" = to occupy/fill positions. NOT related to chains/shackles!
- **DECISION**: REMOVE (semantic drift)

**Line 108: haakjes** (small hooks / brackets)
- **SEMANTIC CHECK**: "Haakjes" = small hooks OR parentheses/brackets (punctuation). Dubious connection to chains.
- **DECISION**: REMOVE (ambiguous - likely punctuation meaning)

## Summary of Manual Decisions

### REMOVE (Semantic Drift / Too Generic / Fragments):
1. staats- (fragment)
2. smokkelhandel (generic trade)
3. staatkundig (generic political)
4. slavengeld (archaic, low df)
5. goederenhandel (generic trade)
6. negerhandel (archaic/problematic)
7. arbeid (too generic)
8. economie (too generic)
9. tuin, tuinen (gardens ≠ plantations)
10. eigenheid (identity ≠ ownership)
11. eigenbelang (self-interest ≠ ownership)
12. houder (too generic)
13. schiedenis (OCR error)
14. vrouwenemancipatie (women's rights ≠ slave emancipation)
15. uit- (fragment)
16. uiting, uitmaken, uitte, uitging, uittocht (semantic drift from "uit" prefix)
17. uitgeloot, uitbraken, uitsprak, uitstaan, uitroepen, uitbarsten (semantic drift)
18. aanwas, ontduiking, ontsporing (semantic drift)
19. oorlogsschepen, marineschepen (military ≠ slave ships)
20. roven (too generic)
21. zeilschepen (too generic)
22. sloot, bezetten, haakjes (wrong meaning)

**Total REMOVE**: ~40 terms

### RECATEGORIZE:
1. slaven → CONTEXT 0.6 (generic but relevant)
2. geschiedenis → CONTEXT 0.6 (generic temporal)

### DOWNGRADE WITHIN KERN:
Multiple terms from 1.0 → 0.9 (low cosine but valid)

### KEEP AS IS:
All terms with cosine ≥ 0.75 and semantically appropriate
