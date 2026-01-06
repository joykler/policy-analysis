import pandas as pd
import json

# Manual evaluation results
evaluations = [
    # Batch 1: Racism
    {
        'chunk_id': 'ad8dfafd:00808',
        'actual_education': 'marginal',
        'actual_governance': 'present',
        'actual_economic': 'primary',
        'actual_racism': 'present',
        'assessment_quality': 'fair',
        'assessment_notes': 'Misclassified as racism primary. This is fundamentally economic history about wealth accumulation through VOC slavery system. Economic exploitation (280k guilders wealth, enslaved people as valued merchandise) is the primary focus, though structural racism is present.'
    },
    {
        'chunk_id': '183a57ee:01608',
        'actual_education': 'not_present',
        'actual_governance': 'present',
        'actual_economic': 'marginal',
        'actual_racism': 'primary',
        'assessment_quality': 'good',
        'assessment_notes': 'Correctly classified. Focuses on slave resistance (Maroons, Haiti revolt, Curacao 1795), violent oppression, and legal dehumanization (6-month rule in Dutch Republic). Governance present through legal framework discussion.'
    },
    {
        'chunk_id': 'ad8dfafd:00823',
        'actual_education': 'marginal',
        'actual_governance': 'marginal',
        'actual_economic': 'primary',
        'actual_racism': 'present',
        'assessment_quality': 'poor',
        'assessment_notes': 'Misclassified. Primarily economic history about Utrecht merchant families, colonial trade networks (tobacco, sugar from Brazil), and Jewish traders. Racism connection is contextual (anti-Jewish exclusions, Portuguese Nation in slave trade) not central.'
    },
    {
        'chunk_id': 'fc00b8d3:00380',
        'actual_education': 'present',
        'actual_governance': 'not_present',
        'actual_economic': 'marginal',
        'actual_racism': 'primary',
        'assessment_quality': 'fair',
        'assessment_notes': 'Correct topic but appropriately low scores. This is scholarly metadiscourse about slavery research methodology (space comparisons, mortality rates, fatalism). Academic education aspect present but substantive topic is racism/slavery conditions.'
    },
    {
        'chunk_id': '8bd16e49:01505',
        'actual_education': 'not_present',
        'actual_governance': 'present',
        'actual_economic': 'marginal',
        'actual_racism': 'primary',
        'assessment_quality': 'excellent',
        'assessment_notes': 'Strong correct identification. Direct testimonies of Caribbean Dutch migrants experiencing discrimination by gemeente offices, skin color prejudice, disrespectful treatment, single mother stereotypes. Clear contemporary racial discrimination and social fragmentation.'
    },

    # Batch 2: Education
    {
        'chunk_id': '9dd5d756:00503',
        'actual_education': 'present',
        'actual_governance': 'primary',
        'actual_economic': 'present',
        'actual_racism': 'not_present',
        'assessment_quality': 'poor',
        'assessment_notes': 'Misclassified. This is government budget document about cultural infrastructure subsidies, museums, libraries. Primarily governance (budget allocations, Erfgoedwet regulatory framework). Model correctly shows uncertainty (all scores ~0.3) but topic assignment wrong.'
    },
    {
        'chunk_id': '9dd5d756:00557',
        'actual_education': 'present',
        'actual_governance': 'primary',
        'actual_economic': 'marginal',
        'actual_racism': 'marginal',
        'assessment_quality': 'fair',
        'assessment_notes': 'Partially correct. Parliamentary motions about Caribbean students BSN, scholarships, media policy. Education content present but wrapped in governance procedures. Should be governance primary, education present.'
    },
    {
        'chunk_id': '2c88535c:01298',
        'actual_education': 'not_present',
        'actual_governance': 'primary',
        'actual_economic': 'present',
        'actual_racism': 'not_present',
        'assessment_quality': 'poor',
        'assessment_notes': 'Completely misclassified. Zero educational content. This is infrastructure governance about Caribbean Netherlands airport masterplans, ICAO regulations, funding agreements. Very low/negative scores correctly show model confusion.'
    },
    {
        'chunk_id': '2c88535c:01319',
        'actual_education': 'primary',
        'actual_governance': 'present',
        'actual_economic': 'marginal',
        'actual_racism': 'marginal',
        'assessment_quality': 'excellent',
        'assessment_notes': 'Strong correct classification. Education inspection report showing systemic educational disadvantage in Bonaire: underqualified teachers, language barriers (Papiaments vs Dutch), learning deficits, governance problems. Core educational disadvantage and brain drain issues.'
    },
    {
        'chunk_id': '7b0dbe47:00967',
        'actual_education': 'primary',
        'actual_governance': 'not_present',
        'actual_economic': 'not_present',
        'actual_racism': 'primary',
        'assessment_quality': 'fair',
        'assessment_notes': 'Complex dual-topic. High education score reflects academic research methodology (statistics, scholarly discussion). Substantive topic is racism: mixed-race partnerships, racial categorization, slavery legacy, healing from trauma. Should be dual-coded education/racism or racism primary with education present.'
    },

    # Batch 3: Economic Vulnerability
    {
        'chunk_id': 'ad8dfafd:00831',
        'actual_education': 'not_present',
        'actual_governance': 'marginal',
        'actual_economic': 'primary',
        'actual_racism': 'present',
        'assessment_quality': 'good',
        'assessment_notes': 'Correctly classified. Focus on colonial wealth accumulation: 280,000 gulden inheritance (2.6M euros today), enslaved people (Siti, Lucretia, Jan) as property with ambiguous freedom status, inheritance law. Economic exploitation is primary theme.'
    },
    {
        'chunk_id': '183a57ee:01578',
        'actual_education': 'not_present',
        'actual_governance': 'marginal',
        'actual_economic': 'primary',
        'actual_racism': 'primary',
        'assessment_quality': 'fair',
        'assessment_notes': 'Dual-topic. Bosman detailed slave trade procedures: cowrie shell pricing, gift protocols, standardization of humans as merchandise ("maatman"). Economic trade mechanics are primary but extreme racist dehumanization is inseparable. Should be dual ECO/RAC.'
    },
    {
        'chunk_id': 'b1922fab:01020',
        'actual_education': 'not_present',
        'actual_governance': 'present',
        'actual_economic': 'primary',
        'actual_racism': 'marginal',
        'assessment_quality': 'good',
        'assessment_notes': 'Correctly classified. Clear economic vulnerability: lack of debt relief in Caribbean Netherlands, no insurance for damages, limited legal recourse, uninsured motorists, victim unable to recover compensation. Structural economic disadvantage despite governance context.'
    },
    {
        'chunk_id': '690c79e1:00429',
        'actual_education': 'not_present',
        'actual_governance': 'primary',
        'actual_economic': 'primary',
        'actual_racism': 'not_present',
        'assessment_quality': 'fair',
        'assessment_notes': 'Dual governance/economic. Government loans to Caribbean countries (Aruba, Curaçao, Sint Maarten), interest rates, Girobank bailout, debt refinancing. Economic assignment defensible but equally governance (fiscal Kingdom relationships). Low scores show model uncertainty.'
    },
    {
        'chunk_id': '799a3980:00107',
        'actual_education': 'marginal',
        'actual_governance': 'present',
        'actual_economic': 'primary',
        'actual_racism': 'primary',
        'assessment_quality': 'excellent',
        'assessment_notes': 'Strong classification. WIC Brazil slavery: deliberate economic strategy for sugar control, 31,000 Africans transported, conquest of Luanda for slave supply. Text analyzes economic motives while acknowledging shift in Dutch attitude toward slavery 1600-1640. Economic exploitation primary, racism substantial.'
    },

    # Batch 4: Governance
    {
        'chunk_id': 'ff22de3d:00702',
        'actual_education': 'not_present',
        'actual_governance': 'primary',
        'actual_economic': 'not_present',
        'actual_racism': 'not_present',
        'assessment_quality': 'good',
        'assessment_notes': 'Correctly classified despite very low scores. Parliamentary accountability tracking: ministerial commitments to Tweede Kamer, policy progress updates, RIVM reports. Pure administrative governance content.'
    },
    {
        'chunk_id': 'ff22de3d:00713',
        'actual_education': 'not_present',
        'actual_governance': 'primary',
        'actual_economic': 'not_present',
        'actual_racism': 'not_present',
        'assessment_quality': 'excellent',
        'assessment_notes': 'Clear correct identification. Parliamentary oversight: government accountability tracking, policy implementation monitoring, ministerial responses. Pure governance content with strongest score differential in sample (GOV 0.338).'
    },
    {
        'chunk_id': 'ff22de3d:00640',
        'actual_education': 'not_present',
        'actual_governance': 'primary',
        'actual_economic': 'marginal',
        'actual_racism': 'not_present',
        'assessment_quality': 'fair',
        'assessment_notes': 'Correct but weak signal. Health/social policy implementation: palliative care programs, loneliness initiatives, Wmo fee structures. All scores very close (~0.25) showing model appropriately uncertain. Content is government service delivery.'
    },
    {
        'chunk_id': '6cecf1ef:01135',
        'actual_education': 'not_present',
        'actual_governance': 'primary',
        'actual_economic': 'present',
        'actual_racism': 'primary',
        'assessment_quality': 'excellent',
        'assessment_notes': 'Complex but correctly prioritized. 1862 Dutch parliamentary debate on slave emancipation law: state oversight vs freedom, political disagreement, compensation costs. Primarily governance (legislative process structure) but substantive topic is slavery/racism. Correct given text focus on political debate mechanics.'
    },
    {
        'chunk_id': '183a57ee:01588',
        'actual_education': 'not_present',
        'actual_governance': 'primary',
        'actual_economic': 'present',
        'actual_racism': 'present',
        'assessment_quality': 'excellent',
        'assessment_notes': 'Strong identification (GOV 0.419 highest score). Suriname Sociëteit 1683-1795 governance structure: Amsterdam financing scheme, hereditary governorship, administrative conflicts planters vs directors, taxation disputes. Clear colonial misgovernance and governance distrust theme.'
    }
]

# Create DataFrame
df = pd.DataFrame(evaluations)

# Reorder columns
df = df[['chunk_id', 'actual_education', 'actual_governance', 'actual_economic', 'actual_racism',
         'assessment_quality', 'assessment_notes']]

# Save to CSV
df.to_csv(r'C:\Users\Home\policy-analysis\semantic_evaluation_results_v16.csv',
          index=False, encoding='utf-8')

print(f"Saved {len(df)} semantic evaluations to semantic_evaluation_results_v16.csv")

# Generate summary statistics
print("\n" + "="*80)
print("SEMANTIC EVALUATION SUMMARY")
print("="*80)

# Quality distribution
print("\n1. QUALITY DISTRIBUTION")
print("-" * 40)
quality_counts = df['assessment_quality'].value_counts()
print(quality_counts)
print(f"\nTotal: {len(df)} chunks evaluated")

# Calculate agreement with cosine scores
print("\n2. PRIMARY TOPIC ACCURACY")
print("-" * 40)

# Read original scores
scores_df = pd.read_csv(r'C:\Users\Home\policy-analysis\chunks_for_semantic_eval_v16.csv')

# Merge
merged = df.merge(scores_df[['chunk_id', 'score_education', 'score_governance',
                              'score_economic', 'score_racism', 'assigned_primary_topic']],
                  on='chunk_id')

# Determine actual primary from semantic eval
def get_actual_primary(row):
    scores = {
        'education': row['actual_education'],
        'governance': row['actual_governance'],
        'economic': row['actual_economic'],
        'racism': row['actual_racism']
    }
    # Convert to numeric: primary=3, present=2, marginal=1, not_present=0
    numeric_scores = {k: {'primary': 3, 'present': 2, 'marginal': 1, 'not_present': 0}[v]
                     for k, v in scores.items()}
    max_score = max(numeric_scores.values())
    primaries = [k for k, v in numeric_scores.items() if v == max_score]
    return primaries[0] if len(primaries) == 1 else 'ambiguous'

merged['actual_primary'] = merged.apply(get_actual_primary, axis=1)

# Determine model primary from scores
def get_model_primary(row):
    scores = {
        'education': row['score_education'],
        'governance': row['score_governance'],
        'economic': row['score_economic'],
        'racism': row['score_racism']
    }
    max_score = max(scores.values())
    primaries = [k for k, v in scores.items() if v == max_score]
    return primaries[0] if len(primaries) == 1 else 'ambiguous'

merged['model_primary'] = merged.apply(get_model_primary, axis=1)

# Calculate accuracy
merged['correct'] = merged['actual_primary'] == merged['model_primary']
accuracy = merged['correct'].sum() / len(merged) * 100

print(f"\nModel correctly identified primary topic: {merged['correct'].sum()}/{len(merged)} ({accuracy:.1f}%)")
print(f"\nAssigned topic matched highest cosine score: {(merged['assigned_primary_topic'].str.contains('Education', case=False) & (merged['model_primary'] == 'education')).sum() + (merged['assigned_primary_topic'].str.contains('Governance', case=False) & (merged['model_primary'] == 'governance')).sum() + (merged['assigned_primary_topic'].str.contains('Economic', case=False) & (merged['model_primary'] == 'economic')).sum() + (merged['assigned_primary_topic'].str.contains('Racism', case=False) & (merged['model_primary'] == 'racism')).sum()}/{len(merged)}")

# Error analysis by assigned category
print("\n3. ACCURACY BY ASSIGNED CATEGORY")
print("-" * 40)

category_map = {
    'Social Fragmentation & Racism': 'racism',
    'Educational Disadvantage & Brain Drain': 'education',
    'Persistent Poverty & Economic Vulnerability': 'economic',
    'Governance Distrust & Corruption': 'governance'
}

merged['assigned_simple'] = merged['assigned_primary_topic'].map(category_map)
merged['category_correct'] = merged['actual_primary'] == merged['assigned_simple']

for category in merged['assigned_primary_topic'].unique():
    cat_data = merged[merged['assigned_primary_topic'] == category]
    correct = cat_data['category_correct'].sum()
    total = len(cat_data)
    print(f"{category}: {correct}/{total} ({correct/total*100:.0f}%)")

# Common error patterns
print("\n4. COMMON ERROR PATTERNS")
print("-" * 40)

errors = merged[~merged['category_correct']]
if len(errors) > 0:
    print(f"\nTotal errors: {len(errors)}/{len(merged)}")
    print("\nError types:")
    for idx, row in errors.iterrows():
        print(f"  - {row['chunk_id']}: Assigned '{row['assigned_primary_topic']}' "
              f"but actually '{row['actual_primary']}'")
        print(f"    Quality: {row['assessment_quality']}")
        print(f"    Scores: EDU={row['score_education']:.3f} GOV={row['score_governance']:.3f} "
              f"ECO={row['score_economic']:.3f} RAC={row['score_racism']:.3f}")
        print()

# Key patterns
print("\n5. KEY PATTERNS IDENTIFIED")
print("-" * 40)
print("""
a) ECONOMIC vs RACISM confusion: Chunks about slavery often blend economic
   exploitation with racial oppression. Model sometimes prioritizes one over other.

b) GOVERNANCE wrapping: Education/economic content wrapped in governance
   procedures (parliamentary motions, budget documents) sometimes misclassified.

c) LOW SCORE uncertainty: When all scores <0.3, model is appropriately uncertain
   but topic assignment may be unreliable.

d) DUAL-TOPIC chunks: Some chunks genuinely span two topics (e.g., economic
   mechanisms of slavery = both ECO + RAC). Single-label classification loses nuance.

e) SCHOLARLY vs SUBSTANTIVE: Academic texts about racism score high on education
   due to research methodology, even when substantive topic is racism.
""")

print("\n" + "="*80)
