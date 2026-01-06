# Cell 17 TypeError Fix - Complete

## Problem
Cell 17 in [dictionary_discovery_v12.ipynb](dictionary_discovery_v12.ipynb#L17) was throwing a `TypeError`:

```
TypeError: argument should be a str or an os.PathLike object where __fspath__ returns a str, not 'NoneType'
```

## Root Cause
The code checked if the key `'workflow_dir'` exists in `CONFIG['workflow']`, but didn't verify the value was not `None`:

```python
# OLD CODE (line 10)
if 'workflow_dir' in CONFIG['workflow']:
    workflow_dir = Path(CONFIG['workflow']['workflow_dir'])  # ❌ Fails if value is None
```

When `CONFIG['workflow']['workflow_dir']` was `None`, passing it to `Path()` caused the TypeError.

## Solution Applied
Added an additional check to ensure the value is not `None`:

```python
# NEW CODE (line 10)
if 'workflow_dir' in CONFIG['workflow'] and CONFIG['workflow']['workflow_dir'] is not None:
    workflow_dir = Path(CONFIG['workflow']['workflow_dir'])  # ✓ Safe
else:
    # Fallback to constructing from workflow_name
    workflow_base = Path(CONFIG["paths"]["workflow_base"])
    workflow_name = CONFIG['workflow']['workflow_name']
    workflow_dir = workflow_base / workflow_name
```

## Why This Happened
The `workflow_dir` key is only populated when `WorkflowFileSystem.create_workflow_folder()` is called (see Cell 6, line 85). If you:
- Run cells out of order
- Skip the workflow creation step
- Load an incomplete CONFIG

Then `workflow_dir` will be `None`, triggering this error.

## Verification
✓ Fix confirmed in Cell 17 line 10
✓ The None check is now present
✓ Fallback logic will activate when workflow_dir is None

## Related Cells
The same pattern appears in other cells (21, 27, 31, 36), but those cells may have their own initialization logic. If you encounter similar errors in those cells, the same fix can be applied.
