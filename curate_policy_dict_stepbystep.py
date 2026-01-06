"""
STEP-BY-STEP DICTIONARY CURATION
Following A__DICTIONARY_CURATION_GUIDE.md methodology
Policy Corpus - Stage 2 (MORE RESTRICTIVE)

Process:
1. Phase 1: Automatic removal (fragments, df=0 seeds, encoding errors)
2. Phase 2: Semantic drift detection (wrong meanings, polysemy)
3. Phase 3: Overgeneralization control (ultra-high df)
4. Phase 4: Category corrections (historical vs contemporary)
5. Phase 5: Weight calibration (df dampening)
"""

import pandas as pd
import numpy as np
from collections import defaultdict

# Load dictionary
input_path = r'C:\Users\Home\policy-analysis\workflow_data\Policy_Slavdict_ft-slavery_slavery_v2\Dictionary\expanded_candidates.csv'
df = pd.read_csv(input_path)

print("="*80)
print("STEP-BY-STEP DICTIONARY CURATION - POLICY CORPUS (STAGE 2)")
print("="*80)
print(f"\nOriginal dictionary: {len(df)} terms")
print(f"Topics: {df['topic'].unique()}")
print()

# Track all curation decisions
removal_log = []
reweight_log = []

def log_removal(term, topic, phase, reason, details=""):
    removal_log.append({
        'term': term,
        'topic': topic,
        'phase': phase,
        'reason': reason,
        'details': details
    })

def log_reweight(term, topic, phase, old_weight, new_weight, reason):
    reweight_log.append({
        'term': term,
        'topic': topic,
        'phase': phase,
        'old_weight': old_weight,
        'new_weight': new_weight,
        'reason': reason
    })

# ============================================================================
# PHASE 1: AUTOMATIC REMOVAL
# ============================================================================
print("PHASE 1: AUTOMATIC REMOVAL")
print("-" * 80)

# 1.1: Fragments (incomplete words)
fragments = {
    'schiedenis', 'slavernijverle-', 'denten', 'bon', 'partement',
    'slaafgemaak-', 'schaffing', 'geschiedenis-', 'afschaffings-',
    'toeris-', 'prijs-', 'wic-', 'onderwijs-', 'emigratie-',
    'kinder-', 'antidiscriminatie-', 'antiracisme-', 'conservatief-'
}

fragment_mask = df['term'].isin(fragments)
fragment_count = fragment_mask.sum()
for idx, row in df[fragment_mask].iterrows():
    log_removal(row['term'], row['topic'], 'Phase 1.1', 'Fragment', 'Incomplete word')
df = df[~fragment_mask]
print(f"1.1 Fragments removed: {fragment_count}")

# 1.2: df=0 seed terms (idealized compounds not in corpus)
df0_seeds = (df['df'] == 0) & (df['is_seed'] == 1)
df0_count = df0_seeds.sum()
for idx, row in df[df0_seeds].iterrows():
    log_removal(row['term'], row['topic'], 'Phase 1.2', 'df=0 seed', 'Idealized compound not in corpus')
df = df[~df0_seeds]
print(f"1.2 df=0 seeds removed: {df0_count}")

# 1.3: Encoding errors
encoding_errors = {'financi�le', 'raciale hi�rarchie', 'kleur-hi�rarchie', 'voc-koloni�n'}
encoding_mask = df['term'].isin(encoding_errors)
encoding_count = encoding_mask.sum()
for idx, row in df[encoding_mask].iterrows():
    log_removal(row['term'], row['topic'], 'Phase 1.3', 'Encoding error', 'Contains � character')
df = df[~encoding_mask]
print(f"1.3 Encoding errors removed: {encoding_count}")

# 1.4: Single df terms (appear only once, unreliable)
single_df = df['df'] == 1
single_df_count = single_df.sum()
for idx, row in df[single_df].iterrows():
    log_removal(row['term'], row['topic'], 'Phase 1.4', 'Single df', 'Appears only once in corpus')
df = df[~single_df]
print(f"1.4 Single df terms removed: {single_df_count}")

print(f"\nPhase 1 total removed: {fragment_count + df0_count + encoding_count + single_df_count}")
print(f"Remaining: {len(df)} terms\n")

# ============================================================================
# PHASE 2: SEMANTIC DRIFT DETECTION
# ============================================================================
print("PHASE 2: SEMANTIC DRIFT DETECTION")
print("-" * 80)

# 2.1: Low cosine + high weight (semantic drift from parent)
low_cosine_high_weight = (df['cosine'] < 0.75) & (df['weight'] >= 0.85)
print(f"2.1 Low cosine (<0.75) + high weight (>=0.85): {low_cosine_high_weight.sum()} terms")
if low_cosine_high_weight.sum() > 0:
    print("\nTerms requiring manual review:")
    for idx, row in df[low_cosine_high_weight].iterrows():
        print(f"  {row['term']:30s} | cosine={row['cosine']:.3f} | weight={row['weight']:.2f} | parent={row['parent']}")

# 2.2: Geographic homonym confusion
geographic_errors = {'cuba', 'zuid-india'}  # Cuba (not Curaçao), South India (not West Indies)
geo_mask = df['term'].isin(geographic_errors)
geo_count = geo_mask.sum()
for idx, row in df[geo_mask].iterrows():
    log_removal(row['term'], row['topic'], 'Phase 2.2', 'Geographic error', 'Wrong location (homonym confusion)')
df = df[~geo_mask]
print(f"2.2 Geographic errors removed: {geo_count}")

# 2.3: Polysemy confusion (wrong meaning of parent)
# Analyze by parent seed to detect semantic drift patterns

print("\n2.3 Semantic drift by parent seed:")
print("-" * 80)

# Topic 1: Educational Disadvantage & Brain Drain
topic1_drift = {
    # From "college" (ambiguous: school vs board)
    'college': 'Ambiguous (school vs executive board)',
    # From over-general seeds
    'niveau': 'Over-general (any level, not education level)',
    'nederlandse': 'Ultra-high df (generic Dutch, not language policy)',
    'nederland': 'Geographic over-generalization',
    'expeditie': 'Wrong semantic space (exploration, not education)',
    # From semantic expansion errors
    'lesmethoden': 'Keep - legitimate teaching methods',
    'lesmethodes': 'Keep - legitimate teaching methods variant',
}

topic1_remove = {'college', 'niveau', 'nederlandse', 'nederland', 'expeditie'}
t1_mask = (df['topic'] == 'Educational Disadvantage & Brain Drain') & df['term'].isin(topic1_remove)
for idx, row in df[t1_mask].iterrows():
    log_removal(row['term'], row['topic'], 'Phase 2.3', 'Semantic drift', topic1_drift.get(row['term'], 'Wrong meaning'))
df = df[~t1_mask]
print(f"  Topic 1 semantic drift removed: {t1_mask.sum()}")

# Topic 2: Governance Distrust & Corruption
topic2_drift = {
    # From "omkoping" (bribery) → "om-" prefix confusion
    'omverwerping': 'Prefix confusion (om-): overthrow, not bribery',
    'koperen': 'Phonetic similarity: copper, not corruption',
    # From "afschaffing" → "af-" prefix confusion
    'afstaan': 'Prefix confusion (af-): cede, not abolish',
    'afname': 'Prefix confusion (af-): decrease, not abolish',
    'afbetaling': 'Prefix confusion (af-): payment, not abolish',
    # Antonyms
    'onafhankelijkheid': 'Antonym of afhankelijkheid (independence vs dependence)',
    'vertrouwen': 'Antonym of wantrouwen (trust vs distrust)',
    # Wrong semantic space
    'nazisme': 'Phonetic to nepotisme, wrong era/context',
    'daadkrachtig': 'Generic (decisive), not governance-specific',
    'marronage': 'Historical slavery term, not contemporary governance',
}

topic2_remove = {
    'omverwerping', 'koperen', 'afstaan', 'afname', 'afbetaling',
    'onafhankelijkheid', 'vertrouwen', 'nazisme', 'daadkrachtig', 'marronage'
}
t2_mask = (df['topic'] == 'Governance Distrust & Corruption') & df['term'].isin(topic2_remove)
for idx, row in df[t2_mask].iterrows():
    log_removal(row['term'], row['topic'], 'Phase 2.3', 'Semantic drift', topic2_drift.get(row['term'], 'Wrong meaning'))
df = df[~t2_mask]
print(f"  Topic 2 semantic drift removed: {t2_mask.sum()}")

# Topic 3: Persistent Poverty & Economic Vulnerability
topic3_drift = {
    # Polysemy: "schuld" = debt vs guilt
    'onschuld': 'From schuld polysemy: innocence, not debt',
    'schuldgevoel': 'From schuld polysemy: guilt feeling, not financial debt',
    # Generic terms
    'plant': 'Over-general: plant (plantage semantic drift)',
    'arbeid': 'Ultra-generic: any labor, not slavery-related economic vulnerability',
    'kinderen': 'Ultra-generic: any children, not economic vulnerability',
    # Prefix confusion from "afschaffing"
    'verschaffen': 'Wrong prefix: provide, not abolish',
    'afstaan': 'Prefix confusion: cede, not abolish',
}

topic3_remove = {
    'onschuld', 'schuldgevoel', 'plant', 'arbeid', 'kinderen',
    'verschaffen', 'afstaan'
}
t3_mask = (df['topic'] == 'Persistent Poverty & Economic Vulnerability') & df['term'].isin(topic3_remove)
for idx, row in df[t3_mask].iterrows():
    log_removal(row['term'], row['topic'], 'Phase 2.3', 'Semantic drift', topic3_drift.get(row['term'], 'Wrong meaning'))
df = df[~t3_mask]
print(f"  Topic 3 semantic drift removed: {t3_mask.sum()}")

# Topic 4: Social Fragmentation & Racism
topic4_drift = {
    # From "uitsluiting" (exclusion) → "-sluiting" suffix confusion
    'ontsluiting': 'Suffix confusion: opening/connection, OPPOSITE of exclusion',
    'opsluiting': 'Suffix confusion: imprisonment, different meaning',
    'uitsluitsel': 'Suffix confusion: clarity/answer, not exclusion',
    'afsluiting': 'Suffix confusion: closing/conclusion, not exclusion',
    # Over-generalization
    'verscheidenheid': 'Generic diversity, not racism-related fragmentation',
    'variatie': 'Generic variation, not fragmentation',
    'diversiteit': 'Generic diversity (positive), wrong frame for racism topic',
}

topic4_remove = {
    'ontsluiting', 'opsluiting', 'uitsluitsel', 'afsluiting',
    'verscheidenheid', 'variatie', 'diversiteit'
}
t4_mask = (df['topic'] == 'Social Fragmentation & Racism') & df['term'].isin(topic4_remove)
for idx, row in df[t4_mask].iterrows():
    log_removal(row['term'], row['topic'], 'Phase 2.3', 'Semantic drift', topic4_drift.get(row['term'], 'Wrong meaning'))
df = df[~t4_mask]
print(f"  Topic 4 semantic drift removed: {t4_mask.sum()}")

phase2_total = geo_count + t1_mask.sum() + t2_mask.sum() + t3_mask.sum() + t4_mask.sum()
print(f"\nPhase 2 total removed: {phase2_total}")
print(f"Remaining: {len(df)} terms\n")

# ============================================================================
# PHASE 3: OVERGENERALIZATION CONTROL
# ============================================================================
print("PHASE 3: OVERGENERALIZATION CONTROL")
print("-" * 80)

# 3.1: Ultra-high document frequency (appears in >50% of documents)
# Assuming corpus ~1000 documents, df>500 is ultra-high
ultra_high_df_threshold = 500
ultra_high = df['df'] > ultra_high_df_threshold
print(f"3.1 Terms with df > {ultra_high_df_threshold}:")
if ultra_high.sum() > 0:
    for idx, row in df[ultra_high].iterrows():
        print(f"  {row['term']:30s} | df={row['df']:4.0f} | weight={row['weight']:.2f}")

# Remove ultra-generic terms
ultra_generic = {'nederlandse', 'nederland'}  # Already in semantic drift, double-check
ultra_mask = df['term'].isin(ultra_generic)
ultra_count = ultra_mask.sum()
for idx, row in df[ultra_mask].iterrows():
    log_removal(row['term'], row['topic'], 'Phase 3.1', 'Ultra-high df', f'df={row["df"]}, too generic')
df = df[~ultra_mask]
print(f"3.1 Ultra-generic terms removed: {ultra_count}")

# 3.2: Generic fragments (already handled in Phase 1)
print(f"\nPhase 3 total removed: {ultra_count}")
print(f"Remaining: {len(df)} terms\n")

# ============================================================================
# PHASE 4: CATEGORY CORRECTIONS
# ============================================================================
print("PHASE 4: CATEGORY CORRECTIONS")
print("-" * 80)

# 4.1: Historical terms should be era_context (0.55 weight)
# Already mostly correct, verify a few edge cases

# 4.2: Stage 2 restriction: Remove academic/scholarly jargon
academic_jargon = {
    'historici', 'historicus', 'historiografie', 'geschiedschrijving',
    'kunsthistorici', 'rijksmuseum', 'museum', 'essay',
    'historiografie', 'geschiedenisboek'
}
academic_mask = df['term'].isin(academic_jargon)
academic_count = academic_mask.sum()
for idx, row in df[academic_mask].iterrows():
    log_removal(row['term'], row['topic'], 'Phase 4.2', 'Academic jargon', 'Stage 2 restriction: not policy language')
df = df[~academic_mask]
print(f"4.2 Academic jargon removed (Stage 2 restriction): {academic_count}")

# 4.3: Remove English terms (Stage 2: Dutch policy only)
english_terms = {'brain drain', 'abolition', 'racism', 'plantation', 'assessment'}
english_mask = df['term'].isin(english_terms)
english_count = english_mask.sum()
for idx, row in df[english_mask].iterrows():
    log_removal(row['term'], row['topic'], 'Phase 4.3', 'English term', 'Stage 2 restriction: Dutch policy language only')
df = df[~english_mask]
print(f"4.3 English terms removed (Stage 2 restriction): {english_count}")

print(f"\nPhase 4 total removed: {academic_count + english_count}")
print(f"Remaining: {len(df)} terms\n")

# ============================================================================
# PHASE 5: WEIGHT CALIBRATION
# ============================================================================
print("PHASE 5: WEIGHT CALIBRATION")
print("-" * 80)

# 5.1: Document frequency dampening
# High df terms need lower weights to avoid dominating signal

print("5.1 High-frequency terms requiring weight adjustment:")
high_df_terms = df[df['df'] > 100].sort_values('df', ascending=False)
print(f"\nTerms with df > 100: {len(high_df_terms)}")

# Apply df-based weight dampening
for idx, row in high_df_terms.iterrows():
    old_weight = row['weight']

    # Dampening formula based on df
    if row['df'] > 1000:  # Ultra-high (>100% corpus, multi-mentions per doc)
        new_weight = max(0.40, old_weight - 0.30)
    elif row['df'] > 500:
        new_weight = max(0.40, old_weight - 0.25)
    elif row['df'] > 300:
        new_weight = max(0.45, old_weight - 0.20)
    elif row['df'] > 200:
        new_weight = max(0.50, old_weight - 0.15)
    elif row['df'] > 100:
        new_weight = max(0.55, old_weight - 0.10)
    else:
        new_weight = old_weight

    if new_weight != old_weight:
        df.at[idx, 'weight'] = new_weight
        log_reweight(row['term'], row['topic'], 'Phase 5.1', old_weight, new_weight,
                    f'df dampening (df={row["df"]})')
        print(f"  {row['term']:30s} | df={row['df']:4.0f} | {old_weight:.2f} -> {new_weight:.2f}")

# 5.2: Standardize cross-topic term weights (ensure consistency)
print("\n5.2 Cross-topic weight standardization:")

# Identify cross-topic terms
term_topics = df.groupby('term')['topic'].apply(lambda x: list(x)).to_dict()
cross_topic_terms = {term: topics for term, topics in term_topics.items() if len(topics) > 1}

print(f"Cross-topic terms: {len(cross_topic_terms)}")

# Check for weight inconsistencies
for term, topics in cross_topic_terms.items():
    term_df = df[df['term'] == term]
    weights = term_df['weight'].unique()

    if len(weights) > 1:
        # Standardize to median weight
        median_weight = term_df['weight'].median()
        print(f"  {term:30s} | topics={len(topics)} | weights={sorted(weights)} -> {median_weight:.2f}")

        for idx, row in term_df.iterrows():
            if row['weight'] != median_weight:
                old_weight = row['weight']
                df.at[idx, 'weight'] = median_weight
                log_reweight(row['term'], row['topic'], 'Phase 5.2', old_weight, median_weight,
                           'Cross-topic standardization')

print(f"\nPhase 5 weight adjustments: {len([r for r in reweight_log if r['phase'] == 'Phase 5.1' or r['phase'] == 'Phase 5.2'])}")
print(f"Final dictionary: {len(df)} terms\n")

# ============================================================================
# SAVE CURATED DICTIONARY
# ============================================================================
output_dir = r'C:\Users\Home\policy-analysis\workflow_data\Policy_Slavdict_ft-slavery_slavery_v2\Dictionary'
curated_path = f'{output_dir}\\curated_dictionary_stepbystep.csv'
df.to_csv(curated_path, index=False)

print("="*80)
print("CURATION COMPLETE")
print("="*80)
print(f"\nFinal statistics:")
print(f"  Original: 1200 terms")
print(f"  Removed: {1200 - len(df)} terms ({100*(1200-len(df))/1200:.1f}%)")
print(f"  Final: {len(df)} terms")
print(f"\nBy topic:")
for topic in df['topic'].unique():
    count = len(df[df['topic'] == topic])
    print(f"  {topic}: {count} terms")

# Save detailed logs
removal_df = pd.DataFrame(removal_log)
reweight_df = pd.DataFrame(reweight_log)

removal_df.to_csv(f'{output_dir}\\curation_removals_log.csv', index=False)
reweight_df.to_csv(f'{output_dir}\\curation_reweights_log.csv', index=False)

print(f"\nFiles saved:")
print(f"  {curated_path}")
print(f"  {output_dir}\\curation_removals_log.csv")
print(f"  {output_dir}\\curation_reweights_log.csv")

# Generate summary report
with open(f'{output_dir}\\curation_stepbystep_report.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("STEP-BY-STEP CURATION REPORT\n")
    f.write("Policy Corpus - Stage 2 (MORE RESTRICTIVE)\n")
    f.write("="*80 + "\n\n")

    f.write("SUMMARY:\n")
    f.write(f"  Original: 1200 terms\n")
    f.write(f"  Removed: {len(removal_log)} terms\n")
    f.write(f"  Reweighted: {len(reweight_log)} terms\n")
    f.write(f"  Final: {len(df)} terms\n\n")

    f.write("REMOVAL BREAKDOWN BY PHASE:\n")
    removal_df_grouped = removal_df.groupby('phase').size()
    for phase, count in removal_df_grouped.items():
        f.write(f"  {phase}: {count} terms\n")

    f.write("\nREMOVAL BREAKDOWN BY REASON:\n")
    removal_reason_grouped = removal_df.groupby('reason').size()
    for reason, count in removal_reason_grouped.items():
        f.write(f"  {reason}: {count} terms\n")

    f.write("\nFINAL DICTIONARY BY TOPIC:\n")
    for topic in df['topic'].unique():
        count = len(df[df['topic'] == topic])
        f.write(f"  {topic}: {count} terms\n")

    f.write("\n" + "="*80 + "\n")

print(f"  {output_dir}\\curation_stepbystep_report.txt")
