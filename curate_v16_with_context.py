"""
Dictionary Curation Script v16 - Context-Informed
Uses TOPIC_FRAMEWORK_CONTEXT.md to guide semantic relevance decisions
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path

# Load data
input_path = Path('C:/Users/Home/policy-analysis/workflow_data/slavery_Slavdict_pretraining_slavery_v16/Dictionary/expanded_candidates.csv')
output_dir = input_path.parent
df = pd.read_csv(input_path)

print(f"=== STARTING CURATION ===")
print(f"Total candidates: {len(df)}")
print(f"Topics: {df['topic'].value_counts().to_dict()}")

# ============================================================================
# DEFINE CONTEXTUAL FILTERS BASED ON TOPIC_FRAMEWORK_CONTEXT.md
# ============================================================================

# Geographic markers (from context: Dutch Caribbean + related regions)
GEOGRAPHIC_MARKERS = {
    # Dutch Caribbean islands
    'aruba', 'bonaire', 'curaçao', 'curacao', 'curaçaoënaar', 'curaçaose',
    'sint maarten', 'saba', 'sint eustatius', 'statia',
    # Derived forms
    'antillen', 'antilliaans', 'antilliaanse', 'caribisch', 'cariben',
    'suriname', 'surinaams', 'surinaamse', 'surinamer',
    # Historical names
    'nederlandse antillen', 'west-indië', 'west-indisch', 'westindisch',
    # Compound forms
    'bonaire', 'bonairiaan', 'bonairiaanse',
    'arubaan', 'arubaanse',
}

# Era markers (from context: abolition and colonial period)
ERA_MARKERS = {
    # Abolition period
    '1863', '1862', '1864', '1865', '1814-1863', '1814', '1848',
    # Colonial period markers
    '1763', '1791', '1795', '1868', '1873', '1890',
    # 20th century decolonization
    '1954', '1975', '2010',
}

# Historical context terms (cross-topic anchors)
HISTORICAL_ANCHORS = {
    'slavernij', 'slaven', 'slaaf', 'slavenhandel', 'slavernijverleden',
    'kolonie', 'koloniën', 'koloniale', 'koloniaal', 'kolonialisme',
    'postkoloniale', 'postkoloniaal', 'dekolonisatie', 'dekoloniseren',
    'emancipatie', 'abolitionisme', 'afschaffing',
    'plantage', 'plantages', 'plantageland', 'plantagesysteem',
    'wic', 'voc', 'west-indische', 'oost-indische',
}

# ============================================================================
# TOPIC-SPECIFIC SEMANTIC FILTERS
# Based on TOPIC_FRAMEWORK_CONTEXT.md explanations
# ============================================================================

EDUCATIONAL_KEEP = {
    # Institutions
    'onderwijs', 'school', 'scholen', 'universiteit', 'hogeschool', 'vo', 'hbo',
    'basisonderwijs', 'middelbaar', 'voortgezet',
    # Language/linguistic (CRITICAL for educational disadvantage)
    'taal', 'taalpolitiek', 'taalonderwijs', 'taalbarrière', 'taalbarri',
    'papiaments', 'papiamentu', 'papiamento', 'moedertaal',
    'nederlands', 'nederlandstalig',
    # Migration (brain drain)
    'emigratie', 'emigreren', 'immigratie', 'migratie', 'brain drain', 'braindrain',
    'wegtrekken', 'vertrek', 'terugkeer',
    # Students/learning
    'student', 'studenten', 'studie', 'leerling', 'leerlingen',
    'scholier', 'scholieren', 'leerplicht',
    # Educational barriers (CORE PROBLEM)
    'achterstand', 'onderwijsachterstand', 'onderwijs-achterstand',
    'schooluitval', 'uitval', 'dropout', 'vroegtijdig schoolverlaten',
    'analfabetisme', 'laaggeletterdheid',
    'uitsluiting', 'onderwijsuitsluiting', 'toegang',
    'tekort', 'lerarentekort', 'capaciteitstekort',
    # Quality/outcomes
    'onderwijskwaliteit', 'onderwijsniveau', 'onderwijsniveaus',
    'niveau', 'kwaliteit', 'prestatie', 'resultaten',
    'curriculum', 'leerplan', 'lesmateriaal',
    # Colonial education legacy
    'katholiek', 'religieus', 'missie', 'missionering',
    'koloniale onderwijs', 'onderwijssysteem',
}

EDUCATIONAL_FILTER = {
    # Generic academic (unless high cosine)
    'academia', 'academisch', 'hoogleraar', 'professor', 'onderzoeker',
    # Too specific occupational
    'lerarencorps', 'schoolbestuur', 'directeur',
    # Broken morphology
    'histori', 'schoolverlat', 'onderwij',
}

GOVERNANCE_KEEP = {
    # Government/administration
    'regering', 'overheid', 'bestuur', 'gouvernement', 'gouverneur',
    'ministerie', 'minister', 'staatssecretaris',
    'bestuurlijke', 'bestuurslaag', 'gemeentebestuur',
    'koninkrijksrelaties', 'koninkrijk',
    # Corruption/distrust (CORE PROBLEM)
    'corruptie', 'corrupt', 'wantrouwen', 'vertrouwen', 'distrust',
    'patronage', 'clientelisme', 'vriendjespolitiek', 'nepotisme',
    'machtsmisbruik', 'wanbeheer', 'malversatie',
    # Autonomy/sovereignty (colonial legacy)
    'autonomie', 'onafhankelijk', 'onafhankelijkheid', 'soevereiniteit',
    'status aparte', 'zelfbestuur', 'zelfregeering',
    'constitutie', 'grondwet', 'statuut',
    # Colonial governance structures
    'koloniaal bestuur', 'koloniale administratie', 'gouvernementeel',
    'gezaghebber', 'gevolmachtigde', 'rijksvertegenwoordiger',
    # Legal/justice system
    'rechtsstaat', 'rechtszekerheid', 'rechtshandhaving',
    'toegang tot recht', 'rechtshulp', 'juridisch',
    'wetgeving', 'wetgever', 'parlementair',
    # Participation/democracy
    'participatie', 'democratie', 'verkiezingen', 'stemrecht',
    'inspraak', 'dialoog', 'consultatie',
}

GOVERNANCE_FILTER = {
    # Generic political terms without colonial context
    'politiek', 'beleid', 'beleidsnota',  # Too generic unless compound
    # Modern management jargon
    'governance', 'sturen', 'sturing',
}

ECONOMIC_KEEP = {
    # Poverty/vulnerability (CORE PROBLEM)
    'armoede', 'armoed', 'arm', 'kansarm', 'kansarme',
    'economische kwetsbaarheid', 'kwetsbaar', 'kwetsbaarheid',
    'ongelijkheid', 'ongelijk', 'dispariteit', 'kloof',
    # Employment/labor
    'werkloos', 'werkloosheid', 'werkloos', 'werkeloosheid',
    'arbeid', 'werk', 'arbeidsmarkt', 'werkgelegenheid',
    'precaire arbeid', 'informele economie', 'informeel',
    'banenmarkt', 'baan', 'banen',
    # Wages/income
    'inkomen', 'salaris', 'loon', 'lonen', 'minimumloon',
    'sociaal minimum', 'levensstandaard', 'levensomstandigheden',
    'kosten van levensonderhoud', 'levensonderhoud',
    # Colonial extractive economy
    'plantage', 'plantages', 'plantage-economie', 'plantageland',
    'slavenarbeid', 'dwangarbeid', 'gedwongen arbeid',
    'handel', 'handelscompagnie', 'voc', 'wic',
    'extractie', 'uitbuiting', 'exploitatie',
    'suiker', 'suikerplantage', 'katoen', 'tabak', 'zout',
    # Wealth disparity (Theodoridis 2024 finding)
    'vermogen', 'bezit', 'eigendom', 'grondbezit', 'landbezit',
    'wealth', 'welvaart', 'welzijn',
    'herverdeling', 'redistributie', 'compensatie',
    # Economic dependency
    'afhankelijkheid', 'economische afhankelijkheid', 'afhankelijk',
    'ontwikkelingshulp', 'subsidie', 'financiering',
    'toerisme', 'toeristen', 'toeristisch',
    'olie-industrie', 'olie', 'raffinaderij',
    # Access to resources
    'toegang', 'kapitaal', 'krediet', 'financiering',
    'investeringen', 'investering', 'ondernemen',
}

ECONOMIC_FILTER = {
    # Modern economics jargon not specific to colonial legacy
    'economie', 'economisch',  # Too generic unless compound
    'markt', 'markten',  # Too generic
    'groei', 'economische groei',  # Generic development discourse
}

SOCIAL_KEEP = {
    # Racism/discrimination (CORE PROBLEM)
    'racisme', 'racis', 'racist', 'racistisch',
    'discriminatie', 'discrimineren', 'discriminerend',
    'vooroordeel', 'vooroordelen', 'stigma', 'stereotyp',
    'colorisme', 'kleurendiscriminatie',
    # Racial hierarchy (slavery legacy)
    'huidskleur', 'kleur', 'wit', 'zwart', 'mulat', 'mestizo',
    'raciale hiërarchie', 'rassentheorie', 'rassenleer',
    'blank', 'gekleurd', 'kleurling',
    # Segregation/exclusion
    'uitsluiting', 'uitgesloten', 'segregatie', 'gesegregeerd',
    'apartheid', 'scheiding', 'scheidingslijn',
    'marginalisatie', 'gemarginaliseerd',
    # Identity/community
    'identiteit', 'culturele identiteit', 'etnische identiteit',
    'gemeenschap', 'bevolking', 'bevolkingsgroep',
    'minderheid', 'minderheden',
    # Social fragmentation
    'fragmentatie', 'verdeeldheid', 'verdeeld',
    'sociale cohesie', 'cohesie', 'samenhang',
    'integratie', 'inclusie', 'diversiteit',
    # Historical trauma/recognition
    'trauma', 'historisch trauma', 'transgenerationeel',
    'erkenning', 'excuses', 'apologetiek',
    'herstel', 'reparatie', 'reparaties', 'compensatie',
    'genoegdoening', 'satisfactie',
    # Cultural dimensions
    'cultuur', 'cultureel', 'erfgoed', 'cultureel erfgoed',
    'traditie', 'geschiedenis', 'herinnering', 'geheugen',
}

SOCIAL_FILTER = {
    # Generic sociology terms
    'sociaal', 'maatschappelijk',  # Too generic unless compound
    'samenleving', 'gemeenschap',  # Keep only if specific context
}

# ============================================================================
# QUALITY FILTERS
# ============================================================================

def is_morphological_error(term):
    """Detect spelling errors and broken morphology"""
    # Broken suffix patterns
    if re.match(r'.*[^a-z]heid$', term):  # "hiedenis" instead of "geschiedenis"
        return True
    # Incomplete compound
    if term.endswith('-') and len(term) < 4:
        return False  # Keep intentional prefix like "onderwijs-"
    # Single character or very short fragments
    if len(term) <= 2 and term not in ['vo', 'hbo', 'wic', 'voc']:
        return True
    # Contains numbers but not era marker
    if any(c.isdigit() for c in term) and term not in ERA_MARKERS:
        # Allow year patterns
        if not re.match(r'\d{4}', term):
            return True
    # Encoding issues
    if '�' in term or 'Ã' in term:
        return True
    return False

def is_overgeneralized(term, df_count, cosine_score):
    """Detect terms that are too generic given their frequency"""
    # High DF but low cosine = probably generic
    if df_count > 200 and cosine_score < 0.85:
        return True
    # Very high DF requires very high cosine
    if df_count > 400 and cosine_score < 0.95:
        return True
    return False

def is_semantically_relevant(term, topic, cosine_score, df_count):
    """Check if term is semantically relevant to topic based on context framework"""
    term_lower = term.lower().strip()

    # Always keep geographic and era markers
    if term_lower in GEOGRAPHIC_MARKERS or term_lower in ERA_MARKERS:
        return True

    # Always keep historical anchors
    if term_lower in HISTORICAL_ANCHORS:
        return True

    # Check for partial matches (compounds)
    def partial_match(term, keyset):
        term_clean = term_lower.replace('-', '').replace(' ', '')
        for key in keyset:
            key_clean = key.replace('-', '').replace(' ', '')
            if key_clean in term_clean or term_clean in key_clean:
                return True
        return False

    # Topic-specific filters
    if 'Educational' in topic:
        if partial_match(term, EDUCATIONAL_KEEP):
            return True
        if partial_match(term, EDUCATIONAL_FILTER):
            # Filtered unless high cosine
            return cosine_score >= 0.90

    elif 'Governance' in topic:
        if partial_match(term, GOVERNANCE_KEEP):
            return True
        if partial_match(term, GOVERNANCE_FILTER):
            return cosine_score >= 0.90

    elif 'Economic' in topic or 'Poverty' in topic:
        if partial_match(term, ECONOMIC_KEEP):
            return True
        if partial_match(term, ECONOMIC_FILTER):
            return cosine_score >= 0.90

    elif 'Social' in topic or 'Racism' in topic:
        if partial_match(term, SOCIAL_KEEP):
            return True
        if partial_match(term, SOCIAL_FILTER):
            return cosine_score >= 0.90

    # Default: rely on statistical thresholds
    return False

# ============================================================================
# CURATION LOGIC
# ============================================================================

def curate_term(row):
    """Apply curation decision algorithm"""
    term = row['term']
    topic = row['topic']
    cosine = row['cosine']
    df_count = row['df']
    weight = row['weight']

    decision = {
        'term': term,
        'topic': topic,
        'cosine': cosine,
        'df': df_count,
        'weight': weight,
        'keep': False,
        'reason': ''
    }

    # Rule 1: Keep all seedwords (cosine=1.0 and weight>=0.9)
    if cosine == 1.0 and weight >= 0.9:
        decision['keep'] = True
        decision['reason'] = 'seedword'
        return decision

    # Rule 2: Keep geographic and era markers
    term_lower = term.lower().strip()
    if term_lower in GEOGRAPHIC_MARKERS:
        decision['keep'] = True
        decision['reason'] = 'geographic_marker'
        return decision

    if term_lower in ERA_MARKERS:
        decision['keep'] = True
        decision['reason'] = 'era_marker'
        return decision

    # Rule 3: Filter morphological errors
    if is_morphological_error(term):
        decision['keep'] = False
        decision['reason'] = 'morphological_error'
        return decision

    # Rule 4: Semantic relevance + statistical thresholds
    if is_semantically_relevant(term, topic, cosine, df_count):
        # Passed semantic filter, now check statistical thresholds
        if cosine >= 0.80 and df_count >= 5:
            decision['keep'] = True
            decision['reason'] = 'semantic_relevant_high_df'
            return decision
        elif cosine >= 0.90 and df_count >= 2:
            decision['keep'] = True
            decision['reason'] = 'semantic_relevant_very_high_cosine'
            return decision
        else:
            # Semantic but weak statistics
            decision['keep'] = False
            decision['reason'] = 'semantic_but_weak_stats'
            return decision

    # Rule 5: Over-generalized filter
    if is_overgeneralized(term, df_count, cosine):
        decision['keep'] = False
        decision['reason'] = 'overgeneralized'
        return decision

    # Rule 6: Strong statistical signal (even if not explicitly in semantic sets)
    if cosine >= 0.90 and df_count >= 5:
        decision['keep'] = True
        decision['reason'] = 'strong_statistical_signal'
        return decision

    # Rule 7: Moderate signal with sufficient frequency
    if cosine >= 0.85 and df_count >= 10:
        decision['keep'] = True
        decision['reason'] = 'moderate_signal_sufficient_freq'
        return decision

    # Default: filter weak signals
    decision['keep'] = False
    decision['reason'] = 'weak_signal'
    return decision

# ============================================================================
# EXECUTE CURATION
# ============================================================================

print("\n=== APPLYING CURATION RULES ===")
decisions = df.apply(curate_term, axis=1, result_type='expand')

# Combine with original data (drop duplicate columns from decisions)
decisions_clean = decisions[['keep', 'reason']].copy()
df_with_decisions = pd.concat([df, decisions_clean], axis=1)

# Filter to kept terms
df_curated = df_with_decisions[df_with_decisions['keep'] == True].copy()

print(f"\n=== CURATION RESULTS ===")
print(f"Total candidates: {len(df)}")
print(f"Kept: {len(df_curated)} ({len(df_curated)/len(df)*100:.1f}%)")
print(f"Filtered: {len(df) - len(df_curated)} ({(len(df)-len(df_curated))/len(df)*100:.1f}%)")

print(f"\n=== KEPT BY TOPIC ===")
print(df_curated['topic'].value_counts())

print(f"\n=== KEPT BY REASON ===")
print(df_curated['reason'].value_counts())

print(f"\n=== FILTERED BY REASON ===")
df_filtered = df_with_decisions[df_with_decisions['keep'] == False]
print(df_filtered['reason'].value_counts())

# ============================================================================
# VALIDATION CHECKS
# ============================================================================

print(f"\n=== VALIDATION CHECKS ===")

# Check 1: Seedwords preserved
seedwords = df[(df['cosine'] == 1.0) & (df['weight'] >= 0.9)]
kept_seedwords = df_curated[(df_curated['cosine'] == 1.0) & (df_curated['weight'] >= 0.9)]
print(f"[OK] Seedwords: {len(kept_seedwords)}/{len(seedwords)} preserved ({len(kept_seedwords)/len(seedwords)*100:.1f}%)")

# Check 2: Geographic markers
geo_count = sum(1 for term in df_curated['term'] if term.lower() in GEOGRAPHIC_MARKERS)
print(f"[OK] Geographic markers in curated dict: {geo_count}")

# Check 3: Era markers
era_count = sum(1 for term in df_curated['term'] if term.lower() in ERA_MARKERS)
print(f"[OK] Era markers in curated dict: {era_count}")

# Check 4: Distribution stats
print(f"\n[OK] Cosine distribution (curated):")
print(f"   Mean: {df_curated['cosine'].mean():.3f}")
print(f"   Min: {df_curated['cosine'].min():.3f}")
print(f"   25%: {df_curated['cosine'].quantile(0.25):.3f}")
print(f"   Median: {df_curated['cosine'].median():.3f}")
print(f"   75%: {df_curated['cosine'].quantile(0.75):.3f}")

print(f"\n[OK] DF distribution (curated):")
print(f"   Mean: {df_curated['df'].mean():.1f}")
print(f"   Min: {df_curated['df'].min():.0f}")
print(f"   Median: {df_curated['df'].median():.0f}")
print(f"   Max: {df_curated['df'].max():.0f}")

# ============================================================================
# SAVE OUTPUTS
# ============================================================================

# Save curated dictionary
output_curated = output_dir / 'curated_dictionary_v16_context.csv'
df_curated[['topic', 'term', 'cosine', 'df', 'weight']].to_csv(output_curated, index=False)
print(f"\n[OK] Saved curated dictionary: {output_curated}")

# Save full decisions for review
output_decisions = output_dir / 'curation_decisions_v16_context.csv'
df_with_decisions.to_csv(output_decisions, index=False)
print(f"[OK] Saved full decisions: {output_decisions}")

# Save filtered terms for review
output_filtered = output_dir / 'filtered_terms_v16_context.csv'
df_filtered.to_csv(output_filtered, index=False)
print(f"[OK] Saved filtered terms: {output_filtered}")

# Generate summary by topic
print(f"\n=== TOPIC SUMMARIES ===")
for topic in df['topic'].unique():
    topic_original = len(df[df['topic'] == topic])
    topic_kept = len(df_curated[df_curated['topic'] == topic])
    print(f"\n{topic}:")
    print(f"  Original: {topic_original}")
    print(f"  Kept: {topic_kept} ({topic_kept/topic_original*100:.1f}%)")

    # Show sample kept terms
    sample = df_curated[df_curated['topic'] == topic].head(10)
    print(f"  Sample terms: {', '.join(sample['term'].tolist())}")

print(f"\n=== CURATION COMPLETE ===")
