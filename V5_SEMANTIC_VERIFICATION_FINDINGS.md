# V5 Semantic Verification - Key Findings

## Methodology

Examined 10 high-confidence chunks by reading full text and counting topic-specific keywords to verify if primary topic assignments are semantically accurate.

---

## Key Finding: Structural Neglect Over-Triggering Confirmed

### Evidence from Chunk Reading

**Chunks 1-3: All assigned to "Structural Neglect & Infrastructure Gaps"**

**Chunk 1** (c12df80d:00000):
- Primary: Structural Neglect (score 0.590)
- Keyword counts: Educational=0, Social=1, Gov=0, Econ=0, **Infra=0**
- Text appears to be about slavery history/documentation
- **Assessment**: Should likely be Educational or Social, NOT infrastructure

**Chunk 2** (676238ea:00000):
- Primary: Structural Neglect (score 0.499)
- Keyword counts: ALL ZERO across all topics
- Text is generic historical content
- **Assessment**: Structura Neglect shouldn't be primary with 0 infrastructure keywords

**Chunk 3** (fded2157:00000):
- Primary: Structural Neglect (score 0.514)
- Keywords: Social=1, all others=0, **Infra=0**
- Text: "publieke herdenking slavernij... geschiedeniscanon... memory politics"
- **Assessment**: About public memory/commemoration, should be Social/Educational, NOT infrastructure

### Pattern Detected

**Structural Neglect is triggering on generic slavery/history content** despite having:
- 0 infrastructure keywords in chunks
- 0 neglect keywords in chunks
- Content clearly about other topics (memory, history, social)

This confirms the issue: **Structural Neglect dictionary has too many generic historical terms**, causing it to match ANY slavery-related text even when infrastructure/neglect isn't the topic.

---

## Chunks with Better Assignments

**Chunk 4** (ade2300d:00000):
- Primary: Persistent Poverty & Economic (score 0.534, margin 0.083)
- Keywords: Social=1, **Econ=1**
- Text: "voc... slaafgemaakten... handel arakan... slavenhandelaren"
- **Assessment**: ✓ CORRECT - about slave trade economics

**Chunk 5** (75b05443:00000):
- Primary: Persistent Poverty & Economic (score 0.491)
- Keywords: Edu=1, Social=3, **Econ=1**
- **Assessment**: ✓ Reasonable, though multi-topic (Social also high)

**Chunk 6** (c167cfff:00000):
- Primary: Persistent Poverty & Economic (score 0.445)
- Keywords: Social=1, Infra=0
- **Assessment**: ✓ Reasonable given economic context

---

## Multi-Label Examples (Low Confidence)

**Chunk 8f840314:00000**:
- Primary: Structural Neglect (0.590)
- Rank 2: Social (0.559) - only 0.031 difference
- Rank 3: Economic (0.550)
- Text: "ongelijkheid nazaten slaafgemaakten... racisme intersectionaliteit"
- **Assessment**: Should be Social #1, but has small margins indicating mult-topic content

---

## Root Cause Analysis

From semantic reading, the problem is clear:

### 1. **Structural Neglect Dictionary Composition**

As verified earlier:
- Infrastructure-specific: 6 terms (5.3%)
- Neglect-specific: 1 term (0.9%)
- **Generic historical: 39 terms (34.5%)**

Result: Structural Neglect vector is dominated by generic terms like:
- `slavernijverleden`, `slavernijgeschiedenis`, `geschiedenis`, `historisch`
- `koloniale`, `slavernij`, `verleden`

These match ANY historical slavery text, not infrastructure-specific content.

### 2. **Semantic Mismatch Examples**

**What Structural Neglect SHOULD match**:
- "achterstallig onderhoud infrastructuur"
- "verwaarlozing publieke voorzieningen"
- "gebrek aan investeringen basisinfrastructuur"

**What it's ACTUALLY matching**:
- "publieke herdenking slavernij" (public memory - should be Social/Educational)
- Generic slavery history documentation (should be Educational)
- Historical references without infrastructure context (should be topic-specific)

---

## Impact on BERTje Training

### Positive Aspects ✓

1. **Economic/Poverty assignments look reasonable** (Chunks 4-6 correctly match economic content)
2. **Multi-label examples exist** (low-confidence chunks show appropriate overlap)
3. **Some high-confidence chunks are correct** (economic chunks verified semantically)

### Concerning Aspects ❌

1. **Structural Neglect over-represents** (23.8% of corpus)
   - Many chunks incorrectly assigned due to generic terms
   - Will teach BERTje wrong patterns: "any slavery history → infrastructure"

2. **Topic confusion for memorial/historical content**
   - Public memory chunks (should be Social/Educational) → Structural Neglect
   - Historical documentation (should be Educational) → Structural Neglect

3. **Infrastructure underrepresented in its own topic**
   - Even high-confidence Structural Neglect chunks have 0 infrastructure keywords
   - Actual infrastructure content may be buried in no-confidence chunks

---

## Recommendations

### Option 1: Re-Curate Structural Neglect (Recommended)

**Remove generic historical terms from Structural Neglect**:
- Keep ONLY: `verwaarlozing`, `achterstelling`, `infrastructuur`, `voorzieningen`, `achterstallig`
- Remove: `slavernijverleden`, `slavernijgeschiedenis`, `geschiedenis`, `historisch`, `koloniale`, `verleden`, etc.

**Expected impact**:
- Structural Neglect drops from 23.8% to ~10-15% (more realistic)
- Freed chunks re-assigned to appropriate topics (Educational, Social)
- High-confidence Structural chunks actually about infrastructure

### Option 2: Accept and Monitor

**If you proceed with current V5**:
- BERTje will learn that "slavery history" often maps to Structural Neglect
- Monitor BERTje predictions on validation set
- If BERTje over-predicts Structural Neglect, confirms the issue
- Can re-train with filtered data later

**Advantage**: Faster to production, test empirically
**Risk**: Wasted training time if BERTje learns incorrect patterns

### Option 3: Weight Down Structural Neglect in Training

**Use confidence-weighted loss with manual adjustments**:
- High-confidence Economic/Social: weight 1.0
- High-confidence Structural: weight 0.5 (reduce influence)
- This partially mitigates the over-triggering issue

**Advantage**: Quick fix without re-curation
**Disadvantage**: Doesn't solve root cause

---

## Conclusion

**V5 cosine labeling has a specific, identifiable problem**: Structural Neglect dictionary contains 34.5% generic historical terms, causing it to over-trigger on any slavery-related content even when infrastructure isn't mentioned.

**Evidence**:
- 3/3 high-confidence Structural Neglect chunks had 0 infrastructure keywords
- These chunks were semantically about history/memory, not infrastructure
- Structural Neglect represents 23.8% of corpus (over-represented)

**For BERTje training**:
- If you want accurate transfer learning → **re-curate Structural Neglect first** (remove generic terms)
- If you want to test quickly → **proceed but monitor validation performance** closely
- If BERTje over-predicts Structural Neglect on validation → confirms dictionary issue

**Recommendation**: Spend 30 minutes re-curating Structural Neglect (remove ~30 generic terms) to avoid training BERTje on incorrect patterns. The economic, social, and governance topics appear more accurate and will transfer better.
