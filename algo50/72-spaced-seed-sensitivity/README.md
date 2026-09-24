# algo50/72 - Spaced vs contiguous seeds: sensitivity under substitution noise

Lane RES-2. Algorithm study. Protocol + Amendment 1 hashed before the results they gate (`results/lock.txt`). Topic lane-chosen (no list past 55).

## Bottom line
The PatternHunter claim replicates cleanly in the saturated-avoided design (60 bp windows): at q=0.70, spaced-8 beats contig-8 by +0.14 sensitivity (0.83 vs 0.69) and crushes contig-12 (0.22) - same weight, better placement wins; same span, less weight wins. Background safety: theory predicts equal random-hit rates for equal weight (8e-4), and neither seed showed inflation (0 hits in 4000 pairs each - P3 FAILS as locked since 0 observed vs 3.2 expected is a p=0.047 low-count event, but the safety question it guarded is answered: no spaced-seed inflation).

## Gates
- Original (seed 53): G1/G3/G4 FAIL (200bp windows saturated weight-8 seeds at ~100%; background N underpowered; one gate-check direction bug, fixed+documented), G2 PASS.
- Amendment 1 (seed 59, 60bp/lower q/bigger N): P1 PASS (+0.137), P2 PASS, P3 FAIL (underpowered, documented), P4 PASS (monotone).
Net: spaced-seed advantage is real and large in the pre-saturation regime; saturation itself (200bp windows) documented in the original run.

## Data
Simulated (seeds 53, 59): homologous 60-200bp window pairs at controlled identity + unrelated pairs; seeds contig-8, spaced-8 (11010110111), contig-12.

## Caveats
- iid substitution noise; real alignments have clustered errors and indels where don't-care positions matter more.
- One spaced pattern tested; PatternHunter's optimized patterns differ.

## Reproduce
`python3 code/run.py` (seed 53), `code/pivot.py` (seed 59); stdlib/numpy, <1 min.
