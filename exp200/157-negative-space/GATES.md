# DOC-2-057 Biomarker discovery by negative space - GATES (locked 2026-09-24 10:50 IST; before any coupling analysis)

## Question
Can broken gene-gene couplings (relationships present in healthy colon and lost in disease) detect UC in mucosa that looks normal (remission or non-involved)? Compared with pairwise and single-marker baselines.

## Data (same cohorts as exp200/156; disclosed: baseline B2/B3 external values were already seen in 156)
- Train: GSE87466 (87 UC vs 21 normal; GPL13158).
- Frozen external E1: GSE38713, non-inflamed UC (8 remission + 7 non-involved) vs 13 controls.
- Frozen external E2: GSE9452, 13 non-inflamed UC vs 5 controls.
- GPL570 probes mapped with the GPL96 annotation; genes kept only if shared by all sets; max-mean probe per gene; within-sample ranks.

## Model N (negative space), training data only
- Genes: the 1,000 most variable in training.
- Couplings: gene pairs with Spearman |r| >= 0.8 in the 21 normals. Each pair gets a linear fit (y on x) in normals; residual SD from normals.
- Per sample and pair: break = |residual| / SD.
- Keep the 100 pairs with the highest training AUROC of break (UC vs normal). N score = mean break over those pairs. There is no other fitting.

## Baselines
- B1: k-TSP (top-scoring pairs; Tan et al., Bioinformatics 2005), k in {1,3,5,7,9} by 5-fold CV on training.
- B2: L1 logistic on ranks (the exp200/156 pivot-2 model, same recipe).
- B3: the best single gene in training (156 found SLC6A14).

## Gates
- G1: N AUROC >= 0.75 on both E1 and E2.
- G2: pooled E1+E2 AUROC (within-cohort percentile) of N minus max(B1,B2,B3) >= 0.03, with 2,000x stratified bootstrap CI lower bound > 0.

## Reported
- Mechanism: which pathways the broken pairs connect (epithelial differentiation / metabolism expected).
- Permutation FDR: label permutation (200x) for the pair-selection AUROC.
- Nomination: the top broken pair, proposed for co-staining in remission biopsies.

## Pivot rule
Negatives are kept; amend and lock before new results.
