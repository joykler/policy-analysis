"""
Apply Curation for Modern Racism & Discrimination - V4
Expected moderate curation (v3 had 16% removal, mainly from uitbuiting drift)
"""

import pandas as pd

# Load progress
df = pd.read_csv('C:/Users/Home/policy-analysis/workflow_data/slavery_Short-slavdict_pretrained_slavery_v4/Dictionary/curation_progress.csv')

print("="*80)
print("MODERN RACISM & DISCRIMINATION - APPLYING CURATION")
print("="*80)

racism_mask = df['topic'] == 'Modern Racism & Discrimination'
racism = df[racism_mask].copy()
racism_expanded = racism[racism['is_seed'] == 0]

print(f"\nTotal: {len(racism)} terms")
print(f"Expanded: {len(racism_expanded)} terms")

removals = []
weight_changes = []

# ============================================================================
# PHASE 1: AUTOMATIC REMOVALS
# ============================================================================

print("\nPHASE 1: Automatic Removals")

# Low cosine (<0.65)
mask = racism_mask & (df['is_seed'] == 0) & (df['cosine'] < 0.65)
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

# "uitbuiting" (exploitation) morphological drift - uit- prefix false matches
wrong_uitbuiting = [
    'ontheffing', 'onttrekkingen', 'onttrekking', 'uitge-', 'uitstroom', 'uitnodigen',
    'uitlatingen', 'ontslag', 'onttrekken', 'uitbrengen', 'uitbreken', 'uiting',
    'opheffing', 'uitputting', 'uitputtende', 'uitmaken', 'uitbarstingen', 'uitgeloot',
    'uitging', 'uitbraken', 'ontduiking', 'uitsprak', 'voortzetting', 'afbreking',
    'uitstaan', 'bezetting', 'ontheemding', 'aanwas', 'uitroepen', 'ontvoering',
    'uit-', 'ontsporing', 'uitte', 'uitbarsten', 'verwijdering', 'uittocht'
]
mask = racism_mask & (df['term'].isin(wrong_uitbuiting))
count = mask.sum()
if count > 0:
    df.loc[mask, 'decision'] = 'REMOVE'
    df.loc[mask, 'reason'] = 'Semantic drift - uitbuiting morphological false matches'
    removals.append(('Uitbuiting drift', count))
    print(f"  Uitbuiting morphological drift: {count} removed")

# "ongelijkheid" (inequality) morphological fragments
wrong_ongelijkheid = ['zedelijkheid', 'onmenselijkheid', 'selijkheid']
mask = racism_mask & (df['term'].isin(wrong_ongelijkheid))
count = mask.sum()
if count > 0:
    df.loc[mask, 'decision'] = 'REMOVE'
    df.loc[mask, 'reason'] = 'Semantic drift - ongelijkheid morphological fragments'
    removals.append(('Ongelijkheid fragments', count))
    print(f"  Ongelijkheid fragments: {count} removed")

# "structureel" (structural) wrong expansions
wrong_structureel = ['turele', 'development', 'concrete']
mask = racism_mask & (df['term'].isin(wrong_structureel))
count = mask.sum()
if count > 0:
    df.loc[mask, 'decision'] = 'REMOVE'
    df.loc[mask, 'reason'] = 'Semantic drift - structureel wrong expansion'
    removals.append(('Structureel drift', count))
    print(f"  Structureel wrong expansions: {count} removed")

# "segregatie" (segregation) overly broad
wrong_segregatie = ['opsplitsing', 'samenvoeging', 'herverdeling', 'omzetting', 'uitsplitsing', 'generaties']
mask = racism_mask & (df['term'].isin(wrong_segregatie))
count = mask.sum()
if count > 0:
    df.loc[mask, 'decision'] = 'REMOVE'
    df.loc[mask, 'reason'] = 'Semantic drift - segregatie too broad'
    removals.append(('Segregatie drift', count))
    print(f"  Segregatie overgeneralization: {count} removed")

# "constructief" from "structureel" - wrong meaning
mask = racism_mask & (df['term'] == 'constructief')
count = mask.sum()
if count > 0:
    df.loc[mask, 'decision'] = 'REMOVE'
    df.loc[mask, 'reason'] = 'Semantic drift - wrong meaning'
    removals.append(('Constructief wrong meaning', count))
    print(f"  Constructief: {count} removed")

# ============================================================================
# PHASE 3: WEIGHT CALIBRATION
# ============================================================================

print("\nPHASE 3: Weight Calibration")

# Core (1.00) + medium cosine (0.65-0.75)
mask = racism_mask & (df['is_seed'] == 0) & (df['weight'] == 1.00) & (df['cosine'] >= 0.65) & (df['cosine'] < 0.75) & (df['decision'] == 'KEEP')
count = mask.sum()
if count > 0:
    df.loc[mask, 'new_weight'] = 0.90
    df.loc[mask, 'reason'] = 'Core (1.00) + cosine 0.65-0.75 -> 0.90'
    weight_changes.append(('Core medium cosine', count))
    print(f"  Core with medium cosine: {count} terms 1.00 -> 0.90")

# Strong (0.95) + low cosine (0.65-0.72)
mask = racism_mask & (df['is_seed'] == 0) & (df['weight'] == 0.95) & (df['cosine'] >= 0.65) & (df['cosine'] < 0.72) & (df['decision'] == 'KEEP')
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
print("MODERN RACISM & DISCRIMINATION - CURATION SUMMARY")
print("="*80)

racism_after = df[racism_mask & (df['decision'] == 'KEEP')]

print(f"\nOriginal: {len(racism)} terms")
print(f"Removed: {len(racism) - len(racism_after)} terms ({(len(racism) - len(racism_after))/len(racism)*100:.1f}%)")
print(f"Kept: {len(racism_after)} terms")
print(f"Weight adjustments: {len(df[racism_mask & (df['new_weight'] != df['weight'])])} terms")

if removals:
    print("\nRemovals:")
    total_removed = 0
    for reason, count in removals:
        print(f"  {reason}: {count}")
        total_removed += count
    print(f"  TOTAL: {total_removed}")

if weight_changes:
    print("\nWeight changes:")
    for reason, count in weight_changes:
        print(f"  {reason}: {count}")

# Save progress
output_path = 'C:/Users/Home/policy-analysis/workflow_data/slavery_Short-slavdict_pretrained_slavery_v4/Dictionary/curation_progress.csv'
df.to_csv(output_path, index=False)
print(f"\nProgress saved to: {output_path}")
print("\nModern Racism & Discrimination curation complete!")
