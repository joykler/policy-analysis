# Dictionary Discovery Workflow v3 - Complete Guide

## Overview

This is the complete implementation guide for the structured dictionary discovery workflow with systematic file saving.

## Folder Structure

```
workflow_data/
  {ModelType}-{Topic}_{Date}_{Version}/
    ├── config/
    │   └── config_{checkpoint}_{timestamp}.json
    ├── Dictionary/
    │   ├── input_dictionary.xlsx (copy of original)
    │   ├── expanded_candidates.csv
    │   ├── curated_dictionary.csv
    │   └── Dictionary_suggestions/
    │       ├── {Topic1}_suggestions.csv
    │       ├── {Topic2}_suggestions.csv
    │       └── ...
    ├── Model_finetuning/
    │   ├── pytorch_model.bin (trained model files)
    │   ├── config.json
    │   ├── training_metrics.json
    │   ├── train_data_option{N}.csv
    │   └── val_data.csv
    ├── Cosine_labeling/
    │   ├── scores_high_confidence.csv
    │   ├── scores_low_confidence.csv
    │   ├── scores_no_confidence.csv
    │   └── scores_all_labeled.csv
    ├── Bertje_labeling/
    │   └── predictions_on_corpus.csv
    ├── Visuals/
    │   ├── topic_clustering.html
    │   ├── topic_distribution.html
    │   ├── confidence_analysis.html
    │   └── training_metrics.html
    └── Other_data/
        ├── chunked_corpus.csv
        ├── vocabulary.csv
        ├── term_frequencies.json
        ├── topic_vectors.npy
        └── topic_vectors_meta.json
```

## Folder Naming Convention

Format: `{ModelType}-{Topic}_{MM.DD.YY}_{Version}`

### Examples:
- `Pretrained-Slavery_10.24.25_v1` - First run using pretrained model on slavery topics
- `Finetuned_Slavery-Policy_10.24.25_v1` - Model finetuned on slavery, applied to policy docs
- `Finetuned_Policy-Policy_10.25.25_v2` - Second version, policy model on policy docs

### Components:
1. **ModelType**:
   - `Pretrained` - Using base model without fine-tuning
   - `Finetuned_{source}` - Model fine-tuned on {source} topic

2. **Topic**:
   - Single: `Slavery`, `Policy`, `Reparations`
   - Combined: `Slavery-Policy`, `Policy-Reparations`

3. **Date**: `MM.DD.YY` format

4. **Version**: Auto-increments (`v1`, `v2`, `v3`) for same date

## Workflow Checkpoints

### CHECKPOINT 0: Initial Setup
**Purpose**: Create folder structure, load configuration, prepare dictionary

**Outputs**:
- `config/config_initial_setup_{timestamp}.json`
- `config/config_with_dictionary_{timestamp}.json`
- `Dictionary/input_dictionary.xlsx` (copy)

**Resume**: Start here for new workflow

---

### CHECKPOINT 1: Text Processing
**Purpose**: Load corpus, chunk into sentences, apply cleaning

**Inputs**:
- Corpus directory (txt files)
- Chunking configuration

**Outputs**:
- `Other_data/chunked_corpus.csv`
- `config/config_checkpoint1_chunks_{timestamp}.json`

**Resume**: Skip if you have `chunked_corpus.csv`

**Key Settings**:
```python
CONFIG["chunking"] = {
    "sentences_per_chunk": 10,
    "min_sentences_to_keep": 3,
    "drop_likely_english": True,
    "remove_stopwords": True,
    "use_stemming": False,
}
```

---

### CHECKPOINT 2: Vocabulary Building
**Purpose**: Build vocabulary from corpus with frequency filtering

**Inputs**:
- `Other_data/chunked_corpus.csv`

**Outputs**:
- `Other_data/vocabulary.csv`
- `Other_data/term_frequencies.json`
- `config/config_checkpoint2_vocab_{timestamp}.json`

**Resume**: Skip if you have `vocabulary.csv`

**Key Settings**:
```python
CONFIG["vocab"] = {
    "min_df": 5,          # Minimum document frequency
    "max_vocab": 50000,   # Maximum vocabulary size
}
```

---

### CHECKPOINT 3: Dictionary Expansion
**Purpose**: Expand seed terms using semantic similarity

**Inputs**:
- `Dictionary/input_dictionary.xlsx`
- `Other_data/vocabulary.csv`
- Sentence transformer model

**Outputs**:
- `Dictionary/expanded_candidates.csv`
- `config/config_checkpoint3_expansion_{timestamp}.json`

**⚠️ MANUAL CURATION REQUIRED**:
1. Review `Dictionary/expanded_candidates.csv`
2. Remove irrelevant terms
3. Save as `Dictionary/curated_dictionary.csv`
4. Proceed to CHECKPOINT 4

**Key Settings**:
```python
CONFIG["expand"] = {
    "k_nearest": 50,          # Nearest neighbors to check
    "topN_per_topic": 300,    # Max terms per topic
    "min_cosine": 0.55,       # Minimum similarity threshold
}
```

---

### CHECKPOINT 4: Topic Vector Creation
**Purpose**: Build weighted topic vectors from curated dictionary

**Inputs**:
- `Dictionary/curated_dictionary.csv`
- `Other_data/vocabulary.csv`
- `Other_data/term_frequencies.json`

**Outputs**:
- `Other_data/topic_vectors.npy`
- `Other_data/topic_vectors_meta.json`
- `Dictionary/Dictionary_suggestions/{topic}_suggestions.csv` (per topic)
- `config/config_checkpoint4_vectors_{timestamp}.json`

**Resume**: Skip if you have `topic_vectors.npy`

**Key Settings**:
```python
CONFIG["scoring"] = {
    "use_sif": True,      # Use SIF weighting
    "sif_a": 1e-3,        # SIF parameter
}
```

---

### CHECKPOINT 5: Chunk Scoring & Confidence Classification
**Purpose**: Score all chunks, classify by confidence level

**Inputs**:
- `Other_data/chunked_corpus.csv`
- `Other_data/topic_vectors.npy`

**Outputs**:
- `Cosine_labeling/scores_high_confidence.csv`
- `Cosine_labeling/scores_low_confidence.csv`
- `Cosine_labeling/scores_no_confidence.csv`
- `Cosine_labeling/scores_all_labeled.csv`
- `config/config_checkpoint5_scoring_{timestamp}.json`

**Resume**: Skip if you have scoring CSVs

**Confidence Thresholds**:
```python
CONFIG["scoring"] = {
    # HIGH CONFIDENCE (for training)
    "high_confidence_score": 0.50,    # Min score
    "high_confidence_margin": 0.05,   # Min margin between top 2

    # LOW CONFIDENCE (pseudo-labels)
    "low_confidence_score": 0.40,
    "low_confidence_margin": 0.02,
}
```

**Classification Logic**:
- **High**: score ≥ 0.50 AND margin ≥ 0.05 → Core examples for training
- **Low**: score ≥ 0.40 AND margin ≥ 0.02 → Pseudo-labels for semi-supervised
- **None**: Below thresholds → Unlabeled data for boundary learning

---

### CHECKPOINT 6: Training Data Preparation
**Purpose**: Create train/val splits from confidence tiers

**Inputs**:
- `Cosine_labeling/scores_*.csv`

**Outputs**:
- `Model_finetuning/bertje_label_mapping.json`
- `Model_finetuning/val_data.csv`
- `Model_finetuning/train_data_option1.csv` (high confidence only)
- `Model_finetuning/train_data_option2.csv` (high + unlabeled)
- `Model_finetuning/train_data_option3.csv` (high + low)
- `Model_finetuning/train_data_option4.csv` (high + low + unlabeled - RECOMMENDED)
- `config/config_checkpoint6_training_prep_{timestamp}.json`

**Resume**: Skip if you have training data CSVs

**Dataset Options**:
1. **Option 1** (High confidence only): Standard supervised learning
2. **Option 2** (High + Unlabeled): Semi-supervised with hard boundaries
3. **Option 3** (High + Low): Pseudo-labeling for fuzzy boundaries
4. **Option 4** (All three) ⭐ RECOMMENDED: Complete spectrum learning

---

### CHECKPOINT 7: Model Training (BERTJE)
**Purpose**: Fine-tune Dutch BERT on labeled data

**Inputs**:
- `Model_finetuning/train_data_option{N}.csv`
- `Model_finetuning/val_data.csv`
- `Model_finetuning/bertje_label_mapping.json`

**Outputs**:
- `Model_finetuning/pytorch_model.bin`
- `Model_finetuning/config.json`
- `Model_finetuning/tokenizer_config.json`
- `Model_finetuning/training_metrics.json`
- `Model_finetuning/logs/` (training logs)
- `config/config_checkpoint7_trained_{timestamp}.json`

**Resume**: Skip if you have trained model

**Training Settings**:
```python
CONFIG["training"] = {
    "num_epochs": 3,
    "batch_size_train": 16,
    "batch_size_eval": 32,
    "learning_rate": 2e-5,
    "weight_decay": 0.01,
    "warmup_ratio": 0.1,
    "dataset_option": "option4",  # Which dataset to use
}
```

---

### CHECKPOINT 8: Visualizations
**Purpose**: Generate interactive visualizations and analysis

**Inputs**:
- `Cosine_labeling/scores_all_labeled.csv`
- `Model_finetuning/training_metrics.json` (if available)

**Outputs**:
- `Visuals/topic_clustering_2d.html`
- `Visuals/topic_clustering_3d.html`
- `Visuals/topic_distribution.html`
- `Visuals/confidence_analysis.html`
- `Visuals/training_metrics.html` (if model trained)
- `config/config_checkpoint8_visuals_{timestamp}.json`

**Resume**: Run anytime after scoring

---

## Loading Pretrained Models

To use a previously fine-tuned model in a new workflow:

```python
CONFIG["model"] = {
    "base_model_name": "NetherlandsForensicInstitute/robbert-2022-dutch-sentence-transformers",
    "use_pretrained": True,
}

CONFIG["paths"]["pretrained_model_path"] = "/path/to/workflow_data/Finetuned_Slavery-Slavery_10.24.25_v1/Model_finetuning"

CONFIG["workflow"]["model_type"] = "Finetuned_Slavery"  # Indicate source of fine-tuning
```

The model will be loaded in the expansion phase and used for:
- Dictionary expansion (better semantic understanding)
- Chunk scoring (domain-specific embeddings)

---

## Complete Workflow Example

### New Workflow from Scratch

1. **Configure** (`CHECKPOINT 0`)
   ```python
   CONFIG["workflow"]["model_type"] = "Pretrained"
   CONFIG["workflow"]["topic"] = "Slavery"
   CONFIG["paths"]["corpus_dir"] = "/path/to/slavery/texts"
   CONFIG["paths"]["dictionary_excel"] = "/path/to/dictionary.xlsx"
   ```

2. **Run CHECKPOINT 0**: Setup folders, load dictionary

3. **Run CHECKPOINT 1**: Process corpus → `chunked_corpus.csv`

4. **Run CHECKPOINT 2**: Build vocabulary → `vocabulary.csv`

5. **Run CHECKPOINT 3**: Expand dictionary → `expanded_candidates.csv`
   - **STOP HERE**: Manually review and curate
   - Save as `curated_dictionary.csv`

6. **Run CHECKPOINT 4**: Build topic vectors → `topic_vectors.npy`

7. **Run CHECKPOINT 5**: Score chunks → confidence tier CSVs

8. **Run CHECKPOINT 6**: Prepare training data → train/val CSVs

9. **Run CHECKPOINT 7**: Train model → trained model in `Model_finetuning/`

10. **Run CHECKPOINT 8**: Generate visualizations

### Using Trained Model on New Data

1. **Configure** (`CHECKPOINT 0`)
   ```python
   CONFIG["workflow"]["model_type"] = "Finetuned_Slavery"
   CONFIG["workflow"]["topic"] = "Policy"  # New topic
   CONFIG["model"]["use_pretrained"] = True
   CONFIG["paths"]["pretrained_model_path"] = "/path/to/previous/Model_finetuning"
   CONFIG["paths"]["corpus_dir"] = "/path/to/policy/texts"
   ```

2. **Run CHECKPOINTS 0-5**: Process with fine-tuned model

3. **Optional**: Run CHECKPOINT 6-7 if you want to further fine-tune on new domain

4. **Run CHECKPOINT 8**: Visualize results

---

## File System API

The `WorkflowFileSystem` class provides systematic file management:

```python
# Initialize
fs = WorkflowFileSystem(CONFIG)

# Create new workflow
workflow_root = fs.create_workflow_folder()

# Or load existing
workflow_root = fs.load_existing_workflow("/path/to/folder")

# Save configuration at any checkpoint
fs.save_config("checkpoint_name")

# Save data to specific folder
fs.save_data(
    data=dataframe,
    filename="my_data",
    folder_key="Other_data",  # or "Dictionary", "Cosine_labeling", etc.
    file_format="csv"  # or "json", "npy"
)

# Copy external file to workflow folder
fs.copy_file_to_folder(
    source_path="/path/to/file.xlsx",
    folder_key="Dictionary",
    new_name="input_dictionary.xlsx"
)
```

**Available folder keys**:
- `config`
- `Dictionary`
- `Dictionary_suggestions`
- `Model_finetuning`
- `Cosine_labeling`
- `Bertje_labeling`
- `Visuals`
- `Other_data`

---

## Best Practices

### 1. Version Control
- Use version numbers for iterations on same date
- Document changes in config files
- Keep previous versions for comparison

### 2. Manual Curation
- Always review expanded candidates before training
- Remove domain-specific noise
- Check for topic drift
- Balance topics (similar number of keywords)

### 3. Training Strategy
- Start with Option 1 (supervised baseline)
- Compare with Option 4 (comprehensive)
- Monitor F1 scores per topic for imbalance
- Use Option 4 for production (best boundary learning)

### 4. Resuming Workflows
- Check `Other_data/` for existing preprocessed files
- Load latest config from `config/` folder
- Skip completed checkpoints
- Always save config after manual steps

### 5. File Organization
- All inputs copied to workflow folder (reproducibility)
- Never modify original corpus
- Keep curated dictionary separate from candidates
- Log all manual decisions in config notes

---

## Troubleshooting

### Out of Memory during Training
- Reduce `batch_size_train` (try 8 or 4)
- Reduce vocabulary size
- Process corpus in batches

### Poor Topic Separation
- Lower `min_cosine` for more diverse candidates
- Increase `high_confidence_margin` for stricter labeling
- Review seed keywords for overlap
- Balance training data across topics

### Model Not Learning
- Check F1 scores per topic (imbalance?)
- Verify training data has enough examples (min 50 per topic)
- Try higher `num_epochs` (up to 10)
- Check for topic ambiguity in manual review

### Checkpoint Recovery
```python
# Find latest checkpoint
import glob
configs = sorted(glob.glob(f"{workflow_root}/config/config_*.json"))
latest_config = configs[-1]

# Load it
with open(latest_config) as f:
    saved_config = json.load(f)

# Resume from there
CONFIG = saved_config["config"]
```

---

## Migration from v2

The v2 workflow saved files in:
```
Model_iterations/
  {Prefix}_{Version}/
    configs/
    processed_data/
```

To migrate:
1. Copy relevant files to new structure
2. Update config paths
3. Re-run checkpoints as needed

**Key changes from v2**:
- Clearer folder naming with model type and date
- Separate folders for different output types
- Systematic checkpoint system
- File system API for consistent saving
- Better separation of concerns (scoring vs training vs visuals)

---

## Summary

This structured workflow provides:
✅ **Reproducibility**: All inputs saved with outputs
✅ **Traceability**: Config snapshots at every checkpoint
✅ **Flexibility**: Resume at any checkpoint
✅ **Clarity**: Named folders for different data types
✅ **Scalability**: Easy to iterate and compare versions
✅ **Maintainability**: Systematic file management API

Next: Use the Jupyter notebook `Dictionary_discovery_v3_structured.ipynb` to execute the workflow!
