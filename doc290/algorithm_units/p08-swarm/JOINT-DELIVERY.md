# Explicit delivery and collateral joint metrics

Established exact probability bookkeeping over caller-supplied ternary target,
offtarget or lost outcome per agent. Each agent's payload assigned to exactly one
state; complete table masses nonnegative and sum exactly to one. Missing outcomes
assumed zero, duplicate rows aggregated. Returns marginals, expected payload in
each state and joint payload distribution, target-threshold success, off-target
cap exceedance (strict >), and combined delivery at/above target threshold with
collateral at/below cap. No marginal independence or physical correlation inferred.

12 local dev methods pass (8 prior + 4). A constructed case always delivers half
total payload but meets zero collateral cap only half the time, so target-only
success must not substitute for combined metric. Cap equality accepted, duplicates/
zero-mass and invalid inputs checked. Payload expectation conservation checked.
Threshold/cap are supplied metrics, NOT biologically validated safety or clinical
limits. Total payload explicit; no energy/info/cost/time equality, coordination,
crowding, flow, anatomy/calibration/scientific claim. Fractions/tuple keys not JSON-
ready; table size can be exponential, no resource guard. Review pending; earlier
modules unchanged. No scored comparison, crossover or invention evidence.
