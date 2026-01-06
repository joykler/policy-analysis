# Rescaled Scores: Visual Guide

## Score Transformation Visualization

```
ORIGINAL COSINE SCORES [0, 1]
│
├─ Most scores compressed here (80%+)
│  ▼
0.0 ────────── 0.3 ─┬─ 0.5 ─┬─ 0.7 ────────── 1.0
                    │       │
                    │       └─ "High" threshold (0.4)
                    └─ "Medium" threshold (0.3)

Poor distribution: Hard to distinguish quality levels


RESCALED SCORES [0, 2]
│
├─ Scores well-distributed across range
│  ▼
0.0 ── 0.5 ── 1.0 ── 1.5 ── 2.0
│      │      │      │      │
│      │      │      └──────┴─ CORE (1.5-2.0)        15%
│      │      └────────────── MODERATE (1.0-1.5)     20%
│      └───────────────────── WEAK (0.5-1.0)         35%
└──────────────────────────── NOISE+CONTEXT (<0.5)   30%

Good distribution: Clear quality tiers
```

## Confidence Tier Systems

### 5-Tier System (for Analysis)

```
RESCALED SCORE RANGE [0, 2]
│
2.0 ┤ ╔═══════════════════════╗
    │ ║    CORE (1.5-2.0)     ║ ← Top 15%: Gold standard
1.5 ┤ ╠═══════════════════════╣
    │ ║  MODERATE (1.0-1.5)   ║ ← Next 20%: Good quality
1.0 ┤ ╠═══════════════════════╣
    │ ║   WEAK (0.5-1.0)      ║ ← Next 35%: Borderline
0.5 ┤ ╠═══════════════════════╣
    │ ║  CONTEXT (0.25-0.5)   ║ ← Next 20%: Weak signal
0.25┤ ╠═══════════════════════╣
    │ ║   NOISE (0-0.25)      ║ ← Bottom 10%: No signal
0.0 ┤ ╚═══════════════════════╝
```

### 3-Tier System (for Training)

```
RESCALED SCORE RANGE [0, 2]
│
2.0 ┤ ╔═══════════════════════════════╗
    │ ║                               ║
    │ ║    HIGH CONFIDENCE            ║
    │ ║    (rescaled >= 1.0)          ║
    │ ║                               ║
    │ ║    Core + Moderate            ║
    │ ║    ~35% of data               ║
    │ ║                               ║
1.0 ┤ ╠═══════════════════════════════╣
    │ ║                               ║
    │ ║    LOW CONFIDENCE             ║
    │ ║    (0.5 <= rescaled < 1.0)    ║
    │ ║                               ║
    │ ║    Weak                       ║
    │ ║    ~35% of data               ║
    │ ║                               ║
0.5 ┤ ╠═══════════════════════════════╣
    │ ║                               ║
    │ ║    NO CONFIDENCE              ║
    │ ║    (rescaled < 0.5)           ║
    │ ║                               ║
    │ ║    Context + Noise            ║
    │ ║    ~30% of data               ║
    │ ║                               ║
0.0 ┤ ╚═══════════════════════════════╝
```

## Data Flow Diagram

### BEFORE Update (Inconsistent)

```
┌─────────────────────────────────────────────────────────────┐
│ Cell 36: Calculate Scores                                   │
│ ├─ Cosine scores: [0, 1] ────────────────┐                 │
│ └─ Rescaled scores: [0, 2] (display only)│                 │
└───────────────────────────────────────────┼─────────────────┘
                                            │
┌───────────────────────────────────────────┼─────────────────┐
│ Cell 37: Analyze & Display                │                 │
│ └─ Show rescaled distributions (no save) ─┘                 │
└─────────────────────────────────────────────────────────────┘
                                            ↓
                                   ┌────────────────┐
                                   │ Confidence CSV │
                                   │ files saved    │
                                   │ with COSINE    │ ← Problem!
                                   │ scores         │
                                   └────────┬───────┘
                                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Cell 50: Dataset Class                                      │
│ └─ Tries to read 'rescaled_<topic>' columns ────────┐      │
└─────────────────────────────────────────────────────┼───────┘
                                                      │
                            ┌─────────────────────────┘
                            │ Columns don't exist or
                            │ have wrong values!
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Training: Confused!                                         │
│ └─ Dataset expects [0, 2] but gets [0, 1]                  │
└─────────────────────────────────────────────────────────────┘
```

### AFTER Update (Consistent)

```
┌─────────────────────────────────────────────────────────────┐
│ Cell 36: Calculate Scores                                   │
│ ├─ Cosine scores: [0, 1] (reference)                       │
│ └─ Rescaled scores: [0, 2] (for training) ──────────┐      │
└─────────────────────────────────────────────────────┼───────┘
                                                      │
┌─────────────────────────────────────────────────────┼───────┐
│ Cell 37: Classify & SAVE                            │       │
│ ├─ 5-tier classification (analysis) ────────────────┤       │
│ ├─ 3-tier classification (training) ────────────────┤       │
│ └─ SAVE files with RESCALED scores ─────────────────┘       │
└─────────────────────────────────────────────────────────────┘
                            ↓
                   ┌────────────────┐
                   │ Confidence CSV │
                   │ files saved    │
                   │ with RESCALED  │ ✓ Correct!
                   │ scores [0, 2]  │
                   └────────┬───────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Cells 41-44: Load & Prepare Training Data                  │
│ └─ Load files → Contains 'rescaled_<topic>' columns ✓      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Cell 50: Dataset Class                                      │
│ └─ Read 'rescaled_<topic>' columns → [0, 2] ✓              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Cells 55-61: Train Model                                   │
│ ├─ Input range: [0, 2] ✓                                   │
│ ├─ Target range: [0, 2] ✓                                  │
│ └─ Model learns rescaled scores ✓                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Cell 68: Generate Predictions                               │
│ ├─ Model outputs: [0, 2] ✓                                 │
│ ├─ Thresholds scaled 2x: 0.6, 0.8 ✓                        │
│ └─ Confidence assignment matches training ✓                 │
└─────────────────────────────────────────────────────────────┘
```

## Threshold Scaling

### Ordinal Classification

```
BEFORE (Cosine)                      AFTER (Rescaled)
───────────────                      ────────────────

0.0 ┤                               0.0 ┤
    │                                   │
    │   LOW                             │   LOW
    │                                   │
0.3 ┤ ─────── threshold                 │
    │                                   │
    │   MEDIUM                          │
    │                               0.6 ┤ ─────── threshold (2x)
0.4 ┤ ─────── threshold                 │
    │                                   │   MEDIUM
    │   HIGH                            │
    │                               0.8 ┤ ─────── threshold (2x)
    │                                   │
1.0 ┤                                   │   HIGH
                                        │
                                    2.0 ┤

Scaling factor: 2x
All thresholds multiplied by 2
```

### Confidence Assignment

```
BEFORE (Cosine)                      AFTER (Rescaled)
───────────────                      ────────────────

Score >= 0.4 & margin > 0.1          Score >= 0.8 & margin > 0.2
        ↓                                    ↓
    HIGH confidence                      HIGH confidence

Score >= 0.3 | margin > 0.05         Score >= 0.6 | margin > 0.1
        ↓                                    ↓
    MEDIUM confidence                    MEDIUM confidence

    Otherwise                            Otherwise
        ↓                                    ↓
    LOW confidence                       LOW confidence

Scaling: All thresholds × 2
```

## Training Data Splits

### Option 1: Labeled Only

```
┌────────────────────────────────────┐
│ HIGH CONFIDENCE (rescaled >= 1.0)  │
│                                    │
│ Core + Moderate quality            │
│ ~1,000-2,000 chunks                │
│                                    │
│ Use for: Direct training           │
└────────────────────────────────────┘
```

### Option 2: Labeled + Pseudo

```
┌────────────────────────────────────┐
│ HIGH CONFIDENCE (rescaled >= 1.0)  │
│ ~1,000-2,000 chunks                │
└────────────────────────────────────┘
              +
┌────────────────────────────────────┐
│ LOW CONFIDENCE (0.5-1.0)           │
│ ~1,500-3,000 chunks (sampled)      │
│                                    │
│ Use as: Pseudo-labels              │
└────────────────────────────────────┘
              =
┌────────────────────────────────────┐
│ TOTAL: ~2,500-5,000 chunks         │
└────────────────────────────────────┘
```

### Option 3: Labeled + Unlabeled

```
┌────────────────────────────────────┐
│ HIGH CONFIDENCE (rescaled >= 1.0)  │
│ ~1,000-2,000 chunks                │
└────────────────────────────────────┘
              +
┌────────────────────────────────────┐
│ NO CONFIDENCE (< 0.5)              │
│ ~1,000-2,000 chunks (sampled)      │
│                                    │
│ Use as: Unlabeled (consistency)    │
└────────────────────────────────────┘
```

## Expected Distribution After Training

```
TRAINING DATA                    MODEL PREDICTIONS
─────────────                    ─────────────────

High: 35% ████████             High conf: 30% ███████
Low:  35% ████████             Med conf:  40% ██████████
None: 30% ███████              Low conf:  30% ███████

Should be similar but not identical
Model learns to distinguish quality
```

## Score Quality Examples

```
RESCALED SCORE    INTERPRETATION              EXAMPLE TEXT
──────────────    ──────────────              ────────────

2.0 ─────────┐   Perfect match               "slavery legacy directly caused
1.8          │   Core relevance              persistent poverty in these
1.6          │                                communities..."
1.5 ─────────┤
1.4          │   Strong match                "historical injustices continue
1.2          │   Moderate relevance          to impact economic development
1.1          │                                through..."
1.0 ─────────┤
0.8          │   Decent match                "inequality stemming from past
0.6          │   Weak relevance              discrimination affects education
0.5 ─────────┤                                access..."
0.4          │   Vague mention               "various historical factors
0.3          │   Context only                including colonial period..."
0.2          │
0.1          │   Little/no relevance         "the region's development over
0.0 ─────────┘                                time shows progress..."
```

## Key Takeaways

### 1. Score Range
```
OLD: [0, 1] → Compressed
NEW: [0, 2] → Well-distributed
```

### 2. Thresholds
```
OLD: 0.3, 0.4 → Based on compressed range
NEW: 0.6, 0.8 → Scaled 2x for new range
```

### 3. Quality Tiers
```
OLD: Hard to distinguish (all ~0.5)
NEW: Clear tiers (0.5, 1.0, 1.5, 2.0)
```

### 4. Training Pipeline
```
OLD: Inconsistent (dataset expects rescaled, gets cosine)
NEW: Consistent (rescaled end-to-end)
```

### 5. Benefits
```
✓ Better distribution (4x)
✓ Clearer quality levels
✓ Improved training signal
✓ Consistent thresholds
✓ End-to-end rescaling
```

## Quick Reference: Cell Changes

```
┌──────────┬────────────────────────────────────────────┐
│ Cell 37  │ + Save rescaled confidence files           │
│          │   (high/low/none with rescaled scores)     │
├──────────┼────────────────────────────────────────────┤
│ Cell 50  │ ~ Clarified rescaled score usage           │
│          │   (no code change, comments updated)       │
├──────────┼────────────────────────────────────────────┤
│ Cell 68  │ ✱ Updated ALL thresholds × 2               │
│          │   0.30→0.60, 0.40→0.80, 0.10→0.20, etc.   │
└──────────┴────────────────────────────────────────────┘

Legend:
  + Added new functionality
  ~ Updated documentation
  ✱ Modified existing logic
```

## Action Items

```
┌─────────────────────────────────────────────────────┐
│ 1. Run Cell 37                                      │
│    ↓                                                │
│    Saves rescaled confidence files                  │
│                                                     │
│ 2. Run Cells 47-61                                  │
│    ↓                                                │
│    Trains model on rescaled scores [0, 2]          │
│                                                     │
│ 3. Run Cells 66-69                                  │
│    ↓                                                │
│    Predicts with rescaled thresholds               │
│                                                     │
│ 4. Validate                                         │
│    ↓                                                │
│    Check distributions match expectations          │
└─────────────────────────────────────────────────────┘
```

---

**For more details**: See [RESCALED_SCORES_README.md](RESCALED_SCORES_README.md)

**For step-by-step guide**: See [QUICK_START_RESCALED_TRAINING.md](QUICK_START_RESCALED_TRAINING.md)

**For technical summary**: See [RESCALED_SCORES_UPDATE_SUMMARY.md](RESCALED_SCORES_UPDATE_SUMMARY.md)
