import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("KENNIS_HERINNERING - APPLYING MANUAL SEMANTIC CURATION")
print("="*80)

df = pd.read_csv(r'C:\Users\Home\policy-analysis\kennis_herinnering_CORRECTED.csv', encoding='utf-8-sig')
print(f"Total expanded terms to review: {len(df)}")

df['action'] = 'KEEP'
df['new_category'] = df['category']
df['new_weight'] = df['weight']
df['manual_notes'] = ''

# VER- PREFIX DRIFT from "verzwijgen" (concealment)
remove_ver_drift = [
    'verkenning', 'verkennen',  # exploration - OPPOSITE!
    'verzuiling',  # pillarization (sociology term)
    'beweren',  # to claim
    'verzoening',  # reconciliation
    'beperken',  # to limit
    'verhinderen',  # to prevent
    'verrijken',  # to enrich - OPPOSITE!
    'vervullen',  # to fulfill
    'verwezenlijking',  # realization
    'verwerken',  # to process
    'verpligting',  # typo for obligation
    'verduurzamen',  # to sustain
    'verankering',  # anchoring
    'beseften',  # realized/understood
    'afspiegeling',  # reflection
    'verlenen',  # to grant
    'vereenigen',  # to unite
    'versterken',  # to strengthen
    'verwierven',  # acquired
    'verhuren',  # to rent
    'vergeleken',  # compared
    'vernietiging',  # destruction
    'vergeving',  # forgiveness
    'vergelding',  # retaliation
    'zagen',  # saws/saw (verb)
    'verkennend', 'verkennende',  # exploratory
]

print(f"\nRemoving {len(remove_ver_drift)} ver- prefix drift from 'verzwijgen':")
for term in remove_ver_drift:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'ver- prefix drift, not about concealing slavery history'
        print(f"  - '{term}'")

# ONT-/VER- PREFIX DRIFT from "ontkenning" (denial)
remove_ont_drift = [
    'onderkennen',  # to recognize - OPPOSITE!
    'verweten',  # blamed
    'bekennen',  # to confess - borderline
    'ontdekking',  # discovery
    'ondervinding',  # experience
    'verjaring',  # expiration/statute of limitations
    'bepaling',  # determination
    'schepping',  # creation
    'verkent',  # explores
    'ontdekken',  # to discover
    'verbastering',  # corruption/bastardization
    'overtuiging',  # conviction/belief
    'veronderstelling',  # assumption
    'ontheffing',  # exemption
]

print(f"\nRemoving {len(remove_ont_drift)} ont-/ver- prefix drift from 'ontkenning':")
for term in remove_ont_drift:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'ont-/ver- prefix drift, not about denial of slavery'
        print(f"  - '{term}'")

# HER- PREFIX DRIFT from "herdenken" (commemoration)
remove_her_drift = [
    'herkennen',  # to recognize (visual)
    'herkende', 'herkent', 'herkenbare', 'herkend',  # recognized
    'nadenken',  # to think
    'herschikking',  # rearrangement
    'herijking',  # recalibration
    'bekeren',  # to convert (religious)
    'herhaling',  # repetition
    'herhaalt',  # repeats
]

print(f"\nRemoving {len(remove_her_drift)} her- prefix drift from 'herdenken':")
for term in remove_her_drift:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'her- prefix drift (recognition/repetition), not commemoration'
        print(f"  - '{term}'")

# GENERIC HISTORY TERMS
remove_history_generic = [
    'historical', 'history',  # English!
    'historische',  # df 120 - ultra-generic
    'historisch',  # df 83 - ultra-generic
    'geschiedenis',  # df 316 - ultra-generic
    'geografie',  # geography - wrong discipline!
    'schiedenis',  # typo
    'kunsthistorici',  # art historians - generic
    'historie',  # history - generic
    'geschiedenissen',  # histories - generic
]

print(f"\nRemoving {len(remove_history_generic)} generic history/geography terms:")
for term in remove_history_generic:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Generic history term or ultra-high df'
        print(f"  - '{term}'")

# ULTRA-HIGH DF TERMS
remove_ultra_high_df = [
    'bewust',  # df 108 - aware
    'kennis',  # df 208 - knowledge
    'koloniale',  # df 524 - ultra-generic
    'beeld',  # df 277 - image
    'kennen',  # df 78 - to know
    'historicus',  # df 72 - historian (generic)
]

print(f"\nRemoving {len(remove_ultra_high_df)} ultra-high df terms:")
for term in remove_ultra_high_df:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = f'Ultra-high df ({df.loc[idx, "df"]}), too generic'
        print(f"  - '{term}' (df={df.loc[idx, 'df']})")

# GENERIC EDUCATION/CURRICULUM
remove_education_generic = [
    'beroepsopleiding',  # vocational training
    'beroepsonderwijs',  # vocational education
    'opleidingstrajecten',  # training paths
    'lerarenopleiding',  # teacher training
]

print(f"\nRemoving {len(remove_education_generic)} generic education/curriculum terms:")
for term in remove_education_generic:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Generic education administration, not slavery education-specific'
        print(f"  - '{term}'")

# FRAGMENTS
remove_fragments = [
    'bewustwordingspro-',
    'koloniale-',
    'slavernij-',
    'kennis-',
]

print(f"\nRemoving {len(remove_fragments)} fragments:")
for term in remove_fragments:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Fragment/prefix'
        print(f"  - '{term}'")

# OTHER GENERIC
remove_other_generic = [
    'materiaal', 'materialen',  # materials - too generic
    'beelden',  # images - too generic
    'lessen',  # lessons - too generic
    'schrift',  # writing/scripture - generic
    'benadering',  # approach - generic, df 31
]

print(f"\nRemoving {len(remove_other_generic)} other generic terms:")
for term in remove_other_generic:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Too generic'
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
output_file = r'C:\Users\Home\policy-analysis\kennis_herinnering_MANUAL_CURATED.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\nSaved full curation: {output_file}")

final_dict = df[df['action'] != 'REMOVE'][['term', 'parent', 'new_category', 'new_weight', 'cosine', 'df', 'manual_notes']].copy()
final_dict.columns = ['term', 'parent', 'category', 'weight', 'cosine', 'df', 'curation_notes']

final_output = r'C:\Users\Home\policy-analysis\kennis_herinnering_FINAL_MANUAL.csv'
final_dict.to_csv(final_output, index=False, encoding='utf-8-sig')
print(f"Saved final dictionary: {final_output}")

print(f"\n{'='*80}")
print("MANUAL CURATION COMPLETE FOR KENNIS_HERINNERING")
print(f"{'='*80}")
