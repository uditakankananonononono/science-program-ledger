# algo50/44 - Mendelian randomization: IVW vs MR-Egger under directional pleiotropy

Lane RES-3. Algorithm study. Protocol hashed before scoring (`results/lock.txt`).

## Bottom line
- With no pleiotropy, IVW is unbiased (-0.003 on a true effect of 0.3).
- Directional pleiotropy (alpha ~ U(0, 0.04)) inflates IVW by +0.141, i.e. it reports ~0.44 instead of 0.3.
- MR-Egger removes the bias (-0.010) but its spread is 2.9x wider (SD 0.101 vs 0.035): a real precision price.

## Results (results/results.json, J=30 variants, 1000 replicates)
| scenario | IVW bias | IVW SD | Egger bias | Egger SD |
|---|---|---|---|---|
| NONE | -0.003 | 0.028 | -0.014 | 0.089 |
| DIR | +0.141 | 0.035 | -0.010 | 0.101 |

## Gates
| gate | rule | value | verdict |
|---|---|---|---|
| G1 | NONE abs IVW bias <= 0.03 | 0.003 | PASS |
| G2 | DIR IVW bias >= 0.10 | 0.141 | PASS |
| G3 | DIR abs Egger bias <= 0.05 | 0.010 | PASS |
| G4 | DIR Egger SD >= 2x IVW SD | 2.9x | PASS |
Project PASSES (all gates). Reproduction of known MR behaviour.

## Caveats
- InSIDE holds by construction; that is exactly the case Egger is built for. Correlated pleiotropy would bias Egger too (not tested).
- Weak-instrument bias is small here (bx >> SE); with weaker instruments Egger's dilution gets worse.
- Median / mode-based estimators not compared.

## Reproduce
`python3 code/run.py` (numpy; ~2 s).
