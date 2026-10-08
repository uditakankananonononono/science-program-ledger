# Proposed fixed-moment local mobility-gradient map

Modeling proposal only, not calibrated hardware or new force law. The source
OctoMag equation (7) uses M^T B_x(P), M^T B_y(P), M^T B_z(P) as force-current rows:
https://vigir.missouri.edu/~gdesouza/Research/Conference_CDs/IEEE_ICRA_2010/data/papers/0469.pdf

For supplied fixed moment m and per-current gradients G[a,b,j], define
F[a,j] = sum_b m[b] G[a,b,j], with a position-derivative axis, b field-component
axis, j actuator. Proposed overdamped local extension: v = L F I for supplied
symmetric positive-definite mobility L. The extension is an assumption, not a
measured drag model. No particular fluid, robot shape, wall, orientation or flow
has been admitted. Linear current-field and fixed moment must be justified per
regime; soft magnetic induced moment may depend on field/current, invalidating
a constant force-current map. Spatial gradients varying along a path invalidate
one fixed map unless approximations are separately bounded.

SI conventions: moment A*m^2; G T/(m*A); force-current N/A; mobility m/(N*s);
velocity-current m/(s*A). Inputs are not unit-aware, no unit conversions or SI
calibration inferred. Mobility symmetry/positive-definiteness is an interface
assumption, not evidence it is physical. Code does NOT certify gradients obey
Maxwell constraints or are realizable by coils. Dense arange fixtures deliberately
are algebraic placeholders, not field-valid instances or an admitted hardware profile.

28 local development methods pass (24 prior + 4 map methods): hand-calculated dense
axis contraction, current-before/after contraction identity, zero moment, invalid
mobility/nonfinite rejection. Earlier LPs unchanged. No schedule run with this map;
no source calibration bytes/code copied; no anatomy, physical robustness, continuous
safety, novelty or scientific gate. Independent review pending.
