# P08-03 numerical failure audit

Separate, non-scoring software audit. No tracking code or S1 protocol changed.
Run from repository root:

    OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 doc290/algorithm_units/p08-numerical-audit/audit.py

Four fixtures check exact current exception class and unchanged state/covariance:
finite dt=1e200 Python exponentiation overflow (OverflowError), finite observation
1e200 innovation quadratic overflow (FloatingPointError), infinite dt rejection
(ValueError), and singular measurement covariance rejection (ValueError).
results.json records local results and the exact audited Kalman hash. Audit aborts
if any case accepts, changes state/covariance, or produces another exception type.

Heterogeneous exception classes remain a limitation, not a fix. No ill-conditioning
threshold, physically meaningful covariance tolerance, realistic imaging calibration,
scientific gate or invention established. This is not exhaustive finite-input safety.
S1 evaluation seeds were not invoked; this audit uses no random draws.
