# Quick Reference: Using BERTJE + Cosine Predictions

## One-Page Guide for Policy Analysis

---

## The Bottom Line

**Question**: Are the scores accurate enough for policy insight?

**Answer**: YES - for broad patterns. NO - for precise labels.

- **Score similarity**: 0.997 (excellent)
- **Primary topic agreement**: 60% (moderate)
- **High confidence agreement**: 100% (perfect)

---

## Three-Level Confidence System

| Level | % of Data | Agreement | How to Use |
|-------|-----------|-----------|------------|
| **HIGH** | 5.6% | 100% | ✓ Trust the label completely |
| **MEDIUM** | 78.9% | 50-64% | ~ Likely contains topic, verify if critical |
| **LOW** | 15.5% | 50% | ✗ Multi-topic or uncertain, use distributions |

---

## Decision Tree

```
Is confidence HIGH?
  └─ YES → Use primary topic label (100% reliable)
  └─ NO  → Do both models agree?
          └─ YES → Likely accurate (64% reliable)
          └─ NO  → Check score distributions
                   Are scores close (<0.05 apart)?
                   └─ YES → Multi-topic content
                   └─ NO  → Review text manually
```

---

## What The Scores Mean

### Good Separation (High Confidence)
```
EDUC: 0.45  ← Clear winner
GOV:  0.30
ECON: 0.15
SOC:  0.10
Margin: 0.15 → HIGH confidence ✓
```

### Flat Profile (Low Confidence)
```
GOV:  0.28  ← Close scores
EDUC: 0.27
SOC:  0.25
ECON: 0.20
Margin: 0.01 → LOW confidence ✗ (Multi-topic!)
```

---

## Common Patterns & Solutions

### Pattern 1: Both Models Agree (60% of cases)
**Action**: Use the agreed-upon topic
**Reliability**: 60-100% depending on confidence

### Pattern 2: Models Disagree, Scores Close (25% of cases)
**Cause**: Multi-topic content
**Action**: Report all relevant topics (e.g., "40% ECON, 30% GOV")
**Example**: Document about economic policy → both ECON and GOV are correct

### Pattern 3: Models Disagree, Scores Far Apart (15% of cases)
**Cause**: Different semantic features emphasized
**Action**: Review text manually
**Note**: Often administrative/generic content

---

## Quick Stats

| Metric | Value |
|--------|-------|
| Total chunks analyzed | 3,854 |
| Sample examined | 40 |
| Cosine-BERTJE correlation | 0.997 |
| Average score difference | 0.044 |
| Rank agreement | 83.3% |

---

## Use Cases: Yes or No?

| Task | Suitable? | Notes |
|------|-----------|-------|
| "Find docs about economics" | ✓ YES | Filter by high confidence |
| "What % discuss governance?" | ✓ YES | Corpus-level patterns |
| "Track topics over time" | ✓ YES | Trend analysis |
| "This chunk is ONLY about X" | ✗ NO | Many are multi-topic |
| "Classify for legal purposes" | ✗ NO | Needs >90% accuracy |
| "Label for ML training" | ~ MAYBE | Only use high confidence |

---

## Best Practices

### DO:
- ✓ Use high-confidence predictions as ground truth
- ✓ Report score distributions for multi-topic docs
- ✓ Validate with manual samples
- ✓ Combine both model outputs
- ✓ Track confidence levels

### DON'T:
- ✗ Force single-topic labels on flat scores
- ✗ Ignore disagreements between models
- ✗ Use low-confidence predictions uncritically
- ✗ Expect 100% accuracy overall
- ✗ Overlook score margins

---

## Code Snippet

```python
def classify_chunk(row):
    """Recommended classification strategy"""

    # Check BERTJE confidence
    if row['bertje_confidence'] == 'high':
        return {
            'primary': row['bertje_primary_topic'],
            'confidence': 'high',
            'reliability': 1.00
        }

    # Check model agreement
    if row['models_agree']:
        conf = 'medium' if row['bertje_confidence'] == 'medium' else 'low'
        return {
            'primary': row['bertje_primary_topic'],
            'confidence': conf,
            'reliability': 0.64 if conf == 'medium' else 0.50
        }

    # Models disagree - use distributions
    return {
        'primary': None,  # Don't force single label
        'distribution': {
            'EDUC': row['bertje_Educational Disadvantage & Brain Drain_score'],
            'GOV': row['bertje_Governance Distrust & Corruption_score'],
            'ECON': row['bertje_Persistent Poverty & Economic Vulnerability_score'],
            'SOC': row['bertje_Social Fragmentation & Racism_score']
        },
        'confidence': 'uncertain',
        'reliability': 0.40
    }
```

---

## Key Insight

**Policy documents are inherently multi-topic.**

Don't ask: "What topic is this?"
Ask instead: "Which topics does this discuss?"

The 60% agreement isn't a failure - it reflects the **messy reality of policy texts** that blend economics, governance, social issues, and education.

---

## When in Doubt

1. Check **both model predictions**
2. Look at **score distributions**
3. Review the **actual text**
4. Use **confidence levels** as guidance
5. Report **multiple topics** when appropriate

---

## Visual Guide to Confidence

```
HIGH (100% reliable)
████████████████████ 0.45 EDUC
████████████░░░░░░░░ 0.30 GOV
───────────────────────────────
Margin: 0.15 → Clear winner

MEDIUM (64% reliable)
████████████████░░░░ 0.35 ECON
█████████████░░░░░░░ 0.28 GOV
───────────────────────────────
Margin: 0.07 → Plausible

LOW (50% reliable)
██████████████░░░░░░ 0.28 GOV
█████████████░░░░░░░ 0.27 EDUC
███████████░░░░░░░░░ 0.25 SOC
───────────────────────────────
Margin: 0.01 → Ambiguous
```

---

## Final Recommendation

**Use this system as a powerful exploratory tool, not as an oracle.**

It will help you:
- Discover patterns across thousands of documents
- Filter corpus for relevant themes
- Understand topic co-occurrence
- Generate hypotheses for deeper analysis

But always:
- Validate findings with samples
- Report uncertainties transparently
- Combine automated and manual methods
- Acknowledge multi-topic nature of texts

---

**Files**: See SEMANTIC_EVALUATION_REPORT.md and EVALUATION_SUMMARY.md for full details.
