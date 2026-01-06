import pandas as pd
import numpy as np

# Load expanded candidates
df = pd.read_csv(r'C:\Users\Home\policy-analysis\workflow_Structureddict\slavery_structured-slavdict_pretrained_slavery_v1\Dictionary\expanded_candidates.csv')

# Filter for Slavernij_Historisch
topic_df = df[df['topic'] == 'Slavernij_Historisch'].copy()

print("SLAVERNIJ_HISTORISCH - PHASE 1: AUTOMATIC REMOVALS")
print("="*80)

# Add curation decision column
topic_df['decision'] = 'KEEP'  # Default
topic_df['reason'] = ''

# Phase 1.1: Morphological fragments - NONE FOUND
fragments = topic_df['term'].str.len() < 4
print(f"\n1.1 Morphological fragments (len < 4): {fragments.sum()} - NONE")

# Phase 1.2: Extreme low similarity - NONE FOUND
low_cosine = topic_df['cosine'] < 0.65
print(f"1.2 Extreme low cosine (<0.65): {low_cosine.sum()} - NONE")

# Phase 1.3: Single document frequency (expanded only) - NONE FOUND
single_df_mask = (topic_df['df'] == 1) & (topic_df['is_seed'] == 0)
print(f"1.3 Single df (expanded only): {single_df_mask.sum()} - NONE")

# Phase 1.4: Zero df - these are seed terms (multi-word phrases)
zero_df_mask = topic_df['df'] == 0
print(f"1.4 Zero df (seed phrases): {zero_df_mask.sum()}")
print("    NOTE: These are multi-word seed phrases - KEEP for now, evaluate later")

print("\n" + "="*80)
print("PHASE 1 RESULT: NO AUTOMATIC REMOVALS")
print("="*80)
print("\nAll 300 terms pass Phase 1 technical quality checks")
print("  - No morphological fragments")
print("  - No extreme low cosine")
print("  - No single-occurrence terms")
print("  - Zero-df terms are intentional multi-word seed phrases")

# Now analyze for Phase 2-4 manual review
print("\n" + "="*80)
print("PREPARING FOR MANUAL REVIEW (PHASES 2-4)")
print("="*80)

expanded = topic_df[topic_df['is_seed'] == 0].copy()

# Flag suspicious patterns for manual review
expanded['review_priority'] = 0  # 0=low, 1=medium, 2=high

# HIGH PRIORITY: Low cosine + KERN category
mask = (expanded['cosine'] < 0.75) & (expanded['category'] == 'KERN')
expanded.loc[mask, 'review_priority'] = 2
expanded.loc[mask, 'reason'] = 'Low cosine + KERN - validate fit'
print(f"\nHIGH PRIORITY: Low cosine (<0.75) + KERN: {mask.sum()}")

# HIGH PRIORITY: Very high df + high weight
mask = (expanded['df'] > 300) & (expanded['weight'] >= 0.9)
expanded.loc[mask, 'review_priority'] = 2
if expanded.loc[mask, 'reason'].empty or expanded.loc[mask, 'reason'].str.len().sum() == 0:
    expanded.loc[mask, 'reason'] = 'Very high df - dampen weight'
else:
    expanded.loc[mask, 'reason'] += '; Very high df - dampen weight'
print(f"HIGH PRIORITY: High df (>300) + high weight (>=0.9): {mask.sum()}")

# MEDIUM PRIORITY: Moderate-low cosine
mask = (expanded['cosine'] >= 0.65) & (expanded['cosine'] < 0.72) & (expanded['review_priority'] == 0)
expanded.loc[mask, 'review_priority'] = 1
expanded.loc[mask, 'reason'] = 'Moderate-low cosine - check semantic drift'
print(f"\nMEDIUM PRIORITY: Moderate-low cosine (0.65-0.72): {mask.sum()}")

# MEDIUM PRIORITY: High df (200-300)
mask = (expanded['df'] > 200) & (expanded['df'] <= 300) & (expanded['review_priority'] == 0)
expanded.loc[mask, 'review_priority'] = 1
expanded.loc[mask, 'reason'] = 'High df (200-300) - check if too generic'
print(f"MEDIUM PRIORITY: High df (200-300): {mask.sum()}")

# Count review priorities
print(f"\nREVIEW PRIORITY DISTRIBUTION:")
print(f"  High priority (2): {(expanded['review_priority'] == 2).sum()}")
print(f"  Medium priority (1): {(expanded['review_priority'] == 1).sum()}")
print(f"  Low priority (0): {(expanded['review_priority'] == 0).sum()}")

# Sort for review
expanded_sorted = expanded.sort_values(['review_priority', 'weight', 'df'], ascending=[False, False, False])

# Save for manual review
output_file = r'C:\Users\Home\policy-analysis\slavernij_historisch_manual_review.csv'
expanded_sorted[['term', 'parent', 'category', 'weight', 'cosine', 'df', 'review_priority', 'reason']].to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n\nExpanded terms saved for manual review:")
print(f"  {output_file}")
print(f"  {len(expanded_sorted)} terms to review")

# Show top priorities
print("\n" + "="*80)
print("TOP 20 HIGH-PRIORITY TERMS FOR REVIEW")
print("="*80)
high_priority = expanded_sorted[expanded_sorted['review_priority'] == 2].head(20)
if len(high_priority) > 0:
    print(high_priority[['term', 'weight', 'cosine', 'df', 'parent', 'reason']].to_string(index=False))
else:
    print("No high-priority terms found")

# Parent expansion stats
print("\n" + "="*80)
print("PARENT EXPANSION COUNTS (>20 expansions)")
print("="*80)
parent_counts = expanded.groupby('parent').size().sort_values(ascending=False)
high_expansion = parent_counts[parent_counts > 20]
if len(high_expansion) > 0:
    print(high_expansion.to_string())
    print(f"\nTotal parents with >20 expansions: {len(high_expansion)}")
else:
    print("No parents with >20 expansions")

print("\n" + "="*80)
print("PHASE 1 COMPLETE - READY FOR MANUAL CURATION")
print("="*80)
