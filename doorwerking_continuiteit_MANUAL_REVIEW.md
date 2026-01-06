# Doorwerking_Continuiteit - Manual Semantic Review
**Topic**: Continuity/Legacy Effects (structural continuation of slavery/colonial patterns)
**Reviewer**: Human semantic understanding
**Date**: 2026-01-03

## Review Focus

This topic is about **doorwerking** (continuation/legacy effects) - how slavery and colonialism continue to affect contemporary society structurally. Key question: Is this term about historical continuity/structural legacy, or just generic policy/administrative language?

## Critical Finding: RISICO Category Over-Expansion

**MAJOR ISSUE**: Lines 27-266 contain 150+ RISICO 0.3 terms that are ULTRA-GENERIC administrative/policy language with NO specific connection to slavery legacy:
- Generic policy terms: "doelmatigheid", "efficiëntie", "uitvoering", "monitoring", "indicatoren"
- Generic time markers: "toenmalig", "in die tijd", "vroeger", "destijds"
- Generic discussion: "discussie", "debat", "overleg", "dialoog"
- Generic process: "procesmatig", "processen", "procedures"
- Ultra-high df terms: "tijd" (404), "geval" (298), "politiek" (125), "context" (110), "uitvoering" (190), "discussie" (86)

**DECISION**: Remove ALL RISICO 0.3 terms. These were categorized as RISICO (risky/ambiguous) specifically because they're NOT clearly about slavery legacy - they're generic policy language.

## Specific Semantic Drift Patterns

### 1. "losstaand" (separate/isolated) → position/status verbs

**Lines 81-100, 143, 157, 173, 177, 183-189, 205, 209-210, 223, 236, 239, 247, 266**:
- losse, vaststaand, losgemaakt, staande, uitgezonderd, achtergesteld, bezat, kosteloos, vastgelegde, ontslagen, afgesloten, afgelegen, geheven, uiterste, vast, overstaan, behouden, uitstaande, scheiden, afwezig

- **SEMANTIC CHECK**: These are about physical position (standing, lying, closed), NOT about causal isolation/independence!
- **DECISION**: REMOVE ALL (semantic drift - position verbs ≠ causal separation)

### 2. "uitvoering" (execution/implementation) → uit- prefix drift

**Lines 31, 90, 93, 113, 119-122, 125, 134, 137, 141, 145, 152, 155, 159, 166, 175, 193, 201, 215-216, 221, 230, 238, 248, 253**:
- uitvoering (190 df!), uitoefening, uitvoeringspraktijk, uitwerken, stelling, uitgeoefend, uitvoert, versie, uitvoerig, uitoefenen, voorbereid, uitvoerige, uitgevoerd, voorbereiding, vervoeren, uitvoer, realisatie, stelde, afhandeling, inrichting, voorbereidend, programmering, voorbereiden, uitgave, verstrekking, uitleg, uitkomsten

- **SEMANTIC CHECK**: Ultra-generic implementation/execution terms. "Uitvoering" has df=190 - appears in almost ANY policy document!
- **DECISION**: REMOVE ALL (ultra-generic policy administration)

### 3. "nuancering" (nuance/refinement) → change/variation verbs

**Lines 38, 109, 179, 181, 186, 191, 200, 202, 214, 226, 229, 256, 261-262, 265**:
- nuancering, balanceren, vervanging, herschikking, herijking, vernuft, vervulling, omzetting, realiseren, verander, verkenningen, vervangt, veranderen, toenemen, conversatie

- **SEMANTIC CHECK**: Generic change/modification terms, NOT specific to historical continuity!
- **DECISION**: REMOVE ALL (too generic)

### 4. Ultra-high df generic terms

**Line 94: geval** (case/instance) - df 298
**Line 115: politiek** (politics/political) - df 125
**Line 28: context** (context) - df 110
**Line 31: uitvoering** (execution) - df 190
**Line 45: discussie** (discussion) - df 86
**Line 71: debat** (debate) - df 142
**Line 112: overleg** (consultation) - df 91
**Line 129: dialoog** (dialogue) - df 42
**Line 142: geschiedenis** (history) - df 316 (already flagged)
**Line 144: tijd** (time) - df 404 (!)
**Line 149: behandeling** (treatment) - df 136
**Line 170: positie** (position) - df 216
**Line 210: vast** (fixed/certain) - df 117

- **SEMANTIC CHECK**: These are ULTRA-GENERIC words appearing in hundreds of documents!
- **DECISION**: REMOVE ALL

### 5. English words (NOT Dutch!)

**Line 108: time** (English for tijd)
**Line 118: systems** (English for systemen)
**Line 140: system--the** (English + typo!)
**Line 194: heritage** (English for erfenis)
**Line 220: text** (English for tekst)
**Line 225: development** (English for ontwikkeling)

- **SEMANTIC CHECK**: These are ENGLISH words, not Dutch!
- **DECISION**: REMOVE ALL

### 6. OCR errors/typos

**Line 172: schiedenis** (typo for geschiedenis - already seen in other topics)
**Line 222: geschiedenis-** (fragment)

- **DECISION**: REMOVE

## What to KEEP

### KERN 1.0 - Core legacy concepts (lines 3-4):
- doorwerking van het slavernijverleden
- doorwerking van het koloniale verleden

### STERK 0.9 - Strong legacy terms (lines 2, 5-8, 20):
- doorwerking
- doorwerking van koloniale verhoudingen
- structurele doorwerking
- structurele ongelijkheid
- systemische ongelijkheid
- structurele achterstelling

### BELEID 0.8 - Policy/structural terms (lines 9-19, 21-24):
- systemisch, structureel, institutioneel
- intergenerationeel, intergenerationele overdracht
- langetermijneffecten
- historische oorzaken, historische wortels, historisch gegroeid, historische achterstand
- ongelijke kansen, kansengelijkheid, ongelijke toegang, ongelijke behandeling

### VALID expansions with decent cosine (>0.70):
- Line 54: systemische (0.97)
- Line 56: intergenerationele (0.96)
- Line 59: institutionele (0.93)
- Line 60: structurele (0.93) - BUT already used as seed, ultra-high df (94)
- Line 63: constitutionele (0.86)
- Line 65: kansenongelijkheid (0.85)
- Line 67: systematiek (0.84)
- Line 72: formeel-systemisch (0.83)
- Line 74: generationeel (0.82)
- Line 78: achterstand (0.82)
- Line 88: instituties (0.78)
- Line 102: doorwerkingen (0.75)
- Line 127: doorbreking (0.72)
- Line 138: uitwerking (0.71)

**NOTE**: Even these need review - many have low cosine or high df.

## Summary Decision

**REMOVE ALL RISICO 0.3 TERMS**: ~150 terms (lines 27-266 minus a few exceptions)
- These were categorized as RISICO specifically because they're ambiguous/generic
- Ultra-high df values confirm they're not topic-specific
- English words, typos, ultra-generic policy language

**REMOVE ultra-high df BELEID/CONTEXT terms**:
- Line 60: structurele (df 94) - seed already captured
- Line 142: geschiedenis (df 316)
- Line 144: tijd (df 404)
- Line 149: behandeling (df 136)
- Line 154: kans (df 101)
- Line 170: positie (df 216)

**KEEP**:
- All KERN 1.0 seeds
- All STERK 0.9 seeds
- BELEID 0.8 seeds with reasonable df
- High cosine (>0.80) expansions that are semantically valid

**Estimated Final**: ~40-50 terms (from 266)
**Estimated Removals**: ~215 terms (80% removal rate - justified by massive RISICO over-expansion)
