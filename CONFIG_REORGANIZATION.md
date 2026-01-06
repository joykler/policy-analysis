# CONFIG Cell Reorganization Summary

## Date: 2025-12-15

## Problem

Cell 5 (CONFIG) had become bloated and disorganized:
- **2,377 lines** (way too long)
- Duplicate sections
- Settings scattered across file
- Hard to find specific options
- Mixed configuration with derived paths

---

## Solution

Completely reorganized CONFIG into clean, logical sections:

### New Structure (237 lines - 90% reduction!)

```python
# ============================================================
# 1. WORKFLOW IDENTIFICATION
# ============================================================
WORKFLOW_NAME = "Policy_Slavdict_FT-slavery_slavery_v1"
# ... workflow setup

# ============================================================
# 2. MAIN CONFIGURATION
# ============================================================
CONFIG = {
    # ======================
    # FILE PATHS
    # ======================
    "paths": {
        "corpus_folder": "PolicyArchive",
        "dictionary_excel": r"C:\...\A___problem_oriented_legacy_seed_v10_4topics.xlsx",
        # ...
    },

    # ======================
    # CORPUS SETTINGS
    # ======================
    "corpus": {
        "mode": "documents",
        "preprocessing": { ... },
    },

    # ======================
    # CHUNKING SETTINGS
    # ======================
    "chunking": {
        "use_token_aware": True,      # Token-aware chunking
        "max_tokens": 500,             # Max tokens per chunk
        "sentences_per_chunk": 30,     # Fallback
        "min_sentences_to_keep": 3,
    },

    # ======================
    # PDF PROCESSING
    # ======================
    "pdf_processing": { ... },

    # ======================
    # VOCABULARY SETTINGS
    # ======================
    "vocab": { ... },

    # ======================
    # TOKENIZATION
    # ======================
    "tokenize": { ... },

    # ======================
    # DICTIONARY EXPANSION (DISABLED)
    # ======================
    "expand": {
        "k_nearest": 0,               # Disabled for cross-encoder
        "topN_per_topic": 0,          # No expansion
        "min_cosine": 0.55,
    },

    # ======================
    # CROSS-ENCODER SETTINGS
    # ======================
    "cross_encoder": {
        "model_name": "GroNLP/bert-base-dutch-cased",
        "batch_size": 32,             # Batch processing
        "max_length": 512,
        "device": "cuda",
    },

    # ======================
    # SCORING SETTINGS
    # ======================
    "scoring": {
        "use_sif": False,             # Disabled for cross-encoder
        "high_confidence_score": 0.40,
        # ...
    },

    # ======================
    # TERM WEIGHTING
    # ======================
    "weights": {
        "weighting_scheme": "seed_only",  # Use seed weights only
        "default_core_weight": 1.0,
        "default_discovered_weight": 0.7,
    },

    # ======================
    # TRAINING DATA SAMPLING
    # ======================
    "sampling": { ... },

    # ======================
    # MODEL TRAINING
    # ======================
    "training": { ... },
}

# ============================================================
# 3. DERIVED PATHS (AUTO-COMPUTED)
# ============================================================
# All paths derived from CONFIG
# ...

# ============================================================
# 4. CONFIGURATION SUMMARY
# ============================================================
print("="*60)
print("CONFIGURATION LOADED")
print("="*60)
print(f"Workflow: {WORKFLOW_NAME}")
print(f"Dictionary: {dict_path.name}")
# ... print summary
```

---

## Key Improvements

### 1. Clear Section Headers
```python
# ======================
# CHUNKING SETTINGS
# ======================
```
Easy to find what you need with visual separators.

### 2. Grouped Related Settings

**Before:** Settings scattered everywhere
```python
"use_token_aware": True,  # line 45
...
"max_tokens": 500,         # line 892
...
"sentences_per_chunk": 30, # line 1523
```

**After:** All chunking settings together
```python
"chunking": {
    "use_token_aware": True,
    "max_tokens": 500,
    "sentences_per_chunk": 30,
    "min_sentences_to_keep": 3,
},
```

### 3. Inline Comments
Every setting has a comment explaining its purpose:
```python
"use_token_aware": True,      # Respects max_tokens limit
"max_tokens": 500,             # Max tokens per chunk (for BERT input)
"batch_size": 32,              # Score 32 chunk-term pairs at once
```

### 4. Removed Duplicates
- Eliminated duplicate `pdf_processing` sections
- Consolidated scattered imports
- Removed redundant comments

### 5. Configuration Summary
Added printout when cell runs:
```
============================================================
CONFIGURATION LOADED
============================================================
Workflow: Policy_Slavdict_FT-slavery_slavery_v1
Dictionary: A___problem_oriented_legacy_seed_v10_4topics.xlsx
Corpus: PolicyArchive

Key Settings:
  • Chunking: Token-aware (500 tokens)
  • Expansion: Disabled (using v10 only)
  • Cross-encoder: GroNLP/bert-base-dutch-cased
  • Batch size: 32
  • Device: cuda
  • SIF weighting: Disabled
  • Term weighting: seed_only
============================================================
```

---

## Configuration Sections

### Core Settings (Always Adjust)

1. **File Paths**
   - Corpus folder
   - Dictionary path
   - Workflow name

2. **Chunking**
   - Token-aware vs sentence-based
   - Max tokens
   - Minimum sentences

3. **Cross-Encoder**
   - Model selection
   - Batch size (speed/memory trade-off)
   - Device (cuda/cpu)

4. **Expansion**
   - Disabled for v10 (curated terms only)
   - Can enable if needed

5. **Scoring**
   - SIF disabled (cross-encoder learns weights)
   - Confidence thresholds

6. **Weighting**
   - seed_only (no corpus statistics)
   - Core vs discovered term weights

### Advanced Settings (Usually Keep Default)

7. **PDF Processing**
   - Page filtering rules
   - OCR fallback
   - Layout detection

8. **Vocabulary**
   - Min/max document frequency
   - Vocab size limits

9. **Tokenization**
   - Lowercasing, hyphen handling
   - Character patterns

10. **Sampling**
    - Unlabeled/pseudo-label ratios

11. **Training**
    - Epochs, batch size, learning rate
    - Dataset option selection

---

## How to Use

### Quick Reference: Key Settings

```python
# To change dictionary:
"dictionary_excel": r"C:\path\to\your_dictionary.xlsx"

# To adjust speed:
"cross_encoder": {
    "batch_size": 32,  # Higher = faster (if GPU memory allows)
}

# To disable token-aware chunking:
"chunking": {
    "use_token_aware": False,
    "sentences_per_chunk": 30,  # Will use this instead
}

# To enable expansion:
"expand": {
    "k_nearest": 50,
    "topN_per_topic": 20,  # Smaller than default
}

# To use CPU instead of GPU:
"cross_encoder": {
    "device": "cpu",
}
```

---

## Benefits

### Before Reorganization:
- ❌ 2,377 lines (scroll forever)
- ❌ Duplicate sections
- ❌ Hard to find settings
- ❌ No overview of configuration
- ❌ Mixed config and code

### After Reorganization:
- ✅ 237 lines (90% reduction)
- ✅ No duplicates
- ✅ Clear section headers
- ✅ Configuration summary printout
- ✅ Clean separation: config → derived paths → code

---

## Verification

After reorganization, when you run Cell 5, you'll see:

```
============================================================
CONFIGURATION LOADED
============================================================
Workflow: Policy_Slavdict_FT-slavery_slavery_v1
Dictionary: A___problem_oriented_legacy_seed_v10_4topics.xlsx
Corpus: PolicyArchive

Key Settings:
  • Chunking: Token-aware (500 tokens)
  • Expansion: Disabled (using v10 only)
  • Cross-encoder: GroNLP/bert-base-dutch-cased
  • Batch size: 32
  • Device: cuda
  • SIF weighting: Disabled
  • Term weighting: seed_only
============================================================
```

This confirms all key settings at a glance!

---

## File Modified

- ✅ [A__dictionary_discovery_v23_policy_crossencoder.ipynb](A__dictionary_discovery_v23_policy_crossencoder.ipynb)
  - Cell 5: Completely reorganized (2,377 → 237 lines)

## Files Created

- ✅ [reorganize_config_cell5.py](reorganize_config_cell5.py) - Reorganization script
- ✅ [CONFIG_REORGANIZATION.md](CONFIG_REORGANIZATION.md) - This documentation

---

## Related Documentation

- [SCORING_OPTIMIZATION_SUMMARY.md](SCORING_OPTIMIZATION_SUMMARY.md) - Batching and expansion disable
- [TOKEN_AWARE_CHUNKING_INTEGRATION.md](TOKEN_AWARE_CHUNKING_INTEGRATION.md) - Token-aware chunking
- [CHECKPOINT_4_5_FIXES_SUMMARY.md](CHECKPOINT_4_5_FIXES_SUMMARY.md) - Cross-encoder setup

---

**Status**: ✅ CONFIG Reorganized

Cell 5 is now clean, well-structured, and 90% shorter. All settings are easy to find and understand!
