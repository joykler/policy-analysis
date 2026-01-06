import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("ARBEID_AFHANKELIJKHEID - APPLYING MANUAL SEMANTIC CURATION")
print("="*80)

df = pd.read_csv(r'C:\Users\Home\policy-analysis\arbeid_afhankelijkheid_CORRECTED.csv', encoding='utf-8-sig')
print(f"Total expanded terms to review: {len(df)}")

df['action'] = 'KEEP'
df['new_category'] = df['category']
df['new_weight'] = df['weight']
df['manual_notes'] = ''

# POLITICS ≠ POLICE - "politionele controle" semantic drift
remove_politics_drift = [
    'political', 'politics',  # English words for "political"!
    'politicologische',  # political science (academic)
    'politici',  # politicians
]

print(f"\nRemoving {len(remove_politics_drift)} politics/political science terms (NOT police control):")
for term in remove_politics_drift:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Semantic drift - politics/political science ≠ politionele (police) control'
        print(f"  - '{term}'")

# ONT- PREFIX DRIFT from "onteigening" (expropriation)
remove_ont_drift = [
    'ontving', 'ontvingen',  # received - NOT expropriation!
    'afspiegeling',  # reflection/mirror
    'verving',  # replacement
    'versteviging',  # strengthening - OPPOSITE!
    'onthulling',  # revelation
    'ontregeling',  # disruption
    'ontmanteling',  # dismantling
    'ontheffing',  # exemption
    'vernietiging',  # destruction - too generic
]

print(f"\nRemoving {len(remove_ont_drift)} ont- prefix drift from 'onteigening':")
for term in remove_ont_drift:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Semantic drift - ont- prefix match, not expropriation'
        print(f"  - '{term}'")

# GENERIC LAND/COUNTRY TERMS from "landbezit"
remove_land_generic = [
    'land',  # land/country - ultra-high df (272)!
    'land-',  # fragment
    'vasteland',  # mainland/continent - geographic
    'landje',  # small plot - diminutive, generic
    'landschappen',  # landscapes - aesthetic/geographic
    'landbouw-',  # fragment
    'landbouwende',  # agricultural - generic adjective
    'landse',  # rural/country-like - generic, df 41
    'landelijk',  # rural/nationwide - ambiguous, generic
]

print(f"\nRemoving {len(remove_land_generic)} generic land/country terms:")
for term in remove_land_generic:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Too generic land/country term, not colonial land ownership'
        print(f"  - '{term}'")

# ACADEMIC DISCIPLINES ≠ LABOR DISCIPLINING
remove_academic_discipline = [
    'interdisciplinaire',  # interdisciplinary (academic)
    'discipline-',  # fragment
    'interdisciplinair',  # interdisciplinary
]

print(f"\nRemoving {len(remove_academic_discipline)} academic discipline terms (NOT labor control):")
for term in remove_academic_discipline:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Semantic drift - academic disciplines ≠ labor disciplining'
        print(f"  - '{term}'")

# GENERIC CONSTRUCTION/HOUSING from "grondbezit"
remove_construction = [
    'bouwgrond',  # building land - urban planning
    'woningbouw',  # housing construction
    'vastgoed-',  # fragment
    'woningen',  # houses/dwellings - generic
    'vastgoed',  # real estate - modern commercial
    'bouwde',  # built - generic verb
]

print(f"\nRemoving {len(remove_construction)} generic construction/housing terms:")
for term in remove_construction:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Generic construction/housing, not colonial land ownership'
        print(f"  - '{term}'")

# GENERIC CONTRACT TERMS from "contractarbeid"
remove_contract_generic = [
    'contract',  # contract - ultra-generic, df 40
    'contracten',  # contracts - generic
    'contractant',  # contractor - generic legal
]

print(f"\nRemoving {len(remove_contract_generic)} generic contract terms:")
for term in remove_contract_generic:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Too generic contract term, not specific to colonial contract labor'
        print(f"  - '{term}'")

# GENERIC LABOR/WORK TERMS
remove_labor_generic = [
    'arbeid',  # labor/work - ultra-generic, df 125!
    'arbeids-',  # fragment
]

print(f"\nRemoving {len(remove_labor_generic)} generic labor/work terms:")
for term in remove_labor_generic:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Too generic labor term, ultra-high df'
        print(f"  - '{term}'")

# FRAGMENTS ALREADY FLAGGED
remove_fragments = [
    'staats-',  # already flagged
    'loon-',  # fragment
]

print(f"\nRemoving {len(remove_fragments)} remaining fragments:")
for term in remove_fragments:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Fragment/prefix'
        print(f"  - '{term}'")

# OTHER GENERIC TERMS
remove_other_generic = [
    'bezit',  # possession - ultra-generic, df 79
    'loon',  # wage - generic
    'eigendom',  # property - generic, df 53
    'verhouding',  # relation/ratio - too generic without prefix
    'streek',  # region - geographic
    'eigenaren',  # owners - ultra-generic, df 113
]

print(f"\nRemoving {len(remove_other_generic)} other generic terms:")
for term in remove_other_generic:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Too generic, ultra-high df'
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

# Save
output_file = r'C:\Users\Home\policy-analysis\arbeid_afhankelijkheid_MANUAL_CURATED.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\nSaved full curation: {output_file}")

final_dict = df[df['action'] != 'REMOVE'][['term', 'parent', 'new_category', 'new_weight', 'cosine', 'df', 'manual_notes']].copy()
final_dict.columns = ['term', 'parent', 'category', 'weight', 'cosine', 'df', 'curation_notes']

final_output = r'C:\Users\Home\policy-analysis\arbeid_afhankelijkheid_FINAL_MANUAL.csv'
final_dict.to_csv(final_output, index=False, encoding='utf-8-sig')
print(f"Saved final dictionary: {final_output}")

print(f"\n{'='*80}")
print("MANUAL CURATION COMPLETE FOR ARBEID_AFHANKELIJKHEID")
print(f"{'='*80}")
