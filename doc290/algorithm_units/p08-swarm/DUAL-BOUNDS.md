# Exact marginal-event outer-bound certificates

Established LP weak-duality check, not invention. Caller supplies rational candidate
vectors over normalization and target/offtarget marginal equations. Enumerate all
ternary states (N<=5), verify lower A^T lambda<=event and upper A^T lambda>=event.
Exact maximum inequality violation is repaired by shifting only normalization
multiplier, then every inequality rechecked. This yields exact outer bounds for the
supplied marginal problem, regardless of candidate solver provenance. No floating
solver candidate extraction wrapper yet; floats refused, exact strings/Fractions only.

Nonnegative probability masses imply lower objective bounds minimum event probability,
upper objective bounds maximum. Independently computed exact product distribution
is a feasible witness, so minimum<=its probability<=maximum; outer dual bounds bracket
that witness too. This does not establish tightness or exact extrema. Loose bounds
can lie outside [0,1] and are reported as such, not silently clipped.

24 dev methods pass (20+4): exact two-agent AND bounds, exact candidate violation
repair, explicit loose candidates, float/dimension refusal. Exactness is for supplied
rational model only, not physical probabilities, dependence, budgets or biological
safety. Fraction growth unprofiled, no input-bit/CPU budget. Previous floating LP
unchanged. No scored comparison/scientific/novelty gate. Review pending.
