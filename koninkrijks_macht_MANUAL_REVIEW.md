# Koninkrijks_Macht - Manual Semantic Review
**Topic**: Kingdom Power Structures (constitutional/administrative relationships within Kingdom of Netherlands)
**Reviewer**: Human semantic understanding
**Date**: 2026-01-03

## Review Focus

This topic is about **Kingdom-specific governance**, not general Dutch state governance. Key question for each term: Is this specifically about the Kingdom relationships (Netherlands-Caribbean islands), or just generic governance that could apply to any state?

## Lines 2-6: KERN 1.0 colonial status terms (very low cosine)

**Line 2: gekoloniseerd** (colonized)
- Parent: koloniale status
- Cosine: 0.6042, df: 2
- **SEMANTIC CHECK**: "Gekoloniseerd" = colonized. Very low cosine, very low df. Too generic/historical.
- **DECISION**: REMOVE (very low cosine + low df)

**Line 3: dekoloniserend** (decolonizing)
- Cosine: 0.6123, df: 2
- **SEMANTIC CHECK**: "Dekoloniserend" = decolonizing (process). Very low cosine/df.
- **DECISION**: REMOVE (very low cosine + low df)

**Line 4: gekoloniseerden** (colonized people)
- Cosine: 0.6879, df: 6
- **SEMANTIC CHECK**: "Gekoloniseerden" = the colonized. Relevant but very low cosine.
- **DECISION**: Downgrade to STERK 0.8

**Line 5: ex-koloniën** (ex-colonies)
- Cosine: 0.7, df: 2
- **SEMANTIC CHECK**: "Ex-koloniën" = former colonies. Relevant to Kingdom status but low df.
- **DECISION**: Downgrade to KERN 0.9 (low cosine, valid term)

**Line 6: dekoloniaal** (decolonial)
- Cosine: 0.7351, df: 2
- **SEMANTIC CHECK**: "Dekoloniaal" = decolonial. Academic term, relevant but low df.
- **DECISION**: KEEP at KERN 1.0

## Lines 7-77: STERK 0.9 terms - many need review

### "zelfbeschikking" (self-determination) parent expansions

Many of these are just generic "self-" or "-zelf" (self/themselves) terms, NOT about self-determination!

**Line 7: zelfidentiteit** (self-identity)
- **SEMANTIC CHECK**: "Zelfidentiteit" = self-identity. Generic identity term, NOT self-determination.
- **DECISION**: REMOVE (semantic drift)

**Line 25: zelfreflectie** (self-reflection)
- **SEMANTIC CHECK**: "Zelfreflectie" = self-reflection. Generic introspection, NOT self-determination.
- **DECISION**: REMOVE (semantic drift)

**Line 32: zelfcensuur** (self-censorship)
- **SEMANTIC CHECK**: "Zelfcensuur" = self-censorship. NOT about political self-determination!
- **DECISION**: REMOVE (semantic drift)

**Line 33: henzelf, 37: onszelf, 40: mijzelf, 42: jezelf, 51: zichzelf, 52: mezelf** (themselves/ourselves/myself/yourself)
- **SEMANTIC CHECK**: These are just reflexive pronouns! NOT about self-determination!
- **DECISION**: REMOVE ALL (semantic drift - pronouns)

**Line 41: zelfbeelden, 46: zelfbeeld** (self-image)
- **SEMANTIC CHECK**: "Zelfbeeld" = self-image/self-perception. NOT about political self-determination.
- **DECISION**: REMOVE (semantic drift)

**Line 65: zelfgenoegzame** (self-satisfied/complacent)
- **SEMANTIC CHECK**: "Zelfgenoegzame" = self-satisfied. NOT about self-determination!
- **DECISION**: REMOVE (semantic drift)

**Line 69: zelf-** (self- prefix)
- **SEMANTIC CHECK**: Just a prefix fragment.
- **DECISION**: REMOVE (fragment)

**Line 70: zelfvertrouwen** (self-confidence)
- **SEMANTIC CHECK**: "Zelfvertrouwen" = self-confidence. NOT about political self-determination!
- **DECISION**: REMOVE (semantic drift)

**Line 75: zelfbewustzijn** (self-awareness/consciousness)
- **SEMANTIC CHECK**: "Zelfbewustzijn" = self-awareness. NOT about political self-determination!
- **DECISION**: REMOVE (semantic drift)

**KEEP from zelfbeschikking** (actually about self-determination/autonomy):
- **zelfbestuur** (self-government) - line 49
- **zelfstandig, zelfstandige, zelfstandigen, zelfstandigheid** (independent/autonomy) - lines 27, 53, 60, 62
- **zelfredzaamheid** (self-reliance) - line 67

### "verhoudingen" (relations/ratios)

**Line 8: verhoudingen** (relations/ratios)
- Parent: gezagsverhouding
- Cosine: 0.6047, df: 75
- **SEMANTIC CHECK**: "Verhoudingen" = relations/ratios. Too generic alone without "gezags-" prefix.
- **DECISION**: REMOVE (too generic)

### Colonial terms - many are valid

**Lines 15, 39: kolonisator, kolonisatoren** (colonizer/colonizers)
- **SEMANTIC CHECK**: Valid for colonial power dynamics.
- **DECISION**: KEEP

**Line 22: voc-koloniën** (VOC colonies)
- **SEMANTIC CHECK**: VOC = Dutch East India Company. Specific historical reference.
- **DECISION**: KEEP

**Line 23: slavenkoloniën** (slave colonies)
- **SEMANTIC CHECK**: Specific type of colony.
- **DECISION**: KEEP

### Generic governance terms

**Line 9: gezagvoerder** (commander/person in charge)
- **SEMANTIC CHECK**: "Gezagvoerder" = commander (airline captain, ship captain). NOT Kingdom-specific!
- **DECISION**: REMOVE (generic authority term)

**Line 13: gouvernement** (government)
- **SEMANTIC CHECK**: "Gouvernement" = government. Too generic.
- **DECISION**: REMOVE (too generic)

**Line 14: nationalistisch** (nationalist)
- **SEMANTIC CHECK**: "Nationalistisch" = nationalist. Generic political ideology, not Kingdom-specific.
- **DECISION**: REMOVE (too generic)

**Line 17: provinciaal, 36: provinciale** (provincial)
- **SEMANTIC CHECK**: "Provinciaal" = provincial. Dutch provinces, NOT Kingdom islands!
- **DECISION**: REMOVE (wrong level of government)

**Line 18: gelegenheid** (occasion/opportunity)
- **SEMANTIC CHECK**: "Gelegenheid" = occasion/opportunity. Generic word, NOT governance!
- **DECISION**: REMOVE (semantic drift)

**Line 12: sociaal-** (social-)
- **SEMANTIC CHECK**: "Sociaal-" = social- prefix. Fragment.
- **DECISION**: REMOVE (fragment)

### Partnership/cooperation terms

**Lines 11, 19: samenwerkingspartners, partnerlanden** (cooperation partners, partner countries)
- **SEMANTIC CHECK**: Could be Kingdom partners or generic international partners. Borderline.
- **DECISION**: KEEP (can apply to Kingdom context)

**Line 21: samenwerkingsverbanden** (cooperation agreements)
- **SEMANTIC CHECK**: Generic cooperation.
- **DECISION**: REMOVE (too generic)

**Line 30: overeenkomsten** (agreements)
- **SEMANTIC CHECK**: "Overeenkomsten" = agreements. Too generic.
- **DECISION**: REMOVE (too generic)

**Line 34: bondgenootschappen** (alliances)
- **SEMANTIC CHECK**: "Bondgenootschappen" = alliances. Generic international relations.
- **DECISION**: REMOVE (too generic)

**Line 43: alliantie** (alliance)
- **SEMANTIC CHECK**: Generic alliance.
- **DECISION**: REMOVE (too generic)

**Line 48: genootschap** (society/association)
- **SEMANTIC CHECK**: "Genootschap" = society/association. Too generic.
- **DECISION**: REMOVE (too generic)

### Other problematic terms

**Line 10: machtsstructuur** (power structure)
- **SEMANTIC CHECK**: Generic power structure.
- **DECISION**: REMOVE (too generic)

**Line 16: heerschappij** (rule/dominion)
- **SEMANTIC CHECK**: "Heerschappij" = rule/dominion. Generic term for rule.
- **DECISION**: KEEP (relevant to colonial dominion)

**Line 24: machtsevenwicht** (balance of power)
- **SEMANTIC CHECK**: Generic IR concept.
- **DECISION**: REMOVE (too generic)

**Line 31: nationalisme** (nationalism)
- **SEMANTIC CHECK**: Generic political ideology.
- **DECISION**: REMOVE (too generic)

## Lines 79-100: BELEID 0.8 terms

Many of these are clearly too generic for Kingdom-specific policy:

**Line 79: beleidsevaluatie** (policy evaluation)
- **SEMANTIC CHECK**: Generic policy evaluation.
- **DECISION**: REMOVE (too generic)

**Line 80: validatie** (validation)
- **SEMANTIC CHECK**: "Validatie" = validation. Generic research/admin term.
- **DECISION**: REMOVE (too generic)

**Line 81: beleidsconclusies** (policy conclusions)
- **SEMANTIC CHECK**: Generic policy conclusions.
- **DECISION**: REMOVE (too generic)

**Line 83: interesse** (interest)
- **SEMANTIC CHECK**: "Interesse" = interest. Generic word!
- **DECISION**: REMOVE (too generic)

**Line 84: validiteit** (validity)
- **SEMANTIC CHECK**: "Validiteit" = validity. Generic research term.
- **DECISION**: REMOVE (too generic)

**Line 85: bestuur-** (governance- prefix)
- **SEMANTIC CHECK**: Fragment.
- **DECISION**: REMOVE (fragment)

**Line 86: onmenselijkheid** (inhumanity)
- **SEMANTIC CHECK**: "Onmenselijkheid" = inhumanity. Not specific to inequality/Kingdom relations.
- **DECISION**: REMOVE (semantic drift)

**Line 87: rechtshandhaving** (law enforcement)
- **SEMANTIC CHECK**: Generic law enforcement.
- **DECISION**: REMOVE (too generic)

**Line 88: overheids-** (government- prefix)
- **SEMANTIC CHECK**: Fragment.
- **DECISION**: REMOVE (fragment)

**Line 90: bevlogenheid** (enthusiasm/passion)
- **SEMANTIC CHECK**: "Bevlogenheid" = enthusiasm. Generic personal quality!
- **DECISION**: REMOVE (semantic drift)

**Line 92: relatie** (relation/relationship)
- **SEMANTIC CHECK**: "Relatie" = relationship. Too generic without "rijks-" prefix.
- **DECISION**: REMOVE (too generic)

**Line 93: selijkheid** (fragment of a word)
- **SEMANTIC CHECK**: Fragment (probably from "gelijkheid" = equality).
- **DECISION**: REMOVE (fragment)

**Line 94: ordening** (order/arrangement)
- **SEMANTIC CHECK**: "Ordening" = ordering/arrangement. Too generic.
- **DECISION**: REMOVE (too generic)

**Line 95: redelijkheid** (reasonableness)
- **SEMANTIC CHECK**: "Redelijkheid" = reasonableness. Generic legal/admin principle.
- **DECISION**: REMOVE (too generic)

**Line 96: mogendheid** (power/might)
- **SEMANTIC CHECK**: "Mogendheid" = great power (country). Could be relevant but very generic.
- **DECISION**: REMOVE (too generic)

**Line 98: parlementaire** (parliamentary)
- **SEMANTIC CHECK**: "Parlementaire" = parliamentary. Could be Kingdom parliament but very generic.
- **DECISION**: KEEP (can apply to Kingdom parliament)

**Line 99: interactie** (interaction)
- **SEMANTIC CHECK**: Generic interaction.
- **DECISION**: REMOVE (too generic)

**Line 100: kwantiteit** (quantity)
- **SEMANTIC CHECK**: "Kwantiteit" = quantity. Generic measurement term!
- **DECISION**: REMOVE (semantic drift)

## Summary Pattern

**Major issue**: "zelfbeschikking" parent massively over-expanded with generic "self-" words and reflexive pronouns that have NOTHING to do with political self-determination.

**Second issue**: Many generic governance/administration terms that could apply to ANY government, not specifically Kingdom structures.

**Valid terms**: Colonial-specific terms (kolonisator, koloniën, etc.), specific Kingdom instruments (toezicht when Kingdom-context), constitutional terms (when Kingdom-specific).

## Estimated Removals for Koninkrijks_Macht

~80-100 terms need removal (mostly semantic drift from "zelfbeschikking" and generic governance terms)
