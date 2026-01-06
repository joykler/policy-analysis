# Visual Comparison: v18 vs v19 Embedding Approach

## v18: Separate Embedding Operations

```
┌─────────────────────────────────────────────────────────────┐
│ CELL 3.2: Encode Vocabulary Only                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Vocabulary Terms                                           │
│  ┌──────────────┐                                           │
│  │ "poverty"    │                                           │
│  │ "inequality" │                                           │
│  │ "education"  │    ──────►  SBERT Encoder  ──────►       │
│  │ "healthcare" │                                           │
│  │ ...          │                                           │
│  └──────────────┘                                           │
│                                                              │
│                              vocab_embeddings.npy           │
│                              ┌────────────────┐             │
│                              │ [0.12, 0.45, ...]│            │
│                              │ [0.33, 0.21, ...]│            │
│                              │ [0.55, 0.67, ...]│            │
│                              └────────────────┘             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ CELL 3.3: Query-Time Re-Encoding                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  For EACH Seed Term:                                        │
│  ┌──────────────┐                                           │
│  │ "slavery"    │  ──────►  SBERT Encoder  ──────►         │
│  └──────────────┘              ↓                            │
│                           [0.28, 0.91, ...]                 │
│                                ↓                            │
│                      NearestNeighbors.kneighbors()          │
│                                ↓                            │
│                       Find similar terms in vocab           │
│                                                              │
│  ⚠️  PROBLEM:                                               │
│  - Seed embedded separately from vocab                      │
│  - Different context = inconsistent similarities            │
│  - Repeated encoding = slower & less reproducible           │
└─────────────────────────────────────────────────────────────┘
```

## v19: Unified Embedding Space

```
┌─────────────────────────────────────────────────────────────┐
│ CELL 3.2: Unified Embedding (Vocab + Seeds Together)       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Combined Terms List                                        │
│  ┌──────────────────┐                                       │
│  │ Vocabulary:      │                                       │
│  │ "poverty"        │                                       │
│  │ "inequality"     │                                       │
│  │ "education"      │                                       │
│  │ "healthcare"     │    ──────►  SBERT Encoder  ──────►   │
│  │ ...              │              (Single Pass!)           │
│  ├──────────────────┤                    ↓                  │
│  │ Seed Terms:      │            Unified Embeddings         │
│  │ "slavery"        │                    ↓                  │
│  │ "discrimination" │                Split                  │
│  │ "exploitation"   │                    ↓                  │
│  │ ...              │          ┌─────────┴─────────┐        │
│  └──────────────────┘          ↓                   ↓        │
│                       vocab_embeddings    seed_embeddings   │
│                       ┌──────────────┐   ┌──────────────┐  │
│                       │[0.12, 0.45,...]  │[0.28, 0.91,...]  │
│                       │[0.33, 0.21,...]  │[0.41, 0.73,...]  │
│                       │[0.55, 0.67,...]  │[0.19, 0.52,...]  │
│                       └──────────────┘   └──────────────┘  │
│                                                              │
│  ✅ SAME EMBEDDING CONTEXT = CONSISTENT SIMILARITIES        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ CELL 3.3: Direct Cosine Similarity (No Re-Encoding)        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Load Pre-Computed Embeddings:                              │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │ seed_embeddings  │         │ vocab_embeddings │         │
│  │ (N_seeds × dim)  │         │ (N_vocab × dim)  │         │
│  └──────────────────┘         └──────────────────┘         │
│           ↓                            ↓                    │
│           └────────────┬───────────────┘                    │
│                        ↓                                    │
│           cosine_similarity(seed_emb, vocab_emb)            │
│                        ↓                                    │
│              Similarity Matrix                              │
│              (N_seeds × N_vocab)                            │
│        ┌─────────────────────────────┐                     │
│        │  v1    v2    v3   ...  vN   │                     │
│   s1   │ 0.85  0.32  0.91  ... 0.12  │                     │
│   s2   │ 0.42  0.78  0.33  ... 0.55  │                     │
│   s3   │ 0.67  0.21  0.88  ... 0.44  │                     │
│   ...  │ ...   ...   ...   ... ...   │                     │
│        └─────────────────────────────┘                     │
│                        ↓                                    │
│              For each seed:                                 │
│              np.argsort(row)[-k:]  # Get top-k              │
│                        ↓                                    │
│              Expanded terms with accurate scores            │
│                                                              │
│  ✅ ADVANTAGES:                                             │
│  - No re-encoding (uses pre-computed embeddings)            │
│  - Matrix operations (fast & vectorized)                    │
│  - Reproducible (same inputs = same outputs)                │
│  - Contextually consistent similarities                     │
└─────────────────────────────────────────────────────────────┘
```

## Key Differences Summary

| Aspect | v18 (Old) | v19 (New) |
|--------|-----------|-----------|
| **Embedding Strategy** | Separate (vocab then seeds) | Unified (vocab + seeds together) |
| **Consistency** | ❌ Different contexts | ✅ Same context |
| **Similarity Method** | NearestNeighbors + re-encoding | Pre-computed cosine similarity |
| **Performance** | N query-time encodings | 1 batch encoding + matrix ops |
| **Reproducibility** | ⚠️ May vary | ✅ Always identical |
| **Accuracy** | Lower (context mismatch) | Higher (consistent space) |
| **Memory** | Lower (on-demand encoding) | Higher (store all embeddings) |
| **Scalability** | Poor (O(N) queries) | Good (matrix operations) |

## Practical Example

**Scenario**: Finding terms similar to seed "slavery"

### v18 Approach:
```python
# Step 1: Embed vocabulary (Cell 3.2)
vocab_emb = embed(["poverty", "inequality", "education", ...])

# Step 2: Query time (Cell 3.3)
query_emb = embed(["slavery"])  # ⚠️ Different encoding!
similarities = cosine(query_emb, vocab_emb)
```

**Problem**: `embed(["slavery"])` alone vs `embed([..., "slavery"])` in context
- Different attention patterns
- Different normalization
- Slightly different vector

### v19 Approach:
```python
# Step 1: Unified embedding (Cell 3.2)
all_emb = embed(["poverty", "inequality", "education", ..., "slavery"])
vocab_emb = all_emb[:-1]
seed_emb = all_emb[-1:]

# Step 2: Direct similarity (Cell 3.3)
similarities = cosine(seed_emb, vocab_emb)  # ✅ Same context!
```

**Benefit**: All terms share the same embedding context
- Consistent attention patterns
- Shared normalization
- Comparable vectors

## Impact on Results

**Expected improvements in v19:**
1. **Higher similarity scores** for truly related terms (better signal)
2. **Lower similarity scores** for unrelated terms (less noise)
3. **More stable rankings** across multiple runs
4. **Better semantic coherence** in expanded dictionaries

**Validation strategy:**
```python
# Run both versions on same data
v18_expanded = run_v18()
v19_expanded = run_v19()

# Compare:
# 1. Overlap in top-k terms
# 2. Similarity score differences
# 3. Manual quality assessment
# 4. Reproducibility test (run v19 twice)
```
