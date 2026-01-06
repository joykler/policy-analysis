import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Load expanded candidates
df_all = pd.read_csv(r'C:\Users\Home\policy-analysis\workflow_Structureddict\slavery_structured-slavdict_pretrained_slavery_v1\Dictionary\expanded_candidates.csv')

# Filter for Raciale_Hierarchie
df = df_all[df_all['topic'] == 'Raciale_Hierarchie'].copy()

print("="*80)
print("RACIALE_HIERARCHIE - CURATION")
print("="*80)

print(f"\nTotal terms: {len(df)}")
print(f"Seeds: {len(df[df['is_seed']==1])}")
print(f"Expanded: {len(df[df['is_seed']==0])}")

print("\nCategory distribution:")
print(df.groupby('category').size())

print("\nWeight distribution:")
print(df.groupby('weight').size().sort_index())

# Add decision columns
df['action'] = 'KEEP'
df['new_category'] = df['category']
df['new_weight'] = df['weight']
df['curation_notes'] = ''

print("\n" + "="*80)
print("PHASE 1: AUTOMATIC REMOVALS")
print("="*80)

# Phase 1 checks
fragments = df['term'].str.len() < 4
low_cosine = df['cosine'] < 0.65
single_df = (df['df'] == 1) & (df['is_seed'] == 0)
zero_df = df['df'] == 0

print(f"Fragments (len<4): {fragments.sum()}")
print(f"Low cosine (<0.65): {low_cosine.sum()}")
print(f"Single df (expanded): {single_df.sum()}")
print(f"Zero df: {zero_df.sum()}")

# Apply Phase 1 removals
if fragments.sum() > 0:
    df.loc[fragments, 'action'] = 'REMOVE'
    df.loc[fragments, 'curation_notes'] = 'Morphological fragment'

if low_cosine.sum() > 0:
    df.loc[low_cosine, 'action'] = 'REMOVE'
    df.loc[low_cosine, 'curation_notes'] = 'Extreme low cosine'

if single_df.sum() > 0:
    df.loc[single_df, 'action'] = 'REMOVE'
    df.loc[single_df, 'curation_notes'] = 'Single document frequency'

print(f"\nPhase 1 removals: {(df['action'] == 'REMOVE').sum()}")

print("\n" + "="*80)
print("TOPIC-SPECIFIC CURATION")
print("="*80)

expanded = df[(df['is_seed'] == 0) & (df['action'] == 'KEEP')].copy()

# Analyze patterns
print(f"\nExpanded terms to review: {len(expanded)}")
print(f"Cosine range: {expanded['cosine'].min():.3f} - {expanded['cosine'].max():.3f}")
print(f"Mean cosine: {expanded['cosine'].mean():.3f}")

# High-expansion parents
parent_counts = expanded.groupby('parent').size().sort_values(ascending=False)
print(f"\nTop 10 parents by expansion:")
print(parent_counts.head(10))

# High df terms
high_df = expanded[expanded['df'] > 200].sort_values('df', ascending=False)
print(f"\nHigh df terms (>200): {len(high_df)}")
if len(high_df) > 0:
    print(high_df[['term', 'category', 'weight', 'df', 'cosine', 'parent']].to_string(index=False))

# Low cosine high weight
suspicious = expanded[(expanded['cosine'] < 0.72) & (expanded['weight'] >= 0.8)]
print(f"\nSuspicious: Low cosine (<0.72) + high weight (>=0.8): {len(suspicious)}")
if len(suspicious) > 0:
    print(suspicious[['term', 'category', 'weight', 'cosine', 'df', 'parent']].head(20).to_string(index=False))

print("\n" + "="*80)
print("APPLYING CURATION RULES")
print("="*80)

# RULE 1: Remove semantic drift - watch for: generic diversity terms, non-racial classification terms

# RULE 2: Ultra-high frequency dampening (df > 300)
ultra_high = (df['df'] > 300) & (df['action'] == 'KEEP')
for idx, row in df[ultra_high].iterrows():
    term = row['term']
    curr_cat = row['category']
    curr_weight = row['weight']

    # Move very generic terms to CONTEXT
    if term in ['mensen', 'personen', 'groepen', 'bevolking', 'cultuur']:
        df.loc[idx, 'action'] = 'RECATEGORIZE'
        df.loc[idx, 'new_category'] = 'CONTEXT'
        df.loc[idx, 'new_weight'] = 0.6
        df.loc[idx, 'curation_notes'] = f'Ultra-high df ({row["df"]}) - too generic, move to CONTEXT'
    elif curr_weight >= 0.8:
        # Dampen weight but keep category
        df.loc[idx, 'action'] = 'REWEIGHT'
        df.loc[idx, 'new_weight'] = max(0.6, curr_weight - 0.2)
        df.loc[idx, 'curation_notes'] = f'Ultra-high df ({row["df"]}) - dampen weight'

print(f"Ultra-high df adjustments: {ultra_high.sum()}")

# RULE 3: Low cosine + BELEID/KERN - validate racial hierarchy specificity
low_cos_policy = (df['cosine'] < 0.72) & (df['category'].isin(['BELEID', 'KERN'])) & (df['action'] == 'KEEP')

# Generic diversity/social terms that aren't racial hierarchy-specific
generic_social = ['diversiteit', 'inclusie', 'gelijkheid', 'verschil', 'classificatie', 'categorie']

for idx, row in df[low_cos_policy].iterrows():
    term = row['term']

    # Check if term is racial hierarchy-specific or just generic social
    if any(gen in term for gen in generic_social) and 'racis' not in term and 'kleur' not in term and 'huidskleur' not in term:
        # Likely too generic
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'curation_notes'] = f'Generic social/diversity term, not racial hierarchy-specific (cosine {row["cosine"]:.3f})'
    elif row['cosine'] < 0.70:
        # Very low cosine - downgrade or remove
        if row['df'] < 5:
            df.loc[idx, 'action'] = 'REMOVE'
            df.loc[idx, 'curation_notes'] = f'Very low cosine ({row["cosine"]:.3f}) + low df'
        else:
            # Downgrade to STERK
            df.loc[idx, 'action'] = 'RECATEGORIZE'
            df.loc[idx, 'new_category'] = 'STERK'
            df.loc[idx, 'new_weight'] = 0.8
            df.loc[idx, 'curation_notes'] = f'Low cosine ({row["cosine"]:.3f}) - downgrade to STERK'

print(f"Low cosine policy term adjustments: {low_cos_policy.sum()}")

# RULE 4: CONTEXT category validation - should be demographic/phenotypic descriptors
context_terms = df[df['category'] == 'CONTEXT']
print(f"\nCONTEXT terms: {len(context_terms)}")
# These should be neutral descriptors (huidskleur, afkomst, etc.)

# RULE 5: Over-expanded parents (>30) - apply stricter review
for parent in parent_counts[parent_counts > 30].index:
    parent_mask = (df['parent'] == parent) & (df['is_seed'] == 0) & (df['action'] == 'KEEP')

    # Apply stricter cosine threshold
    low_cos = (df.loc[parent_mask, 'cosine'] < 0.75)

    for idx in df[parent_mask].index:
        if df.loc[idx, 'cosine'] < 0.75:
            # Stricter threshold for over-expanded parents
            if df.loc[idx, 'df'] < 5:
                df.loc[idx, 'action'] = 'REMOVE'
                df.loc[idx, 'curation_notes'] = f'Over-expanded parent "{parent}" + low cosine/df'
            elif df.loc[idx, 'weight'] > 0.6:
                # Lower weight
                df.loc[idx, 'action'] = 'REWEIGHT'
                df.loc[idx, 'new_weight'] = max(0.6, df.loc[idx, 'weight'] - 0.1)
                df.loc[idx, 'curation_notes'] = f'Over-expanded parent "{parent}" - dampen weight'

high_exp_parents = parent_counts[parent_counts > 30]
print(f"\nOver-expanded parents reviewed: {len(high_exp_parents)}")
if len(high_exp_parents) > 0:
    print(high_exp_parents)

print("\n" + "="*80)
print("CURATION SUMMARY")
print("="*80)

print("\nAction distribution:")
print(df.groupby('action').size())

final_kept = df[df['action'] != 'REMOVE']
print(f"\nFinal dictionary size: {len(final_kept)} (removed {(df['action'] == 'REMOVE').sum()})")

# Category distribution after curation
final_cat_dist = final_kept.groupby('new_category').size()
print(f"\nFinal category distribution:")
print(final_cat_dist)

# Save results
output_file = r'C:\Users\Home\policy-analysis\raciale_hierarchie_curated.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')

final_output = r'C:\Users\Home\policy-analysis\raciale_hierarchie_final.csv'
final_dict = df[df['action'] != 'REMOVE'][['term', 'parent', 'new_category', 'new_weight', 'cosine', 'df', 'curation_notes']].copy()
final_dict.columns = ['term', 'parent', 'category', 'weight', 'cosine', 'df', 'curation_notes']
final_dict.to_csv(final_output, index=False, encoding='utf-8-sig')

print(f"\nFiles saved:")
print(f"  {output_file}")
print(f"  {final_output}")

# Removal reasons
if (df['action'] == 'REMOVE').sum() > 0:
    print("\n" + "="*80)
    print("REMOVAL REASONS")
    print("="*80)
    removed = df[df['action'] == 'REMOVE']
    removal_reasons = removed.groupby('curation_notes').size().sort_values(ascending=False)
    print(removal_reasons)
    print(f"\nTotal removed: {len(removed)}")
