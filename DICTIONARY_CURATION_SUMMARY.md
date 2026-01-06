# Dictionary Curation Summary

**Date:** November 12, 2025
**Output:** `workflow_data/Finetuned_slaverypolicy-Slavery-Policy_11.12.25_v1/Dictionary/Curated_dictionary.csv`

---

## Overview

Created a curated dictionary by combining and filtering terms from two expanded candidate files:
1. `Finetuned_slaverypolicy-Slavery-Policy_11.12.25_v1` (157 terms)
2. `pretrained-Slavery_11.10.25_succes` (1,024 terms)

---

## Curation Results

### Summary Statistics

| Metric | Value |
|--------|-------|
| **Input Terms** | 1,181 unique terms |
| **Curated Terms** | 463 terms (39.2% kept) |
| **Removed Terms** | 718 terms (60.8%) |
| **Topics** | 4 topics |

### Terms per Topic

| Topic | Terms | High Quality (≥0.75) |
|-------|-------|---------------------|
| **Historical Slavery** | 173 | 62 (35.8%) |
| **Heritage & Memory** | 129 | 51 (39.5%) |
| **Modern Racism & Discrimination** | 104 | 47 (45.2%) |
| **Colonial Systems** | 57 | 29 (50.9%) |

---

## Quality Metrics

### Cosine Similarity Distribution

| Threshold | Count | Percentage |
|-----------|-------|------------|
| ≥ 0.9 | 65 | 14.0% |
| ≥ 0.8 | 129 | 27.9% |
| ≥ 0.7 | 274 | 59.2% |
| ≥ 0.6 | 454 | 98.1% |

### Document Frequency Distribution

| Threshold | Count | Notes |
|-----------|-------|-------|
| ≥ 100 | 39 | Very common terms |
| ≥ 50 | 75 | Common terms |
| ≥ 20 | 169 | Moderately common |
| ≥ 10 | 286 | Regular occurrence |

---

## Curation Criteria Applied

### 1. Quality Thresholds
- **Minimum cosine similarity:** 0.60
- **Minimum document frequency:** 3
- **High quality threshold:** 0.75

### 2. Terms REMOVED (Examples)

**Generic Policy/Administrative Jargon:**
- `wodc`, `wbi`, `wiv`, `wsw` (agency acronyms)
- `aanbesteding`, `uitbesteding` (tendering)
- `nederland`, `regering`, `rijksoverheid` (too generic)

**Generic Infrastructure:**
- `infrastructurele`, `bouwt`, `bouwen`, `aanleg`
- `installaties`, `inrichtingen`

**Irrelevant Terms:**
- `vergroenen` (greening)
- `afvalverwerking` (waste processing)
- `wier` (seaweed)
- `recreatie`, `olie`

**Overly Generic:**
- `arbeid` (labor - too generic alone)
- `markt`, `verkoop` (market, sales)
- Time periods alone: `17e`, `18e`, `19e`

### 3. Terms KEPT (Force-Keep List)

**Core Slavery Terms:**
- `slavernij`, `slavernijverleden`, `slavernijgeschiedenis`
- `slavenhandel`, `slaven`, `slaafgemaakten`
- `dwangarbeid`, `slavenarbeid`, `arbeidsdwang`

**Core Colonial Terms:**
- `kolonie`, `koloniaal`, `kolonialisme`, `kolonisatie`
- `plantage`, `plantages`, `plantagehouder`
- `exploitatie`, `wic`, `handelscompagnieën`

**Heritage & Memory:**
- `herinneren`, `herdenken`, `monument`, `erfgoed`
- `geschiedenisonderwijs`, `canon`, `museum`
- `excuses`, `schadevergoeding`, `erkenning`

**Discrimination & Racism:**
- `discriminatie`, `racisme`, `antiracisme`
- `uitsluiting`, `ongelijkheid`, `segregatie`
- `vooroordelen`, `stereotypering`

**Geographic Specificity:**
- `curaçao`, `bonaire`, `aruba`, `surinaamse`
- `West-Indië`, `Caribisch gebied`, `paramaribo`

---

## Sample Terms by Topic

### Historical Slavery (Top 10)
1. `slavernij` (cosine=1.0, df=7)
2. `slavenhandel` (cosine=1.0, df=249)
3. `slaven` (cosine=1.0, df=169)
4. `slavenschip` (cosine=1.0, df=9)
5. `slaafgemaakten` (cosine=1.0, df=377)
6. `mensonterende` (cosine=1.0, df=7)
7. `slaaf` (cosine=0.9733, df=108)
8. `slaafgemaakte` (cosine=0.9731, df=152)
9. `slavenhandelaren` (cosine=0.9609, df=14)
10. `dwangarbeid` (cosine=0.9583, df=120)

### Colonial Systems (Top 10)
1. `exploitatie` (cosine=1.0, df=229)
2. `kolonie` (cosine=1.0, df=116)
3. `koloniaal` (cosine=1.0, df=70)
4. `kolonisatie` (cosine=1.0, df=25)
5. `plantage` (cosine=1.0, df=117)
6. `dwangarbeid` (cosine=1.0, df=32)
7. `curaçao` (cosine=0.978, df=223)
8. `koloniale` (cosine=0.9736, df=9)
9. `plantages` (cosine=0.9373, df=140)
10. `wic` (cosine=0.9135, df=159)

### Heritage & Memory (Top 10)
1. `herinneren` (cosine=1.0, df=12)
2. `herinnering` (cosine=1.0, df=21)
3. `herdenken` (cosine=1.0, df=16)
4. `monument` (cosine=1.0, df=29)
5. `erfgoed` (cosine=1.0, df=38)
6. `museum` (cosine=1.0, df=57)
7. `tentoonstelling` (cosine=1.0, df=13)
8. `educatie` (cosine=1.0, df=27)
9. `slavernijverleden` (cosine=1.0, df=257)
10. `canon` (cosine=1.0, df=11)

### Modern Racism & Discrimination (Top 10)
1. `racisme` (cosine=1.0, df=90)
2. `discriminatie` (cosine=1.0, df=166)
3. `ongelijkheid` (cosine=1.0, df=16)
4. `antiracisme` (cosine=1.0, df=6)
5. `uitsluiting` (cosine=1.0, df=45)
6. `vooroordelen` (cosine=1.0, df=48)
7. `stereotypering` (cosine=1.0, df=19)
8. `racistisch` (cosine=0.9759, df=24)
9. `discrimineren` (cosine=0.9738, df=22)
10. `structurele discriminatie` (cosine=0.9718, df=10)

---

## Curation Rules Applied

### Pattern-Based Filtering

**Keep if term contains:**
- `slav*`, `dwang*` (slavery, coercion)
- `koloni*`, `plantage*` (colonial systems)
- `herinner*`, `herdenk*`, `monument*`, `erfgoed*` (memory/heritage)
- `discrimin*`, `racis*`, `uitslu*` (discrimination)

**Remove if term contains:**
- `vergroen*`, `afval*` (environmental, unrelated)
- `aanbesteding*`, `bouw*`, `infra*` (generic infrastructure)

### Multi-word Phrases
- **Kept:** More specific, better signal
- Examples: `koloniale wetgeving`, `Atlantische driehoekshandel`, `structurele discriminatie`

### Compound Words
- **Prioritized:** Terms with specific components
- Examples: `slavernijverleden`, `geschiedenisonderwijs`, `plantagehouder`

---

## Format Compliance

The curated dictionary conforms to the required format:

```csv
topic,term,cosine,df
Colonial Systems,exploitatie,1.0,229
Colonial Systems,kolonie,1.0,116
Heritage & Memory,herinneren,1.0,12
Historical Slavery,slavernij,1.0,7
...
```

**Columns:**
- `topic` - Standardized topic name
- `term` - Dictionary term (word or phrase)
- `cosine` - Cosine similarity to seed term (0-1)
- `df` - Document frequency (number of chunks containing term)

---

## Topic Name Standardization

Original topic names were standardized:

| Original | Standardized |
|----------|--------------|
| Historical slavery | Historical Slavery |
| Colonialism | Colonial Systems |
| Modern racism& inequality | Modern Racism & Discrimination |
| Heritage & memory | Heritage & Memory |

---

## Next Steps

This curated dictionary can now be used for:

1. **CHECKPOINT 4:** Building weighted topic vectors
2. **CHECKPOINT 5:** Scoring and classifying chunks
3. **CHECKPOINT 6+:** Training BERTje model

The dictionary provides:
- ✅ High-quality terms (59% have cosine ≥ 0.7)
- ✅ Topic-specific vocabulary
- ✅ Removal of noise and generic terms
- ✅ Balance across topics (57-173 terms each)
- ✅ Proper format for workflow processing

---

## Files

**Curation Script:** `curate_dictionary_simple.py`
**Output:** `workflow_data/Finetuned_slaverypolicy-Slavery-Policy_11.12.25_v1/Dictionary/Curated_dictionary.csv`
**Total Terms:** 463
**Quality:** 39.2% retention rate (appropriate for focused, high-quality dictionary)
