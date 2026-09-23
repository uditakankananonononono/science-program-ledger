# EXP200-108 R2 pivot - "Know when the model knows": confidence-gated sequence-only variant calling
Locked: 2026-09-23 21:52 IST, after R1 FAILED (G1, G2) and BEFORE any R2 data were scored.
R1 result is preserved unchanged in results/metrics_R1.json.

## Why pivot
R1: ESM-2 8M sequence-only pooled AUROC 0.635 (fails 0.75) and does not beat BLOSUM62 (0.667).
R1 failure characterization (exploratory, seen on R1 data): AUROC 0.80 at low-entropy (model-confident) sites vs ~0.60 elsewhere.
New direction: the useful product is not a universal sequence-only caller but a self-auditing one that knows which
sites it can call. This must be shown on data the R1 observation never touched.

## Fresh evaluation set
Same filters as R1. 150 genes drawn with seed 20260924 from eligible genes EXCLUDING all 150 R1 genes.

## Fixed parameters (carried from R1, not tuned on R2)
- Confidence threshold: site entropy <= 0.9071 (R1 lowest-quartile boundary).
- Scores: ESM-2 t6_8M WT-marginal log-ratio; BLOSUM62 baseline.

## Gates (R2 SUCCESS requires H1 and H2)
H1  On R2 variants at confident sites: AUROC >= 0.75 with gene-bootstrap 95% CI lower bound >= 0.70, and coverage >= 20% of R2 variants.
H2  At confident sites ESM beats BLOSUM62 by >= 0.05 AUROC (gene-bootstrap CI of difference excludes 0).
Secondary (reported, not gating):
S1  Per-protein label-free normalization (z-score of S_esm against all 19 substitutions at all positions of that protein) vs raw, pooled AUROC.
S2  Does the confident-site advantage replicate with ESM-2 t12_35M (threshold re-derived only from 35M on R1 genes)?

## Failure policy
If H1/H2 fail, the negative is preserved and the next pivot is written as GATES_R3.md before new results.
