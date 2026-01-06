# Validation Model Configuration

## Summary

Added `VALIDATION_MODEL` configuration setting to allow manual selection of which model to use for single-model visualizations (like weight tier validation).

---

## Configuration Setting

### Location: Cell 1

```python
# VALIDATION MODEL FOR SINGLE-MODEL VISUALIZATIONS
# Which model to use for visualizations that show only one model
# Set to specific model name or None for automatic selection
VALIDATION_MODEL = None  # Options: None, 'policy_trained', 'slavery_trained', 'pretrained_bertje'
```

---

## Options

### Option 1: `None` (Default - Automatic Selection)
```python
VALIDATION_MODEL = None
```

**Priority order**:
1. **policy_trained** (most specific to your thesis corpus)
2. **slavery_trained** (domain-adapted for slavery legacy)
3. **pretrained_bertje** (base Dutch BERT)

**Rationale**:
- policy_trained → most specific to policy corpus
- slavery_trained → domain-adapted, understands slavery legacy terms
- pretrained_bertje → base model, general Dutch understanding

This order goes from **most specific to most generalized**.

### Option 2: Force Specific Model
```python
VALIDATION_MODEL = 'slavery_trained'  # Always use slavery model
```

**When to use**:
- You want to see specifically how the slavery-adapted model understands the terms
- Comparing against slavery workflow expansion results
- Ensuring consistency with dictionary expansion model

```python
VALIDATION_MODEL = 'policy_trained'  # Always use policy model
```

**When to use**:
- Focusing on policy-specific thesis results
- Final thesis visualizations
- Most relevant to your research questions

```python
VALIDATION_MODEL = 'pretrained_bertje'  # Always use base model
```

**When to use**:
- Baseline comparison
- Showing improvement from domain adaptation
- General Dutch language understanding

---

## Which Visualizations Use This Setting

### Section 3: Dictionary Fitness Visualizations

All single-model visualizations in Section 3 use `VALIDATION_MODEL`:

1. **Cell 9.7: Weight Tier Validation**
   - Shows: Intra-topic distance by weight tier
   - Uses: One model's embeddings to calculate coherence

2. **Cell 9.8: Expansion Quality Validation** (if present)
   - Shows: Seed vs expanded term quality
   - Uses: One model's embeddings

3. **Other single-model dictionary visualizations**

### What About Multi-Model Comparisons?

Multi-model visualizations (like dictionary clustering 2D/3D with multiple models) are **NOT affected** by this setting. They show all enabled models side by side.

---

## How It Works

### In Visualization Cells:

```python
# Choose validation model based on VALIDATION_MODEL setting
if VALIDATION_MODEL is not None and VALIDATION_MODEL in dict_embeddings:
    # User specified a model - use it
    validation_model = VALIDATION_MODEL
    print(f"   Using user-specified model: {validation_model}")
else:
    # Auto-select with priority: policy > slavery > pretrained
    validation_model = None
    if 'policy_trained' in dict_embeddings:
        validation_model = 'policy_trained'
        print(f"   Auto-selected: policy_trained (most specific to thesis)")
    elif 'slavery_trained' in dict_embeddings:
        validation_model = 'slavery_trained'
        print(f"   Auto-selected: slavery_trained (domain-adapted)")
    elif 'pretrained_bertje' in dict_embeddings:
        validation_model = 'pretrained_bertje'
        print(f"   Auto-selected: pretrained_bertje (base model)")
    elif len(dict_embeddings) > 0:
        validation_model = list(dict_embeddings.keys())[0]
        print(f"   Auto-selected: {validation_model} (fallback)")
```

### Output Messages:

**With VALIDATION_MODEL = None (automatic)**:
```
======================================================================
VISUALIZATION 9.7: Weight Tier Validation
======================================================================

Calculating intra-topic distances...
   Auto-selected: policy_trained (most specific to thesis)
```

**With VALIDATION_MODEL = 'slavery_trained' (manual)**:
```
======================================================================
VISUALIZATION 9.7: Weight Tier Validation
======================================================================

Calculating intra-topic distances...
   Using user-specified model: slavery_trained
```

---

## Use Cases

### Use Case 1: Thesis Final Visualizations
```python
# Cell 1
VALIDATION_MODEL = 'policy_trained'
```

**Why**: Your thesis focuses on policy corpus, so policy_trained is most relevant.

### Use Case 2: Dictionary Quality Analysis
```python
# Cell 1
VALIDATION_MODEL = 'slavery_trained'
```

**Why**: If dictionary was expanded using slavery workflow, validation should use the same model for consistency.

### Use Case 3: Baseline Comparison
```python
# Run 1: Base model
VALIDATION_MODEL = 'pretrained_bertje'

# Run 2: Domain-adapted
VALIDATION_MODEL = 'slavery_trained'

# Run 3: Finetuned
VALIDATION_MODEL = 'policy_trained'
```

**Why**: Compare how different model stages understand the dictionary.

### Use Case 4: Let System Choose
```python
# Cell 1
VALIDATION_MODEL = None  # Default behavior
```

**Why**: Trust the automatic priority, which selects the most specific model available.

---

## Example Workflow

### Scenario: Analyzing Dictionary from Slavery Workflow

You're working with a dictionary that was expanded in the slavery workflow using the slavery_trained model.

**Setup**:
```python
# Cell 1
SOURCE_WORKFLOW = r"C:\...\workflow_Structureddict\slavery_structured-slavdict_pretrained_slavery_v1"
COMPARE_MODELS = {
    'base_cosine': True,
    'pretrained_bertje': True,
    'slavery_trained': True,
    'policy_trained': False
}
VALIDATION_MODEL = 'slavery_trained'  # Match expansion model
```

**Result**:
- Data loaded from slavery workflow
- Dictionary embeddings generated for: pretrained_bertje, slavery_trained
- Single-model visualizations use: **slavery_trained** (as specified)
- Multi-model comparisons show: both models side by side

---

## Priority Rationale

### Why Policy > Slavery > Pretrained?

**policy_trained**:
- Finetuned on YOUR policy corpus
- Most specific to your thesis questions
- Understands policy-specific language best
- Most relevant for final thesis results

**slavery_trained**:
- Domain-adapted for slavery legacy
- Understands historical context
- Better than pretrained for this domain
- Good for dictionary validation

**pretrained_bertje**:
- Base Dutch BERT
- General language understanding
- Useful baseline
- No domain specialization

This order reflects **increasing specificity** to your research domain, with policy being the most specific and relevant to your thesis.

---

## Troubleshooting

### Issue: "Using user-specified model: policy_trained" but you wanted slavery
**Solution**: Check Cell 1 - you may have set `VALIDATION_MODEL = 'policy_trained'`

### Issue: "Auto-selected: pretrained_bertje" but you have slavery_trained loaded
**Check**:
1. Did slavery_trained load successfully in Cell 5?
2. Check Cell 5 output for errors
3. Is `COMPARE_MODELS['slavery_trained'] = True` in Cell 1?
4. Is `MODEL_PATHS['slavery_trained']` set correctly?

### Issue: Want different model for different visualizations
**Solution**:
1. Run first visualization with `VALIDATION_MODEL = 'slavery_trained'`
2. Save results
3. Change to `VALIDATION_MODEL = 'policy_trained'` in Cell 1
4. Re-run Cell 1
5. Re-run the visualization

Or: Use multi-model visualizations that show all models at once.

---

## Summary Table

| Setting | Priority | Use Case |
|---------|----------|----------|
| `None` | policy > slavery > pretrained | Default, automatic |
| `'policy_trained'` | Only policy | Final thesis visuals |
| `'slavery_trained'` | Only slavery | Match expansion model |
| `'pretrained_bertje'` | Only pretrained | Baseline comparison |

---

*Created: 2026-01-05*
*Feature: Configurable validation model selection*
*Default: Automatic priority (policy > slavery > pretrained)*
