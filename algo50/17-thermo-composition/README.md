# algo50/17 - Predicting a microbe's optimal growth temperature from proteome composition: IVYWREL vs a learned 20-amino-acid model

Protocol and gates locked before any proteome composition was computed (PROTOCOL.md, results/lock.txt; Amendment 1 was a crash fix before any score existed). Data: TEMPURA growth temperatures + UniProt reference proteomes (release in results/composition.tsv). 240 organisms, one per genus (120 with Topt >= 50 C, 120 below), 147 families; 5-fold CV holding out whole families.

## Results (results/metrics.json, results/predictions.tsv)
| model | MAE (C) | Pearson r |
|---|---|---|
| B: IVYWREL line (Zeldovich 2007), refit per fold | 6.52 | 0.891 |
| L: ridge on 20 amino-acid fractions | 5.52 | 0.925 |

## Gates
- G1 PASS (just): MAE improves by 1.01 C (95% CI 0.38 to 1.58). The gate needed >= 1.0 with CI above 0, so the point estimate clears it by 0.005 C. The CI supports a real gain, but its size is uncertain.
- G2 PASS: r = 0.925 (needed 0.85).
- G3 FAIL: trained on Bacteria only and tested on 32 Archaea, the learned model is worse (MAE 12.3 vs 9.5 C). The 7-letter IVYWREL signal transfers across domains better than the full 20-letter fit.

## What this means
Within Bacteria-dominated data, using all 20 amino acids beats the classic IVYWREL predictor by about 1 C MAE, even with whole families held out. But the extra signal is partly domain-specific: it does not carry from Bacteria to Archaea, where the simpler IVYWREL rule holds up better. So use the 20-letter model inside a domain and IVYWREL for cross-domain transfer.

## Caveats
- G1 passed by a hair on the point estimate; a different seed or sample could land either side of 1.0 C.
- OGT labels come from literature compilations (TEMPURA Topt_ave), and some are coarse.
- Proteome composition counts every UniProt entry in the reference proteome, including fragments.

## Reproduce
cd code && python3 select.py && python3 compose.py (downloads ~240 proteomes, ~10 min) && python3 model.py
