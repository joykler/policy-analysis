import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("KONINKRIJKS_MACHT - APPLYING MANUAL SEMANTIC CURATION")
print("="*80)

# Load expanded terms
df = pd.read_csv(r'C:\Users\Home\policy-analysis\koninkrijks_macht_manual_review.csv', encoding='utf-8-sig')
print(f"Total expanded terms to review: {len(df)}")

# Add decision columns
df['action'] = 'KEEP'
df['new_category'] = df['category']
df['new_weight'] = df['weight']
df['manual_notes'] = ''

# SEMANTIC DRIFT REMOVALS - "zelfbeschikking" over-expansion
# Many "zelf-" (self) terms that are NOT about political self-determination

remove_zelf_drift = [
    'zelfidentiteit',  # self-identity, not self-determination
    'zelfreflectie',   # self-reflection
    'zelfcensuur',     # self-censorship
    'henzelf', 'onszelf', 'mijzelf', 'jezelf', 'zichzelf', 'mezelf',  # reflexive pronouns!
    'zelfbeelden', 'zelfbeeld',  # self-image
    'zelfgenoegzame',  # self-satisfied
    'zelf-',           # fragment
    'zelfvertrouwen',  # self-confidence
    'zelfbewustzijn',  # self-awareness
    'vanzelfsprekende',  # self-evident/obvious
    'zelforganisatie',  # self-organization (borderline but too generic)
]

print(f"\nRemoving {len(remove_zelf_drift)} semantic drift terms from 'zelfbeschikking' parent:")
for term in remove_zelf_drift:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = f'Semantic drift from zelfbeschikking - not about political self-determination'
        print(f"  - '{term}'")

# GENERIC GOVERNANCE TERMS (not Kingdom-specific)

remove_generic_governance = [
    'verhoudingen',        # relations/ratios - too generic alone
    'gezagvoerder',        # commander (airline/ship) - not Kingdom governance
    'gouvernement',        # government - too generic
    'nationalistisch',     # nationalist - generic ideology
    'nationalisme',        # nationalism
    'provinciaal', 'provinciale',  # provincial - Dutch provinces, not Kingdom islands!
    'gelegenheid',         # occasion/opportunity - not governance!
    'sociaal-',            # fragment
    'machtsstructuur',     # generic power structure
    'machtsevenwicht',     # generic balance of power
    'samenwerkingsverbanden',  # generic cooperation
    'overeenkomsten',      # agreements - too generic
    'bondgenootschappen',  # alliances - too generic
    'alliantie',           # alliance
    'genootschap',         # society/association
]

print(f"\nRemoving {len(remove_generic_governance)} generic governance terms:")
for term in remove_generic_governance:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Too generic - not Kingdom-specific governance'
        print(f"  - '{term}'")

# GENERIC BELEID TERMS (too generic administrative)

remove_generic_beleid = [
    'beleidsevaluatie',    # generic policy evaluation
    'validatie', 'validiteit',  # validation/validity - research terms
    'beleidsconclusies',   # policy conclusions
    'interesse',           # interest - generic word!
    'bestuur-',            # fragment
    'onmenselijkheid',     # inhumanity - semantic drift from ongelijkwaardigheid
    'rechtshandhaving',    # law enforcement - too generic
    'overheids-',          # fragment
    'bevlogenheid',        # enthusiasm - not governance!
    'relatie',             # relationship - too generic alone
    'selijkheid',          # fragment
    'ordening',            # ordering/arrangement
    'redelijkheid',        # reasonableness - generic principle
    'mogendheid',          # great power - too generic
    'interactie', 'interacties',  # interaction
    'kwantiteit',          # quantity - measurement term!
    'beveiliging',         # security - too generic
    'controleerden', 'controleerde',  # controlled - generic verbs
    'onderhoud',           # maintenance - too generic
    'onverschilligheid',   # indifference
    'waardigheid',         # dignity
    'zedelijkheid',        # morality
    'nalatigheid',         # negligence
    'kwetsbaarheid',       # vulnerability
    'beambten',            # officials - too generic
    '-beleid',             # fragment
    'autoriteit',          # authority - too generic
    'handhaving',          # enforcement - too generic
    'beheerste',           # controlled/managed
    'beleidsprogramma',    # policy program - too generic
    'beheer',              # management - too generic
    'beheersen', 'beheersing', 'beheersten',  # manage/control - too generic
    'surveillance',        # surveillance - too generic
    'administratie',       # administration - too generic
    'controle', 'controles',  # control/checks - too generic
    'inspectie',           # inspection - too generic
    'bewaking',            # guarding - too generic
    'toebrengt',           # inflicts/applies - verb
]

print(f"\nRemoving {len(remove_generic_beleid)} generic BELEID terms:")
for term in remove_generic_beleid:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Too generic administrative term - not Kingdom-specific'
        print(f"  - '{term}'")

# GENERIC CONTEXT TERMS

remove_generic_context = [
    'instructie-',         # fragment
    'wereldrijk',          # world empire - too generic
    'toelating',           # admission
    'hoog',                # high - adjective
    'midden-',             # middle- prefix
    'onderaan',            # at the bottom
    'geldigheid',          # validity
    'bestuurde',           # governed
    'handreiking',         # guidance
    'verplichting',        # obligation - too generic
    'voorschriften',       # regulations - too generic
    'committee',           # committee - English word, generic
    'volksbuurten',        # working-class neighborhoods
    'high',                # high - English word
    'af-',                 # off/down prefix
    'eilandje',            # little island - diminutive, not specific
    'besluit',             # decision - too generic
    'stadstaat',           # city-state
    'stemming',            # vote/voting
    'derrechten',          # rights fragment
    'bovenal',             # above all
    'rechtvaardiging',     # justification
    'boven',               # above
    'rechtsgeldig',        # legally valid
]

print(f"\nRemoving {len(remove_generic_context)} generic CONTEXT terms:")
for term in remove_generic_context:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Too generic - not Kingdom-specific marker'
        print(f"  - '{term}'")

# VERY LOW COSINE REMOVALS

remove_very_low_cosine = [
    'gekoloniseerd',       # colonized - cosine 0.6042, very low
    'dekoloniserend',      # decolonizing - cosine 0.6123, very low
]

print(f"\nRemoving {len(remove_very_low_cosine)} very low cosine terms:")
for term in remove_very_low_cosine:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Very low cosine + low df'
        print(f"  - '{term}'")

# RECATEGORIZATIONS

# Inequality terms - move to CONTEXT (generic markers, not Kingdom policy)
recategorize_inequality = ['ongelijkheid', 'ongelijkheden', 'ongelijke', 'ongelijk']
print(f"\nRecategorizing inequality terms to CONTEXT ({len(recategorize_inequality)}):")
for term in recategorize_inequality:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'RECATEGORIZE'
        df.loc[idx, 'new_category'] = 'CONTEXT'
        df.loc[idx, 'new_weight'] = 0.6
        df.loc[idx, 'manual_notes'] = 'Generic inequality marker - move to CONTEXT'
        print(f"  - '{term}'")

# Institutional - move to CONTEXT
if 'institutionele' in df['term'].values:
    idx = df[df['term'] == 'institutionele'].index[0]
    df.loc[idx, 'action'] = 'RECATEGORIZE'
    df.loc[idx, 'new_category'] = 'CONTEXT'
    df.loc[idx, 'new_weight'] = 0.6
    df.loc[idx, 'manual_notes'] = 'Generic institutional marker - move to CONTEXT'
    print(f"  - 'institutionele'")

# Financial terms with high df - move to CONTEXT
if 'financiële' in df['term'].values:
    idx = df[df['term'] == 'financiële'].index[0]
    if df.loc[idx, 'df'] > 200:
        df.loc[idx, 'action'] = 'RECATEGORIZE'
        df.loc[idx, 'new_category'] = 'CONTEXT'
        df.loc[idx, 'new_weight'] = 0.6
        df.loc[idx, 'manual_notes'] = 'Ultra-high df (213) - generic financial term'
        print(f"  - 'financiële' (df=213)")

if 'beleid' in df['term'].values:
    idx = df[df['term'] == 'beleid'].index[0]
    if df.loc[idx, 'df'] > 160:
        df.loc[idx, 'action'] = 'RECATEGORIZE'
        df.loc[idx, 'new_category'] = 'CONTEXT'
        df.loc[idx, 'new_weight'] = 0.6
        df.loc[idx, 'manual_notes'] = 'Ultra-high df (163) - generic policy term'
        print(f"  - 'beleid' (df=163)")

# DOWNGRADES

# Low cosine KERN → STERK
downgrade_kern_to_sterk = [
    'gekoloniseerden',  # cosine 0.6879
]

print(f"\nDowngrading KERN → STERK 0.8:")
for term in downgrade_kern_to_sterk:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        if df.loc[idx, 'action'] == 'KEEP':
            df.loc[idx, 'action'] = 'RECATEGORIZE'
            df.loc[idx, 'new_category'] = 'STERK'
            df.loc[idx, 'new_weight'] = 0.8
            df.loc[idx, 'manual_notes'] = 'Low cosine - downgrade to STERK'
            print(f"  - '{term}'")

# Lower weight for low cosine
if 'ex-koloniën' in df['term'].values:
    idx = df[df['term'] == 'ex-koloniën'].index[0]
    df.loc[idx, 'action'] = 'REWEIGHT'
    df.loc[idx, 'new_weight'] = 0.9
    df.loc[idx, 'manual_notes'] = 'Low cosine - KERN 1.0 to 0.9'
    print(f"  - 'ex-koloniën': KERN 1.0 → 0.9")

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
output_file = r'C:\Users\Home\policy-analysis\koninkrijks_macht_MANUAL_CURATED.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\nSaved full curation: {output_file}")

final_dict = df[df['action'] != 'REMOVE'][['term', 'parent', 'new_category', 'new_weight', 'cosine', 'df', 'manual_notes']].copy()
final_dict.columns = ['term', 'parent', 'category', 'weight', 'cosine', 'df', 'curation_notes']

final_output = r'C:\Users\Home\policy-analysis\koninkrijks_macht_FINAL_MANUAL.csv'
final_dict.to_csv(final_output, index=False, encoding='utf-8-sig')
print(f"Saved final dictionary: {final_output}")

print(f"\n{'='*80}")
print("MANUAL CURATION COMPLETE FOR KONINKRIJKS_MACHT")
print(f"{'='*80}")
