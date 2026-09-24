# DOC-2-057 Negative-space biomarkers: broken gene couplings in quiescent UC (exp200/157)

**Outcome: documented boundary, not counted.**

## Experiment
- Built a score from gene-gene couplings that hold in healthy colon (5,229 pairs, Spearman >= 0.8) and break in UC (GSE87466).
- Tested it frozen on mucosa with no visible inflammation in two external cohorts.
- Compared with k-TSP (Tan 2005), an L1 model and the best single gene.

| cohort | broken couplings | k-TSP | L1 | 1 gene |
|---|---|---|---|---|
| GSE38713 (15 UC vs 13 controls) | **0.84** | 0.76 | 0.79 | 0.79 |
| GSE9452 (13 UC vs 5 controls) | 0.46 | **0.78** | 0.68 | 0.54 |

## Takeaway
- Coupling breaks are strong in training (0.98, permutation p=0.005) and are the best detector in one external cohort. They collapse to chance in the other, which has only 5 controls.
- The pairwise-order baseline (k-TSP) is the most stable across cohorts. Relative-order rules seem more robust to cohort shift than residual-from-regression rules.
- Top broken pairs involve metabolic and epithelial genes (ACSF2 in 6 of the top 15, CLDN8, HNF4G, SLC38A4) and CCL2. This is consistent with loss of epithelial metabolic programs in UC, but it is not validated.

## Limits
- Tiny external control groups.
- GPL570 mapped with the GPL96 annotation.
- The external cohorts were also used in exp200/156 (disclosed in the gates).
