"""
Apply Manual Curation Decisions (Phases 2-5)
Based on analysis in curation_analysis.txt
"""

import pandas as pd
import re

# Load expanded dictionary
df = pd.read_csv('C:/Users/Home/policy-analysis/workflow_data/slavery_Short-slavdict_pretrained_slavery_v3/Dictionary/expanded_candidates.csv')

# Initialize curation columns
df['decision'] = 'KEEP'
df['reason'] = ''
df['new_weight'] = df['weight']
df['new_category'] = df['category']

# Track statistics
removals = []
weight_changes = []
category_changes = []

print("APPLYING MANUAL CURATION DECISIONS")
print("="*80)

# ============================================================================
# PHASE 1: AUTOMATIC REMOVALS
# ============================================================================

# 1. Low cosine
mask = (df['is_seed'] == 0) & (df['cosine'] < 0.65)
count = mask.sum()
df.loc[mask, 'decision'] = 'REMOVE'
df.loc[mask, 'reason'] = 'Phase1: cosine < 0.65'
removals.append(('Low cosine (<0.65)', count))
print(f"Phase 1 - Low cosine: {count} removed")

# 2. Morphological fragments (short + clearly fragments)
fragments_to_remove = ['cn', 'kou', 'na-', 'zoo', 'eis']  # not 'mei' (May is valid), not 'wit' (white is valid)
mask = df['term'].isin(fragments_to_remove)
count = mask.sum()
df.loc[mask, 'decision'] = 'REMOVE'
df.loc[mask, 'reason'] = 'Phase1: morphological fragment'
removals.append(('Morphological fragments', count))
print(f"Phase 1 - Fragments: {count} removed")

# ============================================================================
# PHASE 2: SEMANTIC DRIFT (by topic patterns)
# ============================================================================

print("\nPhase 2 - Semantic Drift Detection")

# HERITAGE & MEMORY: Month names are semantic drift from "1 juli"
month_names = ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december']
mask = (df['topic'] == 'Heritage & Memory') & (df['term'].isin(month_names)) & (df['is_seed'] == 0)
count = mask.sum()
df.loc[mask, 'decision'] = 'REMOVE'
df.loc[mask, 'reason'] = 'Phase2: semantic drift - month names'
removals.append(('Heritage - month names', count))
print(f"  Heritage & Memory - Month names: {count} removed")

# HERITAGE & MEMORY: Wrong meaning expansions from "herdenking" (commemoration)
wrong_herdenking = ['aanbidding', 'bewondering', 'beschuldiging', 'gezag', 'beschouwing', 'rede', 'stiltes', 'heiligen', 'opofferingen', 'beschouwingen']
mask = (df['topic'] == 'Heritage & Memory') & (df['term'].isin(wrong_herdenking))
count = mask.sum()
df.loc[mask, 'decision'] = 'REMOVE'
df.loc[mask, 'reason'] = 'Phase2: semantic drift - wrong meaning'
removals.append(('Heritage - herdenking drift', count))
print(f"  Heritage & Memory - Wrong herdenking meanings: {count} removed")

# HERITAGE & MEMORY: Wrong expansions from "keti koti"
wrong_ketikoti = ['kofi', 'kauri', 'kapuweri', 'khoikhoi', 'kumi']  # These look like unrelated terms
mask = (df['topic'] == 'Heritage & Memory') & (df['term'].isin(wrong_ketikoti))
count = mask.sum()
df.loc[mask, 'decision'] = 'REMOVE'
df.loc[mask, 'reason'] = 'Phase2: semantic drift - wrong keti koti expansion'
removals.append(('Heritage - keti koti drift', count))
print(f"  Heritage & Memory - Wrong keti koti expansions: {count} removed")

# MODERN RACISM: "uitbuiting" (exploitation) generated many wrong terms
# "uitbuiting" has morphological similarity to "uit-" prefix words but wrong semantics
wrong_uitbuiting = [
    'ontheffing', 'onttrekkingen', 'onttrekking', 'uitge-', 'uitstroom', 'uitnodigen',
    'uitlatingen', 'ontslag', 'onttrekken', 'uitbrengen', 'uitbreken', 'uiting',
    'opheffing', 'uitputting', 'uitputtende', 'uitmaken', 'uitbarstingen', 'uitgeloot',
    'uitging', 'uitbraken', 'ontduiking', 'uitsprak', 'voortzetting', 'afbreking',
    'uitstaan', 'bezetting', 'ontheemding', 'aanwas', 'uitroepen', 'ontvoering',
    'uit-', 'ontsporing', 'uitte', 'uitbarsten', 'verwijdering', 'uittocht'
]
mask = (df['topic'] == 'Modern Racism & Discrimination') & (df['term'].isin(wrong_uitbuiting))
count = mask.sum()
df.loc[mask, 'decision'] = 'REMOVE'
df.loc[mask, 'reason'] = 'Phase2: semantic drift - uitbuiting morphological false matches'
removals.append(('Modern Racism - uitbuiting drift', count))
print(f"  Modern Racism - Uitbuiting drift: {count} removed")

# MODERN RACISM: "ongelijkheid" (inequality) morphological fragments
wrong_ongelijkheid = ['zedelijkheid', 'onmenselijkheid', 'selijkheid']
mask = (df['topic'] == 'Modern Racism & Discrimination') & (df['term'].isin(wrong_ongelijkheid))
count = mask.sum()
df.loc[mask, 'decision'] = 'REMOVE'
df.loc[mask, 'reason'] = 'Phase2: semantic drift - ongelijkheid morphological fragments'
removals.append(('Modern Racism - ongelijkheid fragments', count))
print(f"  Modern Racism - Ongelijkheid fragments: {count} removed")

# MODERN RACISM: "structureel" (structural) wrong expansions
wrong_structureel = ['turele', 'development', 'concrete']  # 'infrastructurele' might be valid
mask = (df['topic'] == 'Modern Racism & Discrimination') & (df['term'].isin(wrong_structureel))
count = mask.sum()
df.loc[mask, 'decision'] = 'REMOVE'
df.loc[mask, 'reason'] = 'Phase2: semantic drift - structureel wrong expansion'
removals.append(('Modern Racism - structureel drift', count))
print(f"  Modern Racism - Structureel drift: {count} removed")

# MODERN RACISM: "segregatie" (segregation) overly broad expansions
wrong_segregatie = ['opsplitsing', 'samenvoeging', 'herverdeling', 'omzetting', 'uitsplitsing', 'generaties']
mask = (df['topic'] == 'Modern Racism & Discrimination') & (df['term'].isin(wrong_segregatie))
count = mask.sum()
df.loc[mask, 'decision'] = 'REMOVE'
df.loc[mask, 'reason'] = 'Phase2: semantic drift - segregatie too broad'
removals.append(('Modern Racism - segregatie drift', count))
print(f"  Modern Racism - Segregatie drift: {count} removed")

# COLONIAL SYSTEMS: Colonial-era specific terms that seem correct but low cosine
# Keep these as they're domain-specific and semantically correct, just lower weight

# ============================================================================
# PHASE 3: OVERGENERALIZATION
# ============================================================================

print("\nPhase 3 - Overgeneralization Control")

# High frequency geographic marker "nederland" - lower weight
mask = (df['term'] == 'nederland')
count = mask.sum()
df.loc[mask, 'new_weight'] = 0.35  # Lower from 0.50
df.loc[mask, 'reason'] = 'Phase3: high df (967) - lowered weight'
weight_changes.append(('nederland - too frequent', count))
print(f"  'nederland' (df=967): weight lowered to 0.35 ({count} instances)")

# High frequency "caribisch" - already at 0.50, keep as is (it's important marker)
print(f"  'caribisch' (df=340): keeping at 0.50 (important geographic marker)")

# "koloniale" at core_problem with df=524 - this is actually important, but lower slightly
mask = (df['term'] == 'koloniale')
count = mask.sum()
df.loc[mask, 'new_weight'] = 0.90  # Lower from 1.00 due to high frequency
df.loc[mask, 'reason'] = 'Phase3: high df (524) - lowered from 1.00 to 0.90'
weight_changes.append(('koloniale - high df adjustment', count))
print(f"  'koloniale' (df=524): weight lowered to 0.90 ({count} instances)")

# Generic "arbeid" (labor) from "dwangarbeid" (forced labor) - too generic
mask = (df['topic'] == 'Historical Slavery') & (df['term'] == 'arbeid')
count = mask.sum()
df.loc[mask, 'decision'] = 'REMOVE'
df.loc[mask, 'reason'] = 'Phase3: overgeneralization - arbeid too generic'
removals.append(('Historical Slavery - arbeid too generic', count))
print(f"  Historical Slavery - 'arbeid' too generic: {count} removed")

# Generic "tuin" (garden) from "plantage" - wrong semantic space
mask = (df['term'] == 'tuin')
count = mask.sum()
df.loc[mask, 'decision'] = 'REMOVE'
df.loc[mask, 'reason'] = 'Phase3: semantic drift - tuin means garden not plantation'
removals.append(('Colonial - tuin semantic drift', count))
print(f"  Colonial Systems - 'tuin' (garden): {count} removed")

# ============================================================================
# PHASE 4: CATEGORY CORRECTIONS
# ============================================================================

print("\nPhase 4 - Category Corrections")

# "datum" (date) from "1 juli" - should be removed, not recategorized
mask = (df['term'] == 'datum')
count = mask.sum()
df.loc[mask, 'decision'] = 'REMOVE'
df.loc[mask, 'reason'] = 'Phase4: too generic'
removals.append(('Heritage - datum too generic', count))
print(f"  Heritage & Memory - 'datum' removed: {count}")

# "intrede" (entry/entrance) from "herdenking" - wrong meaning
mask = (df['term'] == 'intrede')
count = mask.sum()
df.loc[mask, 'decision'] = 'REMOVE'
df.loc[mask, 'reason'] = 'Phase4: wrong semantic meaning'
removals.append(('Heritage - intrede wrong meaning', count))
print(f"  Heritage & Memory - 'intrede' removed: {count}")

# ============================================================================
# PHASE 5: WEIGHT CALIBRATION
# ============================================================================

print("\nPhase 5 - Weight Calibration")

# High weight (1.00) + medium-low cosine (0.65-0.75) - lower by 0.10-0.15
mask = (df['is_seed'] == 0) & (df['weight'] == 1.00) & (df['cosine'] >= 0.65) & (df['cosine'] < 0.75) & (df['decision'] == 'KEEP')
count = mask.sum()
df.loc[mask, 'new_weight'] = 0.90
df.loc[mask, 'reason'] = 'Phase5: weight 1.00 + cosine 0.65-0.75 lowered to 0.90'
weight_changes.append(('Core terms with medium cosine', count))
print(f"  Core problem (1.00) with cosine 0.65-0.75: {count} lowered to 0.90")

# High weight (0.95) + low cosine (0.65-0.72) - lower by 0.10
mask = (df['is_seed'] == 0) & (df['weight'] == 0.95) & (df['cosine'] >= 0.65) & (df['cosine'] < 0.72) & (df['decision'] == 'KEEP')
count = mask.sum()
df.loc[mask, 'new_weight'] = 0.85
df.loc[mask, 'reason'] = 'Phase5: weight 0.95 + cosine 0.65-0.72 lowered to 0.85'
weight_changes.append(('Strong problem with low cosine', count))
print(f"  Strong problem (0.95) with cosine 0.65-0.72: {count} lowered to 0.85")

# ============================================================================
# SAVE CURATED DICTIONARY
# ============================================================================

# Filter to KEEP decisions
curated_df = df[df['decision'] == 'KEEP'].copy()

# Update weight and category columns
curated_df['weight'] = curated_df['new_weight']
curated_df['category'] = curated_df['new_category']

# Select relevant columns
output_df = curated_df[['topic', 'term', 'cosine', 'df', 'weight', 'category', 'parent', 'is_seed']]

# Save curated dictionary
output_path = 'C:/Users/Home/policy-analysis/workflow_data/slavery_Short-slavdict_pretrained_slavery_v3/Dictionary/curated_dictionary.csv'
output_df.to_csv(output_path, index=False)

print("\n" + "="*80)
print("CURATION SUMMARY")
print("="*80)

print(f"\nOriginal terms: {len(df)}")
print(f"Removed: {len(df[df['decision'] == 'REMOVE'])}")
print(f"Kept: {len(curated_df)}")
print(f"Weight adjustments: {len(df[df['new_weight'] != df['weight']])}")

print("\n--- Removals by Category ---")
for reason, count in removals:
    print(f"  {reason}: {count}")

print("\n--- Weight Adjustments ---")
for reason, count in weight_changes:
    print(f"  {reason}: {count}")

print("\n--- Per-Topic Statistics ---")
for topic in df['topic'].unique():
    original = len(df[df['topic'] == topic])
    removed = len(df[(df['topic'] == topic) & (df['decision'] == 'REMOVE')])
    kept = len(curated_df[curated_df['topic'] == topic])
    print(f"\n{topic}:")
    print(f"  Original: {original}")
    print(f"  Removed: {removed} ({removed/original*100:.1f}%)")
    print(f"  Kept: {kept} ({kept/original*100:.1f}%)")

print(f"\n\nCurated dictionary saved to:")
print(output_path)

# Save full curation log
curation_log = df[['topic', 'term', 'parent', 'cosine', 'df', 'weight', 'new_weight', 'category', 'decision', 'reason', 'is_seed']]
log_path = 'C:/Users/Home/policy-analysis/workflow_data/slavery_Short-slavdict_pretrained_slavery_v3/Dictionary/curation_log.csv'
curation_log.to_csv(log_path, index=False, encoding='utf-8-sig')
print(f"\nFull curation log saved to:")
print(log_path)
