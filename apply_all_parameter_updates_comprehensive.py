"""
Comprehensive application of ALL parameter updates to Cell 5.2.
This script fixes the issue where previous updates didn't actually modify the cell content.
"""

import json
import re
from pathlib import Path

print("="*80)
print("COMPREHENSIVE PARAMETER UPDATE FOR CELL 5.2")
print("="*80)

# Load notebook
notebook_path = Path("A__dictionary_discovery_v20_unified_embedding.ipynb")
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Find Cell 5.2
cell_52_idx = None
for i, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'CELL 5.2: SIGNIFICANCE-BASED CLASSIFICATION' in source:
            cell_52_idx = i
            break

if cell_52_idx is None:
    raise ValueError("Could not find Cell 5.2!")

print(f"\nFound Cell 5.2 at index {cell_52_idx}")

# Get full cell source
cell_source = ''.join(notebook['cells'][cell_52_idx]['source'])

print(f"Current cell length: {len(cell_source)} characters")

# ============================================================
# COMPLETE FUNCTION REPLACEMENT
# ============================================================

print("\n[STRATEGY] Replacing entire calculate_significance function...")

# Find the function definition
func_start = cell_source.find('def calculate_significance(')
if func_start == -1:
    raise ValueError("Could not find calculate_significance function!")

# Find the end of the function (next top-level code that's not indented)
# Look for the next line that starts with print (the "Calculating significance scores..." line)
func_end = cell_source.find('print("\\nCalculating significance scores...")', func_start)
if func_end == -1:
    raise ValueError("Could not find end of calculate_significance function!")

# Extract everything before and after the function
before_func = cell_source[:func_start]
after_func = cell_source[func_end:]

print(f"  Before function: {len(before_func)} chars")
print(f"  After function: {len(after_func)} chars")

# New function implementation with ALL updates
new_function = '''def calculate_significance(row, topic_cols, corpus_min, corpus_max, corpus_range):
    """
    Calculate significance combining magnitude, differentiation, contrast.

    UPDATED 2025-12-11:
    - Dynamic corpus-specific normalization
    - Reweighted components (CV: 0.6, Mag: 0.25, Con: 0.15)
    - Weak-signal detection and penalty
    - Lowered thresholds (0.60, 0.45, 0.25)
    """
    scores = [row[col] for col in topic_cols]
    max_score = max(scores)
    mean_score = np.mean(scores)
    std_score = np.std(scores)

    # Component 1: Magnitude (dynamic corpus-specific normalization)
    # UPDATED: Uses actual corpus min/max instead of hardcoded 2-9 range
    magnitude = (max_score - corpus_min) / corpus_range if corpus_range > 0 else 0
    magnitude = np.clip(magnitude, 0, 1)

    # Weak-signal detection: Flag chunks in bottom 20% of corpus range
    low_signal_threshold = 0.20  # 20% of corpus range
    weak_signal = magnitude < low_signal_threshold

    # Component 2: Differentiation (CV)
    # UPDATED: Use 0.55 as upper bound (covers both Slavery and Policy corpora)
    cv = std_score / mean_score if mean_score > 0 else 0
    differentiation = cv / 0.55  # Upper bound covers both corpora
    differentiation = np.clip(differentiation, 0, 1)

    # Component 3: Contrast (Z-score)
    # UPDATED: Refined range based on corpus analysis
    z_max = (max_score - mean_score) / std_score if std_score > 0 else 0
    contrast = (z_max - 0.60) / 1.13  # Scale 0.60-1.73 to 0-1
    contrast = np.clip(contrast, 0, 1)

    # Weighted combination
    # UPDATED WEIGHTS based on BERTJE evaluation:
    # - Differentiation (CV) is MOST important (0.6) - BERTJE wins via semantic understanding
    # - Magnitude is less important (0.25) - raw scores vary by corpus
    # - Contrast is helpful but minor (0.15)
    significance = (
        0.60 * differentiation +  # Emphasize topic differentiation (was 0.5)
        0.25 * magnitude +        # De-emphasize raw scores (was 0.3)
        0.15 * contrast           # De-emphasize Z-score (was 0.2)
    )
    significance = np.clip(significance, 0, 1)

    # Apply weak-signal penalty: Prevent low-magnitude chunks from sneaking into
    # high tiers via coincidental CV/contrast. Scale significance by how far
    # above the threshold the magnitude is.
    if weak_signal and low_signal_threshold > 0:
        penalty = magnitude / low_signal_threshold  # 0.0 to 1.0
        significance *= penalty
    else:
        penalty = 1.0

    significance = np.clip(significance, 0, 1)

    # Categorize (UPDATED THRESHOLDS based on evaluation)
    # Check weak_signal FIRST to separate from uniform_scores
    if weak_signal:
        # Low magnitude (near corpus floor) - chunk is irrelevant/off-topic
        category = 'noise_weak_signal'
        priority = 'exclude'
    elif cv < 0.10:
        # Low CV (all topics similar) - no clear topic assignment
        category = 'noise_uniform_scores'
        priority = 'exclude'
    elif significance >= 0.60:  # Lowered from 0.70
        category = 'high_significance'
        priority = 'primary_training'
    elif significance >= 0.45:  # Lowered from 0.50
        category = 'medium_significance'
        priority = 'secondary_training'
    elif significance >= 0.25:  # Lowered from 0.30
        category = 'low_significance'
        priority = 'manual_review'
    else:
        # Catch-all for edge cases (shouldn't happen often)
        category = 'noise_weak_signal'
        priority = 'exclude'

    return {
        'significance_score': significance,
        'significance_category': category,
        'priority': priority,
        'cv': cv,
        'z_max': z_max,
        'magnitude_norm': magnitude,
        'differentiation_norm': differentiation,
        'contrast_norm': contrast,
        'weak_signal_flag': weak_signal,
        'weak_signal_penalty': penalty
    }

'''

# Reconstruct cell with new function
new_cell_source = before_func + new_function + after_func

# ============================================================
# ADD CORPUS STATISTICS CALCULATION
# ============================================================

print("\n[UPDATE] Adding corpus statistics calculation...")

# Find where to insert (after topic_cols definition)
insert_marker = 'print(f"\\nTopic columns: {topic_cols}")'
if insert_marker in new_cell_source:
    corpus_stats_code = '''

# ============================================================
# CALCULATE CORPUS STATISTICS (for dynamic normalization)
# ============================================================

print(f"\\n{'='*80}")
print("CALCULATING CORPUS-SPECIFIC STATISTICS")
print(f"{'='*80}")

all_topic_scores = all_scores_df[[col for col in all_scores_df.columns if col.startswith('score_')]].values
corpus_min = float(all_topic_scores.min())
corpus_max = float(all_topic_scores.max())
corpus_range = corpus_max - corpus_min

print(f"\\nCorpus score range: {corpus_min:.3f} - {corpus_max:.3f}")
print(f"Corpus range span: {corpus_range:.3f}")

# Detect corpus type
if corpus_max < 10.0:
    corpus_type = "slavery"
    print(f"Detected corpus type: SLAVERY (low score range)")
else:
    corpus_type = "policy"
    print(f"Detected corpus type: POLICY (high score range)")

'''
    new_cell_source = new_cell_source.replace(insert_marker, insert_marker + corpus_stats_code)
    print("  [OK] Added corpus statistics calculation")
else:
    print("  [WARNING] Could not find insertion point")

# ============================================================
# UPDATE FUNCTION CALL
# ============================================================

print("\n[UPDATE] Updating function call...")

old_call = 'sig = calculate_significance(row, topic_cols)'
new_call = 'sig = calculate_significance(row, topic_cols, corpus_min, corpus_max, corpus_range)'

if old_call in new_cell_source:
    new_cell_source = new_cell_source.replace(old_call, new_call)
    print("  [OK] Updated function call to pass corpus parameters")
else:
    print("  [WARNING] Could not find function call")

# ============================================================
# Save updated notebook
# ============================================================

print("\n" + "="*80)
print("SAVING UPDATED NOTEBOOK")
print("="*80)

# Convert to list of lines
notebook['cells'][cell_52_idx]['source'] = new_cell_source.split('\n')

# Create backup
backup_path = notebook_path.with_suffix('.ipynb.backup_comprehensive')
import shutil
shutil.copy(notebook_path, backup_path)
print(f"\n  [OK] Created backup: {backup_path.name}")

# Save
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f"  [OK] Saved updated notebook")

# ============================================================
# Verification
# ============================================================

print("\n" + "="*80)
print("VERIFICATION")
print("="*80)

# Re-load and check
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb_check = json.load(f)

cell_check = ''.join(nb_check['cells'][cell_52_idx]['source'])

checks = {
    'corpus_min, corpus_max, corpus_range': 'corpus_min, corpus_max, corpus_range' in cell_check,
    'Dynamic magnitude normalization': 'corpus_min) / corpus_range' in cell_check,
    'Weak-signal detection': 'weak_signal = magnitude < low_signal_threshold' in cell_check,
    'Weak-signal penalty': 'significance *= penalty' in cell_check,
    'Updated weights (0.60, 0.25, 0.15)': '0.60 * differentiation' in cell_check,
    'Updated thresholds (0.60, 0.45, 0.25)': 'significance >= 0.60' in cell_check,
    'CV normalization (0.55)': 'cv / 0.55' in cell_check,
    'Z-score normalization (0.60, 1.13)': '(z_max - 0.60) / 1.13' in cell_check,
    'weak_signal checked first': 'if weak_signal:' in cell_check,
    'Return includes weak_signal_flag': "'weak_signal_flag': weak_signal" in cell_check
}

print("\nFeature verification:")
for feature, present in checks.items():
    status = "[OK]" if present else "[MISSING]"
    print(f"  {status} {feature}")

all_present = all(checks.values())

print("\n" + "="*80)
if all_present:
    print("[SUCCESS] ALL UPDATES APPLIED SUCCESSFULLY")
else:
    print("[WARNING] Some updates may be missing")
print("="*80)

print(f"""
SUMMARY:

Applied ALL parameter updates to Cell 5.2:

1. Added corpus statistics calculation (corpus_min, corpus_max, corpus_range)
2. Replaced entire calculate_significance() function with updated version
3. Dynamic magnitude normalization
4. Updated CV normalization (0.5 -> 0.55)
5. Updated Z-score normalization (0.6/1.1 -> 0.60/1.13)
6. Updated component weights (0.5/0.3/0.2 -> 0.6/0.25/0.15)
7. Added weak-signal detection (magnitude < 0.20)
8. Added weak-signal penalty (significance *= penalty)
9. Updated categorization logic (weak_signal checked first)
10. Updated thresholds (0.50/0.40/0.10 -> 0.60/0.45/0.25)
11. Updated function call to pass corpus parameters
12. Added weak_signal_flag and penalty to return dict

NEXT STEPS:

1. Open notebook and visually verify Cell 5.2
2. Re-run Cell 5.2 on corrected data
3. Verify both noise categories are populated:
   - noise_uniform_scores: ~15-20% (low CV)
   - noise_weak_signal: ~5-10% (low magnitude)
4. Check high/medium/low distributions
5. Validate examples make sense

""")
