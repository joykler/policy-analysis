import pandas as pd
import numpy as np

# Load expanded candidates
df = pd.read_csv(r'C:\Users\Home\policy-analysis\workflow_Structureddict\slavery_structured-slavdict_pretrained_slavery_v1\Dictionary\expanded_candidates.csv')

# Filter for Slavernij_Historisch
topic_df = df[df['topic'] == 'Slavernij_Historisch'].copy()

print("="*80)
print("SLAVERNIJ_HISTORISCH - CURATION ANALYSIS")
print("="*80)

print(f"\nTotal terms: {len(topic_df)}")
print(f"Seeds: {len(topic_df[topic_df['is_seed']==1])}")
print(f"Expanded: {len(topic_df[topic_df['is_seed']==0])}")

print("\n" + "="*80)
print("PHASE 1: AUTOMATIC REMOVAL CANDIDATES")
print("="*80)

# Phase 1.1: Morphological fragments (len < 4)
fragments = topic_df[topic_df['term'].str.len() < 4]
print(f"\n1.1 Morphological fragments (len < 4): {len(fragments)}")
if len(fragments) > 0:
    print(fragments[['term', 'parent', 'cosine', 'df']].to_string(index=False))

# Phase 1.2: Extreme low similarity (cosine < 0.65)
low_cosine = topic_df[topic_df['cosine'] < 0.65]
print(f"\n1.2 Extreme low cosine (<0.65): {len(low_cosine)}")
if len(low_cosine) > 0:
    print(low_cosine[['term', 'parent', 'cosine', 'df']].head(10).to_string(index=False))

# Phase 1.3: Single document frequency
single_df = topic_df[(topic_df['df'] == 1) & (topic_df['is_seed'] == 0)]
print(f"\n1.3 Single document frequency (df=1, expanded only): {len(single_df)}")
if len(single_df) > 0:
    print(single_df[['term', 'parent', 'cosine', 'df']].head(10).to_string(index=False))

# Phase 1.4: Zero document frequency (not in corpus - shouldn't exist but check)
zero_df = topic_df[topic_df['df'] == 0]
print(f"\n1.4 Zero document frequency (df=0): {len(zero_df)}")
if len(zero_df) > 0:
    print(zero_df[['term', 'parent', 'cosine', 'df']].to_string(index=False))

print("\n" + "="*80)
print("CATEGORY & WEIGHT DISTRIBUTION")
print("="*80)

print("\nBy category:")
print(topic_df.groupby('category').size().sort_values(ascending=False))

print("\nBy weight:")
print(topic_df.groupby('weight').size().sort_index())

print("\nBy category and weight:")
cat_weight = topic_df.groupby(['category', 'weight']).size().reset_index(name='count')
print(cat_weight.to_string(index=False))

print("\n" + "="*80)
print("HIGH-FREQUENCY TERMS (df > 200)")
print("="*80)
high_freq = topic_df[topic_df['df'] > 200].sort_values('df', ascending=False)
print(f"\nCount: {len(high_freq)}")
if len(high_freq) > 0:
    print(high_freq[['term', 'category', 'weight', 'df', 'cosine', 'parent']].to_string(index=False))

print("\n" + "="*80)
print("EXPANDED TERMS ANALYSIS")
print("="*80)

expanded = topic_df[topic_df['is_seed'] == 0]

print(f"\nTotal expanded: {len(expanded)}")
print(f"Cosine range: {expanded['cosine'].min():.3f} - {expanded['cosine'].max():.3f}")
print(f"Mean cosine: {expanded['cosine'].mean():.3f}")
print(f"Median df: {expanded['df'].median():.0f}")

# Cosine distribution for expanded terms
print("\nCosine distribution (expanded only):")
bins = [0, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.0]
cosine_dist = pd.cut(expanded['cosine'], bins=bins).value_counts().sort_index()
print(cosine_dist)

print("\n" + "="*80)
print("SUSPICIOUS PATTERNS")
print("="*80)

# Low cosine + high weight
suspicious_weight = expanded[(expanded['cosine'] < 0.75) & (expanded['weight'] >= 0.9)]
print(f"\nLow cosine (<0.75) + high weight (≥0.9): {len(suspicious_weight)}")
if len(suspicious_weight) > 0:
    print(suspicious_weight[['term', 'weight', 'cosine', 'df', 'parent']].head(15).to_string(index=False))

# Very high df + high weight
high_df_weight = expanded[(expanded['df'] > 300) & (expanded['weight'] >= 0.8)]
print(f"\nHigh df (>300) + high weight (≥0.8): {len(high_df_weight)}")
if len(high_df_weight) > 0:
    print(high_df_weight[['term', 'weight', 'df', 'cosine', 'parent']].sort_values('df', ascending=False).to_string(index=False))

print("\n" + "="*80)
print("PARENT EXPANSION ANALYSIS")
print("="*80)

parent_counts = expanded.groupby('parent').size().sort_values(ascending=False)
print(f"\nTop 20 parents by expansion count:")
print(parent_counts.head(20))

high_expansion_parents = parent_counts[parent_counts > 30]
print(f"\n\nParents with >30 expansions: {len(high_expansion_parents)}")
if len(high_expansion_parents) > 0:
    print(high_expansion_parents)

# Save for detailed review
topic_df.to_csv(r'C:\Users\Home\policy-analysis\slavernij_historisch_for_review.csv', index=False)
print(f"\n\nFull data saved to: slavernij_historisch_for_review.csv")
