# algo50/01 - Spaced-seed reduced-alphabet k-mers for alignment-free protein family assignment

Lane RES-1. Algorithm study (not counted toward the flagship 100). Protocol and two amendments were each hashed and timestamped before the results they gate (`results/lock.txt`).

## Bottom line
- The original hypothesis failed: a 256-hash MinHash sketch over Murphy-10 reduced-alphabet spaced seeds (RA-SP) beat plain 3-mer MinHash by only 4.4 points (needed 5) and by 6.0 points in the twilight zone (needed 10). Pivot 1 (use it as a prefilter for Smith-Waterman) also failed its gates.
- The failure had one cause: **the sketch was too small, not the features too weak.** RA-SP produces about 2x more distinct features per protein than plain 3-mers (median 550 vs 278), so a fixed 256-hash sketch throws away more of it. Remove the sketch and the same features win clearly.
- Useful result (Amendment 2, all three gates passed): exact Jaccard on RA-SP features (RA-SP-X) gives 74.5% leave-one-out 1-NN family accuracy vs 65.9% for exact plain 3-mers (post hoc McNemar 119 vs 31, p=2e-13) and 63.5% for the 256-hash sketch of the same features (128 vs 15, p=1.5e-23). In the twilight zone (<40% identity to the closest same-family member) it gets 45.3% vs 29.6% for plain 3-mers.
- As a prefilter: RA-SP-X top-30 candidates re-ranked by Smith-Waterman reach 89.3% accuracy (96% of full all-vs-all SW, 92.8%) while running only 2.9% of the alignments; top-50 reaches 81.2% in the twilight zone (96% of SW). Estimated cost about 15 CPU-s vs about 500 CPU-s for full SW on this set (~34x), in plain Python.
- Practical rule: for protein-length sequences, sketch size must scale with the feature-set size. A sketch of 1024 hashes recovers nearly all of the exact-Jaccard gain (72.2% 1-NN, 90.6% at k=50).

## Data
UniProtKB/Swiss-Prot reviewed human proteome via rest.uniprot.org (retrieval time in `data/retrieved_at.txt`, sha256 in `data/SHA256_raw.txt`; raw file not committed, re-download with the query in `PROTOCOL.md`). Kept proteins with exactly one Pfam domain, 80-600 aa, standard residues; families with >= 6 members; sampled 120 families x up to 10 members (seed 1) -> 1,021 proteins (`data/set.json`). 446 queries (44%) fall in the twilight stratum.

## Methods
Leave-one-out 1-NN family assignment. Reference ceiling: Smith-Waterman (BLOSUM62, gap 11/1, score / min self-score). Alignment-free: K3 (exact plain 3-mer Jaccard), MH3 (bottom-256 MinHash of plain 3-mers), RA-C4 (Murphy-10 contiguous 4-mers, s=256), RA-SP (Murphy-10, seeds 11011 + 1101011, s=256), RA-SP-X (same features, exact Jaccard), and s=1024 variants. Cascade(k): shortlist top-k by sketch similarity, pick the SW-best.

## Results
| Method | 1-NN acc | twilight 1-NN | cascade k=30 | cascade k=50 | twilight k=50 |
|---|---|---|---|---|---|
| SW (ceiling) | 0.928 | 0.845 | - | - | - |
| MH3 (s=256) | 0.588 | 0.188 | 0.818 | 0.853 | 0.679 |
| RA-SP (s=256) | 0.635 | 0.262 | 0.846 | 0.870 | 0.729 |
| K3 (exact) | 0.659 | 0.296 | 0.867 | 0.882 | 0.740 |
| RA-SP-1024 | 0.722 | 0.406 | 0.891 | 0.906 | 0.805 |
| **RA-SP-X (exact)** | **0.745** | **0.453** | **0.893** | **0.910** | **0.812** |

Full grids: `results/results.json` (original protocol), `results/cascade.json` (Amendment 1), `results/amend2.json` (Amendment 2), `results/extra.json` (timings, feature-set sizes, post hoc tests). Figure: `results/fig_cascade.png`.

Gate outcomes: G1 FAIL, G2 FAIL, G3 FAIL; A1 FAIL, A2 FAIL, A3 FAIL; B1 PASS (0.893 at k=30), B2 PASS (0.812 vs needed 0.790), B3 PASS (+11.1 points, p=1.5e-23).

Side observation (not gated): at k=200 every cascade slightly exceeds full SW (0.93-0.94 vs 0.928), i.e. the k-mer shortlist removes some high-scoring SW hits to the wrong family. Worth testing as a deliberate consensus filter.

## Caveats
- One proteome (human), so families are dominated by paralogs; cross-species remote homology is untested.
- Families capped at 10 members; only single-Pfam proteins. Multi-domain proteins will be harder.
- Timings are pure Python/NumPy on 2 cores; relative, not absolute, speed.
- 1-NN numbers differ by <1 point between `results.json` and the cascade files because the cascade code adds a fixed random tie-break.
- The RA-SP-X vs K3 comparison was not a pre-registered gate; it is reported as post hoc.

## Next steps
Cross-species test (Swiss-Prot all organisms, hold out whole taxa), multi-domain proteins, and a C/Rust implementation benchmarked against MMseqs2 prefilter.

## Reproduce
`python3 code/prep.py; for w in 0 1; do python3 code/sw.py $w 2 1e9 & done; wait; python3 code/evaluate.py; python3 code/cascade.py; python3 code/amend2.py` (needs numpy, scipy, biopython, matplotlib).
