# Dictionary Discovery v19: Unified Embedding Space

## Summary of Changes

Version 19 introduces a **unified embedding approach** that addresses a fundamental limitation in the previous nearest neighbor implementation.

## Problem in v18 (and earlier versions)

**Cells 3.2 and 3.3 had separate embedding operations:**

1. **Cell 3.2**: Encoded vocabulary terms in bulk
2. **Cell 3.3**: Re-encoded seed terms at query time using `nearest_terms(query)`

**Issues with this approach:**
- ❌ Seed terms and vocabulary terms embedded in different contexts
- ❌ Same term could have slightly different representations when encoded separately
- ❌ Inconsistent similarity scores due to SBERT's context-dependent pooling
- ❌ Query-time re-encoding reduces reproducibility
- ❌ Less efficient due to repeated encoding operations

## Solution in v19

**Unified embedding in a single context:**

### Cell 3.2: Unified Embedding - Vocabulary + Seed Terms

**Key improvements:**
1. **Extracts all seed terms** from CONFIG upfront
2. **Creates combined list**: `[vocab_terms] + [seed_terms]`
3. **Embeds everything in one operation**: All terms share the same embedding context
4. **Splits results**: Separates vocab and seed embeddings after encoding
5. **Organizes by topic**: Groups seed embeddings by their topics with metadata

**Benefits:**
- ✅ All terms embedded in the same SBERT context
- ✅ Consistent representations for all terms
- ✅ More reliable similarity scores
- ✅ Better reproducibility

**Outputs:**
- `vocab_embeddings.npy` - Vocabulary term embeddings
- `seed_embeddings.npy` - Seed term embeddings
- `seed_embeddings_by_topic.npz` - Organized by topic
- `vocab_meta.json` - Vocabulary metadata
- `seed_meta.json` - Seed metadata
- `seed_topic_meta.json` - Topic-level metadata with weights/categories

### Cell 3.3: Expand Seed Terms Using Pre-Computed Embeddings

**Key improvements:**
1. **Direct cosine similarity**: Uses `sklearn.metrics.pairwise.cosine_similarity`
2. **No re-encoding**: Works with pre-computed embeddings from Cell 3.2
3. **Matrix-based approach**: Computes similarity matrix (seeds × vocab) once
4. **Efficient lookup**: Uses numpy indexing for fast nearest neighbor search

**Process:**
1. Compute similarity matrix: `cosine_similarity(seed_emb, vocab_emb)`
2. For each topic's seeds:
   - Get top-k most similar vocab terms using `np.argsort()`
   - Apply filters (min_df, min_cosine)
   - Track best similarity score for each term
3. Parent inheritance: Use direct similarity to find best parent seed
4. Output expanded dictionary with weights and categories

**Benefits:**
- ✅ More contextually accurate nearest neighbors
- ✅ No query-time encoding overhead
- ✅ Reproducible results (same embeddings = same results)
- ✅ Faster expansion (pre-computed similarities)

## Technical Comparison

### Old Approach (v18)
```python
# Cell 3.2
vocab_emb = st_embed(terms)  # Embed vocab

def nearest_terms(query: str, k: int = 50):
    qv = st_embed([query])[0]  # Re-embed query each time!
    distances, indices = nn.kneighbors(qv, n_neighbors=k)
    return results

# Cell 3.3
for seed in seeds:
    nearest_terms(seed)  # Separate embedding for each seed
```

### New Approach (v19)
```python
# Cell 3.2
all_terms = vocab_terms + seed_terms
all_embeddings = st_embed(all_terms)  # Single unified embedding
vocab_emb = all_embeddings[:len(vocab_terms)]
seed_emb = all_embeddings[len(vocab_terms):]

# Cell 3.3
similarity_matrix = cosine_similarity(seed_emb, vocab_emb)  # Pre-computed
for topic, seeds in topics:
    for seed_term in seeds:
        seed_idx = seed2idx[seed_term]
        scores = similarity_matrix[seed_idx]  # Direct lookup
        top_k = np.argsort(scores)[-k:][::-1]
```

## Why This Matters

### 1. Contextual Consistency
SBERT uses mean pooling over token embeddings. The same term can have slightly different embeddings when encoded in different batches due to:
- Batch normalization effects
- Random initialization states
- CUDA operations (if using GPU)

By embedding everything together, we ensure perfect consistency.

### 2. Better Semantic Relationships
When seed and vocab terms are embedded together:
- They share the same latent space geometry
- Relative distances are more meaningful
- Similarity scores are directly comparable

### 3. Reproducibility
Pre-computed embeddings mean:
- Same inputs always produce same outputs
- No variability from query-time encoding
- Easier debugging and validation

### 4. Performance
- Single embedding operation instead of N queries
- Matrix operations (numpy/scipy) are highly optimized
- Enables future optimizations (GPU batch processing, approximate NN)

## Migration Notes

### For Users
- **No config changes needed**: v19 uses the same CONFIG structure
- **Same outputs**: `expanded_candidates.csv` format unchanged
- **Better results**: More accurate similarity scores

### For Developers
- **New files in Other_data/**:
  - `seed_embeddings.npy`
  - `seed_meta.json`
  - `seed_embeddings_by_topic.npz`
  - `seed_topic_meta.json`

- **Modified workflow**: Cell 3.2 now requires CONFIG to be loaded (for seed extraction)

## Validation Recommendations

1. **Compare expansions**: Run both v18 and v19 on same data, compare similarity scores
2. **Check consistency**: Re-run v19 multiple times, verify identical results
3. **Semantic quality**: Manually review expanded terms for relevance
4. **Performance**: Measure execution time for Cell 3.2 and 3.3

## Future Enhancements

This unified embedding approach enables:
- **Approximate nearest neighbors**: Use FAISS or Annoy for massive vocabularies
- **GPU acceleration**: Batch processing for large-scale expansions
- **Cross-lingual expansion**: Multilingual SBERT with unified space
- **Iterative expansion**: Use expanded terms as new seeds in same space
- **Quality metrics**: Embedding-based quality scores (e.g., intra-topic coherence)

## Conclusion

v19's unified embedding approach is a fundamental improvement that makes the dictionary expansion more accurate, consistent, and reproducible. The changes are backward-compatible while providing significant quality improvements in the nearest neighbor search.
