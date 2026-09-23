# algo50/21 - Protein secondary structure from single sequence: GOR-style information vs a small neural net

Protocol and gates locked before scoring (PROTOCOL.md, results/lock.txt). RCSB DSSP secondary structure: 1500 unique chains (311,665 residues) in 1304 homology groups (3-mer Jaccard >= 0.3), 5-fold group CV. 3 states: H 31.6%, E 23.1%, C 45.3%.

## Results (results/metrics.json)
| method | Q3 | MCC helix | MCC strand |
|---|---|---|---|
| Chou-Fasman-style propensity (+-3 window) | 0.528 | 0.288 | 0.263 |
| GOR-I-style information (+-8 window) | 0.615 | 0.401 | 0.373 |
| MLP, 64 hidden units, one-hot +-8 window | 0.662 | 0.505 | 0.441 |
Majority-class (all coil) Q3 would be 0.453.

## Gates
- G1 PASS: Q3 +0.047 over GOR (95% CI 0.044 to 0.050).
- G2 PASS: MCC improves for both helix (+0.104) and strand (+0.068).
- G3 PASS: Q3 0.662 (needed 0.65).

## What this means
Under a homology-aware split, a small nonlinear model on the same 17-residue window beats the independent-residue GOR approach by about 5 points Q3, and helix detection benefits most. This is a clean, honest REPRODUCTION of a known direction (Qian & Sejnowski 1988 reported ~64% single-sequence Q3 with a neural net; GOR-I-type methods are usually quoted near 60-65%). It is not a new state of the art: modern predictors that use evolutionary profiles or protein language models reach 80%+ Q3. The value here is the like-for-like comparison: same window, same folds, homologs held out.

## Caveats
- Single sequences only, no profiles or MSAs.
- Homology grouping by 3-mer Jaccard is coarser than alignment-based culling, so some remote homologs may cross folds.
- The MLP ran only 30 epochs (early stopping on), with no tuning.
- Unassigned DSSP positions count as coil.

## Reproduce
Download the URL in data/source_url.txt into data/, check the sha256, then cd code && python3 select.py && python3 run.py (~2 min)
