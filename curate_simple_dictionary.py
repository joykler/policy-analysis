"""
Dictionary Curation Script for Simple Slavery Topics
Follows methodology from A__DICTIONARY_CURATION_GUIDE.md
"""

import pandas as pd
import json

# Load expanded dictionary
df = pd.read_csv('C:/Users/Home/policy-analysis/workflow_data/slavery_Short-slavdict_pretrained_slavery_v3/Dictionary/expanded_candidates.csv')

# Add curation decision columns
df['decision'] = 'KEEP'  # Default
df['reason'] = ''

# Curation statistics
stats = {
    'automatic_removals': {},
    'manual_removals': {},
    'weight_adjustments': {},
    'category_changes': {}
}

print("="*80)
print("DICTIONARY CURATION - SIMPLE SLAVERY TOPICS")
print("="*80)
print(f"\nTotal terms: {len(df)}")
print(f"Topics: {df['topic'].unique()}")
print(f"Seed terms: {df['is_seed'].sum()}")
print(f"Expanded terms: {len(df[df['is_seed']==0])}")

# ============================================================================
# PHASE 1: AUTOMATIC REMOVAL (Technical Errors)
# ============================================================================

print("\n" + "="*80)
print("PHASE 1: AUTOMATIC REMOVAL")
print("="*80)

# 1. Extreme low similarity
low_cosine = df[(df['is_seed'] == 0) & (df['cosine'] < 0.65)]
df.loc[low_cosine.index, 'decision'] = 'REMOVE'
df.loc[low_cosine.index, 'reason'] = 'cosine < 0.65 (too distant)'
print(f"\n1. Low cosine (<0.65): {len(low_cosine)} terms")
stats['automatic_removals']['low_cosine'] = len(low_cosine)

# 2. Single document frequency
single_df = df[(df['is_seed'] == 0) & (df['df'] == 1)]
df.loc[single_df.index, 'decision'] = 'REMOVE'
df.loc[single_df.index, 'reason'] = 'df == 1 (single occurrence)'
print(f"2. Single document frequency: {len(single_df)} terms")
stats['automatic_removals']['single_df'] = len(single_df)

# 3. Morphological fragments (very short + not seed)
fragments = df[(df['is_seed'] == 0) & (df['term'].str.len() < 4)]
# Review these manually - some might be valid (e.g., "wic")
print(f"3. Short terms (<4 chars): {len(fragments)} terms (need manual review)")
print(fragments[['topic', 'term', 'parent', 'cosine']].to_string(index=False))

# 4. Encoding errors (look for special characters that seem broken)
# Manual inspection needed - flagging suspicious patterns
suspicious = df[(df['is_seed'] == 0) & (df['term'].str.contains('\ufffd', na=False))]
print(f"\n4. Encoding issues (replacement char): {len(suspicious)} terms")
if len(suspicious) > 0:
    print(suspicious[['topic', 'term', 'parent']].to_string(index=False))

print(f"\nAutomatic removals total: {len(df[df['decision']=='REMOVE'])}")

# ============================================================================
# PHASE 2-5: TOPIC-BY-TOPIC MANUAL CURATION
# ============================================================================

print("\n" + "="*80)
print("PHASE 2-5: TOPIC-BY-TOPIC ANALYSIS")
print("="*80)

for topic in df['topic'].unique():
    print(f"\n{'='*80}")
    print(f"TOPIC: {topic}")
    print(f"{'='*80}")

    topic_df = df[df['topic'] == topic].copy()
    expanded = topic_df[topic_df['is_seed'] == 0].copy()

    print(f"\nTotal terms: {len(topic_df)}")
    print(f"Seed: {len(topic_df[topic_df['is_seed']==1])}")
    print(f"Expanded: {len(expanded)}")
    print(f"Already marked for removal: {len(topic_df[topic_df['decision']=='REMOVE'])}")

    # High priority review flags
    print(f"\n--- HIGH PRIORITY REVIEW FLAGS ---")

    # High weight + low cosine
    high_weight_low_cosine = expanded[(expanded['weight'] >= 0.95) & (expanded['cosine'] < 0.75)]
    print(f"High weight (>=0.95) + low cosine (<0.75): {len(high_weight_low_cosine)}")
    if len(high_weight_low_cosine) > 0:
        print(high_weight_low_cosine[['term', 'cosine', 'weight', 'parent', 'category']].to_string(index=False))

    # High document frequency
    high_df = expanded[expanded['df'] > 300]
    print(f"\nHigh document frequency (>300): {len(high_df)}")
    if len(high_df) > 0:
        print(high_df[['term', 'df', 'weight', 'category']].sort_values('df', ascending=False).to_string(index=False))

    # Medium cosine range (0.65-0.75) - manual review needed
    medium_cosine = expanded[(expanded['cosine'] >= 0.65) & (expanded['cosine'] < 0.75) & (expanded['decision'] != 'REMOVE')]
    print(f"\nMedium cosine (0.65-0.75) needing manual review: {len(medium_cosine)}")
    if len(medium_cosine) > 0:
        print("Top 20 by weight:")
        print(medium_cosine.sort_values('weight', ascending=False)[['term', 'cosine', 'weight', 'parent', 'category']].head(20).to_string(index=False))

    # Parent analysis - who generated most expansions?
    print(f"\n--- PARENT EXPANSION ANALYSIS ---")
    parent_counts = expanded['parent'].value_counts()
    high_expansion_parents = parent_counts[parent_counts > 20]
    if len(high_expansion_parents) > 0:
        print(f"Parents with >20 expansions (need quality control):")
        print(high_expansion_parents.to_string())

print("\n" + "="*80)
print("CURATION ANALYSIS COMPLETE")
print("="*80)
print("\nNext steps:")
print("1. Review flagged terms manually")
print("2. Apply semantic drift detection (Phase 2)")
print("3. Check for overgeneralization (Phase 3)")
print("4. Verify category assignments (Phase 4)")
print("5. Calibrate weights (Phase 5)")
print("\nThis script has completed automatic Phase 1 removals.")
print("Manual review needed for semantic quality.")
