# algo50/34 - Quality-weighted vs majority-vote consensus calling

Lane RES-2. Algorithm study. Protocol hashed before results (`results/lock.txt`).

## Bottom line
Phred-quality weighting strictly dominates majority vote: never worse at any coverage (G1), and at coverage 3 the consensus error rate drops from 1.9e-3 to 7.5e-4 (ratio 0.39, gate <= 0.60). At coverage >= 5 both callers hit 0 observed errors on 20k positions, so the discriminative regime is exactly low coverage; G4 (QW@c8 <= MAJ@c15) passes vacuously at 0-error - boundary documented, not claimed as a real 2x-coverage equivalence.

## Data
Simulated (seed 5): 20,000 positions, Q ~ {10,20,30,40} uniform per read, coverages 3/5/8/15/30.

## Gates
G1 PASS, G2 PASS (0.395), G3 PASS, G4 PASS (vacuous, see caveat). Overall PASS.

## Caveats
- Uniform-Q mixture is milder than real instruments (which have positional/base-context error structure); the low-coverage advantage of QW would likely grow with heavier Q spread.
- c>=5 floor of 0 observed errors means those cells bound error rates at < 5e-5, not exact zeros.

## Reproduce
`python3 code/run.py` (numpy only, <10 s).
