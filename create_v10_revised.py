"""
Create REVISED v10 dictionary - keeping historical category
User insight: Need to differentiate historical segments from contemporary legacy segments
"""

import pandas as pd
from pathlib import Path

# Load v9 as base
v9_path = Path(r"C:\Users\Home\policy-analysis\dictionairy\Slaverylegacy_dictionaryv9_FIXED.xlsx")
df_v9 = pd.read_excel(v9_path)

print(f"Loaded v9: {len(df_v9)} terms across {df_v9['topic'].nunique()} topics")

# REVISED 7-topic framework (keeping historical category)
v10_data = []

# Topic 1: Slavernij_Historisch (KEPT - critical for temporal classification)
# Source: Benaming_Verleden (kept intact with focus on historical events/periods)
# Purpose: Identifies segments discussing historical slavery period (pre-1863, abolition, immediate aftermath)
historical_slavery = [
    ('slavernij', 1.0),
    ('slavernijverleden', 1.0),
    ('slavernijgeschiedenis', 0.9),
    ('slavenhandel', 1.0),
    ('trans-Atlantische slavenhandel', 1.0),
    ('Atlantische slavenhandel', 1.0),
    ('tot slaaf gemaakt', 1.0),
    ('tot slaaf gemaakte', 1.0),
    ('totslaafgemaakt', 0.9),
    ('tot slaaf gemaakten', 1.0),
    ('tot slaaf gemaakten en nazaten', 0.8),
    ('plantage', 0.9),
    ('plantages', 0.9),
    ('plantagesysteem', 0.9),
    ('plantage-economie', 0.9),
    ('slavenhouder', 0.9),
    ('slavenhouders', 0.9),
    ('slavenhouderij', 0.9),
    ('eigendom van personen', 0.9),
    ('bezit van mensen', 0.9),
    ('dwangarbeid', 0.9),
    ('gedwongen arbeid', 0.9),
    ('koloniaal geweld', 0.9),
    ('uitbuiting', 0.8),
    ('roof', 0.6),
    ('roofbouw', 0.8),
    ('ontmenselijking', 0.8),
    ('mensonterende behandeling', 0.8),
    ('misdaad tegen de menselijkheid', 0.8),
    ('emancipatie', 0.9),
    ('afschaffing van de slavernij', 1.0),
    ('afschaffing slavernij', 1.0),
    ('staatstoezicht', 1.0),
    ('staatstoezichtperiode', 0.9),
    ('Middenpassage', 0.6),
    ('slavenschip', 0.6),
    ('slavenmarkt', 0.6),
    ('ketenen', 0.3),
    ('kolonialisme', 1.0),
    ('koloniaal', 0.9),
    ('koloniale geschiedenis', 0.9),
    ('koloniale erfenis', 0.9),
    ('koloniale nalatenschap', 0.9),
    ('koloniaal verleden', 0.9),
    ('postkoloniaal', 0.9),
    ('neokoloniaal', 0.9),
    ('dekolonisatie', 0.9),
    ('dekoloniseren', 0.8),
]

for term, weight in historical_slavery:
    v10_data.append({
        'topic': 'Slavernij_Historisch',
        'keyword': term,
        'weight': weight,
        'category': 'KERN' if weight >= 0.9 else 'STERK'
    })

# Topic 2: Koninkrijks_Macht (KEPT - distinct from power/dependency concept)
# Source: Koninkrijks_Macht (kept intact)
# Purpose: Dutch Kingdom structures and relationships
koninkrijk = df_v9[df_v9['topic'] == 'Koninkrijks_Macht'].copy()
for _, row in koninkrijk.iterrows():
    v10_data.append({
        'topic': 'Koninkrijks_Macht',
        'keyword': row['keyword'],
        'weight': row['weight'],
        'category': row['category']
    })

# Topic 3: Raciale_Hierarchie (KEPT)
# Source: Raciale_Ordening
racial = df_v9[df_v9['topic'] == 'Raciale_Ordening'].copy()
for _, row in racial.iterrows():
    v10_data.append({
        'topic': 'Raciale_Hierarchie',
        'keyword': row['keyword'],
        'weight': row['weight'],
        'category': row['category']
    })

# Topic 4: Arbeid_Afhankelijkheid (SLIGHT RENAME)
# Source: Arbeid_Land_Eigendom (kept intact)
# Purpose: Economic structures of dependency
arbeid = df_v9[df_v9['topic'] == 'Arbeid_Land_Eigendom'].copy()
for _, row in arbeid.iterrows():
    v10_data.append({
        'topic': 'Arbeid_Afhankelijkheid',
        'keyword': row['keyword'],
        'weight': row['weight'],
        'category': row['category']
    })

# Topic 5: Doorwerking_Continuiteit (MERGED)
# Source: Structurele_Doorwerking + Depolitisering_Distantiering
# Purpose: How legacy continues and is obscured
doorwerking = df_v9[df_v9['topic'] == 'Structurele_Doorwerking'].copy()
depol = df_v9[df_v9['topic'] == 'Depolitisering_Distantiering'].copy()
for df_part in [doorwerking, depol]:
    for _, row in df_part.iterrows():
        v10_data.append({
            'topic': 'Doorwerking_Continuiteit',
            'keyword': row['keyword'],
            'weight': row['weight'],
            'category': row['category']
        })

# Topic 6: Erkenning_Verantwoordelijkheid (KEPT)
# Source: Toerekening_Verantwoordelijkheid
erkenning = df_v9[df_v9['topic'] == 'Toerekening_Verantwoordelijkheid'].copy()
for _, row in erkenning.iterrows():
    v10_data.append({
        'topic': 'Erkenning_Verantwoordelijkheid',
        'keyword': row['keyword'],
        'weight': row['weight'],
        'category': row['category']
    })

# Topic 7: Kennis_Herinnering (KEPT)
# Source: Kennis_Archief_Herinnering
kennis = df_v9[df_v9['topic'] == 'Kennis_Archief_Herinnering'].copy()
for _, row in kennis.iterrows():
    v10_data.append({
        'topic': 'Kennis_Herinnering',
        'keyword': row['keyword'],
        'weight': row['weight'],
        'category': row['category']
    })

# Create DataFrame
df_v10 = pd.DataFrame(v10_data)

# Summary
print("\n" + "="*80)
print("V10 REVISED DICTIONARY CREATED")
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
print(f"\nSaved to: {output_path}")

# Compare with v9
print("\n" + "="*80)
print("COMPARISON: v9 -> v10 REVISED")
print("="*80)
print(f"Topics: 8 -> 7 ({-1:+d})")
print(f"Total terms: {len(df_v9)} -> {len(df_v10)} ({len(df_v10)-len(df_v9):+d})")

print("\nKey change: Merged ONLY Structurele_Doorwerking + Depolitisering_Distantiering")
print("Kept: Benaming_Verleden (renamed Slavernij_Historisch) - critical for temporal classification")
print("Kept: Koninkrijks_Macht - distinct from general power/dependency")
print("Kept: Arbeid_Land_Eigendom (renamed Arbeid_Afhankelijkheid)")

print("\n" + "="*80)
print("RATIONALE FOR KEEPING HISTORICAL CATEGORY")
print("="*80)
print("Policy documents contain two types of segments:")
print("1. HISTORICAL: Discussing events 1600s-1863 (slavery period, abolition)")
print("2. CONTEMPORARY: Discussing present-day legacy effects")
print("\nSlavernij_Historisch identifies type 1 segments (temporal classifier)")
print("Other topics identify legacy mechanisms in type 2 segments")
print("\nThis distinction is essential for accurate policy analysis.")

print("\nDictionary optimization complete!")
