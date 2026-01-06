# Fixed Confidence Level Cell - Check Column Names First

## Step 1: Check Your Column Names

Run this first to see what columns you have:

```python
# Check what columns exist in train_df
print("Columns in train_df:")
print(train_df.columns.tolist())
print(f"\nDataFrame shape: {train_df.shape}")
print(f"\nFirst few rows:")
print(train_df.head(2))
```

## Step 2: Use This Fixed Code (Auto-detects column names)

```python
# ============================================================
# CELL 7.5a: Add Confidence Levels Based on Cosine Margins
# ============================================================

print("Adding confidence levels based on cosine score margins...")
print()

import numpy as np

# Define confidence thresholds based on margin between top 2 topics
HIGH_CONFIDENCE_THRESHOLD = 0.15  # margin > 0.15 = high confidence
LOW_CONFIDENCE_THRESHOLD = 0.05   # margin < 0.05 = none/ambiguous

def calculate_confidence_level(row, cosine_columns):
    """
    Calculate confidence level based on cosine score margin.
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

# Auto-detect cosine score columns
# Try different patterns
cosine_columns = []

# Pattern 1: Columns ending with '_cosine'
cosine_columns = [col for col in train_df.columns if col.endswith('_cosine')]

# Pattern 2: If not found, try columns that are topic names from CONFIG
if len(cosine_columns) == 0:
    topic_names = CONFIG.get('topics', [])
    cosine_columns = [col for col in train_df.columns if col in topic_names]

# Pattern 3: If still not found, try columns containing topic keywords and 'score'
if len(cosine_columns) == 0:
    cosine_columns = [col for col in train_df.columns
                      if any(keyword in col.lower() for keyword in ['educational', 'governance', 'poverty', 'racism', 'fragmentation'])
                      and any(score_word in col.lower() for score_word in ['score', 'cosine'])]

# Pattern 4: Last resort - look for numeric columns that aren't IDs
if len(cosine_columns) == 0:
    numeric_cols = train_df.select_dtypes(include=[np.number]).columns
    exclude_patterns = ['id', 'index', 'df', 'count']
    cosine_columns = [col for col in numeric_cols
                      if not any(pattern in col.lower() for pattern in exclude_patterns)]

print(f"Found {len(cosine_columns)} score columns:")
for col in cosine_columns:
    print(f"  - {col}")

if len(cosine_columns) == 0:
    print("\n❌ ERROR: Could not find score columns!")
    print("Available columns:", train_df.columns.tolist())
    raise ValueError("No score columns found. Please check column names.")

# Calculate confidence level for each row
print("\nCalculating confidence levels...")
train_df['confidence_level'] = train_df.apply(
    lambda row: calculate_confidence_level(row, cosine_columns),
    axis=1
)

# Show distribution
print("\n" + "="*60)
print("CONFIDENCE LEVEL DISTRIBUTION")
print("="*60)
conf_dist = train_df['confidence_level'].value_counts()
for conf in ['high', 'low', 'none']:
    count = conf_dist.get(conf, 0)
    pct = count / len(train_df) * 100
    print(f"  {conf:10} {count:6} ({pct:5.1f}%)")

print(f"\nTotal training samples: {len(train_df)}")

# Show examples from each confidence level (FIXED - auto-detect text column)
print("\n" + "="*60)
print("EXAMPLES FROM EACH CONFIDENCE LEVEL")
print("="*60)

# Find text column (try different common names)
text_column = None
for possible_name in ['chunk', 'text', 'content', 'document', 'chunk_text', 'full_text']:
    if possible_name in train_df.columns:
        text_column = possible_name
        break

# If still not found, use first string column
if text_column is None:
    string_cols = train_df.select_dtypes(include=['object']).columns
    if len(string_cols) > 0:
        text_column = string_cols[0]

for conf in ['high', 'low', 'none']:
    subset = train_df[train_df['confidence_level'] == conf]
    if len(subset) > 0:
        sample = subset.iloc[0]
        print(f"\n{conf.upper()} CONFIDENCE EXAMPLE:")

        # Show text if available
        if text_column and text_column in sample.index:
            text_preview = str(sample[text_column])[:80]
            print(f"  Text: {text_preview}...")

        # Show scores
        print(f"  Scores:")
        for col in cosine_columns:
            print(f"    {col}: {sample[col]:.3f}")

        # Calculate and show margin
        scores = sample[cosine_columns].values
        sorted_scores = np.sort(scores)[::-1]
        margin = sorted_scores[0] - sorted_scores[1] if len(sorted_scores) > 1 else 0
        print(f"  Margin: {margin:.3f}")

        # Show which topic dominates
        max_idx = scores.argmax()
        print(f"  Dominant topic: {cosine_columns[max_idx]}")

print("\n" + "="*60)
print("✓ Confidence levels added successfully!")
print("="*60)
```

---

## What This Fixed Version Does

1. **Auto-detects score columns** using multiple patterns:
   - Looks for `_cosine` suffix
   - Checks CONFIG topics
   - Searches for topic keywords
   - Falls back to numeric columns

2. **Auto-detects text column** for examples:
   - Tries common names: `chunk`, `text`, `content`, etc.
   - Falls back to first string column

3. **Handles missing columns gracefully**:
   - Won't crash if text column doesn't exist
   - Shows clear error if score columns not found

4. **Better output formatting**:
   - Clear headers and separators
   - Shows dominant topic for each example

---

## If It Still Doesn't Work

Run this diagnostic cell first:

```python
# DIAGNOSTIC: Show all column info
print("="*60)
print("DIAGNOSTIC INFO")
print("="*60)

print("\nAll columns:")
for i, col in enumerate(train_df.columns):
    print(f"  {i}: {col} (dtype: {train_df[col].dtype})")

print("\nNumeric columns:")
numeric = train_df.select_dtypes(include=[np.number]).columns.tolist()
print(numeric)

print("\nString columns:")
string = train_df.select_dtypes(include=['object']).columns.tolist()
print(string)

print("\nSample row:")
print(train_df.iloc[0])

print("\nDataFrame info:")
train_df.info()
```

This will show you exactly what columns you have, and I can help you adjust the code accordingly!
