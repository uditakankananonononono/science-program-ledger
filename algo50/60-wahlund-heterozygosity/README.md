# algo50/60 - Wahlund effect: heterozygosity deficit under hidden structure

Lane RES-2. Algorithm study. Protocol hashed before results (`results/lock.txt`). Topic lane-chosen (no list past 55).

## Bottom line
Simulated Wahlund deficits match the exact theory F_IS = w(1-w)d^2 / (pq(1-pq)) to within 0.006 in all 8 cells (gate 0.02): at 50/50 mixture with d=0.5, a quarter of expected heterozygosity vanishes (Ho/He = 0.749); at d=0.7 half vanishes (0.505). Deficit ordering follows d^2 exactly (G2), and the unstructured control shows no deficit (F_IS = 0.003, G4).

## Data
Simulated (seed 17): biallelic loci, pA ~ U(0.15,0.25), d in {0.1,0.3,0.5,0.7}, w in {0.5,0.3}, 1000 loci x 500 diploids per cell.

## Gates
G1 PASS (max deviation 0.0051), G2 PASS (exact d^2 ordering), G3 PASS (0.749 <= 0.75), G4 PASS (control 0.003). Overall PASS.

## Caveats
- Within-population HWE and equal drift assumed; real structure adds drift, admixture gradients, and assortative mating.
- F_IS estimator is the simple 1-Ho/He moment estimator, not a likelihood estimator.

## Reproduce
`python3 code/run.py` (numpy, scipy; ~30 s).
