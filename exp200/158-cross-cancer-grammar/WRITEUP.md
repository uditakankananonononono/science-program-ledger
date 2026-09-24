# DOC-2-058 Cross-cancer liquid-biopsy grammar: is there a shared cancer axis in cfDNA 5hmC? (exp200/158)

**Outcome: documented boundary, not counted.**

## Experiment
Leave-one-cancer-out on GSE89570 plasma cfDNA 5hmC (5 cancer types, 96 healthy): learn a shared "cancer-ness" axis from 4 types (consensus direction of per-type shifts), then detect the unseen 5th type. Baselines: pooled elastic-net (Li 2017 approach) and best single gene.

| held-out type | shared axis | elastic-net | 1 gene |
|---|---|---|---|
| colon | 0.72 | 0.84 | 0.70 |
| stomach | 0.84 | 0.88 | 0.88 |
| thyroid | 0.44 | 0.33 | 0.43 |
| pancreas | 0.59 | 0.56 | 0.49 |
| liver | 0.65 | 0.67 | 0.64 |
| mean | 0.65 | 0.65 | 0.63 |

Transfer of the shared axis to another lab (GSE81314): 0.56.

## Finding
- The shared axis is mostly liver: its top genes are hepatocyte genes (PROX1, HNF4G, PLG, PAH, NR1H4, LPA, CFH, C6, AGXT2, IGF1).
- The common "cancer" signal in these plasma samples looks like more liver-derived cfDNA (systemic or hepatic response), not a tumor-intrinsic grammar.
- That explains why GI cancers transfer to each other while thyroid cancer is at or below chance for every method.

## Limits
- One lab for LOCO.
- 19 held-out healthy per fold.
- Processed gene-body counts only.
