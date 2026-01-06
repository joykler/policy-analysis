# Checkpoint 9 Visualization Critique & Recommendations

## Critical Analysis: Current Visualizations vs. Research Needs

Based on V10 thesis application requirements, here's what exists, what's missing, and what's redundant.

---

## EXISTING VISUALIZATIONS

### 1. **Cross-Topic Semantic Space (2D PCA)** - Cell 9.4
**What it shows**:
- Chunks plotted in 2D PCA space
- Color-coded by primary topic (highest cosine score)
- Topic centroids marked with stars
- Variance explained by PC1/PC2

**Research value**:
✓ **Dictionary fitness**: Shows if topics form distinct clusters (dictionary creates separable semantic groups)
✓ **Chunk-level learning**: Indirectly visible through cluster tightness
✗ **Model comparison**: NOT PRESENT - only shows cosine scores, no model comparison

**Critique**:
- **GOOD**: Visualizes whether V10's 7 topics create distinct semantic clusters
- **LIMITATION**: Uses cosine similarity scores (dictionary-based), NOT model embeddings - doesn't show if BERTJE learned topic distinctions
- **MISSING**: No comparison between pretrained vs. finetuned clustering patterns
- **REDUNDANT**: If you also have 3D version (Cell 9.5), 2D may be redundant unless 2D reveals patterns 3D obscures

**Thesis application**:
- Use to demonstrate: "V10 topics create distinguishable semantic spaces" (shows dictionary validity)
- Cannot demonstrate: "Model learned to separate topics" (needs embedding-based visualization)

---

### 2. **Cross-Topic Semantic Space (3D PCA)** - Cell 9.5
**What it shows**:
- Same as 2D but with 3rd principal component
- Interactive 3D rotation

**Research value**:
✓ **Dictionary fitness**: Better than 2D if PC3 explains significant variance
✗ **Model comparison**: Still absent
✗ **Learning demonstration**: Still indirect

**Critique**:
- **REDUNDANT** with 2D unless PC3 adds substantial variance (>10%)
- **THESIS RECOMMENDATION**: Include ONLY IF PC1+PC2 explains <60% variance (meaning 2D is insufficient)
- Otherwise, keep 2D for clarity (easier to read in print thesis)

---

### 3. **Chunk Pre/Post Training Comparison (2D)** - Cell 9.4A
**What it shows**:
- Side-by-side: chunks in PCA space BEFORE and AFTER finetuning
- Uses either BERTJE embeddings OR cosine scores (configurable)

**Research value**:
✓✓ **Model learning (chunk-level)**: CRITICAL - shows if finetuning changed chunk representations
✓✓ **Model comparison**: Direct pre/post comparison
✓ **Dictionary fitness**: If using embeddings, shows model learned dictionary-aligned representations

**Critique**:
- **ESSENTIAL FOR THESIS** - This is your primary evidence that model learned from dictionary
- **CRITICAL QUESTION**: Is this using BERTJE embeddings or cosine scores?
  - If **embeddings**: Perfect - shows model learned new representations
  - If **cosine scores**: Useless - scores don't change with training, only model does
- **CHECK CELL 9.3A configuration**: `USE_BERTJE_EMBEDDINGS = True` must be set
- **MISSING**: Quantitative metrics on clustering improvement (see Recommendations below)

**Thesis application**:
- Chapter 3/4: "Training on V10 dictionary shifted chunk embeddings toward topic-specific regions"
- Evidence of dictionary-guided learning

---

### 4. **Chunk Shift Vectors (3D)** - Cell 9.4B
**What it shows**:
- 3D visualization of pre/post training positions
- Red arrows showing shift direction for top 10% movers
- Shift magnitude per chunk

**Research value**:
✓✓ **Model learning (chunk-level)**: Shows WHICH chunks moved most during training
✓ **Pattern detection**: Can identify if specific topic chunks moved more than others
✗ **Dictionary-level learning**: Doesn't show dictionary term shifts

**Critique**:
- **VERY GOOD** for demonstrating training impact on corpus
- **LIMITATION**: 3D makes it hard to use in printed thesis (use screenshots or animations)
- **MISSING**: Statistical analysis of shift patterns:
  - Do high-score chunks shift less than low-score chunks? (validation of initial labels)
  - Do specific topics shift more? (some topics harder to learn?)
  - Correlation between shift magnitude and score improvement?
- **THESIS USE**: Include 2-3 screenshots with different rotation angles, OR convert to 2D shift visualization

**Recommendation**:
- Add 2D version: X-axis = chunk initial topic score, Y-axis = shift magnitude
- Shows: "Low-confidence chunks moved more during training" (evidence model corrected uncertain cases)

---

### 5. **Dictionary Terms in Semantic Space (2D)** - Cell 9.7
**What it shows**:
- Dictionary seed + expanded terms plotted in 2D PCA
- Pre-training vs. Post-training side-by-side
- Color-coded by topic assignment

**Research value**:
✓✓✓ **Dictionary-level learning**: CRITICAL - shows if model learned to separate topic-specific terms
✓✓ **Dictionary fitness**: Shows if expanded terms cluster with seed terms (validation of expansion)
✓✓ **Model comparison**: Direct pre/post comparison

**Critique**:
- **ESSENTIAL FOR THESIS** - This demonstrates dictionary quality AND model learning
- **WHAT TO LOOK FOR**:
  - Pre-training: Are seed terms already somewhat clustered by topic? (shows dictionary has semantic coherence)
  - Post-training: Do clusters tighten? (shows model learned topic distinctions)
  - Expanded terms: Do they cluster with their seed terms? (validates BERTJE expansion method)
- **MISSING QUANTITATIVE METRICS**:
  - Silhouette score pre/post (cluster quality)
  - Intra-topic vs. inter-topic distance ratio
  - Per-topic cluster tightness change
- **POTENTIAL ISSUE**: If dictionary is large (229 seeds + expansions), plot may be cluttered
  - Solution: Create separate plots per topic (7 small multiples)

**Thesis application**:
- Methodology chapter: "Dictionary expansion produced semantically coherent term clusters"
- Results chapter: "Finetuning increased topic separation in dictionary term space"

---

### 6. **Dictionary Terms (3D with Shift Analysis)** - Cell 9.8
**What it shows**:
- 3D version of Cell 9.7
- Includes shift vectors for terms that moved most
- Top 10 shifters identified

**Research value**:
✓✓ **Dictionary-level learning**: Shows which terms' representations changed most
✓ **Pattern detection**: Can identify problematic terms (large shifts = model initially misrepresented them)

**Critique**:
- **POTENTIALLY REDUNDANT** with 2D version (Cell 9.7)
- **THESIS VALUE**: Only if you want to discuss SPECIFIC terms that shifted dramatically
  - Example: "Term X initially clustered with Topic A but shifted to Topic B post-training"
- **RECOMMENDATION**: Skip 3D, use 2D for thesis clarity
- **ALTERNATIVE USE**: Extract shift magnitude data for analysis (don't need 3D viz for this)

**Better approach**:
- Create table of top 20 shifters with their pre/post topic assignments
- Analyze: Are shifters mostly low-weight terms? (expected - model corrects weak signals)

---

### 7. **Training Metrics Visualization** - Cell 9.6 (mislabeled as 9.6, should be 9.9)
**What it shows**:
- Training/validation loss curves
- Per-topic correlation and MAE metrics
- Overall model performance

**Research value**:
✓✓ **Model learning**: Shows convergence and overfitting detection
✓ **Topic-specific performance**: Reveals which topics are harder to learn
✓ **Model comparison**: Can compare different training runs

**Critique**:
- **ESSENTIAL** - Standard ML validation
- **MISSING DETAILS** (need to check actual implementation):
  - Learning rate schedule visualization?
  - Separate train/val curves?
  - Per-topic performance over epochs (not just final)?
- **THESIS APPLICATION**:
  - Methodology: "Model converged after X epochs without overfitting"
  - Results: "Topics X, Y showed lowest correlation, indicating Z..."

---

## CRITICAL GAPS: What's Missing

### GAP 1: **Model Comparison Across Training Stages**
**What you need**: Side-by-side comparison of:
1. Pretrained BERTJE (baseline)
2. Slavery-trained (intermediate - if you did domain adaptation first)
3. Slavery+Policy-trained (final - your V10 finetuned model)

**Current status**: Cells 9.4A and 9.7 do pre/post, but only 2-way comparison

**Why critical for thesis**:
- Research question requires demonstrating PROGRESSIVE learning
- Need to show: baseline → domain adaptation → task-specific finetuning
- Each step should show improvement in topic separation

**Recommended visualization**:
```
FIGURE: "Progressive Model Refinement"
- 3 panels (or 3 colors in same plot):
  - Panel 1: Pretrained BERTJE embeddings (gray, dispersed)
  - Panel 2: Slavery-domain adapted (light blue, forming clusters)
  - Panel 3: V10 finetuned (dark blue, tight topic clusters)
- Metrics overlaid: Silhouette score, inter-cluster distance
- Caption: "Dictionary-guided finetuning progressively improved topic separation"
```

---

### GAP 2: **Cluster Quality Metrics (Quantitative)**
**What you need**: Numerical validation of visualizations

**Missing metrics**:
1. **Silhouette Score** (pre vs. post):
   - Measures cluster cohesion and separation
   - Range [-1, 1], higher = better clustering
   - CRITICAL for thesis claim: "Model learned to separate topics"

2. **Calinski-Harabasz Index** (variance ratio):
   - Ratio of between-cluster to within-cluster variance
   - Higher = more distinct clusters

3. **Per-topic cluster tightness**:
   - Average distance to topic centroid (pre vs. post)
   - Should DECREASE after training for all topics
   - If some topics don't improve → discuss why in thesis

4. **Inter-topic confusion matrix**:
   - Pre-training: which topics overlap most in embedding space?
   - Post-training: did training reduce overlap?
   - Example: "Raciale_Hierarchie and Doorwerking_Continuiteit had 0.4 overlap pre-training, reduced to 0.15 post-training"

**Recommended visualization**:
```
TABLE: "Clustering Quality Metrics"
| Metric                  | Pretrained | Slavery-trained | V10-finetuned | Improvement |
|-------------------------|------------|-----------------|---------------|-------------|
| Silhouette Score        | 0.23       | 0.41            | 0.58          | +152%       |
| Calinski-Harabasz       | 847        | 1203            | 1876          | +121%       |
| Avg intra-topic dist    | 2.34       | 1.87            | 1.21          | -48%        |

PER-TOPIC TIGHTNESS (distance to centroid):
| Topic                           | Pre   | Post  | Δ      |
|---------------------------------|-------|-------|--------|
| Slavernij_Historisch            | 1.89  | 1.12  | -41%   |
| Koninkrijks_Macht               | 2.11  | 1.34  | -36%   |
| Raciale_Hierarchie              | 2.45  | 1.89  | -23%   | ← Least improvement
...
```

---

### GAP 3: **Dictionary Term Performance Analysis**
**What you need**: Which dictionary terms are well-represented vs. poorly-represented by model

**Missing analysis**:
1. **Seed vs. Expanded term clustering**:
   - Do expanded terms cluster with their parent seeds?
   - Quantify: Average distance from expanded term to parent seed
   - If large → expansion method needs refinement

2. **Weight tier validation**:
   - Do KERN terms (weight 1.0/0.9) form tighter clusters than RISICO terms (weight 0.3)?
   - Should be YES - validates weighting scheme
   - If NO → weighting arbitrary, not semantic

3. **Outlier terms**:
   - Identify terms far from their topic centroid (pre AND post training)
   - These are misclassified or ambiguous terms
   - Thesis discussion: "Term X assigned to Topic A but clusters with Topic B → suggests cross-topic relevance"

**Recommended visualization**:
```
FIGURE: "Dictionary Weight Validation"
- Boxplot: X-axis = weight tier (KERN, STERK, BELEID, CONTEXT, RISICO)
            Y-axis = distance to topic centroid (post-training)
- Expected pattern: KERN tightest, RISICO loosest
- If pattern holds → weights are semantically meaningful
- If not → weights need empirical recalibration

FIGURE: "Expansion Quality"
- Scatter: X-axis = seed term position PC1
           Y-axis = seed term position PC2
           Arrows pointing to expanded terms
- Color by expansion distance (red = far from seed)
- Outlier terms labeled for discussion
```

---

### GAP 4: **Topic Separation Heatmap**
**What you need**: Visual matrix showing topic distinctiveness

**Missing visualization**:
```
FIGURE: "Topic Separation Matrix (Pre vs. Post Training)"

Pre-Training Confusion:
                     Slav  Konin  Rac  Arb  Door  Erk  Ken
Slavernij_Hist       1.00  0.45  0.38  0.52  0.31  0.28  0.41
Koninkrijks_Macht    0.45  1.00  0.34  0.39  0.48  0.42  0.29
Raciale_Hierarchie   0.38  0.34  1.00  0.41  0.56  0.33  0.25
... (symmetric matrix, diagonal = 1.0, off-diagonal = overlap)

Post-Training Separation:
                     Slav  Konin  Rac  Arb  Door  Erk  Ken
Slavernij_Hist       1.00  0.18  0.12  0.21  0.09  0.11  0.15
... (lower off-diagonal = better separation)

Improvement:
- Green cells = separation improved
- Red cells = separation worsened (investigate why)
```

**How to calculate**:
- Cosine similarity between topic centroid embeddings (pre vs. post)
- OR: % of chunks where topic A is 2nd-highest score when topic B is primary

**Thesis value**:
- "Training reduced Doorwerking_Continuiteit / Raciale_Hierarchie overlap from 0.56 to 0.23"
- Shows which topic pairs remain confusable (discussion point)

---

### GAP 5: **Score Distribution Analysis**
**What you need**: Understanding of score patterns across corpus

**Missing visualizations**:
1. **Score distribution per topic** (pre vs. post):
   - Histogram: topic scores for all chunks
   - Expected change: Post-training should show bimodal (high for relevant chunks, low for irrelevant)
   - Pre-training: May be more uniform (model hasn't learned distinctions)

2. **Confidence improvement**:
   - X-axis: Initial cosine score (pre-training proxy)
   - Y-axis: BERTJE predicted score (post-training)
   - Diagonal line = perfect agreement
   - Points above diagonal = model more confident than dictionary
   - Points below = model less confident (investigate why)

3. **Multi-label overlap**:
   - How many chunks score high (>0.5) on multiple topics?
   - Pre vs. post: Should multi-label % decrease if model learns clearer boundaries
   - OR: Multi-label % may INCREASE if model captures legitimate cross-topic segments

**Recommended visualization**:
```
FIGURE: "Topic Score Distributions"
- 7 subplots (one per topic)
- Each subplot: overlaid histograms
  - Blue bars: cosine scores (dictionary-based)
  - Red bars: BERTJE predictions (model-based)
- Look for: Does model sharpen distributions? (narrower peaks = more decisive)

FIGURE: "Confidence Agreement"
- Scatter plot per topic
- Quadrants labeled:
  - Top-right: High dictionary score, high model score (validated)
  - Top-left: Low dictionary, high model (model found relevant content dictionary missed)
  - Bottom-right: High dictionary, low model (false positives in dictionary)
  - Bottom-left: Low both (irrelevant)
- Quantify % in each quadrant for thesis discussion
```

---

### GAP 6: **Temporal/Document-Type Analysis**
**What you need**: V10 applied to thesis research question

**Missing thesis-specific visualizations**:
1. **IDPAD temporal trends** (2015-2024):
   - Line graph: X = year, Y = average topic score
   - 7 lines (one per topic)
   - Research question: Did Erkenning_Verantwoordelijkheid increase post-2022 apology?

2. **Document type comparison**:
   - Grouped bar chart: Topic scores by document source
   - Groups: Dutch govt, UN, Caribbean govt, NGO
   - Shows which actors acknowledge legacy via which mechanisms

3. **Gap identification** (THE CENTRAL PATTERN):
   - Scatter: X = developmental language score (TF-IDF of problem keywords)
             Y = V10 slavery topic scores (average across all 7)
   - Bottom-right quadrant = HIGH development, LOW legacy = THE GAP
   - Quantify: "X% of IDPAD policies discuss development without legacy framing"

**Recommended visualizations**:
```
FIGURE: "IDPAD Temporal Evolution (2015-2024)"
- Line graph with 7 topic trends
- Vertical line at 2022 (apology)
- Annotations for key policy moments
- Expected: Erkenning spike post-2022

FIGURE: "The Development-Legacy Gap"
- 2D scatter: development keywords (X) vs. V10 topics (Y)
- Each dot = one policy document
- Color by year (gradient 2015-2024)
- Bottom-right quadrant highlighted as "gap zone"
- % of documents in gap zone calculated
- Thesis core finding
```

---

## REDUNDANT VISUALIZATIONS

### Redundancy 1: 2D vs. 3D Cross-Topic Space (Cells 9.4 vs. 9.5)
**Recommendation**:
- Keep **2D** for printed thesis (easier to read)
- Keep **3D** only if PC3 explains >10% variance AND you include it as supplementary material
- Delete one to reduce notebook clutter

### Redundancy 2: 2D vs. 3D Dictionary Terms (Cells 9.7 vs. 9.8)
**Recommendation**:
- Keep **2D side-by-side comparison** (Cell 9.7) - most informative
- **Delete 3D** (Cell 9.8) unless you need shift vector details
- Alternative: Extract shift magnitudes from Cell 9.8 for TABLE (not 3D viz)

### Redundancy 3: Multiple Chunk Visualizations (Cells 9.4A vs. 9.4B)
**Recommendation**:
- Keep **2D pre/post comparison** (Cell 9.4A) for thesis
- Keep **3D shift vectors** (Cell 9.4B) only if you want to identify WHICH chunks moved (qualitative analysis)
- Consider: Replace 3D viz with 2D "shift magnitude vs. initial score" scatter plot (more informative for thesis)

---

## RECOMMENDED VISUALIZATION SUITE FOR THESIS

### Essential (Must Include):
1. ✓ **Dictionary Terms 2D Pre/Post** (Cell 9.7) - proves dictionary quality AND model learning
2. ✓ **Chunk Pre/Post 2D** (Cell 9.4A) - proves model learned from corpus
3. ✓ **Training Metrics** (Cell 9.6) - standard ML validation
4. **NEW: Cluster Quality Metrics Table** - quantitative validation
5. **NEW: Topic Separation Matrix** - shows which topics are distinct
6. **NEW: IDPAD Temporal Trends** - answers research question

### Important (Should Include):
7. **NEW: Model Comparison (3-way)** - pretrained → slavery → V10
8. **NEW: Score Distribution Comparison** - dictionary vs. model agreement
9. **NEW: Development-Legacy Gap Scatter** - thesis core finding
10. ✓ **3D Chunk Shifts** (Cell 9.4B) OR **NEW: 2D Shift Analysis** - shows learning patterns

### Supplementary (Optional):
11. ✓ **Cross-Topic 2D** (Cell 9.4) - if not redundant with chunk viz
12. **NEW: Weight Tier Validation** - validates V10 weighting scheme
13. **NEW: Expansion Quality Analysis** - validates BERTJE expansion
14. **NEW: Document Type Comparison** - actor-specific legacy framing

### Delete:
- ✗ 3D Cross-Topic (Cell 9.5) - unless PC3 >10% variance
- ✗ 3D Dictionary (Cell 9.8) - use 2D instead

---

## IMPLEMENTATION OUTLINE

### New Visualization 1: **Cluster Quality Metrics**
```python
# Compute silhouette score for chunk embeddings
from sklearn.metrics import silhouette_score, calinski_harabasz_score

# Pre-training
X_pre = embeddings_pretrained  # From Cell 9.3A
labels = df_chunks['primary_topic'].map({topic: i for i, topic in enumerate(topics)})
silhouette_pre = silhouette_score(X_pre, labels)
ch_pre = calinski_harabasz_score(X_pre, labels)

# Post-training
X_post = embeddings_finetuned
silhouette_post = silhouette_score(X_post, labels)
ch_post = calinski_harabasz_score(X_post, labels)

# Per-topic tightness
intra_topic_distances = {}
for topic in topics:
    topic_mask = df_chunks['primary_topic'] == topic
    topic_embeddings = X_post[topic_mask]
    centroid = topic_embeddings.mean(axis=0)
    distances = np.linalg.norm(topic_embeddings - centroid, axis=1)
    intra_topic_distances[topic] = distances.mean()

# Create table visualization
fig = go.Figure(data=[go.Table(
    header=dict(values=['Metric', 'Pretrained', 'V10-Finetuned', 'Improvement']),
    cells=dict(values=[
        ['Silhouette Score', 'Calinski-Harabasz'],
        [f'{silhouette_pre:.3f}', f'{ch_pre:.1f}'],
        [f'{silhouette_post:.3f}', f'{ch_post:.1f}'],
        [f'+{(silhouette_post/silhouette_pre - 1)*100:.1f}%',
         f'+{(ch_post/ch_pre - 1)*100:.1f}%']
    ])
)])
```

---

### New Visualization 2: **Topic Separation Heatmap**
```python
# Calculate centroid embeddings for each topic
topic_centroids_pre = {}
topic_centroids_post = {}

for topic in topics:
    mask = df_chunks['primary_topic'] == topic
    topic_centroids_pre[topic] = embeddings_pretrained[mask].mean(axis=0)
    topic_centroids_post[topic] = embeddings_finetuned[mask].mean(axis=0)

# Compute pairwise cosine similarity
from sklearn.metrics.pairwise import cosine_similarity

centroids_pre_matrix = np.stack([topic_centroids_pre[t] for t in topics])
centroids_post_matrix = np.stack([topic_centroids_post[t] for t in topics])

similarity_pre = cosine_similarity(centroids_pre_matrix)
similarity_post = cosine_similarity(centroids_post_matrix)

# Create side-by-side heatmaps
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=['Pre-Training Confusion', 'Post-Training Separation', 'Improvement'],
    specs=[[{'type': 'heatmap'}, {'type': 'heatmap'}, {'type': 'heatmap'}]]
)

# Pre-training heatmap
fig.add_trace(go.Heatmap(
    z=similarity_pre,
    x=topics,
    y=topics,
    colorscale='Reds',
    text=np.round(similarity_pre, 2),
    texttemplate='%{text}',
    colorbar=dict(x=0.3)
), row=1, col=1)

# Post-training heatmap
fig.add_trace(go.Heatmap(
    z=similarity_post,
    x=topics,
    y=topics,
    colorscale='Greens_r',  # Reverse so lower is better
    text=np.round(similarity_post, 2),
    texttemplate='%{text}',
    colorbar=dict(x=0.65)
), row=1, col=2)

# Improvement (difference)
improvement = similarity_pre - similarity_post  # Positive = better separation
fig.add_trace(go.Heatmap(
    z=improvement,
    x=topics,
    y=topics,
    colorscale='RdYlGn',  # Red=worse, green=better
    text=np.round(improvement, 2),
    texttemplate='%{text}',
    colorbar=dict(x=1.0)
), row=1, col=3)

fig.update_layout(
    title='Topic Separation Analysis: Training Impact on Inter-Topic Similarity',
    height=600,
    width=1800
)
```

---

### New Visualization 3: **Score Distribution Comparison**
```python
# For each topic, compare cosine scores vs. BERTJE predictions
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=2, cols=4,
    subplot_titles=topics,
    specs=[[{'type': 'histogram'}]*4, [{'type': 'histogram'}]*3 + [None]]
)

for i, topic in enumerate(topics):
    row = i // 4 + 1
    col = i % 4 + 1

    # Get scores for this topic
    cosine_scores = df_chunks[f'cosine_{topic}']
    bertje_scores = df_chunks[f'bertje_{topic}']  # If available

    # Add overlaid histograms
    fig.add_trace(go.Histogram(
        x=cosine_scores,
        name='Cosine (Dictionary)',
        marker_color='blue',
        opacity=0.5,
        legendgroup='cosine',
        showlegend=(i == 0)
    ), row=row, col=col)

    fig.add_trace(go.Histogram(
        x=bertje_scores,
        name='BERTJE (Model)',
        marker_color='red',
        opacity=0.5,
        legendgroup='bertje',
        showlegend=(i == 0)
    ), row=row, col=col)

    # Update axes
    fig.update_xaxes(title_text='Score', row=row, col=col)
    fig.update_yaxes(title_text='Frequency', row=row, col=col)

fig.update_layout(
    title='Topic Score Distributions: Dictionary (Cosine) vs. Model (BERTJE)',
    height=800,
    width=1600,
    barmode='overlay'
)
```

---

### New Visualization 4: **IDPAD Temporal Trends** (Thesis-Specific)
```python
# Assumes you have IDPAD corpus with year metadata
# df_idpad: columns = ['year', 'document_id', 'Slavernij_Historisch', ..., 'Kennis_Herinnering']

# Calculate average topic scores per year
yearly_trends = df_idpad.groupby('year')[topics].mean()

# Create line plot
fig = go.Figure()

for topic in topics:
    fig.add_trace(go.Scatter(
        x=yearly_trends.index,
        y=yearly_trends[topic],
        mode='lines+markers',
        name=topic,
        line=dict(width=2)
    ))

# Add vertical line at 2022 (apology year)
fig.add_vline(
    x=2022,
    line=dict(color='red', width=2, dash='dash'),
    annotation_text='2022 Apology',
    annotation_position='top'
)

fig.update_layout(
    title='IDPAD Policy Evolution (2015-2024): Topic Scores Over Time',
    xaxis_title='Year',
    yaxis_title='Average Topic Score',
    height=600,
    width=1200,
    hovermode='x unified'
)

# Add annotation for key finding
if yearly_trends.loc[2023:, 'Erkenning_Verantwoordelijkheid'].mean() > \
   yearly_trends.loc[:2022, 'Erkenning_Verantwoordelijkheid'].mean():
    fig.add_annotation(
        text='Recognition discourse increased post-apology',
        x=2023,
        y=yearly_trends.loc[2023, 'Erkenning_Verantwoordelijkheid'],
        showarrow=True,
        arrowhead=2
    )
```

---

### New Visualization 5: **Development-Legacy Gap Analysis** (Core Thesis Finding)
```python
# Assumes you've calculated:
# - development_score: TF-IDF score for development keywords (education, poverty, etc.)
# - legacy_score: Average V10 topic score across all 7 topics

fig = go.Figure()

# Scatter plot
fig.add_trace(go.Scatter(
    x=df_idpad['development_score'],
    y=df_idpad['legacy_score'],
    mode='markers',
    marker=dict(
        size=8,
        color=df_idpad['year'],
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title='Year'),
        opacity=0.7
    ),
    text=df_idpad['document_title'],
    hovertemplate='<b>%{text}</b><br>Development: %{x:.2f}<br>Legacy: %{y:.2f}<extra></extra>'
))

# Add quadrant lines
dev_median = df_idpad['development_score'].median()
legacy_median = df_idpad['legacy_score'].median()

fig.add_hline(y=legacy_median, line=dict(color='gray', dash='dash'))
fig.add_vline(x=dev_median, line=dict(color='gray', dash='dash'))

# Highlight "gap zone" (high development, low legacy)
gap_zone = df_idpad[
    (df_idpad['development_score'] > dev_median) &
    (df_idpad['legacy_score'] < legacy_median)
]

fig.add_trace(go.Scatter(
    x=gap_zone['development_score'],
    y=gap_zone['legacy_score'],
    mode='markers',
    marker=dict(size=12, color='red', symbol='x', line=dict(width=2)),
    name='Gap Zone',
    showlegend=True
))

# Add annotations
gap_pct = len(gap_zone) / len(df_idpad) * 100
fig.add_annotation(
    text=f'<b>THE GAP</b><br>{gap_pct:.1f}% of policies<br>(High development, low legacy)',
    x=df_idpad['development_score'].quantile(0.75),
    y=df_idpad['legacy_score'].quantile(0.25),
    showarrow=False,
    font=dict(size=12, color='red'),
    bgcolor='rgba(255,255,255,0.8)',
    bordercolor='red',
    borderwidth=2
)

fig.update_layout(
    title='The Development-Legacy Gap in IDPAD Policies (2015-2024)',
    xaxis_title='Development Language Score (TF-IDF)',
    yaxis_title='V10 Legacy Topic Score (Average)',
    height=700,
    width=1000
)
```

---

## SUMMARY TABLE: Visualization Assessment

| Visualization | Cell | Purpose | Demonstrates Dict Fitness? | Demonstrates Model Learning? | Compares Models? | Thesis-Relevant? | **Recommendation** |
|---------------|------|---------|---------------------------|------------------------------|------------------|------------------|-------------------|
| Cross-Topic 2D | 9.4 | Chunk clustering | ✓ Indirect | ✗ No (uses cosine) | ✗ | Moderate | **KEEP if embeddings, DELETE if cosine scores** |
| Cross-Topic 3D | 9.5 | Chunk clustering 3D | ✓ Indirect | ✗ No | ✗ | Low | **DELETE** (redundant with 2D) |
| Chunk Pre/Post 2D | 9.4A | Model learning on chunks | ✓✓ | ✓✓ | ✓✓ | **HIGH** | **KEEP - ESSENTIAL** (verify uses embeddings!) |
| Chunk Shifts 3D | 9.4B | Shift vectors | ✓ | ✓✓ | ✓ | Moderate | **CONVERT to 2D** or **DELETE** (extract data instead) |
| Dict Terms 2D | 9.7 | Dictionary validation | ✓✓✓ | ✓✓✓ | ✓✓ | **HIGH** | **KEEP - ESSENTIAL** |
| Dict Terms 3D | 9.8 | Dictionary shifts | ✓✓ | ✓✓ | ✓ | Low | **DELETE** (use shift table instead) |
| Training Metrics | 9.6 | ML validation | ✗ | ✓✓ | ✓ | **HIGH** | **KEEP - ESSENTIAL** |
| **Cluster Metrics** | **NEW** | **Quantitative validation** | **✓✓** | **✓✓✓** | **✓✓** | **HIGH** | **ADD - CRITICAL** |
| **Topic Separation** | **NEW** | **Inter-topic confusion** | **✓✓✓** | **✓✓** | **✓✓** | **HIGH** | **ADD - CRITICAL** |
| **Score Distributions** | **NEW** | **Dict vs. model agreement** | **✓✓✓** | **✓✓** | **✓** | **Moderate** | **ADD - Important** |
| **IDPAD Temporal** | **NEW** | **Research question** | **✗** | **✗** | **✗** | **CRITICAL** | **ADD - ESSENTIAL for thesis** |
| **Dev-Legacy Gap** | **NEW** | **Core thesis finding** | **✓✓** | **✗** | **✗** | **CRITICAL** | **ADD - ESSENTIAL for thesis** |
| **3-Way Model Comp** | **NEW** | **Progressive learning** | **✓** | **✓✓✓** | **✓✓✓** | **HIGH** | **ADD - Important** |
| **Weight Validation** | **NEW** | **V10 weighting scheme** | **✓✓✓** | **✗** | **✗** | **Moderate** | **ADD - Supports methodology** |

---

## FINAL RECOMMENDATIONS

### Immediate Actions:
1. **VERIFY Cell 9.4A configuration**: Ensure `USE_BERTJE_EMBEDDINGS = True` (critical!)
2. **DELETE redundant 3D visualizations**: Cells 9.5, 9.8 (keep 2D versions)
3. **ADD quantitative metrics**: Cluster quality table (silhouette, Calinski-Harabasz, per-topic tightness)
4. **ADD topic separation heatmap**: Pre/post confusion matrix

### For Thesis Application:
5. **ADD IDPAD temporal trends**: 7-topic evolution 2015-2024 (answers RQ directly)
6. **ADD development-legacy gap scatter**: Core thesis finding visualization
7. **CONSIDER 3-way model comparison**: If you have pretrained + slavery-adapted + V10 finetuned

### Methodology Validation:
8. **ADD weight tier validation**: Boxplot showing KERN terms cluster tighter than RISICO
9. **ADD expansion quality analysis**: Seed-to-expanded term distance validation
10. **ADD score distribution comparison**: Dictionary (cosine) vs. model (BERTJE) agreement

### Thesis Writing Strategy:
- **Methodology chapter**: Use dict terms 2D (Cell 9.7) + weight validation + expansion quality
- **Results chapter**: Use cluster metrics table + topic separation heatmap + chunk pre/post 2D (Cell 9.4A)
- **Discussion chapter**: Use IDPAD temporal + development-legacy gap + per-topic performance analysis
- **Appendix**: Full training metrics (Cell 9.6) + shift magnitude tables

**Estimated additions**: ~6-8 new visualizations (4 critical, 2-4 important)
**Estimated deletions**: 2-3 redundant visualizations
**Net result**: Leaner, more thesis-aligned visualization suite with quantitative validation
