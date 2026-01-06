# Text Field Usage Analysis - Notebook v24

## Intended Text Processing Pipeline

```
raw_text → text_for_processing → text_for_scoring
```

- **raw_text**: Original chunk text (untouched, for display/reference)
- **text_for_processing**: English-filtered version (if enabled) or copy of raw_text
- **text_for_scoring**: Cleaned, validated, final version for all operations

---

## Cell-by-Cell Analysis

### **Cell 14** - Document Preparation
```python
'clean_text': doc['text']
```
**Status**: ✓ OK - Generic 'text' field from input documents

---

### **Cell 15** - Chunking (Creates text fields)
```python
raw_text = ' '.join(chunk_sentences)
text_for_processing = raw_text  # OR english-filtered version
'raw_text': raw_text,
'text_for_processing': text_for_processing,
```
**Status**: ✓ OK - Creates both fields correctly

---

### **Cell 16** - Text Processing (Creates text_for_scoring)
```python
# Input: text_for_processing
text = row['text_for_processing']
# Output: text_for_scoring
chunks_df['text_for_scoring'] = text_for_scoring
```
**Status**: ✓ OK - Correctly transforms text_for_processing → text_for_scoring

---

### **Cell 22** - Vocabulary Building
```python
text = row['text_for_scoring']
```
**Status**: ✓ OK - Uses text_for_scoring (correct)

---

### **Cell 36** - Topic Scoring
```python
text = chunk['text_for_scoring']  # Used for scoring
'raw_text': chunk['raw_text'],    # Included in output for reference
```
**Status**: ✓ OK - Uses text_for_scoring for operations, raw_text for display

---

### **Cell 37** - Display/Logging
```python
print(f"  Text: {row['raw_text'][:150]}...")
```
**Status**: ✓ OK - Uses raw_text for display (appropriate)

---

### **Cell 41** - BERTJE Training Data Preparation (All labeled data)
```python
Scores_all_labeled['text'] = Scores_all_labeled['raw_text']
```
**Status**: ⚠️ **ISSUE** - Should use `text_for_scoring` instead of `raw_text`
**Reason**: BERTJE should train on the SAME cleaned text used for scoring/vocabulary

---

### **Cell 44** - BERTJE Training Data (High confidence labeled)
```python
df_labeled['text'] = df_labeled['raw_text']
```
**Status**: ⚠️ **ISSUE** - Should use `text_for_scoring` instead of `raw_text`
**Reason**: Same as Cell 41

---

### **Cell 45** - BERTJE Training Data (Pseudo-labels + Unlabeled)
```python
df_pseudo["text"] = df_pseudo["raw_text"]
df_unlabeled["text"] = df_unlabeled["raw_text"]
```
**Status**: ⚠️ **ISSUE** - Should use `text_for_scoring` instead of `raw_text`
**Reason**: Same as Cell 41 and 44

---

### **Cell 52** - Training (uses 'text' column)
```python
texts = train_data["text"].tolist()
```
**Status**: ⚠️ **INDIRECT ISSUE** - Uses 'text' column created in Cells 41-45
**Impact**: If Cells 41-45 use wrong field, this inherits the issue

---

### **Cell 70** - Prediction
```python
if 'text_for_scoring' in corpus_df.columns:
    texts = corpus_df['text_for_scoring'].fillna('').tolist()
elif 'raw_text' in corpus_df.columns:
    texts = corpus_df['raw_text'].fillna('').tolist()
```
**Status**: ⚠️ **PARTIAL ISSUE** - Has fallback to raw_text
**Reason**: Should ALWAYS prefer text_for_scoring. Fallback masks data issues.

---

### **Cell 76** - Visualization Data Validation
```python
required_cols = ['chunk_id', 'raw_text']
optional_cols = ['filename', 'text_for_scoring']
print(f"    - raw_text: {'✓' if 'raw_text' in df_viz.columns else '✗'}")
```
**Status**: ✓ OK - Validation/display code, uses raw_text appropriately for reference

---

### **Cell 77** - Topic Snippets for Display
```python
if 'raw_text' in topic_df.columns:
    topic_df['snippet'] = topic_df['raw_text'].apply(...)
```
**Status**: ✓ OK - Creates display snippets from raw_text (appropriate for visualization)

---

## Summary of Issues

### Critical Issues (Cells 41, 44, 45)

**Problem**: BERTJE training uses `raw_text` instead of `text_for_scoring`

**Impact**:
1. **Inconsistency**: Model trains on raw text but predicts on cleaned text
2. **Quality degradation**: Includes text that failed validation (too short, etc.)
3. **Vocabulary mismatch**: Training vocabulary ≠ scoring vocabulary
4. **English contamination**: If `scoring_drop_english=True`, raw_text includes English but scoring doesn't

**Example scenario**:
- Chunk has `raw_text = "Dit is een test with English words"`
- After processing: `text_for_scoring = "Dit is een test"` (English removed)
- Vocabulary built from: `text_for_scoring` (no English)
- BERTJE trains on: `raw_text` (includes English) ❌
- BERTJE predicts on: `text_for_scoring` (no English) ✓
- Result: **Train/test distribution mismatch**

### Minor Issue (Cell 70)

**Problem**: Fallback to `raw_text` if `text_for_scoring` missing

**Impact**: Masks data pipeline issues instead of failing loudly

---

## Recommended Fixes

### Fix 1: Cell 41 (All labeled data)
```python
# OLD
Scores_all_labeled['text'] = Scores_all_labeled['raw_text']

# NEW
Scores_all_labeled['text'] = Scores_all_labeled['text_for_scoring']
```

### Fix 2: Cell 44 (High confidence labeled)
```python
# OLD
df_labeled['text'] = df_labeled['raw_text']

# NEW
df_labeled['text'] = df_labeled['text_for_scoring']
```

### Fix 3: Cell 45 (Pseudo-labels + Unlabeled)
```python
# OLD
df_pseudo["text"] = df_pseudo["raw_text"]
df_unlabeled["text"] = df_unlabeled["raw_text"]

# NEW
df_pseudo["text"] = df_pseudo["text_for_scoring"]
df_unlabeled["text"] = df_unlabeled["text_for_scoring"]
```

### Fix 4: Cell 70 (Remove fallback or add warning)
```python
# OPTION A: Fail if text_for_scoring missing (strict)
if 'text_for_scoring' not in corpus_df.columns:
    raise ValueError("text_for_scoring column missing - check text processing pipeline")
texts = corpus_df['text_for_scoring'].fillna('').tolist()

# OPTION B: Keep fallback but warn (lenient)
if 'text_for_scoring' in corpus_df.columns:
    texts = corpus_df['text_for_scoring'].fillna('').tolist()
elif 'raw_text' in corpus_df.columns:
    print("WARNING: text_for_scoring missing, falling back to raw_text")
    texts = corpus_df['raw_text'].fillna('').tolist()
else:
    raise ValueError("Neither text_for_scoring nor raw_text found")
```

---

## Validation Checklist

After applying fixes, verify:

- [ ] Cell 22 (vocabulary): Uses `text_for_scoring` ✓ (already correct)
- [ ] Cell 36 (scoring): Uses `text_for_scoring` ✓ (already correct)
- [ ] Cell 41 (all labeled): Uses `text_for_scoring` (needs fix)
- [ ] Cell 44 (high conf labeled): Uses `text_for_scoring` (needs fix)
- [ ] Cell 45 (pseudo/unlabeled): Uses `text_for_scoring` (needs fix)
- [ ] Cell 52 (training): Inherits from Cells 41-45 (fixed indirectly)
- [ ] Cell 70 (prediction): Uses `text_for_scoring` (needs warning/fix)

---

## Impact Assessment

**Before fixes**:
- Vocabulary: text_for_scoring ✓
- Scoring: text_for_scoring ✓
- Training: raw_text ❌
- Prediction: text_for_scoring (with fallback) ⚠️

**After fixes**:
- Vocabulary: text_for_scoring ✓
- Scoring: text_for_scoring ✓
- Training: text_for_scoring ✓
- Prediction: text_for_scoring ✓

**Result**: Full pipeline consistency - all operations use the same cleaned text

---

## Additional Notes

### Why this matters for your research:

1. **Stage 1 (Slavery corpus)**: May have minimal English, but consistency still important
2. **Stage 2 (Policy corpus)**: Likely has more English text, makes the fix critical
3. **Model reproducibility**: Ensures same preprocessing for all steps
4. **Dictionary quality**: BERTJE expansions based on same text as scoring

### Testing after fixes:

1. Re-run Cells 41-45 to regenerate training data
2. Check if `df_labeled['text']` now matches expected cleaned format
3. Re-train BERTJE model (Cells 46-60)
4. Compare prediction quality before/after fix
5. Verify no vocabulary mismatches in logs

---

**Analysis complete - Ready for implementation**
