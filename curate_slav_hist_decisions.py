import pandas as pd

# Load the manual review file
df = pd.read_csv(r'C:\Users\Home\policy-analysis\slavernij_historisch_manual_review.csv', encoding='utf-8-sig')

# Add decision columns
df['action'] = 'KEEP'  # Default: KEEP, REMOVE, RECATEGORIZE, REWEIGHT
df['new_category'] = df['category']
df['new_weight'] = df['weight']
df['curation_notes'] = ''

print("SLAVERNIJ_HISTORISCH CURATION - SYSTEMATIC DECISIONS")
print("="*80)

# =============================================================================
# RULE 1: REMOVE SEMANTIC DRIFT FROM "UITBUITING" PARENT
# =============================================================================
print("\nRULE 1: Remove semantic drift from 'uitbuiting' parent")
print("-"*80)

# These are orthographic matches but wrong meaning
semantic_drift_terms = [
    'uit-', 'uiting', 'uitmaken', 'uitte', 'uitging', 'uittocht',
    'uitputtende', 'uitgeloot', 'uitbraken', 'uitsprak', 'uitstaan',
    'uitroepen', 'uitbarsten', 'uitgeputte', 'uitbarstingen',
    'opheffing', 'voortzetting', 'afbreking', 'verwijdering',
    'ontduiking', 'ontsporing', 'aanwas', 'bezetting'
]

mask = df['term'].isin(semantic_drift_terms)
df.loc[mask, 'action'] = 'REMOVE'
df.loc[mask, 'curation_notes'] = 'Semantic drift from uitbuiting - orthographic not semantic match'
print(f"Removing {mask.sum()} semantic drift terms from 'uitbuiting' parent")

# =============================================================================
# RULE 2: ULTRA-HIGH FREQUENCY DAMPENING (df > 300)
# =============================================================================
print("\nRULE 2: Dampen ultra-high frequency terms")
print("-"*80)

# koloniale (524), slaven (479), geschiedenis (316)
ultra_high_freq = df['df'] > 300

# "koloniale" - grammatical variant, keep in KERN but dampen to 0.9 (already 0.9, no change needed)
mask = (df['term'] == 'koloniale')
# Already 0.9, no change
print(f"'koloniale' (df=524): Already at 0.9 KERN - KEEP as is")

# "slaven" - generic plural, low cosine (0.72) - MOVE to CONTEXT
mask = (df['term'] == 'slaven')
df.loc[mask, 'action'] = 'RECATEGORIZE'
df.loc[mask, 'new_category'] = 'CONTEXT'
df.loc[mask, 'new_weight'] = 0.6
df.loc[mask, 'curation_notes'] = 'Ultra-high df (479) + low cosine (0.72) + too generic - move to CONTEXT'
print("'slaven' (df=479): KERN 0.9 to CONTEXT 0.6")

# "geschiedenis" - generic term, low cosine (0.70) - MOVE to CONTEXT
mask = (df['term'] == 'geschiedenis')
df.loc[mask, 'action'] = 'RECATEGORIZE'
df.loc[mask, 'new_category'] = 'CONTEXT'
df.loc[mask, 'new_weight'] = 0.6
df.loc[mask, 'curation_notes'] = 'Ultra-high df (316) + low cosine (0.70) + too generic - move to CONTEXT'
print("'geschiedenis' (df=316): KERN 0.9 to CONTEXT 0.6")

# =============================================================================
# RULE 3: LOW COSINE (<0.72) + KERN 1.0 → DOWNGRADE OR REMOVE
# =============================================================================
print("\nRULE 3: Downgrade/remove low cosine KERN 1.0 terms")
print("-"*80)

low_cosine_kern1 = (df['cosine'] < 0.72) & (df['weight'] == 1.0) & (df['action'] == 'KEEP')

# Review each
for idx, row in df[low_cosine_kern1].iterrows():
    term = row['term']
    cosine = row['cosine']
    parent = row['parent']

    # Specific semantic drift cases
    if term in ['goederenhandel', 'smokkelhandel']:
        # Generic trade terms, not slavery-specific
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'curation_notes'] = f'Semantic drift - generic trade term, not slavery-specific (cosine {cosine:.3f})'

    elif term in ['staats-', 'staatkundig']:
        # Fragments or generic government terms
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'curation_notes'] = f'Fragment or too generic government term (cosine {cosine:.3f})'

    elif term in ['slavengeld', 'negerhandel']:
        # Archaic/problematic terms with low frequency
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'curation_notes'] = f'Archaic/problematic term, low frequency, low cosine {cosine:.3f}'

    elif term in ['slavenvervoer', 'eigendomsslavernij']:
        # Specific but low cosine - downgrade to STERK 0.8
        df.loc[idx, 'action'] = 'RECATEGORIZE'
        df.loc[idx, 'new_category'] = 'STERK'
        df.loc[idx, 'new_weight'] = 0.8
        df.loc[idx, 'curation_notes'] = f'Relevant but low cosine ({cosine:.3f}) - downgrade to STERK 0.8'

    elif term in ['slavenopstanden', 'transatlantische']:
        # Valid terms, keep at lower weight
        df.loc[idx, 'action'] = 'REWEIGHT'
        df.loc[idx, 'new_weight'] = 0.9
        df.loc[idx, 'curation_notes'] = f'Valid term but low cosine ({cosine:.3f}) - lower to 0.9'

    else:
        # Other low-cosine KERN 1.0 - downgrade to 0.9
        df.loc[idx, 'action'] = 'REWEIGHT'
        df.loc[idx, 'new_weight'] = 0.9
        df.loc[idx, 'curation_notes'] = f'Low cosine ({cosine:.3f}) - lower from 1.0 to 0.9'

actions_taken = df[low_cosine_kern1].groupby('action').size()
print(f"Actions: {actions_taken.to_dict()}")

# =============================================================================
# RULE 4: LOW COSINE (<0.72) + KERN 0.9 → DOWNGRADE TO STERK
# =============================================================================
print("\nRULE 4: Downgrade low cosine KERN 0.9 terms to STERK")
print("-"*80)

low_cosine_kern09 = (df['cosine'] < 0.72) & (df['weight'] == 0.9) & (df['category'] == 'KERN') & (df['action'] == 'KEEP')

# Generic/problematic terms to remove
remove_list = ['arbeid', 'economie', 'tuin', 'houder', 'eigenheid', 'eigenbelang']
mask = low_cosine_kern09 & df['term'].isin(remove_list)
df.loc[mask, 'action'] = 'REMOVE'
df.loc[mask, 'curation_notes'] = 'Too generic or semantic drift - remove'
print(f"Removing {mask.sum()} generic/drift terms")

# Rest - downgrade to STERK 0.8
mask = low_cosine_kern09 & (df['action'] == 'KEEP')
df.loc[mask, 'action'] = 'RECATEGORIZE'
df.loc[mask, 'new_category'] = 'STERK'
df.loc[mask, 'new_weight'] = 0.8
df.loc[mask, 'curation_notes'] = 'Low cosine (<0.72) for KERN - downgrade to STERK 0.8'
print(f"Downgrading {mask.sum()} terms: KERN 0.9 → STERK 0.8")

# =============================================================================
# RULE 5: REMOVE PROBLEMATIC SEMANTIC DRIFT FROM OTHER PARENTS
# =============================================================================
print("\nRULE 5: Remove additional semantic drift")
print("-"*80)

drift_terms = [
    'vrouwenemancipatie',  # Different type of emancipation
    'schiedenis',  # OCR error/fragment
    'geschiedenis-',  # Fragment
    'oorlogsschepen', 'marineschepen', 'zeilschepen',  # Generic ships, not slave ships
    'roven',  # Generic robbery, not historical plunder
]

mask = df['term'].isin(drift_terms)
df.loc[mask, 'action'] = 'REMOVE'
df.loc[mask, 'curation_notes'] = 'Semantic drift or OCR error'
print(f"Removing {mask.sum()} additional drift/error terms")

# =============================================================================
# RULE 6: HIGH DF (200-300) GENERIC TERM - MOVE TO CONTEXT
# =============================================================================
print("\nRULE 6: High df generic terms to CONTEXT")
print("-"*80)

# "koloniën" (278) - geographic/contextual marker
mask = (df['term'] == 'koloniën') & (df['action'] == 'KEEP')
df.loc[mask, 'action'] = 'RECATEGORIZE'
df.loc[mask, 'new_category'] = 'CONTEXT'
df.loc[mask, 'new_weight'] = 0.6
df.loc[mask, 'curation_notes'] = 'High df (278), geographic marker - move to CONTEXT'
print("'kolonien': KERN 0.9 to CONTEXT 0.6")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "="*80)
print("CURATION SUMMARY")
print("="*80)

print("\nAction distribution:")
print(df.groupby('action').size())

print("\nCategory transitions:")
transitions = df[df['action'].isin(['RECATEGORIZE', 'REWEIGHT'])]
trans_summary = transitions.groupby(['category', 'new_category', 'weight', 'new_weight']).size().reset_index(name='count')
print(trans_summary.to_string(index=False))

# Calculate final dictionary size
final_kept = df[df['action'] != 'REMOVE']
print(f"\nFinal dictionary size: {len(final_kept)} terms (removed {(df['action'] == 'REMOVE').sum()})")

# Save curated dictionary
output_file = r'C:\Users\Home\policy-analysis\slavernij_historisch_curated.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\nCurated decisions saved to: {output_file}")

# Create clean final dictionary (removed terms excluded)
final_dict = df[df['action'] != 'REMOVE'][['term', 'parent', 'new_category', 'new_weight', 'cosine', 'df', 'curation_notes']].copy()
final_dict.columns = ['term', 'parent', 'category', 'weight', 'cosine', 'df', 'curation_notes']
final_output = r'C:\Users\Home\policy-analysis\slavernij_historisch_final.csv'
final_dict.to_csv(final_output, index=False, encoding='utf-8-sig')
print(f"Final clean dictionary saved to: {final_output}")

# Show removal reasons
print("\n" + "="*80)
print("REMOVAL REASONS")
print("="*80)
removed = df[df['action'] == 'REMOVE']
removal_reasons = removed.groupby('curation_notes').size().sort_values(ascending=False)
print(removal_reasons)
print(f"\nTotal removed: {len(removed)}")
