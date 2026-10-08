# Discrete corridor extension

Separate corridor.py leaves reviewed feasibility.py unchanged. Established LP
constraint assembly, not an invention. Each node 0..N has an axis-aligned state
box; prefix dt*B control sums impose bounds. Returned primal trajectory is rebuilt
from controls and checked against all boxes, terminal equality and actuator/slew
bounds. Fixed initial incompatibility beyond tolerance is distinguished from solver
status 2 (still no independently checked dual infeasibility certificate).

10 total development methods pass (5 original + 5 corridor). New fixtures enforce
a unique intermediate scalar node, an unreachable intermediate box, incompatible
initial/terminal nodes, malformed boxes, and dense two-actuator exact node path.
No frozen evaluation/holdout or score. Independent review pending.

Boxes apply only to discrete nodes. With changing boxes or nonconvex obstacles,
node feasibility proves no continuous-time safety. No vessel wall/anatomy model,
magnetic calibration, field norm, effort optimum or robustness under mismatch.
Initial corridor comparison accepts violations within declared absolute tolerance,
consistent with final numerical readback. Tolerance remains uncalibrated. Extreme
finite arithmetic/error paths and memory growth O(N^2) are unreviewed. Code duplicates
the baseline LP assembly to keep its reviewed hash unchanged; future drift risk.
