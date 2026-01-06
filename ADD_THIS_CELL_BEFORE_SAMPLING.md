# Fix for KeyError: 'confidence_level'

## Problem
Cell 53 tries to access `train_df['confidence_level']`, but this column doesn't exist yet.

## Solution
Add a NEW CELL between Cell 52 (data loading) and Cell 53 (sampling).

---

## Code to Add (Paste this as a new cell BEFORE Cell 53):

```python
# ============================================================
# CELL 7.5a: Add Confidence Levels Based on Cosine Margins
# ============================================================

print("Adding confidence levels based on cosine score margins...")
print()

import numpy as np

# Define confidence thresholds based on margin between top 2 topics
# margin = (highest_cosine - second_highest_cosine)
HIGH_CONFIDENCE_THRESHOLD = 0.15  # margin > 0.15 = high confidence
LOW_CONFIDENCE_THRESHOLD = 0.05   # margin < 0.05 = none/ambiguous

def calculate_confidence_level(row, cosine_columns):
    """
    Calculate confidence level based on cosine score margin.

    - high: Clear winner (margin > 0.15)
    - low: Some differentiation (0.05 < margin <= 0.15)
    - none: Ambiguous/multi-topic (margin <= 0.05)
    """
    # Get cosine scores for all topics
    cosine_scores = row[cosine_columns].values

    # Sort to get top 2 scores
    sorted_scores = np.sort(cosine_scores)[::-1]

    if len(sorted_scores) < 2:
        return 'high'  # Only one topic - automatically high confidence

    # Calculate margin
    margin = sorted_scores[0] - sorted_scores[1]

    # Assign confidence level
    if margin > HIGH_CONFIDENCE_THRESHOLD:
        return 'high'
    elif margin > LOW_CONFIDENCE_THRESHOLD:
        return 'low'
    else:
        return 'none'

# Get cosine score columns (rescaled scores from dictionary)
# These should have names like: 'Educational Disadvantage & Brain Drain_cosine'
cosine_columns = [col for col in train_df.columns if col.endswith('_cosine')]

if len(cosine_columns) == 0:
    # Fallback: look for columns with topic names
    topic_names = CONFIG['topics']
    cosine_columns = [col for col in train_df.columns
                      if any(topic in col for topic in topic_names)
                      and 'cosine' in col.lower()]

print(f"Found {len(cosine_columns)} cosine score columns:")
for col in cosine_columns:
    print(f"  - {col}")

# Calculate confidence level for each row
train_df['confidence_level'] = train_df.apply(
    lambda row: calculate_confidence_level(row, cosine_columns),
    axis=1
)

# Show distribution
print("\nConfidence level distribution:")
conf_dist = train_df['confidence_level'].value_counts()
for conf in ['high', 'low', 'none']:
    count = conf_dist.get(conf, 0)
    pct = count / len(train_df) * 100
    print(f"  {conf:10} {count:6} ({pct:5.1f}%)")

print(f"\nTotal training samples: {len(train_df)}")

# Show examples from each confidence level
print("\nExample samples from each confidence level:")
for conf in ['high', 'low', 'none']:
    subset = train_df[train_df['confidence_level'] == conf]
    if len(subset) > 0:
        sample = subset.iloc[0]
        print(f"\n  {conf.upper()} confidence example:")
        print(f"    Chunk ID: {sample.get('chunk_id', 'N/A')}")
        print(f"    Chunk: {sample['chunk'][:80]}...")
        for col in cosine_columns:
            print(f"    {col}: {sample[col]:.3f}")
        # Calculate and show margin
        scores = sample[cosine_columns].values
        sorted_scores = np.sort(scores)[::-1]
        margin = sorted_scores[0] - sorted_scores[1] if len(sorted_scores) > 1 else 0
        print(f"    Margin: {margin:.3f}")

print("\n✓ Confidence levels added successfully")
```

---

## Alternative: If Column Names Are Different

If your cosine score columns have different names, adjust the column detection:

```python
# Option 1: If columns are named like "topic_name_score"
cosine_columns = [col for col in train_df.columns if col.endswith('_score')]

# Option 2: If columns are just the topic names
cosine_columns = [col for col in train_df.columns if col in CONFIG['topics']]

# Option 3: Manual specification (if you know the exact names)
cosine_columns = [
    'Educational Disadvantage & Brain Drain',
    'Governance Distrust & Corruption',
    'Persistent Poverty & Economic Vulnerability',
    'Social Fragmentation & Racism'
]
```

---

## What This Does

1. **Finds cosine score columns** in your training data
2. **Calculates margin** between top 2 topic scores for each chunk
3. **Assigns confidence level**:
   - `high`: Margin > 0.15 (clear single-topic chunks)
   - `low`: Margin 0.05-0.15 (some differentiation)
   - `none`: Margin < 0.05 (ambiguous/multi-topic)
4. **Adds `confidence_level` column** to `train_df`
5. **Shows distribution** and examples

---

## After Adding This Cell

Run this new cell, then continue to Cell 53 (the sampling cell). The KeyError should be resolved.

---

## Expected Output

```
Adding confidence levels based on cosine score margins...

Found 4 cosine score columns:
  - Educational Disadvantage & Brain Drain_cosine
  - Governance Distrust & Corruption_cosine
  - Persistent Poverty & Economic Vulnerability_cosine
  - Social Fragmentation & Racism_cosine

Confidence level distribution:
  high         1234 ( 16.0%)
  low          3456 ( 44.8%)
  none         3021 ( 39.2%)

Total training samples: 7711

Example samples from each confidence level:

  HIGH confidence example:
    Chunk ID: chunk_123
    Chunk: Het onderwijssysteem op Bonaire kampt met structurele problemen die terugg...
    Educational Disadvantage & Brain Drain_cosine: 0.842
    Governance Distrust & Corruption_cosine: 0.234
    Persistent Poverty & Economic Vulnerability_cosine: 0.156
    Social Fragmentation & Racism_cosine: 0.089
    Margin: 0.608

✓ Confidence levels added successfully
```

---

## Troubleshooting

If you still get an error:

1. **Check column names**: Run `print(train_df.columns.tolist())` to see actual column names
2. **Check data structure**: Run `print(train_df.head())` to see what data looks like
3. **Verify data was loaded**: Run `print(len(train_df))` to confirm train_df exists

Let me know if you need the column names adjusted!
