# ADDENDUM 3 (locked 2026-09-23 ~23:01 IST, before any v5 outcome metrics)
Two frozen repairs, both calibration mechanics, no gate content change:
1. Memory: the h5ad X is dense (19268 x 21713 ~ 1.7GB > RAM). Loader streams row
   blocks with h5py; control-only variance and library sizes accumulated in pass 1;
   only the selected ~520 columns are materialized in pass 2.
2. Null feasibility: the largest targets (n up to 2347) exceed the 3491-control pool
   for a disjoint size-matched null. Repair: every target's DE uses exactly 100 random
   cells (all targets have >= 500), and its null draws 100v100 disjoint control splits
   (100x). Uniform n=100 => perfectly calibrated across targets.
