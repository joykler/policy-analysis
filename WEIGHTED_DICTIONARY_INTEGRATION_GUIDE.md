# Weighted Dictionary Integration Guide

## Overview

This guide shows how to integrate seed dictionary weights into the vector building process. Your CSV dictionary already has weights - we just need to enable the code to use them!

## Current System (Without Weights)

Currently, the system:
1. Loads seed dictionary from Excel (only `topic` and `keyword` columns)
2. Expands with similar terms
3. You manually curate
4. During vector building: **Only uses SIF weights** (corpus frequency-based)
5. Seed dictionary weights are **completely ignored**

## New System (With Weights)

The new system will:
1. Load seed dictionary WITH weights from CSV/Excel
2. Expand with similar terms
3. During curation: **Preserve seed weights**, assign default to discovered terms
4. During vector building: **Combine seed weights with SIF weights**

---

## Step 1: Add Weights Configuration to CONFIG

Add this section to your CONFIG dict (after the "scoring" section):

```python
CONFIG = {
    # ... existing config ...

    "scoring": {
        "use_sif": True,
        "sif_a": 1e-3,
        # ... existing scoring config ...
    },

    # NEW: Weight configuration
    "weights": {
        "default_core_weight": 1.0,        # Default for seed dictionary terms without explicit weight
        "default_discovered_weight": 0.8,  # Default for terms discovered during expansion
        "weighting_scheme": "multiplicative",  # Options: "multiplicative", "additive", "seed_dominant", "geometric"
        "additive_seed_ratio": 0.7,        # If using "additive"/"seed_dominant": ratio for seed weight
    },

    # ... rest of config ...
}
```

### Weighting Scheme Options

| Scheme | Formula | Use When |
|--------|---------|----------|
| **multiplicative** (recommended) | `seed × sif` | Default - balances importance and rarity |
| **additive** | `(ratio × seed) + ((1-ratio) × sif)` | Want equal blending |
| **seed_dominant** | `(0.7 × seed) + (0.3 × sif)` | Trust your weights more than corpus |
| **geometric** | `sqrt(seed × sif)` | Want balanced, less extreme |

---

## Step 2: Modify Code - Load Dictionary Function

Find the `load_dictionary_from_excel` function (around line 786) and replace it with:

```python
def load_dictionary_from_excel(excel_path, config):
    """Load topics, keywords, and optional weights from Excel or CSV."""
    if not Path(excel_path).exists():
        print(f"⚠ Dictionary file not found: {excel_path}")
        return config["dictionary"]["default_topics"]

    try:
        # Support both Excel and CSV
        if str(excel_path).endswith('.csv'):
            df = pd.read_csv(excel_path)
        else:
            df = pd.read_excel(excel_path, sheet_name=config["dictionary"]["sheet_name"])

        topic_col = config["dictionary"]["topic_column"]
        keyword_col = config["dictionary"]["keyword_column"]

        # Check for weight column
        has_weights = "weight" in df.columns
        default_core_weight = config["weights"]["default_core_weight"]

        if has_weights:
            print(f"✓ Found weight column in seed dictionary")
            # Return dict with weights
            topics_dict = {}
            for topic in df[topic_col].unique():
                topic_df = df[df[topic_col] == topic]
                # Store as list of (keyword, weight) tuples
                # Use explicit weight if present, otherwise use default_core_weight
                topics_dict[topic] = [
                    (row[keyword_col], row.get("weight", default_core_weight))
                    for _, row in topic_df.iterrows()
                ]
        else:
            print(f"⚠ No weight column found - using default_core_weight ({default_core_weight})")
            # Return dict with default weights
            topics_dict = {}
            for topic in df[topic_col].unique():
                keywords = df[df[topic_col] == topic][keyword_col].tolist()
                topics_dict[topic] = [(kw, default_core_weight) for kw in keywords]

        print(f"✓ Loaded {len(topics_dict)} topics with {sum(len(v) for v in topics_dict.values())} keywords")
        return topics_dict

    except Exception as e:
        print(f"❌ Failed to load dictionary: {e}")
        return config["dictionary"]["default_topics"]
```

---

## Step 3: Modify Code - Vector Building

Find the "Build topic vectors" section (around line 2320) and replace with:

```python
# Load curated dictionary (may have weights from seed)
curated_path = dict_fs.folders['Dictionary'] / 'curated_dictionary.csv'

if not curated_path.exists():
    print(f"❌ Curated dictionary not found: {curated_path}")
    print(f"   Please complete manual curation first!")
else:
    pruned = pd.read_csv(curated_path)
    print(f"✓ Loaded curated dictionary: {len(pruned)} terms, {pruned['topic'].nunique()} topics")

    # Get default weights from config
    default_core_weight = CONFIG['weights']['default_core_weight']
    default_discovered_weight = CONFIG['weights']['default_discovered_weight']
    weighting_scheme = CONFIG['weights']['weighting_scheme']

    # Check if curated dictionary has seed weights
    has_seed_weights = 'weight' in pruned.columns
    if has_seed_weights:
        print(f"✓ Curated dictionary has seed weights column")
    else:
        print(f"⚠ No seed weights in curated dictionary - adding default ({default_core_weight})")
        pruned['weight'] = default_core_weight

    # Calculate SIF weights from corpus
    total_tf = max(1, sum(term_freq.values()))
    a = CONFIG['scoring']['sif_a']

    def sif_weight(t: str) -> float:
        """Calculate corpus-based SIF weight."""
        if not CONFIG['scoring']['use_sif']:
            return 1.0
        tf = term_freq.get(t, 1)
        return 1.0 / (a + tf / total_tf)

    def hybrid_weight(term: str, seed_weight: float) -> float:
        """Combine seed dictionary weight with corpus-based SIF weight."""
        sif_w = sif_weight(term)

        if weighting_scheme == "multiplicative":
            combined = seed_weight * sif_w
        elif weighting_scheme == "additive":
            seed_ratio = CONFIG['weights']['additive_seed_ratio']
            combined = (seed_ratio * seed_weight) + ((1.0 - seed_ratio) * sif_w)
        elif weighting_scheme == "seed_dominant":
            seed_ratio = CONFIG['weights']['additive_seed_ratio']
            combined = (seed_ratio * seed_weight) + ((1.0 - seed_ratio) * sif_w)
        elif weighting_scheme == "geometric":
            combined = np.sqrt(seed_weight * sif_w)
        else:
            combined = seed_weight * sif_w

        return combined

    # Build topic vectors with hybrid weights
    topic2vec = {}
    topic2terms = defaultdict(list)

    print(f"\n{'='*60}")
    print("BUILDING TOPIC VECTORS WITH HYBRID WEIGHTS")
    print(f"{'='*60}")
    print(f"Weighting scheme: {weighting_scheme}")
    print(f"Default core weight: {default_core_weight}")
    print(f"Default discovered weight: {default_discovered_weight}")
    print(f"SIF parameter a = {a}")
    if weighting_scheme in ["additive", "seed_dominant"]:
        print(f"Seed ratio: {CONFIG['weights']['additive_seed_ratio']}")
    print()

    for topic in pruned['topic'].unique():
        topic_df = pruned[pruned['topic'] == topic]
        vecs = []
        ws = []

        for _, row in topic_df.iterrows():
            t = row['term']
            seed_w = row.get('weight', default_core_weight)
            if pd.isna(seed_w):
                seed_w = default_core_weight

            if t not in vocab2vec:
                continue

            v = vocab2vec[t]
            w = hybrid_weight(t, seed_w)

            vecs.append(v)
            ws.append(w)
            topic2terms[topic].append(t)

        if not vecs:
            continue

        # Weighted average of term vectors
        V = np.vstack(vecs)
        W = np.array(ws).reshape(-1, 1)
        tv = (V * W).sum(axis=0) / (W.sum() + 1e-12)
        tv = tv / (np.linalg.norm(tv) + 1e-12)
        topic2vec[topic] = tv

        # Show weight statistics
        avg_seed_w = topic_df['weight'].mean() if 'weight' in topic_df.columns else default_core_weight
        avg_combined_w = np.mean(ws)
        print(f"  {topic}:")
        print(f"    Terms: {len(topic2terms[topic])}")
        print(f"    Avg seed weight: {avg_seed_w:.3f}")
        print(f"    Avg combined weight: {avg_combined_w:.3f}")

    print(f"\n✓ Created {len(topic2vec)} topic vectors with hybrid weighting")
```

---

## Step 4: Update Curation to Preserve Weights

When curating, preserve the weight column. Update your curation script or add this function:

```python
def curate_dictionary_preserving_weights(expanded_candidates_path, seed_dict_path, output_path, config):
    """Curate dictionary while preserving seed weights."""
    import pandas as pd

    # Get defaults from config
    default_core_weight = config["weights"]["default_core_weight"]
    default_discovered_weight = config["weights"]["default_discovered_weight"]

    # Load seed dictionary to get original weights
    if str(seed_dict_path).endswith('.csv'):
        seed_df = pd.read_csv(seed_dict_path)
    else:
        seed_df = pd.read_excel(seed_dict_path)

    has_weights = 'weight' in seed_df.columns

    if has_weights:
        term_weights = dict(zip(seed_df['keyword'], seed_df['weight']))
        print(f"✓ Loaded {len(term_weights)} seed term weights")
    else:
        print(f"⚠ No weights in seed dictionary - will use defaults")
        term_weights = {}

    # Load expanded candidates
    candidates_df = pd.read_csv(expanded_candidates_path)

    # YOUR CURATION LOGIC HERE
    curated_df = candidates_df.copy()  # Replace with actual curation

    # Add weight column
    def get_weight(term):
        if term in term_weights:
            return term_weights[term]  # From seed
        else:
            return default_discovered_weight  # Discovered term

    curated_df['weight'] = curated_df['term'].map(get_weight)

    # Statistics
    n_from_seed = (curated_df['term'].isin(term_weights.keys())).sum()
    n_discovered = len(curated_df) - n_from_seed

    print(f"✓ Weight statistics:")
    print(f"  {n_from_seed} terms from seed")
    print(f"  {n_discovered} terms discovered (default={default_discovered_weight})")

    # Save
    curated_df.to_csv(output_path, index=False)
    return curated_df
```

---

## Step 5: Update Your Dictionary Path

You can use your CSV directly. Update CONFIG:

```python
CONFIG = {
    "paths": {
        "dictionary_excel": r"C:\Users\Home\policy-analysis\problem_oriented_slavery_legacy_dictionary.csv",
        # ... other paths ...
    },
    "dictionary": {
        "use_excel": True,  # Will work with CSV too
        "topic_column": "topic",
        "keyword_column": "keyword",
        # ... rest ...
    }
}
```

Or convert to Excel if preferred:

```python
import pandas as pd

df = pd.read_csv(r'C:\Users\Home\policy-analysis\problem_oriented_slavery_legacy_dictionary.csv')
excel_path = r'C:\Users\Home\policy-analysis\problem_oriented_legacy_seed_weighted.xlsx'
df[['topic', 'keyword', 'weight']].to_excel(excel_path, sheet_name='Dictionary', index=False)
```

---

## How the Weighting System Works

### Your Seed Weights (Semantic Importance)

From your CSV:
- **1.0** = Core terms: "armoede", "racisme", "slavernij", "corruptie"
- **0.95** = Very important: "plantage-economie", "koloniale exploitatie"
- **0.90** = Important: "dwangarbeid", "discriminatie"
- **0.85** = Supporting: "kolonialisme", "segregatie"
- **0.75-0.80** = Context terms

### SIF Weights (Statistical Rarity)

Calculated from corpus:
- Rare terms → HIGH weight (e.g., 0.9)
- Common terms → LOW weight (e.g., 0.2)

### Hybrid Weights (Combined)

Using **multiplicative** (recommended):

| Term | Seed | SIF | Hybrid | Interpretation |
|------|------|-----|--------|----------------|
| "plantage-economie" | 0.95 | 0.9 | 0.855 | Important & rare = very high weight |
| "slavernij" | 1.0 | 0.3 | 0.3 | Core but common = moderate weight |
| "historisch" | 0.7 | 0.1 | 0.07 | Generic & common = low weight |
| Discovered term | 0.8 | 0.6 | 0.48 | Default discovered weight |

---

## Configuration Recommendations

### For Historical Corpus (Iteration 1 - Causes):

```python
"weights": {
    "default_core_weight": 1.0,        # Trust your core historical terms
    "default_discovered_weight": 0.75,  # Be cautious with discovered
    "weighting_scheme": "multiplicative",
}
```

### For Policy Corpus (Iteration 2 - Applications):

```python
"weights": {
    "default_core_weight": 0.95,       # Slightly lower
    "default_discovered_weight": 0.85,  # More trust in contemporary terms
    "weighting_scheme": "multiplicative",
}
```

### If You Want More Seed Control:

```python
"weights": {
    "default_core_weight": 1.0,
    "default_discovered_weight": 0.8,
    "weighting_scheme": "seed_dominant",
    "additive_seed_ratio": 0.75,  # 75% seed, 25% SIF
}
```

---

## Benefits

1. **Semantic Control**: You define importance via seed weights
2. **Statistical Balance**: SIF prevents common words from dominating
3. **Two-tier System**: Core terms (1.0) vs discovered terms (0.8)
4. **Transparency**: Clear separation of concerns
5. **Flexibility**: Easy to tune via config

---

## Testing

After integration:

```python
# Check weight distribution
curated_df = pd.read_csv('path/to/curated_dictionary.csv')
print(curated_df['weight'].describe())
print("\nTerms by source:")
print(f"From seed: {(curated_df['weight'] != 0.8).sum()}")
print(f"Discovered: {(curated_df['weight'] == 0.8).sum()}")

# Run with different schemes
CONFIG['weights']['weighting_scheme'] = 'multiplicative'
# Build vectors, evaluate

CONFIG['weights']['weighting_scheme'] = 'seed_dominant'
CONFIG['weights']['additive_seed_ratio'] = 0.75
# Build vectors, compare
```

---

## Troubleshooting

**Q: All weights are 0.8, even for seed terms?**
- Check that seed dictionary has 'weight' column
- Check that curation preserved the weight column

**Q: Weights seem to have no effect?**
- Verify `CONFIG['scoring']['use_sif']` is True
- Check weighting_scheme is set correctly

**Q: Want to give more weight to seed?**
- Use `"weighting_scheme": "seed_dominant"`
- Set `"additive_seed_ratio": 0.8` (80% seed, 20% SIF)

**Q: How to see actual combined weights?**
- Check console output during vector building
- Shows "Avg seed weight" and "Avg combined weight" per topic

---

## Summary

1. Add `CONFIG['weights']` section
2. Replace `load_dictionary_from_excel` function
3. Replace vector building code
4. Update curation to preserve weights
5. Use your CSV (already has weights!)
6. Run workflow - weights now influence vectors!

Your seed weights will now guide topic vector construction while still benefiting from corpus statistics!
