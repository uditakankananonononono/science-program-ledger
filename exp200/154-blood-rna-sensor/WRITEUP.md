# DOC-2-054 Blood RNA as a systemic state sensor: bacterial vs viral (exp200/154)

**Outcome: documented boundary, not counted. The trained classifier transfers well to three independent cohorts, but it does not beat the published Sweeney 7-gene score. Both locked "beat the baseline" gates failed.**

## Experiment
- Training: an L1 logistic classifier on within-sample gene ranks, trained only on adult emergency-department whole blood (GSE63990, Tsalik 2016; 5-fold CV AUROC 0.94). It selected 27 genes.
- Testing: the model was frozen and applied to three independent pediatric cohorts on different platforms.

| cohort | n bacterial / viral | trained model | Herberg 2016 (2-gene) | Sweeney 2016 (7-gene) |
|---|---|---|---|---|
| GSE42026, Illumina | 18 / 41 | 0.855 | 0.870 | **0.912** |
| GSE40396, Illumina | 8 / 35 | **0.896** | 0.857 | 0.893 |
| GSE6269, PBMC, Affy (fresh, pivot) | 91 / 25 | 0.914 | n/a* | **0.922** |

\*FAM89A is not on U133A.

- Primary gate: pooled difference vs Sweeney -0.036 (CI -0.086 to +0.009). Fail.
- Pivot: I averaged the model with Sweeney, locked the method and tested it only on the untouched GSE6269. AUROC 0.931, +0.009 over Sweeney (CI -0.018 to +0.035). Fail.

## What it shows
- A genome-wide model trained on adults generalizes to children, to other platforms and even to PBMCs (0.86-0.91). That is a real result, but it adds nothing measurable over a published 7-gene score.
- Cohorts this size (8-91 bacterial cases) cannot resolve a gain of about 0.01 in AUROC. Beating these signatures would need a pooled multi-cohort benchmark such as Sweeney's own meta-analysis.
- Biology: the viral side of the model is interferon-stimulated genes (IFI27, IFI44L, IFIT1, XAF1, LAMP3), which matches the known antiviral interferon response. The bacterial side includes ITGA7, OLAH, VNN1, HPGD and TMEM165. IFI27 and IFI44L also appear in both published signatures, so the model rediscovered their core.
- Candidate added target (not validated): ITGA7, the top bacterial-side weight and in neither published signature. It would be a qPCR addition to test in a febrile-infant cohort.

## Limits
- Microarrays only.
- GSE42026 overlaps with Herberg's validation data.
- GSE6269 is PBMC rather than whole blood, and its GPL570 probes were mapped with the GPL96 annotation.

## Reproduce
code/run.py (primary) and code/pivot1.py. GEO series matrices and annotations are listed in data/SHA256SUMS.
