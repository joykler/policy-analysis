# Contextual Embedding Fix

## Issue Identified

The previous approach embedded terms as standalone text:
```python
dict_terms_list = df_dict['term'].unique()  # 797 unique terms
# Embed: ["achievement gap", "educational equity", ...]
```

**Problem**: The same term (e.g., "achievement gap") got the SAME embedding regardless of which topic it belonged to. But "achievement gap" means different things in different contexts:
- In **Educational Disadvantage**: refers to learning outcomes
- In **Economic Vulnerability**: might refer to wealth/income disparities

---

## Solution: Contextual Embedding

Terms are now embedded WITH their topic context:
```python
# Format: "Topic: term"
dict_texts = [f"{row['topic']}: {row['term']}" for _, row in df_dict.iterrows()]
# Embed: ["Educational_Disadvantage: achievement gap",
#         "Economic_Vulnerability: achievement gap", ...]
```

**Benefits**:
- Same term in different topics → different embeddings
- Embeddings capture topic-specific semantic meaning
- Direct 1:1 correspondence: df_dict[i] → embedding[i]
- No index mapping needed

---

## What Changed

### Cell 6 - Dictionary Term Embeddings

**Before**:
```python
dict_terms_list = df_dict['term'].unique().tolist()  # 797 unique
embeddings = generate_embeddings(dict_terms_list, ...)  # Shape: (797, 768)
# Problem: df_dict has 848 rows, embeddings has 797 rows → IndexError
```

**After**:
```python
dict_texts = []
for idx, row in df_dict.iterrows():
    contextual_text = f"{row['topic']}: {row['term']}"
    dict_texts.append(contextual_text)
# 848 contextual texts

embeddings = generate_embeddings(dict_texts, ...)  # Shape: (848, 768)
# Perfect: df_dict has 848 rows, embeddings has 848 rows ✓
```

### Cell 7 - Removed

The mapping cell (Cell 9.5b) is no longer needed because embeddings now align 1:1 with df_dict rows.

---

## Example

### Dictionary Data:
```
df_dict:
   topic                              term              weight
0  Educational_Disadvantage          achievement gap   0.8
1  Educational_Disadvantage          school dropout    0.7
...
500 Economic_Vulnerability            achievement gap   0.6
501 Economic_Vulnerability            poverty cycle     0.9
```

### Embeddings Generated:
```
dict_texts[0] = "Educational_Disadvantage: achievement gap"
dict_texts[1] = "Educational_Disadvantage: school dropout"
...
dict_texts[500] = "Economic_Vulnerability: achievement gap"
dict_texts[501] = "Economic_Vulnerability: poverty cycle"

embeddings[0] = embedding for "Educational_Disadvantage: achievement gap"
embeddings[1] = embedding for "Educational_Disadvantage: school dropout"
...
embeddings[500] = embedding for "Economic_Vulnerability: achievement gap"
embeddings[501] = embedding for "Economic_Vulnerability: poverty cycle"
```

### Key Point:
`embeddings[0]` and `embeddings[500]` are DIFFERENT even though both contain "achievement gap", because they have different topic context!

---

## Impact on Visualizations

### Topic Clustering
Terms will now cluster by topic naturally, because:
- All "Educational_Disadvantage: ..." terms will be embedded in a similar semantic space
- All "Economic_Vulnerability: ..." terms will be in a different semantic space
- Cross-topic term similarities will reflect actual semantic overlap

### Coherence Metrics
Topic coherence scores will be more accurate because:
- Intra-topic similarity measures terms in their proper context
- Inter-topic separation measures actual semantic distinctiveness
- No artificial similarity due to shared terms

### Term Comparisons
When comparing models:
- Same contextual text through all models
- Fair comparison of how each model understands the topic-term relationship
- Differences show how domain adaptation affects contextualized understanding

---

## How to Use

### In Your Notebook Code:

**Direct indexing now works**:
```python
# Get embeddings for a specific topic
topic_mask = df_dict['topic'] == 'Educational_Disadvantage'
topic_embeddings = embeddings[topic_mask]  # ✓ Works perfectly!
```

**No helper function needed**:
```python
# OLD approach (no longer needed):
# topic_embeddings, mask = get_embeddings_for_dict_subset(...)

# NEW approach (simple and direct):
topic_data = df_dict[df_dict['topic'] == topic_name]
topic_indices = topic_data.index.tolist()
topic_embeddings = embeddings[topic_indices]
```

---

## Semantic Implications

### Why Context Matters

Consider the term "infrastructure":

**Without context** (old approach):
```
"infrastructure" → one embedding
```
- Model must choose: physical infrastructure? social infrastructure? educational infrastructure?
- Ambiguous, one-size-fits-all representation

**With context** (new approach):
```
"Educational_Disadvantage: infrastructure" → embedding A
"Economic_Vulnerability: infrastructure" → embedding B
"Structural_Neglect: infrastructure" → embedding C
```
- Each embedding captures topic-specific meaning
- Model can specialize: educational infrastructure = schools, libraries
- Economic infrastructure = jobs, businesses
- Structural = roads, utilities

### Impact on Model Training

When you eventually use these embeddings for model training:
- Model learns topic-aware representations
- Same term contributes differently to different topics
- Better topic separation in embedding space
- More nuanced understanding of term semantics

---

## Performance Notes

### Computation:
- **Before**: 797 embeddings to generate
- **After**: 848 embeddings to generate
- **Difference**: ~6.4% more computation
- **Time impact**: Negligible (seconds on GPU)

### Memory:
- **Before**: (797, 768) = 612,096 floats
- **After**: (848, 768) = 651,264 floats
- **Difference**: ~6.4% more memory
- **Impact**: Negligible (~157 KB per model)

### Quality:
- **Before**: Context-free, ambiguous
- **After**: Context-aware, semantically precise
- **Impact**: SIGNIFICANT improvement in semantic quality

**The tiny computational cost is MORE than worth the semantic benefit!**

---

## Testing the Fix

### Step 1: Restart Kernel
In Jupyter: **Kernel → Restart Kernel**

### Step 2: Run Setup Cells
```python
# Cell 1: Configuration
# Cell 2: Filesystem Setup
# Cell 3: Import Libraries
# Cell 4: Load Core Data
# Cell 5: Load BERTJE Models
# Cell 6: Generate Dictionary Term Embeddings (UPDATED)
```

### Step 3: Verify Output
Cell 6 should show:
```
======================================================================
GENERATING DICTIONARY TERM EMBEDDINGS
======================================================================

Dictionary entries to embed: 848
Format: 'Topic: term' (provides context)
Example: 'Educational_Disadvantage_&_Brain_Drain: onderwijsachterstand'

pretrained_bertje:
  Generating embeddings for 848 entries...
  Generated: (848, 768)
  Shape: [848 entries x 768 dimensions]
  Each term embedded WITH its topic context

======================================================================
DICTIONARY EMBEDDINGS COMPLETE
======================================================================
Entries embedded: 848
Models with embeddings: 1
  - pretrained_bertje    : (848, 768)

Contextual embedding approach:
  - Each term embedded WITH topic context
  - Same term in different topics gets different embeddings
  - Embeddings align 1:1 with df_dict rows
======================================================================
```

### Step 4: Run Cell 36 (or any visualization)
Should now work without IndexError!

---

## Troubleshooting

### Issue: Still getting IndexError
**Check**:
1. Did you restart the kernel? (Old embeddings may be cached)
2. Did you re-run Cell 6? (Need new contextual embeddings)
3. Does your Cell 36 code expect the old structure? (Update it)

### Issue: Embeddings shape is (797, 768) not (848, 768)
**Solution**: You're running the old Cell 6. Make sure notebook was saved and reloaded.

### Issue: Output shows "unique terms" instead of "entries"
**Solution**: Old Cell 6 code still in memory. Restart kernel and re-run.

---

## Summary

| Aspect | Before | After |
|--------|--------|-------|
| Input | Unique terms only | All df_dict entries with context |
| Format | `"term"` | `"Topic: term"` |
| Count | 797 embeddings | 848 embeddings |
| Alignment | Mismatched with df_dict | 1:1 with df_dict |
| Semantics | Context-free | Context-aware |
| Indexing | Required mapping | Direct indexing |
| Quality | Ambiguous | Precise |

**Result**: Better semantic representation, simpler code, no IndexError!

---

*Updated: 2026-01-05*
*Issue: Terms should be embedded with topic context*
*Fix: Contextual embedding format "Topic: term"*
