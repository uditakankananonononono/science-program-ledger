# algo50/43 - CRISPR guide efficiency: boosted trees vs Rule Set 1-style linear model

Lane RES-1. Adopted from the killed lane (claimed 2026-09-24T00:31Z, nothing pushed). Protocol hashed and timestamped before any model was run (`results/lock.txt`).

## Bottom line
- All four pre-declared gates passed.
- On Doench 2014 (2,144 guides, 9 genes, leave-one-gene-out), a fixed-hyperparameter histogram gradient-boosting model on a compact feature set (M1) reaches mean Spearman **0.468** vs **0.293** for a Rule Set 1-style ridge and 0.097 for GC content alone.
- The gain is model class, not features: ridge on the same extended features gets 0.300 (diagnostic, not gated) - the extra features add ~0.007 to a linear model, boosting adds ~0.17.
- Transfer to Doench 2016 (4,195 guides, 15 genes, different assays, no refit): M1 **0.352** vs B1 0.314 overall; M1 >= B1 on 14 of 15 genes.
- Practical selection (G4): 53% of M1's predicted top-decile guides truly sit in the gene's top activity quartile (chance 25%, gate 50%).

## Data
- Train/dev: Doench 2014 (`V1_suppl_data.txt`, github.com/MicrosoftResearch/Azimuth `azimuth/data/`; sha256 + retrieval time in `data/`, raw not committed - `code/prep.py` re-downloads). Human CD13/CD15/CD33, mouse CD45/CD43/CD5/CD28/H2-K/THY1; label `Activity`, within-gene `Percent Rank`.
- Transfer: Doench 2016 (`V2_data.xlsx`, sheet `Results`), label `sgRNA Score`, 134 low-flag guides dropped. V2's context string is 30 nt (NNNN[20]NGGNNN) vs V1's 34; V2 is right-padded with N to 34 so one feature builder serves both (padding lands outside the spacer+PAM, positions 30-33 are all-zero indicators for V2).

## Methods
Features (all from the context string + annotation columns): position-specific mono- (34x4) and dinucleotides (33x16), position-independent dinucleotide counts over the spacer, GC overall/distal-5/proximal-5, Wallace Tm of the spacer and its 5'/3' thirds, amino acid cut position, percent peptide. M1 adds GG-dinucleotide position indicators and longest homopolymer run. B0 = spacer GC count only. B1 = ridge on the RS1-style set, alpha from {0.1,1,10,100} by inner leave-one-gene-out on training genes only. M1 = HistGradientBoostingRegressor (max_iter 300, lr 0.06, 31 leaves, min_samples_leaf 20, L2 1.0, fixed before results). Per-fold median imputation and standardization fit on training genes only.

## Results
Leave-one-gene-out (V1), mean Spearman: B0 0.097, B1 0.293, M1 0.468.

| Gene | B0 | B1 | M1 |
|---|---|---|---|
| CD13 | 0.077 | 0.322 | 0.431 |
| CD15 | 0.402 | 0.303 | 0.228 |
| CD28 | 0.104 | 0.425 | 0.412 |
| CD33 | -0.075 | 0.226 | 0.610 |
| CD43 | 0.162 | 0.338 | 0.706 |
| CD45 | -0.066 | 0.358 | 0.535 |
| CD5 | 0.149 | 0.334 | 0.496 |
| H2-K | -0.043 | -0.009 | 0.350 |
| THY1 | 0.166 | 0.341 | 0.443 |

Transfer to V2 (train on all V1, no refit), Spearman: B1 0.314, M1 0.352.

| V2 gene | n | B1 | M1 |
|---|---|---|---|
| CCDC101 | 149 | 0.496 | 0.423 |
| CDK6 | 121 | 0.376 | 0.362 |
| CLDN10 | 71 | 0.368 | 0.535 |
| CUL3 | 154 | 0.350 | 0.378 |
| HPRT1 | 64 | 0.209 | 0.382 |
| MED12 | 924 | 0.343 | 0.397 |
| MLH1 | 255 | 0.362 | 0.402 |
| MSH2 | 218 | 0.363 | 0.401 |
| MSH6 | 419 | 0.400 | 0.356 |
| NF1 | 736 | 0.287 | 0.339 |
| NF2 | 223 | 0.478 | 0.473 |
| PMS2 | 248 | 0.404 | 0.461 |
| TADA1 | 109 | 0.542 | 0.445 |
| TADA2B | 190 | 0.544 | 0.457 |
| TOP2A | 314 | 0.231 | 0.348 |

Gate outcomes: G1 PASS (+0.175 >= 0.02), G2 PASS (+0.196 >= 0.05), G3 PASS (M1 0.352 >= 0.25 and >= B1 - 0.01), G4 PASS (0.530 >= 0.50).

Full numbers: `results/results.json`, `results/diagnostic.json`, `results/logo_predictions.csv`. Figure: `results/fig_logo_transfer.png`.

## Caveats
- This is a reproduction of the known Azimuth direction (boosting > linear for guide activity), not a new SOTA; the point was a from-scratch pipeline with pre-declared gates and a clean transfer test.
- V1 mixes human and mouse genes; transfer target V2 is human. No species-split gate was declared, so the species confound is unquantified here.
- V2 `sgRNA Score` is a combined score across three drug-survival assays, not the same readout as V1 `Activity`; Spearman transfer is the honest metric for that.
- GC-only B0 is deliberately trivial; the real baseline is B1.

## Next steps
Position-specific trinucleotides with grouped regularization; thermodynamic features (ViennaRNA) as an amendment; transfer to Chari 2015 and CRISPRon; per-species splits.

## Reproduce
`python3 code/prep.py && PYTHONPATH=code python3 code/run.py && PYTHONPATH=code python3 code/diagnostic.py && PYTHONPATH=code python3 code/figure.py` (needs numpy, scipy, pandas, scikit-learn, matplotlib, openpyxl).
