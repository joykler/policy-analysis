import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("SLAVERNIJ_HISTORISCH - APPLYING MANUAL SEMANTIC CURATION")
print("="*80)

# Load the manual review file
df = pd.read_csv(r'C:\Users\Home\policy-analysis\slavernij_historisch_manual_review.csv', encoding='utf-8-sig')
print(f"Total terms to review: {len(df)}")

# Add decision columns
df['action'] = 'KEEP'
df['new_category'] = df['category']
df['new_weight'] = df['weight']
df['manual_notes'] = ''

# MANUAL SEMANTIC REMOVALS (based on human review)
remove_terms = [
    # Fragments
    'staats-', 'uit-', 'schiedenis',

    # Generic/not slavery-specific
    'smokkelhandel', 'staatkundig', 'goederenhandel', 'arbeid', 'economie',
    'houder', 'roven',

    # Archaic/problematic
    'slavengeld', 'negerhandel',

    # Semantic drift from "plantage"
    'tuin', 'tuinen',

    # Semantic drift from "eigendom van personen"
    'eigenheid', 'eigenbelang',

    # Wrong type of emancipation
    'vrouwenemancipatie',

    # Semantic drift from "uitbuiting" (orthographic "uit-" matches)
    'uiting', 'uitmaken', 'uitte', 'uitging', 'uittocht',
    'uitgeloot', 'uitbraken', 'uitsprak', 'uitstaan', 'uitroepen', 'uitbarsten',
    'aanwas', 'ontduiking', 'ontsporing',

    # Generic ships (not slave ships)
    'oorlogsschepen', 'marineschepen', 'zeilschepen',

    # Semantic drift from "ketenen"
    'sloot', 'bezetten', 'haakjes',
]

print(f"\nRemoving {len(remove_terms)} semantically problematic terms:")
for term in remove_terms:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        parent = df.loc[idx, 'parent']
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = f'Semantic drift or too generic (manual review)'
        print(f"  - '{term}' (parent: '{parent}')")

# RECATEGORIZATIONS
recategorize_context = {
    'slaven': 'Too generic plural - context marker',
    'geschiedenis': 'Generic temporal term - context marker',
}

print(f"\nRecategorizing {len(recategorize_context)} terms to CONTEXT:")
for term, reason in recategorize_context.items():
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'RECATEGORIZE'
        df.loc[idx, 'new_category'] = 'CONTEXT'
        df.loc[idx, 'new_weight'] = 0.6
        df.loc[idx, 'manual_notes'] = reason
        print(f"  - '{term}': {reason}")

# DOWNGRADES (low cosine but valid terms)
downgrade_kern1_to_09 = [
    'slavenopstanden', 'transatlantische', 'slavernijmusea', 'slavernijcomplex'
]

print(f"\nDowngrading KERN 1.0 → 0.9 ({len(downgrade_kern1_to_09)} terms with low cosine):")
for term in downgrade_kern1_to_09:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        if df.loc[idx, 'weight'] == 1.0:
            df.loc[idx, 'action'] = 'REWEIGHT'
            df.loc[idx, 'new_weight'] = 0.9
            df.loc[idx, 'manual_notes'] = 'Valid term but low cosine - lower to 0.9'
            print(f"  - '{term}'")

downgrade_kern_to_sterk = [
    'eigendomsslavernij', 'slavenvervoer'
]

print(f"\nDowngrading KERN → STERK 0.8 ({len(downgrade_kern_to_sterk)} terms):")
for term in downgrade_kern_to_sterk:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'RECATEGORIZE'
        df.loc[idx, 'new_category'] = 'STERK'
        df.loc[idx, 'new_weight'] = 0.8
        df.loc[idx, 'manual_notes'] = 'Relevant but low cosine - downgrade to STERK'
        print(f"  - '{term}'")

# Apply automatic Phase 1 that was already decided in earlier script
# (These would have been caught by automated rules)
print("\n" + "="*80)
print("SUMMARY")
print("="*80)

print(f"\nAction distribution:")
action_counts = df.groupby('action').size()
print(action_counts)

final_kept = df[df['action'] != 'REMOVE']
print(f"\nFinal size: {len(final_kept)} (removed {(df['action'] == 'REMOVE').sum()})")

# Save curated results
output_file = r'C:\Users\Home\policy-analysis\slavernij_historisch_MANUAL_CURATED.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\nSaved full curation: {output_file}")

# Create final clean dictionary
final_dict = df[df['action'] != 'REMOVE'][['term', 'parent', 'new_category', 'new_weight', 'cosine', 'df', 'manual_notes']].copy()
final_dict.columns = ['term', 'parent', 'category', 'weight', 'cosine', 'df', 'curation_notes']

final_output = r'C:\Users\Home\policy-analysis\slavernij_historisch_FINAL_MANUAL.csv'
final_dict.to_csv(final_output, index=False, encoding='utf-8-sig')
print(f"Saved final dictionary: {final_output}")

print(f"\n{'='*80}")
print("MANUAL CURATION COMPLETE FOR SLAVERNIJ_HISTORISCH")
print(f"{'='*80}")
