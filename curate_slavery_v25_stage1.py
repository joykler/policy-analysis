"""
Dictionary Curation Script for slavery_Slavdict_pretraining_slavery_v25
Stage 1: Slavery Domain Corpus - PERMISSIVE approach
Focus: Historical causes and connections to contemporary problems
"""

import pandas as pd
import re
from pathlib import Path

# Paths
INPUT_PATH = Path("workflow_data/slavery_Slavdict_pretraining_slavery_v25/Dictionary/expanded_candidates.csv")
OUTPUT_PATH = Path("workflow_data/slavery_Slavdict_pretraining_slavery_v25/Dictionary/Curated_dictionary.csv")
REPORT_PATH = Path("workflow_data/slavery_Slavdict_pretraining_slavery_v25/Dictionary/CURATION_REPORT_v25.md")

# Load data
print("Loading expanded dictionary...")
df = pd.read_csv(INPUT_PATH)

print(f"Initial dictionary size: {len(df)} terms")
print(f"Seed terms: {df['is_seed'].sum()}")
print(f"Expanded terms: {(df['is_seed'] == 0).sum()}")
print(f"\nTopics: {df['topic'].unique()}")
print(f"\nDocument frequency range: {df['df'].min()} - {df['df'].max()}")
print(f"Cosine similarity range: {df['cosine'].min():.3f} - {df['cosine'].max():.3f}")

# Initialize decision tracking
df['curation_decision'] = 'KEEP'
df['curation_reason'] = ''

# PHASE 1: AUTOMATIC REMOVAL
print("\n" + "="*70)
print("PHASE 1: AUTOMATIC REMOVAL (Technical Errors)")
print("="*70)

# 1.1: Morphological fragments (very short, likely fragments)
# Be careful with legitimate short terms in Dutch
LEGITIMATE_SHORT = {'wic', 'voc', 'wet', 'olie', 'bon', 'saba'}  # Common abbreviations/short words

mask_fragment = (df['term'].str.len() < 4) & (~df['term'].str.lower().isin(LEGITIMATE_SHORT)) & (df['is_seed'] == 0)
count_fragment = mask_fragment.sum()
df.loc[mask_fragment, 'curation_decision'] = 'REMOVE'
df.loc[mask_fragment, 'curation_reason'] = 'Morphological fragment (len<4)'
print(f"1.1 Morphological fragments: {count_fragment} terms marked for removal")

# 1.2: Extreme low similarity (cosine < 0.65)
mask_low_cosine = (df['cosine'] < 0.65) & (df['is_seed'] == 0)
count_low_cosine = mask_low_cosine.sum()
df.loc[mask_low_cosine, 'curation_decision'] = 'REMOVE'
df.loc[mask_low_cosine, 'curation_reason'] = 'Low cosine similarity (<0.65)'
print(f"1.2 Low cosine similarity: {count_low_cosine} terms marked for removal")

# 1.3: Single document frequency (df == 1)
# More permissive for Stage 1 - only remove if also low cosine or short
mask_single_df = (df['df'] == 1) & (df['cosine'] < 0.72) & (df['is_seed'] == 0)
count_single_df = mask_single_df.sum()
df.loc[mask_single_df, 'curation_decision'] = 'REMOVE'
df.loc[mask_single_df, 'curation_reason'] = 'Single document + low cosine'
print(f"1.3 Single document frequency (with low cosine): {count_single_df} terms marked for removal")

# 1.4: Encoding/OCR errors (simple patterns)
def has_encoding_error(term):
    """Detect obvious encoding issues"""
    if pd.isna(term):
        return True
    # Multiple consecutive spaces or special chars
    if '  ' in term or '\u200b' in term:
        return True
    # Malformed diacritics
    if re.search(r'[àèìòù]{2,}', term):
        return True
    return False

mask_encoding = df['term'].apply(has_encoding_error) & (df['is_seed'] == 0)
count_encoding = mask_encoding.sum()
df.loc[mask_encoding, 'curation_decision'] = 'REMOVE'
df.loc[mask_encoding, 'curation_reason'] = 'Encoding/OCR error'
print(f"1.4 Encoding/OCR errors: {count_encoding} terms marked for removal")

phase1_removals = count_fragment + count_low_cosine + count_single_df + count_encoding
print(f"\nPhase 1 Total: {phase1_removals} terms marked for removal")


# PHASE 2: SEMANTIC DRIFT DETECTION
print("\n" + "="*70)
print("PHASE 2: SEMANTIC DRIFT DETECTION (Wrong Meaning)")
print("="*70)

# 2.1: Low cosine + High weight (likely semantic drift)
mask_drift = (df['cosine'] < 0.72) & (df['weight'] >= 0.95) & (df['is_seed'] == 0) & (df['curation_decision'] == 'KEEP')
count_drift = mask_drift.sum()
df.loc[mask_drift, 'curation_decision'] = 'REVIEW_MANUAL'
df.loc[mask_drift, 'curation_reason'] = 'Low cosine + high weight - possible semantic drift'
print(f"2.1 Potential semantic drift: {count_drift} terms flagged for manual review")

# 2.2: Known polysemous terms that often confuse (Dutch context)
POLYSEMOUS_RISKY = {
    'kast',  # cabinet (furniture) vs caste (social)
    'college',  # school vs executive board
    'staat',  # state/government vs "stands"
    'hof',  # court vs garden
    'bank',  # bank (financial) vs bench
}

mask_polysemy = (df['term'].str.lower().isin(POLYSEMOUS_RISKY)) & (df['is_seed'] == 0) & (df['curation_decision'] == 'KEEP')
count_polysemy = mask_polysemy.sum()
df.loc[mask_polysemy, 'curation_decision'] = 'REVIEW_MANUAL'
df.loc[mask_polysemy, 'curation_reason'] = 'Polysemous term - verify correct meaning'
print(f"2.2 Polysemous terms: {count_polysemy} terms flagged for manual review")

# 2.3: Wrong geographic confusion (other Caribbean islands not relevant to Dutch Caribbean)
# For Stage 1 slavery corpus, keep comparative Caribbean terms at LOW weight
OTHER_CARIBBEAN = {'cuba', 'jamaica', 'haiti', 'trinidad', 'barbados', 'puerto rico', 'dominicaanse republiek'}

mask_other_geo = (df['term'].str.lower().isin(OTHER_CARIBBEAN)) & (df['is_seed'] == 0) & (df['curation_decision'] == 'KEEP')
if mask_other_geo.any():
    # For Stage 1: Keep but ensure low weight (0.40-0.50 for comparative context)
    df.loc[mask_other_geo, 'curation_decision'] = 'REWEIGHT'
    df.loc[mask_other_geo, 'curation_reason'] = 'Other Caribbean - lower to 0.45 for comparative context'
    print(f"2.3 Other Caribbean islands: {mask_other_geo.sum()} terms flagged for reweighting")
else:
    print(f"2.3 Other Caribbean islands: 0 terms found")

phase2_flags = count_drift + count_polysemy + mask_other_geo.sum()
print(f"\nPhase 2 Total: {phase2_flags} terms flagged")


# PHASE 3: OVERGENERALIZATION CONTROL
print("\n" + "="*70)
print("PHASE 3: OVERGENERALIZATION CONTROL (Too Broad)")
print("="*70)

# 3.1: Ultra-high frequency terms (df > 300) with high weight
mask_high_freq = (df['df'] > 300) & (df['weight'] > 0.70) & (df['curation_decision'] == 'KEEP')
count_high_freq = mask_high_freq.sum()
if count_high_freq > 0:
    df.loc[mask_high_freq, 'curation_decision'] = 'REWEIGHT'
    df.loc[mask_high_freq, 'curation_reason'] = 'Ultra-high df (>300) - lower weight by 0.20'
    print(f"3.1 Ultra-high frequency: {count_high_freq} terms flagged for reweighting")
    print(f"    Terms: {df.loc[mask_high_freq, 'term'].tolist()[:5]}")
else:
    print(f"3.1 Ultra-high frequency: 0 terms found")

# 3.2: Generic fragments (terms that are substrings of more specific terms)
# Example: "niveau" when we have "onderwijsniveau", "opleidingsniveau"
GENERIC_FRAGMENTS = {
    'niveau': ['onderwijsniveau', 'opleidingsniveau'],
    'achterstand': ['onderwijsachterstand', 'taalachterstand', 'schoolachterstand'],
    'onderwijs-': ['onderwijs'],  # hyphenated fragment
    'emigratie-': ['emigratie'],  # hyphenated fragment
}

count_generic = 0
for generic, specifics in GENERIC_FRAGMENTS.items():
    # Check if specific versions exist in dictionary
    has_specifics = any((df['term'].str.lower() == s.lower()).any() for s in specifics)
    if has_specifics:
        mask_gen = (df['term'].str.lower() == generic.lower()) & (df['is_seed'] == 0) & (df['curation_decision'] == 'KEEP')
        if mask_gen.any():
            df.loc[mask_gen, 'curation_decision'] = 'REMOVE'
            df.loc[mask_gen, 'curation_reason'] = f'Generic fragment - have specific versions'
            count_generic += mask_gen.sum()

print(f"3.2 Generic fragments: {count_generic} terms marked for removal")

# 3.3: Overly broad institutional terms (for Stage 1, be more permissive)
# Only flag the most extreme cases
ULTRA_GENERIC = {'organisaties', 'instituten', 'systeem', 'structuur'}

mask_ultra_generic = (df['term'].str.lower().isin(ULTRA_GENERIC)) & (df['weight'] > 0.80) & (df['is_seed'] == 0) & (df['curation_decision'] == 'KEEP')
count_ultra_generic = mask_ultra_generic.sum()
if count_ultra_generic > 0:
    df.loc[mask_ultra_generic, 'curation_decision'] = 'REWEIGHT'
    df.loc[mask_ultra_generic, 'curation_reason'] = 'Ultra-generic institutional term - lower to 0.65'
    print(f"3.3 Ultra-generic institutional: {count_ultra_generic} terms flagged for reweighting")
else:
    print(f"3.3 Ultra-generic institutional: 0 terms found")

phase3_total = count_high_freq + count_generic + count_ultra_generic
print(f"\nPhase 3 Total: {phase3_total} terms flagged")


# PHASE 4: CATEGORY CORRECTIONS (Stage 1 - PERMISSIVE)
print("\n" + "="*70)
print("PHASE 4: CATEGORY CORRECTIONS (Stage 1 - Permissive for Historical)")
print("="*70)

# 4.1: Historical processes miscategorized as contemporary problems
# For Stage 1 slavery corpus: KEEP these but ensure proper categorization
HISTORICAL_PROCESSES = {
    'deportaties', 'slavenhandel', 'slavernij', 'kolonisatie', 'plantagesysteem',
    'dwangarbeid', 'transatlantische handel', 'abolitionisme', 'emancipatie',
    'slavenschepen', 'middle passage', 'gewapende opstanden', 'marronage'
}

mask_hist_high = (
    df['term'].str.lower().str.contains('|'.join(HISTORICAL_PROCESSES), na=False) &
    (df['weight'] > 0.85) &
    (df['category'] != 'era_context') &
    (df['is_seed'] == 0) &
    (df['curation_decision'] == 'KEEP')
)

count_hist_recat = mask_hist_high.sum()
if count_hist_recat > 0:
    df.loc[mask_hist_high, 'curation_decision'] = 'RECATEGORIZE'
    df.loc[mask_hist_high, 'curation_reason'] = 'Historical process - move to era_context (0.55-0.65)'
    print(f"4.1 Historical processes to recategorize: {count_hist_recat} terms")
else:
    print(f"4.1 Historical processes: 0 terms need recategorization")

# 4.2: Solution/intervention terms appearing
# For Stage 1: Keep at moderate weight if they help understand domain discourse
INTERVENTION_TERMS = {
    'schuldhulpverlening', 'herstelbetalingen', 'reparaties', 'compensatie',
    'herstelprogramma', 'ontwikkelingshulp', 'onderwijsprogramma'
}

mask_intervention = (
    df['term'].str.lower().isin(INTERVENTION_TERMS) &
    (df['weight'] > 0.75) &
    (df['is_seed'] == 0) &
    (df['curation_decision'] == 'KEEP')
)

count_intervention = mask_intervention.sum()
if count_intervention > 0:
    df.loc[mask_intervention, 'curation_decision'] = 'REWEIGHT'
    df.loc[mask_intervention, 'curation_reason'] = 'Solution/intervention term - lower to 0.70'
    print(f"4.2 Solution/intervention terms: {count_intervention} terms flagged for reweighting")
else:
    print(f"4.2 Solution/intervention terms: 0 terms found")

# 4.3: Bridge terms linking historical to contemporary (KEEP HIGH for Stage 1)
# These are valuable for teaching BERTJE the causal connections
BRIDGE_TERMS = {
    'koloniaal onderwijs', 'koloniale economie', 'slavernijverleden',
    'erfenis van slavernij', 'nawerking', 'structurele ongelijkheid',
    'institutioneel racisme', 'historische achterstand'
}

mask_bridge = df['term'].str.lower().isin(BRIDGE_TERMS) & (df['curation_decision'] == 'KEEP')
count_bridge = mask_bridge.sum()
if count_bridge > 0:
    # Ensure these stay at strong weight (0.75-0.85)
    print(f"4.3 Bridge terms (historical->contemporary): {count_bridge} terms confirmed KEEP at current weight")
else:
    print(f"4.3 Bridge terms: 0 explicit bridge terms found")

phase4_total = count_hist_recat + count_intervention
print(f"\nPhase 4 Total: {phase4_total} terms flagged")


# PHASE 5: WEIGHT CALIBRATION
print("\n" + "="*70)
print("PHASE 5: WEIGHT CALIBRATION (Fine-tuning)")
print("="*70)

# 5.1: High document frequency dampening (more permissive thresholds for Stage 1)
mask_freq_high = (df['df'] > 250) & (df['weight'] > 0.75) & (df['curation_decision'] == 'KEEP')
count_freq_adjust = mask_freq_high.sum()
if count_freq_adjust > 0:
    df.loc[mask_freq_high, 'curation_decision'] = 'REWEIGHT'
    df.loc[mask_freq_high, 'curation_reason'] = 'High df (>250) - lower weight by 0.15'
    print(f"5.1 High frequency dampening: {count_freq_adjust} terms flagged")
else:
    print(f"5.1 High frequency dampening: 0 terms flagged")

# 5.2: Semantic distance dampening (expanded terms with lower cosine)
mask_sem_dist = (
    (df['cosine'] < 0.75) &
    (df['weight'] >= 0.85) &
    (df['is_seed'] == 0) &
    (df['curation_decision'] == 'KEEP')
)
count_sem_dist = mask_sem_dist.sum()
if count_sem_dist > 0:
    df.loc[mask_sem_dist, 'curation_decision'] = 'REWEIGHT'
    df.loc[mask_sem_dist, 'curation_reason'] = 'Cosine <0.75 + high weight - lower by 0.10'
    print(f"5.2 Semantic distance dampening: {count_sem_dist} terms flagged")
else:
    print(f"5.2 Semantic distance dampening: 0 terms flagged")

phase5_total = count_freq_adjust + count_sem_dist
print(f"\nPhase 5 Total: {phase5_total} terms flagged")


# SUMMARY STATISTICS
print("\n" + "="*70)
print("CURATION SUMMARY")
print("="*70)

decision_counts = df['curation_decision'].value_counts()
print("\nDecision breakdown:")
for decision, count in decision_counts.items():
    pct = (count / len(df)) * 100
    print(f"  {decision}: {count} ({pct:.1f}%)")

# Calculate final dictionary size after removals
final_size = len(df[df['curation_decision'].isin(['KEEP', 'REWEIGHT', 'RECATEGORIZE', 'REVIEW_MANUAL'])])
removed_size = len(df[df['curation_decision'] == 'REMOVE'])

print(f"\nProjected dictionary size after curation:")
print(f"  Current: {len(df)} terms")
print(f"  After removals: {final_size} terms ({(final_size/len(df))*100:.1f}% retained)")
print(f"  Removed: {removed_size} terms ({(removed_size/len(df))*100:.1f}%)")

# Topic distribution
print("\nTerms per topic (after removals):")
topic_dist = df[df['curation_decision'] != 'REMOVE'].groupby('topic').size().sort_values(ascending=False)
for topic, count in topic_dist.items():
    print(f"  {topic}: {count} terms")

# Save intermediate results for manual review
print("\n" + "="*70)
print("SAVING RESULTS")
print("="*70)

# Create review file with all flagged terms
review_df = df[df['curation_decision'].isin(['REVIEW_MANUAL', 'REWEIGHT', 'RECATEGORIZE'])].copy()
review_df = review_df.sort_values(['curation_decision', 'weight', 'cosine'], ascending=[True, False, True])

review_path = Path("workflow_data/slavery_Slavdict_pretraining_slavery_v25/Dictionary/curation_review_needed.csv")
review_df.to_csv(review_path, index=False)
print(f"Saved {len(review_df)} terms needing manual review to: {review_path}")

# Save full annotated dictionary
annotated_path = Path("workflow_data/slavery_Slavdict_pretraining_slavery_v25/Dictionary/expanded_candidates_annotated.csv")
df.to_csv(annotated_path, index=False)
print(f"Saved fully annotated dictionary to: {annotated_path}")

print("\n" + "="*70)
print("NEXT STEPS")
print("="*70)
print("1. Review 'curation_review_needed.csv' for manual decisions")
print("2. Apply final decisions and create curated dictionary")
print("3. Generate curation report")
print("\nRun the next script to finalize curation after manual review.")
