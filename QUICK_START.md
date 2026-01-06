# Quick Start: v11 with New Naming System

## ✅ Your Notebook is Fixed!

All `KeyError: 'model_type'` issues have been resolved.

## 🚀 Run Your Workflow

### Step 1: Reload Notebook
Close and reopen `dictionary_discovery_v11.ipynb` in VS Code

### Step 2: Run Cell 2
Should output:
```
✓ Configuration loaded
Workflow: policy_Slavdict-policy_ft-slavery_slavery-policy_v1
```

### Step 3: Run Cell 55 (Create Workflow Folder)
```python
CREATE_NEW = True
fs = WorkflowFileSystem(CONFIG)
workflow_root = fs.create_workflow_folder()
```

Should create:
```
workflow_data/policy_Slavdict-policy_ft-slavery_slavery-policy_v1/
```

### Step 4: Continue Normally
All other cells should work as before!

---

## 📝 Your Current Configuration

**Workflow:** `policy_Slavdict-policy_ft-slavery_slavery-policy_v1`

| Component | Value | Meaning |
|-----------|-------|---------|
| 📁 Corpus | `policy` | Policy documents |
| 📚 Vector | `Slavdict-policy` | Custom slavery dictionary |
| 🤖 BERTJE | `ft-slavery` | Finetuned on slavery texts |
| 🎯 Target | `slavery-policy` | Finding slavery in policy |

**Filters:**
- Years: 2021, 2022, 2023
- Doc types: 8 selected types

---

## 🔧 To Change Configuration

Edit Cell 2 workflow section:

```python
"workflow": {
    "corpus": "policy",              # What corpus?
    "vector_source": "policy-dict-v1", # Which dictionary?
    "bertje_training": "ft-policy",   # BERTJE training?
    "target": "slavery-policy",       # What to find?
    "version": None,                  # Auto-increment
}
```

Workflow name updates automatically!

---

## 📚 Documentation

- **[NOTEBOOK_FIX_COMPLETE.md](NOTEBOOK_FIX_COMPLETE.md)** - Complete fix details
- **[IMPROVED_WORKFLOW_NAMING_SYSTEM.md](IMPROVED_WORKFLOW_NAMING_SYSTEM.md)** - Full naming docs
- **[FIX_SUMMARY.md](FIX_SUMMARY.md)** - What was broken and how it was fixed

---

## ⚠️ Troubleshooting

### KeyError still appears?
1. Reload notebook
2. Run Cell 2 first
3. Check output shows workflow name

### Folder creation fails?
Make sure `workflow_data/` directory exists

### workflow_naming_helper not found?
That's OK! Fallback code handles it automatically

---

## 🎯 Quick Test

Run in a cell:
```python
print(CONFIG['workflow']['workflow_name'])
# Should print: policy_Slavdict-policy_ft-slavery_slavery-policy_v1

print(CONFIG['workflow']['corpus'])
# Should print: policy
```

No errors = you're good to go! ✓
