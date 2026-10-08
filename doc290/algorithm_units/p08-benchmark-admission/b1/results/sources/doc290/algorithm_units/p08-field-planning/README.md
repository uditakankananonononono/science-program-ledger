# P08-04 abstract linear-actuator schedule feasibility

Established LP baseline, not invention, magnetic calibration or anatomy validation.
Discrete model: x[k+1] = x[k] + dt[k] B u[k], with constant linear B. Terminal
state equals target; each actuator has separate absolute bounds and separate slew
bounds |u[k]-u[k-1]| <= slew * dt[k], including supplied previous control at k=0.
These are componentwise actuator bounds, NOT vector field magnitude constraints.
No obstacles, vessel wall constraints, drag, magnetization, dynamics/nonlinear
coupling, field geometry or uncertainty. Five development test methods pass.

SciPy 1.15.3 locally uses linprog(method='highs') with zero objective as a feasibility
problem. Readback independently reconstructs trajectory from controls and checks
terminal/actuator/slew residuals against declared tolerance (default 1e-8). Primal
residual check is floating-point, not an exact rational feasibility certificate.
Solver status 2 is recorded as solver_infeasible, explicitly without independently
verified dual certificate. No optimal-effort claim from zero objective; many
solutions may exist and their schedule is solver-dependent. Other solver failure
or primal-readback failure raises, never turns into a claimed infeasible instance.

Fixtures: analytically unique saturated scalar schedule, first-step slew-limited
reachable/unreachable target, rank-deficient unreachable target, dense actuator
terminal reconstruction, invalid-input caller-buffer preservation. These are
constructed software checks, not frozen benchmark instances/scientific gates.
Extreme finite-input overflow and tolerance scaling remain unreviewed. Missing
hardware mapping remains an open grounding gap, not a blocker to abstract prep.

Official tool reference fetched:
https://docs.scipy.org/doc/scipy/reference/optimize.linprog-highs.html
Describes inequality/equality constraints, bounds, status and infeasibility return.
Live documentation is newer than local SciPy; record local 1.15.3 for reproducibility.

Run tests here:

    OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v

S1/S2 tracking/reacquisition are unchanged. Independent review pending. No scored
comparison, hardware claim, real anatomy gate, scientific gate or novelty evidence.
