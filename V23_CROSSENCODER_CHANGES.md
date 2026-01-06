# Dictionary Discovery v23: Cross-Encoder Implementation

## Overview

Version 23 replaces the bi-encoder scoring approach (v22) with a cross-encoder approach that preserves BERTje's full contextual understanding through cross-attention.

## File Created

- `A__dictionary_discovery_v23_policy_crossencoder.ipynb`

## Key Changes

### Checkpoint 4: Dictionary Loading with Weights

**v22 (Bi-encoder) - Single Cell:**
- Cell 4.1: Loaded curated dictionary with weights, created vocabulary embeddings, built **topic vectors** as weighted averages

**v23 (Cross-encoder) - Two Cells:**

**Cell 4.1 (Cell 32): Load Dictionary & Calculate Hybrid Weights**
- Loads curated dictionary with seed weights
- Calculates hybrid weights (seed weight × SIF weight)
- Builds weighted term lists per topic:
  ```python
  topic2terms_weighted[topic] = [(term1, weight1), (term2, weight2), ...]
  ```
- Shows weight statistics per topic

**Cell 4.2 (Cell 33): Save Weighted Term Lists**
- Saves `topic_terms_weighted.json` (replaces `topic_vectors.npy`)
- Saves metadata with weighting scheme info
- Saves config checkpoint

### Checkpoint 5: Chunk Scoring

**v22 (Bi-encoder) - Two Cells:**
- Cell 5.1: Score chunks via dot product
- Cell 5.2: Significance classification

**v23 (Cross-encoder) - Four Cells:**

**Cell 5.1 (Cell 37): Load Data & Initialize Cross-Encoder**
- Loads chunks DataFrame
- Loads weighted topic terms from Checkpoint 4
- Initializes BERTje cross-encoder model (GroNLP/bert-base-dutch-cased)
- Moves model to GPU if available
- Shows performance estimates

**Cell 5.2 (Cell 38): Score Chunks with Weighted Cross-Encoder**
- Defines scoring functions:
  ```python
  def score_chunk_term_pair(chunk, term):
      # [CLS] chunk [SEP] term [SEP] - CROSS-ATTENTION!
      inputs = tokenizer(chunk, term, ...)
      score = model(**inputs).logits[0][0].item()
      return score

  def score_chunk_against_topic_weighted(chunk, topic, terms_weights):
      # Weighted multi-pass aggregation
      term_scores = [score_chunk_term_pair(chunk, t) for t, w in terms_weights]
      weights = [w for t, w in terms_weights]
      return weighted_avg(term_scores, weights)
  ```
- Scores all chunks across all topics
- Creates `all_scores_df` DataFrame

**Cell 5.3 (Cell 39): Calculate Metrics & Statistics**
- Calculates max_score, primary_topic, margin_score
- Shows score distributions (overall, by topic, margin)
- Counts negative/low scores (vocabulary mismatch indicators)
- Displays cross-encoder vs bi-encoder comparison

**Cell 5.4 (Cell 40): Significance Classification**
- (Unchanged from v22 Cell 5.2)
- Classifies chunks by significance level
- Saves labeled scores to CSV files

## Why This Preserves Context

### Bi-encoder (v22) - Context Lost

```
Chunk embedding:  [racisme] [leidt] [tot] [ongelijkheid]
                      ↕        ↕       ↕        ↕
                  Self-attention within chunk only

Topic vector:     weighted_avg([racisme_emb, discriminatie_emb, ...])
                  Single static vector

Comparison:       dot(chunk_emb, topic_vec)
```

**Problem**: Chunk tokens and topic terms NEVER see each other in the transformer.

### Cross-encoder (v23) - Context Preserved

```
Input to transformer:
[CLS] racisme leidt tot ongelijkheid [SEP] racisme [SEP]
  ↕     ↕      ↕     ↕      ↕           ↕     ↕
  ←─────────────────────────────────────────────→
       FULL CROSS-ATTENTION

- "racisme" in chunk attends to "racisme" in term
- "ongelijkheid" attends to "racisme"
- Model builds joint representation
- [CLS] token encodes entire context
- Classification head: [CLS] -> similarity score
```

**Benefit**: Chunk tokens and term tokens attend to each other through transformer layers.

## How Weighting is Preserved

The cross-encoder uses **weighted multi-pass aggregation**:

1. **Score each term individually** with cross-attention:
   - `score_racisme = cross_encoder("[CLS] chunk [SEP] racisme [SEP]")`
   - `score_discriminatie = cross_encoder("[CLS] chunk [SEP] discriminatie [SEP]")`

2. **Apply weights at aggregation** (just like weighted-average topic vector):
   - High-weight terms (e.g., seed words with weight=3.0) contribute more
   - Low-weight terms (e.g., discovered words with weight=0.5) contribute less

3. **Weighted average**:
   ```python
   final_score = (score_racisme * 3.0 + score_discriminatie * 2.5 + ...) / total_weight
   ```

This mirrors the bi-encoder's weighted-average topic vector, but applies weights to **scores** instead of **embeddings**.

## Expected Benefits

### 1. Proper Vocabulary Mismatch Detection

**v22 Problem**: When using slavery-trained vectors on general policy corpus:
- Score range: 3.8 - 12.0 (NO negatives)
- Even unrelated chunks scored 8.3/12
- High scores caused by topic vector magnitude inflation

**v23 Solution**: Cross-encoder produces normalized scores:
- Expected range: -2 to +5 (includes negatives)
- Unrelated chunks should score < 0 (negative)
- Weakly related chunks: 0 - 0.5
- Related chunks: 0.5 - 2.0
- Highly related chunks: 2.0 - 5.0

### 2. Negative Scores Preserved

v22 dot product scores were always positive (magnitude inflation).

v23 cross-encoder logits can be negative:
- Negative score = true vocabulary mismatch
- Properly identifies when slavery terms don't appear in general policy text

### 3. Better Differentiation

v22 had low CV (0.088) - all topics scored similarly.

v23 should have higher CV - cross-attention distinguishes:
- "racisme" in racism context vs. generic "discriminatie"
- "armoede" about poverty vs. generic "kosten"
- Terms that truly match the chunk's semantic content

## Performance Considerations

### Speed

**v22 (Bi-encoder)**:
- Pre-compute chunk embeddings: N chunks
- Pre-compute topic vectors: 4 topics
- Score: N × 4 dot products
- **Very fast** (minutes for 14,640 chunks)

**v23 (Cross-encoder)**:
- For each chunk-topic pair:
  - Score against each term individually
  - 14,640 chunks × 4 topics × ~50 terms/topic = ~2.9M forward passes
- **Slower** (estimated 8 hours for full corpus)

### Mitigation Strategies (Future)

1. **Hybrid approach**: Use bi-encoder to filter top 100 candidates, then re-rank with cross-encoder
2. **Batch processing**: Score multiple chunk-term pairs in one forward pass
3. **GPU acceleration**: Already implemented (model moves to GPU if available)
4. **Sample first**: Test on subset (1,000 chunks) before running full corpus

## Files Modified

### New Files Created
- `A__dictionary_discovery_v23_policy_crossencoder.ipynb` (main notebook)
- `topic_terms_weighted.json` (output from Checkpoint 4)
- `topic_terms_meta.json` (metadata)

### Files No Longer Created in v23
- `topic_vectors.npy` (replaced by `topic_terms_weighted.json`)
- `vocab_embeddings.npy` (not needed - cross-encoder doesn't use pre-computed embeddings)
- Per-topic suggestion files (skipped in Checkpoint 4)

### Downstream Compatibility

Cell 5.2 (Significance Classification) and later cells should work unchanged:
- Still receive `all_scores_df` with score columns
- Score distributions will differ (negatives, different ranges)
- May need to adjust thresholds for high/low/no confidence

## Testing Recommendations

1. **Run on small sample first** (100 chunks):
   ```python
   chunks_df = chunks_df.head(100)
   ```

2. **Check score distribution**:
   - Do you see negative scores?
   - Is vocabulary mismatch properly detected?
   - Compare to v22 results

3. **Examine specific chunks**:
   - Find chunks that scored 8/12 in v22 but should be unrelated
   - Check if they now score < 0.5 in v23

4. **Full corpus run**:
   - Only after validating on sample
   - Monitor GPU memory usage
   - Expect ~8 hours for 14,640 chunks

## Next Steps

1. Run Checkpoint 4 (Cell 32) to create weighted term lists
2. Run Checkpoint 5 (Cell 36) to score chunks with cross-encoder
3. Compare score distributions to v22
4. Validate that vocabulary mismatch produces negative/low scores
5. Proceed to Checkpoint 5.2 (Significance Classification)

## References

- `cross_encoder_approach.py`: Standalone demonstration of cross-encoder
- `A__TOPIC_FRAMEWORK_CONTEXT.md`: Theoretical framework for 4 topics
- Original discussion: Preserving BERTje's contextual understanding through cross-attention
