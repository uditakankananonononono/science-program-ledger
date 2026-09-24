# algo50/50 - Repeated peeking at trial data vs Pocock group-sequential boundary

Status: LOCKED before any results (lock in results/lock.txt). Lane RES-3. Algorithm study.

## Question
How much does checking a two-arm trial for significance after every batch of patients inflate false positives, and does a Pocock boundary restore control without losing much power?

## Data (simulated)
Two arms, normal outcome SD 1. Look after every 20 patients per arm, up to 200 per arm (K=10 looks). Null: no difference. Alternative: difference 0.3. 5000 replicates each, seed 1.

## Methods
- FIXED: one z-test at 200/arm, two-sided alpha 0.05.
- NAIVE: stop at the first look with two-sided p < 0.05.
- POCOCK: stop at first look with p < 0.0106 (Pocock nominal level for K=10, overall alpha 0.05; value taken as a design constant and checked by G2).
Known SD z-test throughout.

## Gates
- G1: null, NAIVE type-I >= 0.15.
- G2: null, POCOCK type-I in [0.035, 0.06].
- G3: null, FIXED type-I in [0.04, 0.06].
- G4: alt, POCOCK power >= FIXED power - 0.10.
PASS if G1+G2; G3/G4 reported either way. Also reported (not gated): mean patients per arm under alt for POCOCK.

## Failure policy
Negatives preserved; pivots via locked amendments only.
