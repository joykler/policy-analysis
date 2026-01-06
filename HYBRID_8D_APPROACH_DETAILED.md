# Hybrid 8D Approach: Detailed Implementation Guide

**Date**: 2025-11-27
**Purpose**: Detailed specification of hybrid approach using 8D scoring internally for training selection while maintaining 4D framework for thesis analysis

---

## Core Concept

**The Insight**: You can use different dimensional structures at different stages of your pipeline without changing your research questions or final analysis framework.

**The Strategy**:
- **Research layer** (thesis analysis): 4 integrated topics (Educational, Governance, Economic, Racism)
- **Training layer** (BERTje learning): 8 dimensions to identify implicit patterns
- **Bridge**: BERTje classifier outputs 4-topic predictions matching research questions

**Why This Works**: The 8D structure helps solve the training selection problem (identifying implicit patterns) without adding interpretation complexity to your final analysis.

---

## Pipeline Architecture

### Current v16 Pipeline (4D Throughout)

```
Stage 1: Dictionary (4D) → Cosine Label Slavery Corpus (4D scores)
         ↓
Stage 2: Train BERTje on slavery corpus
         ↓
Stage 3: Use encoder → Expand dictionary in policy space (4D)
         ↓
Stage 4: Cosine Label Policy Corpus (4D scores)
         ↓
Stage 5: Select training data (confidence thresholds on 4D scores)
         ↓
Stage 6: Train BERTje classifier (4D outputs)
         ↓
Stage 7: Apply to policy corpus → 4D topic predictions
         ↓
Stage 8: Thesis analysis (4D framework)
```

**Problem**: Stage 5 selection filters out implicit patterns (low margins in 4D scores).

### Hybrid Pipeline (8D Internal, 4D External)

```
Stage 1: Dictionary (8D: 4 problems + 4 contexts) → Cosine Label Slavery Corpus (8D scores)
         ↓
Stage 2: Train BERTje on slavery corpus (8D outputs)
         ↓
Stage 3: Use encoder → Expand dictionaries in policy space (8D)
         ↓
Stage 4: Cosine Label Policy Corpus (8D scores)
         ↓
Stage 5: HYBRID SELECTION (implicit + explicit patterns using 8D scores)
         ↓
         Compose 8D → 4D labels for training
         ↓
Stage 6: Train BERTje classifier (4D outputs)  ← SWITCH TO 4D HERE
         ↓
Stage 7: Apply to policy corpus → 4D topic predictions
         ↓
Stage 8: Thesis analysis (4D framework)
```

**Key Change**: Stages 1-5 use 8D to identify implicit patterns. Stage 6+ switches to 4D for research questions.

---

## The 8 Dimensions Defined

### Problem Dimensions (4)

**1. Problem_Educational**
- Core vocabulary: brain drain, onderwijs-achterstand, schooluitval, taalbarrière
- Related: onderwijs, school, papiamentu, curriculum, leerlingen
- **NO geographic or temporal terms**

**2. Problem_Governance**
- Core vocabulary: corruptie, wantrouwen, patronage, nepotisme, paternalisme
- Related: bestuur, autonomie, wetgeving, constitutie, parlement
- **NO geographic or temporal terms**

**3. Problem_Economic**
- Core vocabulary: armoede, werkloosheid, economische kwetsbaarheid, schuld
- Related: economisch, handel, monocultuur, afhankelijkheid
- **NO geographic or temporal terms**

**4. Problem_Racism**
- Core vocabulary: racisme, discriminatie, kleurisme, segregatie
- Related: huidskleur, vooroordelen, uitsluiting, raciaal
- **NO geographic or temporal terms**

### Context Dimensions (4)

**5. Context_Geographic_Caribbean**
- Island names: curaçao, bonaire, aruba, sint eustatius, saba
- Regional: caribisch nederland, antillen, bes-eilanden
- Languages: papiamentu, papiaments
- **NO problem or temporal terms**

**6. Context_Geographic_Dutch**
- Netherlands: nederland, nederlands, den haag, amsterdam
- Colonial admin: gouverneur, koninkrijk, rijksministerraad
- **NO problem or temporal terms**

**7. Context_Era_Slavery**
- Explicit slavery: slavernij, slavenhandel, slaafgemaakten, plantage
- Temporal: 1863, afschaffing, emancipatie, koloniaal, koloniale
- Historical framing: slavernijverleden, geschiedenis
- **NO problem or contemporary terms**

**8. Context_Era_Modern**
- Contemporary framing: vandaag, heden, huidige, nu, recent
- Modern institutions: IDPAD, VN, mensenrechten
- Policy language: beleid, programma, strategie, ontwikkeling
- **NO historical or slavery-specific terms**

---

## Critical Dictionary Curation Rules

### Separation Principle

**STRICT RULE**: Each term appears in EXACTLY ONE dimension dictionary.

**Why**: Prevents double-counting and allows independent scoring.

**Example Decision Tree**:
```
Term: "plantage-economie"
├─ Contains problem vocabulary? → Economic? NO (it's historical context)
├─ Contains geographic marker? → Geographic? NO (not location-specific)
├─ Contains slavery/historical? → Era_Slavery? YES
└─ Decision: Goes in Context_Era_Slavery (weight 0.9)

Term: "economische kwetsbaarheid"
├─ Contains problem vocabulary? → Economic? YES
├─ Contemporary or historical? → Modern (it's current problem framing)
└─ Decision: Goes in Problem_Economic (weight 1.0)

Term: "papiamentu"
├─ Contains problem vocabulary? → NO
├─ Contains geographic marker? → Caribbean? YES (language specific to region)
└─ Decision: Goes in Context_Geographic_Caribbean (weight 0.8)
```

### Ambiguous Terms Strategy

**Some terms inherently span dimensions**. Resolution strategies:

**1. Slavery-related problem terms** (e.g., "onderwijsuitsluiting")
- Historical: "beperkt onderwijs", "koloniaal onderwijs" → Context_Era_Slavery
- Contemporary: "onderwijsuitsluiting", "onderwijs-achterstand" → Problem_Educational

**2. Geographic-cultural terms** (e.g., "papiamentu")
- Language as marker: → Context_Geographic_Caribbean
- Language education as problem: "taalbarrière", "taalonderwijs" → Problem_Educational

**3. Temporal markers with problem framing** (e.g., "armoede na slavernij")
- If discussing historical context: → Context_Era_Slavery
- If discussing current problem: → Problem_Economic

**General rule**: Classify by **primary function** in sentence context. If term primarily identifies scope → Context. If term primarily identifies problem → Problem.

### Weight Calibration

**Problem dimensions** (aim for strong differentiation):
- Core problems: 0.95-1.0
- Related domain: 0.85-0.9
- Peripheral: 0.7-0.8

**Context dimensions** (aim for presence/absence):
- Strong markers: 0.8-0.9
- Clear markers: 0.7-0.8
- Weak markers: 0.6-0.7

**Rationale**: Context dimensions are mostly binary (Caribbean or not, Slavery-era or not). Problem dimensions need gradations (core vs. peripheral problem vocabulary).

---

## 8D Scoring Mechanics

### Step 1: Independent Dimension Scores

Score each chunk against 8 separate dictionaries:

```python
# For each chunk:
chunk_embedding = bert.encode(chunk_text)

# Score against 8 dimension vectors
scores = {
    'Problem_Educational': cosine(chunk_embedding, educational_vector),
    'Problem_Governance': cosine(chunk_embedding, governance_vector),
    'Problem_Economic': cosine(chunk_embedding, economic_vector),
    'Problem_Racism': cosine(chunk_embedding, racism_vector),
    'Context_Geo_Caribbean': cosine(chunk_embedding, geo_caribbean_vector),
    'Context_Geo_Dutch': cosine(chunk_embedding, geo_dutch_vector),
    'Context_Era_Slavery': cosine(chunk_embedding, era_slavery_vector),
    'Context_Era_Modern': cosine(chunk_embedding, era_modern_vector),
}
```

**Result**: 8 independent scores per chunk (each 0-1 range).

### Step 2: Composite Relevance Calculation

Combine dimensions to create 4-topic relevance scores:

```python
def calculate_composite_relevance(scores):
    """
    Compose 8D scores into 4 topic relevance scores.

    Formula for each topic:
    Relevance = Problem_score * Geographic_presence * Temporal_relevance

    Where:
    - Geographic_presence = max(Geo_Caribbean, 0.3 * Geo_Dutch)
      Rationale: Caribbean context primary; Dutch context relevant but less central

    - Temporal_relevance = Era_Modern + (0.3 * Era_Slavery)
      Rationale: Modern framing primary; historical framing adds context
    """

    # Geographic component (favor Caribbean)
    geo = max(scores['Context_Geo_Caribbean'],
              0.3 * scores['Context_Geo_Dutch'])

    # Temporal component (favor modern, include historical)
    temporal = scores['Context_Era_Modern'] + (0.3 * scores['Context_Era_Slavery'])
    temporal = min(temporal, 1.0)  # Cap at 1.0

    # Composite relevance per topic
    relevance = {
        'Educational': scores['Problem_Educational'] * geo * temporal,
        'Governance': scores['Problem_Governance'] * geo * temporal,
        'Economic': scores['Problem_Economic'] * geo * temporal,
        'Racism': scores['Problem_Racism'] * geo * temporal,
    }

    return relevance, scores  # Return both composite and raw 8D scores
```

**Key Design Choices**:

1. **Multiplicative composition**: Creates natural gradient (0.8 * 0.7 * 0.6 = 0.336)
2. **Geographic favoring Caribbean**: max(Caribbean, 0.3*Dutch) ensures Caribbean primary
3. **Temporal favoring Modern**: Modern + 0.3*Slavery balances implicit/explicit patterns
4. **Caps at 1.0**: Prevents inflated scores from addition

### Step 3: Pattern Classification

Use **raw 8D scores** to classify chunks into pattern types:

```python
def classify_pattern_type(scores):
    """
    Classify chunks by pattern type for training selection.
    """
    problem_present = max(
        scores['Problem_Educational'],
        scores['Problem_Governance'],
        scores['Problem_Economic'],
        scores['Problem_Racism']
    )

    # Explicit pattern: Strong problem + Slavery context
    if (problem_present >= 0.6 and
        scores['Context_Geo_Caribbean'] >= 0.7 and
        scores['Context_Era_Slavery'] >= 0.5):
        return 'EXPLICIT_HIGH'

    # Implicit pattern: Strong problem + Modern context + LOW slavery
    if (problem_present >= 0.6 and
        scores['Context_Geo_Caribbean'] >= 0.7 and
        scores['Context_Era_Modern'] >= 0.6 and
        scores['Context_Era_Slavery'] < 0.3):
        return 'IMPLICIT_HIGH'

    # Moderate pattern: Problem present with context
    if (problem_present >= 0.4 and
        scores['Context_Geo_Caribbean'] >= 0.5):
        return 'MODERATE'

    # Out of scope: Dutch context only or no Caribbean
    if (scores['Context_Geo_Dutch'] >= 0.6 and
        scores['Context_Geo_Caribbean'] < 0.4):
        return 'DUTCH_CONTEXT'

    # Low relevance
    return 'LOW'
```

---

## Training Data Selection Strategy

### Confidence-Based Stratified Sampling (Hybrid Approach)

**Goal**: Sample chunks that represent BOTH explicit patterns (from slavery corpus) AND implicit patterns (policy corpus style).

```python
def select_training_data(chunks_df, target_size=5000):
    """
    Hybrid selection strategy using 8D pattern classification.
    """

    # Classify all chunks by pattern type
    chunks_df['pattern_type'] = chunks_df.apply(
        lambda row: classify_pattern_type(row['8d_scores']),
        axis=1
    )

    # Target distribution for training
    target_distribution = {
        'EXPLICIT_HIGH': 0.30,    # 1500 chunks - Learn explicit linking
        'IMPLICIT_HIGH': 0.30,    # 1500 chunks - Learn implicit patterns
        'MODERATE': 0.30,         # 1500 chunks - Learn gradient
        'LOW': 0.10,              # 500 chunks  - Learn negative class
        'DUTCH_CONTEXT': 0.00,    # 0 chunks    - Out of scope, exclude
    }

    # Sample from each category
    sampled_chunks = []

    for pattern_type, proportion in target_distribution.items():
        n_samples = int(target_size * proportion)
        category_chunks = chunks_df[chunks_df['pattern_type'] == pattern_type]

        if len(category_chunks) >= n_samples:
            # Undersample if too many
            sampled = category_chunks.sample(n=n_samples, random_state=42)
        else:
            # Oversample with replacement if too few
            sampled = category_chunks.sample(n=n_samples, replace=True, random_state=42)

        sampled_chunks.append(sampled)

    training_data = pd.concat(sampled_chunks)

    return training_data
```

**Key Differences from Current v16 Approach**:

| Aspect | Current 4D | Hybrid 8D |
|--------|-----------|-----------|
| High confidence definition | max_score ≥0.4, margin ≥0.05 | EXPLICIT_HIGH **or** IMPLICIT_HIGH |
| Multi-topic chunks | Filtered as "none" | Captured as IMPLICIT_HIGH |
| Implicit patterns | Downsampled (20%) | Oversampled (30%) |
| Training distribution | 40% high, 40% low, 20% none | 30% explicit, 30% implicit, 30% moderate, 10% low |

### Composing 4D Labels from 8D Scores

Once chunks are selected, create 4D labels for training:

```python
def create_4d_training_labels(chunks_df):
    """
    Convert 8D scores to 4D topic labels for classifier training.
    """

    for idx, row in chunks_df.iterrows():
        # Calculate composite relevance (4 topics)
        relevance, raw_8d = calculate_composite_relevance(row['8d_scores'])

        # Convert to ordinal classes for training
        # Low: <0.30, Medium: 0.30-0.50, High: ≥0.50
        labels = {}
        for topic in ['Educational', 'Governance', 'Economic', 'Racism']:
            score = relevance[topic]
            if score < 0.30:
                labels[topic] = 0  # Low
            elif score < 0.50:
                labels[topic] = 1  # Medium
            else:
                labels[topic] = 2  # High

        chunks_df.at[idx, '4d_labels'] = labels

    return chunks_df
```

**Result**: Training data with 4D labels (Low/Medium/High per topic) selected using 8D pattern recognition.

---

## BERTje Training Configuration

### Stage 2: Initial Training on Slavery Corpus (8D outputs)

**Why train with 8D first**: BERTje learns to recognize problem dimensions independently from context dimensions.

```python
# Model architecture (Stage 2)
class BERTje8D(nn.Module):
    def __init__(self):
        self.bert = AutoModel.from_pretrained('GroNLP/bert-base-dutch-cased')
        self.dropout = nn.Dropout(0.1)

        # 8 independent classifiers (3 classes each: Low/Medium/High)
        self.problem_educational = nn.Linear(768, 3)
        self.problem_governance = nn.Linear(768, 3)
        self.problem_economic = nn.Linear(768, 3)
        self.problem_racism = nn.Linear(768, 3)
        self.context_geo_caribbean = nn.Linear(768, 3)
        self.context_geo_dutch = nn.Linear(768, 3)
        self.context_era_slavery = nn.Linear(768, 3)
        self.context_era_modern = nn.Linear(768, 3)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids, attention_mask=attention_mask)
        pooled = outputs.pooler_output
        pooled = self.dropout(pooled)

        # 8 independent predictions
        return {
            'Problem_Educational': self.problem_educational(pooled),
            'Problem_Governance': self.problem_governance(pooled),
            'Problem_Economic': self.problem_economic(pooled),
            'Problem_Racism': self.problem_racism(pooled),
            'Context_Geo_Caribbean': self.context_geo_caribbean(pooled),
            'Context_Geo_Dutch': self.context_geo_dutch(pooled),
            'Context_Era_Slavery': self.context_era_slavery(pooled),
            'Context_Era_Modern': self.context_era_modern(pooled),
        }
```

**Training objective**: Multi-task learning with 8 separate losses (one per dimension).

**Benefit**: Encoder learns to represent text in a way that separates problem patterns from context patterns.

### Stage 6: Final Training on Policy Corpus (4D outputs)

**Why switch to 4D**: Research questions are 4D. Final predictions should match thesis framework.

```python
# Model architecture (Stage 6)
class BERTje4D(nn.Module):
    def __init__(self, pretrained_8d_model):
        # REUSE encoder from Stage 2 (transfer learning)
        self.bert = pretrained_8d_model.bert  # Frozen or fine-tuned
        self.dropout = nn.Dropout(0.1)

        # 4 topic classifiers (3 classes each: Low/Medium/High)
        self.educational = nn.Linear(768, 3)
        self.governance = nn.Linear(768, 3)
        self.economic = nn.Linear(768, 3)
        self.racism = nn.Linear(768, 3)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids, attention_mask=attention_mask)
        pooled = outputs.pooler_output
        pooled = self.dropout(pooled)

        # 4 topic predictions
        return {
            'Educational': self.educational(pooled),
            'Governance': self.governance(pooled),
            'Economic': self.economic(pooled),
            'Racism': self.racism(pooled),
        }
```

**Training strategy**:
- Option A: **Freeze encoder**, only train 4D heads (faster, prevents forgetting)
- Option B: **Fine-tune encoder** with low learning rate (adapts to policy corpus)

**Recommended**: Option B with learning rate 1e-5 for encoder, 1e-4 for heads.

---

## Stage-by-Stage Implementation

### Stage 1: Create 8D Dictionaries

**Input**: Current `problem_oriented_legacy_seed_v6_4topics.csv`

**Process**:
1. Split each 4D topic dictionary into Problem + Context components
2. Extract geographic terms → Context_Geo_Caribbean
3. Extract temporal terms → Context_Era_Slavery, Context_Era_Modern
4. Create Context_Geo_Dutch (add Dutch-context vocabulary)
5. Ensure no term appears in multiple dictionaries

**Output**: 8 CSV files:
```
problem_educational_v7.csv
problem_governance_v7.csv
problem_economic_v7.csv
problem_racism_v7.csv
context_geo_caribbean_v7.csv
context_geo_dutch_v7.csv
context_era_slavery_v7.csv
context_era_modern_v7.csv
```

**Validation**:
- Check for duplicates across dictionaries
- Verify total terms ≈ current v6 + new Context_Geo_Dutch/Era_Modern
- Spot-check 10 terms per dictionary for correct classification

**Script**: `create_8d_dictionaries_v7.py`

### Stage 2: Score Evaluation Sample with 8D

**Input**: 72-chunk evaluation sample

**Process**:
1. Build 8 dimension vectors from 8D dictionaries
2. Score each chunk against all 8 dimensions
3. Calculate composite 4D relevance scores
4. Classify pattern types
5. Compare to v16 4D scores

**Output**: `evaluation_sample_8d_scores_v7.csv`

**Analysis questions**:
- Do Problem dimension scores reach 0.7-0.9 (without geographic cross-contamination)?
- Are implicit patterns identifiable (Problem high, Era_Slavery low)?
- Do composite 4D scores match semantic judgment?
- Is score differentiation better than v16?

**Decision point**: If 8D scoring shows improvement → proceed. If not → revise dictionary split or abandon 8D.

**Script**: `evaluate_8d_scoring_v7.py`

### Stage 3: Full Corpus 8D Labeling (Slavery Corpus)

**Input**: Full slavery corpus (~6,400 chunks)

**Process**:
1. Score all chunks with 8D
2. Classify pattern types
3. Analyze distribution: How many EXPLICIT_HIGH vs. IMPLICIT_HIGH vs. MODERATE?
4. Select training sample (~5,000 chunks) using stratified sampling

**Output**:
- `slavery_corpus_8d_scores_v7.csv` (all chunks)
- `slavery_training_sample_v7.csv` (selected chunks)

**Validation**:
- Check pattern type distribution matches target (30/30/30/10)
- Verify IMPLICIT_HIGH chunks genuinely have low Era_Slavery scores
- Manual review 20 chunks per pattern type

**Script**: `label_slavery_corpus_8d_v7.py`

### Stage 4: Train BERTje with 8D Outputs

**Input**: `slavery_training_sample_v7.csv`

**Process**:
1. Convert 8D scores to ordinal classes (Low/Medium/High per dimension)
2. Configure BERTje8D model architecture
3. Train with multi-task learning (8 separate losses)
4. Validate on held-out slavery corpus (20%)
5. Save trained model + encoder

**Output**:
- `bertje_8d_slavery_v7.pt` (full model)
- `bertje_encoder_v7.pt` (encoder only, for dictionary expansion)

**Metrics to track**:
- Per-dimension accuracy (Problem_Educational, etc.)
- Composite 4D topic accuracy (calculated from 8D predictions)
- Confusion matrices for each dimension

**Training config**:
```python
{
    "model": "GroNLP/bert-base-dutch-cased",
    "num_epochs": 5,
    "batch_size": 16,
    "learning_rate": 2e-5,
    "warmup_steps": 500,
    "weight_decay": 0.01,
    "max_length": 512,
}
```

**Script**: `train_bertje_8d_v7.py`

### Stage 5: Dictionary Expansion in Policy Space

**Input**:
- `bertje_encoder_v7.pt` (trained encoder)
- Policy corpus sample (1,000 chunks)
- Current 8D dictionaries

**Process**:
1. Load trained encoder (from Stage 4)
2. Embed current 8D dictionary terms in policy space
3. Embed policy corpus vocabulary
4. Find semantically similar terms for each dimension
5. Human curation of expanded terms
6. Create expanded 8D dictionaries

**Output**: 8 expanded dictionaries:
```
problem_educational_v7_expanded.csv
problem_governance_v7_expanded.csv
...
```

**Curation guidelines**:
- Accept terms that clearly match dimension function
- Reject terms that could belong to multiple dimensions
- Weight new terms 0.7-0.85 (lower than seed terms)

**Script**: `expand_8d_dictionaries_policy_v7.py`

### Stage 6: Score Policy Corpus with Expanded 8D

**Input**:
- Policy corpus (~1,000 chunks for final training)
- Expanded 8D dictionaries

**Process**:
1. Build dimension vectors from expanded dictionaries
2. Score policy chunks with 8D
3. Classify pattern types
4. Select training sample using implicit pattern criteria
5. Calculate composite 4D labels

**Output**: `policy_training_sample_v7.csv` (with 4D labels)

**Expected distribution**:
- More IMPLICIT_HIGH chunks than slavery corpus
- Fewer EXPLICIT_HIGH chunks
- Pattern types reflect policy corpus reality

**Script**: `label_policy_corpus_8d_v7.py`

### Stage 7: Train Final BERTje Classifier (4D Outputs)

**Input**:
- `policy_training_sample_v7.csv`
- `bertje_encoder_v7.pt` (pre-trained encoder)

**Process**:
1. Initialize BERTje4D model with pre-trained encoder
2. Train 4D classification heads
3. Option: Fine-tune encoder with low LR
4. Validate on held-out policy chunks
5. Save final classifier

**Output**: `bertje_4d_policy_classifier_v7.pt`

**Metrics to track**:
- Per-topic accuracy (Educational, Governance, Economic, Racism)
- Multi-label metrics (chunks can have multiple topics)
- Comparison to v16 baseline (4D throughout)

**Training config**:
```python
{
    "encoder_lr": 1e-5,      # Low LR for fine-tuning
    "head_lr": 1e-4,         # Higher LR for new heads
    "num_epochs": 3,
    "batch_size": 16,
    "freeze_encoder_epochs": 1,  # Freeze encoder first epoch
}
```

**Script**: `train_bertje_4d_classifier_v7.py`

### Stage 8: Apply to Full Policy Corpus

**Input**:
- `bertje_4d_policy_classifier_v7.pt`
- Full policy corpus (all IDPAD-era documents)

**Process**:
1. Load trained classifier
2. Predict 4D topic scores for all policy chunks
3. Identify high-relevance chunks per topic
4. Extract quotes and context
5. Generate visualizations

**Output**:
- `policy_corpus_predictions_v7.csv` (all predictions)
- `high_relevance_chunks_v7.csv` (for thesis analysis)
- Visualization files (topic distribution over time, etc.)

**Script**: `apply_classifier_policy_v7.py`

### Stage 9: Thesis Analysis (4D Framework)

**Input**: `high_relevance_chunks_v7.csv`

**Process**: Standard thesis analysis using 4D framework
- Which topics are most addressed in policy?
- Do policies acknowledge historical roots?
- Temporal trends (early IDPAD vs. late IDPAD)
- Gaps and omissions
- Reparative justice alignment

**Output**: Thesis findings, visualizations, quotes

---

## Validation Strategy

### Internal Validation (During Development)

**After Stage 2** (8D scoring on evaluation sample):
- [ ] Problem scores reach 0.7-0.9 for strong chunks?
- [ ] Context scores clearly differentiate Caribbean/Dutch, Slavery/Modern?
- [ ] Composite 4D scores match semantic judgment (72-chunk evaluation)?
- [ ] Pattern quality >60% Good/Excellent?

**After Stage 4** (BERTje 8D training):
- [ ] Per-dimension validation accuracy >80%?
- [ ] Model can differentiate explicit vs. implicit patterns?
- [ ] Composite 4D predictions reasonable?

**After Stage 7** (BERTje 4D classifier):
- [ ] Held-out policy validation accuracy >75%?
- [ ] Model recognizes implicit patterns (without "slavernij")?
- [ ] Predictions match human judgment on sample?

### External Validation (Against Research Questions)

**Qualitative checks**:
1. Manual review of top 100 high-relevance predictions per topic
2. Do these chunks genuinely address slavery-rooted problems?
3. Are false positives within acceptable bounds?

**Quantitative checks**:
1. Inter-rater reliability: Second coder rates 50 predictions
2. Agreement on topic presence (4D): κ >0.6?
3. Agreement on relevance level: κ >0.5?

**Comparison to baseline**:
- How do v7 (hybrid 8D) predictions compare to v16 (4D throughout)?
- Does v7 identify MORE implicit patterns?
- Are v7 predictions MORE accurate on policy corpus?

---

## Advantages of Hybrid Approach

### 1. Best of Both Worlds

**8D advantages for training selection**:
- ✓ Separates problem vocabulary from context
- ✓ Identifies implicit patterns (Problem high, Era_Slavery low)
- ✓ Reduces cross-contamination in scoring
- ✓ Creates natural relevance gradients through multiplication

**4D advantages for research**:
- ✓ Matches research questions directly
- ✓ Simpler interpretation (no composition rules)
- ✓ Easier to communicate findings
- ✓ Aligns with topic framework in literature

### 2. Solves Training Selection Problem

**Current v16 issue**: Margin requirements filter implicit multi-topic patterns.

**Hybrid solution**: 8D pattern classification explicitly identifies implicit patterns → includes them in training → BERTje learns to recognize them → better policy corpus performance.

### 3. Maintains Research Continuity

**No disruption to**:
- Research questions (still 4 topics)
- Theoretical framework (Educational, Governance, Economic, Racism)
- Literature alignment (existing scholarship uses similar categories)
- Thesis structure (chapters organized by 4 topics)

**Change is internal**: Training methodology improves without changing research framework.

### 4. Testable and Reversible

**Can test 8D on evaluation sample BEFORE committing**:
- If 8D scoring improves pattern quality → proceed
- If 8D scoring doesn't help → stay with improved 4D (multi-topic confidence criteria)

**Can compare final results**:
- Train two versions: v16 (4D) baseline vs. v7 (hybrid 8D)
- Evaluate both on same policy corpus
- Choose better performer for thesis

**Low risk**: If hybrid approach doesn't improve results, fall back to 4D system with alternative improvements (adjust thresholds, reduce geographic weights, etc.).

### 5. Encoder Transfer Learning

**Key insight**: Stage 2 (8D training) teaches encoder to separate problem dimensions from context dimensions.

**Benefit for Stage 7**: When training 4D classifier, encoder already understands:
- What educational problems look like (independent of context)
- What Caribbean context looks like (independent of problems)
- How to compose them (learned from 8D labels)

**Result**: 4D classifier learns faster and better because encoder pre-trained on decomposed structure.

---

## Potential Challenges and Mitigations

### Challenge 1: Dictionary Splitting Complexity

**Problem**: Some terms inherently span dimensions ("colonial education system" is both Educational and Era_Slavery).

**Mitigation**:
- Create decision tree for ambiguous terms (see "Critical Dictionary Curation Rules" section)
- When truly ambiguous, choose **primary function** (what role does term play most often?)
- Document decisions for consistency
- Accept that some arbitrary choices are necessary

### Challenge 2: Composition Rules Require Validation

**Problem**: Formula for composing 8D → 4D (`Problem * geo * temporal`) is theoretically motivated but untested.

**Mitigation**:
- Test multiple composition formulas on evaluation sample
- Compare to semantic judgment (72-chunk evaluation)
- Choose formula with best pattern quality scores
- Document formula rationale in methodology

**Alternative formulas to test**:
```python
# Option 1: Current proposal
relevance = problem * geo * temporal

# Option 2: Additive with weights
relevance = 0.6*problem + 0.3*geo + 0.1*temporal

# Option 3: Threshold + multiply
relevance = problem * (1 if geo>0.5 else 0.3) * (1 if temporal>0.5 else 0.3)

# Option 4: Max instead of multiply for contexts
relevance = problem * max(geo, temporal)
```

### Challenge 3: Training Complexity

**Problem**: More stages (8D→4D) means more hyperparameters, more training time, more potential failure points.

**Mitigation**:
- Use established hyperparameters from literature
- Start with Stage 2 validation: If 8D training fails, stop before investing in full pipeline
- Log all metrics at each stage
- Create checkpoint system: Can resume from any stage if failure occurs

### Challenge 4: Interpretability in Thesis

**Problem**: Methodology section needs to explain why using 8D internally but reporting 4D results.

**Mitigation**:
- Frame as "training strategy" not "topic framework"
- Analogy: "Just as computer vision models use many internal layers but output simple classifications, our approach uses dimensional decomposition internally while outputting integrated topic predictions"
- Emphasize: Research questions and findings are 4D; 8D is internal optimization

### Challenge 5: Increased Dictionary Maintenance

**Problem**: 8 dictionaries instead of 4 = more curation work, more potential inconsistency.

**Mitigation**:
- Create automated checks for cross-dictionary duplicates
- Use standardized curation workflow (see Stage 1 scripts)
- Document all curation decisions
- Version control dictionaries (track changes)

---

## Timeline Estimate

**Assuming 20 hours/week work time**:

| Stage | Task | Estimated Time |
|-------|------|----------------|
| 1 | Create 8D dictionaries from v6 | 8 hours |
| 2 | Score evaluation sample, validate | 4 hours |
| **Decision point** | Proceed with 8D or abandon? | 1 hour |
| 3 | Full slavery corpus 8D labeling | 3 hours |
| 4 | Train BERTje 8D | 6 hours (2h setup + 4h training) |
| 5 | Dictionary expansion in policy space | 12 hours (automated + curation) |
| 6 | Policy corpus 8D labeling + selection | 3 hours |
| 7 | Train BERTje 4D classifier | 4 hours |
| 8 | Apply to full policy corpus | 2 hours |
| 9 | Validation and comparison to v16 | 6 hours |
| **Total** | | **49 hours (~2.5 weeks)** |

**Critical path**: Stage 2 decision point (12 hours). If 8D doesn't show improvement, abandon and save 37 hours.

---

## Success Criteria

### Minimum Viable Success (Proceed to thesis)

- [ ] 8D scoring on evaluation sample: Pattern quality >60% Good/Excellent
- [ ] BERTje 4D classifier validation accuracy >75%
- [ ] Manual review of 100 predictions: >70% genuinely relevant
- [ ] Identifies ≥30 high-certainty policy chunks per topic
- [ ] Hybrid approach performs ≥as well as v16 4D baseline

### Optimal Success (Strong methodology)

- [ ] 8D scoring: Pattern quality >70% Good/Excellent
- [ ] Score ranges expand (strong chunks reach 0.7-0.9)
- [ ] Implicit pattern identification validated (human agreement κ>0.6)
- [ ] BERTje classifier validation accuracy >80%
- [ ] Hybrid approach significantly outperforms v16 baseline
- [ ] Thesis analysis yields clear, interpretable findings

### Failure Criteria (Abandon 8D)

- [ ] 8D scoring shows no improvement over 4D (pattern quality ≤v16)
- [ ] Score ranges don't expand (still max 0.6)
- [ ] Composition rules unclear or inconsistent
- [ ] Training time exceeds 60 hours with poor results
- [ ] BERTje predictions no better than random (accuracy <60%)

---

## Next Immediate Steps

### 1. Create 8D Dictionary Split Script (Highest Priority)

**File**: `create_8d_dictionaries_v7.py`

**Input**: `problem_oriented_legacy_seed_v6_4topics.csv`

**Process**:
```python
# Pseudocode structure:
1. Load v6 4D dictionary
2. For each term:
   a. Classify into one of 8 dimensions using decision tree
   b. Preserve weight
   c. Add to appropriate dimension dictionary
3. Create Context_Geo_Dutch terms (new vocabulary)
4. Create Context_Era_Modern terms (new vocabulary)
5. Validate: Check for duplicates
6. Export 8 CSV files
```

**Validation checks**:
- No term appears in >1 dictionary
- Total terms in 8D ≈ total in 4D + new context terms
- Each dimension has balanced vocabulary (not one dimension with 200 terms, another with 20)

### 2. Implement 8D Scoring on Evaluation Sample

**File**: `evaluate_8d_scoring_v7.py`

**Input**:
- 8 dimension dictionaries
- `chunks_for_semantic_eval_v16.csv` (72 chunks)

**Output**:
- `evaluation_sample_8d_scores_v7.csv`
- Comparison report vs. v16 4D scores

**Analysis**:
- Score distributions per dimension
- Pattern type classification distribution
- Composite 4D relevance vs. semantic judgment
- Decision: Proceed or abandon 8D?

### 3. Document Dictionary Split Decisions

**File**: `DICTIONARY_SPLIT_DECISIONS_v7.md`

**Content**:
- Decision tree for ambiguous terms
- List of all terms moved from 4D to each 8D dimension
- Rationale for difficult classification decisions
- Weight adjustments made

**Purpose**: Transparency and reproducibility for thesis methodology section.

---

## Conclusion

The hybrid 8D approach offers a **practical middle ground**:
- Uses 8D's advantages (pattern classification, cross-contamination reduction) for training selection
- Avoids 8D's disadvantages (interpretation complexity) by outputting 4D predictions
- Maintains research continuity (4D framework throughout thesis)
- Testable at early stage (evaluation sample) before full commitment

**Key insight**: Your pipeline has natural stages where dimensional structure can change. Exploit this by using the dimension structure that's optimal for each stage's purpose.

**Recommended action**: Implement Stages 1-2 (dictionary split + evaluation sample scoring). If results show improvement, proceed with full hybrid pipeline. If not, improve 4D system with multi-topic confidence criteria.

---

**Document by**: Claude (Sonnet 4.5)
**Date**: 2025-11-27
**See also**:
- [PROJECT_CONTEXT_MASTER.md](PROJECT_CONTEXT_MASTER.md) - Research overview
- [WORKFLOW_INTERACTION_ANALYSIS_v16.md](WORKFLOW_INTERACTION_ANALYSIS_v16.md) - Problem diagnosis
- [TOPIC_FRAMEWORK_CONTEXT.md](TOPIC_FRAMEWORK_CONTEXT.md) - 4D topic rationale
