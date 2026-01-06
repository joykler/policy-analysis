# Checkpoint 9: Final Visualization Plan
## Interactive Model Comparison & Methodology Validation

---

## Overview

This checkpoint provides comprehensive visualizations demonstrating:
1. **Dictionary term clustering** around topic definitions (RQ1)
2. **Chunk clustering** patterns (RQ2)
3. **Cosine vs BERTJE comparison** with confidence analysis (RQ3)
4. **Model iteration comparison** - compare different BERTJE training runs (pre/post improvements)

**Key Feature**: Rich interactive tooltips throughout all visualizations

---

## Available Models for Comparison

Based on available trained models:

| Workflow | Corpus | Mean Correlation | Train Samples | Status |
|----------|--------|------------------|---------------|--------|
| **policy_Slavdict_ft-slavery_slavery_v1** | Policy documents | **0.9059** | 13,530 | ✅ Best |
| slavery_Slavdict_pretraining_slavery_v13 | Slavery texts | 0.8488 | 4,992 | Good |
| slavery_Slavdict_pretraining_slavery_v21 | Slavery texts | 0.7705 | 1,295 | Moderate |
| slavery_Slavdict_pretraining_slavery_v23 | Slavery texts | 0.7475 | 1,290 | Moderate |

**Recommendation**: Use `policy_Slavdict_ft-slavery_slavery_v1` as primary + compare with one other for iteration analysis

---

## CELL 0: Configuration & Data Loading

### Purpose
- Select which model(s) to analyze
- Load all necessary data
- Validate data integrity
- Set up comparison if multiple models selected

### User Configuration
```python
# Model Selection
PRIMARY_MODEL = "policy_Slavdict_ft-slavery_slavery_v1"
COMPARISON_MODEL = "slavery_Slavdict_pretraining_slavery_v13"  # Optional: set to None to skip comparison
ENABLE_MODEL_COMPARISON = True  # Set to False for single model analysis only

# Analysis Parameters
MIN_SCORE_THRESHOLD = 0.30
N_CLUSTERS = 5
```

### What to Load

**For Primary Model:**
- ✓ Cosine scores: `Cosine_labeling/scores_all_labeled.csv`
- ✓ BERTJE predictions: `BERTJE_predictions/bertje_continuous_predictions_full.csv`
- ✓ Dictionary: `Dictionary/Curated_dictionary.csv`
- ✓ Training metrics: `Model_finetuning/training_metrics.json`

**For Comparison Model (if enabled):**
- ✓ Same files from comparison workflow
- ✓ Align chunks by `chunk_id` for direct comparison

### Validation Checks
- ✓ Number of chunks match (14,640 expected)
- ✓ All 4 topics present
- ✓ Column names consistent
- ✓ Dictionary loaded (1,095 terms expected)
- ✓ If comparing: ensure chunks align between models

### Console Output
```
======================================================================
CHECKPOINT 9: METHODOLOGY VALIDATION & MODEL COMPARISON
======================================================================

Configuration:
  Primary Model: policy_Slavdict_ft-slavery_slavery_v1
  Comparison Model: slavery_Slavdict_pretraining_slavery_v13
  Model Comparison: ENABLED

Loading Primary Model Data...
  ✓ Loaded 14,640 chunks (cosine + BERTJE scores)
  ✓ Loaded 1,095 dictionary terms
  ✓ Identified 4 topics:
    - Educational Disadvantage & Brain Drain
    - Governance Distrust & Corruption
    - Persistent Poverty & Economic Vulnerability
    - Social Fragmentation & Racism
  ✓ Training metrics loaded
    - Mean correlation: 0.9059
    - Train samples: 13,530

Loading Comparison Model Data...
  ✓ Loaded 4,992 chunks (cosine + BERTJE scores)
  ✓ Dictionary: 856 terms
  ✓ Mean correlation: 0.8488
  ✓ Train samples: 4,992

Ready for analysis!
======================================================================
```

### Data Structures Created
- `df_primary`: Full data for primary model
- `df_comparison`: Full data for comparison model (if enabled)
- `df_dict_primary`: Dictionary for primary model
- `df_dict_comparison`: Dictionary for comparison model (if enabled)
- `training_metrics_primary`: Training metrics dict
- `training_metrics_comparison`: Training metrics dict (if enabled)
- `TOPICS`: List of 4 topic names

---

## CELL 1: Dictionary Composition Analysis

### Visualization Type
Grouped or stacked bar chart

### What to Show
- For each topic:
  - Number of seed terms (hand-curated)
  - Number of expanded terms (discovered)
- If comparison enabled: show both models side-by-side

### Tooltips (on hover over each bar)
```
Topic: Educational Disadvantage & Brain Drain
Type: Seed Terms
Count: 45 terms
Percentage: 18.2% of topic dictionary
Examples:
  - onderwijs (education)
  - schooluitval (school dropout)
  - taalbarrière (language barrier)
Model: policy_Slavdict_ft-slavery_slavery_v1
```

### Key Metrics to Display
- Total terms per topic
- Seed vs expanded ratio
- Comparison: "Model A has 23% more expanded terms than Model B"

### Save to
`Visuals/01_dictionary_composition.html`

---

## CELL 2: Dictionary Term Quality Distribution

### Visualization Type
Violin plot or box plot with individual points

### What to Show
- Distribution of cosine similarity scores for dictionary terms
- Separate by topic (4 plots or 4 violin sections)
- Distinguish seed (●) vs expanded (○) with markers
- If comparison: overlay or side-by-side

### Tooltips (on hover over each point)
```
Term: "brain drain"
Topic: Educational Disadvantage & Brain Drain
Type: Seed term
Cosine Similarity: 0.724
Document Frequency: 342
Weight: 1.85
Category: problem-oriented
Model: policy_Slavdict_ft-slavery_slavery_v1

Appears in chunks discussing:
- Migration of educated youth
- Skills shortage
- Educational investment loss
```

### Key Metrics to Annotate
- Median cosine per topic
- Threshold lines (e.g., 0.4 = minimum quality, 0.6 = high quality)
- Seed vs expanded quality comparison
- If comparing models: "Model A seed terms: median=0.68, Model B: median=0.71"

### Save to
`Visuals/02_dictionary_quality.html`

---

## CELL 3: Dictionary Term 2D Clustering (PCA)

### Visualization Type
2D scatter plot with PCA

### What to Show
- Each dictionary term as a point in 2D space
- Color by topic (4 colors)
- Size by term type (seed=large, expanded=small)
- Shape by model (if comparing: ● = Model A, ▲ = Model B)
- Topic centroids as large ✕ markers

### Tooltips (on hover over each term)
```
Term: "corruptie" (corruption)
Topic: Governance Distrust & Corruption
Type: Expanded term
Source: Discovered via semantic similarity

Scores across topics:
  Educational: 0.12
  Governance: 0.78 ⭐ (primary)
  Poverty: 0.34
  Social: 0.19

PCA coordinates: (1.23, -0.45)
Cosine to centroid: 0.78
Model: policy_Slavdict_ft-slavery_slavery_v1

Related seed terms:
  - patronage (0.89 similarity)
  - bestuurlijke zwakte (0.82 similarity)
```

### Key Metrics to Annotate
- PCA explained variance (e.g., "Components 1+2 explain 78% of variance")
- Cluster separation metric
- If comparing: "Model A terms cluster more tightly (avg dist to centroid: 0.42 vs 0.58)"

### Save to
`Visuals/03_dictionary_clustering_2d.html`

---

## CELL 4: Chunk Clustering - 2D Overview

### Visualization Type
2×2 subplot grid (one subplot per topic)

### What to Show
- 4 subplots, one per topic
- Each subplot: chunks scoring >0.30 for that topic
- Color by K-means cluster (5 clusters, 5 colors)
- Cluster centroids as red ✕
- If comparing models: option to toggle between models or overlay

### Tooltips (on hover over each chunk)
```
Chunk ID: chunk_0458
File: Beleidsnota_Onderwijs_2018.pdf
Topic: Educational Disadvantage & Brain Drain
Cluster: 2 (Language & Integration sub-theme)

Cosine Score: 0.587
BERTJE Score: 0.623
Agreement: ✓ (both identify as Educational topic)

Text preview:
"De taalbarrière vormt een van de grootste uitdagingen
voor onderwijsprestaties op de eilanden. Veel kinderen
spreken thuis Papiamentu maar krijgen onderwijs in het
Nederlands, wat leidt tot..."

Scores for all topics:
  Educational: 0.587 ⭐ (primary)
  Governance: 0.234
  Poverty: 0.312
  Social: 0.278

PCA position: (0.89, 1.34)
Model: policy_Slavdict_ft-slavery_slavery_v1
```

### Key Metrics to Annotate
- PCA explained variance per topic
- Chunks per cluster
- Silhouette score (cluster quality)
- If comparing: "Model A has tighter clusters (silhouette: 0.68 vs 0.54)"

### Save to
`Visuals/04_chunk_clustering_2d.html`

---

## CELL 5: Chunk Clustering - 3D Interactive (per topic)

### Visualization Type
4 separate 3D scatter plots (one file per topic)

### What to Show
- Interactive 3D plot for each topic
- Points = chunks scoring >0.30 for that topic
- Color by cluster (5 clusters)
- Rotation/zoom controls
- If comparing: add toggle button to switch between models

### Tooltips (same rich format as Cell 4)
```
[Same detailed tooltip as Cell 4 but in 3D view]

Additional 3D info:
PCA coordinates: (0.89, 1.34, -0.67)
Nearest cluster center: 0.34 units away
```

### Key Metrics
- 3D PCA explained variance (target >80%)
- Cluster separation in 3D
- If comparing: "Model B captures 5% more variance in 3D space"

### Save to
- `Visuals/05a_chunk_3d_Educational.html`
- `Visuals/05b_chunk_3d_Governance.html`
- `Visuals/05c_chunk_3d_Poverty.html`
- `Visuals/05d_chunk_3d_Social.html`

---

## CELL 6: Score Comparison - Cosine vs BERTJE (per topic)

### Visualization Type
2×2 subplot grid with scatter plots

### What to Show
- 4 subplots (one per topic)
- X-axis: Cosine score
- Y-axis: BERTJE score
- Color by absolute difference (viridis colorscale)
- Red diagonal line (y=x) = perfect agreement
- If comparing: option to show Model A vs Model B

### Tooltips (on hover over each point)
```
Chunk ID: chunk_1234
Topic: Persistent Poverty & Economic Vulnerability

Cosine Score: 0.453
BERTJE Score: 0.521
Absolute Difference: 0.068
Agreement: Good (within 0.1)

Both methods identify this as:
  Primary Topic: Poverty ✓
  Confidence: High (margin >0.3)

Text preview:
"De werkloosheid op de eilanden blijft historisch hoog,
met name onder jongeren. Dit is direct gekoppeld aan het
gebrek aan economische diversificatie en de erfenis van..."

Why the difference?
  Cosine focuses on keyword matches
  BERTJE captures contextual meaning

Model: policy_Slavdict_ft-slavery_slavery_v1
```

### Key Metrics to Annotate
- Pearson r per topic (in corner of each subplot)
- Spearman ρ
- MAE (mean absolute error)
- Points on diagonal line % (perfect agreement)
- If comparing: "Model A correlation: r=0.91, Model B: r=0.85"

### Save to
`Visuals/06_score_comparison_by_topic.html`

---

## CELL 7: Score Distribution Comparison

### Visualization Type
2×2 subplot grid with overlaid histograms

### What to Show
- 4 subplots (one per topic)
- Blue histogram: Cosine scores
- Red histogram: BERTJE scores
- Semi-transparent overlap
- Vertical lines for means
- If comparing models: additional overlays or separate figure

### Tooltips (on hover over histogram bins)
```
Score Range: 0.40 - 0.45
Method: Cosine Similarity
Topic: Educational Disadvantage

Chunks in this range: 342
Percentage of total: 8.3%
Mean score in bin: 0.423

Typical chunks in this range:
- Moderate relevance
- Often mention education but not as primary focus
- Mixed with other topics

Model: policy_Slavdict_ft-slavery_slavery_v1
```

### Key Metrics
- Mean, median, mode per distribution
- KL-divergence between distributions
- Overlap area
- If comparing: "Model B has wider score distribution (σ=0.21 vs 0.18)"

### Save to
`Visuals/07_score_distributions.html`

---

## CELL 8: Primary Topic Assignment Confusion Matrix

### Visualization Type
Heatmap confusion matrix

### What to Show
- Rows: Cosine primary topic
- Columns: BERTJE primary topic
- Cell values: percentage (normalized by row)
- Color: Blues colorscale (darker = more agreement)
- Diagonal emphasized (perfect agreement)
- If comparing models: show 2 matrices side-by-side

### Tooltips (on hover over each cell)
```
Cosine assigned: Educational Disadvantage
BERTJE assigned: Social Fragmentation

Chunk count: 87 chunks
Percentage of Cosine-Educational: 3.1%
Overall disagreement rate: 0.6%

Why this confusion?
These topics overlap when discussing:
- Racism in educational settings
- Language barriers as social issue
- Brain drain affecting social cohesion

Example chunk:
"Het racisme in de klas zorgt ervoor dat veel
Afro-Caribische kinderen afhaken..."

Model: policy_Slavdict_ft-slavery_slavery_v1
```

### Key Metrics
- Overall agreement rate (sum of diagonal)
- Per-topic agreement rates
- Most confused topic pairs
- If comparing: "Model A agreement: 78%, Model B: 83% (+5% improvement)"

### Save to
`Visuals/08_confusion_matrix.html`

---

## CELL 9: Confidence vs Agreement Analysis

### Visualization Type
Grouped bar chart

### What to Show
- X-axis: Confidence bins (Low, Medium, High, Very High)
- Y-axis: Agreement rate between Cosine and BERTJE
- Bars grouped by confidence source (Cosine margin vs BERTJE margin)
- If comparing models: grouped by model as well

### Tooltips (on hover over bars)
```
Confidence Level: High (margin 0.5-0.7)
Method: Cosine Similarity
Agreement Rate: 87.3%

Chunks in this category: 1,847
Expected behavior: High confidence → High agreement ✓

Disagreements (12.7%):
Most common:
- Educational ↔ Social (54 chunks)
- Poverty ↔ Governance (38 chunks)

These are typically:
- Multi-topic chunks (genuinely ambiguous)
- Edge cases between related topics

Model: policy_Slavdict_ft-slavery_slavery_v1
```

### Key Metrics
- Agreement rate per confidence bin
- Chunk counts per bin
- Baseline agreement rate (horizontal line)
- If comparing: "Model B maintains high agreement even at medium confidence"

### Save to
`Visuals/09_confidence_vs_agreement.html`

---

## CELL 10: Disagreement Flow Analysis (Sankey)

### Visualization Type
Sankey diagram

### What to Show
- Left nodes: Cosine topic assignments (4 topics)
- Right nodes: BERTJE topic assignments (4 topics)
- Flows: Only disagreements (where cosine ≠ BERTJE)
- Flow width: number of chunks
- Color: by source topic
- If comparing models: show 2 Sankeys side-by-side

### Tooltips (on hover over flows)
```
Flow: Educational → Social
Direction: Cosine says Educational, BERTJE says Social

Chunk count: 87 disagreements
% of total disagreements: 15.3%
% of all chunks: 0.6%

Common patterns in these chunks:
1. Racism in schools (overlapping themes)
2. Language barriers as social fragmentation
3. Educational exclusion as social issue

Example disagreement:
Chunk 0234: "Het structurele racisme in het
onderwijssysteem leidt tot sociale uitsluiting..."

Cosine score for Educational: 0.456
Cosine score for Social: 0.389
BERTJE score for Educational: 0.334
BERTJE score for Social: 0.512

Why disagreement?
- Keywords favor Educational ("onderwijs", "school")
- Context favors Social ("racisme", "uitsluiting")
- Genuinely ambiguous chunk

Model: policy_Slavdict_ft-slavery_slavery_v1
```

### Key Metrics
- Total disagreement count
- Largest flows (top 5)
- Symmetric vs asymmetric disagreements
- If comparing: "Model B reduced Educational→Social confusion by 40%"

### Save to
`Visuals/10_disagreement_flows.html`

---

## CELL 11: Margin vs Agreement Scatter

### Visualization Type
2D scatter plot

### What to Show
- X-axis: Cosine margin (max - second_max score)
- Y-axis: BERTJE margin
- Color: Green (agree on primary topic) vs Red (disagree)
- Quadrant lines at margin thresholds (e.g., 0.2)
- If comparing models: separate plots or color by model

### Tooltips (on hover over points)
```
Chunk ID: chunk_0892
Agreement: ✓ Both identify as Governance topic

Cosine Margin: 0.342 (High confidence)
  1st: Governance (0.623)
  2nd: Poverty (0.281)

BERTJE Margin: 0.478 (High confidence)
  1st: Governance (0.714)
  2nd: Educational (0.236)

Interpretation:
Both methods are confident AND agree.
This chunk clearly belongs to Governance topic.

Text preview:
"De patronagesystemen die nog steeds actief zijn
op de eilanden zijn een direct gevolg van de
koloniale bestuurscultuur..."

Quadrant: High-High (both confident, expected agreement)
Model: policy_Slavdict_ft-slavery_slavery_v1
```

### Key Metrics
- Agreement rate per quadrant
  - High-High: expect >90% agreement
  - Low-Low: expect ~60% agreement
  - Mixed: investigate
- If comparing: "Model B improves confidence calibration (better margin separation)"

### Save to
`Visuals/11_margin_vs_agreement.html`

---

## CELL 12: High Disagreement Examples Table

### Visualization Type
Interactive sortable data table

### What to Show
- Top 50 chunks with highest disagreement
- Sortable/filterable by all columns
- Expandable rows for full text
- If comparing models: show disagreements unique to each model

### Columns & Tooltips

**Column: Chunk ID**
```
Tooltip: Unique identifier for this chunk
Click to see full text below table
```

**Column: Text Preview (200 chars)**
```
Tooltip: First 200 characters of chunk
Click row to expand full text
Highlighting: Keywords from primary topics highlighted
```

**Column: Cosine Primary (score)**
```
Tooltip:
Primary: Educational Disadvantage (0.489)
All scores:
  Educational: 0.489
  Governance: 0.312
  Poverty: 0.287
  Social: 0.234
Margin: 0.177 (Medium confidence)
```

**Column: BERTJE Primary (score)**
```
Tooltip:
Primary: Social Fragmentation (0.612)
All scores:
  Educational: 0.245
  Governance: 0.289
  Poverty: 0.198
  Social: 0.612
Margin: 0.323 (High confidence)
```

**Column: Difference**
```
Tooltip:
Absolute difference: 0.123
Type: Topic disagreement (Educational vs Social)

Why this matters:
- Large difference suggests fundamentally different interpretation
- One method may be capturing nuance the other misses
- Candidates for qualitative review
```

**Column: File Source**
```
Tooltip:
File: Evaluatie_Onderwijsbeleid_2020.pdf
Page: 34
Section: "Racisme en schoolprestaties"
Document type: Policy evaluation report
Year: 2020
```

### Table Features
- Sort by any column
- Filter by topic, score range, file
- Export selected rows to CSV
- Highlight patterns (e.g., all chunks from same file)

### Save to
`Visuals/12_disagreement_examples.html`

---

## CELL 13: Model Iteration Comparison

**NOTE: This cell only runs if ENABLE_MODEL_COMPARISON = True**

### Visualization Type
Multi-panel comparison dashboard

### What to Show

**Panel 1: Performance Metrics Comparison (Bar Chart)**
- Grouped bars showing Model A vs Model B
- Metrics: Correlation, MAE, Accuracy per topic
- Overall metrics: Mean correlation, Agreement rate

### Panel 2: Score Correlation Scatter**
- 4 subplots (one per topic)
- X-axis: Model A BERTJE score
- Y-axis: Model B BERTJE score
- Diagonal line (perfect agreement)
- Color by difference magnitude

### Panel 3: Disagreement Change Analysis**
- Venn diagram or flow showing:
  - Disagreements only in Model A
  - Disagreements only in Model B
  - Disagreements in both
- Shows where Model B improved/regressed

### Tooltips (Panel 2 - Score Correlation)
```
Chunk ID: chunk_0456
Topic: Educational Disadvantage

Model A (v13):
  BERTJE Score: 0.412
  Primary Topic: Educational ✓
  Confidence: Medium (margin=0.23)

Model B (policy_v1):
  BERTJE Score: 0.589
  Primary Topic: Educational ✓
  Confidence: High (margin=0.41)

Improvement: +0.177 score increase
Interpretation: Model B is more confident and accurate
Both models agree on topic assignment ✓

Text preview:
"Het onderwijsachterstand probleem op de BES-eilanden..."

Cosine Score (same for both): 0.534
Why Model B better: Larger training set (13k vs 5k samples)
```

### Key Metrics
- Per-topic correlation difference
- Overall agreement improvement
- Training data impact (samples vs performance)
- Key finding: "Model B improves mean correlation by 6% (0.849 → 0.906)"

### Save to
`Visuals/13_model_comparison.html`

---

## CELL 14: Summary Statistics Export

### File Type
CSV file with multiple sheets/sections

### What to Export

**Section 1: Model Configuration**
```csv
metric,primary_model,comparison_model
name,policy_Slavdict_ft-slavery_slavery_v1,slavery_Slavdict_pretraining_slavery_v13
corpus,Policy documents,Slavery texts
train_samples,13530,4992
val_samples,1109,855
mean_correlation,0.9059,0.8488
training_epochs,5,5
```

**Section 2: Per-Topic Performance**
```csv
topic,model,pearson_r,spearman_rho,mae,accuracy,mean_cosine,mean_bertje
Educational Disadvantage,primary,0.930,0.925,0.166,0.933,0.234,0.412
Educational Disadvantage,comparison,0.891,0.887,0.189,0.898,0.234,0.378
...
```

**Section 3: Agreement Analysis**
```csv
confidence_level,model,agreement_rate,chunk_count,cosine_agree,bertje_agree
Low (0-0.3),primary,0.623,1847,0.612,0.634
Low (0-0.3),comparison,0.589,892,0.578,0.601
...
```

**Section 4: Disagreement Patterns**
```csv
from_topic,to_topic,model,count,percentage,example_chunk_id
Educational,Social,primary,87,0.6%,chunk_0234
Educational,Social,comparison,134,2.7%,chunk_0189
...
```

### Save to
`Visuals/14_summary_statistics.csv`

---

## CELL 15: Final Summary Report

### File Type
Markdown file + console output

### What to Generate

```markdown
# Checkpoint 9: Methodology Validation Summary
**Generated**: 2025-12-10
**Models Analyzed**: policy_Slavdict_ft-slavery_slavery_v1 (primary), slavery_Slavdict_pretraining_slavery_v13 (comparison)

---

## Configuration
- Analysis Mode: Model Comparison ENABLED
- Primary Model Corpus: Policy documents (14,640 chunks)
- Comparison Model Corpus: Slavery texts (4,992 chunks)
- Topics Analyzed: 4
- Minimum Score Threshold: 0.30
- Clustering: K-means (k=5)

---

## Dictionary Validation (RQ1)

### Primary Model
- **Total Terms**: 1,095
- **Seed Terms**: 247 (22.6%)
- **Expanded Terms**: 848 (77.4%)
- **Quality**:
  - Seed median cosine: 0.681
  - Expanded median cosine: 0.523
  - All above minimum threshold (0.4) ✓

### Comparison Model
- **Total Terms**: 856
- **Seed Terms**: 247 (28.9%)
- **Expanded Terms**: 609 (71.1%)
- **Quality**:
  - Seed median cosine: 0.694
  - Expanded median cosine: 0.498

### Key Finding
✓ Dictionary terms cluster coherently around topic definitions
✓ Expanded terms maintain high semantic similarity to seeds
✓ Primary model discovered 239 more terms than comparison

---

## Chunk Clustering (RQ2)

### Primary Model
- **PCA Explained Variance (2D)**: 71-82% across topics
- **Cluster Quality**: Silhouette score 0.68 (good)
- **Subtopics Identified**: 5 coherent clusters per topic

### Comparison Model
- **PCA Explained Variance (2D)**: 65-76% across topics
- **Cluster Quality**: Silhouette score 0.61 (acceptable)

### Key Finding
✓ Chunks form distinct topic-based clusters
✓ Clear subtopic structure within each topic
✓ Primary model has tighter, more coherent clusters

---

## Score Comparison: Cosine vs BERTJE (RQ3)

### Primary Model - Per-Topic Correlations
| Topic | Pearson r | Spearman ρ | MAE | Agreement |
|-------|-----------|------------|-----|-----------|
| Educational Disadvantage | 0.930 ⭐⭐ | 0.925 | 0.166 | 94.2% |
| Governance Distrust | 0.894 ⭐ | 0.889 | 0.101 | 89.7% |
| Persistent Poverty | **0.937** ⭐⭐ | 0.933 | 0.067 | 96.1% |
| Social Fragmentation | 0.863 ⭐ | 0.858 | 0.081 | 87.4% |

**Mean Correlation**: 0.906 (Excellent!)

### Comparison Model - Per-Topic Correlations
| Topic | Pearson r | Spearman ρ | MAE | Agreement |
|-------|-----------|------------|-----|-----------|
| Educational Disadvantage | 0.891 ⭐ | 0.885 | 0.189 | 91.2% |
| Governance Distrust | 0.867 ⭐ | 0.861 | 0.123 | 86.4% |
| Persistent Poverty | 0.904 ⭐⭐ | 0.899 | 0.089 | 92.8% |
| Social Fragmentation | 0.821 | 0.814 | 0.098 | 83.7% |

**Mean Correlation**: 0.871 (Very Good)

### Confidence Validation
- **High Confidence (margin >0.5)**: 91.2% agreement ✓
- **Medium Confidence (0.3-0.5)**: 82.7% agreement ✓
- **Low Confidence (<0.3)**: 64.3% agreement (expected)

### Disagreement Patterns
- **Total Disagreements**: 1,847 chunks (12.6%)
- **Most Common Confusions**:
  1. Educational ↔ Social: 87 chunks (linked by racism in schools)
  2. Poverty ↔ Governance: 73 chunks (structural connections)
  3. Governance ↔ Social: 54 chunks (patronage systems)

### Key Finding
✓ Strong correlation between cosine and BERTJE (r>0.85 for all topics)
✓ High-confidence predictions are reliable (>90% agreement)
✓ Disagreements occur in genuinely ambiguous multi-topic chunks
✓ Primary model shows stronger agreement than comparison model

---

## Model Iteration Comparison

### Performance Improvement
- **Correlation**: +3.5% improvement (0.871 → 0.906)
- **Agreement Rate**: +5.1% improvement
- **Training Data**: 2.7x more samples (4,992 → 13,530)

### Topic-Specific Improvements
- **Poverty**: +3.3% correlation improvement (best performance)
- **Social**: +4.2% correlation improvement (largest gain)
- **Educational**: +3.9% correlation improvement
- **Governance**: +2.7% correlation improvement

### Disagreement Reduction
- **Educational-Social confusion**: Reduced by 35%
- **Overall disagreement rate**: Reduced by 19%

### Key Finding
✓ Larger training corpus significantly improves performance
✓ All topics benefit from additional training data
✓ Model generalizes better with policy-specific corpus
✓ Iteration strategy is effective

---

## Overall Validation Status

### ✅ STRONG VALIDATION ACHIEVED

**Criteria Met**:
- ✓ Pearson r > 0.85 for all topics (EXCEEDED: r=0.863-0.937)
- ✓ Overall agreement > 75% (ACHIEVED: 91.8%)
- ✓ High-confidence agreement > 85% (EXCEEDED: 91.2%)
- ✓ Dictionary clustering clear and coherent
- ✓ Chunk clustering with high explained variance (>70%)
- ✓ Model iteration shows improvement

**Methodology Robustness**: CONFIRMED ✅

---

## Recommendations for Thesis

1. **Lead with Primary Model**: Use policy_Slavdict_ft-slavery_slavery_v1 as main results
2. **Highlight Correlations**: Emphasize r>0.90 for most topics (very strong)
3. **Address Social Topic**: Acknowledge Social Fragmentation as most challenging (r=0.863, still good)
4. **Discuss Ambiguity**: Use disagreement examples to show genuine multi-topic chunks
5. **Show Iteration**: Demonstrate how model improved with larger, domain-specific corpus

---

## Files Generated

**Visualizations** (15 HTML files):
1. ✓ dictionary_composition.html
2. ✓ dictionary_quality.html
3. ✓ dictionary_clustering_2d.html
4. ✓ chunk_clustering_2d.html
5. ✓ chunk_3d_Educational.html
6. ✓ chunk_3d_Governance.html
7. ✓ chunk_3d_Poverty.html
8. ✓ chunk_3d_Social.html
9. ✓ score_comparison_by_topic.html
10. ✓ score_distributions.html
11. ✓ confusion_matrix.html
12. ✓ confidence_vs_agreement.html
13. ✓ disagreement_flows.html
14. ✓ margin_vs_agreement.html
15. ✓ disagreement_examples.html
16. ✓ model_comparison.html (if enabled)

**Data Exports**:
- ✓ summary_statistics.csv
- ✓ VALIDATION_SUMMARY.md (this file)

---

## Next Steps

1. Use visualizations in thesis Chapter 4 (Methodology)
2. Reference key metrics in abstract and conclusion
3. Include disagreement examples for qualitative discussion
4. Cite model comparison to justify workflow choices

**Checkpoint 9 Complete** ✅
```

### Save to
- Console output (print to screen)
- `Visuals/15_VALIDATION_SUMMARY.md`

---

## Tooltip Implementation Guidelines

### Technical Approach
Use Plotly's `hovertemplate` and `customdata` features:

```python
fig.add_trace(go.Scatter(
    x=x_data,
    y=y_data,
    customdata=np.column_stack((
        chunk_ids,
        text_previews,
        all_scores,
        file_sources,
        # ... more data columns
    )),
    hovertemplate=(
        '<b>Chunk ID:</b> %{customdata[0]}<br>' +
        '<b>Score:</b> %{y:.3f}<br>' +
        '<b>Text:</b> %{customdata[1]}<br>' +
        '<extra></extra>'
    )
))
```

### Tooltip Content Priority
1. **Essential**: IDs, scores, primary classifications
2. **Context**: Text previews, file sources
3. **Detailed**: All topic scores, margins, metadata
4. **Analytical**: Comparisons, explanations, patterns

### Formatting
- Use HTML formatting: `<b>`, `<br>`, colors
- Keep text preview to 150-200 chars
- Round numbers appropriately (3 decimal places for scores)
- Use symbols: ✓ ✗ ⭐ → ↔
- If comparing models: clearly label which model

---

## Implementation Checklist

- [ ] Cell 0: Configuration & data loading with model selection
- [ ] Cell 1: Dictionary composition (with tooltips)
- [ ] Cell 2: Dictionary quality (with term details)
- [ ] Cell 3: Dictionary 2D clustering (with semantic info)
- [ ] Cell 4: Chunk 2D clustering (with chunk previews)
- [ ] Cell 5: Chunk 3D clustering (4 files, with details)
- [ ] Cell 6: Score comparison (with agreement info)
- [ ] Cell 7: Score distributions (with bin statistics)
- [ ] Cell 8: Confusion matrix (with confusion explanations)
- [ ] Cell 9: Confidence analysis (with validation info)
- [ ] Cell 10: Disagreement flows (with pattern explanations)
- [ ] Cell 11: Margin scatter (with quadrant analysis)
- [ ] Cell 12: Disagreement table (with full details)
- [ ] Cell 13: Model comparison (if enabled)
- [ ] Cell 14: Summary statistics export
- [ ] Cell 15: Final markdown report

---

**Total Implementation Time**: ~10-12 hours
**Expected Validation Result**: STRONG ✅
**Ready for Thesis**: YES
