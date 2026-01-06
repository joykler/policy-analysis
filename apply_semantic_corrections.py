import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("APPLYING SEMANTIC CORRECTIONS - MANUAL CURATION")
print("="*80)

# ============================================================================
# TOPIC 1: SLAVERNIJ_HISTORISCH
# ============================================================================
print("\n\n" + "="*80)
print("TOPIC 1: SLAVERNIJ_HISTORISCH")
print("="*80)

df = pd.read_csv(r'C:\Users\Home\policy-analysis\slavernij_historisch_final.csv', encoding='utf-8-sig')
print(f"Original size: {len(df)}")

# SEMANTIC DRIFT REMOVALS (confirmed by manual review)
remove_terms = [
    'tuin',        # "garden" - NOT plantation (semantic drift from "plantage")
    'tuinen',      # "gardens" - NOT plantations
    'eigenheid',   # "uniqueness/identity" - NOT ownership of persons
    'sloot',       # "ditch/moat" - NOT chains
    'bezetten',    # "occupy/fill" - NOT related to chains/shackles
    'haakjes',     # "brackets" (punctuation) - NOT related to chains
]

print(f"\nRemoving {len(remove_terms)} semantic drift terms:")
for term in remove_terms:
    if term in df['term'].values:
        parent = df[df['term'] == term]['parent'].values[0]
        print(f"  - '{term}' (parent: '{parent}')")

df_corrected = df[~df['term'].isin(remove_terms)].copy()
print(f"\nCorrected size: {len(df_corrected)} (removed {len(df) - len(df_corrected)})")

# Save corrected version
df_corrected.to_csv(r'C:\Users\Home\policy-analysis\slavernij_historisch_CORRECTED.csv', index=False, encoding='utf-8-sig')
print("Saved: slavernij_historisch_CORRECTED.csv")

# ============================================================================
# TOPIC 2: KONINKRIJKS_MACHT
# ============================================================================
print("\n\n" + "="*80)
print("TOPIC 2: KONINKRIJKS_MACHT")
print("="*80)

df = pd.read_csv(r'C:\Users\Home\policy-analysis\koninkrijks_macht_final.csv', encoding='utf-8-sig')
print(f"Original size: {len(df)}")

# MANUAL SEMANTIC REVIEW: Kingdom-specific vs generic governance
# Terms that ARE Kingdom-specific (KEEP):
# - "toezicht" (oversight) - used in Kingdom relations context (financial oversight of islands)
# - "interventie" (intervention) - Kingdom intervention in Caribbean territories
# - "autonomie" (autonomy) - Caribbean autonomy within Kingdom
# - "verscherpt toezicht" (heightened oversight) - specific Kingdom instrument
# - "financieel toezicht" (financial oversight) - specific Kingdom instrument

# Terms that are TOO GENERIC (REMOVE):
remove_terms = [
    'inspectie',           # "inspection" - too generic administrative term
    'bewaking',            # "guarding/surveillance" - generic security term
    'controles',           # "controls/checks" - too generic
]

# Terms that need RECATEGORIZATION to CONTEXT (governance context markers):
recategorize_context = [
    'ongelijkheid',        # "inequality" - generic, but relevant as context marker
    'ongelijkheden',       # "inequalities"
    'institutionele',      # "institutional" - too generic for BELEID
]

print(f"\nRemoving {len(remove_terms)} generic governance terms:")
for term in remove_terms:
    if term in df['term'].values:
        print(f"  - '{term}'")

print(f"\nRecategorizing {len(recategorize_context)} to CONTEXT:")
for term in recategorize_context:
    if term in df['term'].values:
        print(f"  - '{term}'")

df_corrected = df[~df['term'].isin(remove_terms)].copy()
df_corrected.loc[df_corrected['term'].isin(recategorize_context), 'category'] = 'CONTEXT'
df_corrected.loc[df_corrected['term'].isin(recategorize_context), 'weight'] = 0.6

print(f"\nCorrected size: {len(df_corrected)} (removed {len(df) - len(df_corrected)})")

df_corrected.to_csv(r'C:\Users\Home\policy-analysis\koninkrijks_macht_CORRECTED.csv', index=False, encoding='utf-8-sig')
print("Saved: koninkrijks_macht_CORRECTED.csv")

# ============================================================================
# TOPIC 3: RACIALE_HIERARCHIE
# ============================================================================
print("\n\n" + "="*80)
print("TOPIC 3: RACIALE_HIERARCHIE")
print("="*80)

df = pd.read_csv(r'C:\Users\Home\policy-analysis\raciale_hierarchie_final.csv', encoding='utf-8-sig')
print(f"Original size: {len(df)}")

# MANUAL SEMANTIC REVIEW: Racial hierarchy vs generic social exclusion
# "uitsluiting" (exclusion) CAN be racial, but many expansions are generic
# Need to check each expansion

# Generic exclusion terms (NOT racial hierarchy specific):
remove_terms = [
    'aansluit',            # "connect/join" - generic
    'opsluiting',          # "confinement/imprisonment" - generic criminal justice
    'sluiting',            # "closure" (of building/facility) - generic
    'afsluiting',          # "closing/fence" - generic
    'afsluit',             # "close off" - generic
    'insluiting',          # "inclusion/enclosure" - generic
    'afsluiten',           # "to close" - generic verb
    'uitsluitsel',         # "clarity/definitive answer" - completely different meaning!
    'aansluiten',          # "to connect" - generic
]

# "achterstelling" (disadvantage) - some expansions are generic:
remove_terms += [
    'achterliggende',      # "underlying/behind" - generic spatial/causal term
]

# Terms that are actually relevant (KEEP):
# - "uitsluiting" itself (social exclusion)
# - "achterstelling" itself (disadvantage)
# - "achtergestelde", "achtergesteld" (disadvantaged) - can be racial

print(f"\nRemoving {len(remove_terms)} generic exclusion terms:")
for term in remove_terms:
    if term in df['term'].values:
        parent = df[df['term'] == term]['parent'].values[0]
        print(f"  - '{term}' (parent: '{parent}')")

df_corrected = df[~df['term'].isin(remove_terms)].copy()
print(f"\nCorrected size: {len(df_corrected)} (removed {len(df) - len(df_corrected)})")

df_corrected.to_csv(r'C:\Users\Home\policy-analysis\raciale_hierarchie_CORRECTED.csv', index=False, encoding='utf-8-sig')
print("Saved: raciale_hierarchie_CORRECTED.csv")

# ============================================================================
# TOPIC 4: ARBEID_AFHANKELIJKHEID
# ============================================================================
print("\n\n" + "="*80)
print("TOPIC 4: ARBEID_AFHANKELIJKHEID")
print("="*80)

df = pd.read_csv(r'C:\Users\Home\policy-analysis\arbeid_afhankelijkheid_final.csv', encoding='utf-8-sig')
print(f"Original size: {len(df)}")

# MANUAL SEMANTIC REVIEW: Exploitation-specific vs generic labor/state
# "staatstoezicht" appears here - but it's about state oversight POST-slavery (1863-1873)
# This IS relevant to labor dependency topic (staatstoezicht period = forced labor)
# KEEP these terms - they are contextually appropriate

# "verhoudingen" (relations/ratios) from "bezitsverhoudingen" (property relations)
# Too generic alone - REMOVE

remove_terms = [
    'verhoudingen',        # "relations/ratios" - too generic without "bezits-" prefix
]

print(f"\nRemoving {len(remove_terms)} generic labor terms:")
for term in remove_terms:
    if term in df['term'].values:
        print(f"  - '{term}'")

df_corrected = df[~df['term'].isin(remove_terms)].copy()
print(f"\nCorrected size: {len(df_corrected)} (removed {len(df) - len(df_corrected)})")

df_corrected.to_csv(r'C:\Users\Home\policy-analysis\arbeid_afhankelijkheid_CORRECTED.csv', index=False, encoding='utf-8-sig')
print("Saved: arbeid_afhankelijkheid_CORRECTED.csv")

# ============================================================================
# TOPIC 5: DOORWERKING_CONTINUITEIT
# ============================================================================
print("\n\n" + "="*80)
print("TOPIC 5: DOORWERKING_CONTINUITEIT")
print("="*80)

df = pd.read_csv(r'C:\Users\Home\policy-analysis\doorwerking_continuiteit_final.csv', encoding='utf-8-sig')
print(f"Original size: {len(df)}")

# This topic had good quality - no major semantic drift detected
# Most terms are appropriately abstract (RISICO category)

print("No semantic corrections needed - topic quality good")
df_corrected = df.copy()

df_corrected.to_csv(r'C:\Users\Home\policy-analysis\doorwerking_continuiteit_CORRECTED.csv', index=False, encoding='utf-8-sig')
print("Saved: doorwerking_continuiteit_CORRECTED.csv")

# ============================================================================
# TOPIC 6: ERKENNING_VERANTWOORDELIJKHEID
# ============================================================================
print("\n\n" + "="*80)
print("TOPIC 6: ERKENNING_VERANTWOORDELIJKHEID")
print("="*80)

df = pd.read_csv(r'C:\Users\Home\policy-analysis\erkenning_verantwoordelijkheid_final.csv', encoding='utf-8-sig')
print(f"Original size: {len(df)}")

# MANUAL SEMANTIC REVIEW: Recognition-specific vs generic admin
# "erkenning" (recognition) has problematic expansions

remove_terms = [
    'zelven',              # "selves" - fragment/generic
    'vizier',              # "sights/visor" - wrong meaning (not "envisioning")
    'stak',                # "stuck/poked" - wrong meaning
    'oratie',              # "oration/speech" - too generic
    'april',               # Month name! (probably from date mentions) - NOT recognition
    'gemeld',              # "reported/mentioned" - too generic administrative
    'antwoorden',          # "answers" - too generic
]

# "recovery", "reparatie" - these ARE relevant (reparations context)
# "genoegdoening" - redress/satisfaction - relevant
# "voldoening" - satisfaction - relevant
# KEEP these

print(f"\nRemoving {len(remove_terms)} generic/drift terms:")
for term in remove_terms:
    if term in df['term'].values:
        parent = df[df['term'] == term]['parent'].values[0]
        print(f"  - '{term}' (parent: '{parent}')")

df_corrected = df[~df['term'].isin(remove_terms)].copy()
print(f"\nCorrected size: {len(df_corrected)} (removed {len(df) - len(df_corrected)})")

df_corrected.to_csv(r'C:\Users\Home\policy-analysis\erkenning_verantwoordelijkheid_CORRECTED.csv', index=False, encoding='utf-8-sig')
print("Saved: erkenning_verantwoordelijkheid_CORRECTED.csv")

# ============================================================================
# TOPIC 7: KENNIS_HERINNERING
# ============================================================================
print("\n\n" + "="*80)
print("TOPIC 7: KENNIS_HERINNERING")
print("="*80)

df = pd.read_csv(r'C:\Users\Home\policy-analysis\kennis_herinnering_final.csv', encoding='utf-8-sig')
print(f"Original size: {len(df)}")

# MANUAL SEMANTIC REVIEW: Memory-specific vs generic commemoration
# "herdenken" (commemorate) has some problematic expansions

remove_terms = [
    'verdenking',          # "suspicion" - completely wrong meaning!
    'verdenken',           # "suspect" - completely wrong meaning!
    'herhalen',            # "repeat" - too generic
    'bedenkingen',         # "concerns/objections" - generic, not commemoration
]

# KEEP:
# - "herdenking", "herdenkingen" (commemoration/memorials) - relevant
# - "herkennen" (recognize) - relevant to recognition
# - "overdenking" (reflection) - relevant
# - "herzien" (revise) - relevant to revising history
# - "herwaardering" (revaluation) - relevant
# - "herontdekking" (rediscovery) - relevant
# - "herschikking" (rearrangement) - relevant to reordering narratives

print(f"\nRemoving {len(remove_terms)} semantic drift terms:")
for term in remove_terms:
    if term in df['term'].values:
        parent = df[df['term'] == term]['parent'].values[0]
        print(f"  - '{term}' (parent: '{parent}')")

df_corrected = df[~df['term'].isin(remove_terms)].copy()
print(f"\nCorrected size: {len(df_corrected)} (removed {len(df) - len(df_corrected)})")

df_corrected.to_csv(r'C:\Users\Home\policy-analysis\kennis_herinnering_CORRECTED.csv', index=False, encoding='utf-8-sig')
print("Saved: kennis_herinnering_CORRECTED.csv")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n\n" + "="*80)
print("SEMANTIC CORRECTION SUMMARY")
print("="*80)

corrections_summary = {
    'Slavernij_Historisch': 6,
    'Koninkrijks_Macht': 3,
    'Raciale_Hierarchie': 10,
    'Arbeid_Afhankelijkheid': 1,
    'Doorwerking_Continuiteit': 0,
    'Erkenning_Verantwoordelijkheid': 7,
    'Kennis_Herinnering': 4,
}

total_removed = sum(corrections_summary.values())
print(f"\nTotal semantic drift terms removed: {total_removed}")
print("\nPer topic:")
for topic, count in corrections_summary.items():
    print(f"  {topic}: {count} removed")

print("\n\nAll corrected dictionaries saved with _CORRECTED suffix")
print("Next: Merge into final V10 dictionary")
