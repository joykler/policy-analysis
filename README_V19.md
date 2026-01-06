# Dictionary Discovery v19: Unified Embedding Space

## Quick Start

This version improves dictionary expansion through unified embedding of vocabulary and seed terms in the same contextual space.

## What's New in v19

**Key Innovation**: Cells 3.2 and 3.3 now use a unified embedding approach for more accurate nearest neighbor search.

### Before (v18):
- Vocabulary terms embedded separately from seed terms
- Seed terms re-encoded at query time
- Inconsistent similarity scores

### After (v19):
- ✅ Vocabulary and seed terms embedded together in single operation
- ✅ Direct cosine similarity using pre-computed embeddings
- ✅ More consistent and reproducible results

## Files in This Release

### Notebooks
- **`A__dictionary_discovery_v19_unified_embedding.ipynb`** - Main workflow with unified embedding

### Documentation
- **`V19_UNIFIED_EMBEDDING_CHANGES.md`** - Detailed technical explanation
- **`V19_COMPARISON_DIAGRAM.md`** - Visual comparison with v18
- **`README_V19.md`** - This file

## Modified Cells

### Cell 3.2: Unified Embedding - Vocabulary + Seed Terms
**What it does:**
1. Extracts all seed terms from CONFIG
2. Combines vocabulary and seed terms into single list
3. Embeds everything in one SBERT operation
4. Splits and organizes embeddings by topic
5. Saves embeddings and metadata

**New outputs:**
- `Other_data/seed_embeddings.npy`
- `Other_data/seed_meta.json`
- `Other_data/seed_embeddings_by_topic.npz`
- `Other_data/seed_topic_meta.json`

### Cell 3.3: Expand Seed Terms Using Pre-Computed Embeddings
**What it does:**
1. Computes similarity matrix between seed and vocab embeddings
2. For each topic, finds top-k most similar vocab terms
3. Assigns parent seeds to discovered terms
4. Inherits weights and categories from parents
5. Outputs expanded dictionary

**Key change:** No query-time re-encoding - uses pre-computed embeddings from Cell 3.2

## Benefits

### 1. Better Accuracy
- Contextually consistent embeddings
- More reliable similarity scores
- Better semantic relationships

### 2. Reproducibility
- Same inputs always produce same outputs
- No variability from query-time encoding
- Easier to debug and validate

### 3. Performance
- Single embedding operation instead of N queries
- Optimized matrix operations
- Faster overall execution

### 4. Scalability
- Enables future use of approximate NN (FAISS, Annoy)
- GPU-friendly batch processing
- Handles larger vocabularies efficiently

## Usage

No changes to CONFIG required! Just run the notebook as usual:

```python
# 1. Set up CONFIG (same as v18)
CONFIG = {
    "workflow": {...},
    "paths": {...},
    "dictionary": {...},
    # ... rest of config
}

# 2. Run CHECKPOINT 0-2 (unchanged)
# - Load documents
# - Create chunks
# - Build vocabulary

# 3. Run CHECKPOINT 3 (improved!)
# - Cell 3.1: Load SBERT model (unchanged)
# - Cell 3.2: Unified embedding (NEW)
# - Cell 3.3: Expansion with pre-computed embeddings (NEW)

# 4. Continue with CHECKPOINT 4+ (unchanged)
```

## Validation

To verify improvements, compare v18 and v19 results:

```python
# Load both versions' outputs
v18_expanded = pd.read_csv("v18_workflow/Dictionary/expanded_candidates.csv")
v19_expanded = pd.read_csv("v19_workflow/Dictionary/expanded_candidates.csv")

# Compare similarity scores
comparison = v18_expanded.merge(
    v19_expanded,
    on=['topic', 'term'],
    suffixes=('_v18', '_v19')
)

# Check differences
print(comparison[['term', 'cosine_v18', 'cosine_v19', 'diff']])

# Test reproducibility (v19 should be identical on re-run)
run_v19_again()
assert v19_expanded.equals(v19_expanded_rerun)  # Should pass!
```

## Technical Details

### Embedding Process

**v18 (separate):**
```
Vocab: [term1, term2, ...] → SBERT → [emb1, emb2, ...]
Seeds: query "seed1" → SBERT → [emb_q]  # Different context!
```

**v19 (unified):**
```
All: [term1, term2, ..., seed1, seed2, ...] → SBERT → [emb1, emb2, ..., emb_s1, emb_s2, ...]
                                                         └─────vocab─────┘  └────seeds────┘
```

### Similarity Computation

**v18 (query-time):**
```python
for seed in seeds:
    query_emb = embed(seed)  # Re-encode each time
    nn.kneighbors(query_emb)
```

**v19 (pre-computed):**
```python
sim_matrix = cosine_similarity(seed_emb, vocab_emb)  # Once
for seed_idx in range(len(seeds)):
    top_k = np.argsort(sim_matrix[seed_idx])[-k:]
```

## Migration from v18

1. **Copy your CONFIG**: No changes needed
2. **Update notebook**: Use v19 instead of v18
3. **Run CHECKPOINT 3**: New cells will create additional files
4. **Compare results**: Validate improvements
5. **Continue workflow**: CHECKPOINT 4+ unchanged

## Troubleshooting

### Issue: "IndexError: index out of bounds" in Cell 4.1
**Cause**: Mismatch between vocabulary list and embeddings array.
**Solution**: Cell 4.1 has been updated to use `vocab_meta.json` instead of `vocabulary.csv`. Re-run Cell 4.1.
**See**: `V19_BUGFIX_NAN_TERMS.md` for details.

### Issue: "KeyError: nan" in Cell 4.1
**Cause**: NaN/invalid terms in vocabulary file.
**Solution**:
- Cell 3.1 now filters NaN terms after loading vocabulary
- Cell 4.1 has defensive filtering
- Re-run from Cell 3.1 to regenerate clean vocabulary
**See**: `V19_BUGFIX_NAN_TERMS.md` for prevention strategies.

### Issue: "KeyError: seed term not in vocab"
**Solution**: Seed terms must be in vocabulary. Check your vocabulary filtering (min_df, min_tf).

### Issue: "Memory error during embedding"
**Solution**: Reduce batch size in `st_embed()` function:
```python
def st_embed(texts: list, batch_size: int = 128):  # Reduced from 256
    return st_model.encode(texts, batch_size=batch_size, ...)
```

### Issue: "Different results than v18"
**Expected**: v19 should produce different (better) similarity scores due to unified context.
**Validation**: Check if v19 results are more semantically coherent.

## Future Enhancements

This unified embedding foundation enables:

1. **Approximate NN**: Use FAISS for massive vocabularies
2. **GPU acceleration**: Batch process large-scale expansions
3. **Cross-lingual**: Multilingual SBERT in unified space
4. **Iterative expansion**: Use expanded terms as new seeds
5. **Quality metrics**: Embedding-based coherence scores

## Questions?

- **Technical details**: See `V19_UNIFIED_EMBEDDING_CHANGES.md`
- **Visual comparison**: See `V19_COMPARISON_DIAGRAM.md`
- **Issues**: Check git issues or contact maintainer

## Citation

If you use this unified embedding approach, please cite:

```bibtex
@software{dictionary_discovery_v19,
  title = {Dictionary Discovery v19: Unified Embedding Space},
  author = {Your Name},
  year = {2024},
  version = {19},
  note = {Improved nearest neighbor search through unified embedding}
}
```
