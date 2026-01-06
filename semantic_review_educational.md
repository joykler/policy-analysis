# Semantic Review: Educational Disadvantage & Brain Drain

## Topic Context
This topic captures how colonial slavery's legacy manifests in contemporary educational problems:
- Systematic educational exclusion under slavery
- Colonial language imposition (Dutch vs Papiamentu)
- Brain drain (educated youth leaving islands)
- Poor educational outcomes and dropout rates

## Semantic Analysis by Weight Tier

### CORE PROBLEMS (1.00) - The Problem Itself

#### ✅ KEEP at 1.00 (TRUE CORE)
1. **brain drain** - The phenomenon itself (seed)
2. **onderwijs-achterstand** - Educational disadvantage (seed)
3. **onderwijsachterstand** - Same concept (seed)
4. **onderwijsongelijkheid** - Educational inequality (seed)
5. **onderwijsuitsluiting** - Educational exclusion (seed)
6. **schooluitval** - School dropout (seed)

#### ⚠️ NEEDS REVIEW
7. **leerachterstand** (0.864 cosine) - "Learning disadvantage"
   - SEMANTIC: Nearly synonym of onderwijs-achterstand
   - DECISION: **KEEP at 1.00** - valid variant, high cosine

8. **onderwijsmethoden** (0.755 cosine, df=2) - "Teaching methods"
   - SEMANTIC: Methods are HOW education happens, not the PROBLEM
   - The problem is EXCLUSION, not methods themselves
   - DECISION: **LOWER to 0.75** - related_moderate (methods are discussed when analyzing exclusion, but aren't the disadvantage)

---

### STRONG PROBLEMS (0.90-0.95) - Clear Manifestations

#### ✅ KEEP at 0.95 (STRONG)
1. **emigratie** - Emigration (seed)
2. **remigratie** - Return migration (0.924 cosine)
3. **onderwijskwaliteit** - Education quality (seed)
4. **onderwijskloof** - Education gap (seed)
5. **schoolachterstand** - School disadvantage (seed)
6. **taalbarrière** - Language barrier (seed)
7. **lerarentekort** - Teacher shortage (seed)
8. **analfabetisme** - Illiteracy (seed)
9. **taalachterstand** - Language disadvantage (seed)
10. **taalproblemen** - Language problems (0.820 cosine)
11. **voortijdig schoolverlaten** - Early school leaving (seed)

#### ⚠️ NEEDS REVIEW
12. **immigratie** (0.925 cosine, df=42) - "Immigration"
    - SEMANTIC: Immigration is OPPOSITE of brain drain
    - Brain drain = people LEAVING (emigration)
    - Immigration = people ARRIVING
    - High cosine because semantically related migration concepts
    - DECISION: **LOWER to 0.75** or **REMOVE** - wrong direction

13. **leerachterstanden** (0.702 cosine, df=4) - "Learning disadvantages" (plural)
    - SEMANTIC: Plural of leerachterstand
    - Low cosine (0.702) is red flag
    - DECISION: **LOWER to 0.85** - keep as related_strong, not strong_problem

14. **schoolverlaten** (0.697 cosine, df=4) - "School leaving"
    - SEMANTIC: Leaving school (generic verb form)
    - We already have "voortijdig schoolverlaten" (EARLY school leaving = problem)
    - Just "schoolverlaten" = neutral (everyone leaves school eventually)
    - DECISION: **LOWER to 0.70** - too generic without "voortijdig"

---

### RELATED STRONG (0.85) - Domain Context

#### ⚠️ SEMANTIC ISSUES

**"moeder" (df=46, from "moedertaal")**
- SEMANTIC: "Mother" as noun vs "mother tongue" (moedertaal)
- BERTJE picked up "moeder" from "moedertaal" but they're different:
  - moedertaal = mother tongue (LANGUAGE concept - relevant)
  - moeder = mother (PERSON - not about language)
- DECISION: **LOWER to 0.50** or **REMOVE** - semantic drift

**"inlandse" (df=2, from "nederlands opgelegd")**
- SEMANTIC: "indigenous/native"
- Related to imposed Dutch vs local languages
- DECISION: **KEEP at 0.75** - relevant but lower (not strong)

**"nederlands" (df=237, weight=0.85)**
- SEMANTIC: "Dutch" (language/nationality)
- CONTEXT: Appears in 237/~850 documents! Overwhelming frequency
- RELEVANCE: Central to language barrier issue BUT too generic
- Parent: "nederlands opgelegd" (imposed Dutch) - that's the PROBLEM
- Just "nederlands" = too broad
- DECISION: **LOWER to 0.60** - common term needs dampening

**"nederlandsche" (df=66, weight=0.85)**
- SEMANTIC: Old spelling of "Dutch"
- DECISION: **LOWER to 0.65** - historical term, moderate frequency

**"nederlands-vlaamse" (df=2)**
- SEMANTIC: "Dutch-Flemish"
- RELEVANCE: Geographic variant, not central to Caribbean context
- DECISION: **LOWER to 0.60** or **REMOVE** - off-topic geographically

**"zuid-nederlandse" (df=3)**
- SEMANTIC: "Southern Dutch"
- RELEVANCE: Geographic variant, European context not Caribbean
- DECISION: **REMOVE** - geographic drift

**"niveau" (df=98, weight=0.85)**
- SEMANTIC: "level" (generic noun)
- CONTEXT: Generic fragment of:
  - onderwijsniveau (education level)
  - kennisniveau (knowledge level)
  - opleidingsniveau (training level)
- DECISION: **REMOVE** - pure generic fragment (methodology says remove)

**"kennisniveau" (df=2, weight=0.85)**
- SEMANTIC: "knowledge level"
- RELEVANCE: Relevant to measuring disadvantage
- DECISION: **LOWER to 0.75** - related_moderate

---

### ADDITIONAL TERMS TO CHECK

Let me check more expanded terms...
