# algo50/16 - AMENDMENT 1: Poisson model fit vs naive area estimator

Locked after the original gates were scored (G1 FAIL: naive area estimator -12.7% at 30x; G4 FAIL: -30% at 5x; G2+G3 PASS; multiplicity-2 recurrence bump from identical single-error corruptions observed), before model-fit results are inspected. Original gates stand.

## Method
PFIT: fit hist[m] = D * Poisson(m | lambda) by least squares over m = 8..50 (log-space residuals, seed-independent closed grid; two free parameters D, lambda; init lambda = argmax region mean, D = hist[round(lambda)]/Pois). Genome size estimate = D; coverage = lambda.

## Gates (locked)
- P1: 30x clean PFIT size within +/-10% of 4,641,652.
- P2: 5x clean PFIT size within +/-20%.
- P3: 30x PFIT lambda within +/-10% of 30 * (1 - 1%*21) (error-thinned expectation ~23.5, range 21.1-25.9).
Pivot PASSES if P1 and P2 pass.
