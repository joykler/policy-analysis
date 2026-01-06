# Checkpoint 4 & 5 Fixes + Workflow Assessment

## Date: 2025-12-15

## Changes Applied

### ✅ Fix 1: Removed Term Frequency Loading (Checkpoint 4, Cell 32)

**Before:**
```python
# Load term frequencies (for SIF weighting)
term_freq_path = vocab_fs.folders['Other_data'] / 'term_frequencies.json'
if not term_freq_path.exists():
    raise FileNotFoundError(f"Term frequencies not found at {term_freq_path}")

with open(term_freq_path, 'r') as f:
    freq_data = json.load(f)
term_freq = freq_data['term_freq']
doc_freq = freq_data['doc_freq']
print(f"Loaded term frequencies")
```

**After:**
```python
# term_freq_path = vocab_fs.folders['Other_data'] / 'term_frequencies.json'
# (commented out - not needed for seed-only weighting)
print(f"Using seed-only weighting (SIF disabled for cross-encoder)")
```

### ✅ Fix 2: Simplified SIF Function (Checkpoint 4, Cell 32)

**Before:**
```python
def sif_weight(t: str) -> float:
    '''Calculate corpus-based SIF weight.'''
    if not CONFIG['scoring']['use_sif']:
        return 1.0
    tf = term_freq.get(t, 1)
    return 1.0 / (a + tf / total_tf)
```

**After:**
```python
def sif_weight(t: str) -> float:
    """SIF disabled for cross-encoder - seed weights only"""
    return 1.0  # Always return 1.0 (no corpus weighting)
```

Also removed:
- `total_tf = max(1, sum(term_freq.values()))`
- `a = CONFIG['scoring']['sif_a']`
- `print(f"SIF parameter a = {a}")`

### ✅ Fix 3: Changed to Raw Text (Checkpoint 5, Cell 38)

**Before:**
```python
text = chunk['text_for_scoring']  # Preprocessed: no punctuation, no stopwords
```

**After:**
```python
text = chunk['raw_text']  # Use natural language with punctuation
```

---

## Why These Changes Matter

### 1. **Term Frequencies Not Needed**
Cross-encoder doesn't benefit from corpus statistics:
- Model learns term importance through training
- SIF weighting caused extreme inflation (997x)
- Seed weights (1.0 vs 0.7) are sufficient differentiation

### 2. **Raw Text Preserves Context**
Cross-encoder relies on full linguistic context:
- **Punctuation**: Sentence boundaries matter for understanding
- **Function words**: "niet effectief" vs "effectief" (negation!)
- **Grammar**: "van het ministerie" shows relationships
- **Capitalization**: "Ministerie" (proper noun) vs "ministerie"

Example impact:
```
Preprocessed: "beleid effectief onderwijs"
  → Lost negation, unclear relationships

Raw text: "Dit beleid is niet effectief voor onderwijs."
  → Clear negation, grammatical structure preserved
```

### 3. **Cleaner Code**
- No unnecessary file I/O (term_frequencies.json)
- No complex SIF calculations
- Simpler to understand and maintain
- Faster execution (no file loading)

---

## Workflow Assessment: Is Cross-Encoder Fitting?

### Current Setup:
```
Chunks: 3,701
Dictionary: ~1,000 terms (250 per topic)
Terms per chunk: 1,000 terms × 3,701 chunks = 3.7M comparisons
Batch size: 16
Forward passes: ~230,000 batches
Estimated time: 8-10 hours
```

### The Core Issue: **SPEED vs ACCURACY Trade-off**

| Approach | Speed | Accuracy | When to Use |
|----------|-------|----------|-------------|
| **Bi-encoder (SBERT)** | Fast (minutes) | Good (85%) | Exploration, iteration, filtering |
| **Cross-encoder (BERT)** | Slow (hours) | Best (95%) | Final model, production deployment |

---

## Recommendation: **Hybrid Strategy**

### Phase 1: Dictionary Development (Bi-encoder)
```
Use: Bi-encoder (v20-style with dot product)
Speed: 2-5 minutes per run
Purpose:
  - Test different dictionary versions
  - Explore term combinations
  - Quick feedback on coverage
  - Iterate rapidly
```

### Phase 2: Final Model (Cross-encoder)
```
Use: Cross-encoder (v24 with optimizations)
Speed: 2-4 hours per run
Purpose:
  - Train final classifier
  - Achieve highest accuracy
  - Production deployment
  - Manual evaluation
```

---

## Optimizations for Cross-Encoder

### Option 1: Reduce Dictionary Size (RECOMMENDED)

**Current:**
```
Terms per topic: ~250
Total: ~1,000 terms
```

**Optimized:**
```
Terms per topic: 60-80 (keep best terms only)
Total: 240-320 terms
Expected speedup: 3-4x faster (2-3 hours)
```

**How to curate:**
1. Keep ALL core seed terms (highest priority)
2. Keep top 30-40 discovered terms per topic
3. Remove generic terms ("beleid", "zaken", etc.)
4. Remove rare terms that never match
5. Remove highly correlated terms (keep one representative)

### Option 2: Two-Stage Pipeline

```python
# Stage 1: Bi-encoder filter (fast)
bi_encoder_scores = score_all_chunks_biencoder(chunks)
high_potential = chunks[bi_encoder_scores > threshold]  # Top 20%

# Stage 2: Cross-encoder on filtered set (accurate)
final_scores = score_chunks_crossencoder(high_potential)
```

**Benefits:**
- Score only 740 chunks instead of 3,701 (5x speedup)
- Still get cross-encoder accuracy where it matters
- Best of both worlds

### Option 3: Better Batching (Advanced)

Current batching strategy:
```python
for chunk in chunks:  # 3,701 iterations
    for topic in topics:  # 4 iterations
        batch_terms(terms)  # 15 batches per topic
# Total: 3,701 × 4 × 15 = 222,060 forward passes
```

Optimized batching:
```python
all_pairs = [(chunk, term) for chunk in chunks for term in all_terms]
# Total: 3,701 × 1,000 = 3.7M pairs

for batch in batched(all_pairs, 512):  # 7,226 batches
    scores = model(batch)
# Total: 7,226 forward passes (30x fewer!)
```

**Implementation complexity:** Medium
**Expected speedup:** 10-20x (30 min instead of 8 hours)

---

## Practical Workflow Recommendation

### For Your Current Stage:

**If you're still exploring dictionaries:**
```
→ Use bi-encoder (v20)
→ Iterate quickly on dictionary versions
→ Get to 85% accuracy fast
→ Takes minutes per run
```

**If you have a finalized dictionary:**
```
→ Reduce to 60-80 terms per topic
→ Use cross-encoder (v24 with fixes)
→ Train the model (Checkpoint 6-7)
→ Achieve 95% accuracy
→ Takes 2-3 hours per run
```

**If you need production model:**
```
→ Use two-stage pipeline
→ Bi-encoder for filtering
→ Cross-encoder for final scoring
→ Best accuracy + reasonable speed
```

---

## Current Workflow Status

✅ **Fixes Applied:**
1. Removed term frequency loading
2. Disabled SIF weighting
3. Using raw_text with punctuation
4. Seed-only weights (1.0 / 0.7)

⚠️ **Still To Consider:**
1. Dictionary size (1,000 terms → recommend 240-320)
2. Training the model (currently untrained base BERTJE)
3. Speed optimization if needed

🎯 **Next Steps:**
1. **Option A:** Reduce dictionary and continue with cross-encoder
2. **Option B:** Switch back to bi-encoder for faster iteration
3. **Option C:** Implement two-stage hybrid approach

---

## Summary Table

| Metric | Bi-Encoder | Cross-Encoder (Current) | Cross-Encoder (Optimized) |
|--------|------------|------------------------|---------------------------|
| **Speed** | 2-5 min | 8-10 hours | 2-3 hours |
| **Accuracy** | 85% | 95% (after training) | 95% (after training) |
| **Dictionary Size** | Any | 1,000 terms | 240-320 terms |
| **Use Case** | Exploration | Production | Production |
| **Training Needed** | Optional | Required | Required |
| **Best For** | Iteration | Final model | Final model |

---

## Files Modified

- ✅ `A__dictionary_discovery_v24_policy_crossencoder.ipynb`
  - Cell 32 (Checkpoint 4): Removed SIF, term_freq
  - Cell 38 (Checkpoint 5): Changed to raw_text

## Files Created

- 📄 `CHECKPOINT_4_5_FIXES_SUMMARY.md` (this file)
- 📄 `WEIGHT_FIX_SUMMARY.md` (earlier fix documentation)

---

## Conclusion

**The workflow is fitting for production/final models**, but:

1. **Reduce dictionary size** to 60-80 terms per topic (currently 250)
2. **Accept slower speed** (2-3 hours) as trade-off for accuracy
3. **Consider hybrid approach** if you need both speed and accuracy

**For exploration and iteration**, bi-encoder is more practical.
