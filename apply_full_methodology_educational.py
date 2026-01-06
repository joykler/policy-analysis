"""
Apply COMPLETE 5-Phase Methodology to Educational Topic
Following A__DICTIONARY_CURATION_GUIDE.md systematically
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
OUTPUT_FILE = DICT_DIR / "curated_dictionary_EDUCATIONAL_FULL_METHODOLOGY.csv"

# ============================================================================
# PHASE 1: TECHNICAL ERRORS (already done, but double-check)
# ============================================================================

def phase1_check_technical_errors(edu):
    """Phase 1: Check for any remaining technical errors"""
    print("\n" + "="*80)
    print("PHASE 1: Technical Errors Check")
    print("="*80)

    issues = []

    # Check for very short terms that might be fragments
    short_terms = edu[(edu['term'].str.len() < 4) & (edu['is_seed'] == 0)]
    if len(short_terms) > 0:
        print(f"\n⚠️  Found {len(short_terms)} very short expanded terms:")
        for idx, row in short_terms.iterrows():
            print(f"  - '{row['term']}' (len={len(row['term'])}, parent: {row['parent']})")
            issues.append((idx, 'REMOVE', f"Very short term (len={len(row['term'])}), likely fragment"))

    # Check for terms with very low cosine that slipped through
    low_cosine = edu[(edu['cosine'] < 0.68) & (edu['is_seed'] == 0)]
    if len(low_cosine) > 0:
        print(f"\n⚠️  Found {len(low_cosine)} terms with very low cosine (<0.68):")
        for idx, row in low_cosine.iterrows():
            print(f"  - '{row['term']}' (cosine={row['cosine']:.3f}, parent: {row['parent']})")
            issues.append((idx, 'REMOVE', f"Very low cosine ({row['cosine']:.3f})"))

    print(f"\nPhase 1: {len(issues)} issues found")
    return issues

# ============================================================================
# PHASE 2: SEMANTIC DRIFT
# ============================================================================

def phase2_semantic_drift(edu):
    """Phase 2: Identify semantic drift"""
    print("\n" + "="*80)
    print("PHASE 2: Semantic Drift Detection")
    print("="*80)

    issues = []

    # Low cosine + high weight = semantic drift red flag
    drift_candidates = edu[(edu['cosine'] < 0.75) & (edu['weight'] >= 0.95) & (edu['is_seed'] == 0)]

    if len(drift_candidates) > 0:
        print(f"\n⚠️  Found {len(drift_candidates)} potential semantic drift terms:")
        print("    (low cosine < 0.75 + high weight >= 0.95)\n")

        for idx, row in drift_candidates.iterrows():
            print(f"  Term: '{row['term']}'")
            print(f"    Parent: '{row['parent']}' | Cosine: {row['cosine']:.3f} | Weight: {row['weight']:.2f}")

            # Manual analysis for educational terms
            term = row['term'].lower()
            parent = row['parent'].lower()

            # Check for specific patterns
            if 'methoden' in term or 'methodes' in term:
                # Teaching methods - related but not core problem
                issues.append((idx, 'REWEIGHT', 0.75, "Methods are related discussion, not core problem"))
                print(f"    -> REWEIGHT to 0.75 (methods are process, not problem)\n")

            elif 'wetgeving' in term:
                # Legislation - institutional context, not core
                issues.append((idx, 'REWEIGHT', 0.75, "Legislation is institutional context"))
                print(f"    -> REWEIGHT to 0.75 (institutional context)\n")

            else:
                # Needs manual review
                print(f"    -> MANUAL REVIEW NEEDED\n")

    print(f"Phase 2: {len(issues)} actions recommended")
    return issues

# ============================================================================
# PHASE 3: OVERGENERALIZATION CONTROL
# ============================================================================

def phase3_overgeneralization(edu):
    """Phase 3: Control overgeneralization"""
    print("\n" + "="*80)
    print("PHASE 3: Overgeneralization Control")
    print("="*80)

    issues = []

    # 3.1: Generic fragments when specific versions exist
    print("\n[3.1] Generic Fragments of Specific Terms")

    # Check niveau
    if 'niveau' in edu['term'].values:
        specific = edu[edu['term'].str.contains('niveau', case=False) & (edu['term'] != 'niveau')]
        if len(specific) >= 3:  # Have 3+ specific versions
            mask = edu['term'] == 'niveau'
            idx = edu[mask].index[0]
            issues.append((idx, 'REMOVE', None, f"Generic fragment - have {len(specific)} specific versions"))
            print(f"  ✓ REMOVE 'niveau' - have specific: {specific['term'].tolist()[:3]}...")

    # 3.2: Ultra-high frequency (df > 100)
    print("\n[3.2] Ultra-High Document Frequency (df > 100, weight > 0.70)")

    ultra_high = edu[(edu['df'] > 100) & (edu['weight'] > 0.70)]
    for idx, row in ultra_high.iterrows():
        old_weight = row['weight']
        new_weight = max(0.50, old_weight - 0.25)
        issues.append((idx, 'REWEIGHT', new_weight, f"Ultra-high df ({row['df']}) overwhelms signal"))
        print(f"  ✓ REWEIGHT '{row['term']}': {old_weight:.2f} -> {new_weight:.2f} (df={row['df']})")

    # 3.3: High frequency (df 50-100, weight > 0.75)
    print("\n[3.3] High Document Frequency (df 50-100, weight > 0.75)")

    high_freq = edu[(edu['df'] >= 50) & (edu['df'] <= 100) & (edu['weight'] > 0.75)]
    for idx, row in high_freq.iterrows():
        old_weight = row['weight']
        new_weight = max(0.60, old_weight - 0.15)
        issues.append((idx, 'REWEIGHT', new_weight, f"High df ({row['df']}) - reduce weight"))
        print(f"  ✓ REWEIGHT '{row['term']}': {old_weight:.2f} -> {new_weight:.2f} (df={row['df']})")

    # 3.4: Ambiguous generic institutional terms
    print("\n[3.4] Ambiguous Institutional Terms")

    generic_institutional = ['college', 'organisaties', 'instituten']
    for term in generic_institutional:
        if term in edu['term'].values:
            row = edu[edu['term'] == term].iloc[0]
            if row['df'] > 30 and row['weight'] > 0.70:
                idx = edu[edu['term'] == term].index[0]
                new_weight = 0.60
                issues.append((idx, 'REWEIGHT', new_weight, f"Ambiguous generic term"))
                print(f"  ✓ REWEIGHT '{term}': {row['weight']:.2f} -> {new_weight:.2f} (ambiguous)")

    print(f"\nPhase 3: {len(issues)} actions recommended")
    return issues

# ============================================================================
# PHASE 4: CATEGORY CORRECTIONS
# ============================================================================

def phase4_category_corrections(edu):
    """Phase 4: Check for miscategorization"""
    print("\n" + "="*80)
    print("PHASE 4: Category Corrections")
    print("="*80)

    issues = []

    # Check for historical terms in contemporary problem categories
    historical_markers = [
        'historie', 'historisch', 'geschiedenis', 'koloniaal', 'koloniale',
        'slavernij', 'eeuw', 'wic', 'compagnie', 'vroeger', 'vroegere'
    ]

    for marker in historical_markers:
        historical_terms = edu[
            (edu['term'].str.contains(marker, case=False, na=False)) &
            (edu['weight'] >= 0.85) &
            (edu['category'].isin(['core_problem', 'strong_problem', 'related_strong']))
        ]

        if len(historical_terms) > 0:
            print(f"\n⚠️  Historical terms with marker '{marker}' in high categories:")
            for idx, row in historical_terms.iterrows():
                print(f"  Term: '{row['term']}'")
                print(f"    Weight: {row['weight']:.2f} | Category: {row['category']}")

                # Determine if truly historical or contemporary usage
                term_lower = row['term'].lower()

                # Always historical - move to era_context
                if row['term'] in ['wic', 'slavernijverleden', 'koloniale', 'koloniaal']:
                    issues.append((idx, 'RECATEGORIZE', 0.55, 'era_context', f"Historical context marker"))
                    print(f"    -> RECATEGORIZE to era_context (0.55)\n")

                # Historical but relevant to domain - keep but lower
                elif marker in ['geschiedenis', 'historisch', 'historie']:
                    if row['weight'] > 0.65:
                        new_weight = 0.55
                        issues.append((idx, 'RECATEGORIZE', new_weight, 'era_context', f"Historical term"))
                        print(f"    -> RECATEGORIZE to era_context ({new_weight:.2f})\n")

    print(f"Phase 4: {len(issues)} actions recommended")
    return issues

# ============================================================================
# PHASE 5: WEIGHT CALIBRATION
# ============================================================================

def phase5_weight_calibration(edu):
    """Phase 5: Fine-tune weights"""
    print("\n" + "="*80)
    print("PHASE 5: Weight Calibration")
    print("="*80)

    issues = []

    # Semantic distance dampening for strong terms (not yet caught)
    print("\n[5.1] Semantic Distance Dampening (cosine < 0.75, weight >= 0.85)")

    distance_dampen = edu[(edu['cosine'] < 0.75) & (edu['weight'] >= 0.85) & (edu['is_seed'] == 0)]
    for idx, row in distance_dampen.iterrows():
        old_weight = row['weight']
        new_weight = old_weight - 0.10
        issues.append((idx, 'REWEIGHT', new_weight, f"Semantic distance dampening (cosine={row['cosine']:.3f})"))
        print(f"  ✓ REWEIGHT '{row['term']}': {old_weight:.2f} -> {new_weight:.2f} (cosine={row['cosine']:.3f})")

    # Check for expanded terms at 1.00 weight - should be rare
    print("\n[5.2] Core Problem Weight Review (expanded terms at 1.00)")

    core_expanded = edu[(edu['weight'] >= 0.98) & (edu['is_seed'] == 0)]
    if len(core_expanded) > 0:
        print(f"\n⚠️  Found {len(core_expanded)} expanded terms at core_problem (1.00) weight:")
        for idx, row in core_expanded.iterrows():
            print(f"  Term: '{row['term']}' (parent: '{row['parent']}', cosine: {row['cosine']:.3f})")

            # Most should be strong_problem, not core
            if row['cosine'] < 0.90:
                new_weight = 0.95
                issues.append((idx, 'REWEIGHT', new_weight, "Lower from core to strong_problem"))
                print(f"    -> REWEIGHT to 0.95 (strong_problem more appropriate)\n")
            else:
                print(f"    -> KEEP at 1.00 (very high cosine, true synonym)\n")

    print(f"Phase 5: {len(issues)} actions recommended")
    return issues

# ============================================================================
# APPLY ALL DECISIONS
# ============================================================================

def apply_decisions(edu, all_issues):
    """Apply all accumulated decisions"""
    print("\n" + "="*80)
    print("APPLYING ALL DECISIONS")
    print("="*80)

    edu_filtered = edu.copy()
    edu_filtered['action'] = 'KEEP'
    edu_filtered['action_reason'] = ''

    remove_count = 0
    reweight_count = 0
    recategorize_count = 0

    for issue in all_issues:
        idx = issue[0]
        action = issue[1]

        if action == 'REMOVE':
            reason = issue[2]
            edu_filtered.loc[idx, 'action'] = 'REMOVE'
            edu_filtered.loc[idx, 'action_reason'] = reason
            remove_count += 1

        elif action == 'REWEIGHT':
            new_weight = issue[2]
            reason = issue[3]
            edu_filtered.loc[idx, 'weight'] = new_weight
            edu_filtered.loc[idx, 'action'] = 'REWEIGHT'
            edu_filtered.loc[idx, 'action_reason'] = reason
            reweight_count += 1

        elif action == 'RECATEGORIZE':
            new_weight = issue[2]
            new_category = issue[3]
            reason = issue[4]
            edu_filtered.loc[idx, 'weight'] = new_weight
            edu_filtered.loc[idx, 'category'] = new_category
            edu_filtered.loc[idx, 'action'] = 'RECATEGORIZE'
            edu_filtered.loc[idx, 'action_reason'] = reason
            recategorize_count += 1

    print(f"\nActions applied:")
    print(f"  REMOVE: {remove_count}")
    print(f"  REWEIGHT: {reweight_count}")
    print(f"  RECATEGORIZE: {recategorize_count}")

    # Filter out removals
    edu_final = edu_filtered[edu_filtered['action'] != 'REMOVE'].copy()

    print(f"\nFinal term count: {len(edu_final)} (removed {len(edu_filtered) - len(edu_final)})")

    return edu_final

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("="*80)
    print("COMPLETE 5-PHASE METHODOLOGY - EDUCATIONAL TOPIC")
    print("="*80)

    # Load
    df = pd.read_csv(INPUT_FILE, encoding='utf-8-sig')
    edu_topic = 'Educational Disadvantage & Brain Drain'

    edu = df[df['topic'] == edu_topic].copy()
    other = df[df['topic'] != edu_topic].copy()

    print(f"\nStarting Educational terms: {len(edu)}")

    # Apply all 5 phases
    all_issues = []

    all_issues.extend(phase1_check_technical_errors(edu))
    all_issues.extend(phase2_semantic_drift(edu))
    all_issues.extend(phase3_overgeneralization(edu))
    all_issues.extend(phase4_category_corrections(edu))
    all_issues.extend(phase5_weight_calibration(edu))

    # Apply decisions
    edu_final = apply_decisions(edu, all_issues)

    # Combine with other topics
    edu_final_clean = edu_final[['topic', 'term', 'cosine', 'df', 'weight', 'category', 'parent', 'is_seed']]
    df_final = pd.concat([edu_final_clean, other], ignore_index=True)
    df_final = df_final.sort_values(['topic', 'weight', 'term'], ascending=[True, False, True])

    # Save
    df_final.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')

    print("\n" + "="*80)
    print("COMPLETE - EDUCATIONAL TOPIC FILTERED")
    print("="*80)
    print(f"\nSaved: {OUTPUT_FILE.name}")
    print(f"Total terms: {len(df_final)}")
    print(f"Educational terms: {len(edu_final_clean)}")

    # Show weight distribution
    print(f"\nEducational weight distribution:")
    for w in [1.00, 0.95, 0.85, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50]:
        count = ((edu_final_clean['weight'] >= w - 0.02) & (edu_final_clean['weight'] <= w + 0.02)).sum()
        if count > 0:
            print(f"  {w:.2f}: {count:3d} terms")

if __name__ == "__main__":
    main()
