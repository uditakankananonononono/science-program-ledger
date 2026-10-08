# Shared-schedule finite-scenario feasibility

Established LP application, not a new robust optimizer. One actuator schedule
must end in a supplied terminal box for every enumerated constant linear actuator
map. All maps start at the same fixed state, share dt, actuator limits, slew and
previous control. No per-scenario recourse/control change. Residual readback rebuilds
every trajectory from the shared schedule and checks every terminal box, plus
actuator/slew. Solver infeasible still has no independently checked dual certificate.
Zero objective is feasibility only, no effort optimality.

15 development methods pass (10 prior + 5 new). New checks: shared exact scalar
gain schedule, independently feasible but jointly impossible targets, compatible
terminal intervals, explicit unlisted-map violation, strict tolerance and bad-map
rejection. The unlisted-map fixture intentionally demonstrates the missing guarantee.
No held-out scoring, scientific gate, anatomy/hardware or novelty claim.

No corridor constraints in this unit. No safety between nodes or even at nonterminal
nodes. Guarantee covers only enumerated constant maps; time-varying maps, unlisted
uncertainty, drag, magnetization, field magnitude and vessel walls are not established.
This is not a continuous uncertainty certificate. More scenario constraints can
make feasibility harder; no robustness benefit claimed from constructed examples.
Absolute tolerance remains uncalibrated, but this separate interface rejects bool
and string tolerance. Original reviewed feasibility.py/corridor.py remain unchanged.
Dense memory/time scaling and extreme finite arithmetic remain unreviewed. Future
integration must reconcile duplicated assembly without weakening frozen evidence.
Independent review pending; not yet published.
