# DOC-2-073 Embedding Reliability-Disease Bias - sandbox slice (exp200/173)

**Outcome: documented boundary. Primary and Pivot 1 failed their locked gates. The null itself is informative.**

## Setup
I tested AlphaMissense (AM), a deployed protein-language-model-derived variant predictor, on 554 random rare-disease genes (UniProt entries with an Orphanet cross-reference). 16,159 ClinVar missense variants (>= 1 star, P/LP vs B/LB) were matched to AM scores and AlphaFold pLDDT. Genes were split into tiers by how studied they are (UniProt citation count, tertiles).

## Results
- **Primary (fail):** AUROC 0.943 (least-studied third), 0.951, 0.956 (most-studied). The gap is 0.013 (CI -0.007 to 0.032). It is also absent within structured residues (-0.009). False "likely pathogenic" calls on benign variants are 8-9% in every tier.
- **Pivot 1 (fail):** AM's sensitivity for pathogenic variants in low-confidence (pLDDT < 70) regions is only 0.06 lower than in confident regions, and the CI includes 0.
- **Descriptive (not gated):** specificity falls as structure confidence rises. 90% of benign variants are called benign in disordered regions (pLDDT < 50) vs 77% at pLDDT >= 90. About 1 in 4 benign variants in well-folded cores gets a "likely pathogenic" call.

## What is useful from the failure
1. For curators working on rare-disease genes: in this sample, AM's performance does not drop for poorly studied genes. The feared "neglected-gene penalty" was not found. AM evidence need not be down-weighted just because a gene is obscure (within ClinVar-represented variants).
2. The main AM error mode is not disorder. It is over-calling benign variants in confident, well-folded regions. That is the place to be careful when using AM as supporting pathogenic evidence.
3. Hypothesis for a future locked test, not a claim: in the least-studied genes, pathogenic variants in disordered regions may be missed more often (a 0.26 gap in a post-hoc subgroup of 94 variants).

## Limits
- ClinVar variant_summary has no creation date, so variants that predate AM's release were not excluded. AM did not train on ClinVar labels, but ClinVar-based tuning risk remains.
- Well-studied genes contribute far more P/LP variants, so tier comparisons weigh genes unequally. The gene-level bootstrap accounts for this in the CIs.
- UniProt citation count is a rough proxy for how studied a gene is.

## Reproduce
python3 code/genes.py; python3 code/clinvar.py; python3 code/af.py; python3 code/run.py; python3 code/pivot1.py
