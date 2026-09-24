# DOC-2-058 A cross-cancer liquid-biopsy grammar - GATES (locked 2026-09-24 11:20 IST, before any 058 analysis; the same cohorts were used in exp200/151, disclosed)

## Question
Is there a shared "cancer-ness" component in plasma cfDNA 5hmC that detects a cancer type never seen in training? Factorized design: a shared axis learned across types.

## Data
GSE89570 plasma, 5 cancer types (colon 78, stomach 62, thyroid 46, pancreas 34, liver 25) plus 96 healthy.

## Design (leave-one-cancer-out, LOCO)
- For each held-out type T: healthy split 80/20 (seed 0). Train on the other 4 types plus 80% of healthy. Test T vs the held-out 20% of healthy.
- Features: within-sample ranks, 2,000 most variable genes in each training fold.

## Models
- F (factorized "shared axis"): per training type, the vector of mean-rank differences vs healthy. Shared axis = the gene-wise MEDIAN of these per-type vectors, keeping the 200 genes with largest |median|. Score = signed mean rank over those genes. Genes are kept only if same-sign in >= 3 of 4 training types.
- B1: pooled elastic-net logistic (Li et al. 2017 approach), cancer vs healthy, C by 3-fold CV.
- B2: best single gene in training.

## Gates
- G1: mean LOCO AUROC of F over the 5 held-out types >= 0.75.
- G2: F mean minus max(B1, B2) mean >= 0.03, AND F >= B1 in at least 4 of 5 held-out types.

## Reported
- Frozen transfer of F (trained on all 5 types) to GSE81314, where 4 of 7 cancer types were never seen (lung, breast, GBM, HBV-context).
- Mechanism: whether shared-axis genes are immune/neutrophil (systemic host response) or tissue genes.
- Nomination: top shared-axis gene.

## Pivot rule
Negatives are kept; amend and lock before new results.
