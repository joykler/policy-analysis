import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("ERKENNING_VERANTWOORDELIJKHEID - APPLYING MANUAL SEMANTIC CURATION")
print("="*80)

df = pd.read_csv(r'C:\Users\Home\policy-analysis\erkenning_verantwoordelijkheid_CORRECTED.csv', encoding='utf-8-sig')
print(f"Total expanded terms to review: {len(df)}")

df['action'] = 'KEEP'
df['new_category'] = df['category']
df['new_weight'] = df['weight']
df['manual_notes'] = ''

# FINANCIAL DEBT TERMS (schuld = debt, not guilt)
remove_financial_debt = [
    'schulden',  # debts (financial)
    'schuldhulpverlening',  # debt assistance
    'schuldenproblematiek',  # debt problems
    'staatsschuld',  # state debt (government finance)
    'schuldenaren',  # debtors
    'studieschuld',  # student debt
]

print(f"\nRemoving {len(remove_financial_debt)} financial debt terms (NOT guilt):")
for term in remove_financial_debt:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Financial debt, not moral/historical guilt'
        print(f"  - '{term}'")

# GENERIC RECOVERY/RENOVATION
remove_recovery_generic = [
    'renovatie',  # renovation (buildings)
    'herinrichting',  # reorganization/refurbishment
    'ontslagen',  # dismissed/fired - NOT restoration!
    'recovery',  # English word
]

print(f"\nRemoving {len(remove_recovery_generic)} generic recovery/renovation terms:")
for term in remove_recovery_generic:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Generic recovery/renovation, not historical redress'
        print(f"  - '{term}'")

# GENERIC LEGAL/JUDICIAL TERMS
remove_legal_generic = [
    'recht',  # law/right - df 146!
    'rechtspraak',  # judiciary
    'rechtspleging',  # legal proceedings
    'recht-',  # fragment
    'rechtshulp',  # legal aid
    'rechtsbescherming',  # legal protection
    'rechtssysteem',  # legal system
    'rechtsorde',  # legal order
    'rechtspositie',  # legal position
    'rechtmatigheid',  # legality
    'wederrechtelijkheid',  # unlawfulness
    'rechtvaardigingen',  # justifications
    'oprechtheid',  # sincerity
    'rechtvaardig',  # just/fair
    'rechtvaardige',  # just/fair
    'rechtvaardigingsgrond',  # justification ground
    'vaardigheid',  # skill! (from recht-vaardigheid)
]

print(f"\nRemoving {len(remove_legal_generic)} generic legal/judicial terms:")
for term in remove_legal_generic:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Generic legal/judicial term, not historical justice-specific'
        print(f"  - '{term}'")

# CONTROL/MANAGEMENT (not accountability)
remove_control = [
    'beheersen',  # to control
    'beheersten',  # controlled
    'beheersing',  # control/mastery
    'bewaking',  # guarding/monitoring
    'beheerste',  # controlled/moderate
]

print(f"\nRemoving {len(remove_control)} control/management terms (NOT accountability):")
for term in remove_control:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Control/management, not accountability'
        print(f"  - '{term}'")

# GENERIC ERKENNING EXPANSIONS
remove_erkenning_generic = [
    'werven',  # to recruit - NOT recognition!
    'ties',  # English or fragment
    'stelling',  # statement/position
    'verminderde',  # decreased
    'afhandeling',  # settlement/handling
    'proef',  # test/trial
    'voorbereid',  # prepared
    'speelt',  # plays - df 87!
    'verstrekking',  # provision/supply
    'stellen',  # to state - df 209!
    'verre',  # far
    'neer',  # down
    'maatregel',  # measure - df 30
    'woordenboek',  # dictionary!
]

print(f"\nRemoving {len(remove_erkenning_generic)} generic erkenning expansions:")
for term in remove_erkenning_generic:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Generic verb/noun, not recognition-specific'
        print(f"  - '{term}'")

# GENERIC STATE TERMS
remove_state_generic = [
    'staatsexamens',  # state exams (education!)
    'staatswijsheid',  # statesmanship
    'staatssteun',  # state aid (EU law)
    'historische',  # historical - df 120, ultra-generic
    'staats-',  # fragment
    'staat-',  # fragment
]

print(f"\nRemoving {len(remove_state_generic)} generic state terms:")
for term in remove_state_generic:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Generic state/government term or ultra-high df'
        print(f"  - '{term}'")

# OBSTACLES/INSURANCE (not liability)
remove_obstacles = [
    'belemmeringen',  # obstacles
    'belemmering',  # obstacle
    'verzekerd',  # insured (insurance)
]

print(f"\nRemoving {len(remove_obstacles)} obstacles/insurance terms (NOT liability):")
for term in remove_obstacles:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Obstacles or insurance, not legal liability'
        print(f"  - '{term}'")

# FRAGMENTS
remove_fragments = [
    'herstel-',
    'reken-',
    'slavernij-',  # could be compound but safer to remove fragment
]

print(f"\nRemoving {len(remove_fragments)} fragments:")
for term in remove_fragments:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Fragment/prefix'
        print(f"  - '{term}'")

# ULTRA-HIGH DF REMAINING
remove_ultra_high_df = [
    'vertrouwen',  # trust - df 70, too generic
]

print(f"\nRemoving {len(remove_ultra_high_df)} ultra-high df terms:")
for term in remove_ultra_high_df:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = f'Ultra-high df ({df.loc[idx, "df"]}), too generic'
        print(f"  - '{term}' (df={df.loc[idx, 'df']})")

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
output_file = r'C:\Users\Home\policy-analysis\erkenning_verantwoordelijkheid_MANUAL_CURATED.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\nSaved full curation: {output_file}")

final_dict = df[df['action'] != 'REMOVE'][['term', 'parent', 'new_category', 'new_weight', 'cosine', 'df', 'manual_notes']].copy()
final_dict.columns = ['term', 'parent', 'category', 'weight', 'cosine', 'df', 'curation_notes']

final_output = r'C:\Users\Home\policy-analysis\erkenning_verantwoordelijkheid_FINAL_MANUAL.csv'
final_dict.to_csv(final_output, index=False, encoding='utf-8-sig')
print(f"Saved final dictionary: {final_output}")

print(f"\n{'='*80}")
print("MANUAL CURATION COMPLETE FOR ERKENNING_VERANTWOORDELIJKHEID")
print(f"{'='*80}")
