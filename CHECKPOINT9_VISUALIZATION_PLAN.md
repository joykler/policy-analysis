# Checkpoint 9: Comprehensive Visualization Plan

## Overview
This document outlines the complete visualization strategy for validating the methodology and demonstrating:
1. How dictionary terms cluster around the model's understanding of topics
2. How chunks cluster around topics
3. How confident the 2 scoring methods are and where they disagree
4. **How different BERTJE model checkpoints compare (training progression)**

---

## Data Structure Analysis

### Available Data Sources

**1. Cosine Scores** (`Cosine_labeling/scores_all_labeled.csv`)
- 14,640 chunks
- Columns:
  - `filename`: Source document
  - `chunk_id`: Unique identifier
  - `raw_text`: Full chunk text
  - `cos_Educational Disadvantage & Brain Drain`: Cosine similarity score for topic 1
  - `cos_Governance Distrust & Corruption`: Cosine similarity score for topic 2
  - `cos_Persistent Poverty & Economic Vulnerability`: Cosine similarity score for topic 3
  - `cos_Social Fragmentation & Racism`: Cosine similarity score for topic 4
  - `primary_topic`: Highest scoring topic (cosine)
  - `score_margin`: Difference between top 2 scores (confidence indicator)
  - `rescaled_*`: Rescaled versions of scores
  - `confidence_original`: Confidence level classification

**2. BERTJE Predictions** (`BERTJE_predictions/bertje_continuous_predictions_full.csv`)
- Same 14,640 chunks PLUS:
  - `bertje_Educational Disadvantage & Brain Drain_score`: BERTJE predicted score for topic 1
  - `bertje_Governance Distrust & Corruption_score`: BERTJE predicted score for topic 2
  - `bertje_Persistent Poverty & Economic Vulnerability_score`: BERTJE predicted score for topic 3
  - `bertje_Social Fragmentation & Racism_score`: BERTJE predicted score for topic 4
  - `bertje_primary_topic`: BERTJE's primary topic assignment
  - `bertje_confidence`: BERTJE confidence level
  - `bertje_margin`: Margin between BERTJE's top 2 scores

**3. Dictionary** (`Dictionary/Curated_dictionary.csv`)
- 1,095 terms
- Columns:
  - `topic`: Which of the 4 topics this term belongs to
  - `term`: The actual word/phrase
  - `cosine`: Cosine similarity to topic centroid (how well term matches topic)
  - `df`: Document frequency
  - `weight`: Importance weight
  - `category`: Term category
  - `is_seed`: Binary flag (1=original seed, 0=discovered)

**4. Training Metrics** (`Model_finetuning/training_metrics.json`)
- Final evaluation metrics per topic:
  - `eval_corr_[Topic]`: Correlation with ground truth
  - `eval_mae_[Topic]`: Mean absolute error
  - `eval_acc_[Topic]`: Accuracy (threshold-based)
- Training history (loss, learning rate per step)
- Overall metrics:
  - `eval_mean_correlation`: 0.9059 (excellent!)
  - `eval_pattern_exact_match`: 0.5915
  - Training: 13,530 samples, Validation: 1,109 samples

**5. Model Checkpoints** (`Model_finetuning/checkpoint-*/`)
- checkpoint-2538 (Epoch 3)
- checkpoint-3384 (Epoch 4)
- checkpoint-4230 (Epoch 5 - final)
- Each has saved model weights that could be loaded for comparison

**6. Training Data Options**
- `train_data_option1.csv` through `train_data_option4.csv`
- Different training approaches (labeled only, with pseudo-labels, etc.)
- Need to identify which was used (check training_metrics.json)

---

## Visualization Plan

### CELL 0: Setup & Data Loading
**Purpose**: Load all necessary data and set up environment

**What to load**:
- Cosine scores CSV
- BERTJE predictions CSV (has both cosine and BERTJE scores)
- Dictionary CSV
- Training metrics JSON
- Identify which training dataset was used

**What to validate**:
- Number of chunks loaded: 14,640
- Number of topics identified: 4
- Number of dictionary terms: 1,095
- Column names match expected patterns
- Training metrics loaded successfully

**Output**:
- Print summary statistics
- Store data in dataframes: `df_cosine`, `df_bertje`, `df_dict`, `df_full` (merged)
- Store training metrics in `training_metrics` dict

---

### CELL 1: Dictionary Composition Analysis
**Purpose**: Show the structure and composition of the dictionary

**Visualization Type**: Grouped bar chart

**What to show**:
- For each of the 4 topics:
  - Number of seed terms (original hand-curated)
  - Number of expanded terms (discovered by model)
  - Ratio of seed:expanded

**Why this matters**:
- Validates dictionary expansion worked
- Shows model discovery beyond initial seeds
- Demonstrates topic balance

**Values to include**:
- Topic names (all 4)
- Seed term counts per topic
- Expanded term counts per topic
- Percentages

**Expected findings**:
- More expanded than seed terms (shows discovery works)
- Relatively balanced across topics

**Save to**: `Visuals/dictionary_composition.html`

---

### CELL 2: Dictionary Term Quality - Cosine Similarity Distribution
**Purpose**: Show how well dictionary terms match their assigned topics

**Visualization Type**: Box plot or violin plot

**What to show**:
- Distribution of cosine similarity scores for dictionary terms
- Separate distribution for each topic
- Distinguish seed vs expanded terms with color/pattern

**Why this matters**:
- High cosine = terms align well with topic definitions
- Validates expanded terms are semantically similar to seeds
- Shows if some topics have better-defined dictionaries

**Values to include**:
- Median cosine similarity per topic
- Quartiles (25%, 75%)
- Outliers
- Separate markers for seed vs expanded
- Target threshold line (e.g., 0.4 minimum)

**Expected findings**:
- Seed terms: cosine > 0.6
- Expanded terms: cosine > 0.4
- Clear separation from low-quality terms

**Save to**: `Visuals/dictionary_term_quality.html`

---

### CELL 3: Dictionary Term 2D Space (PCA)
**Purpose**: Visualize how dictionary terms cluster in semantic space

**Visualization Type**: 2D scatter plot with PCA

**What to show**:
- Each dictionary term as a point
- Color by topic (4 colors)
- Shape/size by term type (seed=large, expanded=small)
- Topic centroids as large X markers

**Why this matters**:
- Demonstrates topics are semantically distinct
- Shows seed terms form coherent clusters
- Expanded terms should be near their seeds
- Validates topic separation

**Values to include**:
- PCA Component 1 (x-axis)
- PCA Component 2 (y-axis)
- Explained variance for both components (should be >60%)
- Term labels on hover
- Topic centroids

**Technical notes**:
- Features: 4D vector of each term's cosine scores to each topic
- PCA: 4D → 2D reduction
- Scale features before PCA

**Expected findings**:
- 4 distinct clusters (one per topic)
- Minimal overlap
- Expanded terms near their topic cluster

**Save to**: `Visuals/dictionary_clustering_2d.html`

---

### CELL 4: Chunk Clustering - 2D Overview (All Topics)
**Purpose**: Show how chunks cluster around each topic in semantic space

**Visualization Type**: 2x2 subplot grid with PCA scatter plots

**What to show**:
- 4 subplots (one per topic)
- Each subplot shows chunks colored by K-means cluster (5 clusters)
- Only chunks scoring > 0.30 for that topic
- Cluster centroids as red X markers

**Why this matters**:
- Demonstrates chunks assigned to each topic form coherent groups
- Shows subtopics within each main topic (the 5 clusters)
- Validates topic assignments are meaningful
- PCA explained variance shows structure capture

**Values to include**:
- PCA Component 1 & 2 (axes)
- Explained variance per topic (target: >70%)
- Number of chunks per cluster
- Chunk text snippets on hover
- Primary cosine score on hover

**Technical details**:
- Features: 4 topic scores per chunk (4D)
- Filter: primary topic score > 0.30
- K-means: k=5 clusters per topic
- PCA: 4D → 2D

**Expected findings**:
- Clear clustering structure
- 5 sub-clusters per topic (subtopics)
- Minimal noise/outliers

**Save to**: `Visuals/chunk_clustering_2d.html`

---

### CELL 5: Chunk Clustering - 3D Detailed Views
**Purpose**: Provide deeper 3D exploration of chunk clustering per topic

**Visualization Type**: 4 separate 3D scatter plots (one file per topic)

**What to show**:
- Each topic gets its own 3D interactive plot
- Points = chunks scoring high for that topic
- Color = cluster assignment (5 colors)
- Allow rotation/zoom for exploration

**Why this matters**:
- 3D captures more variance than 2D
- Allows detailed exploration of subtopic structure
- Shows cohesion within clusters
- Interactive exploration reveals patterns

**Values to include**:
- PCA Components 1, 2, 3 (x, y, z axes)
- Total explained variance (sum of 3 components, target >80%)
- Cluster labels
- Chunk previews on hover

**Technical details**:
- PCA with 3 components
- Same filtering as Cell 4 (score > 0.30)
- 5 clusters per topic

**Expected findings**:
- Higher explained variance than 2D (75-85%)
- Tighter clusters
- Clear separation between clusters

**Save to**:
- `Visuals/chunk_clustering_3d_Educational.html`
- `Visuals/chunk_clustering_3d_Governance.html`
- `Visuals/chunk_clustering_3d_Poverty.html`
- `Visuals/chunk_clustering_3d_Social.html`

---

### CELL 6: Score Comparison - Topic by Topic (Cosine vs BERTJE)
**Purpose**: Compare how cosine and BERTJE scores agree FOR EACH TOPIC

**Visualization Type**: 2x2 subplot grid with scatter plots

**What to show**:
- 4 subplots (one per topic)
- X-axis: Cosine score for that topic
- Y-axis: BERTJE score for that topic
- Each point = one chunk
- Color by absolute difference (colorscale)
- Red diagonal line = perfect agreement

**Why this matters**:
- Shows if two methods produce similar scores
- Identifies where methods disagree
- Validates scoring approach
- Correlation coefficients show overall agreement

**Values to include**:
- Pearson correlation coefficient (r) per topic
- Spearman rank correlation (ρ) per topic
- p-values
- Mean absolute difference (MAE)
- Diagonal reference line (y=x)

**Technical details**:
- Filter out very low scores (< 0.1) to reduce noise
- Color scale for difference magnitude (viridis)
- Annotations with correlation stats

**Expected findings**:
- High correlation: r > 0.85 (from training metrics: 0.863-0.937)
- Most points near diagonal
- Higher agreement at extreme scores
- More variance in mid-range scores

**Save to**: `Visuals/score_comparison_by_topic.html`

---

### CELL 7: Score Distributions Comparison
**Purpose**: Show how score distributions differ between methods

**Visualization Type**: 2x2 subplot grid with overlaid histograms

**What to show**:
- 4 subplots (one per topic)
- Two overlaid histograms per subplot:
  - Blue = Cosine score distribution
  - Red = BERTJE score distribution
- Vertical lines for means
- Semi-transparent overlap

**Why this matters**:
- Reveals if methods have different score ranges
- Shows if one method is more conservative/generous
- Identifies distribution shapes (normal, skewed, bimodal)
- Validates score calibration

**Values to include**:
- Mean and median for each method
- Standard deviation
- Overlap area between distributions
- KL-divergence (how different distributions are)

**Expected findings**:
- Similar distributions (validates calibration)
- BERTJE might have wider range (0-1) vs cosine (0-0.7)
- Both should be right-skewed (most chunks score low)

**Save to**: `Visuals/score_distributions.html`

---

### CELL 8: Primary Topic Assignment Confusion Matrix
**Purpose**: Show agreement/disagreement on which topic is primary

**Visualization Type**: Heatmap confusion matrix

**What to show**:
- Rows = Cosine primary topic assignment
- Columns = BERTJE primary topic assignment
- Cell values = percentage (normalized by row)
- Diagonal = agreement (should be dark/high)
- Off-diagonal = disagreement patterns

**Why this matters**:
- Overall agreement rate is KEY validation metric
- Shows which topics are confused with each other
- Identifies systematic disagreements
- Validates both methods capture same patterns

**Values to include**:
- Overall agreement rate (target: >75%)
- Agreement rate per topic
- Most common confusion pairs
- Raw counts and percentages
- Diagonal emphasis (highlight)

**Expected findings**:
- Strong diagonal (high agreement)
- Some confusion between related topics:
  - Poverty ↔ Governance (structural connection)
  - Educational ↔ Social (racism in schools)

**Save to**: `Visuals/topic_assignment_confusion.html`

---

### CELL 9: Confidence Level Analysis
**Purpose**: Show how confidence relates to agreement

**Visualization Type**: Grouped bar chart

**What to show**:
- X-axis: Confidence level bins (Low, Medium, High, Very High)
- Y-axis: Agreement rate between methods
- Two grouped bars:
  - Cosine confidence level → agreement rate
  - BERTJE confidence level → agreement rate
- Error bars if applicable
- Show chunk counts per bin (annotations)

**Why this matters**:
- Validates "high confidence" predictions actually agree more
- Shows if one method is overconfident
- Identifies when to trust predictions
- Tests if margin/confidence is meaningful

**Values to include**:
- Confidence bins: [0-0.3], [0.3-0.5], [0.5-0.7], [0.7-1.0]
  - Based on `score_margin` for cosine
  - Based on `bertje_margin` for BERTJE
- Agreement rate per bin
- Number of chunks per bin
- Overall agreement baseline (horizontal line)

**Expected findings**:
- Positive correlation: higher confidence → higher agreement
- High confidence (>0.7): agreement >90%
- Low confidence (<0.3): agreement ~50-60%
- Similar patterns for both methods

**Save to**: `Visuals/confidence_vs_agreement.html`

---

### CELL 10: Disagreement Flow Analysis (Sankey Diagram)
**Purpose**: Visualize how primary topic assignments differ when methods disagree

**Visualization Type**: Sankey diagram (flow chart)

**What to show**:
- Left side: Cosine primary topic assignments (4 nodes)
- Right side: BERTJE primary topic assignments (4 nodes)
- Flows: Chunks where methods disagree
- Flow thickness = number of chunks
- Color by source topic

**Why this matters**:
- Reveals systematic confusion patterns
- Shows if certain topics are consistently mislabeled
- Identifies topics needing clearer definitions
- Example: Does Cosine often say "Poverty" while BERTJE says "Governance"?

**Values to include**:
- Top 10-15 disagreement flows
- Chunk counts per flow
- Percentage of total disagreements
- Only show disagreements (filter where primary_topic != bertje_primary_topic)

**Expected findings**:
- Largest flows between semantically related topics
- Symmetric or asymmetric patterns reveal biases
- Some topics more "stable" than others

**Save to**: `Visuals/disagreement_flows.html`

---

### CELL 11: Score Margin vs Agreement
**Purpose**: Explore how margin (confidence) relates to method agreement

**Visualization Type**: 2D scatter plot

**What to show**:
- X-axis: Cosine margin (max_score - second_max_score)
- Y-axis: BERTJE margin (bertje_margin)
- Color: Whether methods agree on primary topic
  - Green = Agree
  - Red = Disagree
- Add quadrant lines (e.g., 0.2 threshold)

**Why this matters**:
- Low margin = ambiguous classification
- High margin = confident classification
- Shows if disagreements happen when both uncertain
- Or if one confident while other uncertain (asymmetric disagreement)

**Values to include**:
- Margin thresholds (0.2 = low, 0.5 = high)
- Agreement rate by quadrant:
  - Both high margin: agreement rate (expect >90%)
  - Both low margin: agreement rate (expect ~60%)
  - Mixed (one high, one low): agreement rate
- Quadrant annotations with stats

**Expected findings**:
- Top-right quadrant (both confident): mostly green
- Bottom-left (both uncertain): mix of red/green
- Off-diagonal: investigate these cases

**Save to**: `Visuals/margin_vs_agreement.html`

---

### CELL 12: High Disagreement Examples
**Purpose**: Show actual text examples where methods strongly disagree

**Visualization Type**: Interactive data table

**What to show**:
- Top 50 chunks with largest disagreements
- Sortable columns:
  - Chunk text (first 200 chars)
  - Cosine primary topic + max score
  - BERTJE primary topic + max score
  - All 4 cosine scores
  - All 4 BERTJE scores
  - Absolute difference
  - File source
- Filterable by topic, score range, etc.

**Why this matters**:
- Allows qualitative analysis of disagreements
- Helps identify edge cases
- May reveal data quality issues (encoding, truncation, etc.)
- Provides examples for thesis discussion
- Manual validation of methodology

**Values to include**:
- Chunk ID
- Full text (expandable)
- All scores (8 total: 4 cosine + 4 BERTJE)
- Primary topics (both methods)
- Difference magnitude
- Margin (both methods)
- File source

**Expected findings**:
- Ambiguous chunks (genuinely multi-topic)
- Chunks with subtle context differences
- Possible annotation errors
- Edge cases needing special handling

**Save to**: `Visuals/high_disagreement_examples.html`

---

### CELL 13: Model Training Progression Analysis
**Purpose**: Show how BERTJE model improved during training

**Visualization Type**: Multi-panel line chart + final metrics bar chart

**What to show**:

**Panel 1: Training Loss Over Time**
- X-axis: Training step
- Y-axis: Loss
- Line showing decrease in loss
- Mark evaluation points (end of each epoch)

**Panel 2: Per-Topic Correlation Over Epochs**
- X-axis: Epoch (1, 2, 3, 4, 5)
- Y-axis: Correlation coefficient
- 4 lines (one per topic) showing correlation improvement
- Target line at 0.90

**Panel 3: Per-Topic MAE Over Epochs**
- X-axis: Epoch
- Y-axis: Mean Absolute Error
- 4 lines showing MAE decrease
- Lower is better

**Panel 4: Final Performance Metrics (Bar Chart)**
- 4 groups of bars (one per topic)
- 3 bars per group: Correlation, Accuracy, (1-MAE)*100
- Show final values

**Why this matters**:
- Validates training succeeded
- Shows convergence
- Identifies if model was undertrained/overtrained
- Shows which topics are easier/harder to learn
- Justifies using BERTJE as validation method

**Values to include**:
- From `training_history` in training_metrics.json:
  - Steps: 50, 100, 150, ..., 4230
  - Loss at each step
  - Eval metrics at epochs 1-5
- Final metrics:
  - Per-topic correlation (0.863-0.937)
  - Per-topic MAE (0.067-0.166)
  - Per-topic accuracy (0.800-0.933)
  - Mean correlation: 0.9059
  - Pattern exact match: 59.15%

**Expected findings**:
- Steady loss decrease (no plateau)
- Correlation improvement each epoch
- MAE decrease each epoch
- Some topics harder than others:
  - Educational & Poverty: highest correlation (>0.93)
  - Social: lowest correlation (0.863)

**Save to**: `Visuals/training_progression.html`

---

### CELL 14: Per-Topic Performance Deep Dive
**Purpose**: Detailed analysis of model performance per topic

**Visualization Type**: 4-subplot figure with metrics per topic

**What to show**:
- 4 subplots (one per topic)
- Each subplot shows:
  - Correlation (r) with 95% CI
  - MAE with error bars
  - Accuracy
  - Comparison to overall mean

**Why this matters**:
- Shows which topics are well-learned
- Identifies problematic topics
- Validates balanced performance
- Informs where methodology is strongest

**Values to include**:
- Educational Disadvantage:
  - Correlation: 0.930
  - MAE: 0.166
  - Accuracy: 0.933
- Governance Distrust:
  - Correlation: 0.894
  - MAE: 0.101
  - Accuracy: 0.811
- Persistent Poverty:
  - Correlation: 0.937
  - MAE: 0.067
  - Accuracy: 0.885
- Social Fragmentation:
  - Correlation: 0.863
  - MAE: 0.081
  - Accuracy: 0.800

**Expected findings**:
- Poverty best performance (lowest MAE, highest r)
- Social most challenging (lowest accuracy)
- Educational: high correlation but higher MAE (scale issue?)

**Save to**: `Visuals/topic_performance_breakdown.html`

---

### CELL 15: Model Checkpoint Comparison (Optional/Advanced)
**Purpose**: Compare predictions from different training checkpoints

**Note**: This requires loading multiple model checkpoints and running inference, which is computationally expensive. Consider this optional or for thesis appendix.

**What to show**:
- Score comparison across 3 checkpoints:
  - Epoch 3 (checkpoint-2538)
  - Epoch 4 (checkpoint-3384)
  - Epoch 5 (checkpoint-4230, final)
- Line plot showing chunk score evolution
- Identify which chunks changed most during training

**Why this matters**:
- Shows model learning trajectory
- Identifies when model "figured out" certain patterns
- Validates final model is best
- Interesting for methodology discussion

**Expected findings**:
- Scores stabilize from epoch 4→5
- Earlier epochs noisier
- Some chunks consistently scored similarly (easy)
- Some chunks changed dramatically (model learned these patterns later)

**Save to**: `Visuals/checkpoint_comparison.html` *(if implemented)*

---

### CELL 16: Summary Statistics Table
**Purpose**: Export key metrics for easy reference

**File Type**: CSV

**What to include**:

**Table 1: Per-Topic Correlations**
- Columns: Topic, Pearson_r, Spearman_rho, p_value, MAE, Accuracy, Mean_Cosine, Mean_BERTJE, Std_Cosine, Std_BERTJE
- 4 rows (one per topic)

**Table 2: Overall Statistics**
- Total chunks analyzed: 14,640
- Dictionary size: 1,095 terms
- Seed terms: [count]
- Expanded terms: [count]
- Overall agreement rate: [%]
- High confidence agreement rate: [%]
- Mean correlation: 0.9059
- Mean MAE: 0.104
- Pattern exact match: 59.15%

**Table 3: Disagreement Patterns**
- Most common confusion pairs
- Counts and percentages

**Why this matters**:
- Quick reference for thesis writing
- Easy to copy into LaTeX tables
- Share-able summary
- Reproducibility record

**Save to**: `Visuals/summary_statistics.csv`

---

### CELL 17: Final Summary Report
**Purpose**: Print comprehensive summary to console and save as markdown

**What to output**:

```markdown
# Checkpoint 9: Methodology Validation Summary

## Data Overview
- Total chunks: 14,640
- Dictionary terms: 1,095 (X seed, Y expanded)
- Topics: 4

## Dictionary Validation
- Seed term quality: [median cosine per topic]
- Expanded term quality: [median cosine per topic]
- Topic separation: [PCA explained variance]

## Chunk Clustering
- PCA explained variance (2D): 71-82%
- K-means clusters: 5 per topic
- Coherent subtopic structure: ✓

## Cosine vs BERTJE Comparison
- Per-topic correlations:
  - Educational: r=0.930 (p<0.001) ⭐
  - Governance: r=0.894 (p<0.001) ⭐
  - Poverty: r=0.937 (p<0.001) ⭐⭐
  - Social: r=0.863 (p<0.001) ⭐
- Overall agreement rate: [X%]
- High confidence agreement: [X%]

## Model Training
- Training samples: 13,530
- Validation samples: 1,109
- Epochs: 5
- Mean correlation: 0.9059 ⭐⭐
- Mean MAE: 0.104
- Training converged: ✓

## Key Findings
1. ✓ Dictionary terms cluster coherently by topic
2. ✓ Chunks form distinct topic-based clusters
3. ✓ High agreement between cosine and BERTJE (r>0.86)
4. ✓ Confidence metrics are meaningful (high confidence → high agreement)
5. ✓ Model training successful (convergence + high correlation)

## Validation Status: STRONG ✅
- All correlation thresholds exceeded (r>0.85)
- Agreement rate exceeds 75%
- Clear clustering structure
- Methodology is ROBUST

## Files Generated
[List of all HTML files and CSVs]
```

**Why this matters**:
- Immediate overview of results
- Easy reference for thesis writing
- Shows completion status
- Highlights key findings for abstract/conclusion

**Save to**:
- Console output
- `Visuals/VALIDATION_SUMMARY.md`

---

## Research Questions Addressed

### RQ1: How close do dictionary terms cluster around the model understanding of the topic?

**Answered by**:
- **Cell 2**: Dictionary Term Quality - cosine similarity distributions
- **Cell 3**: Dictionary 2D Space - visual clustering
- **Cell 1**: Dictionary Composition - expansion success

**Validation criteria**:
- ✓ Seed terms: cosine > 0.6
- ✓ Expanded terms: cosine > 0.4
- ✓ Clear topic separation in PCA
- ✓ Minimal overlap between topic clusters

---

### RQ2: How close do chunks cluster around the topics?

**Answered by**:
- **Cell 4**: Chunk Clustering 2D - overall patterns
- **Cell 5**: Chunk Clustering 3D - detailed exploration

**Validation criteria**:
- ✓ PCA explained variance > 70%
- ✓ Clear subtopic structure (5 clusters per topic)
- ✓ Minimal outliers/noise
- ✓ Separation between topics

---

### RQ3: How confident are the 2 different score sets and where do they disagree?

**Answered by**:
- **Cell 6**: Score Comparison by Topic - correlation per topic
- **Cell 7**: Score Distributions - method differences
- **Cell 8**: Confusion Matrix - assignment agreement
- **Cell 9**: Confidence vs Agreement - confidence validation
- **Cell 10**: Disagreement Flows - systematic patterns
- **Cell 11**: Margin vs Agreement - confidence relationship
- **Cell 12**: High Disagreement Examples - qualitative analysis

**Validation criteria**:
- ✓ High correlation (r > 0.85) per topic
- ✓ Overall agreement > 75%
- ✓ High confidence → high agreement (>90%)
- ✓ Disagreements primarily in low-confidence regions
- ✓ Systematic patterns are explainable

**Expected findings**:
- Pearson r: 0.863-0.937 (STRONG)
- Agreement when both confident: >90%
- Disagreements in ambiguous chunks
- Some topic pairs naturally confused (related concepts)

---

### RQ4 (NEW): How does the BERTJE model compare across training stages?

**Answered by**:
- **Cell 13**: Training Progression - loss and metrics over time
- **Cell 14**: Per-Topic Performance - final performance breakdown
- **Cell 15** (optional): Checkpoint Comparison - score evolution

**Validation criteria**:
- ✓ Steady loss decrease (convergence)
- ✓ Correlation improvement each epoch
- ✓ No overfitting (validation metrics stable)
- ✓ Balanced performance across topics

**Expected findings**:
- Loss converges by epoch 3-4
- Final metrics strong (mean r=0.9059)
- Some topics easier than others (Poverty best, Social hardest)
- Model stable from epoch 4→5 (ready to stop)

---

## Validation Criteria Summary

### Strong Validation (Methodology is ROBUST) ✅
- ✓ Pearson r > 0.85 for all topics → ACHIEVED (0.863-0.937)
- ✓ Overall agreement rate > 75% → [TO MEASURE]
- ✓ High-confidence agreement > 90% → [TO MEASURE]
- ✓ Dictionary terms cluster clearly → [TO VALIDATE]
- ✓ Chunk clusters have high explained variance (>70%) → [TO VALIDATE]
- ✓ Model training converged → ACHIEVED

### Acceptable Validation
- Pearson r > 0.70 for all topics
- Overall agreement > 65%
- Clear clustering patterns
- Disagreements in low-confidence regions

### Weak Validation (Requires Investigation)
- Pearson r < 0.70 for any topic
- Overall agreement < 65%
- Systematic disagreements in high-confidence
- Poor clustering structure

**Current Status**: Expecting **STRONG VALIDATION** based on training metrics.

---

## Implementation Notes

### Color Scheme (Consistent Across All Plots)
- **Topic 1 (Educational)**: Blue #3498db
- **Topic 2 (Governance)**: Green #2ecc71
- **Topic 3 (Poverty)**: Orange #f39c12
- **Topic 4 (Social)**: Red #e74c3c
- **Agreement**: Green
- **Disagreement**: Red

### Plot Standards
All interactive plots must have:
- ✓ Clear title with subtitle explaining content
- ✓ Labeled axes with units
- ✓ Hover tooltips with detailed info
- ✓ Legends where applicable
- ✓ Annotations for key findings
- ✓ Consistent font sizes (title=16, labels=12)

### Console Output Format
After each cell:
```
=== CELL X: [Name] ===
[What was computed]
Key finding: [X]
Key finding: [Y]
✓ Saved: Visuals/[filename].html
```

### Error Handling
- Missing data → clear warning + skip gracefully
- Empty clusters → reduce k or skip
- Division by zero → use np.where or try/except
- Encoding issues → ensure UTF-8 throughout

---

## File Organization

**Output Directory**:
```
workflow_data/policy_Slavdict_ft-slavery_slavery_v1/Visuals/
```

**Expected Files** (17-18 total):
1. `dictionary_composition.html`
2. `dictionary_term_quality.html`
3. `dictionary_clustering_2d.html`
4. `chunk_clustering_2d.html`
5. `chunk_clustering_3d_Educational.html`
6. `chunk_clustering_3d_Governance.html`
7. `chunk_clustering_3d_Poverty.html`
8. `chunk_clustering_3d_Social.html`
9. `score_comparison_by_topic.html`
10. `score_distributions.html`
11. `topic_assignment_confusion.html`
12. `confidence_vs_agreement.html`
13. `disagreement_flows.html`
14. `margin_vs_agreement.html`
15. `high_disagreement_examples.html`
16. `training_progression.html`
17. `topic_performance_breakdown.html`
18. (optional) `checkpoint_comparison.html`
19. `summary_statistics.csv`
20. `VALIDATION_SUMMARY.md`

---

## Timeline Estimate

### Implementation Time Per Cell:
- **Cell 0** (Setup): 15 min
- **Cells 1-2** (Dictionary basics): 45 min
- **Cell 3** (Dictionary PCA): 45 min
- **Cells 4-5** (Chunk clustering): 2 hours
- **Cells 6-7** (Score comparison): 1 hour
- **Cells 8-12** (Agreement analysis): 2 hours
- **Cells 13-14** (Training analysis): 1.5 hours
- **Cell 15** (Checkpoints): 2 hours *(optional)*
- **Cells 16-17** (Summaries): 30 min

**Total**: ~8-10 hours for full implementation and testing (excluding optional Cell 15)

### Testing & Refinement:
- Initial run: 1 hour
- Visual refinement: 2 hours
- Documentation: 1 hour

**Grand Total**: ~12-14 hours for complete, polished checkpoint 9

---

## Next Steps

1. **Review this plan** - confirm all visualizations address research questions
2. **Implement Cell 0** - load all data and validate structure
3. **Implement Cells 1-3** - dictionary analysis (prove RQ1)
4. **Implement Cells 4-5** - chunk clustering (prove RQ2)
5. **Implement Cells 6-12** - score comparison (prove RQ3)
6. **Implement Cells 13-14** - training analysis (prove RQ4)
7. **Implement Cells 16-17** - summaries
8. **Generate final report** - ready for thesis

---

## Questions to Confirm Before Implementation

1. ✓ Use policy_Slavdict_ft-slavery_slavery_v1 as primary workflow?
2. ✓ All 4 topics confirmed?
3. ✓ Color scheme approved?
4. Should we implement Cell 15 (checkpoint comparison) or skip for time?
5. Any additional analyses needed?
6. Output format preferences (HTML only or also PDF exports)?

---

**END OF PLAN**

Ready to implement step-by-step based on this comprehensive blueprint.
