# algo50/54 - Early epidemic growth rate: log-linear regression vs Poisson GLM on low counts

Lane RES-3. Algorithm study. Protocol hashed before scoring (`results/lock.txt`).

## Bottom line
- Starting from ~2 cases/day, the common log(cases+1) regression underestimates a 10%/day growth rate by 0.008 (reports ~9.2%/day). That is a real bias but it missed the locked 0.01 threshold, so the primary gate fails narrowly.
- A Poisson GLM is unbiased (+0.0003) and has 33% lower RMSE (0.0075 vs 0.0111).
- At ~50 cases/day both are essentially unbiased; the problem is a low-count problem.

## Results (results/results.json, 30 days, 2000 replicates, true r=0.10)
| start | LOGLIN bias | LOGLIN RMSE | POISGLM bias | POISGLM RMSE |
|---|---|---|---|---|
| c0=2 | -0.0079 | 0.0111 | +0.0003 | 0.0075 |
| c0=50 | -0.0003 | 0.0019 | +0.000003 | 0.0015 |

## Gates
| gate | rule | value | verdict |
|---|---|---|---|
| G1 | c0=2 abs LOGLIN bias >= 0.01 | 0.0079 | FAIL (narrow) |
| G2 | c0=2 abs POISGLM bias <= 0.005 | 0.0003 | PASS |
| G3 | c0=2 POISGLM RMSE <= 0.8x LOGLIN | 0.67x | PASS |
| G4 | c0=50 abs LOGLIN bias <= 0.005 | 0.0003 | PASS |
Project FAILS its primary gate (G1) as locked. Honest read: the log-linear bias exists and the GLM is clearly better on error, but the bias is smaller than we pre-registered.

## Caveats
- Pure Poisson noise; real case counts are overdispersed (negative binomial), weekday-seasonal and reporting-delayed. Overdispersion would likely enlarge the log-linear bias; not tested.
- Doubling-time error from -0.008 in r: ~6.9 vs ~7.5 days.
- One unused initialization line in code/run.py is overwritten immediately and has no effect.

## Reproduce
`python3 code/run.py` (numpy; ~10 s).
