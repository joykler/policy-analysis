"""
Apply per-topic normalization to Cell 7.2.
This fixes the score range variation issue by normalizing each topic independently.
"""

import json
from pathlib import Path

print("="*80)
print("APPLYING PER-TOPIC NORMALIZATION TO CELL 7.2")
print("="*80)

# Load notebook
notebook_path = Path("A__dictionary_discovery_v20_unified_embedding.ipynb")
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

print(f"\nLoaded notebook: {notebook_path.name}")

# Find Cell 7.2
cell_72_idx = None
for i, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'CELL 7.2' in source and 'ContinuousMultiLabelDataset' in source:
            cell_72_idx = i
            print(f"Found Cell 7.2 at index {i}")
            break

if cell_72_idx is None:
    raise ValueError("Could not find Cell 7.2 with ContinuousMultiLabelDataset!")

# Get current source
cell_source = ''.join(notebook['cells'][cell_72_idx]['source'])

print(f"\nCurrent cell length: {len(cell_source)} characters")

# ============================================================
# REPLACE THE ENTIRE ContinuousMultiLabelDataset CLASS
# ============================================================

print("\n" + "="*80)
print("REPLACING ContinuousMultiLabelDataset CLASS")
print("="*80)

# Find the class definition
class_start = cell_source.find('class ContinuousMultiLabelDataset(Dataset):')
if class_start == -1:
    raise ValueError("Could not find ContinuousMultiLabelDataset class!")

# Find the end of the class (next cell marker or end of source)
# Look for next top-level code that's not indented
next_cell_marker = cell_source.find('\n# ===', class_start + 100)
if next_cell_marker == -1:
    # Class goes to end of cell
    class_end = len(cell_source)
else:
    class_end = next_cell_marker

print(f"  Class starts at position {class_start}")
print(f"  Class ends at position {class_end}")

# Extract before and after
before_class = cell_source[:class_start]
after_class = cell_source[class_end:]

# New class implementation with per-topic normalization
new_class = '''class ContinuousMultiLabelDataset(Dataset):
    """
    Dataset for continuous multi-label regression.

    Uses per-topic normalization to handle different score distributions:
    - Each topic has its own min/max range
    - Normalizes to [0, 1] independently per topic
    - Preserves topic-specific score characteristics

    Example:
        Educational: raw scores 0.9-15.2 -> normalized 0.0-1.0
        Governance: raw scores 0.7-8.1 -> normalized 0.0-1.0
    """

    def __init__(self, dataframe, tokenizer, topics, config):
        self.dataframe = dataframe.reset_index(drop=True)
        self.tokenizer = tokenizer
        self.topics = topics
        self.config = config

        self.texts = dataframe["raw_text"].tolist()

        # ============================================================
        # CALCULATE PER-TOPIC NORMALIZATION STATISTICS
        # ============================================================

        print(f"\\n{'='*60}")
        print("CALCULATING PER-TOPIC NORMALIZATION PARAMETERS")
        print(f"{'='*60}")

        self.topic_stats = {}
        for topic in topics:
            score_col = f"score_{topic}"

            if score_col not in dataframe.columns:
                print(f"[WARNING] Column {score_col} not found, skipping topic: {topic}")
                continue

            topic_scores = dataframe[score_col].values

            # Calculate statistics
            min_score = float(topic_scores.min())
            max_score = float(topic_scores.max())
            score_range = max_score - min_score
            mean_score = float(topic_scores.mean())
            std_score = float(topic_scores.std())

            self.topic_stats[topic] = {
                'min': min_score,
                'max': max_score,
                'range': score_range,
                'mean': mean_score,
                'std': std_score
            }

            print(f"\\n{topic}:")
            print(f"  Raw range: [{min_score:.3f}, {max_score:.3f}]")
            print(f"  Range span: {score_range:.3f}")
            print(f"  Mean: {mean_score:.3f}, Std: {std_score:.3f}")

        print(f"\\n{'='*60}")
        print("NORMALIZING SCORES TO [0, 1] PER TOPIC")
        print(f"{'='*60}")

        # ============================================================
        # EXTRACT AND NORMALIZE LABELS
        # ============================================================

        self.labels = []
        for _, row in dataframe.iterrows():
            label_vec = []

            for topic in topics:
                score_col = f"score_{topic}"

                # Get raw score
                score_val = row.get(score_col, None)

                # Handle missing/NaN scores
                if pd.isna(score_val) or score_val is None:
                    # Default to topic minimum (represents weakest signal)
                    score_val = self.topic_stats[topic]['min']

                score_val = float(score_val)

                # Normalize using per-topic statistics
                stats = self.topic_stats[topic]

                if stats['range'] > 0:
                    # Min-max normalization to [0, 1]
                    score_normalized = (score_val - stats['min']) / stats['range']
                else:
                    # All scores are identical for this topic
                    score_normalized = 0.5  # Neutral value

                # Clip to [0, 1] (handles edge cases like new data outside training range)
                score_normalized = float(np.clip(score_normalized, 0.0, 1.0))

                label_vec.append(score_normalized)

            self.labels.append(label_vec)

        print(f"\\nCreated {len(self.labels)} training examples")
        print(f"Label shape: ({len(self.labels)}, {len(self.labels[0])})")

        # Show example normalized scores
        print(f"\\nExample normalized labels (first 3 samples):")
        for i in range(min(3, len(self.labels))):
            print(f"  Sample {i}: {[f'{x:.3f}' for x in self.labels[i]]}")

    def get_normalization_params(self):
        """
        Return normalization parameters for saving/inference.

        Use this to save normalization stats for later denormalization:
            params = dataset.get_normalization_params()
            with open('topic_normalization_params.json', 'w') as f:
                json.dump(params, f)
        """
        return self.topic_stats

    def denormalize_predictions(self, normalized_scores, topic_idx=None):
        """
        Convert normalized [0, 1] predictions back to raw score range.

        Args:
            normalized_scores: Array of normalized predictions [0, 1]
            topic_idx: If provided, denormalize for specific topic index.
                      Otherwise assumes scores are in topic order.

        Returns:
            Array of denormalized scores in original raw range
        """
        if topic_idx is not None:
            topic = self.topics[topic_idx]
            stats = self.topic_stats[topic]
            return normalized_scores * stats['range'] + stats['min']
        else:
            # Denormalize all topics
            denormalized = []
            for i, topic in enumerate(self.topics):
                stats = self.topic_stats[topic]
                raw_score = normalized_scores[i] * stats['range'] + stats['min']
                denormalized.append(raw_score)
            return denormalized

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx],
            truncation=True,
            max_length=self.config["model"]["max_length"],
            padding=False,
            return_tensors=None
        )

        encoding["labels"] = self.labels[idx]

        return encoding

'''

# Reconstruct cell
new_cell_source = before_class + new_class + after_class

# ============================================================
# CONVERT TO JUPYTER FORMAT
# ============================================================

print("\n" + "="*80)
print("CONVERTING TO JUPYTER FORMAT")
print("="*80)

lines = new_cell_source.split('\n')
source_array = [line + '\n' for line in lines[:-1]]
if lines[-1]:
    source_array.append(lines[-1])

print(f"  Converted to {len(source_array)} lines")

# Update notebook
notebook['cells'][cell_72_idx]['source'] = source_array

# ============================================================
# SAVE
# ============================================================

print("\n" + "="*80)
print("SAVING NOTEBOOK")
print("="*80)

# Create backup
backup_path = notebook_path.with_suffix('.ipynb.backup_cell72')
import shutil
shutil.copy(notebook_path, backup_path)
print(f"  [OK] Created backup: {backup_path.name}")

# Save
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f"  [OK] Saved updated notebook")

# ============================================================
# VERIFICATION
# ============================================================

print("\n" + "="*80)
print("VERIFICATION")
print("="*80)

# Reload and check
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb_check = json.load(f)

cell_check = ''.join(nb_check['cells'][cell_72_idx]['source'])

checks = {
    'Per-topic statistics': 'self.topic_stats' in cell_check,
    'Per-topic normalization': 'stats[\'range\']' in cell_check,
    'Min-max normalization': '(score_val - stats[\'min\']) / stats[\'range\']' in cell_check,
    'Denormalize method': 'def denormalize_predictions' in cell_check,
    'Get params method': 'def get_normalization_params' in cell_check,
    'Handles NaN scores': 'pd.isna(score_val)' in cell_check,
    'Clips to [0,1]': 'np.clip(score_normalized, 0.0, 1.0)' in cell_check,
    'Removed hardcoded 10.0 clip': 'np.clip(score_val, 0.0, 10.0)' not in cell_check
}

print("\n  Feature verification:")
for feature, present in checks.items():
    status = "[OK]" if present else "[MISSING]"
    print(f"    {status} {feature}")

all_good = all(checks.values())

print("\n" + "="*80)
if all_good:
    print("[SUCCESS] PER-TOPIC NORMALIZATION APPLIED")
else:
    print("[WARNING] Some features missing")
print("="*80)

print(f"""
SUMMARY:

Applied per-topic normalization to Cell 7.2:

KEY CHANGES:

1. Calculate normalization statistics per topic:
   - Each topic gets its own min/max/range
   - Handles different score distributions properly

2. Normalize each topic independently:
   - normalized = (raw_score - topic_min) / topic_range
   - Each topic uses full [0, 1] dynamic range

3. Added utility methods:
   - get_normalization_params(): Save stats for inference
   - denormalize_predictions(): Convert [0,1] back to raw scores

4. Removed hardcoded clipping:
   - OLD: np.clip(score_val, 0.0, 10.0)  # Truncated high scores
   - NEW: Per-topic normalization + clip to [0,1]

BENEFITS:

- Handles different topic score distributions fairly
- Educational (0.9-15.2) and Governance (0.7-8.1) both use full [0,1] range
- No information loss from arbitrary clipping
- Model learns balanced representations across topics
- Preserves dot product magnitude information from Cell 5.1

NEXT STEPS:

1. Re-run Cell 7.2 to create dataset with normalized labels
2. Verify normalization parameters look reasonable
3. Save normalization params for inference:

   params = train_dataset.get_normalization_params()
   with open('topic_normalization_params.json', 'w') as f:
       json.dump(params, f)

4. Train model with normalized [0,1] targets
5. At inference, denormalize predictions if you want raw scores:

   raw_scores = train_dataset.denormalize_predictions(predictions)

""")