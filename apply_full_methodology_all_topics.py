"""
Apply COMPLETE 5-Phase Methodology to ALL Topics
Processing one topic at a time with full methodology
"""

import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pandas as pd
import re
from pathlib import Path

# Paths
DICT_DIR = Path(r"C:\Users\Home\policy-analysis\workflow_data\slavery_Slavdict_pretrained_slavery_v2\Dictionary")
INPUT_FILE = DICT_DIR / "curated_dictionary_CLEAN.csv"
OUTPUT_FILE = DICT_DIR / "curated_dictionary_FINAL_ALL_TOPICS.csv"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def apply_5_phase_methodology(topic_df, topic_name):
    """Apply complete 5-phase methodology to a single topic"""

    print("\n" + "="*80)
    print(f"PROCESSING: {topic_name}")
    print("="*80)
    print(f"Starting terms: {len(topic_df)}\n")

    issues = []

    # -------------------------------------------------------------------------
    # PHASE 1: TECHNICAL ERRORS
    # -------------------------------------------------------------------------
    print("[PHASE 1: Technical Errors]")

    # Very low cosine
    low_cosine = topic_df[(topic_df['cosine'] < 0.68) & (topic_df['is_seed'] == 0)]
    for idx, row in low_cosine.iterrows():
        issues.append((idx, 'REMOVE', f"Very low cosine ({row['cosine']:.3f})"))
        print(f"  REMOVE: {row['term']} (cosine={row['cosine']:.3f})")

    print(f"  Phase 1 actions: {len(low_cosine)}")

    # -------------------------------------------------------------------------
    # PHASE 2: SEMANTIC DRIFT
    # -------------------------------------------------------------------------
    print("\n[PHASE 2: Semantic Drift Detection]")

    # Low cosine + high weight
    drift = topic_df[(topic_df['cosine'] < 0.75) & (topic_df['weight'] >= 0.95) & (topic_df['is_seed'] == 0)]
    phase2_count = 0

    for idx, row in drift.iterrows():
        # Apply topic-specific logic
        term_lower = row['term'].lower()

        # Generic rule: lower high-weight terms with low cosine
        if row['cosine'] < 0.72:
            new_weight = 0.85
            issues.append((idx, 'REWEIGHT', new_weight, f"Low cosine ({row['cosine']:.3f}) for high weight"))
            print(f"  REWEIGHT: {row['term']} ({row['weight']:.2f} -> {new_weight:.2f}, cosine={row['cosine']:.3f})")
            phase2_count += 1

    print(f"  Phase 2 actions: {phase2_count}")

    # -------------------------------------------------------------------------
    # PHASE 3: OVERGENERALIZATION
    # -------------------------------------------------------------------------
    print("\n[PHASE 3: Overgeneralization Control]")
    phase3_count = 0

    # 3.1: Generic fragments
    generic_fragments = {
        'niveau': ['niveau'],  # Generic if specific versions exist
        'onderwijs': [],  # Keep, domain term
        'armoede': [],  # Keep, core term
        'racisme': [],  # Keep, core term
    }

    for generic_term, patterns in generic_fragments.items():
        if generic_term in topic_df['term'].values:
            specific = topic_df[topic_df['term'].str.contains(generic_term, case=False) & (topic_df['term'] != generic_term)]
            if len(specific) >= 3 and generic_term != 'onderwijs':  # Don't remove domain core terms
                idx = topic_df[topic_df['term'] == generic_term].index[0]
                issues.append((idx, 'REMOVE', f"Generic fragment - have {len(specific)} specific versions"))
                print(f"  REMOVE: {generic_term} (have {len(specific)} specific versions)")
                phase3_count += 1

    # 3.2: Ultra-high frequency (df > 100, weight > 0.70)
    ultra_high = topic_df[(topic_df['df'] > 100) & (topic_df['weight'] > 0.70)]
    for idx, row in ultra_high.iterrows():
        old_weight = row['weight']
        new_weight = max(0.50, old_weight - 0.25)
        issues.append((idx, 'REWEIGHT', new_weight, f"Ultra-high df ({row['df']})"))
        print(f"  REWEIGHT: {row['term']} ({old_weight:.2f} -> {new_weight:.2f}, df={row['df']})")
        phase3_count += 1

    # 3.3: High frequency (df 50-100, weight > 0.75)
    high_freq = topic_df[(topic_df['df'] >= 50) & (topic_df['df'] <= 100) & (topic_df['weight'] > 0.75)]
    for idx, row in high_freq.iterrows():
        old_weight = row['weight']
        new_weight = max(0.60, old_weight - 0.15)
        issues.append((idx, 'REWEIGHT', new_weight, f"High df ({row['df']})"))
        print(f"  REWEIGHT: {row['term']} ({old_weight:.2f} -> {new_weight:.2f}, df={row['df']})")
        phase3_count += 1

    # 3.4: Ambiguous terms
    ambiguous = ['college', 'organisaties', 'instituten', 'beleid', 'maatregelen']
    for term in ambiguous:
        if term in topic_df['term'].values:
            row = topic_df[topic_df['term'] == term].iloc[0]
            if row['df'] > 30 and row['weight'] > 0.70:
                idx = topic_df[topic_df['term'] == term].index[0]
                new_weight = 0.60
                issues.append((idx, 'REWEIGHT', new_weight, "Ambiguous generic term"))
                print(f"  REWEIGHT: {term} ({row['weight']:.2f} -> {new_weight:.2f}, ambiguous)")
                phase3_count += 1

    print(f"  Phase 3 actions: {phase3_count}")

    # -------------------------------------------------------------------------
    # PHASE 4: CATEGORY CORRECTIONS
    # -------------------------------------------------------------------------
    print("\n[PHASE 4: Category Corrections]")
    phase4_count = 0

    # Historical terms with high weights
    historical_terms = topic_df[
        (topic_df['term'].str.contains('historic|geschiedenis|slavernij|koloni|wic|eeuw', case=False, na=False)) &
        (topic_df['weight'] >= 0.75) &
        (~topic_df['term'].str.contains('verleden', case=False, na=False))  # 'verleden' is seed, keep
    ]

    for idx, row in historical_terms.iterrows():
        if row['is_seed'] == 0:  # Don't recategorize seeds
            new_weight = 0.55
            issues.append((idx, 'RECATEGORIZE', new_weight, 'era_context', "Historical context term"))
            print(f"  RECATEGORIZE: {row['term']} -> era_context (0.55)")
            phase4_count += 1

    print(f"  Phase 4 actions: {phase4_count}")

    # -------------------------------------------------------------------------
    # PHASE 5: WEIGHT CALIBRATION
    # -------------------------------------------------------------------------
    print("\n[PHASE 5: Weight Calibration]")
    phase5_count = 0

    # 5.1: Semantic distance dampening (cosine < 0.75, weight >= 0.85)
    distance_dampen = topic_df[(topic_df['cosine'] < 0.75) & (topic_df['weight'] >= 0.85) & (topic_df['is_seed'] == 0)]
    for idx, row in distance_dampen.iterrows():
        old_weight = row['weight']
        new_weight = old_weight - 0.10
        issues.append((idx, 'REWEIGHT', new_weight, f"Semantic distance (cosine={row['cosine']:.3f})"))
        print(f"  REWEIGHT: {row['term']} ({old_weight:.2f} -> {new_weight:.2f}, cosine={row['cosine']:.3f})")
        phase5_count += 1

    # 5.2: Core problem review (expanded terms at 1.00)
    core_expanded = topic_df[(topic_df['weight'] >= 0.98) & (topic_df['is_seed'] == 0)]
    for idx, row in core_expanded.iterrows():
        if row['cosine'] < 0.90:
            new_weight = 0.95
            issues.append((idx, 'REWEIGHT', new_weight, "Core -> strong_problem"))
            print(f"  REWEIGHT: {row['term']} (1.00 -> 0.95, cosine={row['cosine']:.3f})")
            phase5_count += 1

    print(f"  Phase 5 actions: {phase5_count}")

    # -------------------------------------------------------------------------
    # APPLY ALL DECISIONS
    # -------------------------------------------------------------------------
    print(f"\n[APPLYING DECISIONS]")
    total_actions = len(issues)
    print(f"  Total actions: {total_actions}")

    topic_filtered = topic_df.copy()

    for issue in issues:
        idx = issue[0]
        action = issue[1]

        if action == 'REMOVE':
            topic_filtered = topic_filtered.drop(idx)

        elif action == 'REWEIGHT':
            new_weight = issue[2]
            topic_filtered.loc[idx, 'weight'] = new_weight

        elif action == 'RECATEGORIZE':
            new_weight = issue[2]
            new_category = issue[3]
            topic_filtered.loc[idx, 'weight'] = new_weight
            topic_filtered.loc[idx, 'category'] = new_category

    print(f"  Final terms: {len(topic_filtered)} (removed {len(topic_df) - len(topic_filtered)})")

    return topic_filtered

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("="*80)
    print("COMPLETE 5-PHASE METHODOLOGY - ALL TOPICS")
    print("="*80)

    # Load
    df = pd.read_csv(INPUT_FILE, encoding='utf-8-sig')
    print(f"\nStarting total: {len(df)} terms")

    topics = [
        'Educational Disadvantage & Brain Drain',
        'Governance Distrust & Corruption',
        'Persistent Poverty & Economic Vulnerability',
        'Social Fragmentation & Racism'
    ]

    # Process each topic
    filtered_topics = []

    for topic in topics:
        topic_df = df[df['topic'] == topic].copy()
        filtered = apply_5_phase_methodology(topic_df, topic)
        filtered_topics.append(filtered)

    # Combine all
    df_final = pd.concat(filtered_topics, ignore_index=True)
    df_final = df_final.sort_values(['topic', 'weight', 'term'], ascending=[True, False, True])

    # Save
    df_final.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')

    # Final statistics
    print("\n" + "="*80)
    print("COMPLETE - ALL TOPICS FILTERED")
    print("="*80)
    print(f"\nSaved: {OUTPUT_FILE.name}")
    print(f"Starting: {len(df)} terms")
    print(f"Final: {len(df_final)} terms")
    print(f"Removed: {len(df) - len(df_final)} terms")

    print("\n[BY TOPIC]")
    for topic in topics:
        original = len(df[df['topic'] == topic])
        final = len(df_final[df_final['topic'] == topic])
        removed = original - final
        print(f"\n{topic}:")
        print(f"  Original: {original} | Final: {final} | Removed: {removed}")

    print("\n[WEIGHT DISTRIBUTION - ALL TOPICS]")
    for w in [1.00, 0.95, 0.85, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50]:
        count = ((df_final['weight'] >= w - 0.02) & (df_final['weight'] <= w + 0.02)).sum()
        if count > 0:
            pct = count / len(df_final) * 100
            print(f"  {w:.2f}: {count:4d} terms ({pct:5.1f}%)")

if __name__ == "__main__":
    main()
