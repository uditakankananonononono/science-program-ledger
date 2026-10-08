# F2 recorded boundary diagnostic

All 15 prescribed rows retained. Unchanged published freeze edeca0b75984331cdc79d9659979049563a4f7f4.
Full: 0 exceptions, 2 exact-unreachable/tolerance-primal-checked rows.
Reduced: 1 exception, 2 exact-unreachable/tolerance-primal-checked rows.
No exact-reachable/float-infeasible cases observed. Independent result review pending.

At scales 1e-6 and 1, offset +1e-10 gives exact rational unreachable targets but both
floating methods return primal_checked. Raw exact binary-control replay and target
conversion deltas retained. The floating label is tolerance-based, not mathematical
membership; these disagreements are not automatically defects. At scale 1e6 with
+1e-10 offset, full says solver_infeasible and reduced raises primal lift failed.
That exception is retained, not converted to an infeasibility certificate or retried.
Default absolute tolerance unchanged, no post-freeze tuning or case exclusion.

Exact declared rational model is not physical truth or measured precision. Scalar
fixed cases only, not a blind holdout or general equivalence/performance theorem.
Review note: scalar params hardcoded in harness, protocol descriptions match this
version; future changes need new disclosed version. All source/run hashes in raw.json
and run-receipt.json. Single-thread BLAS/OMP, Python 3.10.12, numpy 2.2.6, scipy 1.15.3.
Builder-measured 0.238s, peak RSS 76840 KiB, telemetry not independently authenticated.
No hardware/anatomy/safety/calibration/scientific gate or invention claim.
