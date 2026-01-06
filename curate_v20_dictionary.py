"""
Comprehensive curation of v20 dictionary based on semantic understanding of the 4-topic framework.

Curation rules:
1. Remove semantic drift terms (marriage from wantrouwen, closing from uitsluiting)
2. Remove questionable low-DF semantic matches (abrupt from corruptie)
3. Remove overly generic high-DF terms that don't discriminate topics
4. Keep policy-relevant compounds even if morphologically derived
5. Keep genuine semantic relatives that add conceptual breadth
"""

import pandas as pd
import numpy as np

# Load dictionary
dict_path = r'workflow_data/slavery_Slavdict_pretraining_slavery_v20/Dictionary/expanded_candidates.csv'
df = pd.read_csv(dict_path)

print("="*80)
print("V20 DICTIONARY CURATION")
print("="*80)
print(f"Starting terms: {len(df):,}")
print()

# Track removals
removed_terms = []

def remove_term(term, topic, reason, parent=None):
    """Helper to track and remove terms"""
    removed_terms.append({
        'term': term,
        'topic': topic,
        'parent': parent,
        'reason': reason
    })

# ============================================================================
# RULE 1: Remove semantic drift from core/strong problems
# ============================================================================
print("RULE 1: Removing semantic drift terms from core/strong problems")
print("-" * 80)

# wantrouwen → marriage terms (NOT governance distrust)
marriage_terms = [
    'trouw', 'hertrouwde', 'huwelijk', 'getrouwde', 'trouwde', 'trouwen',
    'verwantschap'  # kinship, not trust
]
for term in marriage_terms:
    mask = (df['parent'] == 'wantrouwen') & (df['term'] == term)
    if mask.any():
        topic = df[mask]['topic'].iloc[0]
        remove_term(term, topic, 'Semantic drift: marriage term under wantrouwen (distrust)', 'wantrouwen')
        df = df[~mask]
        print(f"  Removed: {term} from wantrouwen (marriage, not distrust)")

# uitsluiting → closing/connecting terms (NOT social exclusion)
closing_terms = [
    'aansluit', 'afsluiten', 'aansluiten', 'sluiten', 'sluit',
    'sluiting', 'afsluiting', 'afsluit', 'sluitend', 'sluitende',
    'insluiting',  # imprisonment - borderline, but more about literal enclosure
    'kast',  # closet/cabinet - clearly wrong
    'ontsluiting',  # unlocking - not exclusion
    'opsluiting',  # imprisonment - borderline
    'uitsluitsel'  # conclusion/answer - wrong
]
for term in closing_terms:
    mask = (df['parent'] == 'uitsluiting') & (df['term'] == term)
    if mask.any():
        topic = df[mask]['topic'].iloc[0]
        remove_term(term, topic, 'Semantic drift: closing/connecting term under uitsluiting (exclusion)', 'uitsluiting')
        df = df[~mask]
        print(f"  Removed: {term} from uitsluiting (closing/connecting, not exclusion)")

# Keep: uitsluiten (to exclude), uitbuiting (exploitation), uitreding (withdrawal)

print(f"Removed {len([r for r in removed_terms if 'Semantic drift' in r['reason']])} semantic drift terms")
print()

# ============================================================================
# RULE 2: Remove questionable low-DF semantic matches
# ============================================================================
print("RULE 2: Removing questionable low-DF semantic matches")
print("-" * 80)

questionable_matches = [
    ('corruptie', 'abrupt', 'Governance Distrust & Corruption'),  # "sudden" not "corruption"
    ('machtsmisbruik', 'daadkrachtig', 'Governance Distrust & Corruption'),  # "decisive" is opposite of "abuse"
    ('patronage', 'koperen', 'Governance Distrust & Corruption'),  # "copper" not "patronage"
    ('nepotisme', 'nazisme', 'Governance Distrust & Corruption'),  # nazism not nepotism
]

for parent, term, topic in questionable_matches:
    mask = (df['parent'] == parent) & (df['term'] == term) & (df['topic'] == topic)
    if mask.any():
        remove_term(term, topic, f'Questionable semantic match under {parent}', parent)
        df = df[~mask]
        print(f"  Removed: {term} from {parent} (questionable semantic match)")

print(f"Removed {len([r for r in removed_terms if 'Questionable' in r['reason']])} questionable matches")
print()

# ============================================================================
# RULE 3: Remove overly generic high-DF substantive terms
# ============================================================================
print("RULE 3: Removing overly generic high-DF substantive terms (DF > 200)")
print("-" * 80)

# Define substantive categories
substantive_cats = ['core_problem', 'strong_problem', 'related_strong', 'related_moderate', 'related_weak']

# Generic terms that appear everywhere but don't discriminate topics
generic_high_df = [
    ('nederlandse', 832),  # "Dutch" - too generic
    ('nederlands', 260),   # "Dutch"
    ('caribisch', 312),    # "Caribbean" - geographic but too broad
]

# However, keep:
# - racisme (268), discriminatie (164) - core problems despite high DF
# - slavenhandel (353) - central to slavery legacy
# - werk (337), ministerie (330) - policy-relevant

for term, expected_df in generic_high_df:
    mask = (df['term'] == term) & (df['category'].isin(substantive_cats))
    if mask.any():
        for _, row in df[mask].iterrows():
            remove_term(term, row['topic'], f'Overly generic high-DF term (DF={expected_df})', row['parent'])
            print(f"  Removed: {term} (DF={expected_df}) from {row['topic'].split('&')[0].strip()}")
        df = df[~mask]

print(f"Removed {len([r for r in removed_terms if 'generic high-DF' in r['reason']])} generic high-DF terms")
print()

# ============================================================================
# RULE 4: Review and remove rare core/strong problems (DF < 3)
# ============================================================================
print("RULE 4: Reviewing rare core/strong problems (DF < 3)")
print("-" * 80)

# Terms that are genuinely rare but important - KEEP these
keep_rare = [
    'taalbarrières',  # language barriers - important concept
    'leerachterstand',  # learning disadvantage - important
    'omkoping',  # bribery - core corruption concept
    'jeugdwerkloosheid',  # youth unemployment - specific important issue
    'ereschuld',  # debt of honor - slavery reparations context
]

# Terms that seem too specific or questionable - REMOVE
remove_rare = [
    'migratie-',  # just hyphenated variant
    'remigratie',  # very specific, only 2 docs
    'schoolsucces',  # positive framing, not a problem
    'taalproblematiek',  # redundant with taalachterstand
    'immigratiegeschiedenis',  # too specific
    'migratieverleden',  # too specific
    'migrantenachtergrond',  # too specific
    'deportatie',  # specific, but maybe keep? Let's be conservative and keep
    'verkoping',  # selling, not really omkoping
    'wantrouwend',  # just adjective form
    'vertrouwdheid',  # familiarity, different from trust
    'vertrouweling',  # confidant - specific role
    'vertrouwensband',  # bond of trust - compound
]

for term in remove_rare:
    mask = (df['term'] == term) & (df['category'].isin(['core_problem', 'strong_problem'])) & (df['df'] < 3)
    if mask.any():
        for _, row in df[mask].iterrows():
            remove_term(term, row['topic'], f'Rare core/strong problem (DF={row["df"]}) - low discriminative value', row['parent'])
            print(f"  Removed: {term} (DF={row['df']}) from {row['parent']}")
        df = df[~mask]

print(f"Removed {len([r for r in removed_terms if 'Rare core/strong' in r['reason']])} rare core/strong terms")
print()

# ============================================================================
# RULE 5: Prune redundant era context terms
# ============================================================================
print("RULE 5: Pruning redundant era context compounds")
print("-" * 80)

# Remove overly specific historical variants that don't add value
# Keep: slavernijverleden, slavernijgeschiedenis, koloniale, koloniaal, geschiedenis
# Remove: excessive morphological variants

era_redundant = []

# For each era parent, keep only top N children by cosine if they have many children
era_parents_to_prune = {
    'afschaffing': 30,  # Keep top 30 of 83
    'geschiedenis': 20,  # Keep top 20 of 61
}

for parent, keep_n in era_parents_to_prune.items():
    parent_terms = df[(df['parent'] == parent) & (df['category'] == 'era_context') & (~df['is_seed'].astype(bool))]

    if len(parent_terms) > keep_n:
        # Keep top N by cosine
        top_n = parent_terms.nlargest(keep_n, 'cosine')
        to_remove = parent_terms[~parent_terms.index.isin(top_n.index)]

        for _, row in to_remove.iterrows():
            remove_term(row['term'], row['topic'], f'Redundant era term under {parent} (keeping top {keep_n})', parent)
            era_redundant.append(row['term'])

        df = df[~df.index.isin(to_remove.index)]
        print(f"  Pruned {len(to_remove)} redundant terms from {parent} (kept top {keep_n})")

print(f"Removed {len(era_redundant)} redundant era terms")
print()

# ============================================================================
# RULE 6: Remove very low cosine terms (< 0.72)
# ============================================================================
print("RULE 6: Removing very low cosine expanded terms (< 0.72)")
print("-" * 80)

low_cosine_mask = (~df['is_seed'].astype(bool)) & (df['cosine'] < 0.72)
low_cosine_terms = df[low_cosine_mask]

for _, row in low_cosine_terms.iterrows():
    remove_term(row['term'], row['topic'], f'Low cosine similarity ({row["cosine"]:.3f})', row['parent'])

print(f"Removed {len(low_cosine_terms)} low cosine terms")
df = df[~low_cosine_mask]
print()

# ============================================================================
# RULE 7: Remove overly generic context terms
# ============================================================================
print("RULE 7: Removing overly generic geographic context")
print("-" * 80)

# "caribisch" already handled in RULE 3
# Keep specific islands: bonaire, curaçao, aruba, suriname, antillen, saba, st. eustatius

print(f"Already handled in RULE 3")
print()

# ============================================================================
# SUMMARY
# ============================================================================
print()
print("="*80)
print("CURATION SUMMARY")
print("="*80)
print(f"Starting terms:     {1200:,}")
print(f"Removed terms:      {len(removed_terms):,}")
print(f"Remaining terms:    {len(df):,}")
print(f"Reduction:          {len(removed_terms)/1200*100:.1f}%")
print()

# Breakdown by reason
print("Removal breakdown by reason:")
from collections import Counter
reason_counts = Counter([r['reason'].split(':')[0] for r in removed_terms])
for reason, count in reason_counts.most_common():
    print(f"  {reason:40s}: {count:4d}")
print()

# Check final composition
print("Final composition:")
print(f"  Seed terms:         {df['is_seed'].sum():,}")
print(f"  Expanded terms:     {(~df['is_seed'].astype(bool)).sum():,}")
print()

substantive_cats = ['core_problem', 'strong_problem', 'related_strong', 'related_moderate', 'related_weak']
substantive = df[df['category'].isin(substantive_cats)]
context = df[~df['category'].isin(substantive_cats)]
print(f"  Substantive terms:  {len(substantive):,} ({len(substantive)/len(df)*100:.1f}%)")
print(f"  Context terms:      {len(context):,} ({len(context)/len(df)*100:.1f}%)")
print()

print("By category:")
for cat in ['core_problem', 'strong_problem', 'related_strong', 'related_moderate', 'related_weak', 'era_context', 'geographic_context']:
    count = len(df[df['category'] == cat])
    print(f"  {cat:25s}: {count:4d} ({count/len(df)*100:.1f}%)")
print()

print("By topic:")
for topic in df['topic'].unique():
    count = len(df[df['topic'] == topic])
    topic_short = topic.split('&')[0].strip()
    print(f"  {topic_short:30s}: {count:4d}")
print()

# Quality metrics
expanded = df[~df['is_seed'].astype(bool)]
print("Quality metrics (expanded terms):")
print(f"  Mean cosine:        {expanded['cosine'].mean():.3f}")
print(f"  Median cosine:      {expanded['cosine'].median():.3f}")
print(f"  Min cosine:         {expanded['cosine'].min():.3f}")
print(f"  High quality (>0.8): {len(expanded[expanded['cosine'] > 0.8])/len(expanded)*100:.1f}%")
print()

# Save curated dictionary
output_path = r'workflow_data/slavery_Slavdict_pretraining_slavery_v20/Dictionary/curated_dictionary.csv'
df.to_csv(output_path, index=False)
print(f"Curated dictionary saved to: {output_path}")

# Save removal log
removal_df = pd.DataFrame(removed_terms)
removal_log_path = r'workflow_data/slavery_Slavdict_pretraining_slavery_v20/Dictionary/curation_removal_log.csv'
removal_df.to_csv(removal_log_path, index=False)
print(f"Removal log saved to: {removal_log_path}")

# Create detailed curation report
print()
print("="*80)
print("CREATING DETAILED CURATION REPORT")
print("="*80)

report_lines = []
report_lines.append("# V20 Dictionary Curation Report")
report_lines.append(f"Date: 2025-11-28")
report_lines.append("")
report_lines.append("## Curation Summary")
report_lines.append(f"- **Starting terms**: 1,200")
report_lines.append(f"- **Removed terms**: {len(removed_terms):,}")
report_lines.append(f"- **Final terms**: {len(df):,}")
report_lines.append(f"- **Reduction**: {len(removed_terms)/1200*100:.1f}%")
report_lines.append("")
report_lines.append("## Curation Rules Applied")
report_lines.append("")
report_lines.append("### Rule 1: Semantic Drift Removal")
report_lines.append("Removed terms that were morphologically similar but semantically unrelated:")
report_lines.append("- **wantrouwen** (distrust): Removed marriage terms (trouw, huwelijk, getrouwde)")
report_lines.append("- **uitsluiting** (exclusion): Removed closing/connecting terms (sluiten, aansluit, kast)")
report_lines.append("")
report_lines.append("### Rule 2: Questionable Semantic Matches")
report_lines.append("Removed low-DF terms with dubious semantic relationships:")
report_lines.append("- corruptie → abrupt (sudden, not corruption)")
report_lines.append("- machtsmisbruik → daadkrachtig (decisive, opposite of abuse)")
report_lines.append("- patronage → koperen (copper, not patronage)")
report_lines.append("")
report_lines.append("### Rule 3: Generic High-DF Terms")
report_lines.append("Removed overly generic terms that don't discriminate topics:")
report_lines.append("- nederlandse (DF: 832)")
report_lines.append("- nederlands (DF: 260)")
report_lines.append("- caribisch (DF: 312)")
report_lines.append("")
report_lines.append("### Rule 4: Rare Core/Strong Problems")
report_lines.append("Reviewed terms with DF < 3; removed overly specific variants")
report_lines.append("")
report_lines.append("### Rule 5: Redundant Era Context")
report_lines.append("Pruned excessive morphological variants in era_context:")
report_lines.append(f"- afschaffing: Kept top 30 of 83 children")
report_lines.append(f"- geschiedenis: Kept top 20 of 61 children")
report_lines.append("")
report_lines.append("### Rule 6: Low Cosine Filter")
report_lines.append("Removed expanded terms with cosine < 0.72")
report_lines.append("")
report_lines.append("## Final Dictionary Composition")
report_lines.append("")
report_lines.append(f"### Overall Stats")
report_lines.append(f"- Seeds: {df['is_seed'].sum():,}")
report_lines.append(f"- Expanded: {(~df['is_seed'].astype(bool)).sum():,}")
report_lines.append(f"- Substantive: {len(substantive):,} ({len(substantive)/len(df)*100:.1f}%)")
report_lines.append(f"- Context: {len(context):,} ({len(context)/len(df)*100:.1f}%)")
report_lines.append("")
report_lines.append("### Quality Metrics")
report_lines.append(f"- Mean cosine: {expanded['cosine'].mean():.3f}")
report_lines.append(f"- Min cosine: {expanded['cosine'].min():.3f}")
report_lines.append(f"- High quality (>0.8): {len(expanded[expanded['cosine'] > 0.8])/len(expanded)*100:.1f}%")
report_lines.append("")

report_path = r'workflow_data/slavery_Slavdict_pretraining_slavery_v20/Dictionary/CURATION_REPORT.md'
with open(report_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))

print(f"Curation report saved to: {report_path}")
print()
print("CURATION COMPLETE!")
