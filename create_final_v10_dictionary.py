import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("CREATING FINAL V10 MERGED DICTIONARY")
print("="*80)

# Load all corrected topic dictionaries
topics = [
    ('Slavernij_Historisch', 'slavernij_historisch_CORRECTED.csv'),
    ('Koninkrijks_Macht', 'koninkrijks_macht_CORRECTED.csv'),
    ('Raciale_Hierarchie', 'raciale_hierarchie_CORRECTED.csv'),
    ('Arbeid_Afhankelijkheid', 'arbeid_afhankelijkheid_CORRECTED.csv'),
    ('Doorwerking_Continuiteit', 'doorwerking_continuiteit_CORRECTED.csv'),
    ('Erkenning_Verantwoordelijkheid', 'erkenning_verantwoordelijkheid_CORRECTED.csv'),
    ('Kennis_Herinnering', 'kennis_herinnering_CORRECTED.csv')
]

all_dicts = []

for topic_name, filename in topics:
    df = pd.read_csv(fr'C:\Users\Home\policy-analysis\{filename}', encoding='utf-8-sig')
    df['topic'] = topic_name
    all_dicts.append(df)
    print(f"{topic_name}: {len(df)} terms")

# Merge all dictionaries
merged = pd.concat(all_dicts, ignore_index=True)

print(f"\n{'='*80}")
print(f"MERGED DICTIONARY STATISTICS")
print(f"{'='*80}")
print(f"\nTotal terms across all topics: {len(merged)}")
print(f"Unique terms: {merged['term'].nunique()}")
print(f"Terms appearing in multiple topics: {len(merged) - merged['term'].nunique()}")

# Category distribution
print(f"\n{'='*80}")
print("CATEGORY DISTRIBUTION (All Topics)")
print(f"{'='*80}")
cat_dist = merged.groupby('category').size().sort_values(ascending=False)
print(cat_dist)
print(f"\nTotal: {cat_dist.sum()}")

# Weight distribution
print(f"\n{'='*80}")
print("WEIGHT DISTRIBUTION (All Topics)")
print(f"{'='*80}")
weight_dist = merged.groupby('weight').size().sort_index()
print(weight_dist)

# Category x Weight
print(f"\n{'='*80}")
print("CATEGORY x WEIGHT DISTRIBUTION")
print(f"{'='*80}")
cat_weight = merged.groupby(['category', 'weight']).size().reset_index(name='count')
print(cat_weight.to_string(index=False))

# Terms appearing in multiple topics
print(f"\n{'='*80}")
print("CROSS-TOPIC TERMS (appearing in 3+ topics)")
print(f"{'='*80}")
term_counts = merged.groupby('term').size().sort_values(ascending=False)
multi_topic = term_counts[term_counts >= 3]
print(f"Terms in 3+ topics: {len(multi_topic)}")
print("\nTop 20 cross-topic terms:")
print(multi_topic.head(20))

# Save merged dictionary
output_file = r'C:\Users\Home\policy-analysis\V10_DICTIONARY_FINAL_MERGED.csv'
merged.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n{'='*80}")
print(f"Merged dictionary saved: {output_file}")
print(f"{'='*80}")

# Create topic-level summary
print(f"\n{'='*80}")
print("PER-TOPIC STATISTICS")
print(f"{'='*80}")

summary_rows = []
for topic_name, _ in topics:
    topic_df = merged[merged['topic'] == topic_name]
    summary_rows.append({
        'Topic': topic_name,
        'Total_Terms': len(topic_df),
        'KERN': len(topic_df[topic_df['category'] == 'KERN']),
        'BELEID': len(topic_df[topic_df['category'] == 'BELEID']),
        'STERK': len(topic_df[topic_df['category'] == 'STERK']),
        'CONTEXT': len(topic_df[topic_df['category'] == 'CONTEXT']),
        'RISICO': len(topic_df[topic_df['category'] == 'RISICO']),
        'Avg_DF': topic_df['df'].mean(),
        'Avg_Cosine': topic_df['cosine'].mean()
    })

summary_df = pd.DataFrame(summary_rows)
print(summary_df.to_string(index=False))

# Save summary
summary_file = r'C:\Users\Home\policy-analysis\V10_DICTIONARY_SUMMARY_STATS.csv'
summary_df.to_csv(summary_file, index=False, encoding='utf-8-sig')
print(f"\nSummary statistics saved: {summary_file}")

print(f"\n{'='*80}")
print("FINAL V10 DICTIONARY CREATION COMPLETE")
print(f"{'='*80}")
print(f"\nFinal curated dictionary: {len(merged)} terms across 7 topics")
print(f"Average terms per topic: {len(merged) / 7:.1f}")
print(f"\nQuality indicators:")
print(f"  - Average cosine similarity: {merged['cosine'].mean():.3f}")
print(f"  - KERN category (strict standard): {len(merged[merged['category'] == 'KERN'])} terms ({100*len(merged[merged['category'] == 'KERN'])/len(merged):.1f}%)")
print(f"  - Terms with df >= 10: {len(merged[merged['df'] >= 10])} ({100*len(merged[merged['df'] >= 10])/len(merged):.1f}%)")
