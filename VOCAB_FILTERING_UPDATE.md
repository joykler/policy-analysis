# Vocabulary Filtering Update

## New Feature: Filter Out Common Terms ✓

The vocabulary builder now removes **overly common terms** (likely stopwords or generic terms) in addition to rare terms.

## Configuration (Cell 2)

```python
"vocab": {
    "min_df": 2,           # Minimum document frequency
    "max_df": 0.8,         # Maximum document frequency (NEW!)
    "max_vocab": 100000,   # Maximum vocabulary size
}
```

## How It Works

### 1. **min_df** - Remove Rare Terms
- **Purpose**: Filter out typos, rare words, and low-quality terms
- **Default**: `2` (absolute count)
- **Examples**:
  - `min_df = 2`: Keep terms appearing in ≥ 2 chunks
  - `min_df = 0.001`: Keep terms appearing in ≥ 0.1% of chunks

### 2. **max_df** - Remove Common Terms (NEW!)
- **Purpose**: Filter out stopwords and overly generic terms
- **Default**: `0.8` (80% of chunks)
- **Examples**:
  - `max_df = 0.8`: Remove terms appearing in > 80% of chunks
  - `max_df = 1000`: Remove terms appearing in > 1000 chunks

### 3. **max_vocab** - Limit Size
- **Purpose**: Keep only the most frequent terms
- **Default**: `100000`
- **Applied after**: min_df and max_df filtering

## Flexible Input

Both `min_df` and `max_df` accept two formats:

### Integer (Absolute Count)
```python
"min_df": 5,      # At least 5 chunks
"max_df": 1000,   # At most 1000 chunks
```

### Float (Percentage)
```python
"min_df": 0.001,  # At least 0.1% of chunks
"max_df": 0.8,    # At most 80% of chunks
```

The system automatically detects which format you're using.

## Example Output

When you run the vocabulary building cell, you'll now see:

```
🔍 Filtering vocabulary...
  Min document frequency: 2 chunks (0.2% of corpus)
  Max document frequency: 800 chunks (80.0% of corpus)
  Max vocabulary size: 100,000

📊 Vocabulary filtering results:
  Original unique terms: 45,231
  Removed 12,450 terms (too rare: < 2 chunks)
  Removed 234 terms (too common: > 800 chunks)
  After frequency filters: 32,547
  Final vocabulary: 32,547 terms

📈 Most common terms (after filtering):
  - 'slavernij': 3,245 occurrences (in 543 chunks, 54.3%)
  - 'kolonie': 2,891 occurrences (in 489 chunks, 48.9%)
  - 'discriminatie': 2,456 occurrences (in 412 chunks, 41.2%)
  ...

⚠️  Examples of removed overly common terms:
  - 'de': appeared in 987 chunks (98.7%)
  - 'het': appeared in 983 chunks (98.3%)
  - 'van': appeared in 976 chunks (97.6%)
  - 'en': appeared in 971 chunks (97.1%)
  - 'in': appeared in 965 chunks (96.5%)
```

## Why This Helps

### Before (No max_df)
- Vocabulary included: "de", "het", "van", "en", "in", etc.
- These appear in almost every chunk
- Not useful for distinguishing topics
- Add noise to embeddings

### After (With max_df = 0.8)
- Common stopwords automatically removed
- Vocabulary focuses on **content words**
- Better topic discrimination
- Cleaner embeddings

## Recommended Settings

### Conservative (Keep More Terms)
```python
"vocab": {
    "min_df": 2,
    "max_df": 0.95,      # Only remove if in > 95% of chunks
    "max_vocab": 100000,
}
```

### Balanced (Default)
```python
"vocab": {
    "min_df": 2,
    "max_df": 0.8,       # Remove if in > 80% of chunks
    "max_vocab": 100000,
}
```

### Aggressive (Stricter Filtering)
```python
"vocab": {
    "min_df": 5,         # Must appear in at least 5 chunks
    "max_df": 0.7,       # Remove if in > 70% of chunks
    "max_vocab": 50000,  # Smaller vocabulary
}
```

### For Small Corpora
```python
"vocab": {
    "min_df": 0.001,     # 0.1% of corpus
    "max_df": 0.9,       # More lenient for small datasets
    "max_vocab": 100000,
}
```

## Comparison: Old vs New

### Old Behavior
```python
"vocab": {
    "min_df": 2,
    "max_vocab": 100000,
}
```
- Only removed rare terms
- Common words like "de", "het" remained
- Required manual stopword list

### New Behavior
```python
"vocab": {
    "min_df": 2,
    "max_df": 0.8,       # NEW!
    "max_vocab": 100000,
}
```
- Removes rare AND common terms
- Automatic stopword filtering
- No manual stopword list needed
- More focused vocabulary

## Cell Updates

### Cell 2 (Config)
Added `max_df` parameter to vocabulary settings

### Cell 17 (Vocabulary Building)
- Calculates max_df threshold (supports int or float)
- Filters out terms above threshold
- Shows statistics for filtered common terms
- Reports both absolute counts and percentages

## Verification

After running Cell 17, check the output for:
1. ✓ "Max document frequency" line appears
2. ✓ "Removed X terms (too common)" is > 0
3. ✓ Examples of removed common terms shown
4. ✓ Terms like "de", "het", "van" appear in removed list

## Adjusting max_df

If you see important terms being removed:
- **Increase max_df**: `0.8` → `0.9` or `0.95`
- More lenient filtering

If you still see too many generic terms:
- **Decrease max_df**: `0.8` → `0.7` or `0.6`
- Stricter filtering

## Impact on Pipeline

This filtering happens **before**:
- Dictionary expansion
- Topic vector creation
- Model training

So it affects the entire downstream pipeline by:
- Reducing noise in embeddings
- Focusing on content-rich terms
- Improving topic discrimination
- Reducing computation time

## Summary

✅ **Added**: `max_df` parameter to remove common terms
✅ **Flexible**: Accepts int (count) or float (percentage)
✅ **Automatic**: No manual stopword list needed
✅ **Informative**: Shows what was filtered and why
✅ **Default**: `max_df = 0.8` (removes terms in > 80% of chunks)

Your vocabulary builder is now more intelligent and focused! 🎯
