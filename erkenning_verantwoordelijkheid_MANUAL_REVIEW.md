# Erkenning_Verantwoordelijkheid - Manual Semantic Review
**Topic**: Recognition & Responsibility (acknowledgment of slavery, apologies, redress)
**Reviewer**: Human semantic understanding
**Date**: 2026-01-03

## Review Focus

This topic is about **erkenning** (recognition/acknowledgment) and **verantwoordelijkheid** (responsibility) for slavery - apologies, accountability, redress, reparations. Key question: Is this term about acknowledging historical wrongs, or just generic responsibility/justice/legal concepts?

## Semantic Drift Patterns

### 1. "schuld" (debt/guilt) → financial debt terms

**CRITICAL**: "Schuld" in Dutch means BOTH "guilt" AND "debt"!

**Lines 13, 40, 43, 47, 60, 63, 73, 80, 87, 96, 98, 130**:
- schuld (RISICO 0.3, df 49)
- onschuld (innocence)
- schuldgevoel (guilt feeling) - KEEP
- schulden (debts - financial!)
- schuldgevoelens (guilt feelings) - KEEP
- schuldslaven (debt slaves - could be relevant)
- schuldhulpverlening (debt assistance - social service!)
- schuldenproblematiek (debt problems - economic!)
- schuldbekentenis (confession of guilt) - KEEP
- staatsschuld (state debt - government finance!)
- schuldenaren (debtors - financial!)
- studieschuld (student debt - education finance!)

**SEMANTIC CHECK**:
- "schulden", "schuldhulpverlening", "schuldenproblematiek", "staatsschuld", "schuldenaren", "studieschuld" are about FINANCIAL DEBT, not moral/historical guilt!
- "schuldgevoel", "schuldgevoelens", "schuldbekentenis" are about guilt/remorse - KEEP
- "schuldslaven" (debt slaves) - ambiguous but could relate to bondage

**DECISION**:
- REMOVE: schuldhulpverlening, schuldenproblematiek, staatsschuld, schuldenaren, studieschuld, schulden (financial debt terms)
- KEEP: schuldgevoel, schuldgevoelens, schuldbekentenis (guilt/remorse)
- KEEP: schuld, onschuld, schuldslaven (borderline but potentially relevant)

### 2. "herstel" (recovery/restoration) → generic recovery/renovation

**Lines 15, 32, 38-39, 41-42, 48, 53-54, 56, 71, 78, 82, 85, 117**:
- herstel (df 82 - generic)
- herstel- (fragment)
- herstellen (to restore/repair)
- hersteloperatie, hersteloperaties (restoration operations)
- rechtsherstel (legal restoration)
- hersteld (restored)
- recovery (English!)
- herstelopdracht (restoration task)
- reparatie (repair/reparations - KEEP)
- herstelbetaling, herstelbetalingen (restoration payments - KEEP)
- renovatie (renovation - buildings!)
- herinrichting (reorganization/refurbishment)
- ontslagen (dismissed/laid off - NOT restoration!)

**SEMANTIC CHECK**:
- "renovatie" = renovation of buildings, NOT historical redress!
- "herinrichting" = reorganization/refurbishment, too generic
- "ontslagen" = dismissed/fired - NOT about restoration!
- "recovery" = English word
- "reparatie" = repair BUT also reparations - KEEP
- "herstelbetaling(en)" = restoration payments - could be reparations - KEEP

**DECISION**:
- REMOVE: renovatie, herinrichting, ontslagen, recovery (English)
- KEEP: herstel seeds, reparatie, herstelbetaling(en), hersteloperatie (operational terms)

### 3. "rechtvaardigheid" (justice) → generic legal/judicial terms

**Lines 26, 57-58, 65-69, 74, 76, 88, 91, 93-94, 101-102, 113, 116, 119, 125, 136**:
- rechtvaardigheid (df 9 - OK as seed)
- rechtspositie (legal position)
- rechtspraak (judiciary/jurisprudence)
- rechtmatigheid (legality)
- recht (law/right - df 146!)
- rechtspleging (legal proceedings)
- onrechtvaardigheid (injustice) - KEEP
- recht- (fragment)
- rechtvaardige (just/fair)
- wederrechtelijkheid (unlawfulness)
- rechtvaardigingen (justifications)
- oprechtheid (sincerity)
- rechtvaardig (just)
- rechtshulp (legal aid)
- onrechtvaardigheden (injustices) - KEEP
- rechtsbescherming (legal protection)
- rechtvaardigingsgrond (justification ground)
- vaardigheid (skill!)
- rechtssysteem (legal system)
- rechtsorde (legal order)
- gerechtigheid (justice)

**SEMANTIC CHECK**:
- "recht" (df 146) - ultra-generic "law/right"!
- "rechtspraak", "rechtspleging", "rechtshulp", "rechtsbescherming", "rechtssysteem", "rechtsorde" - generic legal system terms
- "vaardigheid" = skill (from "recht-vaardigheid") - NOT justice!
- "oprechtheid" = sincerity - generic virtue
- "rechtvaardige", "rechtvaardig", "wederrechtelijkheid", "rechtmatigheid" - generic legal concepts

**DECISION**:
- REMOVE: recht (ultra-high df), rechtspraak, rechtspleging, recht-, rechtshulp, rechtsbescherming, rechtssysteem, rechtsorde, rechtspositie, rechtmatigheid, wederrechtelijkheid, rechtvaardigingen, oprechtheid, rechtvaardig, rechtvaardige, rechtvaardigingsgrond, vaardigheid
- KEEP: rechtvaardigheid (seed), onrechtvaardigheid, onrechtvaardigheden, gerechtigheid (justice-specific)

### 4. "verantwoording" (accountability) → control/management

**Lines 10, 37, 84, 86, 99, 110-111**:
- verantwoording (df 39 - OK)
- verantwoord (responsible/justified)
- beheersen (to control/manage)
- beheersten (controlled - past tense)
- beheersing (control/mastery) - df 22
- bewaking (guarding/monitoring)
- beheerste (controlled/moderate)

**SEMANTIC CHECK**:
- "beheersen", "beheersten", "beheersing", "bewaking", "beheerste" = control/management/monitoring - NOT accountability!

**DECISION**: REMOVE ALL (semantic drift - control ≠ accountability)

### 5. "erkenning" (recognition) → ultra-generic verbs

**Lines 2, 55, 62, 81, 97, 104, 107-109, 112, 115, 124, 127, 133, 135, 138, 142**:
- erkenning (df 98 - high but seed)
- werven (to recruit!)
- strijden (to fight)
- vereist (required)
- ties (English! or fragment)
- stelling (statement/position)
- verminderde (decreased)
- afhandeling (settlement/handling)
- proef (test/trial)
- voorbereid (prepared)
- speelt (plays - df 87!)
- verstrekking (provision/supply)
- stellen (to state - df 209!)
- verre (far)
- neer (down)
- maatregel (measure - df 30)
- woordenboek (dictionary!)

**SEMANTIC CHECK**:
- "werven" = to recruit - NOT recognition!
- "strijden" = to fight/struggle - could relate to struggle FOR recognition, but indirect
- "ties" = English word or fragment!
- "stelling" = position/statement - too generic
- "verminderde", "voorbereid", "speelt", "verre", "neer" = ultra-generic verbs/adjectives
- "stellen" (df 209!) = to state/put - ultra-generic verb!
- "woordenboek" = dictionary - NOT recognition!
- "maatregel" = measure/policy - too generic

**DECISION**:
- REMOVE: werven, ties, stelling, verminderde, afhandeling, proef, voorbereid, speelt, verstrekking, stellen, verre, neer, maatregel, woordenboek
- KEEP: strijden (struggle for recognition - borderline), vereist (required - borderline)

### 6. "staatsverantwoordelijkheid" (state responsibility) → generic state terms

**Lines 52, 61, 75, 79, 83, 103, 106, 114, 118, 120, 131-132, 134, 139**:
- staatstoezigt (state supervision - typo variant)
- staatsbestel (state system)
- staatsrechtelijke (constitutional)
- staatsinrichting (state organization)
- staatsregeling (state regulation)
- staatsexamens (state exams!)
- staatssteun (state aid)
- staats- (fragment)
- staatswijsheid (state wisdom/statesmanship)
- staatkundig (political science/statecraft)
- staatscommissie, staatcommissie (state commission)
- historische (historical - df 120!)
- staat- (fragment)

**SEMANTIC CHECK**:
- "staatsexamens" = state exams (education!) - NOT responsibility!
- "staatswijsheid" = statesmanship - generic political quality
- "staatssteun" = state aid (EU competition law term!)
- "historische" (df 120) - ultra-generic adjective

**DECISION**:
- REMOVE: staatsexamens, staatswijsheid, staatssteun, historische (ultra-high df), staats-, staat-
- KEEP: staatstoezigt, staatsbestel, staatsrechtelijke, staatsinrichting, staatsregeling, staatkundig, staatscommissie/staatcommissie (could relate to slavery commissions)

### 7. "aansprakelijkheid" (liability) → obstacles/insurance

**Lines 105, 122, 141, 143**:
- belemmeringen (obstacles/hindrances)
- beschuldigingen (accusations) - KEEP
- belemmering (obstacle)
- verzekerd (insured!)

**SEMANTIC CHECK**:
- "belemmeringen", "belemmering" = obstacles - NOT liability!
- "verzekerd" = insured (insurance term) - NOT liability in legal sense!

**DECISION**:
- REMOVE: belemmeringen, belemmering, verzekerd
- KEEP: beschuldigingen (accusations - related to accountability)

### 8. English words

**Line 49: recovery** (English for herstel)
**Line 97: ties** (English or fragment)

**DECISION**: REMOVE

### 9. Fragments

**Line 32: herstel-**
**Line 69: recht-**
**Line 89: slavernij-** (but could be compound prefix)
**Line 92: reken-**
**Line 114: staats-**
**Line 139: staat-**

**DECISION**: REMOVE all fragments

### 10. Ultra-high df terms

**Line 66: recht** (df 146)
**Line 115: speelt** (df 87)
**Line 123: vertrouwen** (df 70)
**Line 127: stellen** (df 209)
**Line 134: historische** (df 120)

**DECISION**: REMOVE (too generic)

## Summary of Manual Decisions

### REMOVE (~55 terms):

**Financial debt (not guilt)**: schulden, schuldhulpverlening, schuldenproblematiek, staatsschuld, schuldenaren, studieschuld

**Generic recovery/renovation**: renovatie, herinrichting, ontslagen, recovery

**Generic legal/judicial**: recht, rechtspraak, rechtspleging, recht-, rechtshulp, rechtsbescherming, rechtssysteem, rechtsorde, rechtspositie, rechtmatigheid, wederrechtelijkheid, rechtvaardigingen, oprechtheid, rechtvaardig, rechtvaardige, rechtvaardigingsgrond, vaardigheid

**Control/management (not accountability)**: beheersen, beheersten, beheersing, bewaking, beheerste

**Generic erkenning expansions**: werven, ties, stelling, verminderde, afhandeling, proef, voorbereid, speelt, verstrekking, stellen, verre, neer, maatregel, woordenboek

**Generic state terms**: staatsexamens, staatswijsheid, staatssteun, historische, staats-, staat-

**Obstacles/insurance (not liability)**: belemmeringen, belemmering, verzekerd

**English/fragments**: recovery, ties, herstel-, recht-, reken-, staats-, staat-

**Total REMOVE**: ~55 terms

### KEEP (~85 terms):
- All seeds
- Valid acknowledgment/responsibility terms
- Historical justice terms
- Redress/reparations terms (reparatie, herstelbetaling, etc.)
- Guilt/remorse terms (schuldgevoel, schuldbekentenis)
- Injustice terms (onrechtvaardigheid, onrechtvaardigheden)

**Final estimate**: ~85 terms (from 143)
