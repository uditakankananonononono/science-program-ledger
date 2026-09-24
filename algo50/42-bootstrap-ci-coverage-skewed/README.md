# algo50/42 - Bootstrap percentile vs t confidence intervals on skewed biomarker data

Lane RES-3. Algorithm study. Protocol hashed before scoring (`results/lock.txt`).

## Bottom line (documented negative)
- On log-normal data with n=15, the usual t-interval for the mean covers the truth only 83.1% of the time (nominal 95%).
- The percentile bootstrap does NOT fix this: it covers 81.0%, slightly worse, because its intervals are narrower (1.71 vs 1.99).
- Even at n=100 both still sit just under 92% (0.918 / 0.915).

## Results (results/results.json, 2000 replicates, B=999)
| n | T coverage | PCT coverage | T width | PCT width |
|---|---|---|---|---|
| 15 | 0.831 | 0.810 | 1.992 | 1.706 |
| 100 | 0.918 | 0.915 | 0.814 | 0.791 |

## Gates
| gate | rule | value | verdict |
|---|---|---|---|
| G1 | n=15 T coverage <= 0.925 | 0.831 | PASS |
| G2 | n=15 PCT >= T + 0.02 | 0.810 vs 0.831 | FAIL |
| G3 | n=100 both >= 0.92 | 0.918 / 0.915 | FAIL (narrow) |
| G4 | n=15 PCT width <= 1.10x T | 0.86x | PASS |
Project FAILS (G2). The honest takeaway: "just bootstrap it" is not a fix for small skewed samples; the percentile interval inherits the sample's missing right tail.

## Caveats
- Only the naive percentile bootstrap was tested. BCa, bootstrap-t, or a log-scale (Cox) interval are the standard candidates for a fix and were not run in this sprint; they would need a new locked amendment.
- One distribution (LogNormal sigma=1); milder skew would shrink the gap.

## Reproduce
`python3 code/run.py` (numpy, scipy; ~20 s).
