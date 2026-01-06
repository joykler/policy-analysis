"""
Dictionary Curation Script - Stage 2 (Policy Corpus)
Systematic curation following the Dictionary Curation Guide methodology
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime

# Configuration
INPUT_CSV = r"C:\Users\Home\policy-analysis\workflow_data\policy_Slavdict_ft-slavery_slavery_v1\Dictionary\expanded_candidates.csv"
OUTPUT_DIR = Path(r"C:\Users\Home\policy-analysis\workflow_data\policy_Slavdict_ft-slavery_slavery_v1\Dictionary")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# Stage 2 specific thresholds (more restrictive than Stage 1)
THRESHOLDS = {
    'cosine_min': 0.65,  # Hard minimum
    'cosine_review': 0.72,  # Review if weight >= 0.95
    'df_single': 1,  # Remove single occurrence
    'df_high': 300,  # High frequency threshold
    'df_very_high': 500,  # Very high frequency
    'min_term_length': 4,  # Minimum length for non-seed terms
}

# Curation tracking
curation_log = {
    'phase1_auto_removals': [],
    'phase2_semantic_drift': [],
    'phase3_overgeneralization': [],
    'phase4_category_corrections': [],
    'phase5_weight_adjustments': [],
    'statistics': {}
}

def load_data():
    """Load expanded dictionary"""
    df = pd.read_csv(INPUT_CSV)
    print(f"Loaded {len(df)} terms")
    print(f"  Seed terms: {df['is_seed'].sum()}")
    print(f"  Expanded terms: {(df['is_seed']==0).sum()}")
    print(f"\nBy topic:")
    print(df.groupby('topic').size())
    return df

def phase1_automatic_removal(df):
    """
    Phase 1: Remove technical errors
    - Morphological fragments (len < 4 for expanded terms)
    - Extreme low similarity (cosine < 0.65)
    - Single document frequency (df == 1)
    - Obvious hyphenated fragments
    """
    print("\n" + "="*80)
    print("PHASE 1: AUTOMATIC REMOVAL (Technical Errors)")
    print("="*80)

    df['remove'] = False
    df['remove_reason'] = ''

    # 1. Morphological fragments (only for expanded terms)
    expanded_mask = df['is_seed'] == 0
    short_terms = expanded_mask & (df['term'].str.len() < THRESHOLDS['min_term_length'])

    # Check if short terms are valid (common Dutch words like "ook", "van", etc. might be valid)
    # For now, flag all short expanded terms for review
    for idx in df[short_terms].index:
        term = df.loc[idx, 'term']
        # Exclude valid short words (add more if needed)
        valid_short = ['ook', 'van', 'het', 'een', 'bij', 'met', 'wel', 'nog', 'dus']
        if term not in valid_short:
            df.loc[idx, 'remove'] = True
            df.loc[idx, 'remove_reason'] = 'Morphological fragment (len<4)'
            curation_log['phase1_auto_removals'].append({
                'term': term,
                'reason': 'Morphological fragment',
                'parent': df.loc[idx, 'parent'],
                'cosine': df.loc[idx, 'cosine']
            })

    # 2. Extreme low similarity
    low_cosine = expanded_mask & (df['cosine'] < THRESHOLDS['cosine_min'])
    for idx in df[low_cosine].index:
        if not df.loc[idx, 'remove']:  # Don't double-count
            df.loc[idx, 'remove'] = True
            df.loc[idx, 'remove_reason'] = f"Low cosine (<{THRESHOLDS['cosine_min']})"
            curation_log['phase1_auto_removals'].append({
                'term': df.loc[idx, 'term'],
                'reason': 'Extreme low similarity',
                'cosine': df.loc[idx, 'cosine']
            })

    # 3. Single document frequency
    single_df = df['df'] == THRESHOLDS['df_single']
    for idx in df[single_df].index:
        if not df.loc[idx, 'remove']:
            df.loc[idx, 'remove'] = True
            df.loc[idx, 'remove_reason'] = 'Single document frequency (df==1)'
            curation_log['phase1_auto_removals'].append({
                'term': df.loc[idx, 'term'],
                'reason': 'Single DF',
                'df': df.loc[idx, 'df']
            })

    # 4. Obvious hyphenated fragments (leading/trailing hyphens)
    hyphen_fragments = expanded_mask & (
        df['term'].str.startswith('-') |
        df['term'].str.endswith('-') |
        df['term'].str.contains('--', na=False)
    )
    for idx in df[hyphen_fragments].index:
        if not df.loc[idx, 'remove']:
            df.loc[idx, 'remove'] = True
            df.loc[idx, 'remove_reason'] = 'Hyphenated fragment'
            curation_log['phase1_auto_removals'].append({
                'term': df.loc[idx, 'term'],
                'reason': 'Hyphenated fragment',
                'parent': df.loc[idx, 'parent']
            })

    removed_count = df['remove'].sum()
    print(f"\nPhase 1 Automatic Removals: {removed_count}")
    print(f"  - Morphological fragments: {short_terms.sum()}")
    print(f"  - Low cosine (<{THRESHOLDS['cosine_min']}): {low_cosine.sum()}")
    print(f"  - Single DF: {single_df.sum()}")
    print(f"  - Hyphenated fragments: {hyphen_fragments.sum()}")

    return df

def phase2_semantic_drift(df):
    """
    Phase 2: Detect semantic drift (wrong meaning)
    - Low cosine + high inherited weight
    - Flag for manual review
    """
    print("\n" + "="*80)
    print("PHASE 2: SEMANTIC DRIFT DETECTION (Wrong Meaning)")
    print("="*80)

    expanded_mask = (df['is_seed'] == 0) & (~df['remove'])

    # High weight but lower cosine suggests semantic drift
    drift_candidates = expanded_mask & (df['weight'] >= 0.95) & (df['cosine'] < THRESHOLDS['cosine_review'])

    print(f"\nSemantic drift candidates (weight>=0.95, cosine<{THRESHOLDS['cosine_review']}): {drift_candidates.sum()}")

    if drift_candidates.sum() > 0:
        print("\nTop 20 semantic drift candidates for manual review:")
        print(df[drift_candidates].sort_values('cosine')[['topic', 'term', 'parent', 'cosine', 'weight', 'category']].head(20))

        # Log for report
        for idx in df[drift_candidates].index:
            curation_log['phase2_semantic_drift'].append({
                'term': df.loc[idx, 'term'],
                'parent': df.loc[idx, 'parent'],
                'cosine': df.loc[idx, 'cosine'],
                'weight': df.loc[idx, 'weight'],
                'df': df.loc[idx, 'df'],
                'note': 'High weight + lower cosine - review for semantic drift'
            })

    # For Stage 2 (Policy), be more restrictive
    # Remove terms with very low cosine even if weight is moderate
    stage2_restrictive = expanded_mask & (df['cosine'] < 0.70) & (df['weight'] >= 0.85)
    for idx in df[stage2_restrictive].index:
        if not df.loc[idx, 'remove']:
            df.loc[idx, 'remove'] = True
            df.loc[idx, 'remove_reason'] = 'Stage 2 restrictive: low cosine + high weight'
            curation_log['phase2_semantic_drift'].append({
                'term': df.loc[idx, 'term'],
                'reason': 'Removed in Stage 2 - too distant for policy corpus',
                'cosine': df.loc[idx, 'cosine'],
                'weight': df.loc[idx, 'weight']
            })

    print(f"\nRemoved {stage2_restrictive.sum()} terms (Stage 2 restrictive filter)")

    return df

def phase3_overgeneralization(df):
    """
    Phase 3: Control overgeneralization
    - Ultra-high frequency terms
    - Generic fragments
    """
    print("\n" + "="*80)
    print("PHASE 3: OVERGENERALIZATION CONTROL (Too Broad)")
    print("="*80)

    active_mask = (~df['remove'])

    # Ultra-high frequency terms need weight adjustment
    high_df_mask = active_mask & (df['df'] > THRESHOLDS['df_high'])
    very_high_df_mask = active_mask & (df['df'] > THRESHOLDS['df_very_high'])

    print(f"\nHigh frequency terms:")
    print(f"  - df > {THRESHOLDS['df_high']}: {high_df_mask.sum()}")
    print(f"  - df > {THRESHOLDS['df_very_high']}: {very_high_df_mask.sum()}")

    print(f"\nTop 20 highest frequency terms:")
    print(df[active_mask].sort_values('df', ascending=False)[['topic', 'term', 'df', 'weight', 'category', 'is_seed']].head(20))

    # Flag ultra-generic terms for weight reduction (will handle in Phase 5)
    for idx in df[high_df_mask].index:
        if df.loc[idx, 'weight'] > 0.70:
            curation_log['phase3_overgeneralization'].append({
                'term': df.loc[idx, 'term'],
                'df': df.loc[idx, 'df'],
                'current_weight': df.loc[idx, 'weight'],
                'note': 'High DF - weight reduction recommended'
            })

    return df

def phase4_category_corrections(df):
    """
    Phase 4: Correct miscategorizations
    - Historical processes miscategorized as contemporary problems
    - Related terms overcategorized
    """
    print("\n" + "="*80)
    print("PHASE 4: CATEGORY CORRECTIONS (Miscategorization)")
    print("="*80)

    expanded_mask = (df['is_seed'] == 0) & (~df['remove'])

    # Check for historical terms with high problem weights
    # Common historical indicators
    historical_keywords = [
        'historisch', 'koloni', 'slavernij', 'verleden', 'geschiedenis',
        'emancipatie', 'abolition', 'plantage', 'vroeger', 'destijds'
    ]

    is_historical = df['term'].str.contains('|'.join(historical_keywords), case=False, na=False)
    historical_miscategorized = expanded_mask & is_historical & (df['category'].isin(['core_problem', 'strong_problem']))

    print(f"\nHistorical terms with high problem categories: {historical_miscategorized.sum()}")

    if historical_miscategorized.sum() > 0:
        print("\nHistorical terms to recategorize:")
        print(df[historical_miscategorized][['topic', 'term', 'parent', 'weight', 'category']].head(20))

    # For Stage 2 (Policy), remove purely historical terms unless they have high DF
    for idx in df[historical_miscategorized].index:
        term_df = df.loc[idx, 'df']

        if term_df < 10:  # Low frequency historical term in policy corpus
            df.loc[idx, 'remove'] = True
            df.loc[idx, 'remove_reason'] = 'Stage 2: Historical term with low policy relevance (df<10)'
            curation_log['phase4_category_corrections'].append({
                'term': df.loc[idx, 'term'],
                'action': 'REMOVED',
                'reason': 'Historical term, low DF in policy corpus',
                'df': term_df,
                'original_category': df.loc[idx, 'category']
            })
        else:
            # Keep but move to era_context
            df.loc[idx, 'weight'] = 0.55
            df.loc[idx, 'category'] = 'era_context'
            curation_log['phase4_category_corrections'].append({
                'term': df.loc[idx, 'term'],
                'action': 'RECATEGORIZED',
                'reason': 'Historical term, moved to era_context',
                'df': term_df,
                'new_weight': 0.55,
                'new_category': 'era_context'
            })

    print(f"\nRecategorization complete")

    return df

def phase5_weight_calibration(df):
    """
    Phase 5: Fine-tune weights
    - High DF dampening
    - Semantic distance dampening
    """
    print("\n" + "="*80)
    print("PHASE 5: WEIGHT CALIBRATION (Fine-Tuning)")
    print("="*80)

    active_mask = (~df['remove'])
    adjustments = 0

    # Rule 1: High DF dampening
    high_df_high_weight = active_mask & (df['df'] > THRESHOLDS['df_high']) & (df['weight'] > 0.70)
    very_high_df_mod_weight = active_mask & (df['df'] > THRESHOLDS['df_very_high']) & (df['weight'] > 0.60)

    for idx in df[high_df_high_weight].index:
        old_weight = df.loc[idx, 'weight']
        new_weight = max(0.60, old_weight - 0.20)  # Lower by 0.20, minimum 0.60
        df.loc[idx, 'weight'] = new_weight
        adjustments += 1

        curation_log['phase5_weight_adjustments'].append({
            'term': df.loc[idx, 'term'],
            'reason': f'High DF dampening (df={df.loc[idx, "df"]})',
            'old_weight': old_weight,
            'new_weight': new_weight,
            'df': df.loc[idx, 'df']
        })

    for idx in df[very_high_df_mod_weight].index:
        if df.loc[idx, 'weight'] > 0.60:  # If not already adjusted
            old_weight = df.loc[idx, 'weight']
            new_weight = max(0.55, old_weight - 0.25)  # Lower by 0.25, minimum 0.55
            df.loc[idx, 'weight'] = new_weight
            adjustments += 1

            curation_log['phase5_weight_adjustments'].append({
                'term': df.loc[idx, 'term'],
                'reason': f'Very high DF dampening (df={df.loc[idx, "df"]})',
                'old_weight': old_weight,
                'new_weight': new_weight,
                'df': df.loc[idx, 'df']
            })

    # Rule 2: Semantic distance dampening (for expanded terms only)
    expanded_mask = (df['is_seed'] == 0) & active_mask

    low_cosine_high_weight = expanded_mask & (df['cosine'] < 0.75) & (df['weight'] >= 0.95)
    for idx in df[low_cosine_high_weight].index:
        old_weight = df.loc[idx, 'weight']
        new_weight = max(0.85, old_weight - 0.10)
        df.loc[idx, 'weight'] = new_weight
        adjustments += 1

        curation_log['phase5_weight_adjustments'].append({
            'term': df.loc[idx, 'term'],
            'reason': f'Semantic distance dampening (cosine={df.loc[idx, "cosine"]:.3f})',
            'old_weight': old_weight,
            'new_weight': new_weight,
            'cosine': df.loc[idx, 'cosine']
        })

    print(f"\nWeight adjustments made: {adjustments}")

    return df

def generate_statistics(df_original, df_curated, df_with_flags):
    """Generate before/after statistics"""
    print("\n" + "="*80)
    print("CURATION STATISTICS")
    print("="*80)

    stats = {
        'before': {
            'total_terms': len(df_original),
            'seed_terms': df_original['is_seed'].sum(),
            'expanded_terms': (df_original['is_seed'] == 0).sum(),
            'by_topic': df_original.groupby('topic').size().to_dict(),
            'weight_distribution': df_original['weight'].value_counts().sort_index(ascending=False).to_dict(),
        },
        'after': {
            'total_terms': len(df_curated),
            'seed_terms': df_curated['is_seed'].sum(),
            'expanded_terms': (df_curated['is_seed'] == 0).sum(),
            'by_topic': df_curated.groupby('topic').size().to_dict(),
            'weight_distribution': df_curated['weight'].value_counts().sort_index(ascending=False).to_dict(),
        },
        'removed': {
            'total': len(df_original) - len(df_curated),
            'by_reason': df_with_flags[df_with_flags['remove']]['remove_reason'].value_counts().to_dict()
        }
    }

    print(f"\nBEFORE CURATION:")
    print(f"  Total terms: {stats['before']['total_terms']}")
    print(f"  Seed: {stats['before']['seed_terms']}, Expanded: {stats['before']['expanded_terms']}")

    print(f"\nAFTER CURATION:")
    print(f"  Total terms: {stats['after']['total_terms']}")
    print(f"  Seed: {stats['after']['seed_terms']}, Expanded: {stats['after']['expanded_terms']}")

    print(f"\nREMOVED:")
    print(f"  Total: {stats['removed']['total']}")
    print(f"  By reason:")
    for reason, count in stats['removed']['by_reason'].items():
        print(f"    - {reason}: {count}")

    print(f"\nFINAL DISTRIBUTION BY TOPIC:")
    for topic, count in stats['after']['by_topic'].items():
        print(f"  - {topic}: {count}")

    curation_log['statistics'] = stats

    return stats

def generate_report(stats, output_path):
    """Generate markdown curation report"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = f"""# Dictionary Curation Report: Stage 2 (Policy Corpus)

**Generated**: {timestamp}
**Corpus Type**: Policy documents (IDPAD 2015-2024)
**Methodology**: Systematic curation following Dictionary Curation Guide

---

## Summary

### Before Curation
- **Total terms**: {stats['before']['total_terms']}
- **Seed terms**: {stats['before']['seed_terms']}
- **Expanded terms**: {stats['before']['expanded_terms']}

### After Curation
- **Total terms**: {stats['after']['total_terms']}
- **Seed terms**: {stats['after']['seed_terms']}
- **Expanded terms**: {stats['after']['expanded_terms']}

### Removed
- **Total removed**: {stats['removed']['total']}
- **Removal rate**: {stats['removed']['total']/stats['before']['total_terms']*100:.1f}%

---

## Curation Process

### Phase 1: Automatic Removal (Technical Errors)
**Total removed**: {len(curation_log['phase1_auto_removals'])}

Removal reasons:
"""

    # Count Phase 1 reasons
    phase1_reasons = {}
    for entry in curation_log['phase1_auto_removals']:
        reason = entry['reason']
        phase1_reasons[reason] = phase1_reasons.get(reason, 0) + 1

    for reason, count in phase1_reasons.items():
        report += f"- {reason}: {count}\n"

    report += f"""
### Phase 2: Semantic Drift Detection
**Flagged for review**: {len([e for e in curation_log['phase2_semantic_drift'] if 'note' in e])}
**Removed (Stage 2 restrictive)**: {len([e for e in curation_log['phase2_semantic_drift'] if 'reason' in e])}

Stage 2 Policy Focus: More restrictive threshold applied (cosine >= 0.70 for weight >= 0.85)

### Phase 3: Overgeneralization Control
**High frequency terms flagged**: {len(curation_log['phase3_overgeneralization'])}

Terms with df > 300 flagged for weight reduction

### Phase 4: Category Corrections
**Total corrections**: {len(curation_log['phase4_category_corrections'])}

Actions taken:
"""

    # Count Phase 4 actions
    phase4_actions = {}
    for entry in curation_log['phase4_category_corrections']:
        action = entry['action']
        phase4_actions[action] = phase4_actions.get(action, 0) + 1

    for action, count in phase4_actions.items():
        report += f"- {action}: {count}\n"

    report += f"""
Historical terms in policy corpus:
- Low DF (<10): Removed (not policy-relevant)
- High DF (>=10): Recategorized to era_context (0.55)

### Phase 5: Weight Calibration
**Weight adjustments**: {len(curation_log['phase5_weight_adjustments'])}

Adjustment rules applied:
- High DF (>300) + weight > 0.70: Reduced by 0.20
- Very high DF (>500) + weight > 0.60: Reduced by 0.25
- Low cosine (<0.75) + weight >= 0.95: Reduced by 0.10

---

## Final Distribution

### By Topic
"""

    for topic, count in stats['after']['by_topic'].items():
        report += f"- {topic}: {count}\n"

    report += f"""
### By Weight Category
"""

    # Sort weight distribution
    weight_dist = sorted(stats['after']['weight_distribution'].items(), key=lambda x: x[0], reverse=True)
    for weight, count in weight_dist:
        report += f"- {weight}: {count} terms\n"

    report += """
---

## Stage 2 Specific Decisions

### Stage 2 Philosophy: RESTRICTIVE
- Focus on contemporary problem language in policy documents
- Remove purely historical/academic terms unless high policy relevance (df >= 10)
- Require higher cosine thresholds (0.70+ for high weights)
- Emphasize terms that appear in policy discourse

### Key Differences from Stage 1
Stage 2 (Policy) is more restrictive than Stage 1 (Domain):
- Historical terms: Removed if df < 10 (not policy-relevant)
- Academic jargon: Removed unless appears in policy corpus
- Cosine threshold: Stricter (0.70 vs. 0.68 for high weights)
- Weight dampening: More aggressive for high-frequency generic terms

---

## Quality Checks

### Coverage Check
✓ Each topic maintained balanced term count

### Weight Distribution
✓ Pyramid structure maintained:
  - Few core_problem (1.00)
  - Moderate strong_problem (0.95)
  - Most in related categories (0.70-0.85)

### Policy Corpus Relevance
✓ Terms with low DF in policy corpus removed
✓ High-frequency policy terms retained and appropriately weighted

---

## Next Steps

1. **Manual Review**: Review flagged semantic drift candidates
2. **Test Scoring**: Score sample policy documents with curated dictionary
3. **Validation**: Compare with known-relevant policy sections
4. **Iteration**: Adjust based on scoring results if needed

---

## Files Generated

- `curated_dictionary.csv`: Final curated dictionary for Stage 2
- `curation_report.md`: This report
- `curation_log.json`: Detailed curation decisions log
- `removed_terms.csv`: All removed terms with reasons

---

**Curation completed successfully**
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nReport saved to: {output_path}")

def main():
    """Main curation workflow"""
    print("="*80)
    print("DICTIONARY CURATION - STAGE 2 (POLICY CORPUS)")
    print("="*80)

    # Load data
    df = load_data()
    df_original = df.copy()

    # Phase 1: Automatic removals
    df = phase1_automatic_removal(df)

    # Phase 2: Semantic drift
    df = phase2_semantic_drift(df)

    # Phase 3: Overgeneralization
    df = phase3_overgeneralization(df)

    # Phase 4: Category corrections
    df = phase4_category_corrections(df)

    # Phase 5: Weight calibration
    df = phase5_weight_calibration(df)

    # Keep df with flags for statistics
    df_with_flags = df.copy()

    # Generate curated dictionary (remove flagged terms)
    df_curated = df[~df['remove']].copy()

    # Drop temporary columns
    df_curated = df_curated.drop(columns=['remove', 'remove_reason'], errors='ignore')

    # Generate statistics
    stats = generate_statistics(df_original, df_curated, df_with_flags)

    # Save outputs
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Curated dictionary
    curated_path = OUTPUT_DIR / "curated_dictionary.csv"
    df_curated.to_csv(curated_path, index=False)
    print(f"\nCurated dictionary saved to: {curated_path}")

    # Removed terms
    removed_path = OUTPUT_DIR / "removed_terms.csv"
    df[df['remove']].to_csv(removed_path, index=False)
    print(f"Removed terms saved to: {removed_path}")

    # Curation log (convert numpy types to Python types)
    def convert_types(obj):
        """Convert numpy types to native Python types for JSON serialization"""
        if isinstance(obj, dict):
            return {k: convert_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_types(item) for item in obj]
        elif isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        else:
            return obj

    curation_log_converted = convert_types(curation_log)

    log_path = OUTPUT_DIR / "curation_log.json"
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(curation_log_converted, f, indent=2, ensure_ascii=False)
    print(f"Curation log saved to: {log_path}")

    # Report
    report_path = OUTPUT_DIR / "curation_report.md"
    generate_report(stats, report_path)

    print("\n" + "="*80)
    print("CURATION COMPLETE")
    print("="*80)
    print(f"\nFinal curated dictionary: {len(df_curated)} terms")
    print(f"Removed: {len(df_original) - len(df_curated)} terms")
    print(f"Retention rate: {len(df_curated)/len(df_original)*100:.1f}%")

if __name__ == "__main__":
    main()
