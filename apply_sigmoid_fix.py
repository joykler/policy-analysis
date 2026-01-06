"""
Apply Option B changes to remove sigmoid for [0, 2] range output.
"""
import json
from pathlib import Path

notebook_path = Path(r'C:\Users\Home\policy-analysis\A__dictionary_discovery_v18_rescaled_scores.ipynb')

print("="*80)
print("APPLYING OPTION B: Remove Sigmoid for [0, 2] Range")
print("="*80)

# Load notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"\nLoaded notebook: {notebook_path}")
print(f"Total cells: {len(nb['cells'])}")

changes_made = []

# Find and modify Cell 48 (CELL 7.1)
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue

    source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']

    # Look for the SBERTContinuousMultiLabel class definition
    if 'class SBERTContinuousMultiLabel' in source and 'CELL 7.1' in source:
        print(f"\nFound Cell {i}: SBERTContinuousMultiLabel")

        # CHANGE 1: Remove sigmoid
        if 'torch.sigmoid(head(sentence_embedding))' in source:
            original = 'pred = torch.sigmoid(head(sentence_embedding))  # [batch, 1] -> [0, 1]'
            replacement = 'pred = head(sentence_embedding)  # [batch, 1] -> unbounded, learns [0, 2]'
            source = source.replace(original, replacement)
            changes_made.append(f"Cell {i}: Removed sigmoid activation")
            print(f"  - Removed sigmoid activation")

        # CHANGE 2: Add clamping in loss
        if 'loss = loss_fct(logits, labels.float())' in source:
            original = '        loss = None\n        if labels is not None:\n            loss_fct = nn.MSELoss()\n            loss = loss_fct(logits, labels.float())'
            replacement = '        loss = None\n        if labels is not None:\n            loss_fct = nn.MSELoss()\n            # Clamp predictions to [0, 2] for training stability\n            logits_clamped = torch.clamp(logits, 0.0, 2.0)\n            loss = loss_fct(logits_clamped, labels.float())'
            source = source.replace(original, replacement)
            changes_made.append(f"Cell {i}: Added clamping to loss computation")
            print(f"  - Added clamping to loss computation")

        # CHANGE 3: Update print statement
        if 'Continuous output [0, 1] per topic' in source:
            original = 'print("  - Continuous output [0, 1] per topic")'
            replacement = 'print("  - Continuous output [0, 2] per topic (no sigmoid)")'
            source = source.replace(original, replacement)

            # Also update version number
            source = source.replace('print("V13: SBERTContinuousMultiLabel Defined")',
                                   'print("V18: SBERTContinuousMultiLabel Defined (no sigmoid)")')

            # Update loss description
            source = source.replace('print("  - Loss: MSE on cosine scores")',
                                   'print("  - Loss: MSE on rescaled cosine scores [0, 2]")')

            changes_made.append(f"Cell {i}: Updated documentation")
            print(f"  - Updated documentation")

        # Convert back to list format if needed
        if isinstance(cell['source'], list):
            cell['source'] = source.split('\n')
            # Ensure each line ends with \n except the last
            cell['source'] = [line + '\n' if idx < len(cell['source']) - 1 else line
                            for idx, line in enumerate(cell['source'])]
        else:
            cell['source'] = source

# Create backup
backup_path = notebook_path.with_name(notebook_path.stem + '_backup.ipynb')
print(f"\nCreating backup: {backup_path}")
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

# Save modified notebook
print(f"\nSaving modified notebook: {notebook_path}")
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("\n" + "="*80)
print("CHANGES APPLIED SUCCESSFULLY")
print("="*80)

if changes_made:
    print("\nSummary of changes:")
    for change in changes_made:
        print(f"  - {change}")
else:
    print("\nWarning: No changes were applied. Cell structure may have changed.")
    print("  Please verify manually.")

print("\n" + "="*80)
print("NEXT STEPS")
print("="*80)
print("""
1. Open the notebook in Jupyter/VSCode
2. Restart kernel (to clear old model definition)
3. Run from Cell 7.1 onwards to retrain with new architecture
4. Monitor training:
   - Loss should decrease more smoothly
   - Predictions will be in [0, 2] range
5. Validate that predictions use appropriate range per topic

Note: A backup was created in case you need to revert.
""")

print("\n" + "="*80)
