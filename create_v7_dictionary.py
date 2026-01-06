"""
Create v7 seed dictionary with improved scoring characteristics.

Changes from v6:
1. Reduce uniform term weights (geography 0.75->0.50, era_marker 0.70->0.55)
2. Expand weight differentiation (7 tiers instead of 5)
3. Add topic-specific problem vocabulary (~40 new terms)
4. Remove/reduce generic shared terms
"""

import pandas as pd
import csv

# Load v6 dictionary
v6_df = pd.read_csv('problem_oriented_legacy_seed_v6_4topics.csv')

print("Creating v7 dictionary...")
print(f"Starting with v6: {len(v6_df)} terms")

# Initialize v7 dictionary list
v7_entries = []

# Step 1: Process existing v6 terms with weight adjustments
print("\nStep 1: Adjusting existing term weights...")

for idx, row in v6_df.iterrows():
    topic = row['topic']
    term = row['term']
    weight = row['weight']
    category = row['category']

    # Skip terms we're removing entirely
    if term == 'slavernij' and category in ['historical', 'related']:
        print(f"  REMOVED: '{term}' (too generic for topic differentiation)")
        continue

    # Apply weight adjustments based on category
    if category == 'geography':
        new_weight = 0.50  # was 0.75
        new_category = 'geographic_context'
        print(f"  Adjusted: '{term}' geography 0.75 -> 0.50")

    elif category == 'era_marker':
        new_weight = 0.55  # was 0.70
        new_category = 'era_context'
        print(f"  Adjusted: '{term}' era_marker 0.70 -> 0.55")

    elif category == 'historical':
        new_weight = 0.55  # was 0.80, reclassify as era_context
        new_category = 'era_context'

    elif category == 'core_problem':
        # Keep high weights but differentiate
        if weight == 1.0:
            new_weight = 1.0
            new_category = 'core_problem'
        else:  # was 0.95
            new_weight = 0.95
            new_category = 'strong_problem'

    elif category == 'related':
        # Reclassify based on term specificity
        # This is approximate - could be refined per term
        if weight >= 0.9:
            # Strong domain terms
            new_weight = 0.85
            new_category = 'related_strong'
        elif weight >= 0.85:
            # Moderate domain terms
            new_weight = 0.75
            new_category = 'related_moderate'
        else:
            new_weight = 0.70
            new_category = 'related_moderate'
    else:
        new_weight = weight
        new_category = category

    # Special handling for shared generic terms
    if term in ['plantage', 'slavenhandel']:
        new_weight = 0.65
        new_category = 'related_weak'
        print(f"  Reduced: '{term}' -> 0.65 (generic shared term)")

    if term == 'afschaffing':
        new_weight = 0.55
        new_category = 'era_context'
        print(f"  Reclassified: '{term}' -> era_context 0.55")

    v7_entries.append({
        'topic': topic,
        'term': term,
        'weight': new_weight,
        'category': new_category
    })

print(f"\nAfter adjustments: {len(v7_entries)} terms")

# Step 2: Add new topic-specific vocabulary
print("\nStep 2: Adding new problem vocabulary...")

new_vocab = [
    # Educational additions (~10 terms)
    ('Educational Disadvantage & Brain Drain', 'schoolachterstand', 0.95, 'strong_problem'),
    ('Educational Disadvantage & Brain Drain', 'onderwijskloof', 0.95, 'strong_problem'),
    ('Educational Disadvantage & Brain Drain', 'analfabetisme', 0.90, 'strong_problem'),
    ('Educational Disadvantage & Brain Drain', 'taalachterstand', 0.90, 'strong_problem'),
    ('Educational Disadvantage & Brain Drain', 'onderwijsongelijkheid', 0.90, 'strong_problem'),
    ('Educational Disadvantage & Brain Drain', 'voortijdig schoolverlaten', 0.90, 'strong_problem'),
    ('Educational Disadvantage & Brain Drain', 'kennismigratie', 0.85, 'related_strong'),
    ('Educational Disadvantage & Brain Drain', 'onderwijsachterstand', 0.85, 'related_strong'),
    ('Educational Disadvantage & Brain Drain', 'schoolprestaties', 0.75, 'related_moderate'),
    ('Educational Disadvantage & Brain Drain', 'onderwijssysteem', 0.70, 'related_moderate'),

    # Governance additions (~10 terms)
    ('Governance Distrust & Corruption', 'omkoping', 0.95, 'strong_problem'),
    ('Governance Distrust & Corruption', 'vriendjespolitiek', 0.95, 'strong_problem'),
    ('Governance Distrust & Corruption', 'machtsmisbruik', 0.95, 'strong_problem'),
    ('Governance Distrust & Corruption', 'bestuurlijke zwakte', 0.90, 'strong_problem'),
    ('Governance Distrust & Corruption', 'institutioneel wantrouwen', 0.90, 'strong_problem'),
    ('Governance Distrust & Corruption', 'gebrek aan transparantie', 0.90, 'strong_problem'),
    ('Governance Distrust & Corruption', 'democratisch tekort', 0.90, 'strong_problem'),
    ('Governance Distrust & Corruption', 'politieke afhankelijkheid', 0.85, 'related_strong'),
    ('Governance Distrust & Corruption', 'bestuurscultuur', 0.75, 'related_moderate'),
    ('Governance Distrust & Corruption', 'governance', 0.70, 'related_moderate'),

    # Economic additions (~15 terms) - PRIORITY
    ('Persistent Poverty & Economic Vulnerability', 'structurele armoede', 0.95, 'strong_problem'),
    ('Persistent Poverty & Economic Vulnerability', 'langdurige werkloosheid', 0.95, 'strong_problem'),
    ('Persistent Poverty & Economic Vulnerability', 'inkomensongelijkheid', 0.95, 'strong_problem'),
    ('Persistent Poverty & Economic Vulnerability', 'economische uitsluiting', 0.95, 'strong_problem'),
    ('Persistent Poverty & Economic Vulnerability', 'financiële kwetsbaarheid', 0.90, 'strong_problem'),
    ('Persistent Poverty & Economic Vulnerability', 'verborgen armoede', 0.90, 'strong_problem'),
    ('Persistent Poverty & Economic Vulnerability', 'minimuminkomens', 0.85, 'related_strong'),
    ('Persistent Poverty & Economic Vulnerability', 'arbeidsmarkt', 0.80, 'related_strong'),
    ('Persistent Poverty & Economic Vulnerability', 'economische structuur', 0.80, 'related_strong'),
    ('Persistent Poverty & Economic Vulnerability', 'inkomen', 0.75, 'related_moderate'),
    ('Persistent Poverty & Economic Vulnerability', 'werk', 0.75, 'related_moderate'),
    ('Persistent Poverty & Economic Vulnerability', 'banen', 0.70, 'related_moderate'),
    ('Persistent Poverty & Economic Vulnerability', 'economie', 0.70, 'related_moderate'),
    ('Persistent Poverty & Economic Vulnerability', 'financieel', 0.70, 'related_moderate'),
    ('Persistent Poverty & Economic Vulnerability', 'kosten', 0.65, 'related_weak'),

    # Racism additions (~5 terms)
    ('Social Fragmentation & Racism', 'institutioneel racisme', 0.95, 'strong_problem'),
    ('Social Fragmentation & Racism', 'structureel racisme', 0.95, 'strong_problem'),
    ('Social Fragmentation & Racism', 'sociale ongelijkheid', 0.90, 'strong_problem'),
    ('Social Fragmentation & Racism', 'etnische discriminatie', 0.90, 'strong_problem'),
    ('Social Fragmentation & Racism', 'raciale hiërarchie', 0.90, 'strong_problem'),
]

for topic, term, weight, category in new_vocab:
    v7_entries.append({
        'topic': topic,
        'term': term,
        'weight': weight,
        'category': category
    })
    print(f"  Added: '{term}' to {topic[:20]}... ({weight}, {category})")

print(f"\nAfter additions: {len(v7_entries)} terms")

# Create DataFrame and save
v7_df = pd.DataFrame(v7_entries)

# Sort by topic, then by weight (descending), then by term
v7_df = v7_df.sort_values(['topic', 'weight', 'term'], ascending=[True, False, True])

# Save to CSV
output_file = 'problem_oriented_legacy_seed_v7_4topics.csv'
v7_df.to_csv(output_file, index=False)

print(f"\n{'='*80}")
print("v7 DICTIONARY CREATED")
print(f"{'='*80}")
print(f"Output: {output_file}")
print(f"Total terms: {len(v7_df)}")
print(f"\nPer-topic breakdown:")

for topic in v7_df['topic'].unique():
    topic_df = v7_df[v7_df['topic'] == topic]
    print(f"\n{topic}:")
    print(f"  Total: {len(topic_df)} terms")
    print(f"  Categories:")
    for cat, count in topic_df['category'].value_counts().items():
        print(f"    {cat}: {count}")
    print(f"  Weight range: {topic_df['weight'].min():.2f} - {topic_df['weight'].max():.2f}")

print(f"\n{'='*80}")
print("SUMMARY OF CHANGES")
print(f"{'='*80}")
print(f"v6 terms: {len(v6_df)}")
print(f"v7 terms: {len(v7_df)}")
print(f"Net change: +{len(v7_df) - len(v6_df)} terms")

print("\nKey improvements:")
print("  ✓ Geography weights: 0.75 -> 0.50 (reduced cross-contamination)")
print("  ✓ Era marker weights: 0.70 -> 0.55 (reduced uniform baseline)")
print("  ✓ Weight tiers: 5 -> 7 (better differentiation)")
print("  ✓ New problem vocabulary: +40 terms (stronger topic signals)")
print("  ✓ Generic terms: removed 'slavernij', reduced 'plantage'/'slavenhandel'")

print("\nExpected impact:")
print("  → Max scores expand from 0.55-0.64 to 0.72-0.80")
print("  → Standard deviation increases from 0.08-0.11 to 0.14-0.17")
print("  → High confidence chunks increase from 19% to ~27%")
print("  → Better topic differentiation and pattern quality")

print(f"\nNext step: Test on evaluation sample with score_eval_sample_v7.py")
