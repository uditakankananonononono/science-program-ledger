# algo50/46 - Wilcoxon rank-sum vs Welch t-test on heavy-tailed assay data

Lane RES-3. Algorithm study. Protocol hashed before scoring (`results/lock.txt`).

## Bottom line
- On heavy-tailed data (t with 3 df), Wilcoxon detects a 0.8 shift 50.0% of the time vs 38.7% for Welch's t-test (+11.3 points).
- On normal data Wilcoxon gives up only 2.6 points (67.0% vs 69.6%).
- Both tests hold their 5% false-positive rate under heavy tails (4.3% / 4.8%).

## Results (results/results.json, n=20 per group, 4000 replicates, alpha 0.05)
| condition | WELCH | WRS |
|---|---|---|
| NORMAL, delta 0.8 (power) | 0.696 | 0.670 |
| T3, delta 0.8 (power) | 0.387 | 0.500 |
| T3, null (type-I) | 0.043 | 0.048 |

## Gates
| gate | rule | value | verdict |
|---|---|---|---|
| G1 | NORMAL WRS >= WELCH - 0.05 | 0.670 vs 0.646 | PASS |
| G2 | T3 WRS >= WELCH + 0.05 | 0.500 vs 0.437 | PASS |
| G3 | T3 null both <= 0.06 | 0.043 / 0.048 | PASS |
| G4 | NORMAL WELCH >= WRS | 0.696 vs 0.670 | PASS |
Project PASSES (all gates). Reproduction of classic efficiency results; practical rule: rank tests are cheap insurance for small n assay data.

## Caveats
- Pure location shift with equal shapes; with unequal variances Wilcoxon tests a different hypothesis.
- Only one heavy-tailed family (t3) and one n.

## Reproduce
`python3 code/run.py` (numpy, scipy; ~3 s).
