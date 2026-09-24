# 151F - order-pair rules for cross-lab cfDNA 5hmC (follow-up to 151): BOUNDARY, clean negative (not counted)

Gates were locked before results (commit fa9ecd89).

| model | train CV | external GSE81314 |
|---|---|---|
| k-TSP, k=7 (primary) | 0.77 | 0.61 |
| label-free anchor alignment + elastic-net (secondary) | - | 0.64 |
| one gene SNCAIP (151 baseline) | - | 0.73 |

- G1 FAIL: 0.61 is below 0.80. The difference vs one gene is -0.12 (bootstrap 95% CI -0.32 to +0.09).
- G2 PASS: in-lab CV 0.77.
- G3 FAIL: none of the 14 pair genes overlap 158's hepatocyte axis.
- G4: no nomination, since the rule does not transport.

## Mechanism
- Pair orderings are immune to per-sample scaling. They still lose, so the lab shift between Li 2017 and Song 2017 is not a sample-level scale factor.
- It is gene-specific: some genes' 5hmC gene-body signal sits systematically higher or lower in one protocol. That flips the within-sample order of exactly the gene pairs a classifier learns.
- Label-free median centering (0.64) does not remove it either, because the shift interacts with the cancer-type mix, which differs between cohorts.
- The only thing that survived, one gene (0.73), has a wide CI and may be partly luck with 15 external controls.
- Conclusion: for cfDNA 5hmC, cross-lab transport needs either matched-protocol cohorts or explicit per-gene protocol calibration on shared reference samples. Neither is public. The 151 boundary is confirmed as a data limit rather than a model limit.

This is the one place in the lane where order rules did not transport (contrast FINDINGS section 7, 157F). Order rules fix per-sample and platform scaling, not gene-specific protocol bias.

## Reproduce
code/run.py uses 151's data (checksums in 151/data/SHA256SUMS).
