# Dictionary Discovery v26: Checkpoint 9 Visualization Plan

## Overview
Transform v25 Checkpoint 9 into comprehensive validation suite with:
1. Dictionary fitness validation
2. Model comparison (base cosine vs. pretrained vs. slavery-trained vs. policy-trained)
3. Topic coherence & model performance metrics
4. Chunk scoring analysis
5. Thesis-relevant visualizations

---

## SECTION 1: SETUP & DATA LOADING

### Cell 9.0: Source Override Configuration
**Purpose**: Allow loading data from different workflows for comparison

**Inputs**: None
**Configuration Variables**:
```
CP9_SOURCE = None  # Or specific workflow path
```

**Outputs**:
- `source_fs` object pointing to data source
- Print data source locations

**Packages**: `pathlib`, workflow filesystem utilities

**Saves**: Nothing

---

### Cell 9.1: Visualization Configuration Variables
**Purpose**: Central configuration for all visualizations

**Inputs**: None

**Configuration Variables**:
```python
# === DATA SELECTION ===
# Which model outputs to compare (all paths relative to source_fs)
COMPARE_MODELS = {
    'base_cosine': True,          # Dictionary-based cosine scores (always available)
    'pretrained_bertje': False,   # GroNLP/bert-base-dutch-cased (generate if needed)
    'slavery_trained': False,     # Domain-adapted model (if available)
    'policy_trained': True        # V10 finetuned model (from CP7)
}

# === METADATA FILTERS ===
# Available from chunked_corpus.csv: doc_type, year, document_folder, filename
METADATA_FILTERS = {
    'doc_type': None,      # None = all, or list like ['policy', 'report']
    'year_range': None,    # None = all, or (2015, 2024)
    'doc_folder': None     # None = all, or specific folder
}

# === VISUALIZATION SETTINGS ===
MIN_SCORE_THRESHOLD = 0.3        # For high-confidence filtering
TOP_N_SHIFTERS = 100             # How many shift vectors to show
SAMPLE_SIZE_3D = 1000            # Max chunks for 3D plots (performance)
PCA_RANDOM_STATE = 42
FIGURE_DPI = 150

# === OUTPUT SETTINGS ===
SAVE_INTERACTIVE = True          # Save HTML plots
SAVE_STATIC = True               # Save PNG/PDF for thesis
SHOW_IN_NOTEBOOK = True          # Display plots inline
```

**Outputs**:
- Configuration dictionary
- Print configuration summary

**Packages**: None (pure Python)

**Saves**: Nothing (configuration only)

---

### Cell 9.2: Import Visualization Libraries
**Purpose**: Load all required packages

**Inputs**: None

**Packages to Import**:
```python
# Core
import pandas as pd
import numpy as np
from pathlib import Path
import json

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ML & Metrics
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    silhouette_score,
    calinski_harabasz_score,
    confusion_matrix
)
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import pearsonr, spearmanr

# NLP
from transformers import AutoModel, AutoTokenizer
import torch
from tqdm.auto import tqdm

# Styling
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['figure.dpi'] = FIGURE_DPI
```

**Outputs**:
- Print import status
- Set device (CPU/GPU)

**Saves**: Nothing

---

### Cell 9.3: Load Core Data
**Purpose**: Load all necessary data files

**Inputs**:
- `source_fs.folders['Dictionary'] / 'curated_dictionary.csv'`
- `source_fs.folders['Cosine_labeling'] / 'scores_all_labeled.csv'`
- `source_fs.folders['Other_data'] / 'chunked_corpus.csv'`
- `source_fs.folders['Other_data'] / 'vocab_embeddings.npy'` (if exists)
- `source_fs.folders['Other_data'] / 'vocab_meta.json'` (if exists)

**Data Loading Steps**:
1. **Load dictionary**:
   - Parse topics, terms, weights, categories, is_seed
   - Separate seeds vs. expanded terms
   - Group by topic

2. **Load cosine scores**:
   - All chunk scores from CP5
   - Merge with chunked_corpus metadata (doc_type, year)

3. **Load vocabulary embeddings** (if available):
   - For dictionary term embedding analysis
   - Metadata includes term text, topic assignment

4. **Apply metadata filters** (if configured):
   - Filter by doc_type, year_range, doc_folder

**Outputs**:
- `df_dict`: Dictionary with columns [topic, term, weight, category, is_seed, parent]
- `df_cosine`: Cosine scores merged with metadata
- `df_chunks`: Chunked corpus with metadata
- `vocab_embeddings`: Numpy array if available
- `vocab_meta`: Dictionary metadata
- Topic list: `topics`
- Print data summary statistics

**Validation Checks**:
- Verify expected columns exist
- Check for missing values
- Report filtered vs. total chunks

**Saves**: Nothing (data loaded to memory)

---

## SECTION 2: MODEL EMBEDDINGS GENERATION

### Cell 9.4: Load BERTJE Models
**Purpose**: Load all models specified in COMPARE_MODELS configuration

**Inputs**:
- `COMPARE_MODELS` configuration
- `source_fs.folders['Model_finetuning']` (for policy_trained)

**Model Loading Logic**:

**For each enabled model in COMPARE_MODELS**:

1. **base_cosine** (always True):
   - No model loading needed
   - Already have scores from df_cosine

2. **pretrained_bertje** (if True):
   - Load: `'GroNLP/bert-base-dutch-cased'` from HuggingFace
   - Tokenizer + Model
   - Set to eval mode
   - Move to device

3. **slavery_trained** (if True):
   - Check if exists in workflow
   - Path options:
     - `source_fs.folders['Model_finetuning'] / 'slavery_domain_encoder'`
     - OR user-specified path
   - Load tokenizer + model
   - Set to eval mode

4. **policy_trained** (if True):
   - Load: `source_fs.folders['Model_finetuning'] / 'trained_encoder'`
   - This is the V10-finetuned model from CP7
   - Load tokenizer + model
   - Set to eval mode

**Outputs**:
- Dictionary: `models = {'base_cosine': None, 'pretrained_bertje': model_obj, ...}`
- Dictionary: `tokenizers = {'pretrained_bertje': tokenizer_obj, ...}`
- Print model loading summary
- Error handling: Skip models that fail to load, warn user

**Packages**: `transformers`, `torch`

**Saves**: Nothing (models in memory)

---

### Cell 9.5: Generate Model Embeddings for Dictionary Terms
**Purpose**: Create embeddings for all dictionary terms using each loaded model

**Inputs**:
- `df_dict` (dictionary terms)
- `models` dictionary
- `tokenizers` dictionary

**Processing**:
For each model in `models` (excluding base_cosine):
1. Extract unique terms from df_dict
2. Batch tokenize terms (batch_size=32)
3. Generate embeddings (mean pooling of last hidden state)
4. Store in dictionary: `dict_embeddings[model_name] = embeddings_array`
5. Progress bar for each model

**Outputs**:
- `dict_embeddings`: Dictionary mapping model_name → embeddings array [N_terms, 768]
- `dict_terms_list`: Ordered list of terms (same order as embeddings)
- Print embedding generation summary per model

**Error Handling**:
- Skip models that failed to load
- Handle OOM errors (reduce batch size)

**Packages**: `torch`, `transformers`, `tqdm`

**Saves**: Nothing (embeddings in memory)

---

### Cell 9.6: Generate Model Embeddings for Chunks (Sample)
**Purpose**: Create embeddings for corpus chunks using each model (sample for performance)

**Inputs**:
- `df_chunks` (or filtered subset based on METADATA_FILTERS)
- `models` dictionary
- `tokenizers` dictionary
- `SAMPLE_SIZE_3D` configuration

**Sampling Strategy**:
1. If len(df_chunks) > SAMPLE_SIZE_3D:
   - Stratified sample by primary_topic (from cosine scores)
   - Ensures each topic represented
2. Else: Use all chunks

**Processing**:
For each model in `models` (excluding base_cosine):
1. Extract text_for_scoring from sampled chunks
2. Batch tokenize (batch_size=16, max_length=512)
3. Generate embeddings (mean pooling)
4. Store in dictionary: `chunk_embeddings[model_name] = embeddings_array`
5. Progress bar per model

**Outputs**:
- `chunk_embeddings`: Dictionary mapping model_name → embeddings array [N_chunks, 768]
- `df_chunks_sampled`: Sampled chunks dataframe
- Print embedding generation summary
- Report: Sample size, topics distribution

**Error Handling**:
- Reduce batch size on OOM
- Skip failed models

**Packages**: `torch`, `transformers`, `tqdm`, `numpy`

**Saves**: Nothing (embeddings in memory)

---

## SECTION 3: DICTIONARY FITNESS VISUALIZATIONS

### Cell 9.7: Weight Tier Validation (Boxplot)
**Purpose**: Validate V10 weighting scheme - do higher-weight terms cluster tighter?

**Inputs**:
- `dict_embeddings['policy_trained']` (V10 finetuned model)
- `df_dict` with weight and category columns

**Analysis Steps**:
1. For each term, calculate distance to its topic centroid:
   - Group embeddings by topic
   - Compute topic centroid (mean embedding)
   - Calculate Euclidean distance from each term to its centroid

2. Group distances by weight tier (category):
   - KERN (1.0, 0.9)
   - BELEID (0.8)
   - STERK (0.3-0.9, variable)
   - CONTEXT (0.6)
   - RISICO (0.3)

3. Create boxplot:
   - X-axis: Weight categories (ordered by typical weight)
   - Y-axis: Distance to topic centroid
   - Expected pattern: KERN tightest, RISICO loosest

**Validation Metric**:
- Pearson correlation: weight value vs. distance to centroid (should be negative)
- ANOVA F-statistic: difference between categories

**Outputs**:
- **Figure 1**: Boxplot (Plotly interactive)
  - Title: "Dictionary Weight Tier Validation: Cluster Tightness by Category"
  - Annotations: correlation coefficient, F-statistic
  - Color-coded by category

- **Statistical Summary Table**:
  - Per-category: mean distance, std, min, max
  - Correlation coefficient
  - Interpretation text

**Packages**: `plotly`, `scipy.stats`, `numpy`

**Saves**:
- `Visuals/dictionary_weight_validation.html`
- `Visuals/dictionary_weight_validation.png` (if SAVE_STATIC)
- `Visuals/weight_tier_statistics.csv` (table)

---

### Cell 9.8: Expansion Quality Validation (Scatter + Arrows)
**Purpose**: Do expanded terms cluster with their parent seed terms?

**Inputs**:
- `dict_embeddings['policy_trained']`
- `df_dict` with is_seed and parent columns

**Analysis Steps**:
1. Filter to expanded terms only (is_seed == 0)
2. For each expanded term:
   - Find parent seed term
   - Calculate distance to parent seed in embedding space
   - Calculate distance to topic centroid
   - Compare: Is term closer to parent or to centroid?

3. Identify outliers:
   - Top 20 terms farthest from parent seed
   - These may be mis-expansions or cross-topic terms

**Visualization Options**:

**Option A: 2D PCA with arrows** (seed → expanded term)
- Reduce dict_embeddings to 2D via PCA
- Plot seeds as large markers
- Plot expanded terms as small markers
- Draw arrows from parent seed to expanded terms
- Color by topic
- Highlight outliers (long arrows)

**Option B: Distance distribution histogram**
- X-axis: Distance to parent seed
- Y-axis: Frequency
- Separate distributions per topic
- Mark outlier threshold

**Outputs**:
- **Figure 2A**: 2D PCA scatter with arrows
  - Title: "Dictionary Expansion Quality: Parent-Child Term Clustering"
  - Outlier terms labeled

- **Figure 2B**: Distance distribution histogram
  - Title: "Expansion Distance Distribution by Topic"

- **Outlier Table**:
  - Top 20 terms: [term, parent, distance, topic]
  - For manual review

**Packages**: `plotly`, `sklearn.decomposition`, `numpy`

**Saves**:
- `Visuals/expansion_quality_2d.html`
- `Visuals/expansion_quality_histogram.html`
- `Visuals/expansion_outliers.csv`

---

### Cell 9.9: Dictionary Term Clustering (2D PCA - Multi-Model Comparison)
**Purpose**: Show dictionary term separation ACROSS models (pre/post training comparison)

**Inputs**:
- `dict_embeddings` dictionary (all models)
- `df_dict`

**Processing**:
For each model with embeddings:
1. Standardize embeddings
2. Apply PCA (2 components)
3. Store 2D coordinates

**Visualization**:
Side-by-side subplots (1 row, N columns):
- Column 1: pretrained_bertje (if available)
- Column 2: slavery_trained (if available)
- Column 3: policy_trained (V10)

Each subplot:
- Scatter plot: dictionary terms colored by topic
- Distinguish seeds (large markers) vs. expanded (small)
- Topic centroids marked with stars
- Variance explained annotation

**Comparison Analysis**:
- Visual inspection: Do clusters tighten left→right?
- Quantitative: Calculate silhouette score per model
- Display scores on plots

**Outputs**:
- **Figure 3**: Multi-panel 2D comparison
  - Title: "Dictionary Term Evolution: Progressive Model Refinement"
  - Subtitle shows silhouette scores per panel

- **Metrics Table**:
  - Per model: silhouette score, Calinski-Harabasz index, avg intra-topic distance

**Packages**: `plotly`, `sklearn`, `numpy`

**Saves**:
- `Visuals/dictionary_terms_multimodel_2d.html`
- `Visuals/dictionary_metrics_comparison.csv`

---

### Cell 9.10: Dictionary Term Clustering (3D PCA - Exploration)
**Purpose**: 3D interactive exploration of dictionary term space (best model only)

**Inputs**:
- `dict_embeddings['policy_trained']` (or best-performing model)
- `df_dict`

**Processing**:
1. PCA to 3 components
2. Color by topic
3. Distinguish seeds vs. expanded (marker size/symbol)

**Visualization**:
- 3D scatter (Plotly)
- Hover: term text, topic, weight, category, is_seed
- Topic centroids as stars
- Rotation enabled

**Outputs**:
- **Figure 4**: 3D interactive scatter
  - Title: "Dictionary Term Semantic Space (3D Exploration)"
  - Camera angle preset for best view

**Packages**: `plotly`, `sklearn`

**Saves**:
- `Visuals/dictionary_terms_3d.html`

**Note**: Keep for exploration, may not include in thesis (3D hard to print)

---

## SECTION 4: TOPIC COHERENCE & MODEL PERFORMANCE

### Cell 9.11: Cluster Quality Metrics Table
**Purpose**: Quantitative validation of topic separation across models

**Inputs**:
- `dict_embeddings` (all models)
- `df_dict` topic labels

**Metrics to Calculate**:
For each model with embeddings:

1. **Silhouette Score**:
   - Measures cluster cohesion and separation
   - Range [-1, 1], higher = better
   - `silhouette_score(embeddings, topic_labels)`

2. **Calinski-Harabasz Index** (Variance Ratio):
   - Ratio between-cluster / within-cluster variance
   - Higher = more distinct clusters
   - `calinski_harabasz_score(embeddings, topic_labels)`

3. **Average Intra-Topic Distance**:
   - Per topic: mean distance from terms to topic centroid
   - Overall: weighted average across topics
   - Lower = tighter clusters

4. **Per-Topic Tightness**:
   - For each of 7 topics, calculate mean distance to centroid
   - Compare across models
   - Identify which topics improve most with training

**Outputs**:

- **Table 1: Overall Metrics**
```
| Metric                  | Pretrained | Slavery | Policy | Improvement |
|-------------------------|------------|---------|--------|-------------|
| Silhouette Score        | 0.23       | 0.41    | 0.58   | +152%       |
| Calinski-Harabasz       | 847        | 1203    | 1876   | +121%       |
| Avg Intra-Topic Dist    | 2.34       | 1.87    | 1.21   | -48%        |
```

- **Table 2: Per-Topic Tightness**
```
| Topic                   | Pre   | Post  | Δ      | % Change |
|-------------------------|-------|-------|--------|----------|
| Slavernij_Historisch    | 1.89  | 1.12  | -0.77  | -41%     |
| Koninkrijks_Macht       | 2.11  | 1.34  | -0.77  | -36%     |
| Raciale_Hierarchie      | 2.45  | 1.89  | -0.56  | -23%     |  ← Least
...
```

- **Figure 5**: Bar chart comparing metrics
  - X-axis: Models
  - Y-axis: Metric values (normalized)
  - Grouped bars: 3 metrics

**Packages**: `sklearn.metrics`, `pandas`, `plotly`

**Saves**:
- `Visuals/cluster_quality_overall.csv`
- `Visuals/cluster_quality_per_topic.csv`
- `Visuals/cluster_quality_comparison.html` (bar chart)

---

### Cell 9.12: Topic Separation Heatmap (Confusion Matrix Style)
**Purpose**: Show inter-topic similarity/confusion across models

**Inputs**:
- `dict_embeddings` (all models)
- `df_dict`

**Analysis Steps**:
For each model:
1. Calculate topic centroid embeddings (7 centroids)
2. Compute pairwise cosine similarity matrix (7×7)
   - Diagonal = 1.0 (topic with itself)
   - Off-diagonal = similarity between topics
   - Lower off-diagonal = better separation

3. Calculate improvement: similarity_pre - similarity_post
   - Positive values = better separation after training

**Visualization**:
3-column layout:
- Column 1: Pre-training confusion (pretrained_bertje)
- Column 2: Post-training separation (policy_trained)
- Column 3: Improvement (pre - post)

Each heatmap:
- 7×7 matrix
- Color scale: Red (high similarity/confusion) → Green (low similarity/separation)
- Annotated with similarity values

**Outputs**:
- **Figure 6**: Triple heatmap comparison
  - Title: "Topic Separation Analysis: Inter-Topic Confusion Matrices"
  - Annotations: highlight biggest improvements

- **Separation Statistics**:
  - Average off-diagonal similarity: Pre vs. Post
  - Most confused topic pairs (pre-training)
  - Most improved topic pairs

**Packages**: `plotly`, `sklearn.metrics.pairwise`, `numpy`

**Saves**:
- `Visuals/topic_separation_heatmaps.html`
- `Visuals/topic_separation_statistics.csv`

---

### Cell 9.13: Training Metrics Visualization
**Purpose**: Show model convergence and per-topic performance (from CP7)

**Inputs**:
- `source_fs.folders['Model_finetuning'] / 'training_metrics.json'` (if exists)

**Metrics to Plot**:
1. **Training/Validation Loss Curves**:
   - X-axis: Epoch
   - Y-axis: Loss
   - Two lines: train loss, val loss
   - Identify overfitting (if val loss increases)

2. **Per-Topic Correlation** (final epoch):
   - Bar chart: 7 topics on X-axis
   - Y-axis: Pearson correlation (predicted vs. true scores)
   - Identify weak topics (low correlation)

3. **Per-Topic MAE** (final epoch):
   - Bar chart: 7 topics
   - Y-axis: Mean Absolute Error
   - Lower = better

**Outputs**:
- **Figure 7A**: Loss curves (line plot)
  - Title: "Training Convergence: Loss Over Epochs"

- **Figure 7B**: Per-topic correlation (bar chart)
  - Title: "Per-Topic Model Performance: Correlation"
  - Sort by correlation (ascending)

- **Figure 7C**: Per-topic MAE (bar chart)
  - Title: "Per-Topic Model Performance: Mean Absolute Error"

**Packages**: `plotly`, `pandas`, `json`

**Saves**:
- `Visuals/training_loss_curves.html`
- `Visuals/per_topic_correlation.html`
- `Visuals/per_topic_mae.html`

**Note**: If training_metrics.json missing, skip with warning

---

## SECTION 5: CHUNK SCORING ANALYSIS

### Cell 9.14: Chunk Embeddings & PCA Preparation
**Purpose**: Prepare chunk data for visualization (all models)

**Inputs**:
- `chunk_embeddings` (from Cell 9.6)
- `df_chunks_sampled`
- `df_cosine` (for base_cosine "scores-as-features")

**Processing**:
For each model:

1. **If model has embeddings** (pretrained, slavery, policy):
   - Standardize embeddings
   - Apply PCA (2D and 3D)
   - Store coordinates

2. **If base_cosine**:
   - Use topic scores as "feature space" (7-dimensional)
   - Each chunk = [score_topic1, score_topic2, ..., score_topic7]
   - Standardize
   - Apply PCA (2D and 3D)

3. **Assign primary topic** (for coloring):
   - Use cosine scores to determine primary topic
   - Calculate confidence metrics: max_score, margin, CV

4. **Filter high-confidence** (optional):
   - Keep chunks with max_score >= MIN_SCORE_THRESHOLD
   - For clearer visualizations

**Outputs**:
- `chunk_viz_data`: Dictionary per model
  - `df`: Dataframe with PCA coords, primary_topic, confidence
  - `pca_2d`: Fitted PCA object (2 components)
  - `pca_3d`: Fitted PCA object (3 components)
  - `variance_2d`: Explained variance [PC1, PC2]
  - `variance_3d`: Explained variance [PC1, PC2, PC3]
  - `scaler`: Fitted StandardScaler

- Print summary: chunks per model, variance explained

**Packages**: `sklearn.decomposition`, `sklearn.preprocessing`, `pandas`

**Saves**: Nothing (data structures in memory)

---

### Cell 9.15: Chunk Clustering Visualization (2D Multi-Model)
**Purpose**: Show how chunks cluster by topic across different models

**Inputs**:
- `chunk_viz_data` (all models)

**Visualization**:
Multi-panel layout (1 row, N columns):
- Each column = one model
- Each panel: 2D PCA scatter
  - Points colored by primary_topic
  - Topic centroids as stars
  - Variance explained annotated

**Comparison Insight**:
- Visual: Do clusters become more separated left→right?
- Quantitative: Overlay silhouette scores on each panel

**Outputs**:
- **Figure 8**: Multi-panel 2D chunk clustering
  - Title: "Corpus Chunks: Topic Clustering Across Models"
  - Subtitle: model names + silhouette scores

**Packages**: `plotly.subplots`, `numpy`

**Saves**:
- `Visuals/chunk_clustering_multimodel_2d.html`

---

### Cell 9.16: Chunk Pre/Post Training Comparison (2D Side-by-Side)
**Purpose**: Direct before/after comparison for main model

**Inputs**:
- `chunk_viz_data['pretrained_bertje']` (pre)
- `chunk_viz_data['policy_trained']` (post)

**Visualization**:
Two panels:
- Left: Pre-training (pretrained_bertje)
- Right: Post-training (policy_trained)

Each panel:
- Scatter plot colored by primary_topic
- Same color scheme
- Variance explained

**Outputs**:
- **Figure 9**: Side-by-side comparison
  - Title: "Chunk Representations: Pre vs. Post Training"

**Packages**: `plotly.subplots`

**Saves**:
- `Visuals/chunk_prepost_comparison_2d.html`

---

### Cell 9.17: Chunk Shift Analysis (Calculate Shifts)
**Purpose**: Quantify how much each chunk moved during training

**Inputs**:
- `chunk_embeddings['pretrained_bertje']` (pre)
- `chunk_embeddings['policy_trained']` (post)
- `df_chunks_sampled`

**Analysis Steps**:
1. Calculate shift vectors:
   - shift = embedding_post - embedding_pre
   - shift_magnitude = ||shift|| (Euclidean norm)

2. Identify top shifters:
   - Top 10%: Largest magnitude shifts
   - Bottom 10%: Smallest shifts (stable chunks)

3. Analyze shift patterns:
   - Correlation: initial_score vs. shift_magnitude
     - Hypothesis: Low-confidence chunks shift more (model corrects uncertain cases)
   - Per-topic shift statistics

4. Add to dataframe:
   - shift_magnitude column
   - shift_x, shift_y, shift_z (for 3D viz)

**Outputs**:
- `df_chunks_with_shifts`: Enhanced dataframe
- **Shift Statistics Table**:
  - Overall: mean, median, max shift
  - Per-topic: mean shift magnitude
  - Top 20 shifters list

**Packages**: `numpy`, `pandas`

**Saves**:
- `Visuals/chunk_shift_statistics.csv`
- `Visuals/top_shifters.csv`

---

### Cell 9.18: Chunk Shift Visualization (2D Scatter: Score vs. Shift)
**Purpose**: Show relationship between initial confidence and training-induced shift

**Inputs**:
- `df_chunks_with_shifts`

**Visualization**:
Scatter plot:
- X-axis: Initial max_score (cosine, pre-training proxy)
- Y-axis: Shift magnitude
- Color by primary_topic
- Trendline (regression)

**Expected Pattern**:
- Negative correlation: low initial score → high shift
- Model corrects uncertain/low-confidence predictions more

**Outputs**:
- **Figure 10**: Scatter with trendline
  - Title: "Training Impact: Initial Confidence vs. Embedding Shift"
  - Annotations: correlation coefficient, p-value

**Packages**: `plotly`, `scipy.stats`

**Saves**:
- `Visuals/chunk_shift_vs_score.html`

---

### Cell 9.19: Chunk Shift Vectors (3D Visualization)
**Purpose**: Interactive 3D exploration of shifts (for discovery, not thesis)

**Inputs**:
- `chunk_viz_data['pretrained_bertje']` (3D coords)
- `chunk_viz_data['policy_trained']` (3D coords)
- `df_chunks_with_shifts`

**Visualization**:
3D scatter plot:
- Pre-training positions (light, small markers)
- Post-training positions (bold, larger markers)
- Shift vectors as arrows (for top 10% shifters only, for performance)
- Color by topic

**Outputs**:
- **Figure 11**: 3D shift visualization
  - Title: "Chunk Semantic Shifts: 3D Trajectory Analysis"
  - Camera preset

**Packages**: `plotly`, `numpy`

**Saves**:
- `Visuals/chunk_shifts_3d.html`

**Note**: Exploration only, likely won't include in thesis

---

### Cell 9.20: Chunk Clustering (3D - Best Model)
**Purpose**: 3D exploration of final model chunk clustering

**Inputs**:
- `chunk_viz_data['policy_trained']`

**Visualization**:
3D scatter:
- Chunks colored by primary_topic
- Topic centroids as stars
- Rotation enabled

**Outputs**:
- **Figure 12**: 3D chunk clustering (policy_trained)
  - Title: "Corpus Chunks: 3D Topic Clustering (V10 Model)"

**Packages**: `plotly`

**Saves**:
- `Visuals/chunk_clustering_3d.html`

---

## SECTION 6: SCORE DISTRIBUTION ANALYSIS

### Cell 9.21: Score Distribution Comparison (Dictionary vs. Model)
**Purpose**: Show agreement/disagreement between cosine scores and BERTJE predictions

**Inputs**:
- `df_cosine` (base_cosine scores)
- BERTJE predictions (if available from CP8 output)
  - Load: `source_fs.folders['Bertje_labeling'] / 'bertje_labeled_corpus.csv'`

**Analysis**:
For each of 7 topics:
1. Get cosine scores (dictionary-based)
2. Get BERTJE scores (model-based)
3. Plot overlapping histograms

**Visualization**:
7-panel subplot (2 rows, 4 columns):
- Each panel = one topic
- Two overlapping histograms:
  - Blue: Cosine scores
  - Red: BERTJE scores
- X-axis: Score value
- Y-axis: Frequency

**Interpretation**:
- Similar distributions = good agreement
- BERTJE sharper peaks = model more decisive
- BERTJE shifted right/left = model more/less confident

**Outputs**:
- **Figure 13**: 7-panel histogram comparison
  - Title: "Score Distributions: Dictionary (Cosine) vs. Model (BERTJE)"

**Packages**: `plotly.subplots`, `pandas`

**Saves**:
- `Visuals/score_distribution_comparison.html`

**Note**: Requires CP8 BERTJE labeling output; skip if not available

---

### Cell 9.22: Confidence Agreement Scatter
**Purpose**: Chunk-level agreement between cosine and BERTJE scores

**Inputs**:
- `df_cosine`
- BERTJE predictions

**Visualization**:
7-panel subplot (one per topic):
- Each panel: Scatter plot
  - X-axis: Cosine score
  - Y-axis: BERTJE score
  - Diagonal reference line (perfect agreement)
  - Points above diagonal = BERTJE more confident
  - Points below diagonal = BERTJE less confident

**Quadrant Analysis**:
- **Top-right**: High cosine, high BERTJE (validated)
- **Top-left**: Low cosine, high BERTJE (model found relevance dictionary missed)
- **Bottom-right**: High cosine, low BERTJE (false positives in dictionary)
- **Bottom-left**: Low both (irrelevant)

**Outputs**:
- **Figure 14**: 7-panel scatter with quadrants
  - Title: "Cosine-BERTJE Agreement by Topic"
  - Annotations: % chunks in each quadrant

**Packages**: `plotly.subplots`

**Saves**:
- `Visuals/cosine_bertje_agreement.html`

**Note**: Requires CP8 output

---

## SECTION 7: THESIS-SPECIFIC VISUALIZATIONS (OPTIONAL)

### Cell 9.23: IDPAD Temporal Trends (If Applicable)
**Purpose**: Show how topic scores evolved 2015-2024 in IDPAD corpus

**Inputs**:
- `df_cosine` (or BERTJE predictions)
- Year metadata from chunked_corpus

**Analysis**:
1. Group chunks by year
2. Calculate average topic scores per year
3. Create time series

**Visualization**:
Line plot:
- X-axis: Year (2015-2024)
- Y-axis: Average topic score
- 7 lines (one per topic)
- Vertical line at 2022 (apology)

**Expected Insight**:
- Did Erkenning_Verantwoordelijkheid increase post-2022?

**Outputs**:
- **Figure 15**: Temporal trends
  - Title: "IDPAD Policy Evolution (2015-2024): Topic Scores Over Time"

**Packages**: `plotly`, `pandas`

**Saves**:
- `Visuals/idpad_temporal_trends.html`

**Note**: Only if year metadata available and research question relevant

---

### Cell 9.24: Development-Legacy Gap Analysis (If Applicable)
**Purpose**: Identify policies discussing development without legacy framing

**Inputs**:
- `df_cosine` or BERTJE predictions
- Development keywords (education, poverty, etc.) - TF-IDF scores

**Analysis**:
1. Calculate development_score: TF-IDF of problem keywords
2. Calculate legacy_score: Average across all 7 V10 topics
3. Scatter plot

**Visualization**:
- X-axis: Development score
- Y-axis: Legacy score
- Color by year
- Quadrant lines at medians
- Highlight "gap zone" (high development, low legacy)

**Outputs**:
- **Figure 16**: Gap scatter plot
  - Title: "The Development-Legacy Gap in IDPAD Policies"
  - Annotation: % in gap zone

**Packages**: `plotly`, `sklearn.feature_extraction.text`

**Saves**:
- `Visuals/development_legacy_gap.html`

**Note**: Requires development keyword list; thesis-specific

---

## SECTION 8: SUMMARY & EXPORT

### Cell 9.25: Visualization Summary Report
**Purpose**: Generate summary document of all visualizations

**Outputs**:
- **Markdown report**: `Visuals/VISUALIZATION_SUMMARY.md`
  - List all generated figures
  - Key findings per visualization
  - Recommendations for thesis inclusion

**Packages**: `pathlib`, markdown generation

**Saves**:
- `Visuals/VISUALIZATION_SUMMARY.md`

---

### Cell 9.26: Checkpoint Complete
**Purpose**: Final status message

**Outputs**:
- Print completion message
- List all saved files in Visuals folder
- Data structures available for further analysis

**Saves**: Nothing

---

## DATA FLOW SUMMARY

### Required Inputs (from previous checkpoints):
1. **Dictionary**: `curated_dictionary.csv` (CP4)
2. **Cosine Scores**: `scores_all_labeled.csv` (CP5)
3. **Chunked Corpus**: `chunked_corpus.csv` (CP1)
4. **Vocabulary Embeddings**: `vocab_embeddings.npy` (CP2, optional)
5. **Trained Model**: `trained_encoder/` (CP7)
6. **Training Metrics**: `training_metrics.json` (CP7, optional)
7. **BERTJE Predictions**: `bertje_labeled_corpus.csv` (CP8, optional)

### Generated Outputs (saved to Visuals/):
1. `dictionary_weight_validation.html` + `.png` + statistics.csv
2. `expansion_quality_2d.html` + `_histogram.html` + outliers.csv
3. `dictionary_terms_multimodel_2d.html` + metrics_comparison.csv
4. `dictionary_terms_3d.html`
5. `cluster_quality_overall.csv` + `_per_topic.csv` + `_comparison.html`
6. `topic_separation_heatmaps.html` + statistics.csv
7. `training_loss_curves.html` + per_topic metrics
8. `chunk_clustering_multimodel_2d.html`
9. `chunk_prepost_comparison_2d.html`
10. `chunk_shift_statistics.csv` + top_shifters.csv
11. `chunk_shift_vs_score.html`
12. `chunk_shifts_3d.html`
13. `chunk_clustering_3d.html`
14. `score_distribution_comparison.html` (if CP8 available)
15. `cosine_bertje_agreement.html` (if CP8 available)
16. `idpad_temporal_trends.html` (if applicable)
17. `development_legacy_gap.html` (if applicable)
18. `VISUALIZATION_SUMMARY.md`

**Total**: ~18-20 HTML files, ~10 CSV files, ~5 PNG files (if SAVE_STATIC=True)

---

## PACKAGE DEPENDENCIES

### Core:
- `pandas`, `numpy`, `pathlib`, `json`

### Visualization:
- `matplotlib`, `seaborn`, `plotly`

### ML/Metrics:
- `scikit-learn` (PCA, StandardScaler, metrics)
- `scipy` (stats)

### NLP:
- `transformers` (AutoModel, AutoTokenizer)
- `torch`
- `tqdm`

---

## ESTIMATED RUNTIME

**Assuming**:
- 5,000 chunks in corpus
- 229 dictionary terms
- 3 models to compare (pretrained, policy-trained + base_cosine)

**Per Section**:
- Setup (Cells 9.0-9.3): < 1 min
- Model Loading (9.4): 1-2 min
- Embedding Generation (9.5-9.6): 5-10 min (GPU) / 30-60 min (CPU)
- Dictionary Viz (9.7-9.10): 2-3 min
- Topic Coherence (9.11-9.13): 1-2 min
- Chunk Analysis (9.14-9.20): 5-10 min
- Score Distribution (9.21-9.22): 2-3 min (if CP8 available)
- Thesis-specific (9.23-9.24): 2-3 min (if applicable)
- Summary (9.25-9.26): < 1 min

**Total**: ~20-30 min (GPU) / ~60-90 min (CPU)

---

## CRITICAL DECISIONS NEEDED BEFORE IMPLEMENTATION

### Decision 1: Model Availability
- **Do you have slavery-trained intermediate model?**
  - If NO: Set `COMPARE_MODELS['slavery_trained'] = False`
  - If YES: Provide path

### Decision 2: CP8 BERTJE Labeling
- **Was CP8 (BERTJE labeling) run on v25?**
  - If NO: Skip Cells 9.21-9.22 (score distribution comparison)
  - If YES: Verify output file exists

### Decision 3: Thesis Application
- **Is this for IDPAD corpus analysis?**
  - If YES: Include Cells 9.23-9.24 (temporal trends, gap analysis)
  - If NO: Skip thesis-specific visualizations

### Decision 4: 3D Visualizations
- **Keep all 3D visualizations for exploration?**
  - Recommendation: YES during development, may exclude from final thesis
  - 3D useful for interactive exploration, screenshots for thesis

### Decision 5: Sample Size
- **How many chunks for embedding generation?**
  - Recommendation: `SAMPLE_SIZE_3D = 1000` (balances performance/representation)
  - Adjust based on GPU memory

---

## MODIFICATIONS FROM V25 CHECKPOINT 9

### Additions:
1. ✓ Multi-model comparison (not just pre/post, but pretrained/slavery/policy)
2. ✓ Weight tier validation (NEW)
3. ✓ Expansion quality validation (NEW)
4. ✓ Cluster quality metrics table (NEW)
5. ✓ Topic separation heatmap (NEW)
6. ✓ Chunk shift magnitude analysis (NEW - beyond just 3D viz)
7. ✓ Score distribution comparison (dictionary vs. model)
8. ✓ IDPAD temporal trends (thesis-specific)
9. ✓ Development-legacy gap (thesis-specific)

### Removals:
- ✗ Remove redundant 3D if 2D sufficient (keep both during exploration)

### Improvements:
- Better organization: Dictionary fitness → Topic coherence → Chunk analysis
- Quantitative metrics alongside visualizations (not just visual)
- Modular: Can skip sections if data not available
- Configuration-driven: Easy to enable/disable models or sections

---

## VALIDATION CHECKLIST

Before running v26:
- [ ] Verify CP7 (training) completed successfully
- [ ] Check trained_encoder folder exists and has model files
- [ ] Confirm curated_dictionary.csv has expected columns
- [ ] Verify scores_all_labeled.csv exists
- [ ] Check chunked_corpus.csv has metadata (year, doc_type)
- [ ] Decide which models to compare (update COMPARE_MODELS)
- [ ] Set SAMPLE_SIZE_3D based on available memory
- [ ] Create Visuals/ output folder if doesn't exist

After running v26:
- [ ] Verify ~18-20 HTML files generated
- [ ] Check cluster quality metrics show improvement
- [ ] Validate topic separation heatmap shows reduced confusion
- [ ] Review top shifters list for interpretability
- [ ] Compare silhouette scores across models (should increase)
- [ ] Check weight tier validation shows expected pattern (KERN tight, RISICO loose)

---

## NEXT STEPS (POST-V26)

1. **Review all visualizations** for thesis inclusion
2. **Extract key findings** for Results chapter
3. **Identify problematic topics** (low correlation, high confusion)
4. **Create consolidated figure set** for thesis (8-10 key visualizations)
5. **Write interpretation** for each visualization in thesis text
6. **Generate supplementary materials** (put 3D/exploratory viz in appendix)
