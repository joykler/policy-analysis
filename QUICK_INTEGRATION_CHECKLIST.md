# Quick Integration Checklist - Weighted Dictionary Support

## TL;DR

Your CSV has weights, but the code ignores them. Here's how to fix it in 5 steps.

---

## ✅ Step 1: Add CONFIG Section (2 minutes)

In your notebook, find the CONFIG dict and add this after the "scoring" section:

```python
# NEW: Add this entire section
"weights": {
    "default_core_weight": 1.0,        # For seed terms without explicit weight
    "default_discovered_weight": 0.8,  # For expanded terms not in seed
    "weighting_scheme": "multiplicative",
    "additive_seed_ratio": 0.7,
},
```

**Location**: After `CONFIG["scoring"]`, before next section

---

## ✅ Step 2: Update Dictionary Path (1 minute)

Option A - Use Excel (already created for you):
```python
CONFIG["paths"]["dictionary_excel"] = r"C:\Users\Home\policy-analysis\problem_oriented_legacy_seed_weighted.xlsx"
```

Option B - Use CSV directly:
```python
CONFIG["paths"]["dictionary_excel"] = r"C:\Users\Home\policy-analysis\problem_oriented_slavery_legacy_dictionary.csv"
```

**Location**: In `CONFIG["paths"]`

---

## ✅ Step 3: Replace Load Function (5 minutes)

**Find**: The `load_dictionary_from_excel` function (around line 786)

**Replace with**: See WEIGHTED_DICTIONARY_INTEGRATION_GUIDE.md, "Step 2: Modify Code - Load Dictionary Function"

**Key change**: Now reads 'weight' column and returns `(keyword, weight)` tuples

---

## ✅ Step 4: Replace Vector Building (10 minutes)

**Find**: The section starting with "Load curated dictionary" (around line 2320)

**Replace entire section with**: See WEIGHTED_DICTIONARY_INTEGRATION_GUIDE.md, "Step 3: Modify Code - Vector Building"

**Key changes**:
- Adds `hybrid_weight()` function
- Combines seed weights with SIF weights
- Shows weight statistics in output

---

## ✅ Step 5: Update Curation (5 minutes)

When you curate the dictionary, preserve the weight column.

**Quick method** - Add this after filtering your candidates:

```python
# Load seed weights
seed_df = pd.read_csv(r'C:\Users\Home\policy-analysis\problem_oriented_slavery_legacy_dictionary.csv')
seed_weights = dict(zip(seed_df['keyword'], seed_df['weight']))

# Add weight column to curated data
default_discovered = CONFIG['weights']['default_discovered_weight']  # 0.8
curated_df['weight'] = curated_df['term'].map(lambda t: seed_weights.get(t, default_discovered))

# Save with weights
curated_df.to_csv(output_path, index=False)
```

**What this does**:
- Terms from seed get their original weight (0.7-1.0)
- Discovered terms get default (0.8)

---

## 🧪 Test It Works

After making changes, run the notebook and check console output:

### During Dictionary Loading:
```
✓ Found weight column in seed dictionary
✓ Loaded 5 topics with 377 keywords
```

### During Vector Building:
```
============================================================
BUILDING TOPIC VECTORS WITH HYBRID WEIGHTS
============================================================
Weighting scheme: multiplicative
Default core weight: 1.0
Default discovered weight: 0.8
SIF parameter a = 0.001

  Persistent Poverty & Economic Vulnerability:
    Terms: 71
    Avg seed weight: 0.852
    Avg combined weight: 0.421
  ...
```

If you see this ✓, it's working!

---

## 📊 What Changes?

### Before (SIF only):
- Common important terms (like "slavernij") get low weight
- Rare generic terms might get high weight
- Your expert judgments ignored

### After (Hybrid):
- "plantage-economie" (important + rare) → very high weight
- "slavernij" (important + common) → moderate weight
- "historisch" (generic + common) → very low weight
- **Your weights now matter!**

---

## 🎛️ Tuning Options

Default configuration (recommended):
```python
"weighting_scheme": "multiplicative",  # seed × sif
"default_core_weight": 1.0,            # Full trust in seed
"default_discovered_weight": 0.8,      # Moderate trust in discovered
```

If you want MORE control over seed weights:
```python
"weighting_scheme": "seed_dominant",
"additive_seed_ratio": 0.75,  # 75% seed, 25% SIF
```

If you want MORE statistical influence:
```python
"weighting_scheme": "multiplicative",  # Keep as is
"default_core_weight": 0.9,            # Slightly reduce seed influence
```

---

## ⚠️ Common Issues

**Issue**: "KeyError: 'weights'" during vector building
**Fix**: You forgot Step 1 - add CONFIG['weights'] section

**Issue**: All weights are 1.0 in curated dictionary
**Fix**: Curation didn't preserve weights - see Step 5

**Issue**: Console shows "No weight column found"
**Fix**: Check dictionary path points to weighted file

**Issue**: Weights don't seem to change results
**Fix**: Make sure `CONFIG['scoring']['use_sif']` is `True`

---

## 📁 Files You Need

1. **Integration guide**: [WEIGHTED_DICTIONARY_INTEGRATION_GUIDE.md](WEIGHTED_DICTIONARY_INTEGRATION_GUIDE.md) - Full details
2. **Your weighted seed**: [problem_oriented_legacy_seed_weighted.xlsx](problem_oriented_legacy_seed_weighted.xlsx) - Ready to use
3. **Summary**: [WEIGHTED_DICTIONARY_SUMMARY.md](WEIGHTED_DICTIONARY_SUMMARY.md) - Why and how

---

## Time Estimate

- Reading this: 5 min
- Step 1 (CONFIG): 2 min
- Step 2 (path): 1 min
- Step 3 (load function): 5 min
- Step 4 (vector building): 10 min
- Step 5 (curation): 5 min
- Testing: 5 min

**Total: ~30 minutes** to add weighted dictionary support

---

## Bottom Line

Three code changes + one CONFIG section = your weights now influence topic vectors!

The system will:
- ✅ Read weights from your dictionary
- ✅ Preserve them during curation
- ✅ Combine them with corpus statistics
- ✅ Create better topic vectors that reflect your expert knowledge

Start with Step 1 → Test → Adjust weighting_scheme if needed.
