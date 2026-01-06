# Section 3: Multi-Model Display - Summary

## Overview

Section 3 (Dictionary Fitness Visualizations) has been updated to show **all available models** instead of selecting a single validation model.

---

## Changes Made

### Cell 9 (9.7): Weight Tier Validation
**Status**: ✅ UPDATED

**What it now does**:
1. Calculates intra-topic distances for **ALL** models
2. Creates **combined statistics table** (CSV) with all models
3. Generates **separate visualization** for each model

**Outputs**:
- `weight_tier_validation_<model_name>.html` (one per model)
- `weight_tier_validation_<model_name>.png` (one per model, if SAVE_STATIC=True)
- `weight_tier_stats_combined.csv` (all models in one table)

**Example**:
If you have `pretrained_bertje` and `slavery_trained` loaded:
- `weight_tier_validation_pretrained_bertje.html`
- `weight_tier_validation_slavery_trained.html`
- `weight_tier_stats_combined.csv` (with both models' statistics)

---

### Cell 10 (9.8): Expansion Quality Validation
**Status**: ⚠️ NEEDS UPDATE

**Current behavior**: Uses hardcoded model selection (line 43)
```python
validation_model = 'policy_trained' if 'policy_trained' in dict_embeddings else list(dict_embeddings.keys())[0]
```

**Needed changes**:
1. Loop over all models
2. Calculate centroids per model
3. Calculate distances per model
4. Create separate 2D scatter plot per model
5. Create combined statistics table

This is more complex because:
- Centroids are model-specific
- PCA is model-specific (each model has different embedding space)
- Need separate 2D projections per model

---

### Cell 11 (9.9): Dictionary Term Clustering - 2D
**Status**: ✅ ALREADY MULTI-MODEL

This cell already shows all models in a multi-model comparison visualization.

---

### Cell 12 (9.10): Dictionary Term Clustering - 3D (if exists)
**Status**: ✅ LIKELY ALREADY MULTI-MODEL

Section 3 dictionary clustering cells typically already handle multiple models.

---

## Decision Points

### For Cell 10 (Expansion Quality): Two Approaches

#### Approach A: Full Multi-Model (Recommended)
**What**: Separate visualization per model + combined stats table

**Pros**:
- Consistent with Cell 9
- Compare expansion quality across models
- See which model best distinguishes seeds vs expanded

**Cons**:
- More complex to implement
- Multiple PCA projections needed

**Outputs**:
- `expansion_quality_<model_name>.html` (one per model)
- `expansion_quality_stats_combined.csv`

#### Approach B: Keep Single Model (Simpler)
**What**: Use VALIDATION_MODEL setting (like before the update)

**Pros**:
- Simpler code
- One clear visualization

**Cons**:
- Inconsistent with Cell 9 (Weight Tier)
- Can't compare across models
- User might want to see all models

---

## Recommendation

**Update Cell 10 to full multi-model** (Approach A) to be consistent with Cell 9.

This gives you:
- Consistent Section 3 behavior (all cells show all models)
- Ability to compare expansion quality across models
- Combined tables for analysis
- Separate visualizations for clarity

---

## Implementation Plan for Cell 10

### Step 1: Calculate Per-Model Data
```python
model_results = {}

for model_name in dict_embeddings.keys():
    term_embeddings = dict_embeddings[model_name]

    # Calculate centroids from seeds
    topic_centroids = {}
    for topic in topics:
        topic_seeds_mask = seed_mask & (df_dict['topic'] == topic)
        if topic_seeds_mask.sum() > 0:
            seed_embeddings = term_embeddings[topic_seeds_mask]
            topic_centroids[topic] = seed_embeddings.mean(axis=0)

    # Calculate distances
    for topic in topics:
        if topic not in topic_centroids:
            continue
        topic_mask = df_dict['topic'] == topic
        topic_embeddings = term_embeddings[topic_mask]
        centroid = topic_centroids[topic]
        similarities = cosine_similarity(topic_embeddings, centroid.reshape(1, -1))
        distances = 1 - similarities.flatten()
        df_dict.loc[topic_mask, f'distance_to_centroid_{model_name}'] = distances

    # PCA for 2D visualization
    pca = PCA(n_components=2, random_state=PCA_RANDOM_STATE)
    term_embeddings_2d = pca.fit_transform(term_embeddings)

    model_results[model_name] = {
        'embeddings_2d': term_embeddings_2d,
        'centroids': topic_centroids,
        'pca': pca
    }
```

### Step 2: Create Combined Stats Table
```python
stats_data = []

for model_name in dict_embeddings.keys():
    distance_col = f'distance_to_centroid_{model_name}'

    # Seeds
    seed_distances = df_dict[seed_mask][distance_col]
    stats_data.append({
        'Model': model_name,
        'Group': 'Seeds',
        'Mean_Distance': seed_distances.mean(),
        'Std_Distance': seed_distances.std(),
        'Median_Distance': seed_distances.median(),
        'N_Terms': len(seed_distances)
    })

    # Expanded
    expanded_distances = df_dict[expanded_mask][distance_col]
    stats_data.append({
        'Model': model_name,
        'Group': 'Expanded',
        'Mean_Distance': expanded_distances.mean(),
        'Std_Distance': expanded_distances.std(),
        'Median_Distance': expanded_distances.median(),
        'N_Terms': len(expanded_distances)
    })

df_stats = pd.DataFrame(stats_data)
df_stats.to_csv(visuals_dir / 'expansion_quality_stats_combined.csv', index=False)
```

### Step 3: Create Separate Visualizations
```python
for model_name in dict_embeddings.keys():
    # Get model-specific data
    embeddings_2d = model_results[model_name]['embeddings_2d']
    df_dict[f'pca_x_{model_name}'] = embeddings_2d[:, 0]
    df_dict[f'pca_y_{model_name}'] = embeddings_2d[:, 1]

    # Create scatter plot
    fig = go.Figure()

    # Add seeds
    seed_data = df_dict[seed_mask]
    fig.add_trace(go.Scatter(
        x=seed_data[f'pca_x_{model_name}'],
        y=seed_data[f'pca_y_{model_name}'],
        mode='markers',
        name='Seeds',
        ...
    ))

    # Add expanded
    expanded_data = df_dict[expanded_mask]
    fig.add_trace(go.Scatter(
        x=expanded_data[f'pca_x_{model_name}'],
        y=expanded_data[f'pca_y_{model_name}'],
        mode='markers',
        name='Expanded',
        ...
    ))

    # Add centroids
    # ...

    fig.update_layout(
        title=f"Expansion Quality: {model_name}<br><sub>2D PCA Projection</sub>",
        ...
    )

    # Save
    fig.write_html(str(visuals_dir / f'expansion_quality_{model_name}.html'))
```

---

## Benefits of Multi-Model Section 3

### 1. Cross-Model Comparison
- See which model best separates weight tiers
- Compare expansion quality across models
- Identify model-specific strengths

### 2. Consistent Analysis
- All Section 3 visualizations use same approach
- Easy to understand: each model gets its own graph
- Combined tables for statistical comparison

### 3. Model Selection Insights
- Objectively compare models
- Choose best model for your thesis
- Show progression: pretrained → slavery → policy

### 4. Thesis Value
- Can show: "Model X shows better weight tier separation"
- Can demonstrate: "Finetuning improved expansion quality"
- Evidence-based model selection

---

## Current Status Summary

| Cell | Visualization | Status | Output Files |
|------|--------------|--------|--------------|
| 9.7  | Weight Tier  | ✅ Updated | `weight_tier_validation_<model>.html` + combined CSV |
| 9.8  | Expansion Quality | ⚠️ Needs Update | Currently single model |
| 9.9  | Dict Clustering 2D | ✅ Already Multi | Multi-model comparison |
| 9.10 | Dict Clustering 3D | ✅ Likely Multi | Multi-model comparison |

---

## Next Steps

1. **Review** updated Cell 9 to confirm it works as expected
2. **Decide** on Cell 10: Full multi-model or keep single model?
3. **Implement** Cell 10 update if choosing multi-model approach
4. **Test** all Section 3 cells together
5. **Document** which models to enable for final thesis visualizations

---

*Updated: 2026-01-05*
*Feature: Multi-model display in Section 3 (Dictionary Fitness)*
