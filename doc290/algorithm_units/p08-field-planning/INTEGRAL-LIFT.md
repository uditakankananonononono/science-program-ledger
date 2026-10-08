# Exact integral-box witness lift

Established convexity construction for restricted constant-map terminal dynamics.
Each actuator's integrated-control interval is attained by lower/upper saturated
slew ramps. Convex mixing with one fixed weight per actuator attains any integral
inside its interval, preserving magnitude and step-slew constraints. Independent
actuators permit separate weights, so the integral set is a Cartesian box. Under
constant B, terminal increment is B times this integral vector. No target search
or joint feasibility solver implemented; caller supplies candidate integrals.

49 local dev methods pass (45 prior + 4): exact interior schedule, zero-slew degenerate
interval, independent actuator mixtures and B-integral versus full-schedule terminal
identity, and outside/float refusal. Exact rational replay/bounds checked internally.
Returns Fractions, not JSON-ready. Fraction growth unprofiled. Only supplied rational
abstract model; no measurement precision/hardware/calibration/physical safety claim.
No corridor/scenario intersection/time-varying B/coupled constraints. Previous code
unchanged, no score or novelty. Review pending.
