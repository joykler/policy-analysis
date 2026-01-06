# Vocabulary Filtering Quick Reference

## Configuration

```python
"vocab": {
    "min_df": 2,      # Minimum: Keep terms in ≥ 2 chunks
    "max_df": 0.8,    # Maximum: Remove terms in > 80% chunks
    "max_vocab": 100000,
}
```

## Parameter Types

| Type | Example | Meaning |
|------|---------|---------|
| **Integer** | `min_df = 5` | Absolute count: ≥ 5 chunks |
| **Float** | `max_df = 0.8` | Percentage: ≤ 80% of chunks |

## Common Settings

### Default (Balanced)
```python
"min_df": 2,          # Remove rare terms
"max_df": 0.8,        # Remove common stopwords
```

### Conservative
```python
"min_df": 1,          # Keep most terms
"max_df": 0.95,       # Only remove very common
```

### Aggressive
```python
"min_df": 5,          # More strict on rare terms
"max_df": 0.7,        # More strict on common terms
```

## What Gets Removed?

### Too Rare (min_df)
- Typos: "slvaernij"
- Rare names: "Jan-Pieter"
- Low frequency: appears in < 2 chunks

### Too Common (max_df)
- Stopwords: "de", "het", "van"
- Generic: "en", "in", "op"
- Ubiquitous: appears in > 80% of chunks

## Expected Results

### Typical Corpus
- **Total unique terms**: 40,000-50,000
- **Too rare**: 10,000-15,000 (25-30%)
- **Too common**: 200-300 (< 1%)
- **Final vocabulary**: 30,000-40,000

### Good Signs
✓ Common Dutch stopwords removed
✓ Content words retained
✓ Domain-specific terms kept

### Warning Signs
⚠️ Important terms removed → Increase max_df
⚠️ Stopwords still present → Decrease max_df

## Quick Test

After running vocabulary building:
1. Check removed common terms list
2. Should see: "de", "het", "van", "en", "in"
3. Should NOT see: "slavernij", "kolonie", "discriminatie"

## Adjust If Needed

**Too many terms removed?**
```python
"max_df": 0.9,  # More lenient
```

**Still too many stopwords?**
```python
"max_df": 0.7,  # More strict
```

---

See [VOCAB_FILTERING_UPDATE.md](VOCAB_FILTERING_UPDATE.md) for full details.
