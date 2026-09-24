# algo50/22 - AMENDMENT 1: amplitude+background fit, and the squared-correlation correction

Locked after original scoring (G1 FAIL: single-exponential fit to mean r2 recovers 8.8 kb vs true 50 kb; mechanism: r2 decays like correlation SQUARED, i.e. exp(-2d/lambda), plus a 1/N sampling floor; G2+G3 PASS, G4 FAIL), before amended fits are inspected.

## Method
Fit mean-r2(d) ~ A*exp(-d/l) + c (3 params, unweighted least squares, c>=0). Compare l against lambda/2 = 25 kb (theory: r2 ~ rho^2 for thresholded Gaussian, rho ~ (2/pi)arcsin(a) ~ a, so r2 ~ exp(-2d/lambda)).

## Gates (locked)
- P1: N=500 l within [15, 40] kb (consistent with lambda/2).
- P2: fitted c within [0, 3/N] (recovers the sampling floor).
- P3: N=100 l within [10, 60] kb.
Pivot PASSES if P1+P2 pass.
