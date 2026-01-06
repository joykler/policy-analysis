# Dictionary Curation Guide for BERTJE Semantic Training

## Purpose of This Document

This guide provides systematic methodology for curating BERTJE nearest-neighbor expanded dictionaries in topic modeling workflows. It is designed to be **reusable across different topic frameworks** and **applicable to both stages** of the two-stage training approach.

---

## Overview: Two-Stage Dictionary Training

### Stage 1: Domain Corpus (Semantic Foundation)
- **Corpus Type**: Texts specifically about the research domain (e.g., slavery legacy, climate change, healthcare disparities)
- **Purpose**: Teach BERTJE the semantic space of your topics
- **Dictionary Strategy**: MORE PERMISSIVE - include domain-specific historical/contextual terms
- **Goal**: BERTJE learns what the topics "sound like" in expert/scholarly discussion

### Stage 2: Policy/Application Corpus (Problem Detection)
- **Corpus Type**: General policy/application documents in the target domain
- **Purpose**: Apply learned semantics to identify topic manifestations in practice
- **Dictionary Strategy**: MORE RESTRICTIVE - focus on contemporary problem/application language
- **Goal**: BERTJE identifies topics even when domain background isn't explicitly stated

---

## Understanding the Weighting Architecture

### Weight Tier System (Typical 7-Tier Structure)

Your seed dictionary should use a structured weighting system that signals semantic importance:

| Weight | Category | Purpose | Example Use |
|--------|----------|---------|-------------|
| **1.00** | `core_problem` | The central concept itself | "climate crisis", "racial discrimination", "poverty" |
| **0.95** | `strong_problem` | Clear manifestations/indicators of the core problem | "drought", "segregation", "unemployment" |
| **0.85** | `related_strong` | Domain terms where problems manifest; institutional context | "agriculture", "schools", "labor market" |
| **0.80** | `related_strong_specific` | Specialized high-weight context (optional tier) | "smallholder farming", "primary education" |
| **0.75** | `related_moderate` | Relevant actors, processes, or outcomes | "farmers", "students", "workers" |
| **0.70** | `related_moderate_weak` | Broader contextual terms | "policy", "development", "infrastructure" |
| **0.65** | `related_weak` | Weak contextual clues; historical background | "plantation", "colonial trade", "historical patterns" |
| **0.55** | `era_context` | Temporal markers for domain discussion | "colonial period", "pre-industrial", "historical" |
| **0.50** | `geographic_context` | Spatial markers for domain specificity | "Caribbean", "Sub-Saharan Africa", "rural areas" |

### Why Not Remove Low-Weight Terms?

**Low-weight terms serve strategic purposes:**

1. **Temporal markers** (0.55) help BERTJE distinguish historical discussion from contemporary manifestations
2. **Geographic markers** (0.50) help BERTJE focus on specific contexts vs. generic discussions
3. **Weak related terms** (0.65) provide background context without dominating

**The weighted approach teaches BERTJE that:**
- High-weight term + low-weight context markers = HIGH relevance
- Only low-weight terms without high-weight problems = LOW relevance

This prevents BERTJE from being a simple keyword detector and makes it a **contextual semantic pattern recognizer**.

---

## What BERTJE Expansion Produces

BERTJE nearest-neighbor expansion takes your seed dictionary and finds semantically similar terms in your corpus. The output includes:

- `term`: The expanded term found
- `parent`: The seed term it was expanded from
- `cosine`: Cosine similarity to parent (typically 0.65-1.0)
- `df`: Document frequency (how many documents contain this term)
- `weight`: Inherited from parent's weight
- `category`: Inherited from parent's category
- `topic`: The topic it belongs to
- `is_seed`: 1 if original seed, 0 if expanded

---

## Systematic Curation Methodology
Process the topics one by one, go through the phases for one topic and stop after all the keywords for a topic are adressed.

### Phase 1: Automatic Removal (Technical Errors)

Remove terms that are clearly errors, regardless of corpus type:

#### 1. Morphological Fragments
**Pattern**: Suffix/prefix fragments with no standalone meaning
- Examples: "lingen" (from "leerlingen"), "denten" (from "studenten"), "bon" (from "Bonaire")
- **Action**: Remove all terms where `len(term) < 4 AND not a real word`

#### 2. Extreme Low Similarity
**Pattern**: Cosine similarity too low indicates weak semantic connection
- **Threshold**: `cosine < 0.65` (adjust based on your corpus quality)
- **Action**: Remove - these are noise

#### 3. Single Document Frequency
**Pattern**: Term appears only once in entire corpus
- **Threshold**: `df == 1` (unless corpus is very small)
- **Action**: Remove - likely OCR error, typo, or extreme outlier

#### 4. Obvious Encoding/OCR Errors
**Pattern**: Broken characters, malformed words
- Examples: "schiedenis" (missing "ge-"), "barri​ère" (encoding issue)
- **Action**: Remove or fix if correctable

---

### Phase 2: Semantic Drift Detection (Wrong Meaning)
Read the keywords as a llm dont use a script but use real understanding. Identify terms where BERTJE found orthographic similarity but wrong semantic space.:

#### Detection Criteria:
1. **Low cosine + High inherited weight**
   - Example: cosine < 0.72 but inheriting `strong_problem` (0.95)
   - Red flag: Semantically distant term getting high importance

2. **Polysemous confusion**
   - Example: "college" (school vs. executive board), "kast" (cabinet furniture vs. caste)
   - Check: Does this term have multiple meanings, and did BERTJE get the wrong one?

3. **Homonym geographic confusion**
   - Example: "Cuba" expanded from "Aruba" (different country), "Niger" from "Nigeria"
   - Check: Geographic similarity ≠ semantic relevance

#### Action Decision Tree:
```
If semantic_drift detected:
  If term has correct meaning in SOME contexts:
    → REMOVE (too ambiguous, will create noise)
  Else:
    → REMOVE (wrong meaning entirely)
```

---

### Phase 3: Overgeneralization Control (Too Broad)

Identify terms that are semantically related but too generic to be useful:

#### Patterns to Watch:

1. **Generic fragments of specific terms**
   - You have: "onderwijsniveau" (education level), "opleidingsniveau" (training level)
   - BERTJE adds: "niveau" (level) - TOO GENERIC
   - **Action**: Remove (already have specific versions)

2. **Ultra-high frequency terms**
   - **Threshold**: `df > 300` AND `weight > 0.70` (adjust for corpus size)
   - Example: "nederlandse" appearing in 797/1000 documents
   - **Problem**: Overwhelms signal, appears in every document
   - **Action**: LOWER weight by 0.15-0.25 OR remove if truly uninformative

3. **Ambiguous institutional terms**
   - Example: "organisaties" (organizations), "instituten" (institutes)
   - **Check**: Does this add specificity or just noise?
   - **Action**: If too generic, lower weight significantly or remove

4. **Overly broad problem terms**
   - You have: "taalachterstand" (language disadvantage), "onderwijsachterstand" (education disadvantage)
   - BERTJE adds: "achterstand" (disadvantage) - TOO BROAD
   - **Action**: Remove (already have specific manifestations)

---

### Phase 4: Category Corrections (Miscategorization)

BERTJE inherits category from parent, but expanded term may belong elsewhere:

#### Common Miscategorizations:

1. **Historical processes miscategorized as contemporary problems**
   - **Pattern**: Historical era terms inheriting `strong_problem` (0.95)
   - Example: "deportaties" (historical forced migration) from "emigratie" (contemporary emigration)
   - **Stage 1**: Move to `era_context` (0.55) - keep as historical learning signal
   - **Stage 2**: Remove or keep at 0.55 if policy documents reference history

2. **Related terms overcategorized**
   - **Pattern**: Broader semantic field inheriting parent's high category
   - Example: "arbeidsmigratie" (labor migration) from "emigratie" (brain drain parent at 0.95)
   - **Action**: Lower to `related_strong` (0.85) - relevant but not the core problem

3. **Solutions/interventions appearing**
   - Example: "schuldhulpverlening" (debt assistance) from "schuld" (debt problem)
   - **Decision**:
     - If you want to track policy responses: Keep at 0.70 `related_moderate`
     - If only tracking problems: Remove or lower to 0.60

---

### Phase 5: Weight Calibration (Fine-Tuning)

Adjust inherited weights based on actual term characteristics:

#### Calibration Rules:

1. **High document frequency dampening**
   ```
   If df > 300 AND weight > 0.70:
     → Lower weight by 0.15-0.20

   If df > 500 AND weight > 0.60:
     → Lower weight by 0.20-0.25
   ```

2. **Semantic distance dampening**
   ```
   If cosine < 0.75 AND weight >= 0.95:
     → Lower weight by 0.10 (e.g., 0.95 → 0.85)

   If cosine < 0.72 AND weight >= 0.85:
     → Consider lowering or removing
   ```

3. **Category-specific adjustments**
   - `era_context` and `geographic_context`: Generally keep low (0.50-0.55)
   - `core_problem`: Only highest-quality expansions should remain at 1.00
   - `strong_problem`: Review all with cosine < 0.75

---



## Stage-Specific Strategies

### Stage 1: Domain Corpus (Semantic Foundation)

**Context**: Training on texts that explicitly discuss your research domain (e.g., slavery legacy scholarship, climate science papers, public health research)

#### Curation Philosophy: PERMISSIVE
- **KEEP** more domain-specific historical/technical terms
- **KEEP** era/temporal markers that indicate domain discussion
- **KEEP** broader geographic/contextual terms
- **ACCEPT** lower cosine thresholds (0.68+) for domain-specific vocabulary

#### What to Keep in Stage 1:

1. **Historical/Background Terms** (era_context)
   - Domain's historical processes, even if not contemporary problems
   - Example: "slave trade routes", "colonial administration", "plantation system"
   - Weight: 0.55-0.65 (contextual, not core)

2. **Domain-Specific Technical Vocabulary**
   - Scholarly/expert terminology for your domain
   - Example: "epidemiology", "intersectionality", "extractive economy"
   - Weight: Keep inherited or slightly lower

3. **Intersectional Bridge Terms**
   - Terms that explicitly link historical to contemporary
   - Example: "colonial education system", "plantation economy legacy"
   - Weight: Keep high (0.75-0.85)

4. **Comparative Geographic Terms**
   - Related regions for comparative context
   - Example: If studying Dutch Caribbean, keep "Cuba", "Jamaica" at low weight (0.40)
   - Weight: 0.40-0.50

5. **Domain Debate/Discourse Terms**
   - Terms about discussing the domain itself
   - Example: "reparations debate", "climate denial", "health disparities research"
   - Weight: 0.70-0.75

#### What to Still Remove in Stage 1:
- Morphological fragments (always remove)
- Semantic drift terms (wrong meaning)
- Extreme overgeneralization (uninformative)
- Non-domain geographic terms (e.g., "Cuba" if studying Sub-Saharan Africa)

---

### Stage 2: Policy/Application Corpus (Problem Detection)

**Context**: Training on policy documents, news, or application texts where domain background may not be explicit

#### Curation Philosophy: RESTRICTIVE
- **REMOVE** purely historical terms without contemporary relevance
- **REMOVE** domain-specific jargon unless it appears in policy
- **FOCUS** on problem manifestation language
- **REQUIRE** higher cosine thresholds (0.72+)

#### What to Remove in Stage 2:

1. **Purely Historical Terms**
   - Terms about historical processes without contemporary policy relevance
   - Example: "slave ship routes", "colonial governors" (unless still referenced)
   - Exception: Keep if policy documents explicitly discuss historical causes

2. **Academic/Scholarly Jargon**
   - Technical terms that don't appear in policy language
   - Example: "historiography", "epistemology" (unless in policy discourse)

3. **Low-frequency domain terms**
   - If term has `df < 5` in policy corpus, likely not policy-relevant
   - Remove unless clearly important

4. **Historical era markers**
   - "colonial period", "pre-emancipation", "historical era"
   - Lower weights significantly (0.45) or remove

#### What to Keep in Stage 2:

1. **Contemporary Problem Language**
   - How policy documents describe issues
   - Example: "achievement gap", "wealth disparity", "governance challenges"
   - Keep high weights (0.85-1.00)

2. **Policy Intervention Terms**
   - If tracking policy responses
   - Example: "development programs", "anti-discrimination policy"
   - Weight: 0.70-0.75

3. **Institutional/Administrative Terms**
   - How policy documents reference structures
   - Example: "ministry", "local government", "education system"
   - Weight: 0.70-0.85

---

## Practical Curation Workflow

### Step-by-Step Process

#### 1. Export expanded dictionary to spreadsheet
Include columns: `topic`, `term`, `parent`, `cosine`, `df`, `weight`, `category`, `is_seed`

#### 2. Add curation decision column
Options: `KEEP`, `REMOVE`, `REWEIGHT`, `RECATEGORIZE`

#### 3. Sort strategically
Primary sort: `weight` (descending) - review high-impact terms first
Secondary sort: `cosine` (ascending) - within each weight tier, review lowest similarity first

#### 4. Apply automatic filters
```python
# Pseudo-code
for term in expanded_terms:
    if len(term) < 4 and not is_valid_word(term):
        decision = "REMOVE"  # Morphological fragment
    elif term.cosine < 0.65:
        decision = "REMOVE"  # Too semantically distant
    elif term.df == 1:
        decision = "REMOVE"  # Single occurrence
    elif is_encoding_error(term):
        decision = "REMOVE"  # Technical error
```

#### 5. Manual review priorities (in order)

**Priority 1: High-Impact Terms**
- All `core_problem` (1.00) expansions - verify each manually
- All `strong_problem` (0.95) with cosine < 0.75 - likely miscategorized
- All terms with df > 300 - high frequency needs correct weighting

**Priority 2: Category Mismatches**
- Historical terms with contemporary problem categories
- Generic terms with overly high weights
- Solution terms miscategorized as problems

**Priority 3: Moderate Terms**
- `related_strong` (0.85) with cosine < 0.75
- `related_moderate` with unusual patterns
- Ambiguous polysemous terms

**Priority 4: Low Impact**
- `era_context` and `geographic_context` (already low weight)
- High cosine (>0.85) semantic variants (usually fine)
- `related_weak` terms (already low impact)

#### 6. Document decisions
For each curated term, note reason for decision:
- "Semantic drift - wrong meaning"
- "Overgeneralization - too broad"
- "Historical process - moved to era_context"
- "High df - lowered weight"
- "Morphological fragment - removed"

---

## Quality Checks After Curation

### Sanity Checks:

1. **Coverage Check**
   - Each topic should have: 50-150 terms after curation (depending on topic complexity)
   - Distribution: ~10-20% at 0.85+, ~30-40% at 0.70-0.84, ~30-40% at 0.50-0.69

2. **Weight Distribution**
   - Very few terms (5-15) at 1.00 (core_problem)
   - Moderate terms (20-40) at 0.95 (strong_problem)
   - Most terms at 0.70-0.85 (related categories)

3. **Parent Review**
   - Check which parents generated most expansions
   - If one parent created 50+ expansions, review that family carefully
   - High-expansion parents often need quality control

4. **Cross-Topic Check**
   - Some terms should appear in multiple topics (intersectionality)
   - But if >30% of terms are cross-topic, dictionary may be too generic

5. **Document Frequency Distribution**
   - Most terms should have df = 5-100
   - Very few terms with df > 300
   - Some rare terms (df < 5) are okay if highly specific

---

## Decision Trees for Common Patterns

### Pattern 1: Low Cosine + High Weight

```
Term has cosine < 0.72 AND weight >= 0.95:

→ Is it semantically related to parent topic?
  NO: Remove (semantic drift)
  YES: Continue

→ Is it a historical process term?
  YES, Stage 1: Move to era_context (0.55)
  YES, Stage 2: Remove or keep at 0.50
  NO: Continue

→ Is it broader than parent?
  YES: Lower weight to related_strong (0.85)
  NO: Keep but lower weight by 0.10
```

### Pattern 2: High Document Frequency

```
Term has df > 300:

→ Is it domain-specific or ultra-generic?
  Generic (e.g., "policy", "government"): Remove or lower to 0.60
  Domain-specific: Continue

→ What is current weight?
  > 0.85: Lower by 0.20-0.25
  0.70-0.85: Lower by 0.15-0.20
  < 0.70: Keep as-is (already low impact)
```

### Pattern 3: Historical Term in Contemporary Category

```
Term is about historical era AND category = strong_problem/core_problem:

→ Stage 1 (Domain Corpus):
  Move to era_context (0.55)
  Reason: Valuable for learning but not contemporary problem

→ Stage 2 (Policy Corpus):
  Check df in policy corpus:
    df > 10: Keep at era_context (0.55) - policies reference history
    df < 5: Remove - not policy-relevant
```

### Pattern 4: Parent Generated Many Expansions (>40)

```
Parent term generated >40 expansions:

→ This indicates:
  1. Parent is very broad/generic, OR
  2. Parent is very common in corpus, OR
  3. Semantic space is large

→ Action:
  Review ALL expansions from this parent
  Apply stricter cosine threshold (0.75 instead of 0.70)
  Remove overgeneralizations aggressively

→ Common problematic parents:
  - "geschiedenis" (history) - expands to all historical terms
  - "onderwijs" (education) - expands to all education terms
  - "economie" (economy) - expands to all economic terms
```

---

## Stage Transition: From Stage 1 to Stage 2

When moving from Stage 1 (domain corpus) to Stage 2 (policy corpus):

### 1. Start with Stage 1 Curated Dictionary
- DO NOT start from scratch
- Stage 1 dictionary is the seed for Stage 2 expansion

### 2. Stage 2 Expansion Process
- Use BERTJE model trained on Stage 1
- Expand from same seed terms into policy corpus
- BERTJE now has semantic understanding from Stage 1

### 3. Compare Stage 1 and Stage 2 Expansions
- Terms that appear in BOTH: Likely robust, keep
- Terms ONLY in Stage 1: Historical/domain jargon, evaluate for policy relevance
- NEW terms in Stage 2: Policy-specific language, valuable additions

### 4. Stage 2 Curation Strategy
- More restrictive than Stage 1
- Focus on terms that appear in policy discourse
- Remove domain jargon that didn't transfer to policy corpus

---

## Common Mistakes to Avoid

### 1. Over-Removing Low Cosine Terms
- **Mistake**: Removing all terms with cosine < 0.75
- **Why wrong**: Domain-specific rare terms may have lower cosine but high value
- **Better**: Use cosine < 0.65 as hard threshold, manually review 0.65-0.75

### 2. Keeping All High Cosine Terms
- **Mistake**: Assuming cosine > 0.85 means always keep
- **Why wrong**: Semantic variants can be redundant or fragments
- **Better**: Still check for morphological fragments and redundancy

### 3. Ignoring Document Frequency
- **Mistake**: Not considering how often term appears
- **Why wrong**: df=500 term at weight 0.95 will dominate all scoring
- **Better**: Always adjust weights for high-frequency terms

### 4. Inconsistent Category Assignment
- **Mistake**: Same type of term categorized differently across topics
- **Why wrong**: Creates inconsistent learning signal for BERTJE
- **Better**: Maintain consistent logic (e.g., all historical processes → era_context)

### 5. Removing All Low-Weight Terms
- **Mistake**: "These are only 0.55, let's remove them"
- **Why wrong**: Contextual markers are strategically valuable
- **Better**: Keep era_context and geographic_context at low weights

---

## Validation: How to Know Curation Was Successful

### After curation, check:

1. **Vocabulary Coherence**
   - Read through each topic's term list
   - Ask: "Do these terms collectively describe my topic?"
   - If list feels random or disconnected, more curation needed

2. **Weight Distribution Makes Sense**
   - Heaviest terms (0.95-1.00) are truly the core problems
   - Medium terms (0.70-0.85) provide semantic context
   - Light terms (0.50-0.65) are markers, not signals

3. **Cross-Topic Patterns**
   - Shared terms across topics should make conceptual sense
   - Example: "discriminatie" appearing in both racism and education topics = good
   - Example: "niveau" appearing everywhere = bad (too generic)

4. **Test on Sample Documents**
   - Score a few known-relevant documents with curated dictionary
   - Check: Do they score high on expected topics?
   - Check: Do irrelevant documents score low?

5. **Compare Stage 1 and Stage 2** (if applicable)
   - Stage 2 should be more focused on contemporary problems
   - Stage 1 can be richer in domain background terms
   - Both should share core problem vocabulary

---

## Template for Documentation

After completing curation, document your decisions:

```markdown
# Dictionary Curation Report: [Project Name] - [Stage 1/2]

## Corpus Information
- Corpus type: [Domain/Policy]
- Number of documents: [N]
- Date range: [YYYY-YYYY]
- Topics: [List topics]

## Expansion Statistics
- Seed terms: [N]
- Expanded terms: [N]
- After automatic removal: [N]
- After manual curation: [N]
- Final dictionary size: [N]

## Curation Decisions Summary

### Automatic Removals
- Morphological fragments: [N] terms
- Low cosine (<0.65): [N] terms
- Single document frequency: [N] terms
- Encoding errors: [N] terms

### Category Reassignments
- Moved to era_context: [N] terms
- Moved to related_strong: [N] terms
- [List major reassignment patterns]

### Weight Adjustments
- Lowered due to high df: [N] terms
- Lowered due to low cosine: [N] terms
- [List adjustment patterns]

### Manual Removals by Reason
- Semantic drift: [N] terms
- Overgeneralization: [N] terms
- Wrong geographic scope: [N] terms
- Other: [N] terms

## Notable Patterns
- [Parent X] generated [N] expansions, reviewed for quality
- [Term Y] moved from [category A] to [category B] because [reason]
- High-frequency terms [list] adjusted weights

## Quality Checks Passed
- [ ] Coverage check: Each topic has appropriate term count
- [ ] Weight distribution: Pyramid structure maintained
- [ ] Parent review: High-expansion parents reviewed
- [ ] Cross-topic check: Intersections make sense
- [ ] Document frequency: Distribution is reasonable

## Stage-Specific Notes
[Stage 1: Note domain-specific decisions]
[Stage 2: Note policy-focus decisions, comparison with Stage 1]
```

---

## Quick Reference: Curation Cheat Sheet

| If you see... | Action | Reason |
|--------------|--------|--------|
| len(term) < 4 AND fragment | REMOVE | Morphological error |
| cosine < 0.65 | REMOVE | Too distant |
| df == 1 | REMOVE | Likely error |
| df > 300 AND weight > 0.70 | LOWER by 0.15-0.20 | Too frequent |
| Historical + strong_problem | RECATEGORIZE to era_context | Wrong category |
| cosine < 0.72 AND weight >= 0.95 | REVIEW manually | Likely miscategorized |
| Semantic drift detected | REMOVE | Wrong meaning |
| Term broader than parent | LOWER weight or REMOVE | Overgeneralization |
| Parent created >40 expansions | REVIEW ALL | Quality control needed |
| Stage 2: Only in domain jargon | REMOVE | Not policy-relevant |
| Stage 1: Historical background | KEEP at 0.55 | Learning signal |

---

## Conclusion

Dictionary curation is about **teaching BERTJE what matters**:
- High weights = "Pay attention to this"
- Low weights = "Use this for context"
- Removal = "This is noise"

The goal is not perfect vocabulary, but **semantically coherent training signal** that helps BERTJE learn to recognize your topics in text.

Good curation produces dictionaries where:
1. Core terms are truly central to the topic
2. Related terms provide semantic context without overwhelming
3. Contextual markers help BERTJE distinguish relevant from irrelevant
4. Noise is minimized but semantic richness is preserved

**Remember**: You're not creating a comprehensive glossary. You're creating a **weighted training signal** for a neural model to learn topic semantics.
