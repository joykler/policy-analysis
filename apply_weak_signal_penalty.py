"""
Apply weak-signal penalty to Cell 5.2 to differentiate between:
- noise_uniform_scores: Low CV (all topics similar)
- noise_weak_signal: Low magnitude (all scores near corpus floor)
"""

import json
from pathlib import Path

print("="*80)
print("APPLYING WEAK-SIGNAL PENALTY TO CELL 5.2")
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

cell_source = ''.join(notebook['cells'][cell_52_idx]['source'])

# ============================================================
# UPDATE 1: Add weak-signal detection BEFORE weighted combination
# ============================================================

print("\n[1/3] Adding weak-signal detection...")

old_magnitude = """    # Component 1: Magnitude (dynamic corpus-specific normalization)
    # UPDATED: Uses actual corpus min/max instead of hardcoded 2-9 range
    magnitude = (max_score - corpus_min) / corpus_range
    magnitude = np.clip(magnitude, 0, 1)"""

new_magnitude = """    # Component 1: Magnitude (dynamic corpus-specific normalization)
    # UPDATED: Uses actual corpus min/max instead of hardcoded 2-9 range
    magnitude = (max_score - corpus_min) / corpus_range
    magnitude = np.clip(magnitude, 0, 1)

    # Weak-signal detection: Flag chunks in bottom 20% of corpus range
    low_signal_threshold = 0.20  # 20% of corpus range
    weak_signal = magnitude < low_signal_threshold"""

if old_magnitude in cell_source:
    cell_source = cell_source.replace(old_magnitude, new_magnitude)
    print("  [OK] Added weak-signal detection after magnitude calculation")
else:
    print("  [WARNING] Could not find magnitude calculation to update")

# ============================================================
# UPDATE 2: Add weak-signal penalty to significance score
# ============================================================

print("\n[2/3] Adding weak-signal penalty to significance calculation...")

old_weights = """    # Weighted combination
    # UPDATED WEIGHTS based on BERTJE evaluation:
    # - Differentiation (CV) is MOST important (0.6) - BERTJE wins via semantic understanding
    # - Magnitude is less important (0.25) - raw scores vary by corpus
    # - Contrast is helpful but minor (0.15)
    significance = (
        0.60 * differentiation +  # Emphasize topic differentiation (was 0.5)
        0.25 * magnitude +        # De-emphasize raw scores (was 0.3)
        0.15 * contrast           # De-emphasize Z-score (was 0.2)
    )
    significance = np.clip(significance, 0, 1)"""

new_weights = """    # Weighted combination
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

    significance = np.clip(significance, 0, 1)"""

if old_weights in cell_source:
    cell_source = cell_source.replace(old_weights, new_weights)
    print("  [OK] Added weak-signal penalty after weighted combination")
else:
    print("  [WARNING] Could not find weighted combination to update")

# ============================================================
# UPDATE 3: Update categorization logic to check weak_signal FIRST
# ============================================================

print("\n[3/3] Updating categorization logic...")

old_categorize = """    # Categorize (UPDATED THRESHOLDS based on evaluation)
    # Lowered thresholds to capture +26% more training data
    if cv < 0.10:
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
        category = 'noise_weak_signal'
        priority = 'exclude'"""

new_categorize = """    # Categorize (UPDATED THRESHOLDS based on evaluation)
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
        priority = 'exclude'"""

if old_categorize in cell_source:
    cell_source = cell_source.replace(old_categorize, new_categorize)
    print("  [OK] Updated categorization to check weak_signal first")
else:
    print("  [WARNING] Could not find categorization logic to update")

# ============================================================
# UPDATE 4: Add weak_signal_flag and penalty to return dict
# ============================================================

print("\n[4/3 BONUS] Adding weak_signal_flag to return values...")

old_return = """    return {
        'significance_score': significance,
        'significance_category': category,
        'priority': priority,
        'cv': cv,
        'z_max': z_max,
        'magnitude_norm': magnitude,
        'differentiation_norm': differentiation,
        'contrast_norm': contrast
    }"""

new_return = """    return {
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
    }"""

if old_return in cell_source:
    cell_source = cell_source.replace(old_return, new_return)
    print("  [OK] Added weak_signal_flag and penalty to return dictionary")
else:
    print("  [WARNING] Could not find return statement to update")

# ============================================================
# Save updated notebook
# ============================================================

print("\n" + "="*80)
print("SAVING UPDATED NOTEBOOK")
print("="*80)

# Convert back to list of lines
notebook['cells'][cell_52_idx]['source'] = cell_source.split('\n')

# Create backup (with different name to preserve previous backup)
backup_path = notebook_path.with_suffix('.ipynb.backup2')
import shutil
if backup_path.exists():
    print(f"\n  Previous backup2 exists, will overwrite")
shutil.copy(notebook_path, backup_path)
print(f"  [OK] Created backup: {backup_path}")

# Save updated notebook
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f"  [OK] Saved updated notebook: {notebook_path}")

# ============================================================
# Summary
# ============================================================

print("\n" + "="*80)
print("UPDATE SUMMARY")
print("="*80)

print("""
Applied weak-signal penalty to Cell 5.2:

1. [OK] Added weak-signal detection (magnitude < 0.20)
2. [OK] Added weak-signal penalty to significance score
3. [OK] Updated categorization to check weak_signal FIRST
4. [OK] Added weak_signal_flag and penalty to return values

KEY CHANGES:

BEFORE:
- All noise lumped into 'noise_uniform_scores' or catch-all
- Low-magnitude chunks could sneak into high tiers via coincidental CV

AFTER:
- noise_weak_signal: Low magnitude (bottom 20% of corpus) = irrelevant/off-topic
- noise_uniform_scores: Low CV (< 0.10) = all topics similar, no clear assignment
- Weak-signal penalty: significance *= (magnitude / 0.20) for chunks with magnitude < 0.20

EXPECTED IMPACT:

Current state:
- noise_uniform_scores: ~17-22% of chunks
- noise_weak_signal: 0% (not properly detected)

After update:
- noise_uniform_scores: ~15-20% (chunks with CV < 0.10)
- noise_weak_signal: ~5-10% (chunks with magnitude < 0.20)
- Better separation of noise types
- High/medium tiers contain only genuinely relevant chunks

VALIDATION:
After re-running Cell 5.2, check:
1. noise_weak_signal is now populated (should be ~5-10%)
2. noise_uniform_scores is still populated (~15-20%)
3. These two categories have minimal overlap
4. High/medium chunks have both high magnitude AND high CV
""")

print("="*80)
print("[OK] WEAK-SIGNAL PENALTY APPLIED")
print("="*80)
