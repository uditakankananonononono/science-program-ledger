# F2 numerical boundary audit freeze candidate

Evaluation grid NOT run. Two separate development methods pass at scale 3,
offset -1/2, plus exception retention. Locked grid has 3 coordinate scales x 5
near-boundary offsets = 15 prescribed scalar cases. No timing score or random seeds.
Full/reduced floating LP outputs compared to exact declared rational membership;
controls converted to exact binary-float Fractions for replay against rational B,
target and bounds. Floating B/target conversion deltas separately retained.

Default solver/absolute readback tolerance unchanged. A tolerance-accepted
primal_checked is not exact rational reachability; disagreements are diagnostic,
not automatically defects or performance losses. Rational model values do not
establish physical measurement precision. Exceptions retained, no dropped cases
or tolerance tuning. Exact oracle exception aborts. Only scalar model, prescribed
grid, no blind holdout/physiology/hardware/science/novelty claim.

Protocol/harness must be reviewed and published before run. Text freeze-reference
argument is provenance field, not mechanical permission. Single BLAS/OMP thread set
externally and environment recorded at scoring. Prior production modules unchanged.
