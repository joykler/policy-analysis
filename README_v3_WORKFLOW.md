# Dictionary Discovery Workflow v3 - Quick Start

## What's New in v3

✨ **Systematic File Organization**
- Clear folder structure with descriptive names
- All outputs organized by type (Dictionary, Model, Scoring, Visuals)
- Complete reproducibility with input files copied to workflow folder

✨ **Checkpoint System**
- 9 clear checkpoints with resume capability
- Save/load at any point in the workflow
- Config snapshots at each checkpoint

✨ **Better Folder Naming**
- `{ModelType}-{Topic}_{Date}_{Version}`
- Examples:
  - `Pretrained-Slavery_10.24.25_v1`
  - `Finetuned_Slavery-Policy_10.24.25_v2`

## Files in This Update

1. **WORKFLOW_GUIDE_v3.md** 📖
   - Complete documentation of the new workflow
   - Folder structure explained
   - All 9 checkpoints detailed
   - Best practices and troubleshooting

2. **Dictionary_discovery_v3_structured.ipynb** 📓
   - Starter notebook with CHECKPOINTS 0-1 implemented
   - Shows the new file system API in action
   - Template for implementing remaining checkpoints

3. **Dictionary_discovery_v3_TEMPLATE.ipynb** 📓 (generated)
   - Complete template with all checkpoint placeholders
   - Run `python generate_complete_workflow_notebook.py` to create it

## Quick Start

### Step 1: Read the Guide
```bash
# Open in your favorite markdown viewer
open WORKFLOW_GUIDE_v3.md
```

### Step 2: Start with Existing Notebook
The structured notebook (`Dictionary_discovery_v3_structured.ipynb`) has:
- ✅ CHECKPOINT 0: Setup system (COMPLETE)
- ✅ CHECKPOINT 1: Text processing (COMPLETE)
- ⚠️ CHECKPOINT 2-8: Implement by adapting from `Dictionary_discoveryv2.ipynb`

### Step 3: Follow the Pattern

The new pattern is:
```python
# Old way (v2)
df.to_csv("/some/hardcoded/path/file.csv", index=False)

# New way (v3)
fs.save_data(df, "file_name", "folder_key", "csv")
```

Example from CHECKPOINT 1:
```python
# Process data
chunks_df = pd.DataFrame(all_chunks)

# Save with the new system
fs.save_data(chunks_df, "chunked_corpus", "Other_data", "csv")

# Save checkpoint config
fs.save_config("checkpoint1_chunks")
```

## Migration Path

### If you have existing workflows in Model_iterations/:
1. Keep using `Dictionary_discoveryv2.ipynb` for those
2. Start new workflows with v3 structure
3. Optionally: copy key files to new structure and continue there

### To adapt v2 code to v3:
1. Find all `pd.to_csv()`, `np.save()`, `json.dump()` calls
2. Replace with `fs.save_data()`
3. Add `fs.save_config("checkpoint_name")` after each major step
4. Use `fs.folders["folder_key"]` instead of hardcoded paths

## Folder Structure at a Glance

```
workflow_data/
  Pretrained-Slavery_10.24.25_v1/      # Example folder name
    ├── config/                         # All config snapshots
    ├── Dictionary/                     # Input + expanded + curated dictionaries
    │   └── Dictionary_suggestions/     # Per-topic suggestion CSVs
    ├── Model_finetuning/              # Trained model + metrics
    ├── Cosine_labeling/               # Confidence-classified scores
    ├── Bertje_labeling/               # Predictions on new data
    ├── Visuals/                       # All visualizations
    └── Other_data/                    # Chunks, vocabulary, vectors
```

## Key Benefits

✅ **Everything in one place**: No more hunting for files across directories
✅ **Reproducible**: All inputs saved with outputs
✅ **Traceable**: Config history at every step
✅ **Resumable**: Start anywhere, anytime
✅ **Clear**: Descriptive folder and file names
✅ **Maintainable**: Systematic file management API

## Next Steps

1. ✅ Read `WORKFLOW_GUIDE_v3.md` (comprehensive documentation)
2. ✅ Open `Dictionary_discovery_v3_structured.ipynb` (starter notebook)
3. ✅ Review CHECKPOINT 0 and 1 implementation patterns
4. ⚠️ Adapt remaining checkpoints from `Dictionary_discoveryv2.ipynb`
5. ⚠️ Run your first complete workflow!

## Questions Answered

**Q: Do I need to migrate existing workflows?**
A: No, keep using v2 for existing work. Use v3 for new workflows.

**Q: Can I use my trained models from v2 in v3?**
A: Yes! Set `CONFIG["paths"]["pretrained_model_path"]` to your v2 model folder.

**Q: What if I already have preprocessed data?**
A: Skip to the relevant checkpoint and load your data.

**Q: How do I resume a workflow?**
A: Load the workflow folder with `fs.load_existing_workflow()` and skip completed checkpoints.

**Q: Can I customize the folder structure?**
A: The WorkflowFileSystem class can be extended. The current structure follows best practices for ML project organization.

## Support

- 📖 Full docs: `WORKFLOW_GUIDE_v3.md`
- 📓 Examples: `Dictionary_discovery_v3_structured.ipynb` (CHECKPOINTS 0-1)
- 📝 Reference: `Dictionary_discoveryv2.ipynb` (original implementation)

Happy workflow building! 🚀
