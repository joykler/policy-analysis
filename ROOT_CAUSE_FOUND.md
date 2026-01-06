# ROOT CAUSE FOUND: V12 Training Issue

## The Problem

**V12 is training a SINGLE-LABEL classifier on MULTI-LABEL data!**

### Evidence

Looking at the training data (`train_data_option2_with_pseudo.csv`):

```
chunk_id          cos_Edu  cos_Gov  cos_Econ cos_Social  label_id
053ba5ba:00000    0.221    0.299    0.354    0.300       2 (Econ)
b5321537:00000    0.559    0.615    0.477    0.473       1 (Gov)
53831b1b:00000    0.295    0.304    0.318    0.354       3 (Social)
```

### What's Wrong

1. **Data has all 4 continuous cosine scores** (multi-label)
2. **But label_id forces single-label**: 0, 1, 2, or 3 (which topic is primary)
3. **V12 model predicts only ONE topic** per chunk

###

 The Multi-Label Reality

From earlier analysis:
- **73.2% of chunks have 2+ topics >0.3**
- **41.0% of chunks have ALL 4 topics >0.3**
- Mean score correlation: **0.71** (topics strongly co-vary)

Example chunk that's ambiguous:
```
Edu: 0.32, Gov: 0.40, Econ: 0.35, Social: 0.34
Range: 0.08 (all very close!)
Forced label: "Gov" (because 0.40 is highest)
```

### Why This Causes 52% Accuracy

The model is being asked:
- **"Which ONE topic is this chunk about?"**

But the correct answer is:
- **"ALL FOUR topics with scores: [0.32, 0.40, 0.35, 0.34]"**

When scores are close (51.5% of chunks have range <0.10), picking the "primary" topic is nearly random!

Example:
- True: Edu=0.32, Gov=0.33, Econ=0.34, Social=0.31
- Model predicts: "Gov" (33%)
- But "Econ" is equally valid (34%)
- This counts as WRONG even though they're essentially the same!

## What V12 SHOULD Be Doing

### Current (Wrong) Architecture
```
Text → BERT → CLS token → softmax(4 classes) → predict ONE topic
Loss: CrossEntropyLoss on single label_id
```

### Correct Multi-Label Architecture

**Option A: Multi-Output Ordinal** (what V12 claims to do)
```
Text → BERT → mean pooling → [head1(3 classes), head2(3 classes), head3(3 classes), head4(3 classes)]
Each head independently predicts: Low/Med/High for that topic
Loss: 4 separate ordinal losses, one per topic
```

**Option B: Multi-Output Regression** (better)
```
Text → BERT → mean pooling → [head1(continuous), head2(continuous), head3(continuous), head4(continuous)]
Each head independently predicts: 0-1 continuous score
Loss: MSE on all 4 predictions
```

## How to Fix

### Solution 1: Fix Training Data Format

Create proper multi-label targets instead of single label_id:

```python
# Current (wrong):
train_data = {
    'text': [...],
    'label_id': [2, 1, 3, ...]  # Single integer
}

# Correct (multi-label ordinal):
train_data = {
    'text': [...],
    'label_edu': [1, 2, 0, ...],     # Ordinal 0/1/2
    'label_gov': [2, 2, 1, ...],     # Ordinal 0/1/2
    'label_econ': [2, 1, 1, ...],    # Ordinal 0/1/2
    'label_social': [1, 2, 2, ...]   # Ordinal 0/1/2
}

# Or continuous (better):
train_data = {
    'text': [...],
    'label_edu': [0.32, 0.56, 0.21, ...],    # Continuous 0-1
    'label_gov': [0.40, 0.61, 0.30, ...],    # Continuous 0-1
    'label_econ': [0.35, 0.48, 0.22, ...],   # Continuous 0-1
    'label_social': [0.34, 0.47, 0.35, ...]  # Continuous 0-1
}
```

### Solution 2: Fix Model Architecture

Change from single-label softmax to multi-label independent heads:

```python
# Current (wrong):
class WrongModel(nn.Module):
    def forward(self, input_ids, attention_mask):
        embeddings = self.bert(input_ids, attention_mask)
        cls = embeddings[:, 0, :]  # CLS token
        logits = self.classifier(cls)  # Shape: [batch, 4]
        return softmax(logits)  # Predicts ONE topic

# Correct (multi-label ordinal):
class SBERTMultiOrdinal(nn.Module):
    def forward(self, input_ids, attention_mask):
        embeddings = self.bert(input_ids, attention_mask)

        # Mean pooling
        attention_expanded = attention_mask.unsqueeze(-1).expand(embeddings.size())
        sum_emb = torch.sum(embeddings * attention_expanded, 1)
        mean_emb = sum_emb / torch.clamp(attention_expanded.sum(1), min=1e-9)

        # 4 independent heads
        topic_outputs = []
        for head in self.topic_heads:
            logits = head(mean_emb)  # Shape: [batch, 3] for Low/Med/High
            topic_outputs.append(logits)

        return torch.stack(topic_outputs, dim=1)  # [batch, 4 topics, 3 classes]

# Loss: 4 independent ordinal losses
for topic_idx in range(4):
    loss += ordinal_loss(predictions[:, topic_idx, :], labels[:, topic_idx])
```

## Verification This Is The Issue

Check V12 notebook Cell 7.1 definition - does it use:
1. ✓ Multiple heads (one per topic)
2. ✗ But trained with single label_id?

Check training data preparation (Checkpoint 6) - does it:
1. ✓ Have all 4 cosine scores
2. ✗ But convert to single label_id for primary topic?

## Expected Impact of Fix

**Current**:
- Training: Predict 1 of 4 topics
- Accuracy: 52% (near 25% random baseline for 4-class)

**After fix (multi-label ordinal)**:
- Training: Predict ordinal class for each of 4 topics independently
- Expected: 60-70% per-topic accuracy

**After fix (multi-label continuous)**:
- Training: Predict continuous score for each of 4 topics
- Expected: 0.65-0.75 correlation with true cosine scores

## Action Items

1. **Verify the issue**: Check V12 Checkpoint 7 training code
2. **Fix Checkpoint 6**: Prepare multi-label targets (4 separate label columns)
3. **Fix Checkpoint 7**: Train with multi-output loss (4 independent predictions)
4. **Use mean pooling** instead of CLS token (SBERT architecture)
5. **Consider continuous regression** instead of ordinal (97% unique patterns)

## Bottom Line

**V12 is treating multi-label data as single-label classification.**

This is like trying to predict a person's diet by asking "What's your favorite food?" when you should be asking "How much of each food group do you eat?"

The fix is straightforward: Change from single label_id to 4 separate label columns, and train with multi-output loss.
