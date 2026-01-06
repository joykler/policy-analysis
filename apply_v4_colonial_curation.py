"""
Apply Curation for Colonial Systems - V4
"""

import pandas as pd

# Load dictionary
df = pd.read_csv('C:/Users/Home/policy-analysis/workflow_data/slavery_Short-slavdict_pretrained_slavery_v4/Dictionary/expanded_candidates.csv')

# Initialize curation columns
df['decision'] = 'KEEP'
df['reason'] = ''
df['new_weight'] = df['weight']

print("="*80)
print("COLONIAL SYSTEMS - APPLYING CURATION")
print("="*80)

colonial_mask = df['topic'] == 'Colonial Systems'
colonial = df[colonial_mask].copy()

removals = []
weight_changes = []

# ============================================================================
# DECISIONS BASED ON ANALYSIS
# ============================================================================

# 1. Remove "tuin" (garden) - semantic drift from plantage
mask = colonial_mask & (df['term'] == 'tuin')
if mask.sum() > 0:
    df.loc[mask, 'decision'] = 'REMOVE'
    df.loc[mask, 'reason'] = 'Semantic drift - tuin means garden not plantation'
    removals.append(('tuin - wrong meaning', mask.sum()))
    print(f"REMOVE: tuin (garden) - wrong semantic space")

# 2. Remove generic "landbouw" (agriculture) - too broad from plantage
mask = colonial_mask & (df['term'].isin(['landbouw', 'landbouw-', 'oogst']))
if mask.sum() > 0:
    df.loc[mask, 'decision'] = 'REMOVE'
    df.loc[mask, 'reason'] = 'Overgeneralization - too generic agriculture terms'
    removals.append(('Generic agriculture terms', mask.sum()))
    print(f"REMOVE: {mask.sum()} generic agriculture terms (landbouw, oogst)")

# 3. Lower weight for ultra-high frequency terms
# nederland (df=967)
mask = colonial_mask & (df['term'] == 'nederland')
if mask.sum() > 0:
    df.loc[mask, 'new_weight'] = 0.35
    df.loc[mask, 'reason'] = 'High df (967) - lowered from 0.50 to 0.35'
    weight_changes.append(('nederland', mask.sum()))
    print(f"WEIGHT: nederland 0.50 -> 0.35 (df=967)")

# koloniale (df=524)
mask = colonial_mask & (df['term'] == 'koloniale')
if mask.sum() > 0:
    df.loc[mask, 'new_weight'] = 0.90
    df.loc[mask, 'reason'] = 'High df (524) - lowered from 1.00 to 0.90'
    weight_changes.append(('koloniale', mask.sum()))
    print(f"WEIGHT: koloniale 1.00 -> 0.90 (df=524)")

# 4. Weight calibration: Core (1.00) + low cosine (0.65-0.75)
mask = colonial_mask & (df['is_seed'] == 0) & (df['weight'] == 1.00) & (df['cosine'] >= 0.65) & (df['cosine'] < 0.75)
count = mask.sum()
if count > 0:
    df.loc[mask, 'new_weight'] = 0.90
    df.loc[mask, 'reason'] = 'Weight 1.00 + cosine 0.65-0.75 lowered to 0.90'
    weight_changes.append(('Core with medium-low cosine', count))
    print(f"WEIGHT: {count} core terms (1.00) with cosine 0.65-0.75 -> 0.90")

# 5. Weight calibration: Strong (0.95) + low cosine (0.65-0.72)
mask = colonial_mask & (df['is_seed'] == 0) & (df['weight'] == 0.95) & (df['cosine'] >= 0.65) & (df['cosine'] < 0.72)
count = mask.sum()
if count > 0:
    df.loc[mask, 'new_weight'] = 0.85
    df.loc[mask, 'reason'] = 'Weight 0.95 + cosine 0.65-0.72 lowered to 0.85'
    weight_changes.append(('Strong with low cosine', count))
    print(f"WEIGHT: {count} strong terms (0.95) with cosine 0.65-0.72 -> 0.85")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("COLONIAL SYSTEMS - CURATION SUMMARY")
print("="*80)

colonial_after = df[colonial_mask & (df['decision'] == 'KEEP')]

print(f"\nOriginal: {len(colonial)} terms")
print(f"Removed: {len(colonial) - len(colonial_after)} terms")
print(f"Kept: {len(colonial_after)} terms")
print(f"Weight adjustments: {len(df[colonial_mask & (df['new_weight'] != df['weight'])])} terms")

print("\nRemovals:")
for reason, count in removals:
    print(f"  {reason}: {count}")

print("\nWeight changes:")
for reason, count in weight_changes:
    print(f"  {reason}: {count}")

# Save progress
output_path = 'C:/Users/Home/policy-analysis/workflow_data/slavery_Short-slavdict_pretrained_slavery_v4/Dictionary/curation_progress.csv'
df.to_csv(output_path, index=False)
print(f"\nProgress saved to: {output_path}")
print("\nColonial Systems curation complete!")
