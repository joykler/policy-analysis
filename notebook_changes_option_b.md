# Changes Needed for Option B: Remove Sigmoid for [0, 2] Range

## Summary
Remove `torch.sigmoid()` from the forward pass to allow BERTje to output in [0, 2] range.

---

## Cell 48 (CELL 7.1): SBERTContinuousMultiLabel Architecture

### CHANGE 1: Remove sigmoid from forward pass

**BEFORE (lines 298-301):**
```python
# Predict continuous scores for each topic
topic_predictions = []
for head in self.topic_heads:
    pred = torch.sigmoid(head(sentence_embedding))  # [batch, 1] -> [0, 1]
    topic_predictions.append(pred)
```

**AFTER:**
```python
# Predict continuous scores for each topic (linear output for [0, 2] range)
topic_predictions = []
for head in self.topic_heads:
    pred = head(sentence_embedding)  # [batch, 1] -> unbounded
    topic_predictions.append(pred)
```

### CHANGE 2: Add clamping in loss computation

**BEFORE (lines 306-309):**
```python
loss = None
if labels is not None:
    loss_fct = nn.MSELoss()
    loss = loss_fct(logits, labels.float())
```

**AFTER:**
```python
loss = None
if labels is not None:
    loss_fct = nn.MSELoss()
    # Clamp predictions to [0, 2] for training stability
    logits_clamped = torch.clamp(logits, 0.0, 2.0)
    loss = loss_fct(logits_clamped, labels.float())
```

### CHANGE 3: Update docstring and print statement

**BEFORE (line 318-322):**
```python
print("V13: SBERTContinuousMultiLabel Defined")
print("  - Mean pooling (SBERT)")
print("  - 4 independent regression heads")
print("  - Continuous output [0, 1] per topic")
print("  - Loss: MSE on cosine scores")
```

**AFTER:**
```python
print("V18: SBERTContinuousMultiLabel Defined")
print("  - Mean pooling (SBERT)")
print("  - 4 independent regression heads")
print("  - Continuous output [0, 2] per topic (no sigmoid)")
print("  - Loss: MSE on rescaled cosine scores [0, 2]")
```

---

## Cell 50 (CELL 7.2): Dataset - NO CHANGES NEEDED

The dataset already uses rescaled scores [0, 2]:
```python
cos_val = float(np.clip(cos_val, 0.0, 2.0))
```

✓ This is correct - keep as is!

---

## Optional: Add Inference Clamping Helper

You might want to add a helper method for inference to ensure outputs stay in range:

```python
def predict_with_clamp(self, input_ids, attention_mask):
    """Inference with clamped outputs."""
    outputs = self.forward(input_ids, attention_mask, labels=None)
    predictions = torch.clamp(outputs.logits, 0.0, 2.0)
    return predictions
```

---

## Expected Behavior After Changes

### Training:
- Loss should converge better (proper scale alignment)
- Model can learn full [0, 2] range
- Better performance on high-relevance chunks

### Predictions:
- Educational Disadvantage: outputs near 0.0-2.0 (full range)
- Governance Distrust: outputs near 0.0-1.6 (matches data distribution)
- Persistent Poverty: outputs near 0.0-1.2 (preserves small differences!)
- Social Fragmentation: outputs near 0.0-1.1

### Interpretation:
- 0.0-0.5: Irrelevant/weak relevance
- 0.5-1.0: Moderate relevance
- 1.0-1.5: High relevance
- 1.5-2.0: Very high relevance

---

## Validation Checklist

After making changes and retraining:

1. ✓ Check training loss decreases smoothly
2. ✓ Verify predictions span appropriate range (0-2)
3. ✓ Check per-topic max predictions match data distribution
4. ✓ Correlation metrics should improve
5. ✓ Inspect predictions: high-cosine chunks should get high predictions
6. ✓ Model should better distinguish subtle differences in low-scoring topics
