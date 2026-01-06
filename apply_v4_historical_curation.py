"""
Apply Curation for Historical Slavery - V4
Expected to be high quality based on v3 (only 0.3% removal)
"""

import pandas as pd

# Load progress
df = pd.read_csv('C:/Users/Home/policy-analysis/workflow_data/slavery_Short-slavdict_pretrained_slavery_v4/Dictionary/curation_progress.csv')

print("="*80)
print("HISTORICAL SLAVERY - APPLYING CURATION")
print("="*80)

historical_mask = df['topic'] == 'Historical Slavery'
historical = df[historical_mask].copy()
historical_expanded = historical[historical['is_seed'] == 0]

print(f"\nTotal: {len(historical)} terms")
print(f"Expanded: {len(historical_expanded)} terms")

removals = []
weight_changes = []

# ============================================================================
# PHASE 1: AUTOMATIC REMOVALS
# ============================================================================

print("\nPHASE 1: Automatic Removals")

# Low cosine (<0.65)
mask = historical_mask & (df['is_seed'] == 0) & (df['cosine'] < 0.65)
count = mask.sum()
if count > 0:
    df.loc[mask, 'decision'] = 'REMOVE'
    df.loc[mask, 'reason'] = 'Low cosine (<0.65)'
    removals.append(('Low cosine', count))
    print(f"  Low cosine: {count} removed")

# ============================================================================
# PHASE 2: SEMANTIC DRIFT
# ============================================================================

print("\nPHASE 2: Semantic Drift Detection")

# Generic "arbeid" (labor) from "dwangarbeid" (forced labor)
mask = historical_mask & (df['term'] == 'arbeid')
count = mask.sum()
if count > 0:
    df.loc[mask, 'decision'] = 'REMOVE'
    df.loc[mask, 'reason'] = 'Overgeneralization - arbeid too generic'
    removals.append(('Arbeid too generic', count))
    print(f"  Arbeid (labor): {count} removed - too generic")

# ============================================================================
# PHASE 3: WEIGHT CALIBRATION
# ============================================================================

print("\nPHASE 3: Weight Calibration")

# High df "slaaf" if present
mask = historical_mask & (df['term'] == 'slaaf') & (df['df'] > 300)
if mask.sum() > 0:
    original_weight = df.loc[mask, 'weight'].iloc[0]
    df.loc[mask, 'new_weight'] = max(0.85, original_weight - 0.10)
    df.loc[mask, 'reason'] = f'High df - lowered from {original_weight}'
    weight_changes.append(('slaaf high df', mask.sum()))
    print(f"  slaaf: high df adjustment")

# Core (1.00) + medium cosine (0.65-0.75)
mask = historical_mask & (df['is_seed'] == 0) & (df['weight'] == 1.00) & (df['cosine'] >= 0.65) & (df['cosine'] < 0.75) & (df['decision'] == 'KEEP')
count = mask.sum()
if count > 0:
    df.loc[mask, 'new_weight'] = 0.90
    df.loc[mask, 'reason'] = 'Core (1.00) + cosine 0.65-0.75 -> 0.90'
    weight_changes.append(('Core medium cosine', count))
    print(f"  Core with medium cosine: {count} terms 1.00 -> 0.90")

# Strong (0.95) + low cosine (0.65-0.72)
mask = historical_mask & (df['is_seed'] == 0) & (df['weight'] == 0.95) & (df['cosine'] >= 0.65) & (df['cosine'] < 0.72) & (df['decision'] == 'KEEP')
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
print("HISTORICAL SLAVERY - CURATION SUMMARY")
print("="*80)

historical_after = df[historical_mask & (df['decision'] == 'KEEP')]

print(f"\nOriginal: {len(historical)} terms")
print(f"Removed: {len(historical) - len(historical_after)} terms ({(len(historical) - len(historical_after))/len(historical)*100:.1f}%)")
print(f"Kept: {len(historical_after)} terms")
print(f"Weight adjustments: {len(df[historical_mask & (df['new_weight'] != df['weight'])])} terms")

if removals:
    print("\nRemovals:")
    for reason, count in removals:
        print(f"  {reason}: {count}")

if weight_changes:
    print("\nWeight changes:")
    for reason, count in weight_changes:
        print(f"  {reason}: {count}")

# Save progress
output_path = 'C:/Users/Home/policy-analysis/workflow_data/slavery_Short-slavdict_pretrained_slavery_v4/Dictionary/curation_progress.csv'
df.to_csv(output_path, index=False)
print(f"\nProgress saved to: {output_path}")
print("\nHistorical Slavery curation complete!")
