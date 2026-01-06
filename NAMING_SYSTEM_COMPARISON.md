# Workflow Naming System Comparison

## Your Current System

### Format
```
{model_type}_{topic}_{date}_v{N}
```

### Example
```
Finetuned_slaverypolicy-Slavery-Policy_11.13.25_v1
```

### What it tracks
- ✅ Model type (Pretrained/Finetuned)
- ✅ Topic target (Slavery-Policy)
- ⚠️ Date (not very informative)
- ✅ Version

### What it DOESN'T track
- ❌ **Corpus**: What documents are being analyzed?
- ❌ **Vector source**: Which dictionary creates the topic vectors?
- ❌ **Training details**: What was BERTJE trained on?
- ❌ **Clear separation**: Hard to compare across dimensions

### Problems
1. **Ambiguous**: "Finetuned_slaverypolicy" - finetuned on what? with what?
2. **Hard to compare**: Can't easily see impact of different dictionaries
3. **Date-based**: Version should track iterations, not dates
4. **Missing info**: Can't tell from name alone what dictionary/corpus was used

---

## Proposed System

### Format
```
{corpus}_{vector_source}_{bertje_training}_{target}_v{N}
```

### Example
```
policy_policy-dict-v1_ft-policy_slavery-policy_v1
```

### What it tracks
- ✅ **Corpus**: Policy documents
- ✅ **Vector source**: Policy-focused dictionary v1
- ✅ **BERTJE training**: Finetuned on policy corpus
- ✅ **Target**: Identifying slavery-policy content
- ✅ **Version**: Iteration number (not date)

### Benefits
1. **Complete provenance**: Everything needed to reproduce
2. **Easy comparison**: Change one component, see impact
3. **Self-documenting**: Name tells the full story
4. **Structured**: Each component has clear meaning

---

## Side-by-Side Comparison

| Aspect | Current | Proposed |
|--------|---------|----------|
| **Corpus tracking** | ❌ Not tracked | ✅ First component |
| **Dictionary tracking** | ❌ Not tracked | ✅ Second component |
| **BERTJE training** | ⚠️ Vague ("Finetuned_slaverypolicy") | ✅ Explicit ("ft-policy") |
| **Target** | ✅ Clear ("Slavery-Policy") | ✅ Clear ("slavery-policy") |
| **Version logic** | ⚠️ Date-based | ✅ Iteration-based |
| **Reproducibility** | ⚠️ Missing information | ✅ Complete information |
| **Comparison** | ❌ Hard to compare | ✅ Easy to compare |
| **Length** | Shorter (but less informative) | Longer (but complete) |

---

## Real Examples: Your Workflows

### Current Naming
```
1. Pretrained_Slavery-Slavery_10.30.25_v1
   → What corpus? What dictionary? Unclear!

2. Finetuned_Slavery-Slavery-Policy_11.01.25_v1
   → Finetuned on what? With what dictionary?

3. Finetuned_slaverypolicy-Slavery-Policy_11.13.25_v1
   → Is this different from #2? How?

4. pretrained-Slavery_11.10.25_succes
   → What's "succes"? Different from #1 how?
```

### Proposed Naming
```
1. slavery_slavery-dict_pretrained_slavery_v1
   → Slavery corpus, slavery dictionary, base BERTJE, identifying slavery

2. policy_slavery-dict_ft-policy_slavery-policy_v1
   → Policy corpus, slavery dict, policy-finetuned BERTJE, identifying slavery in policy

3. policy_policy-dict-v1_ft-policy_slavery-policy_v1
   → Policy corpus, NEW policy dict v1, policy-finetuned BERTJE, identifying slavery in policy

4. slavery_slavery-dict_pretrained_slavery_v2
   → Same as #1 but iteration 2 (the "succes" version)
```

Now you can instantly see:
- **#2 vs #3**: Same corpus/BERTJE, but #3 uses policy-focused dictionary
- **#1 vs #4**: Same setup, different iteration
- **#2 vs #3**: Evolution from slavery-dict to policy-dict-v1

---

## Use Cases

### Comparing Different Dictionaries
```
Same everything, different dictionaries:

policy_slavery-dict_ft-policy_slavery-policy_v1
policy_policy-dict-v1_ft-policy_slavery-policy_v1
policy_combined-dict_ft-policy_slavery-policy_v1

→ Instantly clear: testing dictionary impact
```

### Comparing BERTJE Training
```
Same everything, different BERTJE:

policy_policy-dict-v1_pretrained_slavery-policy_v1
policy_policy-dict-v1_ft-policy_slavery-policy_v1
policy_policy-dict-v1_ft-slavery_slavery-policy_v1

→ Instantly clear: testing finetuning impact
```

### Comparing Corpora
```
Same everything, different corpus:

policy_policy-dict-v1_ft-policy_slavery-policy_v1
historical_policy-dict-v1_ft-policy_slavery-policy_v1
mixed_policy-dict-v1_ft-policy_slavery-policy_v1

→ Instantly clear: testing corpus generalization
```

---

## Migration Path

### Phase 1: Adopt for New Workflows
- Keep existing workflows as-is
- Use new naming for all future workflows
- Document mapping in a conversion table

### Phase 2: Create Conversion Table
```python
OLD_TO_NEW_MAPPING = {
    "Pretrained_Slavery-Slavery_10.30.25_v1":
        "slavery_slavery-dict_pretrained_slavery_v1",

    "Finetuned_slaverypolicy-Slavery-Policy_11.13.25_v1":
        "policy_slavery-dict_ft-policy_slavery-policy_v1",

    "pretrained-Slavery_11.10.25_succes":
        "slavery_slavery-dict_pretrained_slavery_v2",
}
```

### Phase 3: Optional Renaming
- Create symlinks from old names to new names
- Update references in notebooks
- Keep old directories for now

---

## Implementation

### 1. Copy Helper Script
The `workflow_naming_helper.py` file provides:
- `generate_workflow_name()` - Auto-generate names
- `parse_workflow_name()` - Parse names back to components
- `get_workflow_description()` - Human-readable description
- `compare_workflows()` - Compare two workflows

### 2. Update Your Notebook Config
Replace your current config with:
```python
config = {
    "workflow": {
        "corpus": "policy",
        "vector_source": "policy-dict-v1",
        "bertje_training": "ft-policy",
        "target": "slavery-policy",
        "version": None,  # Auto-increments
        "metadata": { ... }
    }
}

# Generate name automatically
workflow_name, version = generate_workflow_name(config['workflow'])
```

See `notebook_config_snippet.py` for full example.

### 3. Run Your Workflow
Everything else stays the same! Only the naming changes.

---

## Quick Reference

### Component Options

#### Corpus (What you're analyzing)
- `policy` - Policy documents
- `historical` - Historical texts
- `parliament` - Parliamentary records
- `mixed` - Multiple sources
- Custom: `{your-corpus-name}`

#### Vector Source (Dictionary for topic vectors)
- `pretrained` - Base SBERT (no dictionary)
- `slavery-dict` - Slavery-focused dictionary
- `policy-dict` - Policy-focused dictionary
- `policy-dict-v1` - Specific version
- `combined-dict` - Merged dictionaries

#### BERTJE Training (How model was trained)
- `pretrained` - Base BERTje (no finetuning)
- `ft-policy` - Finetuned on policy corpus
- `ft-slavery` - Finetuned on slavery texts
- `ft-mixed` - Finetuned on mixed corpus

#### Target (What you're identifying)
- `slavery` - Historical slavery
- `colonialism` - Colonial systems
- `racism` - Modern racism
- `slavery-policy` - Slavery in policy context
- `4topic` / `5topic` - Multi-topic classification

---

## Your Next Workflow

Based on your curated dictionary work:

```python
"workflow": {
    "corpus": "policy",
    "vector_source": "policy-dict-v1",  # Your new dictionary!
    "bertje_training": "ft-policy",
    "target": "slavery-policy",
    "version": None,
    "metadata": {
        "dictionary_file": "Curated_dictionary_policy_focused.csv",
        "dictionary_size": 563,
        "notes": "Combined policy-focused dictionary with enhanced colonial terms"
    }
}
```

Generates: **`policy_policy-dict-v1_ft-policy_slavery-policy_v1`**

This clearly shows you're using the new policy-focused dictionary (v1) to analyze policy documents!

---

## Questions?

- **Too long?** → Information > brevity. Reproducibility matters.
- **Underscores or dashes?** → Underscores separate components, dashes within components
- **What about dates?** → Use version numbers. Dates in metadata if needed.
- **Backwards compatible?** → Yes, keep old workflows, use new naming forward

The goal: **From the name alone, anyone (including future you) should know exactly what the workflow does.**
