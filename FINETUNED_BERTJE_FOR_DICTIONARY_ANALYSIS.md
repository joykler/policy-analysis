# Should Finetuned BERTJE Be Used as Encoder for Dictionary Expansion?

## Quick Answer: **YES, but as an ITERATIVE improvement, not a replacement**

---

## The Concept

### Current Dictionary Creation Process:
1. Start with seed dictionary (curated terms)
2. Use **pretrained BERTJE** embeddings
3. Find similar words via cosine similarity
4. Expand dictionary with suggestions
5. Use expanded dictionary for topic scoring

### Proposed Enhancement:
1. Start with seed dictionary
2. Use **pretrained BERTJE** for initial expansion
3. Train BERTJE on labeled data using this dictionary
4. Use **finetuned BERTJE** embeddings for BETTER expansion
5. Re-expand dictionary (iteration 2)
6. Optionally: Train again, expand again (iteration 3+)

---

## Why Finetuned BERTJE Could Be Better

### 1. **Domain-Specific Embeddings**

**Pretrained BERTJE**:
- Trained on general Dutch text (news, Wikipedia, books)
- Understands general Dutch language patterns
- May not capture policy/slavery-specific semantics

**Finetuned BERTJE**:
- Trained on YOUR policy/slavery corpus
- Learned which words co-occur in YOUR specific context
- Embeddings reflect YOUR domain's semantic space

**Example**:
```
Word: "plantage" (plantation)

Pretrained BERTJE nearest neighbors:
- boerderij (farm)
- landgoed (estate)
- tuin (garden)
- bedrijf (business)

Finetuned BERTJE nearest neighbors:
- slavernij (slavery)
- slaafgemaakten (enslaved people)
- suikerriet (sugar cane)
- dwangarbeid (forced labor)
```

The finetuned version understands "plantage" in the context of colonial slavery, not just agriculture.

---

### 2. **Topic-Aligned Semantic Space**

**Current problem**: Pretrained embeddings don't know about your 4 topics

**After finetuning**:
- BERTJE learned to distinguish Educational vs Economic vs Governance vs Social content
- Word embeddings are "pulled" toward their relevant topics
- Similar words cluster by topic, not just general semantics

**Example**:
```
Seed word: "discriminatie" (discrimination)

Pretrained expansion:
- ongelijkheid (inequality) [could be economic OR social]
- uitsluiting (exclusion) [could be economic OR social]
- vooroordeel (prejudice) [social]

Finetuned expansion:
- racisme (racism) [SOCIAL - correct topic]
- institutioneel racisme (institutional racism) [SOCIAL + GOVERNANCE]
- vooroordelen (prejudices) [SOCIAL - correct topic]
- segregatie (segregation) [SOCIAL - correct topic]
```

Finetuned BERTJE knows which sense of "inequality" matters for YOUR topics.

---

### 3. **Multi-Topic Awareness**

**Pretrained**: Treats all contexts equally

**Finetuned**: Understands that some words belong to multiple topics

**Example**:
```
Word: "onderwijs" (education)

Pretrained neighbors:
- school, student, leren (general education terms)

Finetuned neighbors:
- kansenongelijkheid (inequality of opportunity) [EDUC + SOCIAL]
- toegang onderwijs (access to education) [EDUC + ECON]
- onderwijsachterstand (educational disadvantage) [EDUC - primary topic]
```

The finetuned model learned which education terms are relevant to your specific topics.

---

## Evidence from Your Current Results

### From Your Semantic Evaluation:

**Current dictionary (pretrained BERTJE embeddings)**:
- Cosine multi-label correlation: ~70%
- Works reasonably well
- But has some gaps (e.g., cultural/identity SOCIAL content)

**Finetuned BERTJE**:
- Has learned to identify topics with 60-65% accuracy
- **Knows** which words/phrases indicate which topics
- Could suggest better expansion terms

---

## The Iterative Improvement Cycle

### Iteration 0: Bootstrap (Current State)
```
Seed Dictionary (curated)
    ↓
Pretrained BERTJE embeddings
    ↓
Initial expanded dictionary
    ↓
Cosine scoring on corpus
    ↓
Training data with cosine labels
```

### Iteration 1: First Finetuning
```
Training data (cosine labels)
    ↓
Finetune BERTJE (v1)
    ↓
[BERTJE now understands YOUR domain]
    ↓
Use finetuned BERTJE embeddings for NEW dictionary expansion
    ↓
Expanded dictionary v2 (domain-aware)
    ↓
Re-score corpus with new dictionary
    ↓
New training data (better labels)
```

### Iteration 2+: Refinement
```
Training data v2
    ↓
Finetune BERTJE (v2)
    ↓
Embeddings even better
    ↓
Dictionary v3
    ↓
...
```

**Convergence**: After 2-3 iterations, improvements plateau

---

## Practical Implementation

### Step 1: Train BERTJE with Current Dictionary
```python
# Current state: You're about to do this
train_bertje(
    data=cosine_labeled_data,
    dictionary=pretrained_expanded_dict
)
# Output: bertje_v1.model
```

### Step 2: Use Finetuned BERTJE for Dictionary Expansion
```python
# NEW: Extract embeddings from finetuned model
from transformers import AutoModel, AutoTokenizer

model = AutoModel.from_pretrained("path/to/bertje_v1")
tokenizer = AutoTokenizer.from_pretrained("path/to/bertje_v1")

# Get embeddings for vocabulary
def get_word_embedding(word, model, tokenizer):
    """Get contextualized embedding for a word"""
    inputs = tokenizer(word, return_tensors="pt")
    outputs = model(**inputs)
    # Use [CLS] token or mean pooling
    embedding = outputs.last_hidden_state[:, 0, :].detach().numpy()
    return embedding

# Expand dictionary using finetuned embeddings
for seed_word in seed_dictionary:
    seed_emb = get_word_embedding(seed_word, model, tokenizer)

    # Find similar words in vocabulary
    for candidate in vocabulary:
        cand_emb = get_word_embedding(candidate, model, tokenizer)
        similarity = cosine_similarity(seed_emb, cand_emb)

        if similarity > threshold:
            expanded_dict.add(candidate)
```

### Step 3: Generate Dictionary v2
```python
# Now you have an improved dictionary
# Use it to re-score the corpus
dictionary_v2 = expanded_with_finetuned_bertje

# This might find terms that pretrained BERTJE missed
```

### Step 4: Compare Dictionaries
```python
# What's new in v2?
new_terms = set(dictionary_v2) - set(dictionary_v1)

# What got removed?
removed_terms = set(dictionary_v1) - set(dictionary_v2)

# Manual review of changes
```

---

## Expected Improvements

### What Finetuned Dictionary SHOULD Capture Better:

1. **Domain-Specific Synonyms**
   - Pretrained: "slaaf" → "dienaar" (servant) [too general]
   - Finetuned: "slaaf" → "slaafgemaakte" (enslaved person) [correct terminology]

2. **Multi-Word Expressions**
   - Pretrained: "brain drain" → separate words
   - Finetuned: "brain drain" → "talentenvlucht" (Dutch equivalent in context)

3. **Policy Language**
   - Pretrained: might miss bureaucratic terms
   - Finetuned: learns policy-specific vocabulary from your corpus

4. **Topic Boundaries**
   - Better distinction between economic terms and social terms
   - Less cross-contamination between topics

---

## Potential Risks

### 1. **Overfitting to Corpus**
If your corpus is small or biased:
- Finetuned embeddings might be TOO specific
- Might miss general terms that are still relevant
- **Solution**: Blend pretrained and finetuned dictionaries

### 2. **Circular Reasoning**
- Dictionary created from finetuned model
- Model was trained on data labeled by old dictionary
- Risk of reinforcing existing biases
- **Solution**: Keep seed dictionary as anchor, only expand edges

### 3. **Computational Cost**
- Need to extract embeddings for entire vocabulary
- Can be slow for large vocabularies (100k+ words)
- **Solution**: Only re-expand for words near topic boundaries

---

## Recommended Approach

### Conservative Strategy (Recommended):

```python
# 1. Keep core seed dictionary unchanged (curated, high-quality)
seed_core = load_curated_seeds()

# 2. Expand using BOTH pretrained and finetuned
pretrained_expansion = expand_with_pretrained_bertje(seed_core)
finetuned_expansion = expand_with_finetuned_bertje(seed_core)

# 3. Combine with weights
dictionary_v2 = {
    'core': seed_core,  # Weight: 1.0 (unchanged)
    'pretrained': pretrained_expansion,  # Weight: 0.3
    'finetuned': finetuned_expansion,    # Weight: 0.7 (prefer domain-specific)
}

# 4. Filter by co-occurrence in corpus
# Only keep expanded terms that actually appear in your documents
dictionary_v2 = filter_by_corpus_presence(dictionary_v2)

# 5. Manual review of top N new additions
review_top_additions(dictionary_v2, n=50)
```

### Aggressive Strategy (If You Have Time):

Full iterative cycle:
1. Train BERTJE with current dictionary → Model v1
2. Expand dictionary with Model v1 → Dictionary v2
3. Re-score corpus with Dictionary v2 → Labels v2
4. Train BERTJE with Labels v2 → Model v2
5. Expand dictionary with Model v2 → Dictionary v3
6. Compare v1 vs v2 vs v3 performance

Stop when improvements plateau (usually 2-3 iterations).

---

## Evidence This Works (From Literature)

**Domain adaptation via iterative refinement** is a proven technique:

1. **BERT for specialized domains** (medical, legal):
   - Finetuned BERT finds better synonyms than pretrained
   - Especially for technical terms

2. **Semantic lexicon induction**:
   - Task-specific embeddings improve synonym detection
   - Reduces false positives

3. **Your specific case**:
   - Policy language is specialized
   - Colonial/slavery terminology is domain-specific
   - General Dutch embeddings won't capture nuances

**Expected improvement**: 5-15% better dictionary quality (fewer irrelevant terms, more complete coverage)

---

## Practical Next Steps

### Option A: Quick Test (1-2 hours)
```python
# After training BERTJE v1:
# 1. Extract embeddings for 10 seed words
# 2. Find top 20 nearest neighbors using finetuned vs pretrained
# 3. Manually compare quality
# 4. If better → proceed to full expansion
```

### Option B: Full Implementation (1-2 days)
```python
# 1. Create dictionary expansion pipeline with finetuned BERTJE
# 2. Generate dictionary v2
# 3. Compare cosine scores: v1 dictionary vs v2 dictionary
# 4. Evaluate which gives better multi-label correlation
# 5. If v2 is better → use it for next training iteration
```

### Option C: Hybrid Approach (Recommended - 3-4 hours)
```python
# 1. Use finetuned BERTJE to expand ONLY the weakest topic
#    (From your analysis: SOCIAL topic, especially cultural content)
# 2. Add 20-30 high-quality terms to SOCIAL dictionary
# 3. Keep other topics' dictionaries unchanged
# 4. Re-train and evaluate
```

---

## Decision Criteria

### Use Finetuned BERTJE for Dictionary IF:

✓ You have a well-trained model (>70% accuracy)
✓ Your corpus is domain-specific (policy/slavery)
✓ You want to improve specific weak areas (SOCIAL topic)
✓ You have time for 1-2 iterations
✓ Current dictionary has obvious gaps

### Stick with Pretrained IF:

✗ Model accuracy is low (<60%)
✗ Corpus is very diverse/general
✗ Current dictionary already works well
✗ No time for iteration
✗ Risk of overfitting is high (small corpus)

---

## Your Specific Case

### Based on your evaluation results:

**Current state**:
- Cosine (pretrained dictionary): 70% multi-label correlation
- BERTJE (finetuned): 60-65% multi-label correlation
- Gap: SOCIAL topic (cultural/identity content)

**Recommendation**:

✓ **YES, use finetuned BERTJE for targeted dictionary improvement**

**Focus on**:
1. Expand SOCIAL topic dictionary
2. Add cultural/identity terms that pretrained BERTJE missed
3. Use finetuned embeddings to find these domain-specific terms

**Expected result**:
- SOCIAL topic accuracy: 50% → 65-70%
- Overall multi-label correlation: 60-65% → 70-75%
- Better alignment with cosine scores

---

## Implementation Code Sketch

```python
# After training BERTJE with stratified sampling:

from transformers import AutoModel, AutoTokenizer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load your finetuned model
model = AutoModel.from_pretrained(f"workflow_data/{workflow_name}/Model_finetuning")
tokenizer = AutoTokenizer.from_pretrained(f"workflow_data/{workflow_name}/Model_finetuning")

# Load current dictionary
current_dict = pd.read_csv("Curated_dictionary.csv")

# Focus on SOCIAL topic (weakest performance)
social_seeds = current_dict[current_dict['topic'] == 'Social Fragmentation & Racism']['term'].tolist()

# Extract vocabulary from corpus
corpus_vocab = set()
for chunk in corpus['text']:
    tokens = tokenizer.tokenize(chunk)
    corpus_vocab.update(tokens)

# Get embeddings for seeds
def get_embedding(word):
    inputs = tokenizer(word, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].numpy()

seed_embeddings = {seed: get_embedding(seed) for seed in social_seeds}

# Find similar words in corpus vocabulary
candidates = []
for word in corpus_vocab:
    if word in social_seeds:
        continue

    word_emb = get_embedding(word)

    # Check similarity to all seeds
    max_sim = 0
    best_seed = None
    for seed, seed_emb in seed_embeddings.items():
        sim = cosine_similarity(word_emb, seed_emb)[0][0]
        if sim > max_sim:
            max_sim = sim
            best_seed = seed

    if max_sim > 0.7:  # Threshold
        candidates.append({
            'word': word,
            'similarity': max_sim,
            'closest_seed': best_seed
        })

# Sort and review
candidates_df = pd.DataFrame(candidates).sort_values('similarity', ascending=False)

print(f"Found {len(candidates_df)} candidate terms for SOCIAL topic")
print("\nTop 20 candidates:")
print(candidates_df.head(20))

# Manual review and addition to dictionary
# Save as dictionary_v2
```

---

## Bottom Line

**YES, use your finetuned BERTJE for dictionary improvement**, especially to:

1. **Fix the SOCIAL topic gap** (cultural/identity terms)
2. **Add domain-specific policy vocabulary**
3. **Improve multi-topic term detection**

**Start with a targeted approach**:
- Focus on SOCIAL topic (weakest area)
- Add 20-50 high-quality terms
- Evaluate improvement
- If successful, expand to other topics

**Expected gain**: 5-10% improvement in multi-label correlation, especially for SOCIAL topic

This creates a virtuous cycle: better dictionary → better labels → better model → better dictionary → ...
