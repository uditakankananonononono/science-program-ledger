# DOC-2-073 The Embedding Reliability-Disease Bias Question - locked gates (22:22 IST, before variant/score data are joined)

## Sandbox-fit slice
Running protein language models is not possible here. Instead I test a deployed PLM-derived clinical predictor: AlphaMissense (AM, per-protein substitution scores published on AlphaFold DB), plus AlphaFold per-residue pLDDT, on rare-disease genes.

## Question (forward-useful)
Is AM less reliable on POORLY STUDIED rare-disease genes than on well-studied ones, and is any gap explained by structure confidence? This tells variant curators where AM evidence should be down-weighted.

## Data
- Genes: reviewed human UniProt entries with an Orphanet cross-reference (rare-disease genes), canonical length <= 2700, random 600 (seed 0). Study density = number of literature citations in the UniProt entry (lit_pubmed_id count). Tiers = bottom vs top tertile within the sample.
- Variants: ClinVar variant_summary.txt.gz (GRCh38 rows, single-gene missense from Name p.XxxNNNYyy), review status >= 1 star, P/LP vs B/LB (conflicting and VUS excluded).
- Scores: AF-<acc>-F1-aa-substitutions.csv (AM), AF-<acc>-F1-confidence_v6.json (pLDDT). The reference residue must match the ClinVar protein change, otherwise the variant is dropped.
- Circularity guard: AM was released 2023-09-19 and never trained on ClinVar labels. If ClinVar provides a creation date, primary analysis = variants created on or after 2023-09-19, provided >= 300 P/LP and >= 300 B/LB. Otherwise all variants, with the limitation stated.

## Gates
G1 AUROC(high-study tier) - AUROC(low-study tier) >= 0.03, gene-level bootstrap (1000) 95% CI excludes 0.
G2 Restricted to residues with pLDDT >= 70, the difference is >= 0.02 with CI excluding 0 (the gap is not just disorder).
Reported, not gated: per-tier fraction of P/LP sites with pLDDT < 70; AM calibration (fraction of P/LP called "likely_pathogenic") per tier.
Failure policy: negative preserved (a null gap is itself useful - AM equally reliable across study density); pivots appended with new locked gates.

## Primary result (22:33) - FAIL, preserved (a useful null)
No creation date in variant_summary, so all variants were used (circularity limitation applies). 554 genes, 16,159 scored missense variants. AUROC: low-study 0.943, mid 0.951, high 0.956. G1 diff 0.013 (CI -0.007 to 0.032), fail. G2 (pLDDT >= 70) diff -0.009 (CI -0.033 to 0.015), fail. AlphaMissense is about equally reliable on poorly and well-studied rare-disease genes. False "likely pathogenic" on B/LB is 8-9% in every tier.

## Pivot 1 (locked 22:34, before computation): where does AM miss pathogenic variants?
Unit: P/LP variants. Sensitivity = fraction with am_class == LPath.
P1-G1 sensitivity(pLDDT < 70) <= sensitivity(pLDDT >= 70) - 0.15, gene-level bootstrap 95% CI of the gap excluding 0.
P1-G2 the gap is >= 0.10 within BOTH the low- and high-study tiers separately.
Reported: specificity by pLDDT band (B/LB called LBen); variant share by band.

## Pivot 1 result (22:35) - FAIL, preserved
Overall sensitivity gap (pLDDT >= 70 vs < 70) 0.057, CI -0.019 to 0.265 (fail). High-study tier 0.007 (fail). Low-study tier 0.26 (CI 0.07-0.56, n = 94 low-pLDDT variants), which is a post-hoc subgroup, recorded only as a hypothesis for a future locked test.
Closing: topic closed as a documented boundary (primary + pivot fail); no further pivots on this data.
