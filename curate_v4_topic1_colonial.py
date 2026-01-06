"""
Curate Colonial Systems Topic - V4 Dictionary
Topic-by-topic approach
"""

import pandas as pd

# Load full dictionary
df = pd.read_csv('C:/Users/Home/policy-analysis/workflow_data/slavery_Short-slavdict_pretrained_slavery_v4/Dictionary/expanded_candidates.csv')

# Initialize curation columns if not present
if 'decision' not in df.columns:
    df['decision'] = 'KEEP'
    df['reason'] = ''
    df['new_weight'] = df['weight']
    df['new_category'] = df['category']

print("="*80)
print("COLONIAL SYSTEMS - DETAILED CURATION")
print("="*80)

# Filter to Colonial Systems only
colonial = df[df['topic'] == 'Colonial Systems'].copy()
colonial_expanded = colonial[colonial['is_seed'] == 0].copy()

print(f"\nTotal terms: {len(colonial)}")
print(f"Seed: {colonial['is_seed'].sum()}")
print(f"Expanded: {len(colonial_expanded)}")

# ============================================================================
# PHASE 1: AUTOMATIC REMOVAL
# ============================================================================

print("\n" + "="*80)
print("PHASE 1: AUTOMATIC REMOVAL")
print("="*80)

# 1. Low cosine
low_cosine = colonial_expanded[colonial_expanded['cosine'] < 0.65]
print(f"\n1. Low cosine (<0.65): {len(low_cosine)} terms")
if len(low_cosine) > 0:
    print(low_cosine[['term', 'cosine', 'parent', 'df']].sort_values('cosine').to_string(index=False))

# 2. Single document frequency
single_df = colonial_expanded[colonial_expanded['df'] == 1]
print(f"\n2. Single document frequency: {len(single_df)} terms")
if len(single_df) > 0:
    print(single_df[['term', 'parent', 'cosine']].head(10).to_string(index=False))

# 3. Short terms (potential fragments)
short_terms = colonial_expanded[colonial_expanded['term'].str.len() < 4]
print(f"\n3. Short terms (<4 chars): {len(short_terms)} terms")
if len(short_terms) > 0:
    print(short_terms[['term', 'parent', 'cosine', 'df']].to_string(index=False))

# ============================================================================
# PHASE 2: SEMANTIC DRIFT DETECTION
# ============================================================================

print("\n" + "="*80)
print("PHASE 2: SEMANTIC DRIFT DETECTION")
print("="*80)

# High priority: High weight + low cosine
high_weight_low_cosine = colonial_expanded[(colonial_expanded['weight'] >= 0.95) & (colonial_expanded['cosine'] < 0.75)]
print(f"\nHigh weight (>=0.95) + low cosine (<0.75): {len(high_weight_low_cosine)} terms")
if len(high_weight_low_cosine) > 0:
    print(high_weight_low_cosine[['term', 'cosine', 'weight', 'parent', 'category']].sort_values('cosine').to_string(index=False))

# Medium cosine range - needs review
medium_cosine = colonial_expanded[(colonial_expanded['cosine'] >= 0.65) & (colonial_expanded['cosine'] < 0.75)]
print(f"\nMedium cosine (0.65-0.75): {len(medium_cosine)} terms (showing top 30 by weight)")
if len(medium_cosine) > 0:
    print(medium_cosine.sort_values('weight', ascending=False)[['term', 'cosine', 'weight', 'parent']].head(30).to_string(index=False))

# ============================================================================
# PHASE 3: OVERGENERALIZATION
# ============================================================================

print("\n" + "="*80)
print("PHASE 3: OVERGENERALIZATION CONTROL")
print("="*80)

# High document frequency
high_df = colonial_expanded[colonial_expanded['df'] > 300]
print(f"\nHigh document frequency (>300): {len(high_df)} terms")
if len(high_df) > 0:
    print(high_df[['term', 'df', 'weight', 'category', 'parent']].sort_values('df', ascending=False).to_string(index=False))

# Ultra-high df (>500)
ultra_high_df = colonial_expanded[colonial_expanded['df'] > 500]
print(f"\nUltra-high document frequency (>500): {len(ultra_high_df)} terms")
if len(ultra_high_df) > 0:
    print(ultra_high_df[['term', 'df', 'weight']].to_string(index=False))

# ============================================================================
# PARENT ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("PARENT EXPANSION ANALYSIS")
print("="*80)

parent_counts = colonial_expanded['parent'].value_counts()
high_expansion = parent_counts[parent_counts > 20]
print(f"\nParents with >20 expansions:")
print(high_expansion.to_string())

# Show sample from highest expansion parent
if len(high_expansion) > 0:
    top_parent = high_expansion.index[0]
    print(f"\nSample from '{top_parent}' ({high_expansion.iloc[0]} expansions):")
    parent_terms = colonial_expanded[colonial_expanded['parent'] == top_parent].sort_values('cosine', ascending=False)
    print(parent_terms[['term', 'cosine', 'weight', 'df']].head(15).to_string(index=False))

# ============================================================================
# WEIGHT & CATEGORY DISTRIBUTION
# ============================================================================

print("\n" + "="*80)
print("WEIGHT & CATEGORY DISTRIBUTION")
print("="*80)

print("\nWeight distribution:")
print(colonial['weight'].value_counts().sort_index(ascending=False).to_string())

print("\nCategory distribution:")
print(colonial['category'].value_counts().to_string())

# ============================================================================
# RECOMMENDATIONS
# ============================================================================

print("\n" + "="*80)
print("CURATION RECOMMENDATIONS")
print("="*80)

print("\nAUTOMATIC REMOVALS:")
print(f"  - Low cosine (<0.65): {len(low_cosine)} terms")
print(f"  - Single df: {len(single_df)} terms")

print("\nMANUAL REVIEW NEEDED:")
print(f"  - High weight + low cosine: {len(high_weight_low_cosine)} terms")
print(f"  - Medium cosine range: {len(medium_cosine)} terms")
print(f"  - High df terms: {len(high_df)} terms")
print(f"  - Short terms: {len(short_terms)} terms")

print("\nWEIGHT ADJUSTMENTS RECOMMENDED:")
print(f"  - High df (>300) should have weight lowered")
print(f"  - Core (1.00) with cosine 0.65-0.75 → lower to 0.90")
print(f"  - Strong (0.95) with cosine 0.65-0.72 → lower to 0.85")

print("\n" + "="*80)
print("Review complete. Ready for manual curation decisions.")
print("="*80)
