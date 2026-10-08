# Exact square-map terminal solver

Established exact Gaussian elimination plus interval membership/witness lift.
For a square invertible constant B, Bz=target-initial has one rational integral
vector. An actuator integral outside its exact interval proves unreachable in this
supplied abstract model. Otherwise exact convex witness lifting provides a schedule,
and terminal equality is replayed. Pivot row swaps supported. Singular/rectangular
maps explicitly raise unsupported, never misclassified as unreachable. Time/bound
validation precedes unreachable verdict. No corridor or coupled actuator constraints.

53 local development methods pass (49 prior + 4): dense pivot swap reachable target,
exact tiny beyond-boundary unreachable target, singular/rectangular unsupported,
and invalid time refused rather than called unreachable. Exact results concern
supplied rational numbers, not physical measurement precision/calibration. Fractions
not JSON-ready; growth/scaling unprofiled. No anatomy/hardware/safety/novelty/scoring
gate. Earlier production code untouched. Prior misleading 'midpoint' test/doc label
renamed to 'interior' (3/4 mixing weight); math unchanged. Review pending.
