# Iterative Evaluation Report
**Workflow:** slavery_structured-slavdict_pretrained_slavery_v1

---

## Workflow Metadata

| Field | Value |
|-------|-------|
| **Path** | `workflow_reneweddict/slavery_structured-slavdict_pretrained_slavery_v1` |
| **Corpus** | Slavery (domain corpus) |
| **Dictionary** | structured-slavdict |
| **Training Status** | Pretrained (Stage 1) |
| **Version** | v1 |
| **Topics** | 3 topics |

**Topics:**
1. Historical_Slavery_Colonialism
2. Structural_Continuity_Neocolonial
3. Contemporary_Manifestations

---

## Q1: Dictionary Coverage & Thematic Representation

### Findings

**Term Counts by Topic:**

| Topic | Seed Terms | Corpus-Expanded | Total | Removal Rate |
|-------|------------|-----------------|-------|--------------|
| Historical_Slavery_Colonialism | 54 | 242 | 296 | 1.3% |
| Structural_Continuity_Neocolonial | 40 | 243 | 283 | 5.7% |
| Contemporary_Manifestations | 49 | 154 | 203 | 32.3% |
| **Total** | **143** | **639** | **782** | **13.1%** |

**Coverage Assessment:**

1. **Historical_Slavery_Colonialism (296 terms)** - EXCELLENT coverage
   - Core concepts: slavernij, slaaf, slavenhandel, plantage, kolonie, VOC, WIC
   - Includes compound terms: plantagesysteem, slavenhandelaren, kolonisatoren
   - Historical era markers: geschiedenis, verleden, historisch
   - Racial hierarchy terms: raciaal, superioriteit, inferioriteit

2. **Structural_Continuity_Neocolonial (283 terms)** - GOOD coverage
   - Core concepts: doorwerking, erfenis, postkoloniaal, structureel
   - Continuity markers: voortdurend, blijvend, chronisch
   - Economic patterns: extractie, ongelijkheid, armoede, achterstanden
   - Migration/diaspora: migranten, immigratie, diaspora-related terms

3. **Contemporary_Manifestations (203 terms)** - ADEQUATE coverage (but smallest)
   - Core concepts: racisme, discriminatie, uitsluiting
   - Identity terms: zwart, wit, Afro-*, Surinaams, Antilliaans
   - Institutional: institutioneel racisme, systemisch racisme
   - Anti-racism: antiracisme, antidiscriminatie

**Gaps Identified:**
- Contemporary topic has smallest term count (203 vs 283-296)
- Heavy cleanup was needed (32.3% removal) due to problematic `uitsluiting` parent
- Some generic terms may still cause noise (e.g., `sluiten`, `sluit`)

### Evidence
- Source: `Dictionary/COMPLETE_CURATION_SUMMARY.md`
- Source: `Other_data/topic_vectors_meta.json`

---

## Q2: Dictionary Coherence & Weight Quality

### Findings

**Weight Distribution (7-Tier Framework):**

| Weight Tier | Historical | Structural | Contemporary | Total | % |
|-------------|-----------|-----------|--------------|-------|---|
| 1.00 (core_problem) | 105 | 28 | 40 | 173 | 22.1% |
| 0.95 (strong_problem) | 113 | 212 | 136 | 461 | 59.0% |
| 0.85 (related_strong) | 31 | 12 | 5 | 48 | 6.1% |
| 0.75 (related_moderate) | 33 | 31 | 15 | 79 | 10.1% |
| 0.55 (era_context) | 14 | 0 | 7 | 21 | 2.7% |

**Pyramid Structure Assessment:**
- Core (1.00): 22.1% - appropriately small peak
- Strong (0.95): 59.0% - largest tier (provides semantic richness)
- Related tiers (0.85-0.75): 16.2% - domain context
- Era context (0.55): 2.7% - temporal markers

**Observation:** The pyramid is "inverted" at the top (more 0.95 than 1.00), but this is **semantically appropriate** because:
- 1.00 reserved for THE concept itself (slavernij, racisme, doorwerking)
- 0.95 includes clear manifestations/indicators (larger vocabulary)

**Topic-Specific Weight Quality:**

1. **Historical** - Well-stratified
   - 35.5% core (plantation, slavery core terms)
   - 38.2% strong (trade, colonial infrastructure)
   - Good era_context usage (14 terms at 0.55)

2. **Structural** - Concentrated at 0.95
   - Only 9.9% core (narrow definition)
   - 74.9% strong (continuity patterns, economic effects)
   - No era_context terms (appropriate - focuses on ongoing patterns)

3. **Contemporary** - Balanced
   - 19.7% core (racisme, discriminatie)
   - 67.0% strong (identity terms, institutional forms)
   - Some era_context (7 terms at 0.55)

**Curation Quality:**
- 5-phase systematic curation applied
- Problem parents identified and cleaned:
  - `uitsluiting` → 34/36 orthographic matches removed
  - `structurele` → construction terms removed
  - `onderontwikkeling` → opposite meanings removed

### Evidence
- Source: `Dictionary/COMPLETE_CURATION_SUMMARY.md`
- Weight statistics from curation summary tables

---

## Summary: Q1 & Q2 Assessment

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Coverage | GOOD | All core themes represented |
| Balance | MODERATE | Contemporary smaller (203 vs 283-296) |
| Weight Distribution | GOOD | Proper pyramid structure |
| Semantic Fit | GOOD | Manual curation removed drift |
| Curation Quality | HIGH | 5-phase process documented |

**Strengths:**
- Comprehensive historical slavery vocabulary
- Good compound term preservation
- Systematic curation with documented rationales
- 7-tier weight framework properly applied

**Weaknesses:**
- Contemporary topic has fewest terms after heavy cleanup
- Some generic terms may cause false positives (sluiten, blijft, etc.)
- Structural topic highly concentrated at 0.95 weight

---

## Q3: Topic Distinctiveness vs. Interdependence

### Findings

**IMPORTANT NOTE:** This is a multilabel classification system - chunks can (and should) have multiple active topics. Primary topic assignment is NOT a useful metric here. Instead, we focus on:
- Score distributions per topic
- Topic correlations
- Score variance (CV)
- Multi-label co-occurrence patterns

---

### Per-Topic Score Distributions (BERTJE)

| Topic | Mean | Std | Min | Max | CV |
|-------|------|-----|-----|-----|-----|
| Contemporary_Manifestations | 4.62 | 1.15 | 1.17 | 8.44 | **0.249** |
| Historical_Slavery_Colonialism | 4.86 | 1.18 | 1.28 | 7.89 | **0.243** |
| Structural_Continuity_Neocolonial | 4.16 | 0.75 | 1.81 | 6.78 | **0.180** |

**Key Observations:**
- **Structural topic has lowest CV (0.180)** - less variance in scores = less discriminative signal
- **Structural topic has smallest score range** (4.97 vs 6.6-7.3 for others)
- Contemporary and Historical show healthy variance (CV ~0.24-0.25)

### Per-Topic Score Distributions (Cosine)

| Topic | Mean | Std | Min | Max | CV |
|-------|------|-----|-----|-----|-----|
| Contemporary_Manifestations | 4.57 | 1.17 | 1.14 | 8.71 | **0.257** |
| Historical_Slavery_Colonialism | 4.83 | 1.22 | 1.14 | 8.93 | **0.253** |
| Structural_Continuity_Neocolonial | 4.25 | 0.91 | 1.12 | 7.22 | **0.214** |

**Same pattern in Cosine:** Structural has lower CV and smaller range.

---

### Topic Correlations

**BERTJE Correlations:**

|  | Contemporary | Historical | Structural |
|--|--------------|------------|------------|
| **Contemporary** | 1.00 | 0.42 | 0.45 |
| **Historical** | 0.42 | 1.00 | 0.49 |
| **Structural** | 0.45 | 0.49 | 1.00 |

**Cosine Correlations:**

|  | Contemporary | Historical | Structural |
|--|--------------|------------|------------|
| **Contemporary** | 1.00 | 0.53 | 0.58 |
| **Historical** | 0.53 | 1.00 | 0.62 |
| **Structural** | 0.58 | 0.62 | 1.00 |

**Interpretation:**
- Correlations are **moderate** (0.42-0.62) - topics are related but not redundant
- BERTJE training **reduced correlations** compared to Cosine baseline (good!)
- Structural correlates most strongly with both other topics (0.49-0.62)
- This is **expected and acceptable** - slavery legacy topics naturally overlap

---

### Multi-Label Co-occurrence Patterns (BERTJE)

Using mean score as threshold (4.55):

| Topics Active | Chunks | % |
|---------------|--------|---|
| 0 topics | 704 | 24.8% |
| 1 topic | 944 | 33.2% |
| 2 topics | 588 | 20.7% |
| 3 topics | 604 | 21.3% |

**Interpretation:**
- **54.8% of chunks have 1-2 active topics** - good multilabel behavior
- **21.3% have all 3 topics** - expected for integrative slavery legacy texts
- **24.8% have no strong topic** - corpus contains some off-topic content

---

### Score Variance Analysis

**Within-Chunk CV (differentiation between topics):**
- Mean CV: 0.140
- Std CV: 0.070

**Interpretation:**
- CV of 0.14 indicates **moderate differentiation** between topics per chunk
- Model distinguishes between topics but not strongly
- Lower than ideal (0.20+ would indicate better differentiation)

---

### Training Performance by Topic (R²)

| Topic | R² | Interpretation |
|-------|-----|----------------|
| Historical_Slavery_Colonialism | 0.747 | GOOD |
| Contemporary_Manifestations | 0.732 | GOOD |
| Structural_Continuity_Neocolonial | 0.563 | MODERATE |

**Key Observation:** Structural topic has lower R² (0.563 vs 0.73-0.75)
- Model learns Historical and Contemporary patterns well
- Structural topic may conceptually overlap with both (colonial patterns + ongoing effects)

---

### CONCERN: Structural Topic Signal Weakness

The Structural_Continuity_Neocolonial topic shows weaker signal:
1. **Lowest CV** (0.180 vs 0.24-0.25) - less discriminative
2. **Smallest score range** (4.97 vs 6.6-7.3)
3. **Lowest R²** (0.563 vs 0.73-0.75)
4. **Highest correlations** with other topics

This does NOT mean the topic is "failing" - it may indicate:
- The concept is inherently bridging (connecting historical to contemporary)
- Dictionary terms overlap semantically with other topics
- May need more distinctive seed terms

### Evidence
- Source: `Bertje_labeling/bertje_labeled_corpus.csv` (score analysis)
- Source: `Cosine_labeling/scores_all_labeled.csv` (score analysis)
- Source: `Model_finetuning/training_metrics.json`

---

## Q4: Semantic Relevance of Captures

### Findings

**Cosine Scoring Confidence Tiers:**

| Tier | Chunks | % |
|------|--------|---|
| High Confidence | 13,832 | 16.3% |
| Low Confidence | 19,827 | 23.3% |
| No Confidence | 51,427 | 60.4% |

**Note:** Cosine scoring appears to have more chunks than BERTJE (85k vs 2.8k) - likely includes all document chunks before filtering.

**Training Metrics Progression:**

| Epoch | Eval Loss | Mean Pearson | Primary Topic Acc | R² |
|-------|-----------|--------------|-------------------|-----|
| 1 | 0.771 | 0.756 | 75.4% | 0.409 |
| 2 | 0.485 | 0.821 | 79.8% | 0.628 |
| 3 | 0.449 | 0.836 | 82.2% | 0.656 |
| 4 | 0.373 | 0.858 | 83.3% | 0.714 |
| 5 (Final) | 0.373 | 0.860 | 82.6% | 0.714 |

**Training Effect Assessment:**
- Loss decreased from 0.771 → 0.373 (51.6% reduction) ✓
- Pearson correlation improved: 0.756 → 0.860 ✓
- Primary topic accuracy improved: 75.4% → 82.6% ✓
- R² improved: 0.409 → 0.714 ✓
- Training shows consistent improvement

**Final Model Performance:**

| Metric | Value | Assessment |
|--------|-------|------------|
| Global R² | 0.714 | GOOD |
| Mean Pearson | 0.860 | GOOD |
| Median Pearson | 0.974 | EXCELLENT |
| Primary Topic Accuracy | 82.6% | GOOD |
| Top-2 Overlap Accuracy | 100% | EXCELLENT |
| % Pearson > 0.85 | 78.3% | GOOD |

**Per-Topic MAE (Mean Absolute Error):**

| Topic | MAE | RMSE |
|-------|-----|------|
| Contemporary_Manifestations | 0.485 | 0.614 |
| Historical_Slavery_Colonialism | 0.494 | 0.618 |
| Structural_Continuity_Neocolonial | 0.484 | 0.601 |

MAE is relatively uniform across topics (~0.49), suggesting consistent prediction quality.

### Evidence
- Source: `Model_finetuning/training_metrics.json`
- Source: `Cosine_labeling/scores_*.csv` (line counts)

---

## Summary: Q3 & Q4 Assessment

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Topic Correlations | GOOD | Moderate (0.42-0.62), training reduced them |
| Score Variance | MODERATE | CV ~0.14, could be higher |
| Multi-label Patterns | GOOD | 54.8% have 1-2 topics, 21% have all 3 |
| Training Effect | GOOD | Clear improvement across epochs |
| Model Performance | GOOD | R²=0.71, Pearson=0.86 |
| Per-Topic Balance | MODERATE | Structural has weaker signal |

**OBSERVATION: Structural Topic Needs Attention**

The Structural_Continuity_Neocolonial topic shows weaker discriminative signal:
- Lowest CV (0.180 vs 0.24-0.25)
- Smallest score range (4.97 vs 6.6-7.3)
- Lowest R² (0.563 vs 0.73-0.75)

This is NOT necessarily a failure - it may reflect the bridging nature of "structural continuity" (connecting historical to contemporary). However, consider:
1. Adding more distinctive seed terms for Structural topic
2. Reviewing dictionary terms for overlap with other topics
3. This pattern may improve when applied to policy corpus

---

## Step 3: Visualization Analysis

### Available Visualizations

The workflow has 40 pre-generated visualizations in `Visuals/` folder, organized by section:

| Section | Visualizations |
|---------|----------------|
| Section 3: Dictionary Fitness | 6 files (weight tier validation, expansion quality, clustering) |
| Section 4: Topic Coherence | 3 files (cluster quality, topic separation, training metrics) |
| Section 5: Chunk Analysis | 3 files (chunk shift, score distribution) |
| Section 6: Score Distribution | 3 files (cosine vs bertje comparison, disagreements) |
| Other | 25 files (3D embeddings, heatmaps, overlap analysis) |

---

### Key Metrics from Visualizations

**Cluster Quality Metrics:**

| Model | Silhouette | Calinski-Harabasz | Avg Intra-Distance |
|-------|------------|-------------------|---------------------|
| pretrained_bertje | **0.422** | **498** | 3.48 |
| slavery_trained | 0.290 | 245 | 8.49 |

**Observation:** Training DECREASED cluster quality metrics:
- Silhouette dropped 31% (0.42 → 0.29)
- Calinski-Harabasz dropped 51%
- Intra-cluster distance increased 144%

This is **unexpected** but may indicate the model is learning more nuanced representations rather than tight clusters.

---

**Per-Topic Tightness (pretrained_bertje):**

| Topic | Tightness |
|-------|-----------|
| Contemporary_Manifestations | 4.30 |
| Historical_Slavery_Colonialism | 3.42 |
| Structural_Continuity_Neocolonial | **2.96** (tightest) |

---

**Cosine vs BERTJE Agreement:**

| Topic | Pearson r | Agreement % |
|-------|-----------|-------------|
| Contemporary_Manifestations | 0.902 | 87.1% |
| Historical_Slavery_Colonialism | 0.899 | 87.1% |
| Structural_Continuity_Neocolonial | **0.829** | 89.0% |

**Observation:** High agreement (>87%) between Cosine and BERTJE across all topics. Structural has slightly lower Pearson (0.83) but highest agreement % (89%).

---

**Weight Tier Distances (pretrained_bertje):**

| Weight Tier | Mean Distance | N Terms |
|-------------|---------------|---------|
| core_problem (1.00) | 0.058 | 173 |
| strong_problem (0.95) | 0.055 | 461 |
| related_strong (0.85) | 0.056 | 48 |
| related_moderate (0.75) | 0.056 | 79 |
| era_context (0.55) | 0.067 | 21 |

**Observation:** Weight tiers show expected pattern - era_context (lowest weight) has highest distance from topic centers.

---

**Topic Co-occurrence (above threshold):**

| Topic Pair | Co-occurrence Count |
|------------|---------------------|
| Contemporary + Historical | 345 |
| Contemporary + Structural | 358 |
| Historical + Structural | 341 |
| All three topics | ~340 (overlap) |

**Observation:** Relatively balanced co-occurrence across topic pairs.

---

### Visualization Summary

| Aspect | Status | Notes |
|--------|--------|-------|
| Visualizations Generated | COMPLETE | 40 files in Visuals/ |
| Dictionary Clustering | GOOD | Clear topic separation in 2D/3D |
| Weight Tier Validation | GOOD | Expected distance patterns |
| Cosine-BERTJE Agreement | HIGH | 87-89% agreement |
| Cluster Quality | MIXED | Training reduced cluster metrics |

---

## Key Metrics Summary

### Dictionary Metrics

| Metric | Historical | Structural | Contemporary | Total |
|--------|------------|------------|--------------|-------|
| Term Count | 296 | 283 | 203 | 782 |
| Seed Terms | 54 | 40 | 49 | 143 |
| Expanded Terms | 242 | 243 | 154 | 639 |
| Seed % | 18.2% | 14.1% | 24.1% | 18.3% |
| Removal Rate | 1.3% | 5.7% | 32.3% | 13.1% |

### Weight Distribution

| Weight Tier | Count | % |
|-------------|-------|---|
| 1.00 (core_problem) | 173 | 22.1% |
| 0.95 (strong_problem) | 461 | 59.0% |
| 0.85 (related_strong) | 48 | 6.1% |
| 0.75 (related_moderate) | 79 | 10.1% |
| 0.55 (era_context) | 21 | 2.7% |

### Topic Independence Metrics

| Metric | Value | Assessment |
|--------|-------|------------|
| Silhouette Score (pretrained) | 0.422 | GOOD |
| Calinski-Harabasz (pretrained) | 498 | GOOD |
| Mean Topic Correlation (BERTJE) | 0.45 | MODERATE (acceptable) |
| Mean Topic Correlation (Cosine) | 0.58 | MODERATE (acceptable) |

### Scoring Quality Metrics

| Metric | Value |
|--------|-------|
| Global R² | 0.714 |
| Mean Pearson | 0.860 |
| Median Pearson | 0.974 |
| Cosine-BERTJE Agreement | 87-89% |
| Mean Within-Chunk CV | 0.140 |

### Per-Topic Performance

| Topic | R² | CV | Score Range |
|-------|-----|-----|-------------|
| Historical_Slavery_Colonialism | 0.747 | 0.243 | 6.61 |
| Contemporary_Manifestations | 0.732 | 0.249 | 7.27 |
| Structural_Continuity_Neocolonial | 0.563 | 0.180 | 4.97 |

### Multi-Label Distribution

| Topics Active | Chunks | % |
|---------------|--------|---|
| 0 | 704 | 24.8% |
| 1 | 944 | 33.2% |
| 2 | 588 | 20.7% |
| 3 | 604 | 21.3% |

---

## Overall Assessment

### Strengths

1. **Dictionary Quality**: Systematic 5-phase curation produced clean, well-weighted dictionary (782 terms, 13.1% removal rate)

2. **Training Effect**: Model training showed clear improvement:
   - Loss reduced 51.6%
   - R² improved from 0.409 → 0.714
   - Pearson correlation: 0.756 → 0.860

3. **Topic Correlation Reduction**: BERTJE training reduced inter-topic correlations compared to Cosine baseline (0.45 vs 0.58 mean)

4. **Multi-label Behavior**: Healthy distribution - 54.8% of chunks have 1-2 active topics, 21.3% have all 3

5. **High Agreement**: 87-89% agreement between Cosine and BERTJE scoring methods

6. **Historical & Contemporary Topics**: Both show good discriminative signal (CV ~0.24-0.25, R² ~0.73-0.75)

### Weaknesses

1. **Structural Topic Weakness**: Lower discriminative signal:
   - CV: 0.180 (vs 0.24-0.25 for others)
   - Score range: 4.97 (vs 6.6-7.3)
   - R²: 0.563 (vs 0.73-0.75)

2. **Contemporary Topic Size**: Smallest dictionary (203 terms) after 32.3% removal due to `uitsluiting` parent issues

3. **Within-Chunk Differentiation**: Mean CV of 0.14 is moderate - topics could be more distinct per chunk

4. **Cluster Quality Decrease**: Training reduced silhouette/Calinski-Harabasz metrics (may indicate more nuanced but less separated representations)

5. **Off-Topic Content**: 24.8% of chunks have no strong topic signal

### Recommended Actions

**For Next Iteration (Dictionary):**

1. **Strengthen Structural Topic**:
   - Add more distinctive seed terms specific to "continuity" and "legacy patterns"
   - Review terms that overlap heavily with Historical and Contemporary
   - Consider terms like: `nawerking`, `blijvende gevolgen`, `structurele ongelijkheid`

2. **Expand Contemporary Topic**:
   - Find alternative parent terms to replace problematic `uitsluiting`
   - Consider: `institutionele discriminatie`, `hedendaags racisme`, `systemische uitsluiting`

3. **Review Generic Terms**:
   - Check terms like `sluiten`, `blijft`, `voort` that may cause false positives
   - Consider lowering weights or removing if overly generic

**For Next Iteration (Training):**

4. **Investigate Cluster Quality Drop**:
   - Analyze why training decreased silhouette scores
   - Consider if this indicates overfitting or beneficial nuance

5. **Consider Corpus Filtering**:
   - 24.8% off-topic content may affect training
   - Could pre-filter chunks with minimum topic signal

**For Policy Corpus (Stage 2):**

6. **Apply Stricter Curation**:
   - Use higher cosine thresholds (≥0.72)
   - Remove domain-specific jargon not in policy language
   - Focus on contemporary manifestation language

7. **Monitor Structural Topic**:
   - Check if policy corpus provides better signal for "structural continuity"
   - May need topic redefinition if pattern persists

---

## Conclusion

**Overall Rating: GOOD**

This Stage 1 workflow successfully:
- Created a well-curated 782-term dictionary with proper 7-tier weighting
- Trained a model achieving R²=0.714 and 87-89% scoring agreement
- Produced healthy multilabel patterns across 2,840 chunks

**Primary Concern:** The Structural_Continuity_Neocolonial topic shows weaker discriminative signal. This may be inherent to the bridging nature of the concept, or may indicate dictionary/definition issues to address.

**Ready for Stage 2:** Yes, with recommended dictionary refinements for the Structural topic.

---

*Report generated: 2026-01-15*
*Framework: ITERATIVE_EVALUATION_FRAMEWORK.md*
*Workflow: slavery_structured-slavdict_pretrained_slavery_v1*
