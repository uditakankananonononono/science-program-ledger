# 006C ADDENDUM 1 (locked 2026-09-24 ~01:10 IST, BEFORE any DL training or 6AL5 scoring)
1. Permutation scheme made computable: instead of 200 perms x 16-fold LOCO (infeasible
   on this hardware), permutation discipline applies to a FIXED LOCKED SPLIT: train on
   the 13 lowest-PDB-ID complexes, test on the 3 highest (1WEJ, 2JEL, 5LHQ - by sorted
   ID, chosen blind to outcomes). 200 perms of that exact split; observed fixed-split
   AUROC must exceed ALL nulls. G1 LOCO-CV is still run and reported honestly (no perm
   criterion on it). Recipe unchanged (30 epochs etc.).
2. Provenance note: 006B computed 6AL5 structural features/labels as preparation but
   never fit, selected, tuned, or scored any model on it (006B WRITEUP: "G2 NOT RUN -
   G1 never cleared; 6AL5 stays untouched per discipline"). 006C re-featurizes 6AL5
   under its own locked spec (4.0A label, new feature set). Pristine status holds.
3. 6AL5's antibody is the B43 FAB (TITLE record), chains H+L; antigen chain A (CD19).
