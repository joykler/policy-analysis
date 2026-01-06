# Checkpoint 4: Seed + Corpus Embedding Merge Updates

## Summary

Checkpoint 4 has been enhanced to properly merge seed embeddings with corpus embeddings, ensuring both are normalized identically and tracking which terms originated from seeds vs corpus for better diagnostics.

## Changes Applied

### 1. Explicit Embedding Normalization

**Before**: Embeddings were loaded but not explicitly normalized before merging.

**After**: Both vocab and seed embeddings are normalized to unit vectors before creating lookups.

```python
# Normalize vocab embeddings before creating lookup
print("Normalizing vocabulary embeddings...")
vocab_emb_normalized = vocab_emb / (np.linalg.norm(vocab_emb, axis=1, keepdims=True) + 1e-12)
vocab2vec = {term: vocab_emb_normalized[term2idx[term]] for term in terms if term in term2idx}

# Normalize seed embeddings identically
print("Normalizing seed embeddings...")
seed_emb_normalized = seed_emb / (np.linalg.norm(seed_emb, axis=1, keepdims=True) + 1e-12)
seed_vectors = {term: seed_emb_normalized[seed_term2idx[term]] for term in seed_terms if term in seed_term2idx}
```

**Why This Matters**:
- Ensures cosine similarity = dot product (faster computation)
- Prevents magnitude differences from affecting similarity scores
- Makes seed and corpus embeddings directly comparable

### 2. Source Tracking

**New Feature**: Track whether each term came from seed dictionary or corpus vocabulary.

```python
# Track source of each term (seed vs corpus)
term_source = {}  # term -> 'corpus' or 'seed'

# Initially mark all vocab terms as corpus
for term in vocab2vec.keys():
    term_source[term] = 'corpus'

# Update source for seed terms (including overlaps)
for term in seed_vectors.keys():
    term_source[term] = 'seed'
```

**Benefits**:
- Can identify which terms are being boosted by seed embeddings
- Helps diagnose if seed terms are actually contributing to topics
- Enables downstream analysis of seed vs corpus term quality

### 3. Enhanced Merge Diagnostics

**New Console Output**:

```
================================================================================
SEED + CORPUS MERGE DIAGNOSTICS
================================================================================
  Corpus-only terms: 12,345
  Overlapping terms: 234 (seed embeddings will be used)
  Seed-only terms: 89
  Example overlaps: slavernij, kolonie, racisme, discriminatie, dwangarbeid

✓ Merged vocab + seed vectors: 12,668 unique terms
  Breakdown: 12,345 corpus-only, 234 seed-override, 89 seed-only
```

**What This Shows**:
- **Corpus-only**: Terms from expanded vocabulary not in seed dictionary
- **Overlapping**: Terms in both (seed embedding overrides corpus embedding)
- **Seed-only**: Curated seed terms not found in corpus vocabulary
- **Example overlaps**: Sample terms where seed embeddings are used

### 4. Topic Vector Source Breakdown

**Enhanced Topic Statistics**:

```python
topic2sources = defaultdict(lambda: {'corpus': 0, 'seed': 0})  # Track term sources per topic

# During topic vector construction
for _, row in topic_df.iterrows():
    t = row['term']
    # ... existing code ...
    source = term_source.get(t, 'corpus')
    topic2sources[topic][source] += 1
```

**New Console Output**:

```
  Educational Disadvantage & Brain Drain:
    Terms: 127 (45 seed, 82 corpus)
    Avg seed weight: 2.150
    Avg combined weight: 1.823

  Governance Distrust & Corruption:
    Terms: 98 (38 seed, 60 corpus)
    Avg seed weight: 2.100
    Avg combined weight: 1.765
```

**Benefits**:
- See how many curated seeds vs discovered corpus terms contribute to each topic
- Identify topics that are seed-heavy vs corpus-heavy
- Validate that seed terms are actually being used

### 5. Source Information in Suggestions

**Enhanced Suggestion CSVs**:

The per-topic suggestion files now include a `source` column:

| topic | term | similarity | source | keep |
|-------|------|------------|--------|------|
| Educational... | onderwijsachterstand | 0.847 | seed | True |
| Educational... | schooluitval | 0.823 | corpus | True |
| Educational... | taalachterstand | 0.811 | seed | True |

**Benefits**:
- Curators can see if high-similarity terms came from seeds or corpus
- Helps validate whether corpus expansion is finding relevant new terms
- Enables filtering by source during manual curation

### 6. Normalization Verification

**New Safety Check**:

```python
# Verify all embeddings are normalized
sample_norms = [np.linalg.norm(vocab2vec[t]) for t in list(vocab2vec.keys())[:10]]
avg_norm = np.mean(sample_norms)
if abs(avg_norm - 1.0) > 0.01:
    print(f"⚠ WARNING: Embeddings may not be properly normalized (avg norm={avg_norm:.4f})")
else:
    print(f"✓ Embedding normalization verified (avg norm={avg_norm:.4f})")
```

Catches normalization issues early before they affect scoring.

### 7. Updated Metadata Persistence

**Enhanced topic_vectors_meta.json**:

```json
{
  "topics": ["Educational Disadvantage & Brain Drain", ...],
  "terms": {
    "Educational Disadvantage & Brain Drain": ["onderwijsachterstand", ...],
    ...
  },
  "term_sources": {
    "Educational Disadvantage & Brain Drain": {
      "seed": 45,
      "corpus": 82
    },
    ...
  }
}
```

The metadata now includes `term_sources` for each topic, preserving the seed/corpus breakdown.

## Expected Console Output

When CP4 runs with seed embeddings available:

```
================================================================================
CHECKPOINT 4 START - LOADING REQUIRED DATA
================================================================================
✓ Loaded term frequencies
✓ Loaded vocab embeddings: (15234, 768)
✓ Loaded vocabulary metadata: 15234 terms
Creating vocab2vec mapping...
Normalizing vocabulary embeddings...
✓ Created normalized vocab2vec: 15234 terms
✓ Loaded seed embeddings: (456, 768)
✓ Loaded seed metadata: 456 terms
Normalizing seed embeddings...
✓ Created normalized seed vector lookup: 456 terms

================================================================================
SEED + CORPUS MERGE DIAGNOSTICS
================================================================================
  Corpus-only terms: 14998
  Overlapping terms: 236 (seed embeddings will be used)
  Seed-only terms: 220
  Example overlaps: slavernij, kolonie, racisme, discriminatie, dwangarbeid

✓ Merged vocab + seed vectors: 15454 unique terms
  Breakdown: 14998 corpus-only, 236 seed-override, 220 seed-only
✓ Embedding normalization verified (avg norm=1.0000)

================================================================================
BUILDING TOPIC VECTORS FROM CURATED DICTIONARY
================================================================================
✓ Loaded curated dictionary: 563 terms, 4 topics
✓ Curated dictionary has seed weights column

================================================================================
BUILDING TOPIC VECTORS WITH HYBRID WEIGHTS
================================================================================
Weighting scheme: multiplicative
Default core weight: 2.0
Default discovered weight: 1.0
SIF parameter a = 0.001

  Educational Disadvantage & Brain Drain:
    Terms: 127 (45 seed, 82 corpus)
    Avg seed weight: 2.150
    Avg combined weight: 1.823

  Governance Distrust & Corruption:
    Terms: 98 (38 seed, 60 corpus)
    Avg seed weight: 2.100
    Avg combined weight: 1.765

  [... other topics ...]

✓ Created 4 topic vectors with hybrid weighting
✓ Saved topic vectors
✓ Saved topic metadata (including source tracking)

================================================================================
GENERATING TOPIC-SPECIFIC SUGGESTIONS
================================================================================
  Generating suggestions for: Educational Disadvantage & Brain Drain
  Generating suggestions for: Governance Distrust & Corruption
  [... other topics ...]
✓ Saved per-topic suggestions to Dictionary_suggestions/

================================================================================
CHECKPOINT 4 COMPLETE
================================================================================
```

## Key Improvements Summary

| Feature | Before | After |
|---------|--------|-------|
| **Normalization** | Implicit | Explicit L2 normalization for both vocab and seed |
| **Source Tracking** | None | `term_source` dict tracks 'seed' vs 'corpus' |
| **Merge Diagnostics** | Basic overlap count | Detailed breakdown: corpus-only, overlap, seed-only |
| **Topic Stats** | Term count only | Term count + seed/corpus breakdown |
| **Suggestion Files** | term, similarity, keep | term, similarity, **source**, keep |
| **Metadata** | topics, terms | topics, terms, **term_sources** |
| **Verification** | None | Normalization check with warning |

## Compatibility

- **Backward Compatible**: Works with or without seed_embeddings.npy files
- **Graceful Degradation**: If seed embeddings missing, prints warning and uses corpus-only mode
- **Preserved Behavior**: Topic vector construction logic unchanged, only enhanced with tracking

## Testing

To test CP4 updates:

1. Ensure Checkpoint 3 has generated both:
   - `vocab_embeddings.npy` / `vocab_meta.json` (corpus terms)
   - `seed_embeddings.npy` / `seed_meta.json` (seed terms)

2. Run Cell 32 (CP4)

3. Check console output for:
   - "Normalizing vocabulary embeddings" message
   - "Normalizing seed embeddings" message
   - Merge diagnostics table
   - Topic stats showing `(X seed, Y corpus)` breakdown
   - Normalization verification passing

4. Inspect output files:
   - `Dictionary_suggestions/*.csv` should have `source` column
   - `topic_vectors_meta.json` should have `term_sources` section

## Next Steps

With CP4 complete:
- ✅ **CP1**: Token-aware chunking ✅
- ✅ **CP4**: Seed+corpus merge with source tracking ✅
- ⏭️ **CP5.1**: Verify bi-encoder scoring (no cross-encoder leakage)
- ⏭️ **CP5.2**: Port v22 corpus-adaptive significance logic
- ⏭️ **CP6**: Update sampling/stratification
- ⏭️ **CP9**: Align visualization cells

---

**Status**: Checkpoint 4 seed+corpus embedding merge updates complete ✅
