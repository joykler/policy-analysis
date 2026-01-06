"""
Apply Curation for Heritage & Memory - V4
Based on v3 learnings: this topic had 43% removal rate due to semantic drift
"""

import pandas as pd

# Load progress from Colonial curation
df = pd.read_csv('C:/Users/Home/policy-analysis/workflow_data/slavery_Short-slavdict_pretrained_slavery_v4/Dictionary/curation_progress.csv')

print("="*80)
print("HERITAGE & MEMORY - APPLYING CURATION")
print("="*80)

heritage_mask = df['topic'] == 'Heritage & Memory'
heritage = df[heritage_mask].copy()
heritage_expanded = heritage[heritage['is_seed'] == 0]

print(f"\nTotal: {len(heritage)} terms")
print(f"Expanded: {len(heritage_expanded)} terms")

removals = []
weight_changes = []

# ============================================================================
# PHASE 1: AUTOMATIC REMOVALS
# ============================================================================

print("\nPHASE 1: Automatic Removals")

# Low cosine (<0.65)
mask = heritage_mask & (df['is_seed'] == 0) & (df['cosine'] < 0.65)
count = mask.sum()
if count > 0:
    df.loc[mask, 'decision'] = 'REMOVE'
    df.loc[mask, 'reason'] = 'Low cosine (<0.65)'
    removals.append(('Low cosine', count))
    print(f"  Low cosine: {count} removed")

# ============================================================================
# PHASE 2: SEMANTIC DRIFT (Known patterns from v3)
# ============================================================================

print("\nPHASE 2: Semantic Drift Detection")

# Month names from "1 juli"
month_names = ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december']
mask = heritage_mask & (df['term'].isin(month_names)) & (df['is_seed'] == 0)
count = mask.sum()
if count > 0:
    df.loc[mask, 'decision'] = 'REMOVE'
    df.loc[mask, 'reason'] = 'Semantic drift - month names from date'
    removals.append(('Month names', count))
    print(f"  Month names: {count} removed")

# Wrong meanings from "herdenking" (commemoration)
wrong_herdenking = ['aanbidding', 'bewondering', 'beschuldiging', 'gezag', 'beschouwing', 'rede', 'stiltes', 'heiligen', 'opofferingen', 'beschouwingen', 'intrede']
mask = heritage_mask & (df['term'].isin(wrong_herdenking))
count = mask.sum()
if count > 0:
    df.loc[mask, 'decision'] = 'REMOVE'
    df.loc[mask, 'reason'] = 'Semantic drift - wrong herdenking meaning'
    removals.append(('Herdenking drift', count))
    print(f"  Herdenking wrong meanings: {count} removed")

# Wrong expansions from "keti koti"
wrong_ketikoti = ['kofi', 'kauri', 'kapuweri', 'khoikhoi', 'kumi']
mask = heritage_mask & (df['term'].isin(wrong_ketikoti))
count = mask.sum()
if count > 0:
    df.loc[mask, 'decision'] = 'REMOVE'
    df.loc[mask, 'reason'] = 'Semantic drift - wrong keti koti expansion'
    removals.append(('Keti koti drift', count))
    print(f"  Keti koti wrong expansions: {count} removed")

# Generic "datum" (date)
mask = heritage_mask & (df['term'] == 'datum')
count = mask.sum()
if count > 0:
    df.loc[mask, 'decision'] = 'REMOVE'
    df.loc[mask, 'reason'] = 'Overgeneralization - too generic'
    removals.append(('Datum too generic', count))
    print(f"  Datum (date): {count} removed")

# ============================================================================
# PHASE 3: WEIGHT CALIBRATION
# ============================================================================

print("\nPHASE 3: Weight Calibration")

# High df terms
mask = heritage_mask & (df['term'] == 'nederland')
if mask.sum() > 0:
    df.loc[mask, 'new_weight'] = 0.35
    df.loc[mask, 'reason'] = 'High df - lowered to 0.35'
    weight_changes.append(('nederland', mask.sum()))
    print(f"  nederland: 0.50 -> 0.35")

# Core (1.00) + medium cosine (0.65-0.75)
mask = heritage_mask & (df['is_seed'] == 0) & (df['weight'] == 1.00) & (df['cosine'] >= 0.65) & (df['cosine'] < 0.75) & (df['decision'] == 'KEEP')
count = mask.sum()
if count > 0:
    df.loc[mask, 'new_weight'] = 0.90
    df.loc[mask, 'reason'] = 'Core (1.00) + cosine 0.65-0.75 -> 0.90'
    weight_changes.append(('Core medium cosine', count))
    print(f"  Core with medium cosine: {count} terms 1.00 -> 0.90")

# Strong (0.95) + low cosine (0.65-0.72)
mask = heritage_mask & (df['is_seed'] == 0) & (df['weight'] == 0.95) & (df['cosine'] >= 0.65) & (df['cosine'] < 0.72) & (df['decision'] == 'KEEP')
count = mask.sum()
if count > 0:
    df.loc[mask, 'new_weight'] = 0.85
    df.loc[mask, 'reason'] = 'Strong (0.95) + cosine 0.65-0.72 -> 0.85'
    weight_changes.append(('Strong low cosine', count))
    print(f"  Strong with low cosine: {count} terms 0.95 -> 0.85")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("HERITAGE & MEMORY - CURATION SUMMARY")
print("="*80)

heritage_after = df[heritage_mask & (df['decision'] == 'KEEP')]

print(f"\nOriginal: {len(heritage)} terms")
print(f"Removed: {len(heritage) - len(heritage_after)} terms ({(len(heritage) - len(heritage_after))/len(heritage)*100:.1f}%)")
print(f"Kept: {len(heritage_after)} terms")
print(f"Weight adjustments: {len(df[heritage_mask & (df['new_weight'] != df['weight'])])} terms")

print("\nRemovals:")
total_removed = 0
for reason, count in removals:
    print(f"  {reason}: {count}")
    total_removed += count
print(f"  TOTAL: {total_removed}")

print("\nWeight changes:")
for reason, count in weight_changes:
    print(f"  {reason}: {count}")

# Save progress
output_path = 'C:/Users/Home/policy-analysis/workflow_data/slavery_Short-slavdict_pretrained_slavery_v4/Dictionary/curation_progress.csv'
df.to_csv(output_path, index=False)
print(f"\nProgress saved to: {output_path}")
print("\nHeritage & Memory curation complete!")
