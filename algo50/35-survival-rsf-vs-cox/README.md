# 35 - Random survival forest vs Cox PH on five public cohorts (headline FAIL; post-hoc pivot PASS)

Cohorts bundled with scikit-survival: GBSG2, WHAS500, FLCHAIN, ACTG320 (aids), VA lung cancer. 5x5 repeated CV (3x5 for flchain). Gates locked before any fit (commit 67b3cca8; Amendment 1 = IBS crash fix, commit 737fea50).

| Gate | Result | Value (95% CI) |
|---|---|---|
| G1 pooled delta C RSF - Cox >= 0.01 | FAIL | -0.0012 (-0.0062, +0.0033) |
| G2 pooled delta IBS (Cox - RSF) > 0 | FAIL | -0.0042 (-0.0055, -0.0028): RSF calibration worse |
| G3 RSF better in >= 4/5 cohorts | FAIL | 2/5 (gbsg2, aids) |

Mean C (Cox / RSF / GBM): gbsg2 0.677/0.692/0.676, whas500 0.768/0.763/0.759, flchain 0.796/0.792/0.798, aids 0.740/0.747/0.722, veterans 0.718/0.698/0.668.

Post-hoc pivot (Amendment 2, locked and pushed before scoring, commit bd099489): rank-average of the same Cox and RSF risk scores in each test fold.
- P1 pooled delta C (ensemble - Cox) >= 0.005: PASS, +0.0066 (0.0041, 0.0091)
- P2 ensemble >= Cox in >= 4/5 cohorts: PASS, 5/5 (gains +0.017, +0.003, +0.002, +0.010, +0.001)

Takeaway: an untuned RSF does not beat Cox on these small clinical cohorts, and its survival curves are less well calibrated. The two models make different errors, so averaging their risk rankings gives a small, consistent gain.

Caveats: the pivot is post hoc. The gain is small (+0.007 C). The bootstrap resamples correlated CV folds, so the CI is optimistic; per-cohort gains in whas500, flchain and veterans are tiny. There is no calibration claim for the ensemble. Forest hyperparameters were defaults, not tuned.
