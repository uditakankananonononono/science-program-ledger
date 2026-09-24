# 154F - pooled 6-cohort bacterial vs viral classifier vs Sweeney (follow-up to 154): BOUNDARY (not counted)

Gates were locked before fitting (commit a245ee27). Leave-one-cohort-out over 6 cohorts (2 new: GSE60244, GSE68004).

| held-out cohort | pooled L1 model | Sweeney 7-gene |
|---|---|---|
| GSE63990 adult ED | 0.895 | 0.894 |
| GSE42026 pediatric | 0.833 | 0.912 |
| GSE40396 pediatric | 0.886 | 0.893 |
| GSE6269 PBMC | 0.966 | 0.919 |
| GSE60244 adult LRTI (new) | 0.813 | 0.926 |
| GSE68004 GAS vs adenovirus (new) | 0.836 | 0.777 |

- G1 FAIL: mean difference -0.015 (95% CI -0.049 to +0.017).
- G2 FAIL: model >= 0.85 in 3 of 6 cohorts.
- G3 FAIL: interferon genes on the viral side (IFI27, SIGLEC1, OTOF), but none of the pre-listed neutrophil genes on the bacterial side.
- G4: nomination HAMP (hepcidin), the top bacterial-side weight and in neither published signature. Recorded, not validated.

## Mechanism
- Pooling 5 heterogeneous cohorts (4 platforms, PBMC vs whole blood, adult vs child) did not help. CV picked the weakest regularization (C=1) in every fold. The pooled model then filled up with platform-idiosyncratic genes (CACNA1B, KCNJ5, AP3B2, INTS7) alongside the true interferon signal.
- Sweeney's score was itself built by multi-cohort meta-analysis with per-cohort z-scoring, so it already contains the robust cross-cohort part. A generic learner on pooled ranks re-learns noise.
- The model wins where the held-out cohort resembles pooled training (GSE6269 PBMC, GSE68004 GAS). It loses on adult LRTI and one pediatric Illumina cohort.
- Taken with 154, beating a meta-analysis-derived signature needs the same meta-analytic gene selection (effect-size consistency across cohorts), not more samples in a single pooled L1.
- HAMP fits known biology: hepcidin is IL-6-inducible and rises in bacterial infection. It remains only a nomination.

## Data
GEO series matrices for the 6 cohorts plus GPL annotations; checksums in SHA256SUMS. GSE6269 is GPL96 (PBMC).
