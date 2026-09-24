# GATES ADDENDUM A - DOC-1-031 (locked 2026-09-24 08:40 IST, BEFORE any model fitting or scoring)

## Protocol fidelity correction
The locked GATES.md Data section listed "TRAIN: AmPEP training set + iAMP-2L Supp-S1 bench".
The Macrel paper's exact training protocol (train/build-AMP-table.py, verified in source) trains
on the AmPEP training set ONLY; Supp-S1 is the paper's auxiliary benchmark set, not training
data. Since the claim says "the Macrel paper's exact training protocol", training must be
AmPEP-only.

Correction: TRAIN = AmPEP train (3,268 AMP + deduped non-AMP, per build-AMP-table.py). Supp-S1
(3,887 seqs, AMP.train_bench.faa.gz) becomes an UNGATED secondary held-out evaluation reported
alongside dev for context. No gate thresholds change; no outcome has been computed yet.
