"""
Systematic Curation of Topic 2: Social Fragmentation & Racism
Following the Dictionary Curation Guide methodology
"""

import pandas as pd

# Read the expanded candidates
df = pd.read_csv(r"C:\Users\Home\policy-analysis\workflow_data\slavery_Slavdict_pretrained_slavery_v3\Dictionary\expanded_candidates.csv")

# Filter for Topic 2
topic2 = df[df['topic'] == 'Social Fragmentation & Racism'].copy()

print(f"Total terms for Social Fragmentation & Racism: {len(topic2)}")
print(f"\nWeight distribution:")
print(topic2['weight'].value_counts().sort_index(ascending=False))

print(f"\nCategory distribution:")
print(topic2['category'].value_counts())

print(f"\nDocument frequency statistics:")
print(topic2['df'].describe())

print(f"\nCosine similarity statistics:")
print(topic2['cosine'].describe())

# Add curation decision column
topic2['curation_decision'] = 'REVIEW'
topic2['curation_reason'] = ''

print("\n" + "="*80)
print("STARTING SYSTEMATIC CURATION - TOPIC 2")
print("="*80)

# Phase 1: Automatic Removals
print("\n### PHASE 1: AUTOMATIC REMOVAL (Technical Errors) ###\n")

# 1. Morphological fragments (len < 4 and not seed)
fragments = topic2[(topic2['term'].str.len() < 4) & (topic2['is_seed'] == 0)]
print(f"Morphological fragments (len<4, not seed): {len(fragments)}")
if len(fragments) > 0:
    print(fragments[['term', 'parent', 'cosine', 'df', 'weight']].to_string())
    topic2.loc[fragments.index, 'curation_decision'] = 'REMOVE'
    topic2.loc[fragments.index, 'curation_reason'] = 'Morphological fragment'

# 2. Extreme low similarity (cosine < 0.65)
low_cosine = topic2[(topic2['cosine'] < 0.65) & (topic2['is_seed'] == 0)]
print(f"\nLow cosine (<0.65, not seed): {len(low_cosine)}")
if len(low_cosine) > 0:
    print(low_cosine[['term', 'parent', 'cosine', 'df', 'weight']].to_string())
    topic2.loc[low_cosine.index, 'curation_decision'] = 'REMOVE'
    topic2.loc[low_cosine.index, 'curation_reason'] = 'Extreme low similarity'

# 3. Single document frequency (df == 1)
single_df = topic2[(topic2['df'] == 1) & (topic2['is_seed'] == 0)]
print(f"\nSingle document frequency (df=1, not seed): {len(single_df)}")
if len(single_df) > 0:
    print(single_df[['term', 'parent', 'cosine', 'df', 'weight']].head(20).to_string())
    topic2.loc[single_df.index, 'curation_decision'] = 'REMOVE'
    topic2.loc[single_df.index, 'curation_reason'] = 'Single document frequency'

# Summary of automatic removals
auto_removed = topic2[topic2['curation_decision'] == 'REMOVE']
print(f"\n### PHASE 1 SUMMARY ###")
print(f"Total automatic removals: {len(auto_removed)}")
print(f"Remaining for manual review: {len(topic2) - len(auto_removed)}")

# Phase 2: Manual Review Priorities
print("\n" + "="*80)
print("### PHASE 2-5: MANUAL REVIEW NEEDED ###")
print("="*80)

# Terms that need manual review (not automatically removed and not seed)
manual_review = topic2[(topic2['curation_decision'] == 'REVIEW') & (topic2['is_seed'] == 0)].copy()

# Sort by priority: weight DESC, then cosine ASC
manual_review_sorted = manual_review.sort_values(['weight', 'cosine'], ascending=[False, True])

print(f"\nTotal terms for manual review: {len(manual_review_sorted)}")

# Priority 1: High-impact terms
print("\n### PRIORITY 1: HIGH-IMPACT TERMS ###")

# Core problem (1.00) expansions
core_expansions = manual_review_sorted[(manual_review_sorted['weight'] == 1.0)]
print(f"\nCore problem (1.00) expansions: {len(core_expansions)}")
if len(core_expansions) > 0:
    print(core_expansions[['term', 'parent', 'cosine', 'df', 'weight', 'category']].to_string())

# Strong problem (0.95) with low cosine (<0.75)
strong_low_cosine = manual_review_sorted[(manual_review_sorted['weight'] == 0.95) & (manual_review_sorted['cosine'] < 0.75)]
print(f"\nStrong problem (0.95) with cosine < 0.75: {len(strong_low_cosine)}")
if len(strong_low_cosine) > 0:
    print(strong_low_cosine[['term', 'parent', 'cosine', 'df', 'weight', 'category']].to_string())

# High frequency terms (df > 100)
high_freq = manual_review_sorted[manual_review_sorted['df'] > 100]
print(f"\nHigh frequency (df > 100): {len(high_freq)}")
if len(high_freq) > 0:
    print(high_freq[['term', 'parent', 'cosine', 'df', 'weight', 'category']].to_string())

# Priority 2: Suspicious patterns
print("\n### PRIORITY 2: SUSPICIOUS PATTERNS ###")

# Low cosine + high weight
suspicious = manual_review_sorted[(manual_review_sorted['cosine'] < 0.72) & (manual_review_sorted['weight'] >= 0.95)]
print(f"\nLow cosine (<0.72) + High weight (>=0.95): {len(suspicious)}")
if len(suspicious) > 0:
    print(suspicious[['term', 'parent', 'cosine', 'df', 'weight', 'category']].to_string())

# All terms sorted by weight (for full review)
print("\n### ALL TERMS FOR MANUAL REVIEW (sorted by weight DESC, cosine ASC) ###")
print(f"\nTotal: {len(manual_review_sorted)}")

# Save to file for detailed review
output_file = r"C:\Users\Home\policy-analysis\topic2_racism_manual_review.csv"
manual_review_sorted.to_csv(output_file, index=False)
print(f"\nFull list saved to: {output_file}")

# Display all for LLM review
print("\n" + "="*80)
print("COMPLETE TERM LIST FOR LLM SEMANTIC REVIEW")
print("="*80)
print(manual_review_sorted[['term', 'parent', 'cosine', 'df', 'weight', 'category']].to_string())

# Save current state
topic2.to_csv(r"C:\Users\Home\policy-analysis\topic2_racism_curation_state.csv", index=False)
print(f"\n\nCuration state saved to: topic2_racism_curation_state.csv")
