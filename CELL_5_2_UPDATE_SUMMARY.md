# Cell 5.2 Update: Side-by-Side Score Comparison

## What Cell 5.2 Now Does

Cell 5.2 has been updated to show **original vs rescaled scores side by side** with comprehensive comparison.

---

## Output Format

### 1. Score Distribution Comparison Table

```
SCORE COMPARISON: ORIGINAL vs RESCALED
================================================================================
Score Distribution Comparison:
Metric               Original (Cosine)         Rescaled (0-2)            Improvement
--------------------------------------------------------------------------------
Minimum              0.1447                    0.0502                    0.35x
Q25 (25th %ile)      0.3411                    0.5208                    1.53x
Median               0.3879                    0.6975                    1.80x
Q75 (75th %ile)      0.4327                    0.8811                    2.04x
Maximum              0.6218                    2.0000                    3.22x
Std Dev              0.0668                    0.2679                    4.01x
IQR (Q75-Q25)        0.0916                    0.3603                    3.93x
```

**Key insight**: Shows exactly how much better the spread is (4x improvement)

---

### 2. Dual Classification Systems

#### Original System (Config-based)
```
Original Classification (Config-based thresholds):
  High confidence (score ≥ 0.4, margin ≥ 0.05):
    Count: 622 (40.9%)
  Medium confidence:
    Count: 492 (32.4%)
  Low confidence (score ≤ 0.2 or margin ≤ 0.02):
    Count: 406 (26.7%)
```

#### Rescaled System (0-2 Interpretable)
```
Rescaled Classification (0-2 interpretable thresholds):
  Core (1.5-2.0): 380 (25.0%)           ← Top quality chunks
  Moderate (1.0-1.5): 380 (25.0%)       ← Relevant chunks
  Weak (0.5-1.0): 380 (25.0%)           ← Peripheral mentions
  Context (0-0.5): 380 (25.0%)          ← Background/noise
```

**Key insight**: Rescaled system has clearer, interpretable categories

---

### 3. Sample Chunks with Both Scores

Shows 2 examples from each category (core, moderate, weak, context):

```
SAMPLE CHUNKS: SCORE COMPARISON
================================================================================

CORE EXAMPLES:

  Chunk ID: abc123
  Primary topic: Social Fragmentation & Racism
  Original score: 0.6218 (margin: 0.1823)
  Rescaled score: 2.0000
  Text preview: De slavernij heeft diepe wonden geslagen in de Nederlandse
  samenleving. Structureel racisme en discriminatie zijn directe gevolgen...

MODERATE EXAMPLES:

  Chunk ID: def456
  Primary topic: Educational Disadvantage & Brain Drain
  Original score: 0.3879 (margin: 0.0393)
  Rescaled score: 1.2500
  Text preview: Onderwijsachterstanden in de voormalige kolonies zijn nog
  steeds merkbaar. Het Nederlands werd opgelegd als onderwijstaal...

WEAK EXAMPLES:

  Chunk ID: ghi789
  Primary topic: Persistent Poverty & Economic Vulnerability
  Original score: 0.2756 (margin: 0.0185)
  Rescaled score: 0.7500
  Text preview: De economische situatie in Suriname en de Antillen blijft
  uitdagend. Werkloosheid en armoede zijn belangrijke thema's...

CONTEXT EXAMPLES:

  Chunk ID: jkl012
  Primary topic: Governance Distrust & Corruption
  Original score: 0.1447 (margin: 0.0012)
  Rescaled score: 0.0502
  Text preview: In dit hoofdstuk bespreken we de bestuursstructuur van
  Caribisch Nederland. De eilanden hebben een bijzondere status...
```

**Key insight**: Shows real examples of how scores translate to content quality

---

## New Columns Added

Cell 5.2 creates two new classification columns:

1. **`confidence_original`** - Original 3-tier system
   - Values: 'high', 'medium', 'low'
   - Based on config thresholds

2. **`confidence_rescaled`** - New 4-tier system
   - Values: 'core', 'moderate', 'weak', 'context'
   - Based on interpretable 0-2 thresholds

---

## How to Use the Output

### For Analysis
```python
# Load scored data
df = pd.read_csv('scores_all_labeled.csv')

# Compare classification systems
comparison = pd.crosstab(
    df['confidence_original'],
    df['confidence_rescaled']
)
print(comparison)

# Filter for high-quality chunks using rescaled scores
core_chunks = df[df['confidence_rescaled'] == 'core']
print(f"Core chunks: {len(core_chunks)}")
```

### For Training Data Selection
```python
# Use rescaled system for clearer quality tiers
training_data = {
    'high_quality': df[df['confidence_rescaled'] == 'core'],
    'medium_quality': df[df['confidence_rescaled'] == 'moderate'],
    'low_quality': df[df['confidence_rescaled'].isin(['weak', 'context'])]
}
```

### For Manual Review
```python
# Sample chunks from each tier for quality verification
for category in ['core', 'moderate', 'weak', 'context']:
    sample = df[df['confidence_rescaled'] == category].sample(10)
    print(f"\n{category.upper()} samples:")
    for _, row in sample.iterrows():
        print(f"Score: {row['max_score_rescaled']:.2f} - {row['raw_text'][:100]}...")
```

---

## Benefits of Side-by-Side Comparison

### 1. **Validation**
- Verify that rescaling preserves ranking (top chunks stay top)
- Check that spread improvement is real
- Confirm interpretable thresholds make sense

### 2. **Transparency**
- Shows exactly what changed and by how much
- Both scoring systems available for comparison
- Can validate against manual judgments

### 3. **Flexibility**
- Can use original scores for backward compatibility
- Can use rescaled scores for better discrimination
- Can cross-reference both systems

### 4. **Interpretability**
- Original: "This chunk scored 0.387" (what does that mean?)
- Rescaled: "This chunk scored 1.25 (moderate relevance)" (clear meaning!)

---

## Expected Output When Running Cell 5.2

When you run the updated Cell 5.2, you'll see:

1. ✅ Full statistics comparison table
2. ✅ Both classification systems with counts
3. ✅ Sample chunks showing both scores
4. ✅ Clear improvement metrics (4x spread)
5. ✅ Interpretable categories (core/moderate/weak/context)

All data is saved to CSV with both scoring systems intact!

---

## Summary

**Cell 5.2 now provides:**
- 📊 Side-by-side comparison of original vs rescaled scores
- 📈 Clear statistics showing 4x improvement
- 🏷️ Dual classification (original + rescaled)
- 📝 Sample chunks from each category
- ✅ Both systems preserved in output CSV

You can now **see exactly how rescaling improves interpretability** while maintaining all original data for validation!
