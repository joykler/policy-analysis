# How to Reduce Dictionary for Faster Cross-Encoder Scoring

## Goal: Reduce from ~1,000 terms to ~240 terms (60 per topic)

## Why Reduce?
- **Current**: 250 terms/topic = 8-10 hours scoring time
- **Reduced**: 60 terms/topic = 2-3 hours scoring time
- **Quality**: Often BETTER (removing noise, keeping signal)

---

## Method 1: Python Script (Automated)

Save this as `reduce_dictionary.py` and run it:

```python
import pandas as pd
from pathlib import Path

# Configuration
WORKFLOW = "slavery_Slavdict_pretrained_slavery_v5"  # Update this
TERMS_PER_TOPIC = 60  # How many to keep per topic

# Load dictionary
workflow_path = Path(f"workflow_data/{WORKFLOW}")
dict_path = workflow_path / "Dictionary" / "curated_dictionary.csv"

df = pd.read_csv(dict_path)
print(f"Original dictionary: {len(df)} terms")

# Strategy: Keep top N terms per topic based on:
# 1. Core seed terms (source='core' or higher weight)
# 2. Best discovered terms by weight

reduced_terms = []

for topic in df['topic'].unique():
    topic_df = df[df['topic'] == topic].copy()

    # Sort by weight (descending) and source priority
    # Ensure we keep all core terms if they exist
    if 'source' in topic_df.columns:
        topic_df['priority'] = topic_df['source'].map({'core': 0, 'discovered': 1}).fillna(1)
        topic_df = topic_df.sort_values(['priority', 'weight'], ascending=[True, False])
    else:
        topic_df = topic_df.sort_values('weight', ascending=False)

    # Keep top N
    keep = topic_df.head(TERMS_PER_TOPIC)
    reduced_terms.append(keep)

    print(f"\n{topic}:")
    print(f"  Original: {len(topic_df)} terms")
    print(f"  Keeping: {len(keep)} terms")
    print(f"  Weight range: {keep['weight'].min():.2f} - {keep['weight'].max():.2f}")

# Combine and save
reduced_df = pd.concat(reduced_terms, ignore_index=True)

# Save backup
backup_path = dict_path.parent / f"{dict_path.stem}_backup_1000terms.csv"
df.to_csv(backup_path, index=False)
print(f"\n✓ Backup saved: {backup_path.name}")

# Save reduced version
reduced_df.to_csv(dict_path, index=False)
print(f"✓ Reduced dictionary saved: {dict_path.name}")
print(f"\nTotal: {len(reduced_df)} terms ({len(df) - len(reduced_df)} removed)")
```

**Run it:**
```bash
python reduce_dictionary.py
```

---

## Method 2: Manual in Excel/CSV

### Step 1: Open the Dictionary
```
File: workflow_data/slavery_Slavdict_pretrained_slavery_v5/Dictionary/curated_dictionary.csv
```

### Step 2: Create Backup
Save a copy as `curated_dictionary_backup_1000terms.csv`

### Step 3: Filter and Sort
For each topic:
1. Filter by topic name
2. Sort by `weight` column (highest first)
3. Keep top 60 rows
4. Delete the rest

### Step 4: Verify Totals
- Educational Disadvantage: 60 terms
- Governance Distrust: 60 terms
- Persistent Poverty: 60 terms
- Social Fragmentation: 60 terms
- **Total: 240 terms**

### Step 5: Save
Save as original filename `curated_dictionary.csv`

---

## Method 3: Interactive Python (Jupyter/Notebook)

```python
import pandas as pd

# Load
df = pd.read_csv("workflow_data/.../Dictionary/curated_dictionary.csv")

# Show current distribution
print(df['topic'].value_counts())

# Review terms to keep (interactive)
for topic in df['topic'].unique():
    topic_df = df[df['topic'] == topic].sort_values('weight', ascending=False)

    print(f"\n{topic} - Top 60 terms:")
    print(topic_df.head(60)[['term', 'weight']].to_string())

    # Manual review: any to remove or add?

# Keep top 60 per topic
reduced = df.groupby('topic', group_keys=False).apply(
    lambda x: x.nlargest(60, 'weight')
)

# Save
reduced.to_csv("workflow_data/.../Dictionary/curated_dictionary.csv", index=False)
print(f"Reduced to {len(reduced)} terms")
```

---

## Curation Strategy: What to Keep?

### Priority 1: Core Seed Terms (KEEP ALL)
```
Terms marked as 'core' or manually curated
Example: "onderwijsachterstand", "slavernij", "discriminatie"
These have domain expert knowledge
```

### Priority 2: High-Weight Discovered Terms
```
Terms with weight > 0.9
Automatically expanded but high relevance
Example: "schooluitval", "raciale hiërarchie"
```

### Priority 3: Distinctive Terms
```
Terms unique to one topic (not generic)
Example: "brain drain" (specific to education)
NOT: "beleid" (appears in all topics)
```

### Remove: Generic/Ambiguous Terms
```
Terms that appear in multiple contexts
Example: "zaken", "bijvoorbeeld", "recent"
These add noise, not signal
```

### Remove: Rare Terms (Never Match)
```
Terms that appear < 5 times in corpus
Example: highly specific technical jargon
Can't train model on terms it never sees
```

---

## Quality Checks After Reduction

### Check 1: Weight Distribution
```python
# Should see clear core vs discovered separation
reduced['weight'].describe()

# Expected:
# Min: 0.70 (discovered terms)
# Max: 1.00 (core terms)
# Mean: ~0.85
```

### Check 2: Topic Balance
```python
# All topics should have similar counts
reduced['topic'].value_counts()

# Expected:
# Topic 1: 60 terms
# Topic 2: 60 terms
# Topic 3: 60 terms
# Topic 4: 60 terms
```

### Check 3: Term Quality
```python
# Sample 10 random terms per topic - are they relevant?
for topic in reduced['topic'].unique():
    print(f"\n{topic} - Random sample:")
    print(reduced[reduced['topic']==topic].sample(10)['term'].tolist())
```

---

## Expected Impact

### Speed Improvement:
```
Before: 1,006 terms × 3,701 chunks = 3.7M comparisons
After:  240 terms × 3,701 chunks = 888K comparisons
Speedup: 4.2x faster (8 hours → 2 hours)
```

### Quality Impact:
```
Removing noise terms often IMPROVES quality:
  - Clearer topic separation
  - Less confusion from ambiguous terms
  - Stronger signal-to-noise ratio
```

### Training Impact:
```
With fewer terms:
  - Model learns faster
  - More focused patterns
  - Better generalization
```

---

## After Reduction: Re-run Pipeline

### Step 1: Verify Dictionary
```bash
# Check file size
ls -lh workflow_data/.../Dictionary/curated_dictionary.csv

# Should be ~25% of original size
```

### Step 2: Re-run Checkpoint 4
```
Expected output:
  Educational Disadvantage: 60 terms
  Governance Distrust: 60 terms
  Persistent Poverty: 60 terms
  Social Fragmentation: 60 terms

  Weight range: 0.700 - 1.000
  Avg weight: 0.850
```

### Step 3: Re-run Checkpoint 5
```
Expected time: 2-3 hours (down from 8-10 hours)
Progress bar should show 3,701 iterations (not 14,640)
```

### Step 4: Check Results
```
Score distribution should be:
  - Negative scores: 20-40% (good - detecting non-matches)
  - Low positive (0-0.3): 40-50%
  - Mid positive (0.3-0.5): 10-20%
  - High positive (>0.5): 5-10% (after training)
```

---

## Troubleshooting

### Issue: "Not enough terms per topic"
```
Solution: Increase TERMS_PER_TOPIC to 80 or 100
Still much better than 250
```

### Issue: "Lost important core terms"
```
Solution:
1. Check backup file
2. Manually add back critical terms
3. Ensure 'source' column marks core terms
```

### Issue: "Topics unbalanced"
```
Solution:
- Some topics naturally have more terms
- OK to have 50-70 range instead of exactly 60
- Focus on quality, not exact count
```

---

## Alternative: Semi-Automated Curation

```python
import pandas as pd

df = pd.read_csv("workflow_data/.../Dictionary/curated_dictionary.csv")

# Auto-keep: All core terms + top 30 discovered per topic
auto_keep = []

for topic in df['topic'].unique():
    topic_df = df[df['topic'] == topic]

    # Keep all core
    if 'source' in topic_df.columns:
        core = topic_df[topic_df['source'] == 'core']
        auto_keep.append(core)

        # Top 30 discovered
        discovered = topic_df[topic_df['source'] == 'discovered']
        discovered = discovered.nlargest(30, 'weight')
        auto_keep.append(discovered)
    else:
        # No source column: keep top 60 by weight
        auto_keep.append(topic_df.nlargest(60, 'weight'))

reduced = pd.concat(auto_keep, ignore_index=True)

# Manual review of borderline terms (weight 0.75-0.85)
borderline = df[(df['weight'] >= 0.75) & (df['weight'] <= 0.85)]
print("\nBorderline terms for manual review:")
print(borderline[['topic', 'term', 'weight']])

# Save
reduced.to_csv("workflow_data/.../Dictionary/curated_dictionary.csv", index=False)
```

---

## Summary

**Recommended approach:**
1. Use automated script (Method 1)
2. Keep 60 terms per topic
3. Re-run Checkpoint 4 & 5
4. Verify results look reasonable
5. Continue to training

**Expected outcome:**
- 4x faster scoring
- Same or better quality
- Cleaner, more focused dictionary
