# DOC-1-006 GATES v2 — locked 2026-09-24 ~00:26 IST, BEFORE v2 results.
# Trigger: G1 FAILED (discovery repeated-CV AUROC 0.552 +/- 0.097, obs 0.530,
# permutation p=0.42 vs 200 full-pipeline nulls). Documented negative preserved.
# Pre-registered pivot (GATES.md failure clause): DL arm on the SAME frozen 24 features.
# - Model: sklearn MLPClassifier (hidden (16,), alpha=1.0 - strong regularization for
#   n=22, max_iter 2000, random_state frozen), StandardScaler fit inside each fold.
# - Same gates: 20x repeated 5-fold CV mean AUROC >= 0.70 AND observed exceeding ALL
#   200 full-pipeline permutation nulls.
# - If v2 also fails: documented boundary for this design (patient-level marker
#   aggregates do not predict 3-month PET/CT response in GSE151511); the honest-negative
#   finding (published memory-correlates are not recoverable as simple aggregates at
#   n=22) goes in the writeup with the external-cohort clause unexecuted (no panel to
#   transport). No further fishing on this dataset pair.
