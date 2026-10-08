# Synthetic map-to-schedule integration

33 development test methods pass (32 prior + 1 integration). Three symmetric
trace-free synthetic actuator gradients, fixed moment [1,0,0], diagonal mobility
[1,2,3], and target [1,2,3] over two equal time steps give the unique saturated
schedule of .5 in every actuator at both times. A separate replay forms the total
field gradient from currents, contracts force with moment, then applies mobility.
Replayed terminal matches target to declared 1e-8 tolerance. Raw fixture output kept.

Arbitrary numerical units, no SI-calibrated instance. Trace-free symmetry does not
prove finite-coil realization. The local fixed moment/map/mobility assumptions are
not established in vivo or along a spatial path. This is a software connection
fixture, not held-out benchmark scoring or a hardware/anatomy/scientific gate.
No new optimizer, performance comparison or novelty claim. Prior modules unchanged.
Independent review pending; fixture does not weaken prior model-gap disclosures.
