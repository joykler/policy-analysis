import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("RACIALE_HIERARCHIE - APPLYING MANUAL SEMANTIC CURATION")
print("="*80)

df = pd.read_csv(r'C:\Users\Home\policy-analysis\raciale_hierarchie_manual_review.csv', encoding='utf-8-sig')
print(f"Total expanded terms to review: {len(df)}")

df['action'] = 'KEEP'
df['new_category'] = df['category']
df['new_weight'] = df['weight']
df['manual_notes'] = ''

# VERY LOW COSINE KERN TERMS
remove_very_low_cosine = [
    'hiërarchie', 'hiërarchieën',  # hierarchy - too generic, very low cosine
    'persoonskenmerken',  # personal characteristics - too generic
    'rassenverhoudingen',  # race relations - low cosine, low df
]

print(f"\nRemoving {len(remove_very_low_cosine)} very low cosine KERN terms:")
for term in remove_very_low_cosine:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Very low cosine (<0.59) + too generic or low df'
        print(f"  - '{term}'")

# SEMANTIC DRIFT FROM "segregatie" - generic organization/grouping terms
remove_segregatie_drift = [
    'organisation', 'population',  # English words, not Dutch!
    'werkgroep',  # work group - generic
    'verbouw', 'verbouwen',  # renovation/remodeling - NOT segregation!
    'herschikking',  # rearrangement - generic
    'gemeenschappen',  # communities - too generic alone
    'distributie',  # distribution - generic
    'verspreiden', 'verspreiding',  # distribute/distribution - generic
    'groeperingen',  # groups - generic
    'formatie',  # formation - generic
    'coöperatie',  # cooperation - generic
    'kolonisatie-', 'kolonisatie', 'koloniseren',  # colonization - different topic!
    'samenkomst',  # meeting - generic
    'wederopbouw',  # reconstruction - generic
    'reformatie',  # reformation - religious/generic
    'georganiseerd', 'georganiseerde',  # organized - generic
    'meerderheid', 'meerderheidsgroep',  # majority - too generic
    'splitsing',  # split - generic
    'verbieden',  # prohibit - generic verb
    'omzwervingen',  # wanderings - generic
    'nederzetting',  # settlement - generic
    'rederij',  # shipping company - NOT segregation!
    'ontplooiing',  # development - generic
    'afwisseling',  # alternation - generic
    'associatie',  # association - generic
    'meebouwen',  # build along - generic
    'afvaardiging',  # delegation - generic
    'afname',  # decrease - generic
    'vereenvoudigen',  # simplify - generic
    'genereren',  # generate - generic
    'afbouw',  # reduction/dismantling - generic
    'geformeerd',  # formed - generic
    'vervorming',  # distortion - generic
    'verzameling',  # collection - generic
    'compagnie',  # company - generic
    'generaties',  # generations - too generic
    'uitsplitsing',  # breakdown - generic
    'omzetting',  # conversion - generic
    'herverdeling',  # redistribution - generic economic term
    'samenvoeging',  # merger - generic
    'opsplitsing',  # split-up - generic
    'toenemen',  # increase - verb
    'afschaffing',  # abolition - could be relevant but not segregation-specific
]

print(f"\nRemoving {len(remove_segregatie_drift)} semantic drift from 'segregatie':")
for term in remove_segregatie_drift:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Semantic drift - generic organization/grouping, not racial segregation'
        print(f"  - '{term}'")

# SEMANTIC DRIFT FROM "achterstelling" - spatial/temporal position terms
remove_achterstelling_drift = [
    'vooraan', 'voorgetrokken', 'voorgrond', 'voorstander', 'vooren',  # in front/forward
    'stelling',  # position/statement - too generic
    'bestel',  # system - too generic
    'opeenvolging',  # succession - temporal
    'vervaardiging',  # manufacturing - NOT disadvantage!
    'vooruitlopend', 'vooruit',  # forward/ahead - spatial
    'achtereenvolgens',  # successively - temporal sequence
    'voorhoeve',  # on behalf of - legal term
    'vooruitzicht',  # prospect - expectation
    'voorhang', 'voorhand',  # beforehand - temporal
    'voorval',  # incident - generic
    'opvolging',  # succession - temporal
    'navolging',  # emulation - imitation
    'voorzagen',  # foresaw - verb
    'hoede',  # care/custody - protection
    'voorafgaande', 'voorafging',  # preceding - temporal
    'erachter',  # behind it - spatial
    'voorvechter',  # advocate/champion - positive term!
    'achtervolging',  # pursuit/persecution - could be relevant but indirect
    'achterste',  # rear/back - spatial
    'achteruitgang',  # decline - could be relevant but very indirect
    'voorloper',  # forerunner - positive term!
    'voordragt',  # nomination - administrative
    'voortrekker',  # pioneer - positive!
    'achterliggende',  # underlying/behind - spatial/causal
    'achterblijven', 'achterblijvende', 'achterblijvers',  # lag behind - could be relevant but indirect
]

print(f"\nRemoving {len(remove_achterstelling_drift)} semantic drift from 'achterstelling':")
for term in remove_achterstelling_drift:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Semantic drift - spatial/temporal position, not social disadvantage'
        print(f"  - '{term}'")

# SEMANTIC DRIFT FROM "uitsluiting" - "uit-" prefix (out/exit) terms
remove_uitsluiting_drift = [
    'uitwisselingen',  # exchanges - generic
    'uitdragen',  # carry out - generic verb
    'uitwerking',  # effect/working out - too generic
    'onthulling',  # revelation - generic
    'onttrekken',  # withdraw - generic
    'uitging',  # went out - verb
    'uit-', 'uitvoe-', 'uitge-',  # fragments/prefixes
    'afzet',  # sales/deposition - NOT exclusion!
    'uitbreken',  # break out - generic
    'uitstek',  # protrusion/excellence - NOT exclusion!
    'uitstroom',  # outflow - generic
    'aansluitende', 'aangesloten',  # connecting/connected - OPPOSITE of exclusion!
    'opluchting',  # relief - emotion
    'uitbannen',  # eradicate - could be relevant to fighting exclusion
    'uitlatingen',  # statements - generic
    'uitmaken',  # matter/constitute - generic
    'uitnodigen',  # invite - OPPOSITE of exclusion!
    'voortrekken',  # prefer/pull forward - preferential treatment
    'afkeer',  # aversion - emotion, not policy
    'uitstrekt',  # extends - spatial
    'uitroeiing',  # eradication - violence term
    'uitreden',  # ride out - verb
    'verstreken',  # elapsed/expired - temporal
    'aangrenzende',  # adjacent - spatial
    'aantrekken',  # attract - OPPOSITE of exclusion!
    'aaneenschakeling',  # linkage - connection
    'intrekken',  # withdraw/retract - generic
    'afhandeling',  # handling/settlement - administrative
    'uitgezet',  # deported - could be relevant (deportation = exclusion)
    'opgesloten',  # imprisoned - confinement, not social exclusion
]

print(f"\nRemoving {len(remove_uitsluiting_drift)} semantic drift from 'uitsluiting':")
for term in remove_uitsluiting_drift:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Semantic drift - uit- prefix (exit/out), not social exclusion'
        print(f"  - '{term}'")

# GENERIC DISCRIMINATION/RACISM TERMS
remove_generic_racism = [
    'nationalisme', 'nationalistische', 'nationalistisch',  # nationalism - too generic
    'fascisme',  # fascism - different ideology
    'conformisme',  # conformism - generic
    'nische',  # fragment
    'commotie',  # commotion - generic
    'cultureel-politieke',  # cultural-political - too generic
]

print(f"\nRemoving {len(remove_generic_racism)} generic racism/ideology terms:")
for term in remove_generic_racism:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Too generic political/ideological term'
        print(f"  - '{term}'")

# OTHER PROBLEMATIC TERMS
other_removes = [
    'verfstof',  # paint substance - NOT colorism!
    'antisemitisme',  # anti-Semitism - different form of discrimination
    'zwangerschapsdiscriminatie',  # pregnancy discrimination - gender issue
]

print(f"\nRemoving {len(other_removes)} other problematic terms:")
for term in other_removes:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'REMOVE'
        df.loc[idx, 'manual_notes'] = 'Wrong domain or semantic drift'
        print(f"  - '{term}'")

# KEEP BUT RECATEGORIZE
# Very generic structural terms → CONTEXT
recategorize_context = ['structurele']  # structural - very generic, very high df

print(f"\nRecategorizing to CONTEXT:")
for term in recategorize_context:
    if term in df['term'].values:
        idx = df[df['term'] == term].index[0]
        df.loc[idx, 'action'] = 'RECATEGORIZE'
        df.loc[idx, 'new_category'] = 'CONTEXT'
        df.loc[idx, 'new_weight'] = 0.6
        df.loc[idx, 'manual_notes'] = f'Ultra-high df ({df.loc[idx, "df"]}) - too generic, move to CONTEXT'
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

# Save
output_file = r'C:\Users\Home\policy-analysis\raciale_hierarchie_MANUAL_CURATED.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\nSaved full curation: {output_file}")

final_dict = df[df['action'] != 'REMOVE'][['term', 'parent', 'new_category', 'new_weight', 'cosine', 'df', 'manual_notes']].copy()
final_dict.columns = ['term', 'parent', 'category', 'weight', 'cosine', 'df', 'curation_notes']

final_output = r'C:\Users\Home\policy-analysis\raciale_hierarchie_FINAL_MANUAL.csv'
final_dict.to_csv(final_output, index=False, encoding='utf-8-sig')
print(f"Saved final dictionary: {final_output}")

print(f"\n{'='*80}")
print("MANUAL CURATION COMPLETE FOR RACIALE_HIERARCHIE")
print(f"{'='*80}")
