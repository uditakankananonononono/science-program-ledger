# P1 preregistration (locked before any test-split evaluation)
Data: UCI17 WDBC zip sha256 bc154869ef13f753f9e2b5a17e248cfe1ba4b6721db7c4da9f4880e40b05d3af (569 rows, 30 features, CC BY 4.0).
Problem: selective diagnosis; accept/abstain with bounded malignant-miss among accepted cases.
Base model (both arms identical): StandardScaler + LogisticRegression(C=1.0, lbfgs, max_iter=2000) fit on train; score s=P(malignant).
Baseline (Chow-style symmetric rule): accept if max(s,1-s)>=tau; tau chosen on calibration.
New method RCAB (risk-controlled asymmetric band): accept malignant if s>=t_hi, accept benign if s<=t_lo, else abstain; (t_lo,t_hi) chosen on calibration to maximise coverage subject to Clopper-Pearson upper bound (conf 0.90) on malignant-miss rate among accepted-benign <= delta AND benign-false-alarm rate among accepted-malignant <= delta. Same constraint and same bound used for the baseline's tau (applied to its accepted set). Grid: thresholds from calibration score quantiles.
Protocol: 100 repeats, seed r=0..99, stratified 60/20/20 train/cal/test via numpy RandomState(r) permutation within class. delta=0.02 primary; delta=0.05 secondary.
Primary metric: paired per-repeat difference in test coverage (RCAB - Chow). Also report realized test miss rate of accepted-benign for both arms and the fraction of repeats violating delta.
WIN: mean diff >= +0.02 AND 95% bootstrap CI (10000 resamples, seed 7) lower bound > 0 AND RCAB violation fraction <= 0.15.
NEGATIVE: CI upper bound < 0 -> baseline better. Otherwise NULL. All reported verbatim, no re-banding.
Audit: effect-size and per-repeat sign counts reported. Equivalence check: with t_lo=1-t_hi forced, RCAB must reproduce Chow coverage exactly (assert before running).

## Amendment A1 (after v1 run, before any v2 run)
v1 result (results_v1_degenerate.json, commit 23499e8): ALL 200 comparisons NULL with diff exactly 0 at delta 0.02 and 0.05. Diagnosis: the 0.90 Clopper-Pearson bound with 0 errors needs n>=ceil(ln(0.1)/ln(1-delta)) accepted per side (n>=114 at 0.02, n>=45 at 0.05); the calibration set has ~43 benign cases, so no threshold pair was feasible, both arms abstained on everything (coverage 0). This is a design defect in delta choice, not evidence about the methods. v1 is reported as a degenerate NULL.
Change: deltas become 0.10 (primary) and 0.20 (secondary), all else identical (same splits, bound, bands, WIN rule with mean diff >=+0.02). Mean coverage of each arm is additionally reported to rule out degeneracy.
