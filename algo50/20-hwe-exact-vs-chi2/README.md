# algo50/20 - Hardy-Weinberg exact test vs chi-square at small allele counts

Lane RES-2. Algorithm study. Protocol hashed before scoring (`results/lock.txt`).

## Bottom line
- At MAF 0.05 / n=500 the chi-square HWE test's type-I rate is 4.4x the exact test's (1.55% vs 0.35% at alpha 1%); the exact test sits at/below nominal while chi2 is inflated.
- The exact test costs little power: under F=0.1 inbreeding (MAF 0.2, n=500) power 33.9% vs chi2 37.4%.
- At MAF 0.01 / n=200 the exact test stays conservative (0.2%); chi2 runs at 2% (2x nominal).

## Data
Simulated genotype counts (multinomial, seed 1, 2000 replicates per condition). A: null MAF 0.05 n=500; B: null MAF 0.01 n=200; C: inbreeding F=0.1 MAF 0.2 n=500.

## Results (results/results.json)
| condition | CHI2 rate | EXACT rate |
|---|---|---|
| A null MAF 0.05 n=500 (type-I) | 0.0155 | 0.0035 |
| B null MAF 0.01 n=200 (type-I) | 0.020 | 0.002 |
| C F=0.1 MAF 0.2 n=500 (power) | 0.3735 | 0.339 |

## Gates
- G1 PASS: 0.0155 >= 2x 0.0035.
- G2 PASS: 0.0035 in [0.003, 0.02].
- G3 PASS: 0.339 >= 0.3735 - 0.05.
- G4 PASS: 0.002 <= 0.05.
Project PASSES (all gates).

## Caveats
- Exact test is discrete-conservative at tiny counts (0.2% at alpha 1%): the "win" is calibration, not more discoveries.
- Single alpha (0.01), single F; results are regime-specific.
- No mid-p variant tested (would recover some conservativeness).

## Reproduce
`python3 code/run.py` (needs numpy, scipy; ~2 min).
