# Finite-scenario minimax terminal-error LP

Established epigraph LP, not invention. One shared actuator schedule, one nonnegative
error bound t. For every scenario/terminal coordinate, -t <= terminal-target <= t.
Minimize t, retaining original actuator/slew constraints. This is a separately named
soft-target problem: target deviations are explicit outputs, not feasibility success
on the earlier exact-target/box problems. No corridor or intermediate-state safety.

18 local development methods pass (15 prior + 3 analytic minimax controls): two gains
1/2 against target 1 require shared control 2/3 and error 1/3; first-step slew cap .5
against target 1 gives error .5; compatible per-scenario targets give zero error.
Returned trajectories/errors are reconstructed separately, and max absolute coordinate
terminal error is compared to solver epigraph bound. This checks primal objective
consistency, NOT a dual optimality certificate. Analytic fixtures support only those
constructed cases. No scored benchmark/held-out test or general superiority claim.

Enumeration only, constant maps, fixed shared initial state. No uncertainty continuum,
recourse, hardware/field magnitude/anatomy/drag/magnetization calibration. Absolute
coordinate infinity error gives each coordinate equal numerical weight; physical
units/scaling need a future explicit policy. Floating point solver status, tolerance,
dense scaling, duplicated assembly drift and extreme finite arithmetic remain limits.
Original reviewed scenario/corridor/feasibility modules unchanged. Review pending.
