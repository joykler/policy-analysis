# CP1 Column Structure Fix

## Issue Identified

The chunking cells (15) were creating a `text_for_processing` column that contained partially filtered text (English sentences removed). This was incorrect because:

1. **Cell 1.3 (CP1 chunking)** should ONLY create `raw_text` (unfiltered chunks)
2. **Cell 1.4** should then process `raw_text` → `text_for_scoring` (with all cleaning applied)
3. Having `text_for_processing` as an intermediate column was confusing and redundant

## Problem

### Before (Incorrect)
```
CP1.3 Chunking:
  - Creates: raw_text (full text)
  - Creates: text_for_processing (English sentences removed)  ← Wrong!

CP1.4 Processing:
  - Reads: text_for_processing
  - Creates: text_for_scoring (stopwords removed, cleaned)
```

**Issues**:
- Two intermediate columns (`text_for_processing` and `text_for_scoring`)
- English filtering happened twice (once in chunking, once in scoring prep)
- Confusion about which column to use downstream
- `text_for_processing` column in saved CSVs serves no purpose

### After (Correct)
```
CP1.3 Chunking:
  - Creates: raw_text (full text, unfiltered)  ← Only this!

CP1.4 Processing:
  - Reads: raw_text
  - Creates: text_for_scoring (all cleaning: English removal, stopwords, etc.)
```

**Benefits**:
- Clear separation: chunking creates raw data, processing cleans it
- `raw_text` preserved for reference/debugging
- Only one cleaned column (`text_for_scoring`) for scoring
- Matches standard pipeline architecture

## Changes Applied

### Cell 15 (CP1.3 Chunking)

**Removed from both `chunk_documents` and `chunk_documents_token_aware`**:

```python
# OLD: Created text_for_processing
if config.scoring_drop_english:
    retained = [s for s in chunk_sentences if not likely_english_sentence(s)]
    if not retained:
        stats['chunks_filtered']['all_english'] += 1
        continue
    text_for_processing = ' '.join(retained)
else:
    text_for_processing = raw_text

chunk_records.append({
    'raw_text': raw_text,
    'text_for_processing': text_for_processing,  # ← Removed this
    ...
})
```

**New behavior**:
```python
# NEW: Only create raw_text
raw_text = ' '.join(chunk_sentences)

chunk_records.append({
    'raw_text': raw_text,  # Only this column
    # No text_for_processing
    ...
})
```

**Also added verification**:
```python
print(f"\nColumn check:")
print(f"  ✓ raw_text: {'present' if 'raw_text' in cp1_chunked_df_raw.columns else 'MISSING'}")
print(f"  ✗ text_for_processing: {'SHOULD NOT EXIST' if 'text_for_processing' in cp1_chunked_df_raw.columns else 'correctly absent'}")
print(f"  Note: text_for_scoring will be created in Cell 1.4")
```

### Cell 16 (CP1.4 Text Processing)

**Changed to process `raw_text` instead of `text_for_processing`**:

```python
# OLD: Processed text_for_processing
def apply_text_processing(chunks_df: pd.DataFrame, config: ProcessingConfig):
    for _, row in chunks_df.iterrows():
        text = row['text_for_processing']  # ← Wrong column
        ...

# NEW: Process raw_text
def apply_text_processing(chunks_df: pd.DataFrame, config: ProcessingConfig):
    # Verify raw_text exists
    if 'raw_text' not in chunks_df.columns:
        raise ValueError("raw_text column not found! Check Cell 1.3 output.")

    # Warn if text_for_processing exists (shouldn't be there)
    if 'text_for_processing' in chunks_df.columns:
        print("⚠️  WARNING: text_for_processing column found but will be ignored.")
        print("   Cell 1.3 should only create raw_text. This may be from an old run.")

    for _, row in chunks_df.iterrows():
        text = row['raw_text']  # ← Correct column
        ...
```

**Enhanced cleaning logic**:
```python
def clean_text_for_scoring(text: str, ...):
    # OPTIONAL: Remove English sentences first (if configured)
    if drop_english:
        sentences = re.split(r'(?<=[.!?])\s+', text)
        retained = [s for s in sentences if not likely_english_sentence(s)]
        if not retained:
            return ""  # All English - will be filtered
        text = ' '.join(retained)

    # Then apply token-level cleaning (stopwords, numbers, etc.)
    ...
```

**Also added statistics**:
```python
stats = {
    'filtered_all_english': filtered_all_english,  # New
    'filtered_for_tokens': filtered_for_tokens,
    'result_chunks': len(processed_df)
}
```

**And verification**:
```python
print(f"\nFinal column check:")
print(f"  ✓ raw_text: {'present' if 'raw_text' in cp1_chunked_df.columns else 'MISSING'}")
print(f"  ✓ text_for_scoring: {'present' if 'text_for_scoring' in cp1_chunked_df.columns else 'MISSING'}")
print(f"  ✗ text_for_processing: {'SHOULD NOT EXIST' if 'text_for_processing' in cp1_chunked_df.columns else 'correctly absent'}")
```

## Expected Output After Fix

### Cell 15 (CP1.3) Output:
```
================================================================================
STAGE 1.3: CHUNK CLEAN TEXT
================================================================================
✓ Using token-aware chunking (max 500 tokens)
  Tokenizer source: model.base_model_name = NetherlandsForensicInstitute/robbert-2022-dutch-sentence-transformers
  ✓ Loaded tokenizer: NetherlandsForensicInstitute/robbert-2022-dutch-sentence-transformers
  Token stats: avg=387.2, max=499, over_limit=0
  ✓ token_count metadata preserved (8234 rows)
✓ Created 8234 raw chunks -> workflow_data/.../Other_data/cp1_stage2_chunks_raw.csv

Column check:
  ✓ raw_text: present
  ✗ text_for_processing: correctly absent
  Note: text_for_scoring will be created in Cell 1.4

✓ Stage 1.3 complete
```

### Cell 16 (CP1.4) Output:
```
================================================================================
STAGE 1.4: BUILD text_for_scoring FROM raw_text
================================================================================
✓ Processed 7523 chunks ready after scoring prep
  Filtered (all English): 345
  Filtered (min tokens): 366

Sample cleaned text:
  Raw text: Het slavernijverleden heeft diepe sporen nagelaten in de Nederlandse samenleving. The legacy...
  Cleaned:  slavernijverleden diepe sporen nagelaten nederlandse samenleving legacy...

Final column check:
  ✓ raw_text: present
  ✓ text_for_scoring: present
  ✗ text_for_processing: correctly absent

✓ Stage 1.4 complete
```

## CSV Output Structure

### Before (Incorrect)
```
chunked_corpus.csv columns:
- file_path
- chunk_uid
- raw_text
- text_for_processing  ← Shouldn't be here
- text_for_scoring
- sentence_count
- token_count
- ...
```

### After (Correct)
```
chunked_corpus.csv columns:
- file_path
- chunk_uid
- raw_text              ← Unfiltered reference text
- text_for_scoring      ← Cleaned text for embeddings
- sentence_count
- token_count
- ...
```

## Downstream Impact

**No changes needed** in downstream cells because:
- CP2-CP3 (vocab building) use `text_for_scoring` ✓
- CP5 (scoring) uses `text_for_scoring` ✓
- CP6+ don't directly reference text columns ✓

The fix only affects CP1 internal logic, not the final output column set used by later checkpoints.

## Migration for Existing Workflows

If you have existing `chunked_corpus.csv` files with `text_for_processing`:

1. **Option A (Recommended)**: Re-run CP1 with fixed cells
   - Ensures correct column structure
   - Removes redundant column

2. **Option B (Quick Fix)**: Drop the column manually
   ```python
   df = pd.read_csv('chunked_corpus.csv')
   if 'text_for_processing' in df.columns:
       df = df.drop(columns=['text_for_processing'])
       df.to_csv('chunked_corpus.csv', index=False)
   ```

3. **Option C**: Ignore it
   - Cell 16 now warns but ignores `text_for_processing`
   - Still processes `raw_text` correctly
   - Works but leaves junk column in CSV

## Testing

To verify the fix works:

1. Run Cell 15 (CP1.3) and check:
   - Console shows "text_for_processing: correctly absent"
   - `cp1_stage2_chunks_raw.csv` has `raw_text` but NOT `text_for_processing`

2. Run Cell 16 (CP1.4) and check:
   - Console shows "Final column check" with all ✓ marks
   - No warning about text_for_processing (unless loading old data)
   - Sample shows raw → cleaned transformation

3. Run Cell 17 (CP1.5 save) and check:
   - `chunked_corpus.csv` has both `raw_text` and `text_for_scoring`
   - No `text_for_processing` column

---

**Status**: CP1 column structure corrected ✅
**Files Modified**: Cells 15 and 16 in `A__dictionary_discovery_v24_unified_embedding.ipynb`
