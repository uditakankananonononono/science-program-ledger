# 154F - follow-up to 154 (DOC-2-054): pooled multi-cohort bacterial-vs-viral blood classifier vs Sweeney
Approved by the parent (11:17) as a fresh attack on 154's failure. Locked 2026-09-24 ~12:27 IST, before any model fitting.
Failure being attacked: single-cohort training plus small externals could not resolve gains of about 0.01, and the adult-only training set limited what the model could learn.

## Cohorts (6; GEO; checksums in data/SHA256SUMS)
| cohort | platform | population | bacterial vs viral |
|---|---|---|---|
| GSE63990 | GPL571 | adult ED | as in 154 |
| GSE42026 | GPL6947 | pediatric | as in 154 |
| GSE40396 | GPL10558 | pediatric | as in 154 |
| GSE6269 | GPL96, PBMC | pediatric | S. pneumoniae / S. aureus / E. coli vs influenza |
| GSE60244 (NEW) | GPL10558 | adult LRTI | BACTERIA 22 vs VIRUS 71; coinfection and controls excluded |
| GSE68004 (NEW) | GPL10558 | pediatric | GAS + GAS/SF 17 vs HAdV 19; Kawasaki and healthy excluded |

## Method (fixed)
- Leave-one-cohort-out (LOCO): train on 5 cohorts, test on the 6th.
- Features: within-sample percentile ranks over genes shared by all 6.
- Model: L1 logistic regression, C chosen from {0.03, 0.1, 0.3, 1} by 5-fold CV on the pooled training cohorts.

## Baseline (named, published)
Sweeney et al. 2016 (Sci Transl Med) 7-gene bacterial/viral score: mean z of HK3, TNIP1, GPAA1, CTSB minus mean z of IFI27, JUP, LAX1, computed per cohort (identical to 154).

## Gates
- G1: mean over the 6 held-out cohorts of (model - Sweeney) AUROC >= +0.02, AND the 95% CI lower bound > 0. The CI comes from a stratified bootstrap within cohorts (2,000 resamples).
- G2: the model's held-out AUROC >= 0.85 in >= 5 of 6 cohorts (frozen external per fold).
- G3 (mechanism): the pooled full model's top-20 genes include interferon-stimulated genes on the viral side AND >= 1 neutrophil/bacterial-response gene on the bacterial side, among OLAH, ITGA7, VNN1, HPGD, MMP8, CD177, ANXA3, ARG1, HP, TNIP1, HK3 (host-response literature: Tsalik 2016, Sweeney 2016).
- G4: a scorer CLI plus a nomination (the top bacterial-side gene outside both published signatures).
- PASS = G1-G4. Otherwise a boundary. No change of cohorts, contrasts or C grid after results.
