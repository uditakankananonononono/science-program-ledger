# algo50/45 - AMENDMENT 1 (locked after G3 FAIL at threshold 0.5, before P1 is run)

G3 (per-minute accuracy of M1 at fixed threshold 0.5, record-held-out) FAILED:
0.712 < 0.80. The pre-declared pivot P1 from PROTOCOL.md now applies, unchanged:

- P1: per leave-one-record-out fold, pick the classification threshold that
  maximizes per-minute accuracy on the training records only (grid
  0.05..0.95 step 0.01, using the fold's own trained M1 model applied to its
  training minutes), then measure accuracy on the held-out record's minutes.
  Gate P1: pooled held-out accuracy at these training-chosen thresholds
  >= 0.80.

No other gates change. G4 (record-level a-vs-c AUROC 0.835 < 0.90) had no
declared pivot and stands as a FAIL.
