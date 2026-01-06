import json
from datetime import datetime

# Create standalone visualization notebook
notebook = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.8.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

cells = []

# ============================================================
# Cell 0: Notebook Header (Markdown)
# ============================================================

header_md = """# Visualization Workflow v1
## Standalone Dictionary & Model Validation Visualizations

**Purpose**: Generate comprehensive visualizations for dictionary fitness, model performance, and topic coherence analysis.

**Independence**: This notebook can run independently by loading outputs from any completed workflow run.

**Date Created**: """ + datetime.now().strftime("%Y-%m-%d") + """

---

## Overview

This notebook generates visualizations for:
1. **Dictionary Fitness**: Weight validation, expansion quality, term clustering
2. **Model Comparison**: Pretrained vs. Domain-adapted vs. Policy-trained
3. **Topic Coherence**: Cluster quality, separation metrics
4. **Chunk Analysis**: Clustering, shifts, scoring patterns
5. **Score Distribution**: Cosine vs. BERTJE comparison
6. **Thesis-Specific**: Temporal trends, document type analysis

---

## Required Data Files

**From Source Workflow** (configured via `SOURCE_WORKFLOW`):
- `Dictionary/Curated_dictionary.csv` - Dictionary terms with weights, categories
- `Cosine_labeling/scores_all_labeled.csv` - Chunk scores from cosine similarity
- `Other_data/chunked_corpus.csv` - Chunk metadata (doc_type, year, text)
- `Model_finetuning/trained_encoder/` - Policy-trained model (if comparing models)
- `Model_finetuning/training_metrics.json` - Training history (optional)
- `BERTJE_predictions/bertje_*_predictions_*.csv` - BERTJE predictions (optional)

**Generated Outputs**:
- `Visuals/` - All visualization files (HTML, PNG, CSV)

---

## Quick Start

1. **Set source workflow path** in Cell 1 (Configuration)
2. **Configure models to compare** (base_cosine, pretrained_bertje, slavery_trained, policy_trained)
3. **Apply metadata filters** if needed (doc_type, year_range, doc_folder)
4. **Run all cells** to generate visualizations

---"""

cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [header_md]
})

# ============================================================
# Cell 1: Configuration (Code)
# ============================================================

config_code = """# ============================================================
# CONFIGURATION
# ============================================================

from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 1. SOURCE WORKFLOW PATH
# ============================================================

# Set to the workflow directory containing Dictionary/, Cosine_labeling/, etc.
# Example: "workflow_data/Policy_Slavdict_FT-slavery_slavery_v1"
# Or set to None to use current directory

SOURCE_WORKFLOW = None  # Set to workflow path or None for current directory

# ============================================================
# 2. MODEL COMPARISON SETTINGS
# ============================================================

COMPARE_MODELS = {
    'base_cosine': True,          # Dictionary-based cosine scores (always available)
    'pretrained_bertje': True,    # GroNLP/bert-base-dutch-cased (will generate embeddings)
    'slavery_trained': False,     # Domain-adapted model (set True if available)
    'policy_trained': True        # V10 finetuned model (from workflow's Model_finetuning/)
}

# Model paths (auto-detected from SOURCE_WORKFLOW if None)
MODEL_PATHS = {
    'pretrained_bertje': 'GroNLP/bert-base-dutch-cased',  # HuggingFace model
    'slavery_trained': None,      # Auto-detect or set custom path
    'policy_trained': None        # Auto-detect from SOURCE_WORKFLOW/Model_finetuning/trained_encoder
}

# ============================================================
# 3. METADATA FILTERS
# ============================================================

# Filter chunks by metadata (None = no filter, use all chunks)
METADATA_FILTERS = {
    'doc_type': None,      # None = all, or list like ['policy', 'report']
    'year_range': None,    # None = all, or tuple like (2015, 2024)
    'doc_folder': None     # None = all, or specific folder name
}

# ============================================================
# 4. VISUALIZATION SETTINGS
# ============================================================

MIN_SCORE_THRESHOLD = 0.3        # Minimum score for "relevant" classification
TOP_N_SHIFTERS = 100             # How many top-shifting chunks to visualize
SAMPLE_SIZE_3D = 1000            # Max chunks for 3D plots (performance limit)
PCA_RANDOM_STATE = 42            # For reproducibility
FIGURE_DPI = 150                 # Figure resolution

# ============================================================
# 5. OUTPUT SETTINGS
# ============================================================

SAVE_INTERACTIVE = True          # Save HTML plots (interactive)
SAVE_STATIC = False              # Save PNG/PDF for thesis (requires kaleido)
SHOW_IN_NOTEBOOK = True          # Display plots inline

# ============================================================
# 6. GLOBAL STATE
# ============================================================

VIZ_AVAILABLE = True  # Will be set to False if critical errors occur

print("="*70)
print("VISUALIZATION WORKFLOW v1 - CONFIGURATION")
print("="*70)
print(f"\\nSource workflow: {SOURCE_WORKFLOW if SOURCE_WORKFLOW else 'Current directory'}")
print(f"\\nModels to compare:")
for model, enabled in COMPARE_MODELS.items():
    status = "✓" if enabled else "⊘"
    print(f"  {status} {model}")
print(f"\\nVisualization settings:")
print(f"  - Score threshold: {MIN_SCORE_THRESHOLD}")
print(f"  - 3D sample size: {SAMPLE_SIZE_3D}")
print(f"  - PCA random state: {PCA_RANDOM_STATE}")
print(f"\\nOutput settings:")
print(f"  - Save interactive (HTML): {SAVE_INTERACTIVE}")
print(f"  - Save static (PNG): {SAVE_STATIC}")
print(f"  - Show in notebook: {SHOW_IN_NOTEBOOK}")
print("="*70)"""

cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [config_code]
})

# ============================================================
# Cell 2: Filesystem Setup (Code)
# ============================================================

filesystem_code = """# ============================================================
# FILESYSTEM SETUP
# ============================================================

print(f"\\n{'='*70}")
print("FILESYSTEM SETUP")
print(f"{'='*70}")

# --------------------------------------------------------
# 1. Determine Base Directory
# --------------------------------------------------------

if SOURCE_WORKFLOW is None:
    # Use current working directory
    base_dir = Path.cwd()
    print(f"\\nUsing current directory: {base_dir}")
else:
    # Use specified workflow directory
    base_dir = Path(SOURCE_WORKFLOW)
    if not base_dir.is_absolute():
        base_dir = Path.cwd() / base_dir

    if not base_dir.exists():
        print(f"\\n❌ ERROR: Source workflow directory not found: {base_dir}")
        print(f"   Please check SOURCE_WORKFLOW path in Cell 1")
        VIZ_AVAILABLE = False
    else:
        print(f"\\nUsing workflow directory: {base_dir}")

# --------------------------------------------------------
# 2. Define Folder Structure
# --------------------------------------------------------

if VIZ_AVAILABLE:
    folders = {
        'Dictionary': base_dir / 'Dictionary',
        'Cosine_labeling': base_dir / 'Cosine_labeling',
        'Other_data': base_dir / 'Other_data',
        'Model_finetuning': base_dir / 'Model_finetuning',
        'BERTJE_predictions': base_dir / 'BERTJE_predictions',
        'Visuals': base_dir / 'Visuals'
    }

    print(f"\\nFolder structure:")

    # Check which folders exist
    for folder_name, folder_path in folders.items():
        exists = folder_path.exists()
        status = "✓" if exists else "⚠"

        if folder_name == 'Visuals':
            # Create if doesn't exist
            if not exists:
                folder_path.mkdir(parents=True, exist_ok=True)
                print(f"  {status} {folder_name:20s}: Created")
            else:
                print(f"  {status} {folder_name:20s}: {folder_path}")
        elif folder_name in ['BERTJE_predictions', 'Model_finetuning']:
            # Optional folders
            print(f"  {status} {folder_name:20s}: {'Found' if exists else 'Not found (optional)'}")
        else:
            # Required folders
            if not exists:
                print(f"  {status} {folder_name:20s}: ❌ NOT FOUND (REQUIRED)")
                VIZ_AVAILABLE = False
            else:
                print(f"  {status} {folder_name:20s}: {folder_path}")

    # Create convenience variable
    visuals_dir = folders['Visuals']

    print(f"\\n{'='*70}")

    if VIZ_AVAILABLE:
        print("✓ Filesystem setup complete")
    else:
        print("❌ Filesystem setup failed - missing required folders")
        print("   Required: Dictionary/, Cosine_labeling/, Other_data/")

    print(f"{'='*70}")

else:
    print(f"\\n⊘ Skipping filesystem setup - VIZ_AVAILABLE = False")"""

cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [filesystem_code]
})

# Now add all the CP9 cells from the v26 notebook
# Read the v26 notebook to extract CP9 cells

print("Loading CP9 cells from v26 notebook...")

with open(r'C:\Users\Home\policy-analysis\A__dictionary_discovery_v26_newdict.ipynb', 'r', encoding='utf-8') as f:
    v26_nb = json.load(f)

# Extract cells 73-106 (CP9 cells)
# But we need to modify them slightly:
# - Replace source_fs references with folders dict
# - Skip the CP9 header cell (73) since we have our own

cp9_cells_to_extract = list(range(74, 107))  # Cells 74-106 (skip 73 which is just header)

print(f"Extracting {len(cp9_cells_to_extract)} CP9 cells...")

for cell_idx in cp9_cells_to_extract:
    if cell_idx < len(v26_nb['cells']):
        cell = v26_nb['cells'][cell_idx].copy()

        # Modify source code to use 'folders' instead of 'source_fs.folders'
        if cell['cell_type'] == 'code' and cell['source']:
            source = cell['source']

            if isinstance(source, list):
                source_text = ''.join(source)
            else:
                source_text = source

            # Replace source_fs references
            source_text = source_text.replace('source_fs.folders.get(', 'folders.get(')
            source_text = source_text.replace('source_fs.folders[', 'folders[')
            source_text = source_text.replace('source_fs.root', 'base_dir')

            # For model paths, use folders dict
            source_text = source_text.replace(
                "source_fs.folders.get('Model_finetuning')",
                "folders['Model_finetuning']"
            )

            cell['source'] = [source_text]

        cells.append(cell)

print(f"Extracted {len(cells) - 3} CP9 cells")

# Set notebook cells
notebook['cells'] = cells

# Save
output_path = r'C:\Users\Home\policy-analysis\A___Visualizations_v1.ipynb'

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print(f"\n{'='*70}")
print("STANDALONE VISUALIZATION NOTEBOOK CREATED!")
print(f"{'='*70}")
print(f"\nNotebook: A___Visualizations_v1.ipynb")
print(f"Total cells: {len(cells)}")
print(f"\nStructure:")
print(f"  Cell 0: Header & Documentation (Markdown)")
print(f"  Cell 1: Configuration")
print(f"  Cell 2: Filesystem Setup")
print(f"  Cells 3-{len(cells)-1}: CP9 Visualizations (from v26)")
print(f"\nFeatures:")
print(f"  ✓ Independent workflow - no dependencies on main training notebook")
print(f"  ✓ Configurable source workflow path")
print(f"  ✓ Flexible model comparison (enable/disable models)")
print(f"  ✓ Metadata filtering (doc_type, year, folder)")
print(f"  ✓ All 34 CP9 visualizations included")
print(f"  ✓ Auto-creates output directory (Visuals/)")
print(f"\nReady to run!")
print(f"{'='*70}")
