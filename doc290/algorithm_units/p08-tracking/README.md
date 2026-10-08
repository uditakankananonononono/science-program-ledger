# P08-03 variable-rate tracking baseline

Established constant-velocity Kalman filtering baseline, not an algorithm invention
or a validated microrobot tracker. State is [x,y,vx,vy]. Caller supplies dt,
acceleration spectral density q, initial covariance and measurement covariance.
No imaging noise or physiological calibration is inferred. Missing observations
perform prediction only. Position update uses solve and Joseph covariance form;
NIS is an innovation diagnostic, not a calibrated alarm or safety guarantee.

Requires numpy; run `python3 -m unittest -v` in this directory. Five tests pass:
closed-form prediction/update, process-covariance partition identity, 100 variable
interval/dropout symmetry/PSD checks, and invalid-input no-mutation checks.
Synthetic software correctness only, not independent biological validation.

Remaining gaps: independent numerical review, exact overflow/error-contract
coverage, real trajectories, imaging/degradation calibration, published comparator,
frozen outcome evaluation and novel contribution. No P08-03 scientific gate is
passed. Near-zero negative covariance tolerance is 1e-12, not an inferred repair;
noise matrices with values below that numerical tolerance need careful review.
No downstream navigation success or benchmark win claimed.

## Offline RTS smoother baseline

Nine tracking test methods pass locally. smoother.smooth takes supplied filtered
and predicted Gaussian records plus transitions and runs established offline RTS
backward smoothing. It uses future data and is NOT a real-time control estimator.
A two-time direct joint-Gaussian conditional fixture independently supplies the
expected mean/covariance, plus terminal identity, single-record copy, prediction-
only identity and malformed/singular/inconsistent-record rejection checks.

Prediction covariances must be positive definite; singular predictions rejected.
Externally supplied records are not certified consistent; negative output covariance
is rejected rather than repaired. An initial negative-covariance test fixture was
incorrect (it produced positive covariance); corrected fixture uses a filtered
covariance of 5I against prediction 2I and terminal I, giving negative output.
No production formula was changed to force a test pass. No real-data/calibration,
causal benefit, discovery or benchmark win. Independent review pending.

## Error-metric unit

14 tracking tests pass locally. metrics.evaluate reports position/velocity RMSE
and full-state NEES with explicit boolean truth availability. Missing truth is
excluded and counted, never zero-filled; all-missing yields None metrics, not a
perfect score. Estimate/covariance validation covers every row, including excluded
truth. Positive-definite evaluation covariance required; singular unsupported.
Hand-calculated errors, missing-truth cases, invalid-input and NEES linear-coordinate
invariance fixtures pass. NEES numbers alone do not demonstrate calibration or
chi-square guarantees: model correctness and dependence assumptions remain open.
No real trajectory comparison, noise calibration, invention or win.
