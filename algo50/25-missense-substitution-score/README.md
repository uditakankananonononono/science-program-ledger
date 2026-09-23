# algo50/25 - How much does the amino-acid swap alone say about missense pathogenicity? BLOSUM62/PAM250 vs a ClinVar-learned substitution score

Protocol and gates locked before scoring (PROTOCOL.md, results/lock.txt). ClinVar (release file dated 2026-09-14): 199,671 GRCh38 missense SNVs with assertion criteria, 60,482 P/LP vs 139,189 B/LB, 15,493 genes. 5-fold CV holding out whole genes.

## Results (results/metrics.json; per-variant scores in results/scores.tsv.gz)
| score | AUROC, all (>= 1 star) | AUROC, >= 2 stars (63,812 variants) |
|---|---|---|
| PAM250 (Dayhoff 1978) | 0.654 | 0.628 |
| BLOSUM62 (Henikoff 1992) | 0.683 | 0.663 |
| Learned swap score (420 one-hot features, gene-held-out) | 0.757 | 0.717 |

## Gates
- G1 PASS: +0.073 AUROC over BLOSUM62 (95% CI 0.069 to 0.078).
- G2 PASS: +0.103 over PAM250 (CI 0.098 to 0.108).
- G3 PASS: on the stricter >= 2-star labels, +0.054 over BLOSUM62 (CI 0.047 to 0.061).

## What the learned score picks up (descriptive, from out-of-fold scores)
Most benign-looking swaps: V>I, I>V, S>G, T>S, S>A (2.6-9% pathogenic). Most damaging: C>W, W>G, W>C, W>S, C>F (81-85% pathogenic). Losing or gaining Trp or Cys dominates, which alignment matrices under-weight because they were built for evolutionary similarity, not clinical harm.

## What this means
The swap alone carries real signal (AUROC ~0.76), and a matrix learned from clinical labels beats matrices built for sequence alignment by 7-10 points, even on genes the model never saw and on the stricter labels. It is still far from full predictors that add conservation and structure (often quoted above 0.9). The practical point: if you must score by substitution alone, don't use BLOSUM62.

## Caveats
- Circularity risk: ClinVar submitters often use in-silico evidence (ACMG PP3/BP4) when classifying, which can bake substitution severity into the labels. The gene-held-out split does not remove this. The 2-star check reduces but does not remove it.
- P/LP and B/LB variants come from different gene mixes and ascertainment. Holding out genes guards against the model memorizing genes, not against ascertainment bias.
- The 'Likely' classes are merged with the definite ones.

## Reproduce
Download the URL in data/source_url.txt into data/ and check the sha256, then cd code && python3 extract.py && python3 run.py (~6 min; the bootstrap dominates)
