# Arbeid_Afhankelijkheid - Manual Semantic Review
**Topic**: Labor Dependency (forced labor, contract labor, movement restrictions, unequal labor opportunities)
**Reviewer**: Human semantic understanding
**Date**: 2026-01-03

## Review Focus

This topic is about **labor exploitation and dependency**, specifically forced labor systems that emerged from slavery. Key question: Is this term specifically about exploitative labor relationships, or just generic labor/land/governance?

## Major Semantic Drift Patterns

### 1. "politionele controle" (police control) → political science terms

**Lines 45, 49, 57, 89**: political, politics, politicologische, politici
- **SEMANTIC CHECK**:
  - "political" = English word for "political" (NOT Dutch!)
  - "politics" = English word for "politics" (NOT Dutch!)
  - "politicologische" = political science (academic field)
  - "politici" = politicians
- **ISSUE**: These are about POLITICS/POLITICAL SCIENCE, not "politionele" (police) control!
- **DECISION**: REMOVE ALL (wrong semantic domain - politics ≠ police)

### 2. "onteigening" (expropriation) → "ont-" prefix drift

The parent "onteigening" (expropriation/dispossession) has generated many "ont-" prefix matches:

**Line 81: ontving** (received)
- **SEMANTIC CHECK**: "Ontving" = received (past tense of ontvangen). NOT expropriation!
- **DECISION**: REMOVE (semantic drift)

**Line 96: ontvingen** (received - plural)
- **SEMANTIC CHECK**: Same as ontving.
- **DECISION**: REMOVE (semantic drift)

**Line 97: afspiegeling** (reflection/mirror)
- **SEMANTIC CHECK**: "Afspiegeling" = reflection/mirror. NOT expropriation!
- **DECISION**: REMOVE (semantic drift)

**Line 101: verving** (replacement)
- **SEMANTIC CHECK**: "Verving" = replacement. Could relate to land replacement but very indirect.
- **DECISION**: REMOVE (too generic)

**Line 105: versteviging** (strengthening)
- **SEMANTIC CHECK**: "Versteviging" = strengthening/reinforcement. OPPOSITE of expropriation!
- **DECISION**: REMOVE (semantic drift)

**Line 114: ontheemding** (displacement)
- **SEMANTIC CHECK**: "Ontheemding" = displacement/making homeless. This IS related to expropriation!
- **DECISION**: KEEP

**Line 115: ontginning** (cultivation/land clearing)
- **SEMANTIC CHECK**: "Ontginning" = land reclamation/clearing. Could relate to colonial land appropriation.
- **DECISION**: KEEP (borderline but relevant)

**Line 126: onthulling** (revelation/unveiling)
- **SEMANTIC CHECK**: "Onthulling" = revelation/unveiling. NOT expropriation!
- **DECISION**: REMOVE (semantic drift)

**Line 130: ontregeling** (disruption)
- **SEMANTIC CHECK**: "Ontregeling" = disruption/deregulation. Too generic.
- **DECISION**: REMOVE (too generic)

**Line 131: ontmanteling** (dismantling)
- **SEMANTIC CHECK**: "Ontmanteling" = dismantling. Could relate to dismantling of property rights but very indirect.
- **DECISION**: REMOVE (too generic)

**Line 134: ontheffing** (exemption/discharge)
- **SEMANTIC CHECK**: "Ontheffing" = exemption/discharge from duty. NOT expropriation!
- **DECISION**: REMOVE (semantic drift)

**Line 133: vernietiging** (destruction)
- **SEMANTIC CHECK**: "Vernietiging" = destruction. Could relate to property destruction but too generic.
- **DECISION**: REMOVE (too generic)

### 3. "landbezit" (land ownership) → generic land/country terms

**Line 47: land** (land/country)
- **SEMANTIC CHECK**: "Land" = land OR country. Ultra-high df (272) - appears everywhere!
- **DECISION**: REMOVE (too generic, ultra-high df)

**Line 50: land-** (land- prefix)
- **SEMANTIC CHECK**: Fragment.
- **DECISION**: REMOVE (fragment)

**Line 70: vasteland** (mainland/continent)
- **SEMANTIC CHECK**: "Vasteland" = mainland/continent. Geographic term, NOT about land ownership!
- **DECISION**: REMOVE (semantic drift)

**Line 85: landhuis** (country house)
- **SEMANTIC CHECK**: "Landhuis" = country house/mansion. While plantation owners had these, the term itself is just architecture.
- **DECISION**: KEEP (plantation manor houses are relevant)

**Line 86: landje** (small piece of land)
- **SEMANTIC CHECK**: "Landje" = small plot of land (diminutive). Generic.
- **DECISION**: REMOVE (too generic diminutive)

**Line 90: landschappen** (landscapes)
- **SEMANTIC CHECK**: "Landschappen" = landscapes. Geographic/aesthetic term, NOT ownership!
- **DECISION**: REMOVE (semantic drift)

**Line 111: landbouw-** (agriculture- prefix)
- **SEMANTIC CHECK**: Fragment.
- **DECISION**: REMOVE (fragment)

**Line 125: landbouwende** (agricultural/farming)
- **SEMANTIC CHECK**: "Landbouwende" = agricultural/farming. Too generic adjective.
- **DECISION**: REMOVE (too generic)

**Line 128: landse** (rural/country-like)
- **SEMANTIC CHECK**: "Landse" = rural/country-like. Generic adjective, high df (41).
- **DECISION**: REMOVE (too generic)

**Line 135: landelijk** (rural/nationwide)
- **SEMANTIC CHECK**: "Landelijk" = rural OR nationwide. Ambiguous, generic.
- **DECISION**: REMOVE (too generic)

### 4. "disciplinering" (disciplining) → academic disciplines

**Line 46: interdisciplinaire** (interdisciplinary)
- **SEMANTIC CHECK**: "Interdisciplinaire" = interdisciplinary. Academic term, NOT about labor discipline!
- **DECISION**: REMOVE (semantic drift - academic ≠ labor control)

**Line 52: discipline-** (discipline- prefix)
- **SEMANTIC CHECK**: Fragment.
- **DECISION**: REMOVE (fragment)

**Line 71: interdisciplinair** (interdisciplinary)
- **SEMANTIC CHECK**: Same as line 46.
- **DECISION**: REMOVE (semantic drift)

### 5. "grondbezit" (land ownership) → construction/housing terms

**Line 82: bouwgrond** (building land)
- **SEMANTIC CHECK**: "Bouwgrond" = land designated for construction. Generic urban planning term.
- **DECISION**: REMOVE (too generic)

**Line 87: woningbouw** (housing construction)
- **SEMANTIC CHECK**: "Woningbouw" = housing construction/house building. Generic construction, NOT colonial land ownership!
- **DECISION**: REMOVE (semantic drift)

**Line 99: vastgoed-** (real estate- prefix)
- **SEMANTIC CHECK**: Fragment.
- **DECISION**: REMOVE (fragment)

**Line 106: woningen** (houses/dwellings)
- **SEMANTIC CHECK**: "Woningen" = houses/dwellings. Too generic.
- **DECISION**: REMOVE (too generic)

**Line 113: vastgoed** (real estate)
- **SEMANTIC CHECK**: "Vastgoed" = real estate. Modern commercial term, too generic.
- **DECISION**: REMOVE (too generic)

**Line 119: bouwde** (built)
- **SEMANTIC CHECK**: "Bouwde" = built (past tense). Generic verb.
- **DECISION**: REMOVE (too generic verb)

### 6. "contractarbeid" (contract labor) → generic contract terms

**Line 51: contract** (contract)
- **SEMANTIC CHECK**: "Contract" = contract. Ultra-generic, high df (40).
- **DECISION**: REMOVE (too generic)

**Line 53: contracten** (contracts)
- **SEMANTIC CHECK**: "Contracten" = contracts (plural). Ultra-generic.
- **DECISION**: REMOVE (too generic)

**Line 88: contractant** (contractor/contracting party)
- **SEMANTIC CHECK**: "Contractant" = contractor/party to contract. Generic legal term.
- **DECISION**: REMOVE (too generic)

### 7. "arbeidsdwang" (forced labor) → generic labor/work terms

**Line 73: arbeid** (labor/work)
- **SEMANTIC CHECK**: "Arbeid" = labor/work. Ultra-generic, ultra-high df (125)!
- **DECISION**: REMOVE (too generic)

**Line 103: arbeids-** (labor- prefix)
- **SEMANTIC CHECK**: Fragment.
- **DECISION**: REMOVE (fragment)

### 8. "staatstoezicht" (state supervision) → generic state terms

**Line 80: staats-** (state- prefix)
- **SEMANTIC CHECK**: Fragment. Already flagged in auto-curation.
- **DECISION**: REMOVE (fragment)

### 9. Other generic terms

**Line 55: bezit** (possession)
- **SEMANTIC CHECK**: "Bezit" = possession/ownership. Ultra-generic, high df (79).
- **DECISION**: REMOVE (too generic)

**Line 65: loon** (wage)
- **SEMANTIC CHECK**: "Loon" = wage. Generic, not necessarily unequal.
- **DECISION**: REMOVE (too generic)

**Line 72: loon-** (wage- prefix)
- **SEMANTIC CHECK**: Fragment.
- **DECISION**: REMOVE (fragment)

**Line 84: eigendom** (property)
- **SEMANTIC CHECK**: "Eigendom" = property/ownership. Generic, high df (53).
- **DECISION**: REMOVE (too generic)

**Line 91: verhouding** (relation/ratio)
- **SEMANTIC CHECK**: "Verhouding" = relation/ratio. Too generic without "bezits-" prefix.
- **DECISION**: REMOVE (too generic)

**Line 121: streek** (region/area)
- **SEMANTIC CHECK**: "Streek" = region/area. Geographic term.
- **DECISION**: REMOVE (too generic)

**Line 129: eigenaren** (owners)
- **SEMANTIC CHECK**: "Eigenaren" = owners. Generic, ultra-high df (113).
- **DECISION**: REMOVE (too generic)

## Summary of Manual Decisions

### REMOVE (Semantic Drift / Too Generic / Fragments):

**Politics ≠ Police (4 terms)**:
- political, politics, politicologische, politici

**"ont-" prefix drift from onteigening (9 terms)**:
- ontving, ontvingen, afspiegeling, verving, versteviging, onthulling, ontregeling, ontmanteling, ontheffing, vernietiging

**Generic land/country terms (10 terms)**:
- land, land-, vasteland, landje, landschappen, landbouw-, landbouwende, landse, landelijk

**Academic disciplines ≠ labor disciplining (3 terms)**:
- interdisciplinaire, discipline-, interdisciplinair

**Generic construction/housing (6 terms)**:
- bouwgrond, woningbouw, vastgoed-, woningen, vastgoed, bouwde

**Generic contract terms (3 terms)**:
- contract, contracten, contractant

**Generic labor/work (2 terms)**:
- arbeid, arbeids-

**Fragments (3 terms)**:
- staats-, loon-, eigendom (if too generic)

**Other generic (5 terms)**:
- bezit, loon, verhouding, streek, eigenaren

**Total estimated REMOVE**: ~45 terms

### KEEP (Valid labor dependency terms):
- All seed terms (staatstoezicht, contractarbeid, dwangarbeid, etc.)
- Specific labor exploitation terms (arbeidsuitbuiting, slavenarbeid, slavenverzet, etc.)
- Land ownership terms related to colonial exploitation (grondbezitters, grootgrondbezitters, landarme, etc.)
- Contract labor specific (contractarbeiders, arbeidscontract)
- Forced labor specific (dwangarbeiders, arbeidsregime)
