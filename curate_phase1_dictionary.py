"""
Dictionary Curation Script for Phase 1 (Domain Corpus - Semantic Foundation)
Following the systematic 5-phase methodology from A__DICTIONARY_CURATION_GUIDE.md
"""

import sys
import io
# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pandas as pd
import numpy as np
import re
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

INPUT_FILE = r"C:\Users\Home\policy-analysis\workflow_data\slavery_Slavdict_pretrained_slavery_v2\Dictionary\expanded_candidates.csv"
OUTPUT_DIR = Path(r"C:\Users\Home\policy-analysis\workflow_data\slavery_Slavdict_pretrained_slavery_v2\Dictionary")
STAGE = "Stage 1: Domain Corpus (Semantic Foundation)"

# Phase 1: Automatic removal thresholds
MIN_COSINE_THRESHOLD = 0.65  # Stage 1 is more permissive
MIN_TERM_LENGTH = 4  # For fragment detection
MIN_DF_THRESHOLD = 1  # Remove single occurrence (df == 1)

# Phase 3: Overgeneralization thresholds
HIGH_DF_THRESHOLD = 300  # Ultra-high frequency
VERY_HIGH_DF_THRESHOLD = 500

# Phase 2 & 4: Manual review thresholds
LOW_COSINE_HIGH_WEIGHT = 0.72  # Red flag threshold
STRONG_PROBLEM_WEIGHT = 0.95
CORE_PROBLEM_WEIGHT = 1.00

# Common Dutch morphological fragments to watch for
COMMON_FRAGMENTS = ['lingen', 'denten', 'heid', 'ties', 'sten', 'eren', 'ingen']

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def is_morphological_fragment(term):
    """Check if term is likely a morphological fragment"""
    if len(term) < MIN_TERM_LENGTH:
        return True

    # Check if it's just a common suffix
    if term in COMMON_FRAGMENTS:
        return True

    # Check if it ends with common fragment and is short
    for fragment in COMMON_FRAGMENTS:
        if term.endswith(fragment) and len(term) < 6:
            return True

    return False

def is_encoding_error(term):
    """Detect obvious encoding errors"""
    # Contains unusual Unicode characters
    if re.search(r'[\u200b-\u200f\ufeff]', term):  # Zero-width characters
        return True

    # Contains mixed scripts inappropriately
    if re.search(r'[а-яА-Я]', term) and not all(ord(c) >= 1024 for c in term if c.isalpha()):
        return True  # Cyrillic mixed with Latin

    # Broken accents or diacritics
    if '​' in term or '\u200b' in term:
        return True

    return False

def categorize_removal_reason(row, reason_code):
    """Map reason codes to human-readable explanations"""
    reasons = {
        'P1_FRAGMENT': f"Morphological fragment (len={len(row['term'])})",
        'P1_LOW_COSINE': f"Cosine too low ({row['cosine']:.3f} < {MIN_COSINE_THRESHOLD})",
        'P1_SINGLE_DF': f"Single document occurrence (df={row['df']})",
        'P1_ENCODING': "Encoding/OCR error detected",
        'P2_SEMANTIC_DRIFT': f"Semantic drift (cosine={row['cosine']:.3f}, weight={row['weight']})",
        'P3_GENERIC_FRAGMENT': "Generic fragment of specific term",
        'P3_ULTRA_HIGH_DF': f"Ultra-high document frequency (df={row['df']})",
        'P3_TOO_BROAD': "Overly broad/generic term",
        'MANUAL_REVIEW': "Flagged for manual review"
    }
    return reasons.get(reason_code, reason_code)

# ============================================================================
# PHASE 1: AUTOMATIC REMOVAL
# ============================================================================

def phase1_automatic_removal(df):
    """Phase 1: Remove technical errors automatically"""
    print("\n" + "="*80)
    print("PHASE 1: AUTOMATIC REMOVAL (Technical Errors)")
    print("="*80)

    df['decision'] = 'KEEP'
    df['reason'] = ''
    df['phase'] = ''

    initial_count = len(df)

    # 1. Morphological fragments
    mask_fragment = df['term'].apply(is_morphological_fragment) & (df['is_seed'] == 0)
    df.loc[mask_fragment, 'decision'] = 'REMOVE'
    df.loc[mask_fragment, 'reason'] = 'P1_FRAGMENT'
    df.loc[mask_fragment, 'phase'] = 'Phase 1'
    print(f"  ✓ Morphological fragments: {mask_fragment.sum()} terms flagged")

    # 2. Extreme low similarity
    mask_low_cosine = (df['cosine'] < MIN_COSINE_THRESHOLD) & (df['is_seed'] == 0)
    df.loc[mask_low_cosine & (df['decision'] == 'KEEP'), 'decision'] = 'REMOVE'
    df.loc[mask_low_cosine & (df['reason'] == ''), 'reason'] = 'P1_LOW_COSINE'
    df.loc[mask_low_cosine & (df['phase'] == ''), 'phase'] = 'Phase 1'
    print(f"  ✓ Low cosine (<{MIN_COSINE_THRESHOLD}): {mask_low_cosine.sum()} terms flagged")

    # 3. Single document frequency
    mask_single_df = (df['df'] == MIN_DF_THRESHOLD) & (df['is_seed'] == 0)
    df.loc[mask_single_df & (df['decision'] == 'KEEP'), 'decision'] = 'REMOVE'
    df.loc[mask_single_df & (df['reason'] == ''), 'reason'] = 'P1_SINGLE_DF'
    df.loc[mask_single_df & (df['phase'] == ''), 'phase'] = 'Phase 1'
    print(f"  ✓ Single document frequency (df=1): {mask_single_df.sum()} terms flagged")

    # 4. Encoding errors
    mask_encoding = df['term'].apply(is_encoding_error) & (df['is_seed'] == 0)
    df.loc[mask_encoding & (df['decision'] == 'KEEP'), 'decision'] = 'REMOVE'
    df.loc[mask_encoding & (df['reason'] == ''), 'reason'] = 'P1_ENCODING'
    df.loc[mask_encoding & (df['phase'] == ''), 'phase'] = 'Phase 1'
    print(f"  ✓ Encoding errors: {mask_encoding.sum()} terms flagged")

    removed_p1 = (df['decision'] == 'REMOVE').sum()
    print(f"\n  📊 Phase 1 Total: {removed_p1} terms marked for removal")
    print(f"  📊 Remaining: {initial_count - removed_p1} terms")

    return df

# ============================================================================
# PHASE 2: SEMANTIC DRIFT DETECTION
# ============================================================================

def phase2_semantic_drift(df):
    """Phase 2: Detect terms with wrong meaning"""
    print("\n" + "="*80)
    print("PHASE 2: SEMANTIC DRIFT DETECTION")
    print("="*80)

    # Low cosine + High weight = RED FLAG
    mask_drift = (
        (df['cosine'] < LOW_COSINE_HIGH_WEIGHT) &
        (df['weight'] >= STRONG_PROBLEM_WEIGHT) &
        (df['is_seed'] == 0) &
        (df['decision'] == 'KEEP')
    )

    df.loc[mask_drift, 'decision'] = 'MANUAL_REVIEW'
    df.loc[mask_drift, 'reason'] = 'P2_SEMANTIC_DRIFT'
    df.loc[mask_drift, 'phase'] = 'Phase 2'

    print(f"  ⚠️  Low cosine + high weight: {mask_drift.sum()} terms flagged for manual review")
    print(f"      (cosine < {LOW_COSINE_HIGH_WEIGHT} AND weight >= {STRONG_PROBLEM_WEIGHT})")

    # Show examples
    if mask_drift.sum() > 0:
        examples = df[mask_drift][['topic', 'term', 'parent', 'cosine', 'weight', 'category']].head(10)
        print("\n  [!] Examples requiring manual review:")
        for idx, row in examples.iterrows():
            print(f"      - '{row['term']}' (parent: '{row['parent']}', cosine: {row['cosine']:.3f}, weight: {row['weight']:.2f})")

    return df

# ============================================================================
# PHASE 3: OVERGENERALIZATION CONTROL
# ============================================================================

def phase3_overgeneralization(df):
    """Phase 3: Control for overly broad/generic terms"""
    print("\n" + "="*80)
    print("PHASE 3: OVERGENERALIZATION CONTROL")
    print("="*80)

    # 1. Ultra-high frequency with high weight
    mask_high_df = (
        (df['df'] > HIGH_DF_THRESHOLD) &
        (df['weight'] > 0.70) &
        (df['is_seed'] == 0) &
        (df['decision'] == 'KEEP')
    )

    df.loc[mask_high_df, 'decision'] = 'REWEIGHT'
    df.loc[mask_high_df, 'reason'] = 'P3_ULTRA_HIGH_DF'
    df.loc[mask_high_df, 'phase'] = 'Phase 3'

    # Calculate weight adjustment
    df.loc[mask_high_df, 'weight_adjustment'] = -0.20  # Lower by 0.20

    print(f"  ⚠️  Ultra-high frequency (df > {HIGH_DF_THRESHOLD}): {mask_high_df.sum()} terms flagged for reweighting")

    # Show examples
    if mask_high_df.sum() > 0:
        examples = df[mask_high_df][['term', 'df', 'weight', 'category']].head(10)
        print("\n  [!] Examples flagged for weight reduction:")
        for idx, row in examples.iterrows():
            new_weight = max(0.50, row['weight'] - 0.20)
            print(f"      - '{row['term']}' (df: {row['df']}, weight: {row['weight']:.2f} -> {new_weight:.2f})")

    # 2. Very high frequency - more aggressive
    mask_very_high_df = (
        (df['df'] > VERY_HIGH_DF_THRESHOLD) &
        (df['weight'] > 0.60) &
        (df['is_seed'] == 0) &
        (df['decision'] == 'KEEP')
    )

    df.loc[mask_very_high_df, 'decision'] = 'REWEIGHT'
    df.loc[mask_very_high_df, 'reason'] = 'P3_ULTRA_HIGH_DF'
    df.loc[mask_very_high_df, 'phase'] = 'Phase 3'
    df.loc[mask_very_high_df, 'weight_adjustment'] = -0.25  # Lower by 0.25

    print(f"  ⚠️  Very high frequency (df > {VERY_HIGH_DF_THRESHOLD}): {mask_very_high_df.sum()} additional terms")

    return df

# ============================================================================
# PHASE 4: CATEGORY CORRECTIONS
# ============================================================================

def phase4_category_corrections(df):
    """Phase 4: Flag terms that may be miscategorized"""
    print("\n" + "="*80)
    print("PHASE 4: CATEGORY CORRECTIONS")
    print("="*80)

    # Historical terms with contemporary problem categories
    # This requires domain knowledge, so we'll flag for manual review

    # Look for historical markers in terms with high weights
    historical_markers = [
        'historie', 'historisch', 'geschiedenis', 'koloniaal', 'koloniale',
        'slavernij', 'eeuw', 'periode', 'verleden', 'vroeger',
        'emancipatie', 'abolition', 'plantage', 'vroegere'
    ]

    pattern = '|'.join(historical_markers)
    mask_historical = (
        df['term'].str.contains(pattern, case=False, na=False) &
        (df['weight'] >= STRONG_PROBLEM_WEIGHT) &
        (df['category'].isin(['core_problem', 'strong_problem'])) &
        (df['is_seed'] == 0) &
        (df['decision'] == 'KEEP')
    )

    df.loc[mask_historical, 'decision'] = 'RECATEGORIZE'
    df.loc[mask_historical, 'reason'] = 'P4_HISTORICAL_TERM'
    df.loc[mask_historical, 'phase'] = 'Phase 4'
    df.loc[mask_historical, 'suggested_category'] = 'era_context'
    df.loc[mask_historical, 'suggested_weight'] = 0.55

    print(f"  ⚠️  Historical terms in contemporary categories: {mask_historical.sum()} terms flagged")

    if mask_historical.sum() > 0:
        examples = df[mask_historical][['term', 'parent', 'weight', 'category']].head(10)
        print("\n  [!] Examples suggested for era_context (0.55):")
        for idx, row in examples.iterrows():
            print(f"      - '{row['term']}' (current weight: {row['weight']:.2f})")

    return df

# ============================================================================
# PHASE 5: WEIGHT CALIBRATION
# ============================================================================

def phase5_weight_calibration(df):
    """Phase 5: Fine-tune weights based on characteristics"""
    print("\n" + "="*80)
    print("PHASE 5: WEIGHT CALIBRATION")
    print("="*80)

    # Initialize weight_adjustment if not exists
    if 'weight_adjustment' not in df.columns:
        df['weight_adjustment'] = 0.0

    # Semantic distance dampening for strong terms
    mask_distance = (
        (df['cosine'] < 0.75) &
        (df['weight'] >= STRONG_PROBLEM_WEIGHT) &
        (df['is_seed'] == 0) &
        (df['decision'] == 'KEEP')
    )

    df.loc[mask_distance, 'decision'] = 'REWEIGHT'
    df.loc[mask_distance & (df['reason'] == ''), 'reason'] = 'P5_SEMANTIC_DISTANCE'
    df.loc[mask_distance & (df['phase'] == ''), 'phase'] = 'Phase 5'
    df.loc[mask_distance, 'weight_adjustment'] = -0.10

    print(f"  ⚠️  Semantic distance dampening: {mask_distance.sum()} terms")
    print(f"      (cosine < 0.75 AND weight >= {STRONG_PROBLEM_WEIGHT})")

    return df

# ============================================================================
# GENERATE STATISTICS AND REPORTS
# ============================================================================

def generate_statistics(df_original, df_curated):
    """Generate comprehensive curation statistics"""
    print("\n" + "="*80)
    print("CURATION STATISTICS SUMMARY")
    print("="*80)

    # Overall counts
    total_original = len(df_original)
    kept = (df_curated['decision'] == 'KEEP').sum()
    removed = (df_curated['decision'] == 'REMOVE').sum()
    reweight = (df_curated['decision'] == 'REWEIGHT').sum()
    recategorize = (df_curated['decision'] == 'RECATEGORIZE').sum()
    manual_review = (df_curated['decision'] == 'MANUAL_REVIEW').sum()

    print(f"\nOVERALL SUMMARY:")
    print(f"  - Original terms: {total_original}")
    print(f"  - Seed terms: {(df_original['is_seed'] == 1).sum()}")
    print(f"  - Expanded terms: {(df_original['is_seed'] == 0).sum()}")
    print(f"\nDECISION BREAKDOWN:")
    print(f"  - KEEP as-is: {kept} ({kept/total_original*100:.1f}%)")
    print(f"  - REMOVE: {removed} ({removed/total_original*100:.1f}%)")
    print(f"  - REWEIGHT: {reweight} ({reweight/total_original*100:.1f}%)")
    print(f"  - RECATEGORIZE: {recategorize} ({recategorize/total_original*100:.1f}%)")
    print(f"  - MANUAL_REVIEW needed: {manual_review} ({manual_review/total_original*100:.1f}%)")

    # By phase
    print(f"\nREMOVALS BY PHASE:")
    for phase in ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4', 'Phase 5']:
        count = ((df_curated['phase'] == phase) & (df_curated['decision'] == 'REMOVE')).sum()
        if count > 0:
            print(f"  - {phase}: {count} terms")

    # By reason
    print(f"\nREMOVAL REASONS:")
    reason_counts = df_curated[df_curated['decision'] == 'REMOVE']['reason'].value_counts()
    for reason, count in reason_counts.items():
        readable_reason = categorize_removal_reason(df_curated[df_curated['reason'] == reason].iloc[0], reason)
        print(f"  - {readable_reason}: {count}")

    # By topic
    print(f"\nBY TOPIC:")
    for topic in df_curated['topic'].unique():
        topic_df = df_curated[df_curated['topic'] == topic]
        kept_topic = (topic_df['decision'] == 'KEEP').sum()
        removed_topic = (topic_df['decision'] == 'REMOVE').sum()
        print(f"\n  {topic}:")
        print(f"    - Original: {len(topic_df)}")
        print(f"    - Keep: {kept_topic}")
        print(f"    - Remove: {removed_topic}")
        print(f"    - Other actions: {len(topic_df) - kept_topic - removed_topic}")

    # Weight distribution
    print(f"\nWEIGHT DISTRIBUTION (after adjustments):")
    df_final = df_curated[df_curated['decision'].isin(['KEEP', 'REWEIGHT', 'RECATEGORIZE'])].copy()
    if 'weight_adjustment' in df_final.columns:
        df_final['final_weight'] = df_final['weight'] + df_final['weight_adjustment'].fillna(0)
    else:
        df_final['final_weight'] = df_final['weight']

    for weight_tier in [1.00, 0.95, 0.85, 0.75, 0.70, 0.65, 0.55, 0.50]:
        count = (df_final['final_weight'] >= weight_tier - 0.02).sum() if weight_tier == 0.50 else \
                ((df_final['final_weight'] >= weight_tier - 0.02) & (df_final['final_weight'] < weight_tier + 0.03)).sum()
        print(f"  - Weight {weight_tier:.2f}: {count} terms")

def generate_review_files(df, output_dir):
    """Generate files for manual review"""
    print("\n" + "="*80)
    print("GENERATING REVIEW FILES")
    print("="*80)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Full curated file with decisions
    output_file = output_dir / "expanded_candidates_WITH_CURATION_DECISIONS.csv"
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"  ✓ Full file with decisions: {output_file.name}")

    # 2. Terms requiring manual review
    manual_review = df[df['decision'] == 'MANUAL_REVIEW']
    if len(manual_review) > 0:
        review_file = output_dir / "MANUAL_REVIEW_REQUIRED.csv"
        manual_review.to_csv(review_file, index=False, encoding='utf-8-sig')
        print(f"  ✓ Manual review needed: {review_file.name} ({len(manual_review)} terms)")

    # 3. High-priority manual review (sorted)
    high_priority = df[
        (df['decision'] == 'MANUAL_REVIEW') |
        ((df['weight'] >= 0.95) & (df['is_seed'] == 0) & (df['decision'] != 'REMOVE'))
    ].sort_values(['weight', 'cosine'], ascending=[False, True])

    if len(high_priority) > 0:
        priority_file = output_dir / "HIGH_PRIORITY_REVIEW.csv"
        high_priority.to_csv(priority_file, index=False, encoding='utf-8-sig')
        print(f"  ✓ High-priority review: {priority_file.name} ({len(high_priority)} terms)")

    # 4. Terms to remove
    to_remove = df[df['decision'] == 'REMOVE']
    remove_file = output_dir / "TERMS_TO_REMOVE.csv"
    to_remove.to_csv(remove_file, index=False, encoding='utf-8-sig')
    print(f"  ✓ Terms to remove: {remove_file.name} ({len(to_remove)} terms)")

    # 5. Final curated dictionary (applying decisions)
    final_df = df[df['decision'].isin(['KEEP', 'REWEIGHT', 'RECATEGORIZE'])].copy()

    # Apply weight adjustments
    if 'weight_adjustment' in final_df.columns:
        final_df['weight'] = final_df['weight'] + final_df['weight_adjustment'].fillna(0)

    # Apply category changes
    if 'suggested_category' in final_df.columns:
        mask_recategorize = final_df['decision'] == 'RECATEGORIZE'
        final_df.loc[mask_recategorize, 'category'] = final_df.loc[mask_recategorize, 'suggested_category']

    if 'suggested_weight' in final_df.columns:
        mask_recategorize = final_df['decision'] == 'RECATEGORIZE'
        final_df.loc[mask_recategorize, 'weight'] = final_df.loc[mask_recategorize, 'suggested_weight']

    # Clean up and keep only essential columns
    final_columns = ['topic', 'term', 'cosine', 'df', 'weight', 'category', 'parent', 'is_seed']
    final_df = final_df[final_columns]

    curated_file = output_dir / "curated_dictionary_PHASE1_AUTO.csv"
    final_df.to_csv(curated_file, index=False, encoding='utf-8-sig')
    print(f"  ✓ Curated dictionary: {curated_file.name} ({len(final_df)} terms)")

    return final_df

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("="*80)
    print("DICTIONARY CURATION - PHASE 1 (DOMAIN CORPUS)")
    print("Following A__DICTIONARY_CURATION_GUIDE.md Methodology")
    print("="*80)

    # Load data
    print(f"\n[*] Loading: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)
    print(f"    Loaded {len(df)} terms across {df['topic'].nunique()} topics")

    df_original = df.copy()

    # Execute 5-phase curation
    df = phase1_automatic_removal(df)
    df = phase2_semantic_drift(df)
    df = phase3_overgeneralization(df)
    df = phase4_category_corrections(df)
    df = phase5_weight_calibration(df)

    # Generate statistics
    generate_statistics(df_original, df)

    # Generate review files
    final_df = generate_review_files(df, OUTPUT_DIR)

    print("\n" + "="*80)
    print("[OK] CURATION COMPLETE")
    print("="*80)
    print(f"\nNext steps:")
    print(f"  1. Review: HIGH_PRIORITY_REVIEW.csv")
    print(f"  2. Review: MANUAL_REVIEW_REQUIRED.csv")
    print(f"  3. Validate: TERMS_TO_REMOVE.csv")
    print(f"  4. After manual review, use curated_dictionary_PHASE1_AUTO.csv")
    print(f"\nAll files saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
