# algo50/48 - IC50 estimation: four-parameter logistic fit vs linear interpolation

Lane RES-3. Algorithm study. Protocol hashed before scoring (`results/lock.txt`, includes amendment A hash).

## Bottom line (mostly negative, surprising direction)
- The expected "4PL fit beats eyeball interpolation" did NOT hold for shallow curves. At Hill slope 1, simple log-dose interpolation had lower median error than a free 4PL fit (0.041 vs 0.057 log10 units on-grid; 0.048 vs 0.067 with IC50 placed off-grid in amendment A).
- For steep curves (Hill 3) with IC50 off-grid, 4PL edges ahead (0.035 vs 0.039).
- Both methods are within ~15% of the true IC50 on the dose scale in the median case at this noise level, so the practical gap is small.

## Results
Original (results/results.json, IC50 fixed at 1, symmetric grid):
| Hill | INTERP median err | FOURPL median err | 4PL converged |
|---|---|---|---|
| 1 | 0.041 | 0.057 | 100% |
| 3 | 0.016 | 0.037 | 100% |

Amendment A (results/results_pivot_a.json, log10 IC50 ~ U(-1,1)):
| Hill | INTERP median err | FOURPL median err | 4PL converged |
|---|---|---|---|
| 1 | 0.048 | 0.067 | 100% |
| 3 | 0.039 | 0.035 | 100% |

## Gates
| gate | rule | value | verdict |
|---|---|---|---|
| G1 | h=1 FOURPL <= 0.8x INTERP | 0.057 vs 0.041 | FAIL |
| G2 | 4PL converged >= 95% | 100% | PASS |
| G3 | h=3 FOURPL <= INTERP | 0.037 vs 0.016 | FAIL |
| G4 | h=1 FOURPL err <= 0.10 | 0.057 | PASS |
| P1 | off-grid h=1 FOURPL <= 0.8x INTERP | 0.067 vs 0.048 | FAIL |
| P2 | off-grid h=3 FOURPL <= INTERP | 0.035 vs 0.039 | PASS |
| P3 | 4PL converged >= 95% | 100% | PASS |
Project FAILS its primary hypothesis (G1, P1). Documented negative.

## Caveats
- The original grid was symmetric around the true IC50, a best case for interpolation; amendment A fixed that and interpolation still won at h=1.
- Likely reason (not tested): a free 4PL spends degrees of freedom on top/bottom plateaus with only 8 doses and SD-8 noise. A 4PL with fixed 0/100 plateaus (normalized data) would likely win; that needs a new amendment.
- Median error only; 4PL gives a confidence interval and interpolation does not, which this study does not score.

## Reproduce
`python3 code/run.py` then `python3 code/pivot_a.py` (numpy, scipy; ~10 s each).
