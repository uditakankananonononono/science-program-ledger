# algo50/50 - Repeated peeking at trial data vs Pocock group-sequential boundary

Lane RES-3. Algorithm study. Protocol hashed before scoring (`results/lock.txt`).

## Bottom line
- Checking a two-arm trial for p<0.05 after every 20 patients per arm (10 looks) gives a 19.5% false-positive rate, nearly 4x the nominal 5%.
- A Pocock boundary (p<0.0106 at each look) brings it back to 5.0%.
- Cost: power drops from 85.0% to 74.3% for a 0.3 SD effect, but trials that work stop early (130 vs 200 patients per arm on average).

## Results (results/results.json, 5000 replicates)
| scenario | FIXED | NAIVE peeking | POCOCK | POCOCK mean n/arm |
|---|---|---|---|---|
| null (type-I) | 0.055 | 0.195 | 0.050 | 194 |
| effect 0.3 (power) | 0.850 | 0.901 | 0.743 | 130 |

## Gates
| gate | rule | value | verdict |
|---|---|---|---|
| G1 | NAIVE type-I >= 0.15 | 0.195 | PASS |
| G2 | POCOCK type-I in [0.035, 0.06] | 0.050 | PASS |
| G3 | FIXED type-I in [0.04, 0.06] | 0.055 | PASS |
| G4 | POCOCK power >= FIXED - 0.10 | 0.743 vs 0.750 | FAIL (narrow) |
Project PASSES its primary gates (G1+G2). G4 fails narrowly: Pocock's power cost at a fixed max n is slightly over 10 points. Reproduction of known group-sequential behaviour.

## Caveats
- Known-SD z-test; real trials estimate SD, which inflates naive peeking further at early looks.
- O'Brien-Fleming boundaries (smaller power cost, less early stopping) were not compared.
- The Pocock constant 0.0106 was taken from standard tables and confirmed empirically by G2.

## Reproduce
`python3 code/run.py` (numpy, scipy; ~3 s).
