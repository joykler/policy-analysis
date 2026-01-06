import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("DOORWERKING_CONTINUITEIT - APPLYING MANUAL SEMANTIC CURATION")
print("="*80)

df = pd.read_csv(r'C:\Users\Home\policy-analysis\doorwerking_continuiteit_CORRECTED.csv', encoding='utf-8-sig')
print(f"Total expanded terms to review: {len(df)}")

df['action'] = 'KEEP'
df['new_category'] = df['category']
df['new_weight'] = df['weight']
df['manual_notes'] = ''

# CRITICAL DECISION: Remove ALL RISICO 0.3 terms
# These are ultra-generic policy/admin language with no specific slavery legacy connection
print(f"\nRemoving ALL RISICO 0.3 terms (ultra-generic policy language):")
risico_mask = df['weight'] == 0.3
risico_count = risico_mask.sum()
df.loc[risico_mask, 'action'] = 'REMOVE'
df.loc[risico_mask, 'manual_notes'] = 'RISICO 0.3 - too generic policy/admin language, not slavery legacy-specific'
print(f"  Removed {risico_count} RISICO 0.3 terms")

# ULTRA-HIGH DF TERMS (even if not RISICO)
remove_ultra_high_df = [
    'structurele',  # df 94 - seed already captured
    'geschiedenis',  # df 316 - ultra-generic
    'tijd',  # df 404 - ultra-generic time
    'behandeling',  # df 136 - too generic
    'kans',  # df 101 - too generic
    'positie',  # df 216 - ultra-generic
]

print(f"\nRemoving {len(remove_ultra_high_df)} ultra-high df generic terms:")
for term in remove_ultra_high_df:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = f'Ultra-high df (>{df.loc[idx, "df"]}) - too generic'
        print(f"  - '{term}' (df={df.loc[idx, 'df']})")

# ENGLISH WORDS (not Dutch!)
remove_english = [
    'time', 'systems', 'system--the', 'heritage', 'text', 'development'
]

print(f"\nRemoving {len(remove_english)} English words (NOT Dutch):")
for term in remove_english:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'English word, not Dutch'
        print(f"  - '{term}'")

# OCR ERRORS/TYPOS
remove_typos = [
    'schiedenis',  # typo for geschiedenis
    'geschiedenis-',  # fragment
]

print(f"\nRemoving {len(remove_typos)} OCR errors/fragments:")
for term in remove_typos:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'OCR error or fragment'
        print(f"  - '{term}'")

# SUMMARY
print("\n" + "="*80)
print("SUMMARY")
print("="*80)

print(f"\nAction distribution:")
action_counts = df.groupby('action').size()
print(action_counts)

final_kept = df[df['action'] != 'REMOVE']
print(f"\nFinal size: {len(final_kept)} (removed {(df['action'] == 'REMOVE').sum()})")

print(f"\nCategory distribution of KEPT terms:")
kept_cats = final_kept.groupby('category').size()
print(kept_cats)

# Save
output_file = r'C:\Users\Home\policy-analysis\doorwerking_continuiteit_MANUAL_CURATED.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\nSaved full curation: {output_file}")

final_dict = df[df['action'] != 'REMOVE'][['term', 'parent', 'new_category', 'new_weight', 'cosine', 'df', 'manual_notes']].copy()
final_dict.columns = ['term', 'parent', 'category', 'weight', 'cosine', 'df', 'curation_notes']

final_output = r'C:\Users\Home\policy-analysis\doorwerking_continuiteit_FINAL_MANUAL.csv'
final_dict.to_csv(final_output, index=False, encoding='utf-8-sig')
print(f"Saved final dictionary: {final_output}")

print(f"\n{'='*80}")
print("MANUAL CURATION COMPLETE FOR DOORWERKING_CONTINUITEIT")
print(f"{'='*80}")
