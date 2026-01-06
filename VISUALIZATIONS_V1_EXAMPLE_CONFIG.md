# A___Visualizations_v1 - Example Configuration

## Typical Setup

Here's a typical configuration for the standalone visualization notebook:

### Scenario: Compare Base Cosine vs. Pretrained BERTje vs. Policy-trained Model

**Goal**: Generate visualizations using:
- Dictionary and cosine scores from `Policy_Slavdict_FT-slavery_slavery_v1` workflow
- Policy-trained model from the same workflow
- Pretrained BERTje from HuggingFace
- NO slavery-trained model (we don't have one)

---

## Cell 1 Configuration

```python
# ============================================================
# 1. SOURCE WORKFLOW PATH
# ============================================================

# Where your Dictionary/ and Cosine_labeling/ folders are
SOURCE_WORKFLOW = "workflow_data/Policy_Slavdict_FT-slavery_slavery_v1"

# ============================================================
# 2. MODEL COMPARISON SETTINGS
# ============================================================

COMPARE_MODELS = {
    'base_cosine': True,          # Use existing cosine scores - always enable
    'pretrained_bertje': True,    # Download from HuggingFace - enable for baseline
    'slavery_trained': False,     # We don't have this model - disable
    'policy_trained': True        # We have this model - enable
}

# ============================================================
# 3. EXPLICIT MODEL PATHS
# ============================================================

MODEL_PATHS = {
    # Pretrained - downloads automatically, no changes needed
    'pretrained_bertje': 'GroNLP/bert-base-dutch-cased',

    # Slavery-trained - we don't have it, leave as None
    'slavery_trained': None,

    # Policy-trained - set to exact path of trained_encoder folder
    'policy_trained': 'workflow_data/Policy_Slavdict_FT-slavery_slavery_v1/Model_finetuning/trained_encoder'
}

# ============================================================
# 4. METADATA FILTERS
# ============================================================

# No filters - use all chunks
METADATA_FILTERS = {
    'doc_type': None,
    'year_range': None,
    'doc_folder': None
}

# ============================================================
# 5. VISUALIZATION SETTINGS
# ============================================================

MIN_SCORE_THRESHOLD = 0.3
TOP_N_SHIFTERS = 100
SAMPLE_SIZE_3D = 1000
PCA_RANDOM_STATE = 42
FIGURE_DPI = 150

# ============================================================
# 6. OUTPUT SETTINGS
# ============================================================

SAVE_INTERACTIVE = True   # Save HTML files
SAVE_STATIC = False       # Don't save PNG (install kaleido first if you want this)
SHOW_IN_NOTEBOOK = True   # Display inline
```

---

## Alternative Scenario: Models from Different Workflows

**Goal**: Compare models from different workflow runs:
- Dictionary/scores from v1 workflow
- Slavery-trained model from v13 workflow (different corpus)
- Policy-trained model from v1 workflow

```python
# Data source
SOURCE_WORKFLOW = "workflow_data/Policy_Slavdict_FT-slavery_slavery_v1"

# Enable all 4 model types
COMPARE_MODELS = {
    'base_cosine': True,
    'pretrained_bertje': True,
    'slavery_trained': True,      # Enable this time
    'policy_trained': True
}

# Models from different workflows
MODEL_PATHS = {
    'pretrained_bertje': 'GroNLP/bert-base-dutch-cased',

    # Slavery-trained from a DIFFERENT workflow (v13)
    'slavery_trained': 'workflow_data/slavery_Slavdict_pretraining_slavery_v13/Model_finetuning/slavery_domain_encoder',

    # Policy-trained from SAME workflow as data
    'policy_trained': 'workflow_data/Policy_Slavdict_FT-slavery_slavery_v1/Model_finetuning/trained_encoder'
}
```

**Note**: This is useful for comparing:
- Pre-training on slavery corpus (v13) vs. finetuning on policy corpus (v1)
- Different training strategies
- Transfer learning effectiveness

---

## Filtered Analysis Example

**Goal**: Analyze only policy documents from 2020-2024

```python
SOURCE_WORKFLOW = "workflow_data/Policy_Slavdict_FT-slavery_slavery_v1"

COMPARE_MODELS = {
    'base_cosine': True,
    'pretrained_bertje': False,   # Skip for speed
    'slavery_trained': False,
    'policy_trained': True
}

MODEL_PATHS = {
    'pretrained_bertje': 'GroNLP/bert-base-dutch-cased',
    'slavery_trained': None,
    'policy_trained': 'workflow_data/Policy_Slavdict_FT-slavery_slavery_v1/Model_finetuning/trained_encoder'
}

# Apply filters
METADATA_FILTERS = {
    'doc_type': ['policy'],           # Only policy documents
    'year_range': (2020, 2024),       # Recent years only
    'doc_folder': None
}

# Reduce sample size for faster execution
SAMPLE_SIZE_3D = 500
```

---

## Thesis Publication Example

**Goal**: Generate high-quality static images for thesis

```python
SOURCE_WORKFLOW = "workflow_data/Policy_Slavdict_FT-slavery_slavery_v1"

COMPARE_MODELS = {
    'base_cosine': True,
    'pretrained_bertje': True,
    'slavery_trained': False,
    'policy_trained': True
}

MODEL_PATHS = {
    'pretrained_bertje': 'GroNLP/bert-base-dutch-cased',
    'slavery_trained': None,
    'policy_trained': 'workflow_data/Policy_Slavdict_FT-slavery_slavery_v1/Model_finetuning/trained_encoder'
}

METADATA_FILTERS = {
    'doc_type': None,
    'year_range': None,
    'doc_folder': None
}

# Publication settings
MIN_SCORE_THRESHOLD = 0.3
TOP_N_SHIFTERS = 100
SAMPLE_SIZE_3D = 1000
PCA_RANDOM_STATE = 42
FIGURE_DPI = 300              # Higher DPI for publication quality

# Enable static exports
SAVE_INTERACTIVE = True       # Keep HTML for exploration
SAVE_STATIC = True            # Generate PNG for thesis
SHOW_IN_NOTEBOOK = True
```

**Prerequisites**: Install kaleido first:
```bash
pip install kaleido
```

---

## Quick Testing Example

**Goal**: Fast test run with minimal models and small sample

```python
SOURCE_WORKFLOW = "workflow_data/Policy_Slavdict_FT-slavery_slavery_v1"

# Only base cosine - no model loading needed
COMPARE_MODELS = {
    'base_cosine': True,
    'pretrained_bertje': False,
    'slavery_trained': False,
    'policy_trained': False
}

MODEL_PATHS = {
    'pretrained_bertje': 'GroNLP/bert-base-dutch-cased',
    'slavery_trained': None,
    'policy_trained': None
}

METADATA_FILTERS = {
    'doc_type': None,
    'year_range': None,
    'doc_folder': None
}

# Small sample for speed
SAMPLE_SIZE_3D = 200
TOP_N_SHIFTERS = 20

SAVE_INTERACTIVE = True
SAVE_STATIC = False
SHOW_IN_NOTEBOOK = True
```

**Runtime**: ~5 minutes (no model loading)

---

## Common Pitfalls

### ❌ Wrong: Forgetting to set model paths
```python
COMPARE_MODELS = {
    'policy_trained': True    # Enabled
}

MODEL_PATHS = {
    'policy_trained': None    # But path is None!
}
```

**Error**: "policy_trained enabled but MODEL_PATHS['policy_trained'] is None"

### ✓ Correct: Set explicit path
```python
COMPARE_MODELS = {
    'policy_trained': True
}

MODEL_PATHS = {
    'policy_trained': 'workflow_data/Policy_Slavdict_FT-slavery_slavery_v1/Model_finetuning/trained_encoder'
}
```

---

### ❌ Wrong: Trying to auto-detect from SOURCE_WORKFLOW
```python
# This WON'T work anymore - models are not auto-detected
SOURCE_WORKFLOW = "workflow_data/Policy_Slavdict_FT-slavery_slavery_v1"
COMPARE_MODELS['policy_trained'] = True
MODEL_PATHS['policy_trained'] = None  # Expecting auto-detection - NO!
```

### ✓ Correct: Explicit path even if same as SOURCE_WORKFLOW
```python
SOURCE_WORKFLOW = "workflow_data/Policy_Slavdict_FT-slavery_slavery_v1"
COMPARE_MODELS['policy_trained'] = True
MODEL_PATHS['policy_trained'] = 'workflow_data/Policy_Slavdict_FT-slavery_slavery_v1/Model_finetuning/trained_encoder'
```

---

### ❌ Wrong: Relative path without consideration
```python
MODEL_PATHS['policy_trained'] = 'Model_finetuning/trained_encoder'
```

**May fail** if running from different directory.

### ✓ Correct: Use full path or path from notebook location
```python
# Option 1: Full path from repository root
MODEL_PATHS['policy_trained'] = 'workflow_data/Policy_Slavdict_FT-slavery_slavery_v1/Model_finetuning/trained_encoder'

# Option 2: Absolute path
MODEL_PATHS['policy_trained'] = '/full/absolute/path/to/Model_finetuning/trained_encoder'
```

---

## Path Resolution

The notebook handles paths as follows:

1. **SOURCE_WORKFLOW**:
   - If `None`: Uses current working directory
   - If relative: Resolved from current working directory
   - If absolute: Used as-is

2. **MODEL_PATHS** (policy_trained, slavery_trained):
   - If `None`: Model disabled with warning
   - If relative: Resolved from current working directory
   - If absolute: Used as-is
   - **NOT** auto-detected from SOURCE_WORKFLOW

3. **Output** (Visuals/):
   - Created inside SOURCE_WORKFLOW directory
   - Auto-created if doesn't exist

---

## Verification Checklist

Before running, verify:

- [ ] `SOURCE_WORKFLOW` points to directory with `Dictionary/` and `Cosine_labeling/`
- [ ] If `COMPARE_MODELS['policy_trained'] = True`, then `MODEL_PATHS['policy_trained']` is set
- [ ] If `COMPARE_MODELS['slavery_trained'] = True`, then `MODEL_PATHS['slavery_trained']` is set
- [ ] Paths in `MODEL_PATHS` actually exist (check with file explorer)
- [ ] Model folders contain required files (config.json, pytorch_model.bin, tokenizer files)
- [ ] For `SAVE_STATIC = True`, kaleido is installed

---

**Ready to configure and run!** 🚀
