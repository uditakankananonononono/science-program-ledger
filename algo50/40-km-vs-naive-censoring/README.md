# algo50/40 - Kaplan-Meier vs naive median survival under censoring

Lane RES-3. Algorithm study. Protocol hashed before scoring (`results/lock.txt`).

## Bottom line
- At 32% censoring, Kaplan-Meier recovers the true median survival essentially without bias (+0.002%), while dropping censored patients underestimates it by 34% and treating censoring as death by 27%.
- At 63% censoring, KM is still within +0.8% (median reached in 96.9% of trials); the naive estimates are off by 54-66%.

## Results (results/results.json, n=200, 1000 replicates, true median 6.931)
| censoring | KM rel. bias | DROP rel. bias | ASDEATH rel. bias | KM median reached |
|---|---|---|---|---|
| 31.6% (Cmax=30) | +0.00002 | -0.339 | -0.266 | 100% |
| 63.2% (Cmax=10) | +0.0077 | -0.662 | -0.544 | 96.9% |

## Gates
| gate | rule | value | verdict |
|---|---|---|---|
| G1 | 30%: abs KM bias <= 0.05 | 0.00002 | PASS |
| G2 | 30%: ASDEATH bias <= -0.15 | -0.266 | PASS |
| G3 | 60%: abs KM bias <= 0.10 and reached >= 90% | 0.0077, 96.9% | PASS |
| G4 | 30%: abs DROP bias >= 0.10 | 0.339 | PASS |
Project PASSES (all gates). Textbook reproduction, useful as a teaching/auditing baseline, not a new method.

## Caveats
- At 63% censoring KM bias is computed only over the 96.9% of trials where the median was reached; that conditioning can hide a small bias.
- Censoring is independent of survival by construction. Informative censoring (sicker patients dropping out) breaks KM too, and is not tested.
- Exponential survival only; no ties, no covariates.

## Reproduce
`python3 code/run.py` (numpy; ~5 s).
