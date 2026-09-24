# 84 - Gibbs motif recovery

**Bottom line: G1 FAIL (boundary, documented), G2-G4 PASS.** Gibbs site sampler recovers planted 10-mers only when per-site information clears the search threshold: 0% success at q<=0.65, 65% at q=0.8, 90% at q=0.95 (cap = ZOOPS 0.9). The recovery cliff sits between q=0.65 and q=0.8, matching theory: q=0.8 gives ~9.6 bits/motif vs ~8.2 bits needed to locate one site in 300bp, and finite-sample + local-optimum losses push observed success below the 0.8 gate.

## Data
Simulated, seed 87. N in {10,30} sequences x 300bp uniform background; ZOOPS 0.9; motif width 10 with preferred-base probability q in {0.5,0.65,0.8,0.95}; 20 replicates/cell.

## Method
Gibbs site sampler, 300 full sweeps (each sweep updates every sequence once, random order), full conditional over all 291 start positions, pseudocount 0.5.

## Gates (locked in results/lock.txt before scoring)
| Gate | Expectation | Result | Verdict |
|---|---|---|---|
| G1 | success>=0.8 at q>=0.8, N=30 | 0.65 @ q=0.8; 0.90 @ q=0.95 | FAIL at q=0.8 |
| G2 | success<=0.3 at q=0.5, N=30 | 0.0 | PASS |
| G3 | N=10 within 0.2 of N=30 | max gap 0.10 | PASS |
| G4 | monotone in q | 0/0/0.65/0.90 (N=30) | PASS |

## Caveats
- Implementation note (documented before scoring): first run used 250 single-sequence updates, misreading "300 sweeps"; corrected to 300 full sweeps per the locked protocol. All scored numbers come from the corrected implementation.
- Success = >=60% of planted sites recovered within +/-5bp in a replicate.
- q=0.95 N=30 caps at 0.9 because 10% of sequences carry no site (ZOOPS 0.9).
- N=10 slightly beats N=30 at q=0.95 (1.0 vs 0.9) - fewer sequences, easier convergence; within noise.

## Reproduce
python3 code/run.py  (seed 87, ~50s)
