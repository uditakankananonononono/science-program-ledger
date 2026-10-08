# Synthetic gradient structure

Model-consistency prep, not new physics, hardware calibration or coil realizability.
For local magnetostatics in a current-free homogeneous region, curl-free field and
zero divergence imply symmetric trace-free gradient. University source fetched:
https://www.geol.umd.edu/facilities/seismology/the-gradiometer-has-finite-size/
The source also warns finite-difference gradiometers need not reproduce the exact
local tensor. Our check is for analytic local derivatives, not finite sensor data.

Five synthetic coefficients construct each 3x3 actuator gradient; symmetry/trace
residuals checked with declared absolute tolerance. No units or device values inferred.
Does not validate boundary conditions, finite-coil realizability, workspace variation,
magnetization, permeability discontinuities or time-dependent electromagnetic fields.
Necessary local structure is not a sufficient global hardware certificate.

32 dev methods pass (28 prior + 4 new): construction and mobility-map algebra,
asymmetry/trace negatives, rigid-frame rotation and invalid input. Constructed
coefficients are placeholders, not measured gradients. Prior modules unchanged.
Tolerance 1e-12 uncalibrated; extreme arithmetic may raise FloatingPointError.
No schedule score, anatomy, physical safety, scientific gate or novelty claim.
