# Project Context: Slavery Legacy Analysis in Dutch Caribbean Policy

**Last Updated**: 2025-11-27
**Purpose**: Maintain consistent understanding of research objective, methodology, and quality standards

---

## RESEARCH OBJECTIVE

**Research Question**: How is the legacy of Slavery addressed through developmental policies in the Dutch Caribbean during the International Decade for the People of African Descent (IDPAD, 2015-2024)?

**Thesis Location**: `Master Applied history ThesisCedric Berkelouw 545970.pdf`

**What We're Identifying**:
Chunks in policy/historical documents that demonstrate connections between:
- Contemporary developmental problems AND historical slavery/colonial causes
- Explicit or implicit references to slavery legacy
- Reparative approaches to development

**Why Computational Approach**:
- Need to analyze large corpus systematically
- Identify patterns across many documents that manual reading cannot scale to
- Bridge historical scholarship with policy discourse analysis

---

## THE 4-TOPIC FRAMEWORK

**Source**: Convergence of UN IDPAD priorities, historical scholarship (Nimako & Willemsen 2011; Staat en Slavernij 2023; Ketenen van het Verleden 2021), and political science research

### Topic 1: Educational Disadvantage & Brain Drain

**Contemporary problems**: Poor outcomes, dropout, language barriers, brain drain, racism in schools

**Slavery/colonial roots**: Enslaved denied education, colonial Dutch-language imposition devalued local languages, islands developed as extraction economies (not educational centers), post-emancipation restrictions continued

### Topic 2: Social Fragmentation & Racism

**Contemporary problems**: Colorism, hierarchies by skin color, intra-community racism, discrimination

**Slavery/colonial roots**: Racial hierarchy system institutionalized (White/mixed-race/Black), colorism persists, identity destruction (African cultures/languages/families erased), scientific racism embedded

### Topic 3: Governance Distrust & Corruption

**Contemporary problems**: Low institutional trust, patronage/clientelism, weak rule of law, Dutch paternalism

**Slavery/colonial roots**: Colonial governance designed to extract wealth (not serve people), complete denial of political agency, patronage as survival strategy under slavery, legal systems protected oppressors

### Topic 4: Persistent Poverty & Economic Vulnerability

**Contemporary problems**: High poverty, unemployment, tourism dependency, precarious labor, wealth inequality

**Slavery/colonial roots**: Extractive economy for Dutch benefit only, **zero wealth transfer at emancipation** (Theodoridis 2024: emancipation had zero impact on wealth distribution—planters kept land, enslaved got nothing), economic segregation to lowest-wage work, no reparations

### Cross-Cutting: **DENIED AGENCY**

All topics stem from systematic denial of agency under slavery:
- Educational: denied right to learn
- Social: denied cultural identity/human dignity
- Governance: denied political participation/self-determination
- Economic: denied property ownership/fair compensation

**Critical Understanding**: These aren't neutral "developmental categories"—they are structural legacies of slavery that policy often fails to recognize as historically rooted.

---

## METHODOLOGY OVERVIEW

**Approach**: Dictionary-based cosine labeling → BERTje training → Policy analysis

### The 8-Step Workflow

**Main Notebook**: `dictionary_discovery_v16_improved_scoring.ipynb`

1. **PDF → Chunks**: Convert documents to text segments
2. **Clean Seed Dictionary**: Core problem vocabulary for 4 topics (`problem_oriented_legacy_seed_v6_4topics.csv`)
3. **Expand Dictionary**: Use BERTje embeddings to find semantically related terms
4. **Curate Dictionary**: Review expanded terms, assign weights based on relevance
5. **Build Topic Vectors**: Create weighted vocabulary representations per topic
6. **Cosine Label Chunks**: Score chunks for topic relevance (creates training data)
7. **Train BERTje**: Model learns to recognize topic patterns from labeled data
8. **Analyze Policy**: Apply trained model to identify relevant segments, visualize gaps

**Key Insight**: Steps 2-6 generate training labels (not ground truth); Step 7 learns patterns; Step 8 performs actual research analysis.

---

## QUALITY STANDARDS FOR LABELING SYSTEM

### Purpose of Dictionary-Based Labels

**Not ground truth** — Labels are training signals for BERTje to learn patterns

**Goal**: BERTje learns to differentiate:
- Highly relevant chunks (strong connection to slavery-rooted problems) vs. irrelevant chunks
- Distinctive patterns for each topic
- Ability to generalize beyond explicit keywords

**Acceptable**: Small errors per chunk if overall pattern teaches distinction

**Unacceptable**: Flat/compressed scores that prevent learning confidence levels

### Critical Quality Metrics

**Score Range Requirement**:
- Strong topic presence should score **0.7-0.9**
- Weak/absent topic presence should score **<0.2**
- Need clear differentiation between high and low relevance

**Topic Differentiation Requirement**:
- Different topics should have **different score distributions**
- Standard deviation per topic should be **>0.20**
- Flat distributions (all scores ~0.3) prevent learning

**Pattern Quality Requirement**:
- **>50%** of chunks should have Good/Excellent pattern quality
  - **Excellent**: All 4 topic scores match semantic judgment
  - **Good**: 3-4 scores match, pattern shape learnable
  - **Fair**: 2 scores match, partially learnable
  - **Poor**: Pattern misleading for training

**Training Sufficiency Requirement**:
- **>60%** of chunks should be training-sufficient
  - **Yes**: BERTje can learn meaningful understanding from this pattern
  - **Marginal**: Pattern somewhat learnable but noisy
  - **No**: Pattern will confuse training

### Common Dictionary Problems to Avoid

**1. Score Compression**
- **Problem**: All scores clustered in narrow range (e.g., 0.2-0.5)
- **Cause**: Insufficient weight differentiation, too many medium-weight terms
- **Impact**: BERTje cannot learn confidence levels
- **Solution**: Stronger differentiation between core terms (high weight) and context terms (lower weight)

**2. Cross-Contamination**
- **Problem**: Terms appearing in all/most chunks lift all scores uniformly
- **Impact**: Creates background noise, obscures true topic signals
- **Common Culprits**: Generic development language (ontwikkeling, maatschappij)
- **Solution**: Remove terms that don't differentiate topics; specific vocabulary over generic

**3. Topic Under-representation**
- **Problem**: Some topics consistently score lower despite semantic presence
- **Cause**: Insufficient vocabulary for that topic
- **Impact**: BERTje under-learns that topic's patterns
- **Solution**: Add core terms with sufficient weight, expand topic-specific vocabulary

**4. Over-generalization**
- **Problem**: Topic scores too high in irrelevant contexts
- **Cause**: Terms too generic or broad
- **Impact**: False positives, noisy training signal
- **Solution**: Replace generic terms with more specific problem vocabulary

### Evaluation Strategy

**Sample**: 72 chunks stratified by 4 topics × 3 confidence levels = 12 conditions, 6 chunks each

**Note**: Primary labels used ONLY for stratified sampling, NOT as ground truth in evaluation

**Assessment Dimensions**:
1. **Pattern Quality**: Do all 4 scores match semantic judgment?
2. **Training Sufficiency**: Can BERTje learn meaningful patterns?
3. **Per-Topic Alignment**: Does each topic score match semantic presence?

**Success Criteria Before Proceeding to BERTje Training**:
- Pattern quality >50% Good/Excellent
- Training sufficiency >60% Yes
- Score ranges: 20%+ of strong chunks score >0.7
- Topic differentiation: std dev >0.20 per topic

---

## DICTIONARY STRUCTURE & GUIDELINES

**Seed Dictionary File**: `problem_oriented_legacy_seed_v6_4topics.csv`

**Format**:
```
topic,term,weight,category
Educational Disadvantage & Brain Drain,brain drain,1.0,core_problem
Educational Disadvantage & Brain Drain,onderwijs,0.9,related
Educational Disadvantage & Brain Drain,slavernij,0.8,historical
Educational Disadvantage & Brain Drain,curacao,0.75,geography
Educational Disadvantage & Brain Drain,1863,0.7,era_marker
```

### The Dual Challenge: Topic AND Scope

**Core Dictionary Difficulty**: The dictionary must simultaneously identify chunks that are:
1. **Relevant to TOPIC** (Educational/Racism/Governance/Economic problems)
2. **Relevant to SCOPE** (Dutch Caribbean + slavery/colonial legacy)

**Problem**: Terms serving one function can interfere with the other:
- **Geographic/era terms** (curacao, bonaire, 1863, slavernij) help identify scope (Dutch Caribbean + slavery context)
- BUT if weighted too high, they appear in most chunks → lift all scores uniformly → create background noise
- **Topic-specific terms** (onderwijs, corruptie, armoede) help identify specific problems
- BUT if too generic, they don't distinguish slavery-rooted problems from general developmental problems elsewhere

**Example of Tension**:
- Chunk about education in Curacao + mentions slavery → Should score HIGH for Educational + scope
- Chunk about education in Curacao, no slavery connection → Should score MEDIUM (topic yes, scope partial)
- Chunk about slavery in Curacao, no educational content → Should score LOW for Educational (scope yes, topic no)
- Chunk about education in Amsterdam → Should score LOW (topic yes, scope no)

**Balancing Act**:
- Scope terms need to be present but **weighted lower** or used strategically across topics
- Topic terms need to be **specific enough** to capture slavery-rooted problems, not just any developmental problem
- Intersection of topic + scope creates the ideal signal

**Approaches to Balance** (to be tested in iterations):
- Use scope terms (geographic, historical) at **moderate weights** (0.5-0.7) across all topics to create baseline
- Use topic-specific terms at **higher weights** (0.9-1.0) to differentiate topics
- Use **slavery-specific formulations** of problems (e.g., "colonial education system" not just "education system") to capture intersection
- Test different weight configurations to find optimal balance

### Weight Guidelines

**Core problem terms** (weight 0.95-1.0):
- Central problematic terms that define the topic
- Should be specific to the topic, not generic
- Examples: brain drain, racisme, corruptie, armoede

**Related domain terms** (weight 0.85-0.9):
- Topic-specific vocabulary
- Examples: onderwijs, school (for Educational), bestuur, overheid (for Governance)

**Historical context terms** (weight 0.7-0.8):
- Terms providing historical framing
- Should be topic-specific where possible
- Balance: needed for scope, but can create cross-contamination if too broad

**Geographic markers** (weight 0.5-0.7):
- Help identify geographic scope (Dutch Caribbean)
- Risk: appear in most chunks, can create background noise
- Balance needed: present for scope identification but not dominant

**Era markers** (weight 0.7):
- Historical period markers (1863, slavernijverleden, koloniaal)
- Help identify temporal scope (slavery/colonial era)
- Risk: can over-score chunks that mention history without connecting to contemporary problems
- Balance: needed for scope but should be moderated

### Dictionary Curation Principles

**When Adding Terms**:
1. **Specificity**: Is this term specific enough to differentiate topics?
2. **Coverage**: Does this term appear in actual chunks discussing the topic?
3. **Scope vs. Topic**: Does this term identify topic, scope, or both?
4. **Weight**: How central is this term to topic + scope intersection?

**When Adjusting Weights**:
1. **Role**: Is this primarily for topic differentiation or scope identification?
2. **Frequency**: How often does this term appear across chunks?
3. **Discrimination**: Does this term help distinguish relevant from irrelevant chunks?
4. **Balance**: Are scope terms and topic terms weighted appropriately relative to each other?

**Balancing Topics**:
- Economic and Governance topics often need MORE vocabulary than Educational/Racism
- Check: Do all topics have comparable numbers of high-weight core terms?
- Check: Are topic-specific terms strong enough to differentiate despite shared scope terms?

**Historical vs. Contemporary**:
- Balance historical context terms (for scope) with contemporary problem terms (for topic)
- Contemporary problem vocabulary often provides better topic differentiation
- Historical vocabulary provides scope grounding

---

## ITERATION WORKFLOW

### Phase 1: Dictionary Preparation
1. Review current dictionary weights and vocabulary
2. Identify problematic patterns from previous evaluation
3. Adjust weights/terms to address identified problems
4. Test balance between scope and topic identification
5. Save updated dictionary version

### Phase 2: Labeling & Scoring
1. Build topic vectors from updated dictionary
2. Score evaluation sample (72 chunks) with cosine similarity
3. Check score distributions: mean, std dev, min, max per topic
4. Verify score ranges expand beyond 0.6 for strong presence
5. Verify topics have differentiated distributions

### Phase 3: Evaluation
1. Perform semantic evaluation on 72-chunk sample
2. Calculate pattern quality distribution
3. Calculate training sufficiency distribution
4. Calculate per-topic alignment (correct/too high/too low/severely wrong)
5. Check against success criteria

### Phase 4: Decision Point
- **If criteria met** → Proceed to BERTje training (Phase 5)
- **If criteria NOT met** → Return to Phase 1, iterate dictionary

### Phase 5: BERTje Training
1. Label full corpus with validated dictionary
2. Prepare train/validation splits
3. Fine-tune BERTje classifier on labeled data
4. Validate on held-out slavery corpus
5. Test domain transfer to policy documents

### Phase 6: Thesis Analysis
1. Apply trained BERTje to IDPAD-era policy documents (2015-2024)
2. Identify chunks addressing slavery-rooted problems
3. Analyze: Do policies acknowledge historical foundations?
4. Identify gaps: Which slavery legacies are ignored?
5. Evaluate reparative justice integration
6. Generate thesis findings and visualizations

---

## KEY PRINCIPLES

### Research Focus
- **End goal**: Understand how policy addresses (or ignores) slavery legacy
- **Means**: Computational methods to scale analysis across large corpus
- **NOT the goal**: Perfect dictionary or 100% accurate labels per chunk

### Quality Over Precision
- **Priority**: Pattern shape that enables BERTje learning
- **Acceptable**: 60-70% correct per-topic alignment if pattern quality is good
- **Unacceptable**: Flat distributions even if individual scores seem "reasonable"

### Iteration is Expected
- Dictionary-based topic modeling requires multiple iterations
- Each iteration reveals specific problems → address systematically
- Don't proceed to training until success criteria met

### The Dual Challenge
- Dictionary must identify BOTH topic (problem type) AND scope (Dutch Caribbean + slavery context)
- Balancing these functions requires careful weight calibration
- Expect tension between scope terms and topic terms—find optimal balance through iteration

### Domain Knowledge Integration
- Topic framework based on historical scholarship + community input
- Not arbitrary categories—these are documented structural legacies
- Understanding historical roots informs dictionary curation choices

---

## CRITICAL QUESTIONS FOR SELF-CHECK

### During Dictionary Curation
1. **Does this term identify topic, scope, or both?** → Weight accordingly
2. **Does this term appear broadly without differentiating?** → Reduce weight or remove
3. **Is this term specific enough to capture slavery-rooted problems?** → Not just any developmental problem
4. **Are scope terms balanced so they ground without dominating?** → Moderate weights for geographic/historical terms
5. **Are Economic and Governance dictionaries as rich as Educational and Racism?** → Often need expansion

### During Evaluation
1. **Are score ranges expanding beyond 0.6 for strong presence?** → If no, insufficient differentiation
2. **Do different topics have different score distributions?** → If no, too much shared vocabulary
3. **Is pattern quality >50% Good/Excellent?** → If no, dictionary needs refinement
4. **Is training sufficiency >60% Yes?** → If no, do NOT proceed to training
5. **Are scope terms helping or hindering topic differentiation?** → Check if geography/history terms create noise

### Before Proceeding to Next Phase
1. **Have I met all success criteria?** → Be honest about metrics
2. **Am I iterating based on specific identified problems?** → Not random trial-and-error
3. **Do I understand what caused the previous iteration's problems?** → Learn from each iteration
4. **Have I tested the balance between topic and scope identification?** → Both must work together

---

## KEY FILE LOCATIONS

### Context Documents
- **This context**: `PROJECT_CONTEXT_MASTER.md`
- **Topic framework detail**: `TOPIC_FRAMEWORK_CONTEXT.md`
- **Thesis PDF**: `Master Applied history ThesisCedric Berkelouw 545970.pdf`

### Workflow & Data
- **Main workflow notebook**: `dictionary_discovery_v16_improved_scoring.ipynb`
- **Seed dictionary**: `problem_oriented_legacy_seed_v6_4topics.csv`
- **Workflow data folder**: `workflow_data\slavery_Slavdict_pretraining_slavery_v{version}\`

### Evaluation Outputs (version-specific)
- Evaluation reports: `COSINE_EVALUATION_REPORT_v{version}.md`
- Evaluation results CSV: `semantic_evaluation_results_v{version}.csv`
- Scores data: `workflow_data\...\Cosine_labeling\scores_all_labeled.csv`

---

## IF YOU LOSE CONTEXT MID-TASK

1. Read this document: `PROJECT_CONTEXT_MASTER.md`
2. Read topic framework: `TOPIC_FRAMEWORK_CONTEXT.md`
3. Check latest evaluation report for current status
4. Identify which workflow phase you're in (Phases 1-6 above)
5. Review relevant principles and quality standards
6. Continue from appropriate workflow step

---

**Version**: 1.0 (2025-11-27)
**Next Update**: After completing dictionary iteration and evaluation
