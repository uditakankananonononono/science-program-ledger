# Injected solver-output controls

24 local development test methods pass (19 prior + 5 added controls). No production
code changed. Success/status=0 solver responses are injected rather than calling
HiGHS for these controls. For feasibility, corridor and scenario modules: NaN/Inf/
-Inf controls rejected; wrong-terminal controls rejected; correct finite output
accepted. Separate actuator-limit, slew-limit and intermediate-corridor-only
violations rejected. This addresses specific primal-readback paths, not general
solver reliability or infeasibility/optimality certificates.

Minimax epigraph corruption controls remain in its earlier review-repaired tests.
These added checks are constructed negative controls only; shape/type-corrupted
solver return contract, arithmetic overflow, condition numbers, tolerance scaling,
continuous safety, hardware calibration and exhaustive outputs remain unverified.
No invention, score or scientific gate. Independent review pending.
