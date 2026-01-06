# BERTJE Model Integration Guide

**Question:** What effect should the current BERTJE model have on dictionary creation and chunk classification?

---

## Current Pipeline Overview

### What You Have Now

**Cell 5.1: Dot Product Scoring**
```python
score = np.dot(chunk_embedding, topic_vector)
# Uses: SIF-weighted SBERT embeddings + weighted topic vectors
# Output: Raw similarity scores (unbounded, e.g., -3.5 to 3.5)
```

**Cell 5.2: Significance Filtering**
```python
# Filters chunks by significance_category
# Uses: CV, magnitude, contrast metrics
# Output: high/medium/low significance categories
```

**Cell 7.1-7.3: BERTJE Training**
```python
# Trains BERTJE to predict normalized [0,1] scores
# Input: chunk text
# Output: 4 topic scores (Educational, Governance, Poverty, Social)
# Performance: Pearson=0.82, R²=0.54, MAE=0.10
```

---

## Integration Strategy: Two Complementary Approaches

### Approach A: **BERTJE as Primary Scorer** (Recommended for Production)

Replace Cell 5.1's dot product with BERTJE predictions.

#### Use Case: Production Classification
```python
# NEW Cell 5.1 (BERTJE-based)
def score_chunk_with_bertje(text):
    """Use trained BERTJE model instead of dot product."""
    # Load trained model
    model = load_bertje_model('models/bertje_final/')

    # Get predictions
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
    outputs = model(**inputs)
    normalized_scores = outputs.cpu().numpy()[0]  # [0, 1] range

    # Denormalize to original score range
    raw_scores = denormalize_scores(normalized_scores, topic_normalization_params)

    return raw_scores  # Same format as dot product output
```

**Advantages:**
- ✅ More accurate (Pearson 0.82 vs dot product's implicit correlation)
- ✅ Learned semantic patterns beyond keyword matching
- ✅ Handles complex topic relationships
- ✅ No need to maintain topic vectors/embeddings

**When to use:**
- New corpus with unknown characteristics
- Final production deployment
- When you want best accuracy

---

### Approach B: **Hybrid: BERTJE + Dot Product** (Recommended for Iteration)

Use both methods and combine or compare.

#### Use Case: Dictionary Refinement

```python
# Combine both scores
dotprod_score = np.dot(chunk_embedding, topic_vector)
bertje_score = model.predict(text)

# Disagreement detection
disagreement = abs(dotprod_score - bertje_score) > threshold

if disagreement:
    # BERTJE found something dot product missed (or vice versa)
    # Flag for human review or dictionary expansion
    flag_for_review(chunk, dotprod_score, bertje_score)
```

**Advantages:**
- ✅ Identifies where dot product (keyword-based) fails
- ✅ Discovers new semantic patterns for dictionary
- ✅ Validates dictionary coverage
- ✅ Iterative improvement loop

**When to use:**
- During dictionary development
- Quality assurance
- Corpus exploration

---

## Effect on Dictionary Creation

### Current Dictionary Creation Process

**Cell 4.1: Dictionary Expansion**
```
Seed terms → SBERT embeddings → Find similar terms → Weight by frequency
```

**Problem:** Dictionary is static, based on initial seed terms.

### How BERTJE Should Inform Dictionary

#### 1. **Identify Missing Concepts** (Discovery)

```python
# Find chunks where BERTJE scores high but dot product scores low
high_bertje = bertje_scores > 0.7
low_dotprod = dotprod_scores < 0.3
missing_concepts = chunks[high_bertje & low_dotprod]

# Extract key terms from these chunks
for chunk in missing_concepts:
    keywords = extract_keywords(chunk.text)
    # Add to dictionary candidate list
    dictionary_candidates.extend(keywords)
```

**Effect:** Discover terms/phrases BERTJE learned that aren't in dictionary.

**Example:**
```
Chunk: "Families struggling with intergenerational debt cycles"
Dot product score: 0.2 (no matching keywords)
BERTJE score: 0.9 (learned semantic pattern)

→ Add to dictionary: "intergenerational debt", "debt cycles"
```

---

#### 2. **Validate Dictionary Quality** (Quality Check)

```python
# Compare BERTJE vs dot product on validation set
correlation = pearson(bertje_scores, dotprod_scores)

if correlation < 0.6:
    # Dictionary is missing important concepts
    # BERTJE has learned patterns not captured by dictionary
    refine_dictionary()
```

**Effect:** Quantify how well dictionary captures topic semantics.

**Interpretation:**
- High correlation (>0.8): Dictionary is comprehensive ✓
- Medium correlation (0.6-0.8): Dictionary is good but missing some patterns
- Low correlation (<0.6): Dictionary needs significant expansion

---

#### 3. **Weight Existing Terms** (Optimization)

```python
# For each dictionary term, check if BERTJE finds it predictive
for term in dictionary:
    chunks_with_term = find_chunks_containing(term)

    # Compare BERTJE scores for chunks with/without term
    with_term_score = bertje_scores[chunks_with_term].mean()
    without_term_score = bertje_scores[~chunks_with_term].mean()

    importance = with_term_score - without_term_score

    # Update term weight
    dictionary[term]['weight'] *= (1 + importance)
```

**Effect:** Re-weight dictionary terms based on learned importance.

**Example:**
```
Term: "poverty"
Chunks with "poverty": BERTJE avg = 0.8
Chunks without: BERTJE avg = 0.3
Importance: 0.5 (high!)

→ Increase weight of "poverty" in dictionary
```

---

## Effect on Chunk Classification

### Current Classification (Dot Product)

```python
# Cell 5.1 output
scores = {
    'Educational': 2.1,
    'Governance': 0.8,
    'Poverty': 1.5,
    'Social': 1.2
}
primary_topic = 'Educational'  # max score
```

### With BERTJE Integration

#### Option 1: **Replace Dot Product** (Simplest)

```python
# Use BERTJE as sole classifier
scores = bertje_model.predict(chunk_text)
# Same format, different values
```

**Effect:**
- More accurate topic assignment
- Better handles ambiguous chunks
- Learns context beyond keywords

---

#### Option 2: **Ensemble** (Most Robust)

```python
# Combine both methods
dotprod_scores = dot_product_scoring(chunk)
bertje_scores = bertje_model.predict(chunk)

# Weighted average
final_scores = {
    topic: 0.3 * dotprod_scores[topic] + 0.7 * bertje_scores[topic]
    for topic in topics
}
```

**Effect:**
- Leverages strengths of both approaches
- Dot product: Explicit keyword matching
- BERTJE: Learned semantic patterns
- More robust to outliers

**Weighting strategy:**
- 70% BERTJE / 30% dot product (trust learned model more)
- Or dynamic: Use correlation to set weights

---

#### Option 3: **Confidence-Based Routing** (Most Sophisticated)

```python
# Use BERTJE when confident, fall back to dot product otherwise
bertje_scores = bertje_model.predict(chunk)
confidence = max(bertje_scores) - sorted(bertje_scores)[-2]  # Margin

if confidence > 0.3:
    # High confidence - use BERTJE
    final_scores = bertje_scores
else:
    # Low confidence - use dot product or ensemble
    final_scores = dot_product_scoring(chunk)
```

**Effect:**
- Best of both worlds
- BERTJE for clear cases
- Dot product for edge cases

---

## Recommended Integration Workflow

### Phase 1: Validation (Now)
```
1. Run BOTH dot product (Cell 5.1) and BERTJE on same chunks
2. Calculate correlation between methods
3. Identify disagreements
4. Sample and manually review disagreements
```

**Purpose:** Understand where BERTJE adds value.

### Phase 2: Dictionary Refinement (Next)
```
1. Extract chunks where BERTJE >> dot product
2. Analyze these chunks for missing concepts
3. Add discovered terms to dictionary
4. Re-run dot product with expanded dictionary
5. Measure improvement
```

**Purpose:** Improve dictionary using BERTJE insights.

### Phase 3: Hybrid Deployment (Production)
```
1. Use BERTJE as primary scorer
2. Keep dot product as baseline/fallback
3. Monitor both for drift/disagreement
4. Periodically retrain BERTJE on new data
```

**Purpose:** Production-ready classification.

---

## Concrete Implementation Examples

### Example 1: Improve Dictionary

```python
# Find chunks where BERTJE outperforms dot product
threshold = 0.5

for chunk in corpus:
    dotprod_scores = dot_product_score(chunk)
    bertje_scores = bertje_predict(chunk)

    # BERTJE found strong Poverty signal, dot product didn't
    if bertje_scores['Poverty'] > 0.8 and dotprod_scores['Poverty'] < 0.3:
        # Extract keywords
        keywords = extract_keywords(chunk.text, n=10)

        # Check if keywords already in dictionary
        new_keywords = [k for k in keywords if k not in poverty_dictionary]

        # Add to candidate list
        poverty_expansion_candidates.extend(new_keywords)

# Review and add top candidates to dictionary
top_candidates = rank_by_frequency(poverty_expansion_candidates)
poverty_dictionary.update(top_candidates[:20])
```

### Example 2: Classify New Documents

```python
def classify_document(text, use_bertje=True, ensemble=False):
    """
    Classify document using BERTJE and/or dot product.

    Args:
        text: Document text
        use_bertje: Use BERTJE model (recommended)
        ensemble: Combine BERTJE + dot product

    Returns:
        dict: Topic scores
    """
    if use_bertje and not ensemble:
        # Pure BERTJE classification
        scores = bertje_model.predict(text)
        scores = denormalize_scores(scores, normalization_params)

    elif ensemble:
        # Hybrid approach
        bertje_scores = bertje_model.predict(text)
        bertje_scores = denormalize_scores(bertje_scores, normalization_params)

        dotprod_scores = dot_product_score(text, topic_vectors)

        # 70-30 ensemble
        scores = {
            topic: 0.7 * bertje_scores[topic] + 0.3 * dotprod_scores[topic]
            for topic in topics
        }

    else:
        # Pure dot product (original method)
        scores = dot_product_score(text, topic_vectors)

    return scores
```

### Example 3: Quality Assurance

```python
def qa_check_corpus(corpus, sample_size=100):
    """
    Compare BERTJE vs dot product on sample to check dictionary quality.
    """
    sample = corpus.sample(sample_size)

    bertje_scores = []
    dotprod_scores = []

    for chunk in sample:
        bertje_scores.append(bertje_model.predict(chunk.text))
        dotprod_scores.append(dot_product_score(chunk))

    # Calculate correlation per topic
    for topic in topics:
        bertje_topic = [s[topic] for s in bertje_scores]
        dotprod_topic = [s[topic] for s in dotprod_scores]

        corr = pearson(bertje_topic, dotprod_topic)

        print(f"{topic}: correlation = {corr:.3f}")

        if corr < 0.6:
            print(f"  ⚠ Low correlation - dictionary may be missing {topic} concepts")

            # Find examples where they disagree
            disagreements = find_disagreements(bertje_topic, dotprod_topic, threshold=0.5)
            print(f"  Found {len(disagreements)} disagreements")

            # Review samples
            for idx in disagreements[:5]:
                print(f"\n  Example disagreement:")
                print(f"    Text: {sample.iloc[idx].text[:100]}...")
                print(f"    BERTJE: {bertje_topic[idx]:.3f}")
                print(f"    DotProd: {dotprod_topic[idx]:.3f}")
```

---

## Summary: Recommended Actions

### Immediate (This Week)

1. **Run correlation analysis:**
   - Compare BERTJE vs dot product on test set
   - Identify systematic disagreements
   - Sample and review edge cases

2. **Extract dictionary candidates:**
   - Find chunks where BERTJE >> dot product
   - Extract keywords from these chunks
   - Create expansion candidate list

### Short-term (Next Sprint)

3. **Expand dictionary:**
   - Review and add top candidates
   - Re-run dot product with expanded dictionary
   - Measure improvement in correlation

4. **Implement hybrid scoring:**
   - Deploy ensemble (70% BERTJE, 30% dot product)
   - Use for production classification

### Long-term (Ongoing)

5. **Iterative refinement:**
   - Periodically re-train BERTJE on new data
   - Use BERTJE to discover new dictionary terms
   - Monitor correlation to track dictionary quality

6. **Production deployment:**
   - Replace Cell 5.1 with BERTJE-based scoring
   - Keep dot product as baseline for QA
   - Build monitoring dashboard

---

## Key Insights

### BERTJE Should **NOT** Replace Dictionary Entirely

**Dictionary is still valuable for:**
- Explainability (can see which keywords triggered)
- Bootstrapping new topics
- Quick prototyping
- Domain expert validation

**BERTJE complements dictionary by:**
- Learning implicit patterns
- Handling semantic variations
- Capturing context
- Improving accuracy

### BERTJE's Value: Discovery + Accuracy

**Discovery:** Identifies concepts missing from dictionary
**Accuracy:** More reliable scoring than keyword matching
**Iteration:** Creates feedback loop to improve dictionary

### The Full Loop

```
Dictionary → Dot Product Scores → Train BERTJE → Find Gaps → Expand Dictionary → Repeat
```

This creates a **virtuous cycle** where:
1. Dictionary provides initial guidance
2. BERTJE learns beyond dictionary
3. BERTJE discoveries improve dictionary
4. Improved dictionary helps next BERTJE iteration

---

**Bottom Line:**

Use BERTJE to **enhance** the pipeline, not replace it entirely:
- **Primary scorer:** BERTJE (more accurate)
- **Dictionary role:** Initialization + explainability + discovery
- **Hybrid approach:** Best of both worlds for production