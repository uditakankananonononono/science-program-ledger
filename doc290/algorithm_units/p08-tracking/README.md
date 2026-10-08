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
