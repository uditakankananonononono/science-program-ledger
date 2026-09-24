# algo50/08 - Neighbor-joining vs UPGMA: how much does violating the molecular clock cost UPGMA?

Lane RES-2. Algorithm study (not counted toward the flagship 100). Protocol hashed and timestamped before scoring (`results/lock.txt`).

## Bottom line
- Textbook direction reproduced cleanly on 100 simulated 32-taxon trees per regime (JC69, L=1000): under rate variation (branch lengths x lognormal sigma 0.5), UPGMA's mean normalized RF error more than triples, 0.074 -> 0.228, while NJ barely moves, 0.052 -> 0.067.
- Mild surprise: NJ beats UPGMA even when the clock holds exactly (0.052 vs 0.074). UPGMA's greedy average-linkage errors compound even in its own regime.
- Rate variation is the mechanism: same topologies in both regimes, only branch lengths rescaled.

## Data
Simulated (no downloads; regenerable from seeds 1000..1099): coalescent ultrametric trees, 32 taxa, scaled to ~0.25 subs/site root-to-tip; RATEVAR multiplies each branch by exp(N(0,0.5)). JC69 sequences, 1000 nt. JC69-corrected distances, saturation clamped at p=0.749 (helps UPGMA if anything).

## Results (results/results.json)
| regime | UPGMA mean nRF | NJ mean nRF |
|---|---|---|
| CLOCK (ultrametric) | 0.0737 | 0.0520 |
| RATEVAR (sigma=0.5) | 0.2284 | 0.0675 |

## Gates
- G1 PASS: RATEVAR NJ 0.0675 <= UPGMA 0.2284 - 0.05.
- G2 PASS: CLOCK NJ 0.0520 <= UPGMA 0.0737 + 0.05.
- G3 PASS (mechanism): UPGMA RATEVAR 0.2284 >= CLOCK 0.0737 + 0.05.
- G4 PASS: NJ RATEVAR 0.0675 <= 0.25.

Project PASSES (all four gates). A reproduction of known direction, not new science: value is the quantified cost curve at sigma=0.5 and the with-clock NJ advantage.

## Caveats
- Single tree size (32), single length (1000 nt), JC69 only - no model-misspecification stress (e.g., GTR+Gamma data) which would hit both methods.
- nRF is unrooted; UPGMA's rooted ultrametric output is evaluated only on unrooted splits, the generous comparison.
- Simulation uses coalescent heights for CLOCK and iid exponentials for RATEVAR base trees; other tree shapes (pectinate vs balanced) shift absolute numbers.

## Reproduce
`python3 code/run.py` (needs numpy; ~1 min).
