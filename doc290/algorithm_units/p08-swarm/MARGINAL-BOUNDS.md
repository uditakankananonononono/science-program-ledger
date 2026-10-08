# Marginal-only dependence bounds

Established small distribution LP, not invention. Supplied exact rational target/
offtarget marginals and payload thresholds define 3^N ternary outcomes; metric
membership computed rationally. Floating LP minimizes/maximizes event probability
with normalization and each target/offtarget marginal equality, allowing arbitrary
cross-agent dependence. N 1..5 enforced before enumerating states. Lost marginal
implied by normalization and other two. Not an estimate of real dependence.

20 dev methods pass (16 prior + 4). Two-agent p=.5 full-payload bounds [0,.5],
half-payload bounds [.5,1], single-agent fixed probability, N guard and corrupted
NaN solver mass refusal. Returned primal distributions/marginals/event probability
read back finite/nonnegative/normalized within absolute 1e-8 tolerance. No independent
dual optimality certificate; extrema remain solver claims supported by analytic
fixtures, not a universal exact certificate. Rational-to-float marginals may round.
Near-boundary negative mass within tolerance is reported, not clipped; distributions
are numerical witnesses, not exact probability tables. Other solver failure aborts.

Cap is supplied metric, not biological safety. No validated physical marginals,
coordination/energy/info/cost/time equality or anatomy/scientific gate. Size guard
bounds outcome count, not Fraction bits/input size/CPU. No held-out/scored comparison
or novelty claim. Earlier baselines unchanged; review pending.
