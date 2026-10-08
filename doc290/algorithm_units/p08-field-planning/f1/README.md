# F1 pre-score full-vs-reduced comparison

Protocol/harness freeze candidate. Evaluation seeds 3000-3019 NOT run. Two harness
dev methods pass with seed 2999, horizon 8, feasible/impossible classes and an
exception-retention injection. Dev timings not reported as evaluation evidence.
Locked 20 seeds x 3 horizons x 2 classes x 3 repeats = 360 paired rows.
Warm-up separate, order alternates, generation outside timer. Full/reduced whole
calls timed including reconstruction; all exceptions/status mismatches retained.
Exception pairs excluded from ratios but counted, not omitted from status tables.
Ratios for nonexception mismatched statuses are retained too; interpretation must
consider their mismatch flags rather than presenting them as successful comparison.

Constructed feasible targets derive from valid interior ramp mixtures. Impossible
class uses zero first map row with target first coordinate 1, deliberately easy
infeasibility, not evidence of general infeasibility-solver speed. Status expected
from constructed witness/zero row, but floating solvers do not yield exact general
certificates. Instance array hashes retained with fixed generation contract.

No novelty: established integral-box reduction. No score/runtime/equivalence claim
until published freeze and subsequent run/review. One process, three repeats, no
cache flush or OS noise control. Single-environment timing not stable superiority.
No device/anatomy/calibration/physical/scientific gate. Prior solvers unchanged.
