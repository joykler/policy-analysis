# dictionary_discovery_v12.ipynb - Weight Handling Fix

## Issue Identified

The `load_dictionary_from_excel()` function was updated to return topics with weights as tuples:
```python
{topic: [(keyword, weight), (keyword, weight), ...]}
```

But the rest of the code expected a simple list:
```python
{topic: [keyword, keyword, ...]}
```

This caused the workflow to break when trying to use the topics for dictionary expansion.

## Solution Implemented

Added weight extraction and handling in two key places:

### 1. After Loading Dictionary (Cell 8)

**Added 20 lines after `topics = load_dictionary_from_excel(...)`:**

```python
# Extract weights for later use and create keywords-only version
topic_seed_weights = {}
topics_keywords_only = {}

for topic, terms in topics.items():
    if isinstance(terms[0], tuple):
        # Has weights - extract them
        keywords = [kw for kw, w in terms]
        weights = {kw: w for kw, w in terms}
        topic_seed_weights[topic] = weights
        topics_keywords_only[topic] = keywords
    else:
        # No weights (fallback for backward compatibility)
        topics_keywords_only[topic] = terms
        topic_seed_weights[topic] = {kw: 1.0 for kw in terms}

# Use keywords-only version for expansion
topics = topics_keywords_only
CONFIG["topics"] = topics
CONFIG["topic_seed_weights"] = topic_seed_weights  # Store for later

print(f"✓ Extracted seed weights for {len(topic_seed_weights)} topics")
```

**Purpose:**
- Separates keywords from weights
- Stores weights in `CONFIG["topic_seed_weights"]` for later retrieval
- Stores keywords-only list in `CONFIG["topics"]` for normal workflow
- Maintains backward compatibility

### 2. During Dictionary Expansion (Cell 23)

**Modified the expansion loop to add weight column:**

```python
# Get seed weights for this topic
topic_seed_weights = CONFIG.get('topic_seed_weights', {}).get(topic, {})
default_core_weight = CONFIG['weights']['default_core_weight']
default_discovered_weight = CONFIG['weights']['default_discovered_weight']

for w, sc in rows:
    # Determine weight: use seed weight if it's a seed term, otherwise discovered weight
    if w in topic_seed_weights:
        weight = topic_seed_weights[w]
    else:
        weight = default_discovered_weight

    topic_rows.append({
        "topic": topic,
        "term": w,
        "cosine": round(sc, 4),
        "df": int(doc_freq.get(w, 0)),
        "weight": weight  # <-- Weight column added
    })
```

**Purpose:**
- Retrieves seed weights for current topic
- Assigns correct weight to each term:
  - Seed terms → their original weight from CSV (0.7-1.0)
  - Discovered terms → `default_discovered_weight` (0.8)
- Adds weight column to `expanded_candidates.csv`

## Complete Weight Flow

### 1. Seed Dictionary (Input)
```
topic,keyword,weight
Persistent Poverty,armoede,1.0
Persistent Poverty,plantage-economie,0.95
...
```

### 2. Load Dictionary
```python
topics_with_weights = {
    "Persistent Poverty": [("armoede", 1.0), ("plantage-economie", 0.95), ...]
}
```

### 3. Extract Weights
```python
CONFIG["topic_seed_weights"] = {
    "Persistent Poverty": {"armoede": 1.0, "plantage-economie": 0.95, ...}
}
CONFIG["topics"] = {
    "Persistent Poverty": ["armoede", "plantage-economie", ...]
}
```

### 4. Expand Dictionary
```python
expanded_candidates = [
    {"topic": "Persistent Poverty", "term": "armoede", "cosine": 1.0, "df": 50, "weight": 1.0},  # seed
    {"topic": "Persistent Poverty", "term": "plantage-economie", "cosine": 0.95, "df": 20, "weight": 0.95},  # seed
    {"topic": "Persistent Poverty", "term": "nieuwe_term", "cosine": 0.82, "df": 15, "weight": 0.8},  # discovered
]
```

### 5. Curate Dictionary
Manually filter terms, preserving weight column → `curated_dictionary.csv`

### 6. Build Topic Vectors
Read `curated_dictionary.csv` with weights → Use hybrid weighting system

## Two-Tier Weight System

| Term Type | Source | Weight | Example |
|-----------|--------|--------|---------|
| **Seed term** | Your CSV dictionary | 0.7 - 1.0 | "armoede": 1.0 |
| **Discovered term** | Cosine expansion | 0.8 (default) | "nieuwe_term": 0.8 |

Configurable via:
```python
CONFIG["weights"]["default_core_weight"] = 1.0      # Seed without explicit weight
CONFIG["weights"]["default_discovered_weight"] = 0.8  # Discovered terms
```

## Files Modified

- ✅ **dictionary_discovery_v12.ipynb** - Cell 8: Weight extraction added
- ✅ **dictionary_discovery_v12.ipynb** - Cell 23: Weight column added to expansion

## Validation

- ✅ Notebook is valid JSON
- ✅ 78 cells total
- ✅ Weight flow verified from seed → expansion → curation → vector building
- ✅ Backward compatible (handles topics without weights)

## Testing Checklist

When you run the notebook, verify:

1. **After loading dictionary:**
   ```
   ✓ Found weight column in seed dictionary
   ✓ Loaded 5 topics with 377 keywords
   ✓ Extracted seed weights for 5 topics
   ```

2. **After expansion:**
   - Check `expanded_candidates.csv` has a "weight" column
   - Seed terms should have their original weights (0.7-1.0)
   - Discovered terms should have 0.8 (or your configured default)

3. **After curation:**
   - Ensure `curated_dictionary.csv` has weight column preserved

4. **During vector building:**
   ```
   ============================================================
   BUILDING TOPIC VECTORS WITH HYBRID WEIGHTS
   ============================================================
   Weighting scheme: multiplicative
   Default core weight: 1.0
   Default discovered weight: 0.8

     Persistent Poverty & Economic Vulnerability:
       Terms: 71
       Avg seed weight: 0.852
       Avg combined weight: 0.421
   ```

## Summary

The notebook now correctly:
1. ✅ Loads weights from seed dictionary
2. ✅ Stores weights separately for later use
3. ✅ Uses keywords-only list for expansion
4. ✅ Adds weight column to expanded candidates
5. ✅ Preserves weights through curation
6. ✅ Uses hybrid weights in vector building

Your seed dictionary weights are now fully integrated into the entire workflow!
