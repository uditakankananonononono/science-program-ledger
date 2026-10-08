# Reduced terminal integral-box LP

Established convex reachable-set reduction, not invention. Restricted constant B,
independent actuator magnitudes/slew and previous control. Compute each integrated
control interval, solve Bz=target-initial with box bounds in m variables, then lift
by mixing saturated lower/upper slew ramps. Rectangular/singular maps supported via
LP (solver infeasible still lacks independently verified dual certificate). No
corridor, coupled limits, time-varying map, effort objective or scenario intersection.

57 local dev methods pass (53 + 4): rectangular redundancy, rank-deficient unreachable,
zero-slew degenerate interval, injected successful NaN output refusal. Full schedule
and terminal/integral/actuator/slew residuals reconstructed. Strict bool/np.bool_
tolerance rejection; absolute tolerance uncalibrated. A solver excursion within
absolute tolerance is explicitly clipped to the integral box, amount reported;
terminal replay must still pass. Larger excursions rejected, no hidden relaxation.

Dimension m versus full horizon*m does not establish runtime benefit. Floating
interval/lift can differ from full LP near feasibility boundaries; frozen comparison
needed before any equivalence/speed claim. Exact rational units remain a separate
restricted baseline. Numerical scaling/extreme arithmetic and Fraction growth not
settled. No physical hardware/anatomy/calibration/safety/scientific gate or score.
Earlier modules unchanged. Independent review pending.
