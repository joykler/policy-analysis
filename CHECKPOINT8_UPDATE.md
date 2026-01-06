# Checkpoint 8 Update: Continuous Multi-Label Architecture

**Date**: 2025-12-09
**Updated**: Cells 66-71 in `A__dictionary_discovery_v20_unified_embedding.ipynb`

---

## What Changed

### **OLD Checkpoint 8** (v19 and earlier)
- Expected ordinal classification model (3 classes per topic)
- Loaded from `continuous_regression_model/` directory
- Used sigmoid outputs and threshold-based classification
- Output: Ordinal classes (0=Low, 1=Medium, 2=High)

### **NEW Checkpoint 8** (v20)
- Uses continuous multi-label regression model from Checkpoint 7
- Loads from `full_model/` directory (standard HuggingFace format)
- No sigmoid in model (raw regression outputs, clamped [0-10] at inference)
- Output: Continuous scores matching dot product range

---

## Architecture Changes

### Model Definition

**OLD**:
```python
# Sigmoid in forward pass
pred = torch.sigmoid(head(sentence_embedding))  # [0, 1]
```

**NEW**:
```python
# No sigmoid, clamp at inference only
pred = head(sentence_embedding)  # Unbounded during training

# In forward():
if not self.training:
    logits = torch.clamp(logits, 0.0, 10.0)  # Match dot product range
```

### Loading Process

**OLD**:
```python
# Looking for specific continuous_regression_model structure
model_save_path = model_dir / 'continuous_regression_model'
metadata_path = model_dir / 'continuous_model_metadata.json'
```

**NEW**:
```python
# Load from standard full_model structure (from Checkpoint 7)
full_model_path = model_dir / 'full_model'
model_config_path = full_model_path / 'model_config.json'

# Load model config
with open(model_config_path, 'r') as f:
    model_config = json.load(f)

# Instantiate and load weights
bertje_model = SBERTContinuousMultiLabel(
    model_name=model_config['base_model'],
    num_topics=model_config['num_topics']
)
state_dict = torch.load(full_model_path / 'pytorch_model.bin')
bertje_model.load_state_dict(state_dict)
```

---

## Cell-by-Cell Breakdown

### **Cell 66** (8.1): Setup & Architecture
- Import dependencies
- Define `SBERTContinuousMultiLabel` class
- **Key change**: No sigmoid, clamp at inference only
- Output range: [0, 10] to match dot product scores

### **Cell 67** (8.2): Load Trained Model
- Load from `full_model/` directory
- Read `model_config.json` for configuration
- Load `pytorch_model.bin` for weights
- Load tokenizer
- **Key change**: Uses standard HF structure from Checkpoint 7

### **Cell 68** (8.3): Load Corpus
- Load `chunked_corpus.csv` from workflow
- Prepare texts for model
- Handle `text_for_scoring` or `raw_text` columns

### **Cell 69** (8.4): Predict on Corpus
- Batch prediction with progress bar
- **Output**: Continuous scores [0-10] per topic
- Calculate statistics per topic (mean, std, quantiles)
- **Derived metrics**:
  - `bertje_primary_topic` (argmax)
  - `bertje_max_score`
  - `bertje_score_margin`
  - `bertje_cv` (coefficient of variation - differentiation)
- **Confidence classification**: 4-tier (high, medium, low, very_low)

### **Cell 70** (8.5): Save Results
- Save full labeled corpus
- Create confidence-split files (4 tiers)
- Create per-topic files (high confidence only)
- Save summary statistics JSON

---

## Output Files

### Main Files

1. **`bertje_labeled_corpus.csv`**: Full corpus with BERTje labels
   - Original columns (filename, chunk_id, raw_text, etc.)
   - Per-topic scores: `bertje_score_Educational`, `bertje_score_Governance`, etc.
   - Derived metrics: `bertje_primary_topic`, `bertje_max_score`, `bertje_score_margin`, `bertje_cv`
   - `bertje_confidence`: 4-tier classification

2. **`bertje_labeling_summary.json`**: Statistics and metadata
   - Score distributions
   - Topic distributions
   - Confidence distributions
   - Thresholds used
   - Model information

### Confidence-Split Files

3. **`bertje_high_confidence.csv`**: High score + high margin + high CV
4. **`bertje_medium_confidence.csv`**: Above median score + decent margin
5. **`bertje_low_confidence.csv`**: Above bottom quartile
6. **`bertje_very_low_confidence.csv`**: Bottom quartile

### Per-Topic Files (High Confidence Only)

7. **`bertje_topic_Educational_high_conf.csv`**
8. **`bertje_topic_Governance_high_conf.csv`**
9. **`bertje_topic_Persistent_high_conf.csv`**
10. **`bertje_topic_Social_high_conf.csv`**

---

## Confidence Classification Logic

### 4-Tier System

**Thresholds** (calculated from data distribution):
- `score_p75`, `score_p50`, `score_p25` (primary score percentiles)
- `margin_p75`, `margin_p50` (margin percentiles)
- `cv_p75` (CV percentile)

**Classification**:

```python
def classify_confidence(row):
    score = row['bertje_primary_score']
    margin = row['bertje_score_margin']
    cv = row['bertje_cv']

    # High: top quartile score + top quartile margin + top quartile CV
    if score >= score_p75 and margin >= margin_p75 and cv >= cv_p75:
        return 'high'

    # Medium: above median score + decent margin
    elif score >= score_p50 and margin >= margin_p50:
        return 'medium'

    # Low: above bottom quartile
    elif score >= score_p25:
        return 'low'

    # Very low: bottom quartile
    else:
        return 'very_low'
```

**Rationale**:
- **High confidence**: Clear topic signal (high CV), strong score, good margin
- **Medium confidence**: Moderate signal, decent differentiation
- **Low confidence**: Weak signal, may need review
- **Very low confidence**: Ambiguous, likely noise or multi-topic

---

## Key Differences from Old Version

| Aspect | OLD (v19) | NEW (v20) |
|--------|-----------|----------|
| **Model Output** | Sigmoid [0, 1] | Raw scores [0-10] |
| **Model Loading** | `continuous_regression_model/` | `full_model/` (HF standard) |
| **Output Type** | Ordinal classes (0-2) | Continuous scores |
| **Confidence Tiers** | 5 levels (percentile-based) | 4 levels (score+margin+CV) |
| **Threshold Method** | Percentile only | Multi-factor (score, margin, CV) |
| **Per-Topic Files** | All confidence levels | High confidence only |
| **CV Metric** | Not included | Included (differentiation measure) |

---

## Usage Example

### Running Checkpoint 8

```python
# 1. Ensure Checkpoint 7 completed (model trained)
# 2. Run Cell 66 (Setup)
# 3. Run Cell 67 (Load Model)
# 4. Run Cell 68 (Load Corpus)
# 5. Run Cell 69 (Predict)
# 6. Run Cell 70 (Save Results)
```

### Expected Output

```
================================================================================
CHECKPOINT 8: LABEL FULL CORPUS WITH FINE-TUNED MODEL
================================================================================

✓ Transformers library available
✓ SBERTContinuousMultiLabel architecture defined

================================================================================
LOADING TRAINED MODEL
================================================================================
Device: cuda

📂 Loading from current workflow:
  C:\Users\Home\policy-analysis\workflow_data\slavery_Slavdict_pretraining_slavery_v25\Model_finetuning

✓ Found trained model
Model Configuration:
  Base model: GroNLP/bert-base-dutch-cased
  Topics: 4

Loading trained weights from: pytorch_model.bin
✓ Model loaded in evaluation mode

Topics (4):
  1. Educational Disadvantage & Brain Drain
  2. Governance Distrust & Corruption
  3. Persistent Poverty & Economic Vulnerability
  4. Social Fragmentation & Racism

================================================================================
LOADING CORPUS FOR LABELING
================================================================================
✓ Loaded corpus: 1520 chunks
✓ Prepared 1520 texts for labeling

================================================================================
GENERATING PREDICTIONS
================================================================================
Predicting on 1520 chunks...
Predicting: 100%|███████████████████| 48/48 [00:15<00:00,  3.14it/s]

✓ Prediction complete
  Shape: (1520, 4)
  Range: [2.34, 8.91]

Score distribution per topic:
  Educational:
    Mean: 5.12
    Std:  1.34
    Min:  2.34
    Q25:  4.23
    Med:  5.08
    Q75:  5.98
    Max:  8.91
  ...

✓ Added derived metrics:
  - bertje_primary_topic
  - bertje_max_score
  - bertje_score_margin
  - bertje_primary_score
  - bertje_cv (differentiation)

Calculating confidence tiers...
✓ Confidence distribution:
  high        245
  medium      512
  low         563
  very_low    200

================================================================================
SAVING LABELED CORPUS
================================================================================
✓ Saved labeled corpus:
  bertje_labeled_corpus.csv
  1520 chunks
  9 BERTje columns

✓ Confidence-split files:
  High:     bertje_high_confidence.csv (245 chunks, 16.1%)
  Medium:   bertje_medium_confidence.csv (512 chunks, 33.7%)
  Low:      bertje_low_confidence.csv (563 chunks, 37.0%)
  Very Low: bertje_very_low_confidence.csv (200 chunks, 13.2%)

✓ Per-topic files (high confidence):
  Educational         : 78 chunks
  Governance          : 54 chunks
  Persistent          : 62 chunks
  Social              : 51 chunks

✓ CHECKPOINT 8 COMPLETE - CORPUS LABELED
```

---

## Integration with Analysis Pipeline

### What You Can Do With BERTje Labels

1. **Quality Assessment**:
   - Compare SBERT labels (Checkpoint 5) vs BERTje labels (Checkpoint 8)
   - Check agreement on high-confidence chunks
   - Identify chunks where models disagree (review candidates)

2. **Active Learning**:
   - Use high-confidence labels as training data
   - Review medium/low confidence chunks manually
   - Iterate: Label → Review → Retrain

3. **Topic Analysis**:
   - Use per-topic high-confidence files for qualitative analysis
   - Extract representative chunks per topic
   - Analyze co-occurrence patterns (chunks with multiple high scores)

4. **Multi-Label Detection**:
   - Filter chunks with low CV (multiple topics equally relevant)
   - Identify cross-cutting themes
   - Example: Educational + Racism co-occurrence

5. **Dictionary Refinement**:
   - Extract high-frequency terms from high-confidence chunks
   - Use as seeds for next dictionary iteration
   - Compare to existing dictionary terms

---

## Troubleshooting

### Error: Model not found

**Symptom**:
```
❌ ERROR: Model not found at <path>
Expected structure:
  <path>/
  └── full_model/
      ├── pytorch_model.bin
      ├── model_config.json
      └── tokenizer files
```

**Solution**:
1. Ensure Checkpoint 7 completed successfully
2. Check that `full_model/` directory exists
3. Verify `pytorch_model.bin` and `model_config.json` are present
4. If loading from different workflow, update `CONFIG['paths']['pretrained_model_path']`

### Error: Corpus not found

**Symptom**:
```
❌ ERROR: Corpus not found at <path>/chunked_corpus.csv
```

**Solution**:
1. Ensure Checkpoint 1 completed (corpus chunking)
2. Check workflow directory structure
3. If loading from different workflow, set `corpus_source_workflow` variable in Cell 68

### Low Confidence Percentage

**Symptom**:
Most chunks classified as low/very_low confidence

**Diagnosis**:
- Model may not have trained well (check Checkpoint 7 metrics)
- Corpus very different from training data
- Score distribution skewed

**Solution**:
1. Check Checkpoint 7 evaluation results (Pearson, MAE, etc.)
2. If Pearson < 0.75, retrain with more epochs or adjust learning rate
3. Review score distribution in Cell 69 output
4. Consider adjusting confidence thresholds

---

## Comparison to SBERT Labels

### Score Scale Alignment

**SBERT** (Checkpoint 5): Dot product scores [~1-9]
**BERTje** (Checkpoint 8): Regression outputs [0-10]

Scores should be similar in magnitude since:
- BERTje trained on SBERT labels
- Regression targets = SBERT dot product scores
- Clamped to [0-10] at inference

### Expected Agreement

**High-confidence chunks**: 70-85% agreement
- BERTje learned patterns from SBERT
- Should replicate primary topic in most cases

**Low-confidence chunks**: 40-60% agreement
- More ambiguous, harder for model to predict
- Disagreement expected (multi-topic or edge cases)

### When to Trust Each

**Use SBERT labels when**:
- Initial labeling (Checkpoint 5)
- Creating training data for BERTje
- Dictionary-driven analysis (transparent)

**Use BERTje labels when**:
- Labeling large corpus (faster than SBERT scoring)
- Want confidence estimates (4-tier system)
- Active learning (focus review on low-confidence)
- Model learned domain-specific patterns (fine-tuned)

**Use BOTH when**:
- Quality control (agreement = high quality)
- Disagreement analysis (interesting edge cases)
- Ensemble labeling (combine predictions)

---

## Next Steps After Checkpoint 8

1. **Validation**:
   - Sample high-confidence chunks, manually verify quality
   - Check agreement with SBERT labels
   - Inspect disagreements (model errors or genuine ambiguity?)

2. **Analysis**:
   - Use high-confidence per-topic files for qualitative coding
   - Analyze score distributions by document/source
   - Identify multi-topic patterns (low CV chunks)

3. **Iteration**:
   - If quality good → proceed with analysis
   - If quality poor → retrain (Checkpoint 7) with more data/epochs
   - If ambiguous → manual review + active learning

4. **Export**:
   - Convert to analysis-ready format (e.g., for NVivo, Atlas.ti)
   - Create topic summaries
   - Generate visualizations

---

## Summary

**Checkpoint 8 now**:
- ✓ Works with new continuous regression architecture (Checkpoint 7)
- ✓ Loads from standard HuggingFace `full_model/` structure
- ✓ Outputs continuous scores [0-10] matching SBERT scale
- ✓ Provides 4-tier confidence classification (high, medium, low, very_low)
- ✓ Includes CV metric for differentiation assessment
- ✓ Creates multiple output files for different use cases

**Key improvements**:
- Aligned with Checkpoint 7 training
- More granular scores (continuous vs ordinal)
- Multi-factor confidence (score + margin + CV)
- Better documentation and error handling

**Ready for**: Full corpus labeling with fine-tuned BERTje model! 🚀
