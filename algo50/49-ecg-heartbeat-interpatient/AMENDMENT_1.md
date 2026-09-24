# algo50/49 - AMENDMENT 1 (locked after G1, G2, G4 FAIL, before pivots run)

Outcomes on the original gates: G1 FAIL (M1 beats B1 by +0.009 and +0.015,
needed +0.02 both directions), G2 FAIL (in the DS2->DS1 direction the linear
model on morphology+RR scores 0.869 vs 0.929 for RR-only B0 - morphology
weights do not transfer linearly across patients), G3 PASS (V sensitivity
0.946 / 0.917), G4 FAIL (S sensitivity 0.100 / 0.175, far under 0.55).

The two pre-declared pivots from PROTOCOL.md now apply, unchanged:

- P1 (from G4): oversample S beats in each training split to 50% of that
  split's N count (random duplication, seed 0), refit M1. Gate P1:
  S sensitivity(M1) >= 0.55 in both directions.
- P2 (from G1): restrict accuracy to N/V/F/Q beats. Gate P2:
  accuracy(M1) >= accuracy(B1) + 0.02 in both directions on those classes.

Both are evaluated from fresh fits on the cached features (same
hyperparameters as the original run).
