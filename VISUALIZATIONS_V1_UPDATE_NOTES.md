# A___Visualizations_v1 - Update Notes

## Update: Explicit Model Path Configuration

**Date**: 2026-01-04
**Issue**: Original version tried to auto-detect trained models from SOURCE_WORKFLOW
**Problem**: Trained models can be in different workflow directories than the data source
**Solution**: Now requires explicit paths for all trained models

---

## What Changed

### Cell 1 (Configuration)

#### Before:
```python
MODEL_PATHS = {
    'pretrained_bertje': 'GroNLP/bert-base-dutch-cased',
    'slavery_trained': None,      # Auto-detect or set custom path
    'policy_trained': None        # Auto-detect from SOURCE_WORKFLOW
}
```

- Models would auto-detect from `SOURCE_WORKFLOW/Model_finetuning/`
- Assumed models are in the same workflow as data

#### After:
```python
MODEL_PATHS = {
    'pretrained_bertje': 'GroNLP/bert-base-dutch-cased',  # HuggingFace model

    # SET THIS to your slavery-trained model path
    'slavery_trained': None,

    # SET THIS to your policy-trained model path
    'policy_trained': None
}

# Example configuration:
# MODEL_PATHS = {
#     'pretrained_bertje': 'GroNLP/bert-base-dutch-cased',
#     'slavery_trained': 'workflow_data/slavery_Slavdict_pretraining_slavery_v13/Model_finetuning/slavery_domain_encoder',
#     'policy_trained': 'workflow_data/Policy_Slavdict_FT-slavery_slavery_v1/Model_finetuning/trained_encoder'
# }
```

- **NO auto-detection** - must explicitly set paths
- Models can be from **ANY** workflow directory
- Clear example provided in comments

---

### Cell 7 (Model Loading)

#### Before:
```python
if MODEL_PATHS['policy_trained'] is not None:
    policy_path = Path(MODEL_PATHS['policy_trained'])
else:
    # Auto-detect from source_fs
    policy_path = source_fs.folders.get('Model_finetuning') / 'trained_encoder'
```

#### After:
```python
if MODEL_PATHS['policy_trained'] is not None:
    policy_path = Path(MODEL_PATHS['policy_trained'])
    if not policy_path.is_absolute():
        policy_path = Path.cwd() / policy_path
else:
    policy_path = None
    print(f"   ⚠ policy_trained enabled but MODEL_PATHS['policy_trained'] is None")
    print(f"   Set MODEL_PATHS['policy_trained'] to exact path in Cell 1")
    COMPARE_MODELS['policy_trained'] = False
```

- **NO auto-detection fallback**
- Clear error message if path not set
- Automatically disables model if path missing
- Handles relative paths from current directory

---

## Why This Change?

### Original Design Issue:
1. SOURCE_WORKFLOW points to data (Dictionary, Cosine scores)
2. But trained models might be from different workflow runs
3. Example real scenario:
   - Data from: `Policy_Slavdict_FT-slavery_slavery_v1`
   - Slavery model from: `slavery_Slavdict_pretraining_slavery_v13`
   - Policy model from: `Policy_Slavdict_FT-slavery_slavery_v1`

### With Auto-detection:
- Would only look in `Policy_Slavdict_FT-slavery_slavery_v1/Model_finetuning/`
- Couldn't access `slavery_Slavdict_pretraining_slavery_v13` model
- Confusing where models should be

### With Explicit Paths:
- User specifies exact location of each model
- Models can be from any workflow
- Clear separation: data source vs. model source
- More flexible for comparing different training runs

---

## Migration Guide

### If you used the old version:

#### Old configuration:
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
    'policy_trained': None  # Auto-detected
}
```

#### New configuration:
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

    # ADD THIS - explicit path to policy-trained model
    'policy_trained': 'workflow_data/Policy_Slavdict_FT-slavery_slavery_v1/Model_finetuning/trained_encoder'
}
```

**Action Required**: Add explicit path for `policy_trained` (and `slavery_trained` if you have it)

---

## Benefits

### 1. Flexibility
```python
# Data from v1, models from different workflows
SOURCE_WORKFLOW = "workflow_data/Policy_Slavdict_FT-slavery_slavery_v1"

MODEL_PATHS = {
    'slavery_trained': 'workflow_data/slavery_Slavdict_pretraining_slavery_v13/Model_finetuning/slavery_domain_encoder',
    'policy_trained': 'workflow_data/Policy_Slavdict_FT-slavery_slavery_v2/Model_finetuning/trained_encoder'
}
```

### 2. Clarity
- No ambiguity about where models come from
- Explicit is better than implicit
- Easy to see all sources at a glance

### 3. Comparison Scenarios
```python
# Compare same data with different training runs
SOURCE_WORKFLOW = "workflow_data/Policy_Slavdict_FT-slavery_slavery_v1"

# Run 1: Compare v1 and v2 policy models
MODEL_PATHS['policy_trained'] = '.../Policy_Slavdict_FT-slavery_slavery_v1/Model_finetuning/trained_encoder'

# Run 2: Change to v2
MODEL_PATHS['policy_trained'] = '.../Policy_Slavdict_FT-slavery_slavery_v2/Model_finetuning/trained_encoder'
```

### 4. Error Prevention
- If path wrong, immediate clear error message
- No silent failures or unexpected behavior
- Validates paths exist before model loading

---

## Backwards Compatibility

**Breaking Change**: Yes - old configurations will NOT work

**Error Message**: If you enable a model but don't set its path:
```
⚠ policy_trained enabled but MODEL_PATHS['policy_trained'] is None
Set MODEL_PATHS['policy_trained'] to exact path in Cell 1
```

**Fix**: Simply add the model path in Cell 1 configuration

---

## Example Use Cases

### Use Case 1: Standard Single Workflow
```python
SOURCE_WORKFLOW = "workflow_data/Policy_Slavdict_FT-slavery_slavery_v1"
MODEL_PATHS['policy_trained'] = "workflow_data/Policy_Slavdict_FT-slavery_slavery_v1/Model_finetuning/trained_encoder"
```

### Use Case 2: Cross-Workflow Comparison
```python
SOURCE_WORKFLOW = "workflow_data/Policy_Slavdict_FT-slavery_slavery_v1"
MODEL_PATHS['slavery_trained'] = "workflow_data/slavery_Slavdict_pretraining_slavery_v13/Model_finetuning/slavery_domain_encoder"
MODEL_PATHS['policy_trained'] = "workflow_data/Policy_Slavdict_FT-slavery_slavery_v1/Model_finetuning/trained_encoder"
```

### Use Case 3: Model Comparison Study
```python
# Data stays the same
SOURCE_WORKFLOW = "workflow_data/Policy_Slavdict_FT-slavery_slavery_v1"

# Compare different policy-trained versions
# Iteration 1:
MODEL_PATHS['policy_trained'] = "workflow_data/Finetuned_Slavery-Slavery-policy_11.01.25_v1/Model_finetuning/trained_encoder"

# Iteration 2:
MODEL_PATHS['policy_trained'] = "workflow_data/Finetuned_Slavery-Slavery-policy_11.01.25_v2/Model_finetuning/trained_encoder"
```

---

## Files Updated

1. **A___Visualizations_v1.ipynb**
   - Cell 1: Configuration (MODEL_PATHS section rewritten)
   - Cell 7: Model loading (removed auto-detection)

2. **VISUALIZATIONS_V1_README.md**
   - Quick Start section updated
   - Troubleshooting section expanded
   - Required Data Files section clarified

3. **VISUALIZATIONS_V1_EXAMPLE_CONFIG.md** (NEW)
   - Multiple example configurations
   - Common pitfalls explained
   - Migration guide

4. **VISUALIZATIONS_V1_UPDATE_NOTES.md** (this file)
   - Documents the change
   - Explains rationale
   - Provides migration path

---

## Testing Checklist

Before running updated notebook:

- [ ] Set `SOURCE_WORKFLOW` to data location
- [ ] If using policy_trained: Set `MODEL_PATHS['policy_trained']` to exact path
- [ ] If using slavery_trained: Set `MODEL_PATHS['slavery_trained']` to exact path
- [ ] Verify paths exist on filesystem
- [ ] Check model folders contain: config.json, pytorch_model.bin, tokenizer files
- [ ] Run Cell 1 and verify no warnings
- [ ] Run Cell 2 (filesystem setup) and verify all folders found

---

**Updated and ready to use!** ✅
