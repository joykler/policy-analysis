import pandas as pd
import csv

# Load data
df = pd.read_csv(r'C:\Users\Home\policy-analysis\workflow_data\slavery_Slavdict_pretraining_slavery_v16\Cosine_labeling\evaluation_sample.csv')

# Create evaluation template CSV
output_rows = []

for i in range(len(df)):
    chunk = df.iloc[i]

    # Extract text preview (first 1000 chars)
    text_preview = chunk['raw_text'][:1000].replace('\n', ' ').replace('\r', ' ')

    output_rows.append({
        'chunk_num': i + 1,
        'chunk_id': chunk['chunk_id'],
        'assigned_topic': chunk['primary_topic'],
        'confidence': chunk['confidence_level'],
        'score_ed': round(chunk['cos_Educational Disadvantage & Brain Drain'], 4),
        'score_gov': round(chunk['cos_Governance Distrust & Corruption'], 4),
        'score_econ': round(chunk['cos_Persistent Poverty & Economic Vulnerability'], 4),
        'score_rac': round(chunk['cos_Social Fragmentation & Racism'], 4),
        'text_preview': text_preview,
        # Fields for evaluation (to be filled)
        'actual_ed': '',
        'actual_gov': '',
        'actual_econ': '',
        'actual_rac': '',
        'primary_correct': '',
        'judgment': '',
        'notes': ''
    })

# Save to CSV
output_df = pd.DataFrame(output_rows)
output_df.to_csv(r'C:\Users\Home\policy-analysis\evaluation_template_60.csv', index=False, encoding='utf-8', quoting=csv.QUOTE_ALL)

print(f"Created evaluation template for {len(output_rows)} chunks")
print("Saved to: evaluation_template_60.csv")

# Also create a summary for quick scanning
print("\n" + "="*80)
print("SUMMARY OF ALL 60 CHUNKS")
print("="*80)

for i, row in enumerate(output_rows):
    highest_score = max(row['score_ed'], row['score_gov'], row['score_econ'], row['score_rac'])

    print(f"\n{i+1}. {row['assigned_topic'][:20]} ({row['confidence']})")
    print(f"   Ed:{row['score_ed']:.3f} Gov:{row['score_gov']:.3f} Econ:{row['score_econ']:.3f} Rac:{row['score_rac']:.3f}")
    print(f"   {row['text_preview'][:150]}...")

print("\n" + "="*80)
print("Template ready for manual evaluation")
print("="*80)
