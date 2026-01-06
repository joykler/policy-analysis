# Revised Seed Dictionary Strategy - Understanding Contextual Terms

## Critical Insight: Purpose of "Duplicated" Terms

I was **wrong** to recommend removing temporal, geographic, and slavery-period terms from all topics.

### **Why These Terms Should Stay**

**Their purpose is FILTERING, not classification**:

1. **Temporal terms** (`historisch`, `geschiedenis`, `zeventiende eeuw`, etc.):
   - **Purpose**: Focus on HISTORICAL causes, not contemporary outcomes
   - **Example**: "racisme" + "historisch" = historical racial structures (RELEVANT)
   - **Example**: "racisme" without temporal = contemporary racism (NOT RELEVANT)
   - Should be in ALL topics to ensure historical focus

2. **Geographic terms** (`Suriname`, `Curaçao`, `Aruba`, etc.):
   - **Purpose**: Focus on CARIBBEAN context specifically
   - **Example**: "koloniale" + "Curaçao" = Caribbean colonial system (RELEVANT)
   - **Example**: "koloniale" without geographic = could be India, Indonesia (NOT RELEVANT)
   - Should be in ALL topics to ensure Caribbean localization

3. **Slavery-period terms** (`slavernijverleden`, `slavernijperiode`, `afschaffing`):
   - **Purpose**: Anchor to slavery legacy specifically
   - **Example**: "onderwijsuitsluiting" + "slavernijverleden" = educational exclusion from slavery (RELEVANT)
   - **Example**: "onderwijsuitsluiting" alone = modern educational access issues (NOT RELEVANT)
   - Should be in ALL topics to maintain slavery legacy focus

### **What This Means for Multi-Label Scoring**

In a **multi-label system with cosine similarity**, these terms act as:
- **Topic-agnostic filters**: Boost relevance when content is about the right context (historical Caribbean slavery)
- **Shared baseline**: All topics get equal boost for appropriate context
- **Differentiation comes from topic-specific terms**: The unique vocabulary per topic still drives classification

**Example - How It Works**:

**Chunk about historical Caribbean educational exclusion**:
- Gets boost from: `Curaçao` (0.90), `slavernijverleden` (0.90), `historisch` (0.70) = present in ALL topics
- **Educational topic wins because**: `onderwijsuitsluiting` (0.90), `onderwijs-achterstand` (1.00) = UNIQUE to Educational
- **Result**: Educational scores higher because shared terms + unique terms > shared terms alone

**Chunk about modern Caribbean poverty**:
- Gets boost from: `Curaçao` (0.90), but NO temporal terms (not historical)
- **Lower scores across ALL topics** because missing temporal filter
- **Result**: Likely "none" confidence - correctly filtered as not about historical slavery legacy

---

## What Actually Needs Fixing

The problem is NOT the shared contextual terms. The problem is:

### **1. Educational Has Too Many TOPIC-SPECIFIC Generic Terms**

These are the real culprits that over-trigger:

**Remove from Educational** (these are truly too generic):
- ❌ `geschiedenisonderwijs` (0.80) - "history education" triggers on ANY historical discussion
- ❌ `curriculum ontwikkeling` (0.75) - generic administrative term
- ❌ `onderwijsvoorzieningen` (0.75) - generic services term

**Why**: These trigger on administrative/historical content even without educational focus

**Example**: Chunk 195cdf4c (parliamentary debate about abolition)
- Contains: `debat` (implicit in "debat over afschaffing")
- `geschiedenisonderwijs` present could boost score for discussing historical events
- But chunk is about POLITICAL debate, not educational content

**Fix**: Remove overly broad educational-adjacent terms, keep only actual learning/schooling terms

---

### **2. Social Fragmentation Lacks EXPLICIT Racial Discourse Terms**

The topic has `racisme` (1.00) but missing:

**ADD to Social Fragmentation**:
- ✅ `racistisch` (0.95) - adjectival form that actually appears in text
- ✅ `discriminerend` (0.95) - "discriminating" as modifier
- ✅ `neger` (0.90) - racial slur discussed in historical documents
- ✅ `slavenhandel` (0.95) - slave trade as racial commerce
- ✅ `abolitionisten` (0.90) - abolition movement (racial justice)

**Why**: Chunk 34795144 explicitly says "woord 'neger' discriminerend en racistisch" but Social Fragmentation scored LOWEST

**Current Social Fragmentation vocabulary**:
- Has: `racisme` (noun)
- Missing: `racistisch` (adjective), `discriminerend` (adjective)
- **Problem**: Text uses adjectives, dictionary has nouns

---

### **3. Governance Lacks POLITICAL/PARLIAMENTARY Vocabulary**

**ADD to Governance**:
- ✅ `parlementaire` (0.90) - parliamentary
- ✅ `constitutionele` (0.90) - constitutional
- ✅ `hervormingen` (0.85) - reforms
- ✅ `kabinet` (0.90) - cabinet
- ✅ `wetgeving` (0.90) - legislation
- ✅ `debat` (0.85) - debate (in political context)

**Why**: Chunk 195cdf4c discusses "parlementaire hervormingen", "kabinet-Thorbecke", "constitutionele hervormingen"
- Current Governance vocabulary likely lacks these specific political process terms
- **Result**: Governance scored 0.327 (rank #3), Educational scored 0.457 (rank #1)

---

### **4. "afschaffing" Should Be Multi-Topic**

**Current**: `afschaffing` (0.85) in Educational and Social Fragmentation

**Actually**: Abolition is relevant to MULTIPLE topics:
- **Governance** (0.90): Political act, legislation, parliamentary debate
- **Social Fragmentation** (0.85): Racial liberation, end of racial hierarchy
- **Educational** (0.75): Educational context only if discussing abolition education

**Fix**:
- Keep in Social Fragmentation (0.85) - racial liberation
- ADD to Governance (0.90) - higher weight for political act
- REDUCE in Educational to (0.75) - only for educational discussions
- Or REMOVE from Educational entirely if not about abolition education

---

## Revised Recommendations

### **KEEP (Do NOT Remove)**

✅ **Temporal terms in ALL topics**:
- `historisch`, `geschiedenis`, `destijds`
- `zeventiende eeuw`, `achttiende eeuw`, `negentiende eeuw`
- `1863`, `1873`
- **Purpose**: Filter for historical vs contemporary content

✅ **Geographic terms in ALL topics**:
- `Suriname`, `Curaçao`, `Aruba`, `Bonaire`
- `Sint Maarten`, `Sint Eustatius`, `Saba`
- `Antillen`, `Caribisch Nederland`, `BES-eilanden`
- **Purpose**: Focus on Caribbean, exclude other colonial contexts (India, Indonesia)

✅ **Slavery-period terms in ALL topics**:
- `slavernijverleden`, `slavernijperiode`, `koloniaal verleden`
- `slavernijperiode`, `koloniaal tijdperk`
- **Purpose**: Anchor to slavery legacy specifically

### **REMOVE (Too Generic WITHIN Topics)**

❌ **From Educational** - Generic educational-adjacent terms:
- `geschiedenisonderwijs` (0.80) - triggers on any historical discussion
- `curriculum ontwikkeling` (0.75) - too administrative
- `onderwijsvoorzieningen` (0.75) - too generic
- `taalbeleid` (0.80) - political term, move to Governance

**Rationale**: These trigger on non-educational content when discussing history, policy, or administration

❌ **From All Topics** - Truly redundant duplicates:
- Keep only ONE instance of each geographic/temporal term across topics
- OR keep in all but ensure they have SAME weight across topics
- Current issue: Different weights create noise

**Actually, checking the data**: If they already have same weights across topics, KEEP them as-is.

---

### **ADD - Topic-Specific Vocabulary**

#### **Social Fragmentation & Racism**

Add morphological variants and explicit terms:

```
ADD:
- racistisch (0.95) - adjectival form
- discriminerend (0.95) - present participle
- discrimineren (0.90) - verb form
- neger (0.90) - racial slur (historical)
- negerin (0.85) - feminine form
- slavenhandel (0.95) - slave trade
- slavenarbeid (0.90) - slave labor
- slavenhouder (0.90) - slave holder
- abolitionisten (0.90) - abolitionists
- vrijkopen (0.85) - buying freedom
- slavenregister (0.85) - slave registry
- zwarte afrikanen (0.85) - racialized reference
- blanke (0.85) - white (racial category)
- meester (0.85) - master (slavery relationship)
```

**Why**: These terms actually appear in corpus but aren't captured by current dictionary

#### **Governance Distrust & Corruption**

Add political/parliamentary vocabulary:

```
ADD:
- parlementaire (0.90) - parliamentary
- parlement (0.90) - parliament
- constitutionele (0.90) - constitutional
- constitutie (0.90) - constitution
- hervormingen (0.85) - reforms
- hervorming (0.85) - reform
- kabinet (0.90) - cabinet
- minister (0.90) - minister
- wetgeving (0.90) - legislation
- debat (0.85) - debate (political)
- staten-generaal (0.90) - States General
- afschaffing (0.90) - abolition (as political act)
- afschaffingsdebat (0.95) - abolition debate
- koloniaal bestuur (0.95) - colonial administration
- bestuur (0.85) - governance
- taalbeleid (0.80) - language policy (MOVE from Educational)
```

**Why**: Parliamentary debate chunks should score high for Governance, currently don't

#### **Persistent Poverty & Economic Vulnerability**

Add trade/economic specifics:

```
ADD:
- slavenhandel (0.95) - slave trade (if not in Social Fragmentation)
- handel (0.90) - trade
- handelscompagnie (0.90) - trading company
- wic (0.95) - West India Company
- west-indische compagnie (0.95) - WIC full name
- exporteconomie (0.90) - export economy
- suikerproductie (0.90) - sugar production
```

**Why**: Economic dimension of slavery needs specific trade/commerce vocabulary

---

## Revised Strategy Summary

### **What NOT to Change** ✅

1. **Keep temporal/geographic/slavery-period terms in ALL topics**
   - They serve as contextual filters
   - Ensure focus on historical Caribbean slavery legacy
   - Don't differentiate between topics (that's the point)

### **What TO Change** ⚠️

2. **Remove overly generic TOPIC-SPECIFIC terms**
   - Educational: Remove `geschiedenisonderwijs`, `curriculum ontwikkeling`, `onderwijsvoorzieningen`
   - These trigger on non-educational content

3. **Add missing morphological variants**
   - Social Fragmentation: Add `racistisch`, `discriminerend` (adjectives appear in text, not just nouns)
   - Governance: Add `parlementaire`, `constitutionele` (adjectives missing)

4. **Add missing topic-specific vocabulary**
   - Social Fragmentation: Explicit racial terms (`neger`, `slavenhandel`, `abolitionisten`)
   - Governance: Political process terms (`kabinet`, `hervormingen`, `debat`)
   - Persistent Poverty: Trade terms (`handel`, `wic`, `exporteconomie`)

5. **Redistribute cross-cutting terms appropriately**
   - `afschaffing`: Higher weight in Governance (0.90), keep in Social (0.85), reduce/remove from Educational
   - `taalbeleid`: Move from Educational to Governance
   - `debat`: Add to Governance (political debates), keep out of Educational

---

## Expected Impact on Problem Chunks

### **Chunk 34795144** (Uncle Tom's Cabin - racism)

**Current scores**:
- Educational: 0.455 [#1]
- Social Fragmentation: 0.382 [#5]

**Text contains**: "woord 'neger' discriminerend en racistisch", "abolitionisten"

**After fixes**:
- Social Fragmentation gains: `neger` (0.90), `racistisch` (0.95), `discriminerend` (0.95), `abolitionisten` (0.90)
- Educational loses: `geschiedenisonderwijs` removed (was boosting for historical discussion)
- **Expected**: Social Fragmentation: 0.48-0.52 [#1], Educational: 0.35-0.38 [#3-4]

**Why it works**: Adding exact words from chunk to Social Fragmentation dictionary

---

### **Chunk 195cdf4c** (Parliamentary abolition debate)

**Current scores**:
- Educational: 0.457 [#1]
- Governance: 0.327 [#3]

**Text contains**: "parlementaire hervormingen", "constitutionele hervormingen", "kabinet-Thorbecke II", "afschaffing slavernij"

**After fixes**:
- Governance gains: `parlementaire` (0.90), `constitutionele` (0.90), `hervormingen` (0.85), `kabinet` (0.90), `afschaffing` (0.90)
- Educational loses: `geschiedenisonderwijs` removed, generic terms reduced
- **Expected**: Governance: 0.48-0.52 [#1], Educational: 0.32-0.36 [#3-4]

**Why it works**: Adding political vocabulary that appears in chunk

---

### **Multi-Label System Improvement**

**Contextual terms (temporal/geographic/slavery)** remain in ALL topics:
- Continue to filter for historical Caribbean slavery content ✓
- Don't interfere with topic differentiation ✓
- Provide shared baseline boost for relevant content ✓

**Topic-specific terms** now better differentiate:
- Social Fragmentation: Stronger racial discourse vocabulary ✓
- Governance: Political process terminology ✓
- Educational: Tighter, less generic ✓

**Result**:
- Better topic separation (margins increase)
- Correct topics rank higher (#1-2 instead of #3-5)
- Contextual filtering preserved

---

## Implementation: Only Add/Remove Topic-Specific Terms

```python
# DO NOT REMOVE (keep these in ALL topics):
# - temporal, geographic, slavery-period terms

# REMOVE from Educational:
REMOVE_EDUCATIONAL = [
    'geschiedenisonderwijs',
    'curriculum ontwikkeling',
    'onderwijsvoorzieningen',
    'taalbeleid',  # Move to Governance
]

# ADD to Social Fragmentation & Racism:
ADD_SOCIAL = [
    ('racistisch', 0.95),
    ('discriminerend', 0.95),
    ('neger', 0.90),
    ('slavenhandel', 0.95),
    ('abolitionisten', 0.90),
    # ... (full list as before)
]

# ADD to Governance:
ADD_GOVERNANCE = [
    ('parlementaire', 0.90),
    ('kabinet', 0.90),
    ('hervormingen', 0.85),
    ('afschaffing', 0.90),
    ('taalbeleid', 0.80),  # From Educational
    # ... (full list as before)
]

# ADJUST weight for afschaffing in Educational:
# Either REDUCE to 0.75 or REMOVE entirely
```

This preserves the contextual filtering while improving topic-specific differentiation.

