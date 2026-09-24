# ADDENDUM P1 - locked 2026-09-24 06:52 IST BEFORE P1 outcomes (invokes locked failure tree P1)
G1 result (dev CV, seed 7): composite f1-f6 AUROC 0.9210 vs phyloP 0.8815 (margin +0.0395, PASS half)
vs phastCons 0.9163 (margin +0.0048, FAIL the locked +0.03). G1 as locked: FAIL.
Locked tree: P1 arm executes now.
P1 form (locked): features = f1-f6 + normalized 3-mer composition (64 dims) over the same +/-25bp window.
Same LR (L2 C=1.0, class_weight balanced, standardized), same 5-fold stratified CV seed 7, same margins:
P1 passes G1' iff margin_vs_phyloP >= 0.03 AND margin_vs_phastCons >= 0.03.
If P1 passes: P1 model becomes the composite for G2 (frozen chr22, thresholds unchanged: >=0.65 and
>= max(baseline frozen AUROC)+0.01). If P1 fails: P2 strata (splice-region-only, UTR-only) run under
the same margins; if every arm fails -> documented boundary (conservation saturates).
Thresholds unchanged from GATES.md; no re-fishing.
