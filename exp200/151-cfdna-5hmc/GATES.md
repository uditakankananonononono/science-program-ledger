# DOC-2-051 Liquid biopsy signal before the tumor is loud - GATES (locked 2026-09-24 10:20 IST; only sample labels and file formats inspected)

## Experiment
Cell-free DNA 5hmC gene-body profiles: is a coordinated multi-gene module signature a better and more transferable cancer detector than one marker or a published-style gene-level model?
- Train: GSE89570 (Li et al., Cell Res 2017) plasma only. Cancer (colon, stomach, pancreas, liver, thyroid; n=245) vs healthy (n=96). Benign excluded.
- Frozen external: GSE81314 (Song et al., Cell Res 2017; different lab and normalization). All cancers (n=49) vs non-cancer (8 healthy + 7 HBV). Input/blood controls excluded.
- Features: within-sample ranks over genes shared by both sets, keeping genes with median count >= 10 in training.

## Models
- M (module model): on training only, cluster the 2,000 most variable genes into 50 co-variation modules (k-means on z-scored ranks, seed 0). Each sample becomes 50 module mean-ranks. L2 logistic, C picked by 5-fold CV.
- B1 (one marker): the single gene with the highest training AUROC.
- B2 (named published approach): elastic-net logistic regression on gene features, the classifier approach of Li et al. 2017 (Cell Res 27:1243), with alpha 0.5 and C by 5-fold CV on the same features.

## Gates
- G1: external AUROC of M >= 0.80.
- G2: external AUROC of M minus max(B1, B2) >= 0.03, with 2,000x stratified bootstrap CI lower bound > 0.

## Reported
- Mechanism: the top-weighted modules are tested for enrichment of liver- or immune-specific genes (tissue-of-origin shedding is expected).
- Tool: code/predict.py.
- Nomination: the top module hub gene, proposed as a targeted 5hmC-qPCR marker.

## Pivot rule
Negatives are kept; amend and lock before new results.

## Amendment A (10:31, before any results were produced)
B2 elastic-net with saga did not converge in reasonable CPU on 15,011 genes. B2 now uses the same 2,000 most-variable training genes as M, with saga tol 1e-3 and max_iter 1000. Nothing else changes.

## Primary result (10:32) - G1 FAIL, G2 FAIL, preserved
- Training 5-fold CV AUROC: M 0.76, B2 0.78.
- Frozen external AUROC on GSE81314: M 0.61, B1 (SNCAIP, one gene) 0.73, B2 elastic-net 0.64.
- Difference vs B1: -0.12 (CI -0.27 to +0.04).
Closed as a documented boundary. Cross-lab transfer of cfDNA 5hmC gene-body signatures fails in this setting.
