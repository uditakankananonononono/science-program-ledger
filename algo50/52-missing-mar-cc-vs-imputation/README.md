# algo50/52 - Missing clinical data under MAR: complete-case vs mean vs regression imputation vs IPW

Lane RES-3. Algorithm study. Protocol hashed before scoring (`results/lock.txt`).

## Bottom line
- With 41% of a lab value missing, more often in patients with high covariate x, the complete-case mean is off by -0.35 SD. Mean imputation has the same bias and also shrinks the SD by 30% (0.70 vs 1.0).
- Regression imputation from x removes the mean bias (+0.002) but still understates the SD (0.92).
- Inverse-probability weighting fixes both mean (-0.001) and SD (0.99).

## Results (results/results.json, n=500, 2000 replicates, true mean 1, true SD 1)
| method | mean bias | mean SD estimate |
|---|---|---|
| CC | -0.350 | 0.911 |
| MEANIMP | -0.350 | 0.697 |
| REGIMP | +0.002 | 0.922 |
| IPW | -0.001 | 0.991 |

## Gates
| gate | rule | value | verdict |
|---|---|---|---|
| G1 | abs CC bias >= 0.20 | 0.350 | PASS |
| G2 | abs REGIMP bias <= 0.03 | 0.002 | PASS |
| G3 | MEANIMP SD <= 0.80 | 0.697 | PASS |
| G4 | abs IPW bias <= 0.05 | 0.001 | PASS |
Project PASSES (all gates). Reproduction of standard missing-data theory.

## Caveats
- Missingness is MAR given x and the models are correctly specified (linear y~x, logistic missingness). Under MNAR (missing depends on y itself), all four methods are biased; not tested.
- Multiple imputation with proper variance was not run; single regression imputation understates uncertainty.

## Reproduce
`python3 code/run.py` (numpy; ~10 s).
