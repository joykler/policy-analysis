"""
Curate expanded_candidates.csv based on semantic relevance methodology
Author: Claude Code
Date: 2025-11-26
"""

import pandas as pd
import json
import re
from pathlib import Path

# Paths
BASE_PATH = Path(r"C:\Users\Home\policy-analysis\workflow_data\slavery_Slavdict_pretraining_slavery_v16")
CANDIDATES_PATH = BASE_PATH / "Dictionary" / "expanded_candidates.csv"
CONFIG_PATH = BASE_PATH / "config" / "config_with_dictionary_20251125_183819.json"
OUTPUT_PATH = BASE_PATH / "Dictionary" / "curated_dictionary_v16.csv"

# Load data
print("="*80)
print("DICTIONARY CURATION - SLAVERY LEGACY TOPICS")
print("="*80)
print(f"\nLoading candidates from: {CANDIDATES_PATH}")
df = pd.read_csv(CANDIDATES_PATH)
print(f"   Total candidates: {len(df)}")

print(f"\nLoading seed weights from: {CONFIG_PATH}")
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)
seed_weights = config['config']['topic_seed_weights']

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def is_seedword(term, topic, seed_weights):
    """Check if term is in the seed dictionary"""
    return term in seed_weights.get(topic, {})

def get_seed_weight(term, topic, seed_weights):
    """Get original seed weight if it exists"""
    return seed_weights.get(topic, {}).get(term, None)

def is_geographic_marker(term):
    """Check if term is a geographic marker"""
    geo_markers = {
        'aruba', 'bonaire', 'curaçao', 'suriname', 'antillen',
        'caribisch nederland', 'bes-eilanden', 'sint maarten', 'saba',
        'sint eustatius', 'curaçaoënaar', 'curaçaoënaars', 'surinaams',
        'surinaamse', 'antilliaans', 'antilliaanse', 'caribisch', 'caribische'
    }
    return term.lower() in geo_markers

def is_era_marker(term):
    """Check if term is an era/year marker"""
    # Match years like 1863, 1814-1863, etc.
    year_pattern = r'^(\d{4}|\d{4}-\d{4})$'
    return bool(re.match(year_pattern, term))

def is_morphological_error(term):
    """Check if term appears to be a morphological error or broken word"""
    errors = {
        'çao', 'denten', 'histori', 'hiedenis', 'schiedenis',  # Partial words
        # Add more as needed
    }

    # Too short or too long
    if len(term) < 3 or len(term) > 40:
        return True

    # Obvious fragments
    if term in errors:
        return True

    # Starts/ends with hyphen inappropriately
    if term.startswith('-') or (term.endswith('-') and len(term) <= 4):
        return True

    return False

def is_overgeneralized(term, df_val, cosine_val, topic):
    """Check if term is too generic"""

    # Very high DF with moderate cosine suggests generic term
    if df_val > 200 and cosine_val < 0.85:
        return True

    # Known overly generic terms
    generic_terms = {
        'college', 'cursus', 'cursussen', 'academie',
        'mensen', 'land', 'jaar', 'tijd', 'plaats',
        'nederland', 'nederlandse',  # Unless specific context
    }

    if term.lower() in generic_terms and cosine_val < 0.90:
        return True

    return False

def is_semantically_relevant(term, topic, cosine_val, df_val):
    """Check semantic relevance based on topic and term characteristics"""

    topic_patterns = {
        "Educational Disadvantage & Brain Drain": {
            'keep': [
                r'onderwijs', r'school', r'leer', r'student', r'studie', r'studer',
                r'taal', r'papiament', r'moedertaal', r'curriculum',
                r'emigr', r'immigr', r'migra', r'brain',
                r'hogeschool', r'universiteit', r'academisch',
                r'achterstand', r'tekort', r'barrière', r'uitsluiting',
                r'koloni.*onderwijs', r'alfabet',
            ],
            'filter': [
                r'historicus', r'hoogleraar', r'academie$',  # Too occupation-specific
                r'historiografie', r'historikerstreit',  # Too academic
            ]
        },
        "Governance Distrust & Corruption": {
            'keep': [
                r'corrupt', r'wantrou', r'bestuur', r'gouvern', r'regering',
                r'autonom', r'constitut', r'wetgev', r'parlement',
                r'minister', r'kabinet', r'overheid', r'beleid',
                r'nepotisme', r'paternalisme', r'patronage',
                r'zelfbeschikking', r'soeverein',
            ],
            'filter': []
        },
        "Persistent Poverty & Economic Vulnerability": {
            'keep': [
                r'armoed', r'werkloos', r'economisch', r'handel',
                r'plantage', r'slavenhandel', r'voc', r'wic',
                r'afhankelijk', r'kwetsbaar', r'schuld',
                r'dwangarbeid', r'slavenarbeid', r'arbeid',
                r'extractie', r'monocultuur',
            ],
            'filter': []
        },
        "Social Fragmentation & Racism": {
            'keep': [
                r'racis', r'discrimina', r'segreg', r'uitsluit',
                r'ongelijk', r'vooroordel', r'kleurisme',
                r'etnisch', r'raciaal', r'huidskleur',
                r'emancipatie', r'abolition', r'nazaten', r'nageslacht',
                r'verdeeld', r'fragmenta',
            ],
            'filter': []
        }
    }

    patterns = topic_patterns.get(topic, {'keep': [], 'filter': []})

    # Check filter patterns first (explicit exclusions)
    for pattern in patterns['filter']:
        if re.search(pattern, term, re.IGNORECASE):
            return False

    # Check keep patterns
    for pattern in patterns['keep']:
        if re.search(pattern, term, re.IGNORECASE):
            return True

    # If no pattern match, require higher cosine for acceptance
    return cosine_val >= 0.85

def determine_weight(row, seed_weights):
    """Determine the appropriate weight for a term"""
    term = row['term']
    topic = row['topic']
    cosine = row['cosine']
    df_val = row['df']
    current_weight = row['weight']

    # 1. Seedwords keep original weight
    if is_seedword(term, topic, seed_weights):
        return get_seed_weight(term, topic, seed_weights)

    # 2. Geographic markers
    if is_geographic_marker(term):
        return 0.75

    # 3. Era markers
    if is_era_marker(term):
        return 0.70

    # 4. Historical/contextual terms (downgrade from 0.80)
    historical_patterns = [
        r'slavernij(verleden|periode|geschiedenis)',
        r'post-?koloni', r'koloni.*geschiedenis',
        r'historisch', r'geschiedenis-?'
    ]
    for pattern in historical_patterns:
        if re.search(pattern, term, re.IGNORECASE):
            return 0.70

    # 5. High-value discoveries
    if cosine >= 0.90 and df_val >= 10:
        # Check if it's a core topic term
        if is_semantically_relevant(term, topic, cosine, df_val):
            return 0.85
        else:
            return 0.80

    # 6. Good discoveries
    if cosine >= 0.80 and df_val >= 5:
        return 0.80

    # 7. Moderate discoveries
    if cosine >= 0.75 and df_val >= 3:
        return 0.80

    # Default for anything that passes filters
    return 0.80

# ============================================================================
# CURATION LOGIC
# ============================================================================

def curate_candidates(df, seed_weights):
    """Apply curation filters and return curated dataframe"""

    results = []
    stats = {
        'total': 0,
        'kept': 0,
        'filtered': 0,
        'reasons': {
            'seedword': 0,
            'high_value': 0,
            'good_semantic': 0,
            'geographic_marker': 0,
            'era_marker': 0,
            'morphological_error': 0,
            'overgeneralized': 0,
            'weak_semantic': 0,
            'low_cosine': 0,
        },
        'by_topic': {}
    }

    for topic in df['topic'].unique():
        print(f"\n{'='*80}")
        print(f"CURATING: {topic}")
        print(f"{'='*80}")

        topic_df = df[df['topic'] == topic].copy()
        stats['by_topic'][topic] = {'total': len(topic_df), 'kept': 0, 'filtered': 0}

        for idx, row in topic_df.iterrows():
            term = row['term']
            cosine = row['cosine']
            df_val = row['df']
            current_weight = row['weight']

            stats['total'] += 1
            decision = 'KEEP'
            reason = ''
            new_weight = current_weight

            # FILTER CHECKS
            # 1. Morphological errors
            if is_morphological_error(term):
                decision = 'FILTER'
                reason = 'morphological_error'
                stats['reasons']['morphological_error'] += 1

            # 2. Overgeneralized terms
            elif is_overgeneralized(term, df_val, cosine, topic):
                decision = 'FILTER'
                reason = 'overgeneralized'
                stats['reasons']['overgeneralized'] += 1

            # 3. Low cosine threshold
            elif cosine < 0.75:
                decision = 'FILTER'
                reason = 'low_cosine'
                stats['reasons']['low_cosine'] += 1

            # 4. Weak semantic relevance
            elif not is_semantically_relevant(term, topic, cosine, df_val) and cosine < 0.85:
                decision = 'FILTER'
                reason = 'weak_semantic'
                stats['reasons']['weak_semantic'] += 1

            # KEEP CHECKS
            else:
                # Determine reason for keeping
                if is_seedword(term, topic, seed_weights):
                    reason = 'seedword'
                    stats['reasons']['seedword'] += 1
                elif is_geographic_marker(term):
                    reason = 'geographic_marker'
                    stats['reasons']['geographic_marker'] += 1
                elif is_era_marker(term):
                    reason = 'era_marker'
                    stats['reasons']['era_marker'] += 1
                elif cosine >= 0.90 and df_val >= 10:
                    reason = 'high_value'
                    stats['reasons']['high_value'] += 1
                else:
                    reason = 'good_semantic'
                    stats['reasons']['good_semantic'] += 1

                # Determine final weight
                new_weight = determine_weight(row, seed_weights)

            # Record decision
            if decision == 'KEEP':
                results.append({
                    'topic': topic,
                    'term': term,
                    'cosine': cosine,
                    'df': df_val,
                    'weight': new_weight,
                    'curation_reason': reason
                })
                stats['kept'] += 1
                stats['by_topic'][topic]['kept'] += 1
            else:
                stats['filtered'] += 1
                stats['by_topic'][topic]['filtered'] += 1

    return pd.DataFrame(results), stats

# ============================================================================
# EXECUTE CURATION
# ============================================================================

print("\n" + "="*80)
print("STARTING CURATION")
print("="*80)

curated_df, stats = curate_candidates(df, seed_weights)

# ============================================================================
# VALIDATION
# ============================================================================

print("\n" + "="*80)
print("CURATION STATISTICS")
print("="*80)

print(f"\nOverall Statistics:")
print(f"   Total candidates: {stats['total']}")
print(f"   Kept: {stats['kept']} ({stats['kept']/stats['total']*100:.1f}%)")
print(f"   Filtered: {stats['filtered']} ({stats['filtered']/stats['total']*100:.1f}%)")

print(f"\nReasons for Keeping:")
print(f"   Seedwords: {stats['reasons']['seedword']}")
print(f"   High-value discoveries: {stats['reasons']['high_value']}")
print(f"   Good semantic fit: {stats['reasons']['good_semantic']}")
print(f"   Geographic markers: {stats['reasons']['geographic_marker']}")
print(f"   Era markers: {stats['reasons']['era_marker']}")

print(f"\nReasons for Filtering:")
print(f"   Morphological errors: {stats['reasons']['morphological_error']}")
print(f"   Overgeneralized: {stats['reasons']['overgeneralized']}")
print(f"   Weak semantic relevance: {stats['reasons']['weak_semantic']}")
print(f"   Low cosine (< 0.75): {stats['reasons']['low_cosine']}")

print(f"\nBy Topic:")
for topic, topic_stats in stats['by_topic'].items():
    retention = topic_stats['kept']/topic_stats['total']*100 if topic_stats['total'] > 0 else 0
    print(f"\n   {topic}:")
    print(f"      Total: {topic_stats['total']}")
    print(f"      Kept: {topic_stats['kept']} ({retention:.1f}%)")
    print(f"      Filtered: {topic_stats['filtered']}")

# Weight distribution
print(f"\nWeight Distribution in Curated Dictionary:")
print(curated_df['weight'].value_counts().sort_index(ascending=False))

# ============================================================================
# VALIDATION CHECKS
# ============================================================================

print("\n" + "="*80)
print("VALIDATION CHECKS")
print("="*80)

# Check 1: All seedwords present
print("\nChecking seedwords preservation...")
missing_seeds = []
for topic, seeds in seed_weights.items():
    topic_terms = set(curated_df[curated_df['topic'] == topic]['term'])
    for seed_term, seed_weight in seeds.items():
        # Only check if it was in the original candidates
        if seed_term in df[df['topic'] == topic]['term'].values:
            if seed_term not in topic_terms:
                missing_seeds.append((topic, seed_term))

if missing_seeds:
    print(f"   WARNING: {len(missing_seeds)} seedwords missing!")
    for topic, term in missing_seeds[:10]:  # Show first 10
        print(f"      - {topic}: {term}")
else:
    print("   All seedwords from candidates preserved")

# Check 2: Geographic markers
print("\nChecking geographic markers...")
geo_terms = curated_df[curated_df['curation_reason'] == 'geographic_marker']
print(f"   Found {len(geo_terms)} geographic marker terms")
print(f"   Sample: {geo_terms['term'].head(10).tolist()}")

# Check 3: Era markers
print("\nChecking era markers...")
era_terms = curated_df[curated_df['curation_reason'] == 'era_marker']
print(f"   Found {len(era_terms)} era marker terms")
print(f"   Sample: {era_terms['term'].head(10).tolist()}")

# Check 4: DF distribution
print("\nChecking DF distribution...")
print(f"   Min DF: {curated_df['df'].min()}")
print(f"   Max DF: {curated_df['df'].max()}")
print(f"   Median DF: {curated_df['df'].median()}")
print(f"   Terms with DF >= 10: {len(curated_df[curated_df['df'] >= 10])}")

# Check 5: Cosine distribution
print("\nChecking cosine distribution...")
print(f"   Min cosine: {curated_df['cosine'].min():.4f}")
print(f"   Max cosine: {curated_df['cosine'].max():.4f}")
print(f"   Median cosine: {curated_df['cosine'].median():.4f}")
print(f"   Terms with cosine >= 0.90: {len(curated_df[curated_df['cosine'] >= 0.90])}")

# ============================================================================
# SAVE RESULTS
# ============================================================================

print("\n" + "="*80)
print("SAVING CURATED DICTIONARY")
print("="*80)

# Save without curation_reason column
output_df = curated_df[['topic', 'term', 'cosine', 'df', 'weight']].copy()
output_df.to_csv(OUTPUT_PATH, index=False, encoding='utf-8')
print(f"\nSaved curated dictionary to: {OUTPUT_PATH}")
print(f"   Total terms: {len(output_df)}")

# Also save a version with curation reasons for analysis
analysis_path = BASE_PATH / "Dictionary" / "curated_dictionary_v16_with_reasons.csv"
curated_df.to_csv(analysis_path, index=False, encoding='utf-8')
print(f"\nSaved analysis version to: {analysis_path}")

print("\n" + "="*80)
print("CURATION COMPLETE!")
print("="*80)
