"""
Dictionary Curation Script for slavery_Slavdict_pretrained_slavery_v3
Applies systematic fixes identified in cross-topic analysis
"""

import pandas as pd
import json
from datetime import datetime

def curate_dictionary(input_path, output_path):
    """Apply curation rules to dictionary"""

    # Read original
    df = pd.read_csv(input_path)
    original_count = len(df)

    print(f"Original dictionary: {len(df)} terms")
    print(f"Unique terms: {df['term'].nunique()}")
    print()

    curation_log = {
        'timestamp': datetime.now().isoformat(),
        'original_count': original_count,
        'actions': {
            'removed_universal': [],
            'removed_semantic_drift': [],
            'weight_adjusted': [],
            'recategorized': []
        }
    }

    # ========================================
    # PHASE 1: REMOVE UNIVERSAL ERRORS
    # ========================================
    print("PHASE 1: Removing universal errors...")

    # 1.1 Morphological fragments (all topics)
    fragments = ['bon', 'schiedenis', 'denten', 'plant', 'schaffing', 'partement']

    for frag in fragments:
        removed = df[df['term'] == frag]
        if len(removed) > 0:
            topics = removed['topic'].tolist()
            df = df[df['term'] != frag]
            curation_log['actions']['removed_universal'].append({
                'term': frag,
                'reason': 'morphological_fragment',
                'topics': topics,
                'count': len(removed)
            })
            print(f"  [OK] Removed '{frag}' from {len(removed)} topics (morphological fragment)")

    # 1.2 Wrong geographic scope
    cuba_removed = df[df['term'] == 'cuba']
    if len(cuba_removed) > 0:
        topics = cuba_removed['topic'].tolist()
        df = df[df['term'] != 'cuba']
        curation_log['actions']['removed_universal'].append({
            'term': 'cuba',
            'reason': 'wrong_geographic_scope',
            'topics': topics,
            'count': len(cuba_removed)
        })
        print(f"  [OK] Removed 'cuba' from {len(cuba_removed)} topics (wrong geographic scope)")

    print(f"  Phase 1 complete: Removed {original_count - len(df)} entries")
    print()

    # ========================================
    # PHASE 2: REMOVE SEMANTIC DRIFT (OPPOSITE MEANINGS)
    # ========================================
    print("PHASE 2: Removing semantic drift (opposite meanings)...")

    # 2.1 Educational topic - opposite meanings
    educational_opposites = ['immigratie', 'deportatie', 'deportaties', 'remigratie']
    for term in educational_opposites:
        removed = df[(df['term'] == term) & (df['topic'] == 'Educational Disadvantage & Brain Drain')]
        if len(removed) > 0:
            df = df[~((df['term'] == term) & (df['topic'] == 'Educational Disadvantage & Brain Drain'))]
            curation_log['actions']['removed_semantic_drift'].append({
                'term': term,
                'topic': 'Educational Disadvantage & Brain Drain',
                'reason': 'opposite_meaning_immigration_vs_emigration',
                'weight': removed.iloc[0]['weight']
            })
            print(f"  [OK] Removed '{term}' from Educational (opposite meaning)")

    # 2.2 Racism topic - uitsluiting family (opposite meanings)
    racism_opposites = [
        'ontsluiting', 'aansluiten', 'aansluit', 'insluiting', 'uitsluitsel',
        'afsluiten', 'afsluiting', 'sluiten', 'sluiting', 'sluit', 'afsluit',
        'opsluiting', 'uitreding', 'uitlating', 'verscheidenheid'
    ]
    for term in racism_opposites:
        removed = df[(df['term'] == term) & (df['topic'] == 'Social Fragmentation & Racism')]
        if len(removed) > 0:
            df = df[~((df['term'] == term) & (df['topic'] == 'Social Fragmentation & Racism'))]
            curation_log['actions']['removed_semantic_drift'].append({
                'term': term,
                'topic': 'Social Fragmentation & Racism',
                'reason': 'opposite_or_different_meaning_from_uitsluiting',
                'weight': removed.iloc[0]['weight']
            })
            print(f"  [OK] Removed '{term}' from Racism (opposite/different meaning)")

    # 2.3 Governance topic - wantrouwen family (opposite meanings - trust/marriage)
    governance_opposites = [
        'vertrouwen', 'trouw', 'vertrouweling', 'vertrouwensband', 'vertrouwde',
        'verwantschap', 'hertrouwde', 'vertrouwden', 'trouwde', 'trouwen',
        'huwelijk', 'vertrouwd', 'rouw'
    ]
    for term in governance_opposites:
        removed = df[(df['term'] == term) & (df['topic'] == 'Governance Distrust & Corruption')]
        if len(removed) > 0:
            df = df[~((df['term'] == term) & (df['topic'] == 'Governance Distrust & Corruption'))]
            curation_log['actions']['removed_semantic_drift'].append({
                'term': term,
                'topic': 'Governance Distrust & Corruption',
                'reason': 'opposite_meaning_trust_marriage_from_wantrouwen',
                'weight': removed.iloc[0]['weight']
            })
            print(f"  [OK] Removed '{term}' from Governance (trust/marriage - opposite)")

    # 2.4 Governance topic - omkoping family (unrelated meanings)
    governance_omkoping = [
        'omverwerping', 'omzetting', 'koperen', 'omslag', 'verwijdering',
        'afdwingen', 'omging', 'abrupt', 'vernietiging'
    ]
    for term in governance_omkoping:
        removed = df[(df['term'] == term) & (df['topic'] == 'Governance Distrust & Corruption')]
        if len(removed) > 0:
            df = df[~((df['term'] == term) & (df['topic'] == 'Governance Distrust & Corruption'))]
            curation_log['actions']['removed_semantic_drift'].append({
                'term': term,
                'topic': 'Governance Distrust & Corruption',
                'reason': 'unrelated_meaning_from_omkoping',
                'weight': removed.iloc[0]['weight']
            })
            print(f"  [OK] Removed '{term}' from Governance (unrelated to bribery)")

    # 2.5 Governance - other semantic drift
    governance_other = ['nazisme', 'daadkrachtig']
    for term in governance_other:
        removed = df[(df['term'] == term) & (df['topic'] == 'Governance Distrust & Corruption')]
        if len(removed) > 0:
            df = df[~((df['term'] == term) & (df['topic'] == 'Governance Distrust & Corruption'))]
            curation_log['actions']['removed_semantic_drift'].append({
                'term': term,
                'topic': 'Governance Distrust & Corruption',
                'reason': 'semantic_drift',
                'weight': removed.iloc[0]['weight']
            })
            print(f"  [OK] Removed '{term}' from Governance (semantic drift)")

    # 2.6 Economic topic - opposite meanings
    economic_opposites = ['onafhankelijkheid', 'onschuld']
    for term in economic_opposites:
        removed = df[(df['term'] == term) & (df['topic'] == 'Persistent Poverty & Economic Vulnerability')]
        if len(removed) > 0:
            df = df[~((df['term'] == term) & (df['topic'] == 'Persistent Poverty & Economic Vulnerability'))]
            curation_log['actions']['removed_semantic_drift'].append({
                'term': term,
                'topic': 'Persistent Poverty & Economic Vulnerability',
                'reason': 'opposite_meaning',
                'weight': removed.iloc[0]['weight']
            })
            print(f"  [OK] Removed '{term}' from Economic (opposite meaning)")

    # 2.7 Economic topic - emotional vs financial debt
    economic_guilt = ['schuldgevoel', 'schuldgevoelens']
    for term in economic_guilt:
        removed = df[(df['term'] == term) & (df['topic'] == 'Persistent Poverty & Economic Vulnerability')]
        if len(removed) > 0:
            df = df[~((df['term'] == term) & (df['topic'] == 'Persistent Poverty & Economic Vulnerability'))]
            curation_log['actions']['removed_semantic_drift'].append({
                'term': term,
                'topic': 'Persistent Poverty & Economic Vulnerability',
                'reason': 'emotional_guilt_not_financial_debt',
                'weight': removed.iloc[0]['weight']
            })
            print(f"  [OK] Removed '{term}' from Economic (emotional vs. financial)")

    phase2_removed = original_count - len(df) - sum(len(a['topics']) if 'topics' in a else 1 for a in curation_log['actions']['removed_universal'])
    print(f"  Phase 2 complete: Removed {phase2_removed} semantic drift entries")
    print()

    # ========================================
    # PHASE 3: WEIGHT ADJUSTMENTS
    # ========================================
    print("PHASE 3: Adjusting weights for high-frequency terms...")

    weight_adjustments = [
        # Educational
        ('Educational Disadvantage & Brain Drain', 'nederlandse', 1195, 0.85, 0.60),
        ('Educational Disadvantage & Brain Drain', 'nederland', 1137, 0.85, 0.60),
        ('Educational Disadvantage & Brain Drain', 'nederlands', 279, 0.85, 0.70),
        ('Educational Disadvantage & Brain Drain', 'onderwijs', 172, 0.75, 0.65),
        ('Educational Disadvantage & Brain Drain', 'scholen', 121, 0.75, 0.70),
        ('Educational Disadvantage & Brain Drain', 'school', 110, 0.75, 0.70),
        ('Educational Disadvantage & Brain Drain', 'kinderen', 266, 0.75, 0.65),
        ('Educational Disadvantage & Brain Drain', 'niveau', 109, 0.85, 0.70),

        # Governance
        ('Governance Distrust & Corruption', 'kamer', 466, 0.75, 0.60),
        ('Governance Distrust & Corruption', 'ministerie', 397, 0.75, 0.65),
        ('Governance Distrust & Corruption', 'regering', 338, 0.75, 0.65),
        ('Governance Distrust & Corruption', 'minister', 315, 0.75, 0.65),
        ('Governance Distrust & Corruption', 'wet', 288, 0.75, 0.65),
        ('Governance Distrust & Corruption', 'overheid', 244, 0.75, 0.65),
        ('Governance Distrust & Corruption', 'debat', 200, 0.75, 0.65),
        ('Governance Distrust & Corruption', 'organisatie', 163, 0.75, 0.60),
        ('Governance Distrust & Corruption', 'bestuur', 168, 0.75, 0.65),

        # Economic
        ('Persistent Poverty & Economic Vulnerability', 'werk', 339, 0.75, 0.65),
        ('Persistent Poverty & Economic Vulnerability', 'werken', 273, 0.75, 0.65),
        ('Persistent Poverty & Economic Vulnerability', 'handel', 282, 0.75, 0.65),
        ('Persistent Poverty & Economic Vulnerability', 'financiële', 262, 0.70, 0.60),
        ('Persistent Poverty & Economic Vulnerability', 'economische', 255, 0.75, 0.65),
        ('Persistent Poverty & Economic Vulnerability', 'plantages', 218, 0.85, 0.75),
        ('Persistent Poverty & Economic Vulnerability', 'financieel', 139, 0.70, 0.60),
        ('Persistent Poverty & Economic Vulnerability', 'planters', 121, 0.85, 0.75),
        ('Persistent Poverty & Economic Vulnerability', 'handelaren', 84, 0.75, 0.65),

        # Racism
        ('Social Fragmentation & Racism', 'discriminatie', 265, 0.85, 0.70),
        ('Social Fragmentation & Racism', 'slaaf', 337, 0.75, 0.65),
        ('Social Fragmentation & Racism', 'slaafgemaakten', 359, 0.75, 0.70),
        ('Social Fragmentation & Racism', 'slaafgemaakte', 152, 0.75, 0.70),
    ]

    for topic, term, df_val, old_weight, new_weight in weight_adjustments:
        mask = (df['topic'] == topic) & (df['term'] == term) & (df['weight'] == old_weight)
        if mask.any():
            df.loc[mask, 'weight'] = new_weight
            curation_log['actions']['weight_adjusted'].append({
                'term': term,
                'topic': topic,
                'df': df_val,
                'old_weight': old_weight,
                'new_weight': new_weight,
                'reason': 'high_frequency_dampening'
            })
            print(f"  [OK] Adjusted '{term}' in {topic.split()[0]:15} | df={df_val:4} | {old_weight} -> {new_weight}")

    print(f"  Phase 3 complete: Adjusted {len(curation_log['actions']['weight_adjusted'])} weights")
    print()

    # ========================================
    # PHASE 4: REMOVE ADDITIONAL PROBLEMATIC TERMS
    # ========================================
    print("PHASE 4: Removing additional problematic terms...")

    # Educational - polysemy
    problematic = [
        ('Educational Disadvantage & Brain Drain', 'college', 'polysemy_executive_board_not_school'),
        ('Educational Disadvantage & Brain Drain', 'moeder', 'overgeneralization_from_moedertaal'),
    ]

    for topic, term, reason in problematic:
        removed = df[(df['term'] == term) & (df['topic'] == topic)]
        if len(removed) > 0:
            df = df[~((df['term'] == term) & (df['topic'] == topic))]
            curation_log['actions']['removed_semantic_drift'].append({
                'term': term,
                'topic': topic,
                'reason': reason,
                'weight': removed.iloc[0]['weight']
            })
            print(f"  [OK] Removed '{term}' from {topic.split()[0]} ({reason})")

    # Governance - overgeneralization
    gov_overgen = [
        ('Governance Distrust & Corruption', 'uitdrukking', 'semantic_drift_from_onderdrukking'),
        ('Governance Distrust & Corruption', 'uitdrukkingen', 'semantic_drift_from_onderdrukking'),
    ]

    for topic, term, reason in gov_overgen:
        removed = df[(df['term'] == term) & (df['topic'] == topic)]
        if len(removed) > 0:
            df = df[~((df['term'] == term) & (df['topic'] == topic))]
            curation_log['actions']['removed_semantic_drift'].append({
                'term': term,
                'topic': topic,
                'reason': reason,
                'weight': removed.iloc[0]['weight']
            })
            print(f"  [OK] Removed '{term}' from {topic.split()[0]} ({reason})")

    # Economic - wrong meanings
    econ_wrong = [
        ('Persistent Poverty & Economic Vulnerability', 'werkelijke', 'means_actual_not_work'),
        ('Persistent Poverty & Economic Vulnerability', 'werkelijk', 'means_actual_not_work'),
        ('Persistent Poverty & Economic Vulnerability', 'behandel', 'means_treat_not_trade'),
        ('Persistent Poverty & Economic Vulnerability', 'planten', 'means_plants_too_generic'),
        ('Persistent Poverty & Economic Vulnerability', 'tuin', 'means_garden_too_generic'),
    ]

    for topic, term, reason in econ_wrong:
        removed = df[(df['term'] == term) & (df['topic'] == topic)]
        if len(removed) > 0:
            df = df[~((df['term'] == term) & (df['topic'] == topic))]
            curation_log['actions']['removed_semantic_drift'].append({
                'term': term,
                'topic': topic,
                'reason': reason,
                'weight': removed.iloc[0]['weight']
            })
            print(f"  [OK] Removed '{term}' from {topic.split()[0]} ({reason})")

    # Racism - additional problematic from afschaffing family
    racism_afschaffing = [
        'afstaan', 'afdracht', 'afnemen', 'afstel', 'afrekening', 'afbouw',
        'aflossing', 'aflossingen', 'afzet', 'afhandeling', 'afgeven', 'afleggen',
        'afwerpen', 'verschuiving', 'afkeer', 'omzetting', 'afbetaling',
        'verwerven', 'afname', 'afrekeningen', 'afdwingen', 'vermindering',
        'verveling', 'afwijzen', 'opschaling', 'verschansing', 'verlaging'
    ]

    for term in racism_afschaffing:
        removed = df[(df['term'] == term) & (df['topic'] == 'Social Fragmentation & Racism')]
        if len(removed) > 0:
            df = df[~((df['term'] == term) & (df['topic'] == 'Social Fragmentation & Racism'))]
            curation_log['actions']['removed_semantic_drift'].append({
                'term': term,
                'topic': 'Social Fragmentation & Racism',
                'reason': 'semantic_drift_from_afschaffing',
                'weight': removed.iloc[0]['weight']
            })
            print(f"  [OK] Removed '{term}' from Racism (afschaffing drift)")

    # Economic - afschaffing family
    for term in racism_afschaffing:
        removed = df[(df['term'] == term) & (df['topic'] == 'Persistent Poverty & Economic Vulnerability')]
        if len(removed) > 0:
            df = df[~((df['term'] == term) & (df['topic'] == 'Persistent Poverty & Economic Vulnerability'))]
            curation_log['actions']['removed_semantic_drift'].append({
                'term': term,
                'topic': 'Persistent Poverty & Economic Vulnerability',
                'reason': 'semantic_drift_from_afschaffing',
                'weight': removed.iloc[0]['weight']
            })
            print(f"  [OK] Removed '{term}' from Economic (afschaffing drift)")

    print(f"  Phase 4 complete")
    print()

    # ========================================
    # SUMMARY
    # ========================================
    print("=" * 60)
    print("CURATION COMPLETE")
    print("=" * 60)
    print(f"Original terms: {original_count}")
    print(f"Curated terms: {len(df)}")
    print(f"Removed: {original_count - len(df)} ({(original_count - len(df))/original_count*100:.1f}%)")
    print()
    print(f"Actions taken:")
    print(f"  - Universal errors removed: {len(curation_log['actions']['removed_universal'])}")
    print(f"  - Semantic drift removed: {len(curation_log['actions']['removed_semantic_drift'])}")
    print(f"  - Weights adjusted: {len(curation_log['actions']['weight_adjusted'])}")
    print()

    # Per-topic summary
    print("Per-topic breakdown:")
    for topic in df['topic'].unique():
        topic_count = len(df[df['topic'] == topic])
        print(f"  {topic}: {topic_count} terms")
    print()

    curation_log['final_count'] = len(df)
    curation_log['removed_total'] = original_count - len(df)
    curation_log['unique_terms'] = df['term'].nunique()

    # Save curated dictionary
    df.to_csv(output_path, index=False)
    print(f"[OK] Saved curated dictionary to: {output_path}")

    # Save curation log
    log_path = output_path.replace('.csv', '_curation_log.json')
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(curation_log, f, indent=2, ensure_ascii=False)
    print(f"[OK] Saved curation log to: {log_path}")

    return df, curation_log

if __name__ == '__main__':
    input_path = r'C:\Users\Home\policy-analysis\workflow_data\slavery_Slavdict_pretrained_slavery_v3\Dictionary\expanded_candidates.csv'
    output_path = r'C:\Users\Home\policy-analysis\workflow_data\slavery_Slavdict_pretrained_slavery_v3\Dictionary\curated_dictionary.csv'

    df_curated, log = curate_dictionary(input_path, output_path)
