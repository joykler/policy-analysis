"""
Apply Overgeneralization Filters to Educational Topic
Following A__DICTIONARY_CURATION_GUIDE.md Phase 3 methodology
"""

import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pandas as pd
from pathlib import Path

# Paths
DICT_DIR = Path(r"C:\Users\Home\policy-analysis\workflow_data\slavery_Slavdict_pretrained_slavery_v2\Dictionary")
INPUT_FILE = DICT_DIR / "curated_dictionary_CLEAN.csv"
OUTPUT_FILE = DICT_DIR / "curated_dictionary_EDUCATIONAL_FILTERED.csv"

def main():
    print("="*80)
    print("OVERGENERALIZATION FILTERING - EDUCATIONAL TOPIC")
    print("Following Phase 3 Methodology from A__DICTIONARY_CURATION_GUIDE.md")
    print("="*80)

    # Load dictionary
    df = pd.read_csv(INPUT_FILE, encoding='utf-8-sig')
    edu_topic = 'Educational Disadvantage & Brain Drain'

    # Separate educational and other topics
    edu = df[df['topic'] == edu_topic].copy()
    other = df[df['topic'] != edu_topic].copy()

    print(f"\nStarting Educational topic: {len(edu)} terms")

    # Track decisions
    edu['action'] = 'KEEP'
    edu['action_reason'] = ''
    edu['weight_new'] = edu['weight']

    # =========================================================================
    # PHASE 3.1: GENERIC FRAGMENTS
    # =========================================================================
    print("\n" + "="*80)
    print("PHASE 3.1: Generic Fragments of Specific Terms")
    print("="*80)

    removals = []

    # Rule: Remove "niveau" because we have specific versions
    if 'niveau' in edu['term'].values:
        specific_niveau = edu[edu['term'].str.contains('niveau', case=False) & (edu['term'] != 'niveau')]
        if len(specific_niveau) > 0:
            mask = edu['term'] == 'niveau'
            edu.loc[mask, 'action'] = 'REMOVE'
            edu.loc[mask, 'action_reason'] = 'Generic fragment - have specific versions (onderwijsniveau, etc.)'
            removals.append('niveau')
            print(f"\n✓ REMOVE: niveau")
            print(f"  Reason: Generic fragment, have specific versions: {specific_niveau['term'].tolist()[:5]}")

    print(f"\nPhase 3.1 Summary: {len(removals)} terms removed")

    # =========================================================================
    # PHASE 3.2: ULTRA-HIGH FREQUENCY (df > 100)
    # =========================================================================
    print("\n" + "="*80)
    print("PHASE 3.2: Ultra-High Frequency Dampening (df > 100, weight > 0.70)")
    print("="*80)

    mask_ultra_high = (edu['df'] > 100) & (edu['weight'] > 0.70) & (edu['action'] == 'KEEP')
    ultra_high_terms = edu[mask_ultra_high].copy()

    reweight_count = 0
    for idx, row in ultra_high_terms.iterrows():
        old_weight = row['weight']
        # Aggressive dampening for very high frequency
        new_weight = max(0.50, old_weight - 0.25)

        edu.loc[idx, 'action'] = 'REWEIGHT'
        edu.loc[idx, 'weight_new'] = new_weight
        edu.loc[idx, 'action_reason'] = f'Ultra-high df ({row["df"]}) - dominates signal'

        print(f"\n✓ REWEIGHT: {row['term']:30s}")
        print(f"  df={row['df']:3d}, weight: {old_weight:.2f} -> {new_weight:.2f}")
        print(f"  Reason: Appears in {row['df']} documents, overwhelms topic signal")

        reweight_count += 1

    print(f"\nPhase 3.2 Summary: {reweight_count} terms reweighted")

    # =========================================================================
    # PHASE 3.3: HIGH FREQUENCY (df 50-100, weight > 0.75)
    # =========================================================================
    print("\n" + "="*80)
    print("PHASE 3.3: High Frequency Dampening (df 50-100, weight > 0.75)")
    print("="*80)

    mask_high = (
        (edu['df'] >= 50) &
        (edu['df'] <= 100) &
        (edu['weight'] > 0.75) &
        (edu['action'] == 'KEEP')
    )
    high_freq_terms = edu[mask_high].copy()

    for idx, row in high_freq_terms.iterrows():
        old_weight = row['weight']
        new_weight = max(0.60, old_weight - 0.15)

        edu.loc[idx, 'action'] = 'REWEIGHT'
        edu.loc[idx, 'weight_new'] = new_weight
        edu.loc[idx, 'action_reason'] = f'High df ({row["df"]}) - reduce weight'

        print(f"\n✓ REWEIGHT: {row['term']:30s}")
        print(f"  df={row['df']:3d}, weight: {old_weight:.2f} -> {new_weight:.2f}")

        reweight_count += 1

    print(f"\nPhase 3.3 Summary: {len(high_freq_terms)} additional terms reweighted")

    # =========================================================================
    # PHASE 3.4: AMBIGUOUS GENERIC TERMS
    # =========================================================================
    print("\n" + "="*80)
    print("PHASE 3.4: Ambiguous/Generic Institutional Terms")
    print("="*80)

    # Check for overly generic institutional terms
    generic_institutional = ['college', 'organisaties', 'instituten', 'instellingen']

    for term in generic_institutional:
        if term in edu['term'].values:
            mask = (edu['term'] == term) & (edu['action'] == 'KEEP')
            if mask.sum() > 0:
                row = edu[mask].iloc[0]
                old_weight = row['weight']

                # Decision based on df and weight
                if row['df'] > 30 and old_weight > 0.70:
                    new_weight = 0.60  # Lower significantly
                    edu.loc[mask, 'action'] = 'REWEIGHT'
                    edu.loc[mask, 'weight_new'] = new_weight
                    edu.loc[mask, 'action_reason'] = f'Ambiguous generic term (df={row["df"]})'

                    print(f"\n✓ REWEIGHT: {term:30s}")
                    print(f"  df={row['df']:3d}, weight: {old_weight:.2f} -> {new_weight:.2f}")
                    print(f"  Reason: Too generic/ambiguous")

                    reweight_count += 1

    # =========================================================================
    # FINAL SUMMARY
    # =========================================================================
    print("\n" + "="*80)
    print("FILTERING SUMMARY")
    print("="*80)

    removed = edu[edu['action'] == 'REMOVE']
    reweighted = edu[edu['action'] == 'REWEIGHT']
    kept = edu[edu['action'] == 'KEEP']

    print(f"\nOriginal Educational terms: {len(edu)}")
    print(f"  REMOVE: {len(removed)}")
    print(f"  REWEIGHT: {len(reweighted)}")
    print(f"  KEEP unchanged: {len(kept)}")
    print(f"\nFinal Educational terms: {len(edu) - len(removed)}")

    if len(removed) > 0:
        print(f"\nTerms removed:")
        for idx, row in removed.iterrows():
            print(f"  - {row['term']:30s} | {row['action_reason']}")

    if len(reweighted) > 0:
        print(f"\nTerms reweighted ({len(reweighted)} total):")
        for idx, row in reweighted.head(10).iterrows():
            print(f"  - {row['term']:30s} | {row['weight']:.2f} -> {row['weight_new']:.2f} | df={row['df']}")
        if len(reweighted) > 10:
            print(f"  ... and {len(reweighted) - 10} more")

    # =========================================================================
    # CREATE FILTERED DICTIONARY
    # =========================================================================
    print("\n" + "="*80)
    print("CREATING FILTERED DICTIONARY")
    print("="*80)

    # Apply weight changes
    edu_filtered = edu[edu['action'] != 'REMOVE'].copy()
    edu_filtered['weight'] = edu_filtered['weight_new']

    # Drop action columns
    edu_filtered = edu_filtered[['topic', 'term', 'cosine', 'df', 'weight', 'category', 'parent', 'is_seed']]

    # Combine with other topics
    df_final = pd.concat([edu_filtered, other], ignore_index=True)
    df_final = df_final.sort_values(['topic', 'weight', 'term'], ascending=[True, False, True])

    # Save
    df_final.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')

    print(f"\n✓ Saved filtered dictionary: {OUTPUT_FILE.name}")
    print(f"  Total terms: {len(df_final)}")
    print(f"  Educational terms: {len(edu_filtered)}")

    # Weight distribution for Educational
    print(f"\nEducational weight distribution:")
    for weight in [1.00, 0.95, 0.85, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50]:
        count = ((edu_filtered['weight'] >= weight - 0.02) & (edu_filtered['weight'] <= weight + 0.02)).sum()
        if count > 0:
            pct = count / len(edu_filtered) * 100
            print(f"  {weight:.2f}: {count:3d} terms ({pct:5.1f}%)")

    print("\n" + "="*80)
    print("EDUCATIONAL TOPIC FILTERING COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
