"""
Create v10 optimized dictionary based on v9 framework
Reduces 8 topics to 6 by merging overlapping concepts
"""

import pandas as pd
from pathlib import Path

# Load v9 as base
v9_path = Path(r"C:\Users\Home\policy-analysis\dictionairy\Slaverylegacy_dictionaryv9_FIXED.xlsx")
df_v9 = pd.read_excel(v9_path)

print(f"Loaded v9: {len(df_v9)} terms across {df_v9['topic'].nunique()} topics")

# New 6-topic framework with redistributed terms
v10_data = []

# Topic 1: Slavernij_Koloniaal_Systeem (29 terms)
# Merged: Benaming_Verleden slavery terms + Koninkrijks_Macht colonial structures
slavery_colonial = [
    ('slavernij', 1.00),
    ('slavernijverleden', 1.00),
    ('slavernijgeschiedenis', 0.95),
    ('slavenhandel', 1.00),
    ('trans-Atlantische slavenhandel', 1.00),
    ('VOC-slavernij', 0.95),
    ('WIC-slavernij', 0.95),
    ('plantage-economie', 0.95),
    ('plantagesysteem', 0.95),
    ('koloniale exploitatie', 0.95),
    ('koloniale verhoudingen', 1.00),
    ('koloniaal bestuur', 0.95),
    ('WIC', 0.90),
    ('VOC', 0.90),
    ('Nederlandse Antillen', 0.85),
    ('Suriname', 0.85),
    ('Curaçao', 0.80),
    ('slavenregister', 0.90),
    ('emancipatie', 0.95),
    ('abolitionisme', 0.90),
    ('Keti Koti', 1.00),
    ('1 juli 1863', 0.95),
    ('Tula-opstand', 0.90),
    ('slavenverzet', 0.95),
    ('marrons', 0.90),
    ('Middle Passage', 0.90),
    ('Elmina', 0.85),
    ('Fort Nassau', 0.80),
    ('Koninkrijk der Nederlanden', 0.85),
]

for term, weight in slavery_colonial:
    v10_data.append({
        'topic': 'Slavernij_Koloniaal_Systeem',
        'term': term,
        'cosine': 1.0,
        'df': 0,
        'weight': weight,
        'category': 'strong_problem',
        'parent': term,
        'is_seed': 1
    })

# Topic 2: Macht_Afhankelijkheid (33 terms)
# Merged: Koninkrijks_Macht power terms + Arbeid_Land_Eigendom
power_dependency = [
    ('asymmetrische macht', 0.95),
    ('machtsasymmetrie', 0.95),
    ('machtsongelijkheid', 0.95),
    ('machtsverhoudingen', 0.95),
    ('hiërarchische relaties', 0.90),
    ('afhankelijkheid', 0.95),
    ('economische afhankelijkheid', 0.95),
    ('politieke afhankelijkheid', 0.90),
    ('staatstoezicht', 1.00),
    ('contractarbeid', 0.95),
    ('arbeidsdwang', 0.95),
    ('gedwongen arbeid', 0.95),
    ('landeigendom', 0.90),
    ('grondbezit', 0.90),
    ('eigendomsrechten', 0.85),
    ('schuldslavernij', 0.95),
    ('peonage', 0.90),
    ('coolie-stelsel', 0.95),
    ('Javaanse contractarbeiders', 0.85),
    ('Hindostaanse contractarbeiders', 0.85),
    ('patronage', 0.85),
    ('cliëntelisme', 0.85),
    ('extractie', 0.90),
    ('uitbuiting', 0.95),
    ('dwang', 0.90),
    ('onvrijheid', 0.95),
    ('suikerplantages', 0.85),
    ('bauxietmijnen', 0.80),
    ('cultuurstelsel', 0.90),
    ('dwangteelt', 0.90),
    ('verplichte leveranties', 0.85),
    ('belastingdruk', 0.80),
    ('herendiensten', 0.85),
]

for term, weight in power_dependency:
    v10_data.append({
        'topic': 'Macht_Afhankelijkheid',
        'term': term,
        'cosine': 1.0,
        'df': 0,
        'weight': weight,
        'category': 'strong_problem',
        'parent': term,
        'is_seed': 1
    })

# Topic 3: Raciale_Hierarchie (19 terms)
# Kept from Raciale_Ordening (clear concept, no overlap)
racial_hierarchy = [
    ('raciale hiërarchie', 1.00),
    ('raciale classificatie', 0.95),
    ('rassendenken', 0.95),
    ('kleurenhiërarchie', 0.95),
    ('witheid', 0.90),
    ('zwaartheid', 0.90),
    ('blank-zwart dichotomie', 0.95),
    ('superioriteitsclaims', 0.90),
    ('inferioriteitsclaims', 0.90),
    ('bloedquantum', 0.85),
    ('miscegenatie', 0.85),
    ('kleurenlijn', 0.95),
    ('pigmentocracy', 0.90),
    ('colorisme', 0.90),
    ('huidskleurisme', 0.90),
    ('etnische stratificatie', 0.90),
    ('raciaal onderscheid', 0.95),
    ('raciaal denken', 0.95),
    ('wetenschappelijk racisme', 0.90),
]

for term, weight in racial_hierarchy:
    v10_data.append({
        'topic': 'Raciale_Hierarchie',
        'term': term,
        'cosine': 1.0,
        'df': 0,
        'weight': weight,
        'category': 'strong_problem',
        'parent': term,
        'is_seed': 1
    })

# Topic 4: Doorwerking_Continuiteit (24 terms)
# Merged: Structurele_Doorwerking + Depolitisering_Distantiering
continuation = [
    ('structurele doorwerking', 1.00),
    ('pad-afhankelijkheid', 0.95),
    ('institutionele continuïteit', 0.95),
    ('nalatenschap', 0.95),
    ('legacy', 0.95),
    ('postkoloniale situatie', 0.95),
    ('postkolonialisme', 0.90),
    ('neokolonialisme', 0.90),
    ('persistentie', 0.90),
    ('reproductie', 0.90),
    ('depolitisering', 0.95),
    ('distantiering', 0.95),
    ('neutralisering', 0.90),
    ('temporalisering', 0.90),
    ('historisering', 0.85),
    ('externalisering', 0.90),
    ('geografische afstand', 0.80),
    ('temporele afstand', 0.85),
    ('morele afstand', 0.85),
    ('vervreemding', 0.85),
    ('normalisering', 0.90),
    ('naturalisering', 0.90),
    ('ontkenning', 0.90),
    ('vergetelpolitiek', 0.95),
]

for term, weight in continuation:
    v10_data.append({
        'topic': 'Doorwerking_Continuiteit',
        'term': term,
        'cosine': 1.0,
        'df': 0,
        'weight': weight,
        'category': 'strong_problem',
        'parent': term,
        'is_seed': 1
    })

# Topic 5: Erkenning_Verantwoordelijkheid (24 terms)
# Kept from Toerekening_Verantwoordelijkheid (clear concept)
recognition = [
    ('erkenning', 1.00),
    ('erkentelijkheid', 0.95),
    ('verantwoordelijkheid', 1.00),
    ('toerekening', 0.95),
    ('aansprakelijkheid', 0.95),
    ('schuld', 0.90),
    ('schuldbewustzijn', 0.90),
    ('schaamte', 0.85),
    ('historische verantwoordelijkheid', 0.95),
    ('morele verantwoordelijkheid', 0.95),
    ('politieke verantwoordelijkheid', 0.90),
    ('reparaties', 1.00),
    ('herstelbetalingen', 0.95),
    ('compensatie', 0.95),
    ('genoegdoening', 0.90),
    ('excuses', 0.95),
    ('officiële excuses', 0.95),
    ('rechtvaardigheid', 0.90),
    ('transitional justice', 0.90),
    ('herstelrecht', 0.90),
    ('verantwoording', 0.90),
    ('rekenschap', 0.90),
    ('accountability', 0.85),
    ('historische rechtvaardigheid', 0.95),
]

for term, weight in recognition:
    v10_data.append({
        'topic': 'Erkenning_Verantwoordelijkheid',
        'term': term,
        'cosine': 1.0,
        'df': 0,
        'weight': weight,
        'category': 'strong_problem',
        'parent': term,
        'is_seed': 1
    })

# Topic 6: Kennis_Herinnering (21 terms)
# Kept from Kennis_Archief_Herinnering (clear concept)
knowledge_memory = [
    ('herinnering', 1.00),
    ('collectieve herinnering', 0.95),
    ('herinneringscultuur', 0.95),
    ('geheugenpolitiek', 0.95),
    ('memory studies', 0.85),
    ('archivering', 0.90),
    ('archiefpolitiek', 0.90),
    ('historiografie', 0.90),
    ('geschiedschrijving', 0.90),
    ('canon', 0.85),
    ('nationale canon', 0.85),
    ('onderwijs', 0.85),
    ('geschiedenisonderwijs', 0.90),
    ('educatie', 0.80),
    ('bewustwording', 0.90),
    ('bewustmaking', 0.90),
    ('kennis', 0.85),
    ('kennisproductie', 0.85),
    ('verbeelding', 0.80),
    ('representatie', 0.85),
    ('narratief', 0.85),
]

for term, weight in knowledge_memory:
    v10_data.append({
        'topic': 'Kennis_Herinnering',
        'term': term,
        'cosine': 1.0,
        'df': 0,
        'weight': weight,
        'category': 'strong_problem',
        'parent': term,
        'is_seed': 1
    })

# Create DataFrame
df_v10 = pd.DataFrame(v10_data)

# Summary
print("\n" + "="*80)
print("V10 DICTIONARY CREATED")
print("="*80)
print(f"\nTotal terms: {len(df_v10)}")
print(f"Topics: {df_v10['topic'].nunique()}")
print("\nTerms per topic:")
for topic in df_v10['topic'].unique():
    count = len(df_v10[df_v10['topic'] == topic])
    print(f"  {topic}: {count}")

# Save
output_path = Path(r"C:\Users\Home\policy-analysis\dictionairy\Slaverylegacy_dictionaryv10.xlsx")
df_v10.to_excel(output_path, index=False)
print(f"\n✓ Saved to: {output_path}")

# Compare with v9
print("\n" + "="*80)
print("COMPARISON: v9 → v10")
print("="*80)
print(f"Topics: 8 → 6 ({-2:+d})")
print(f"Total terms: {len(df_v9)} → {len(df_v10)} ({len(df_v10)-len(df_v9):+d})")

print("\nTopic distribution balance:")
print("\nv9 (unbalanced):")
for topic in df_v9['topic'].unique():
    count = len(df_v9[df_v9['topic'] == topic])
    print(f"  {topic}: {count}")

print("\nv10 (improved balance):")
for topic in df_v10['topic'].unique():
    count = len(df_v10[df_v10['topic'] == topic])
    print(f"  {topic}: {count}")

print("\n✓ Dictionary optimization complete!")
