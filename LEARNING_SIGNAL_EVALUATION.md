# Learning Signal Evaluation for BERTje Training

**Context**: BERTje needs to learn topic patterns from SBERT dot product scores [~1-9] that capture both magnitude and multi-topic combinations.

**Key Dataset Characteristics (v25 slavery corpus)**:
- Total chunks: 1,520
- Score range: 0.9 - 9.2 (per topic)
- Mean scores: Educational=3.93, Governance=4.33, Economic=4.49, Racism=4.82
- CV range: 0.31 - 0.64 (ALL chunks have CV > 0.20, indicating good differentiation)
- Multi-topic chunks: ~50% have score_margin < 0.5 (multiple topics co-occur)

---

## Core Requirements

BERTje must learn:
1. **Multi-topic patterns**: Many chunks relate to 2-3 topics simultaneously
   - Example: [Edu=7.56, Gov=4.75, Econ=4.86, Racism=5.71] → Educational + Racism
   - Example: [Edu=4.32, Gov=5.70, Econ=4.77, Racism=5.52] → All 4 topics co-occur

2. **Relative magnitudes**: The difference between 8.0 and 4.0 is meaningful
   - 8.0 = strong relevance, 4.0 = moderate relevance, 2.0 = weak relevance

3. **Differentiation patterns**: High CV = clear topic, Low CV = mixed/general content
   - CV > 0.20: Clear topic differentiation
   - CV < 0.10: Boilerplate/noise (but v25 has NONE - already filtered)

4. **Topic co-occurrence shapes**: Not just "which topic?" but "what combination?"
   - Educational + Racism (common: educational discrimination)
   - Governance + Economic (common: patronage, corruption affecting economy)
   - All 4 topics (general policy discussion)

---

## Evaluation Framework

For each learning signal option, evaluate:
- **Pattern Preservation**: Does it preserve multi-topic combinations?
- **Magnitude Information**: Does it retain meaningful score differences?
- **Training Stability**: Can the model optimize effectively?
- **Interpretability**: Can we understand what the model learned?
- **Computational Cost**: Training and inference efficiency

---

## Option 1: Raw Dot Product Scores (Current v19 Approach)

### Configuration
```python
# Labels: [score_Edu, score_Gov, score_Econ, score_Racism]
# Example: [7.56, 4.75, 4.86, 5.71]

# Model: 4 independent regression heads
# Loss: MSE on raw scores
loss = MSE(predictions, labels)

# Output: Continuous scores [0-10] per topic
```

### Strengths
✅ **Full magnitude preservation**: 8.0 vs 4.0 distinction maintained
✅ **Natural multi-label**: Each topic scored independently
✅ **Simple architecture**: 4 linear heads, one MSE loss
✅ **Interpretable outputs**: Scores directly comparable to SBERT labels

### Weaknesses
❌ **Scale sensitivity**: Scores in [1-9] range, but model outputs unbounded
❌ **Imbalanced magnitudes**: Racism (mean=4.82) naturally higher than Educational (mean=3.93)
❌ **No differentiation signal**: Model doesn't explicitly learn CV patterns
❌ **Uniform weighting**: All errors weighted equally (is 8→7 error same as 2→1?)

### Metrics to Track
- **Pearson correlation** per chunk (pattern + relative magnitude)
- **MAE** per topic
- **CV correlation**: Does model learn differentiation?
- **Pairwise error**: Does model capture relative topic strengths?

### Verdict
**Good baseline**, but could be improved with normalization or weighted loss.

**Score: 7/10** (solid, but room for improvement)

---

## Option 2: Min-Max Normalized Scores [0, 1]

### Configuration
```python
# Normalize per topic to [0, 1]
min_scores = [0.908, 0.749, 1.280, 0.892]  # Per topic
max_scores = [9.222, 7.618, 8.588, 8.345]  # Per topic

normalized = (score - min_score) / (max_score - min_score)

# Example: [7.56, 4.75, 4.86, 5.71] →
#          [0.80, 0.58, 0.49, 0.58]

# Loss: MSE on [0, 1] normalized
loss = MSE(sigmoid(predictions), normalized_labels)
```

### Strengths
✅ **Balanced training**: All topics in same [0, 1] range
✅ **Stable gradients**: Bounded outputs prevent explosions
✅ **Fair comparison**: Model can't exploit topic magnitude differences
✅ **Magnitude preserved**: Within-topic differences still meaningful

### Weaknesses
❌ **Cross-topic comparison lost**: Can't directly compare Edu=0.8 to Gov=0.6 (different scales)
❌ **Min/max coupling**: Entire dataset needed to normalize (not incremental)
❌ **Boundary effects**: Outliers compressed at 0/1 boundaries
⚠️ **Interpretation**: Needs denormalization to compare to SBERT scores

### Metrics to Track
- **Normalized Pearson** per chunk
- **Denormalized MAE** (convert back to original scale)
- **Range correlation**: Does model match spread?

### Verdict
**Good for balanced training**, but loses cross-topic magnitude comparison.

**Score: 7.5/10** (better training stability, slight interpretation cost)

---

## Option 3: Z-Score Normalization (Standardized)

### Configuration
```python
# Standardize per topic to mean=0, std=1
mean_scores = [3.928, 4.325, 4.492, 4.824]  # Per topic
std_scores = [1.220, 1.040, 1.029, 1.066]   # Per topic

z_score = (score - mean) / std

# Example: [7.56, 4.75, 4.86, 5.71] →
#          [2.98, 0.41, 0.36, 0.83]

# Loss: MSE on standardized scores
loss = MSE(predictions, z_scores)
```

### Strengths
✅ **Statistically principled**: Centers data, equal variance per topic
✅ **Outlier robust**: Extreme values less impactful
✅ **Cross-topic comparable**: Z-scores directly comparable
✅ **Magnitude meaningful**: Z=2.98 means "2.98 std above mean" (very high)

### Weaknesses
❌ **Negative values**: Z-scores can be negative (low scores)
❌ **Unbounded**: Z-scores have no natural upper limit (outliers → Z=4+)
❌ **Interpretation**: Requires reverse transformation
⚠️ **Assumes normality**: Works best if scores are normally distributed

### Metrics to Track
- **Standardized Pearson** per chunk
- **Denormalized MAE**
- **Z-score MAE**: How well model predicts standardized scores

### Verdict
**Good for statistical training**, but negative values and unbounded range complicate things.

**Score: 6.5/10** (statistically sound, but interpretation harder)

---

## Option 4: Softmax-Style Probability Distribution

### Configuration
```python
# Convert scores to probability distribution over topics
# Chunk: [7.56, 4.75, 4.86, 5.71]

# Softmax with temperature T=1.0
exp_scores = exp(scores / T)
probs = exp_scores / sum(exp_scores)

# Result: [0.52, 0.03, 0.04, 0.08] (Educational dominates)

# Loss: KL divergence or cross-entropy
loss = KLDivergence(log_softmax(predictions), probs)
```

### Strengths
✅ **Proper probability**: Sums to 1.0
✅ **Differentiable**: Log-softmax + KL divergence
✅ **Relative emphasis**: Automatically emphasizes differences

### Weaknesses
❌ **MAGNITUDE LOSS**: [8,7,1,1] → same probs as [4,3.5,0.5,0.5]
❌ **Single-topic bias**: Softmax exaggerates winner (destroys multi-label)
❌ **Not multi-label**: Probabilities sum to 1 → can't represent co-occurrence
❌ **Temperature sensitivity**: T=0.5 → sharp, T=2.0 → smooth

### Example Problem
```
Multi-topic chunk: [Edu=5.0, Gov=5.2, Econ=4.8, Racism=5.0]
Softmax: [0.24, 0.27, 0.22, 0.24] → Almost uniform (good!)

But: [Edu=8.0, Gov=7.5, Econ=2.0, Racism=2.0] (Edu+Gov strong)
Softmax: [0.47, 0.35, 0.09, 0.09]
vs [Edu=4.0, Gov=3.5, Econ=1.0, Racism=1.0] (same pattern, weaker)
Softmax: [0.47, 0.35, 0.09, 0.09] → IDENTICAL! Magnitude lost!
```

### Verdict
**AVOID**: Destroys magnitude and multi-label information.

**Score: 2/10** (fundamentally wrong for multi-label regression)

---

## Option 5: Hybrid: Raw Scores + CV Regularization

### Configuration
```python
# Primary loss: MSE on raw scores
primary_loss = MSE(predictions, labels)

# Regularization: CV matching
pred_cv = std(predictions) / mean(predictions)
label_cv = std(labels) / mean(labels)
cv_loss = MSE(pred_cv, label_cv)

# Combined
loss = primary_loss + λ * cv_loss  # λ = 0.1 to 1.0
```

### Strengths
✅ **Magnitude preserved**: Raw scores maintained
✅ **Differentiation learning**: Explicitly trains model to match CV
✅ **Pattern emphasis**: High CV chunks (clear topics) get pattern reward
✅ **Multi-objective**: Balances accuracy and shape learning

### Weaknesses
⚠️ **Hyperparameter**: Need to tune λ weight
⚠️ **Complexity**: Two loss components to balance
❓ **Overfitting risk**: CV regularization might overfit to training CV distribution

### Metrics to Track
- **Primary MAE**: Magnitude accuracy
- **CV correlation**: Pattern learning
- **Hybrid loss**: Track both components separately

### Verdict
**Interesting enhancement** to Option 1, explicitly rewards pattern learning.

**Score: 8/10** (sophisticated, requires tuning)

---

## Option 6: Weighted MSE by Score Magnitude

### Configuration
```python
# Weight errors by importance (higher scores = more important)
weights = labels / labels.sum(axis=1, keepdims=True)

# Example: [7.56, 4.75, 4.86, 5.71] → weights [0.33, 0.21, 0.21, 0.25]
# Errors on Educational (7.56) weighted 0.33
# Errors on Governance (4.75) weighted 0.21

loss = (weights * (predictions - labels)^2).sum()
```

### Strengths
✅ **Magnitude-aware**: Prioritizes getting high scores right
✅ **Natural weighting**: Derived from data, not hyperparameter
✅ **Multi-label compatible**: Each topic weighted independently
✅ **Interpretable**: "Focus on what's important"

### Weaknesses
⚠️ **Low-score neglect**: Weak signals (score=2) get low weight
⚠️ **Uniform chunks**: When all scores similar, weights uniform (no benefit)
❓ **Justification**: Is error at 8→7 really more important than 2→1?

### Alternative Weighting
```python
# Certainty weighting: High CV = high weight (clear signal)
weights = cv_scores  # Use chunk's CV as confidence

# Or differentiation weighting:
weights = (max_score - min_score) / mean_score  # Range-based
```

### Verdict
**Promising**, especially with CV-based weighting for significance.

**Score: 7.5/10** (clever, needs empirical validation)

---

## Option 7: Multi-Task Learning (Regression + Classification)

### Configuration
```python
# Task 1: Regression (primary)
regression_loss = MSE(predictions_continuous, labels)

# Task 2: Classification (auxiliary)
# Bin scores into [Low: 0-3, Medium: 3-6, High: 6-10]
bins = [0, 3, 6, 10]
labels_binned = digitize(labels, bins)  # Shape: [batch, 4] of classes

classification_loss = CrossEntropy(predictions_discrete, labels_binned)

# Combined
loss = regression_loss + α * classification_loss  # α = 0.5
```

### Strengths
✅ **Robust features**: Classification forces discrete pattern learning
✅ **Complementary**: Regression=fine-grained, classification=coarse
✅ **Regularization**: Classification prevents overfitting to noise
✅ **Interpretable**: Can report both continuous and binned predictions

### Weaknesses
⚠️ **Complex architecture**: Two output heads per topic (8 heads total)
⚠️ **Binning arbitrary**: Where to set boundaries? [0-3-6-10] vs [0-2-5-8]?
⚠️ **Training overhead**: 2x parameters, slower convergence
❓ **Benefit unclear**: Does classification actually help regression?

### Verdict
**Overengineered** for this task. Regression alone should suffice.

**Score: 5/10** (interesting idea, probably unnecessary complexity)

---

## Option 8: Quantile Regression (Robust to Outliers)

### Configuration
```python
# Instead of MSE, use quantile loss
# Predicts median (50th percentile) instead of mean

# Quantile loss (τ = 0.5 for median)
def quantile_loss(predictions, labels, tau=0.5):
    errors = labels - predictions
    return max(tau * errors, (tau - 1) * errors).mean()

loss = quantile_loss(predictions, labels, tau=0.5)
```

### Strengths
✅ **Outlier robust**: Less sensitive to extreme scores
✅ **Median prediction**: More stable than mean for skewed distributions
✅ **Uncertainty estimation**: Can predict multiple quantiles (τ=0.25, 0.5, 0.75)

### Weaknesses
❌ **Not standard**: Most frameworks don't support quantile regression easily
❌ **Magnitude bias**: Optimizes for median, not mean (scores shift)
❓ **Unclear benefit**: Are outliers actually a problem in this data?

### Verdict
**Specialized use case**. Only if outliers are known problem.

**Score: 5/10** (niche, probably overkill)

---

## Option 9: Cosine Embedding Loss (Angular Distance)

### Configuration
```python
# Treat score vectors as directions, ignore magnitude
# Loss: 1 - cosine_similarity(predictions, labels)

loss = 1 - (predictions · labels) / (||predictions|| * ||labels||)
```

### Strengths
✅ **Pure pattern**: Focuses on relative proportions, not magnitudes
✅ **Scale invariant**: [8,7,1,1] and [4,3.5,0.5,0.5] treated as same pattern
✅ **Normalized**: Output in [0, 2] range

### Weaknesses
❌ **MAGNITUDE LOSS**: Same problem as softmax - [8,7,1,1] ≈ [2,1.75,0.25,0.25]
❌ **Not desired**: We WANT magnitude! 8.0 means strong relevance
❌ **Undermines multi-label**: Pattern alone insufficient

### Verdict
**AVOID**: Explicitly discards the magnitude information we want to preserve.

**Score: 3/10** (wrong objective for this task)

---

## Option 10: Rank-Based Learning (Ordinal Regression)

### Configuration
```python
# For each chunk, learn the ranking of topics
# Example: [Edu=7.56, Gov=4.75, Econ=4.86, Racism=5.71]
# Ranking: Edu > Racism > Econ > Gov

# Pairwise ranking loss
loss = 0
for i in range(4):
    for j in range(i+1, 4):
        if labels[i] > labels[j]:
            # Predict i > j
            loss += max(0, 1 - (predictions[i] - predictions[j]))

# Margin ranking loss (PyTorch built-in)
loss = MarginRankingLoss(predictions, labels)
```

### Strengths
✅ **Ordinal information**: Learns relative ordering
✅ **Robust to scale**: Invariant to linear transformations
✅ **Multi-label compatible**: Can handle co-occurrence (close rankings)

### Weaknesses
❌ **Magnitude loss**: Only cares about order, not distances
❌ **Close scores**: [5.0, 4.9] vs [5.0, 2.0] treated similarly (both Edu > Gov)
❌ **No absolute scale**: Can't distinguish "all high" from "all low"

### Example Problem
```
Chunk A: [8.0, 7.5, 2.0, 2.0] → Edu > Gov >> Econ ≈ Racism
Chunk B: [4.0, 3.5, 1.0, 1.0] → Same ranking, VERY different meaning!

Ranking loss: Both perfect! But we want model to distinguish them.
```

### Verdict
**Insufficient**: Ranking alone doesn't capture magnitude or multi-label nature.

**Score: 4/10** (too much information lost)

---

## Option 11: Combined Regression + Ranking (Hybrid)

### Configuration
```python
# Primary: Regression on raw scores
regression_loss = MSE(predictions, labels)

# Auxiliary: Pairwise ranking
ranking_loss = 0
for i in range(4):
    for j in range(i+1, 4):
        if labels[i] > labels[j] + margin:  # Only if clear difference
            ranking_loss += max(0, 1 - (predictions[i] - predictions[j]))

# Combined
loss = regression_loss + β * ranking_loss  # β = 0.1 to 0.5
```

### Strengths
✅ **Best of both**: Magnitude from regression, ordinality from ranking
✅ **Robust features**: Ranking enforces structural consistency
✅ **Margin awareness**: Only penalizes clear ranking errors (margin > 0.5)
✅ **Multi-label**: Regression handles co-occurrence, ranking clarifies priorities

### Weaknesses
⚠️ **Hyperparameter**: Need to tune β and margin
⚠️ **Complexity**: Two loss components
⚠️ **Computational cost**: O(n²) pairwise comparisons per chunk

### Verdict
**Sophisticated enhancement** to regression. Worth trying if basic regression insufficient.

**Score: 8.5/10** (comprehensive, but complex)

---

## Recommended Approach: Progressive Evaluation

### Phase 1: Baseline (Options 1-2)
1. **Option 1**: Raw dot product scores (simple MSE)
   - Establish baseline performance
   - Check for magnitude issues

2. **Option 2**: Min-max normalized [0,1]
   - Compare training stability
   - Evaluate if normalization helps

**Decision point**: If Option 1 works well → proceed. If unstable → use Option 2.

---

### Phase 2: Enhancement (Options 5-6)
3. **Option 5**: Raw + CV regularization
   - Add differentiation learning
   - Tune λ weight (try 0.1, 0.5, 1.0)

4. **Option 6**: Weighted MSE by CV or magnitude
   - Test different weighting schemes
   - Compare to unweighted baseline

**Decision point**: If significant improvement → adopt. Otherwise stick with Phase 1.

---

### Phase 3: Advanced (Optional, if needed)
5. **Option 11**: Regression + Ranking
   - Only if clear ranking errors in Phase 2
   - Tune β weight carefully

**Decision point**: Cost-benefit analysis. Is complexity justified?

---

## Evaluation Metrics (Apply to ALL Options)

### Primary Metrics (Pattern Learning)
1. **Pearson Correlation** (per chunk): Pattern + relative magnitude
   - Target: > 0.85 mean correlation
   - Distribution: Check median, min, max

2. **Euclidean Distance**: Combined magnitude + pattern error
   - Target: < 1.0 mean distance (out of ~4-5 range)

3. **CV Correlation**: Does model learn differentiation?
   - Target: > 0.75 correlation

### Secondary Metrics (Accuracy)
4. **MAE per topic**: How accurate are predictions?
   - Educational: Target < 0.8
   - Governance: Target < 0.7
   - Economic: Target < 0.7
   - Racism: Target < 0.7

5. **Pairwise Error**: Relative topic strengths
   - Target: < 0.5 mean error on topic differences

### Diagnostic Metrics
6. **Range Correlation**: Does model match score spread?
7. **STD Correlation**: Does model match variance patterns?
8. **Primary Topic Accuracy**: % chunks where argmax matches
   - Secondary metric (multi-label means argmax incomplete)

---

## Final Recommendations

### 🥇 **Top Choice: Option 5 (Raw + CV Regularization)**
- **Rationale**: Preserves magnitude, explicitly learns patterns, theoretically sound
- **Configuration**: `loss = MSE(pred, labels) + 0.5 * MSE(CV(pred), CV(labels))`
- **Expected benefit**: 5-10% improvement in CV correlation over raw MSE

### 🥈 **Runner-up: Option 2 (Min-Max Normalized)**
- **Rationale**: Simplest enhancement, proven stability benefits
- **Use if**: Option 1 shows training instability or topic bias
- **Configuration**: Normalize per topic to [0,1], use sigmoid output

### 🥉 **Baseline: Option 1 (Raw Scores)**
- **Rationale**: Simplest, most direct, interpretable
- **Start here**: Always establish this baseline first
- **Configuration**: 4 linear heads, MSE loss, clamp outputs [0,10]

### ⚠️ **Avoid**
- **Option 4**: Softmax (destroys multi-label)
- **Option 9**: Cosine loss (discards magnitude)
- **Option 7**: Multi-task (overengineered)

---

## Implementation Checklist

For each option tested:
- [ ] Define loss function clearly
- [ ] Implement custom metrics (Pearson, CV correlation, etc.)
- [ ] Log per-topic MAE separately
- [ ] Visualize predictions vs labels (scatter plots)
- [ ] Check for systematic bias (over/under-prediction per topic)
- [ ] Test on held-out set (not just validation during training)
- [ ] Compare to SBERT baseline (is BERTje better than SBERT re-labeling?)
- [ ] Analyze failure cases (which chunks does model get wrong?)
- [ ] Document hyperparameters (learning rate, batch size, λ weights, etc.)

---

## Expected Outcomes

**Realistic targets** (based on v25 data characteristics):
- **Pearson correlation**: 0.80-0.90 (good pattern learning)
- **MAE per topic**: 0.5-0.8 (within 1 point on 0-9 scale)
- **CV correlation**: 0.70-0.85 (learns differentiation)
- **Pairwise error**: 0.3-0.5 (captures relative strengths)

**Success criteria**:
- BERTje predictions correlate > 0.85 with SBERT labels (Pearson)
- Multi-topic chunks correctly show elevated scores on multiple topics
- Clear-topic chunks correctly show one dominant score
- Model generalizes to unseen documents (held-out test set)

**When to stop**:
- Diminishing returns (< 2% improvement from added complexity)
- Overfitting detected (validation worse than training)
- Good enough for downstream task (classification, retrieval, etc.)

---

## Conclusion

The **learning signal** should preserve **magnitude** (score differences matter) and **multi-label patterns** (topics co-occur). Options 1, 2, and 5 are most promising. Start simple (Option 1), add normalization if needed (Option 2), then enhance with CV regularization (Option 5) if pattern learning is insufficient.

**DO NOT** use softmax, cosine loss, or pure ranking - they discard critical magnitude information.

The goal is for BERTje to internalize the **semantic space** SBERT learned, producing similar score patterns for similar content. Success means BERTje can replace SBERT for labeling new documents while preserving multi-topic, magnitude-aware predictions.
