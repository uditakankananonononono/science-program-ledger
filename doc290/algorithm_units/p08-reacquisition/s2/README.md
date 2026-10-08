# S2 freeze candidate: corrupted reacquisition

No evaluation seeds run. Two development tests pass at seed 1999 (clean only),
checking reproducibility/counts and unsupported schedule rejection. Evaluation:
20 seeds x five locked scenarios x 80 times, burst gap indices 20-29, first return
30, confirmation 31. Primary position RMSE is causal outputs at 30-39, including
the deferred prediction-only output at 30. No retrospective rewrite of that error.
Actual confirmation delay dt31 retained. Full RMSE, errors at 30/31, gate rejection
indices and deferred decision scores retained. Exact paired losses/ties reported.

Immediate Kalman and a fixed-NIS gate are baselines. The gate checks all observed
measurements; the deferred intervention is only at the one prescribed first return.
These are different policies, not equally tuned thresholds or a posterior-optimal
comparison. NIS threshold is a declared fixed numeric value, not empirical imaging
calibration. Known q/R and matched model favor Gaussian estimators. Maneuver is an
explicit model-mismatch case; corrupted confirmation and both-corrupt are negative
controls. No scientific gate, innovation, realistic imaging or winner rule.

Prior deferred-unit review: PASS-WITH-NOTES as application baseline only. Reviewer
ran four fixtures plus 50 randomized oracle controls; corruption of confirmation
reproduced the disclosed failure. First likelihood/prior/clutter/mixture uncertainty
are absent. Prior-art links were not independently audited by that reviewer.

Do not score until independent approval and publication confirmation. No behavioral
change after freeze without version/disclosure. Any scoring exception aborts, no
failed-seed removal. Outputs contain hashes of protocol/harness/deferred/Kalman.

Run tests here with one BLAS thread:

    OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v

S1 and reviewed deferred.py unchanged. Publication owner must supply the referenced
freeze; the CLI flag alone does not prove publication.
