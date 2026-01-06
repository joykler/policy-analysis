# Cell 53 & 54 Fix: Use Existing Significance-Based Confidence

## Problem

**Cell 53** recalculates confidence using hardcoded margin thresholds:
```python
HIGH_CONFIDENCE_THRESHOLD = 0.15  # For cosine similarity (0-1 range)
LOW_CONFIDENCE_THRESHOLD = 0.05   # For cosine similarity (0-1 range)
```

**Issues:**
1. These thresholds are for OLD cosine scores (0-1 range)
2. New dot product scores have different range (0-10)
3. Confidence is ALREADY calculated in Cell 37 using significance scoring
4. This redundantly recalculates and OVERWRITES the better significance-based confidence

**Cell 54** uses the recalculated confidence for stratified sampling.

---

## Solution: Use Existing Confidence from Cell 37

Cell 37 already provides `confidence` column with values:
- `high` = High significance (significance >= 0.70)
- `low` = Medium + Low significance (0.30 <= significance < 0.70)
- `none` = Noise (significance < 0.30 or CV < 0.10)

---

## Option 1: Delete Cells 53 & 54 (RECOMMENDED)

The confidence calculation in Cell 37 is superior because it uses:
- Coefficient of Variation (noise detection)
- Magnitude + Differentiation + Contrast
- Calibrated for dot product scores

**Simply delete Cell 53 and Cell 54** - the data already has the `confidence` column.

If you want stratified sampling, add it to Cell 44 (training data prep) instead.

---

## Option 2: Update Cell 53 to Use Existing Confidence

If you want to keep Cell 53 for validation/checking, update it to just verify the existing confidence:

```python
# ============================================================
# CELL 7.5a: Verify Confidence Distribution
# ============================================================

print("Checking confidence distribution from significance scoring...")
print()

# The 'confidence' column was already calculated in Cell 37 (significance-based)
# It maps significance scores to: high/low/none

if 'confidence' not in train_df.columns:
    raise ValueError("'confidence' column not found! Did you run Cell 37 (significance scoring)?")

# Show distribution
print("Confidence level distribution (from Cell 37 significance scoring):")
for conf in ['high', 'low', 'none']:
    count = (train_df['confidence'] == conf).sum()
    pct = count / len(train_df) * 100
    print(f"  {conf:10} {count:6} ({pct:5.1f}%)")

print(f"\nTotal: {len(train_df)}")
print("✓ Using existing significance-based confidence")
```

---

## Option 3: Update Cell 54 for Dot Product Scores

If you want to keep stratified sampling but need to recalculate confidence for some reason, update the thresholds for dot product:

```python
# ============================================================
# CELL 7.5a: Calculate Confidence (Dot Product Scores)
# ============================================================

# NOTE: This recalculates confidence using margin-based approach
# Cell 37 uses a BETTER approach (CV-based significance)
# Consider deleting this cell and using Cell 37's confidence instead

# Thresholds for DOT PRODUCT scores (0-10 range)
HIGH_CONFIDENCE_THRESHOLD = 1.5  # ~15-20% of typical range
LOW_CONFIDENCE_THRESHOLD = 0.5   # ~5-10% of typical range

def calculate_confidence_level(row, score_columns):
    scores = row[score_columns].values
    sorted_scores = np.sort(scores)[::-1]

    if len(sorted_scores) < 2:
        return 'high'

    margin = sorted_scores[0] - sorted_scores[1]

    if margin > HIGH_CONFIDENCE_THRESHOLD:
        return 'high'
    elif margin > LOW_CONFIDENCE_THRESHOLD:
        return 'low'
    else:
        return 'none'

# Auto-detect DOT PRODUCT score columns
score_columns = [col for col in train_df.columns if col.startswith('score_') and col != 'score_margin']

if len(score_columns) == 0:
    raise ValueError("No 'score_' columns found! Check that Cell 36 (dot product scoring) ran correctly.")

print(f"Found {len(score_columns)} score columns: {score_columns}")

# Add confidence levels
train_df['confidence_level'] = train_df.apply(
    lambda row: calculate_confidence_level(row, score_columns),
    axis=1
)

# Show distribution
print("\nConfidence level distribution (margin-based):")
for conf in ['high', 'low', 'none']:
    count = (train_df['confidence_level'] == conf).sum()
    pct = count / len(train_df) * 100
    print(f"  {conf:10} {count:6} ({pct:5.1f}%)")

print(f"\nTotal: {len(train_df)}")
print("⚠️  Warning: This uses simple margin-based confidence.")
print("   Cell 37's CV-based significance is more accurate for noise detection!")
```

---

## Recommended Action

**DELETE Cell 53 and Cell 54** entirely.

Reasoning:
1. Cell 37 already provides superior confidence classification
2. Uses CV to detect noise (uniform scores)
3. Calibrated for dot product scores
4. No need for redundant calculations
5. Stratified sampling can be done in Cell 44 if needed

---

## If You Need Stratified Sampling

Add to Cell 44 (after creating data options):

```python
# =====================
# OPTIONAL: STRATIFIED SAMPLING BY CONFIDENCE
# =====================

APPLY_CONFIDENCE_SAMPLING = CONFIG.get("training", {}).get("apply_confidence_sampling", False)

if APPLY_CONFIDENCE_SAMPLING and 'confidence' in data_opt4.columns:
    print(f"\n{'='*60}")
    print("APPLYING CONFIDENCE-BASED STRATIFIED SAMPLING")
    print(f"{'='*60}")

    # Target distribution
    TARGET_DISTRIBUTION = {
        'high': 0.50,   # 50% high confidence (primary training data)
        'low': 0.40,    # 40% low confidence (secondary data)
        'none': 0.10    # 10% none (hard negatives)
    }

    print("\nOriginal distribution:")
    for conf in ['high', 'low', 'none']:
        count = (data_opt4['confidence'] == conf).sum()
        pct = count / len(data_opt4) * 100
        print(f"  {conf:10} {count:6} ({pct:5.1f}%)")

    # Sample to target distribution
    sampled_dfs = []
    target_total = len(data_opt4)

    for conf in ['high', 'low', 'none']:
        subset = data_opt4[data_opt4['confidence'] == conf]
        target = int(target_total * TARGET_DISTRIBUTION[conf])

        if len(subset) == 0:
            continue

        if len(subset) >= target:
            sampled = subset.sample(n=target, random_state=42)
        else:
            sampled = subset  # Use all available

        sampled_dfs.append(sampled)

    data_opt4 = pd.concat(sampled_dfs, ignore_index=True).sample(frac=1, random_state=42)

    print("\nAfter stratified sampling:")
    for conf in ['high', 'low', 'none']:
        count = (data_opt4['confidence'] == conf).sum()
        pct = count / len(data_opt4) * 100
        print(f"  {conf:10} {count:6} ({pct:5.1f}%)")
```

---

## Summary

| Cell | Current Issue | Recommended Fix |
|------|---------------|-----------------|
| Cell 53 | Recalculates confidence with hardcoded cosine thresholds | **DELETE** - use Cell 37's confidence |
| Cell 54 | Stratified sampling using wrong confidence | **DELETE** - or move to Cell 44 if needed |

The `confidence` column from Cell 37 is better because:
- ✅ Uses CV to detect noise (uniform scores)
- ✅ Calibrated for dot product range (0-10)
- ✅ Multi-component significance score
- ✅ No hardcoded thresholds
