# GATES v3 (locked 2026-09-23 ~22:51 IST, before ANY stimulated-condition network metric)
v2 outcome (documented boundary, under-powered per its own rule): with a correctly
size-matched null, 0/27 CROP-seq targets move the top-500 control-variable genes beyond
sampling noise in UNSTIMULATED resting Jurkat cells. Resting-state network prediction
is not testable here - the perturbations are quiet at rest (consistent with the assay's
stimulation design and with weak self-DE on QC).

## Pivot direction: STIMULATED condition (TCR-stimulated cells - the regime where these
TCR-pathway perturbations biologically act). Everything else identical to v2+addendum-2:
- controls = 705 stimulated control cells; top-500 variable genes selected on STIMULATED
  controls only; per-target size-matched null (100x) on stimulated controls;
- panel = targets passing; if < 5, under-powered boundary ships, not counted;
- G1: median Pearson r (network predictor vs observed DE) exceeds mean-DE baseline by
  >= 0.05 AND >= 50% of panel beats permutation null (p <= 0.05);
- G2: median precision@20 exceeds baseline.
- Failure policy: sign-only pivot would be v4 (locked before inspection). If v3 fails
  outright, the two-condition boundary (quiet at rest / quiet under stimulation) ships
  documented, not counted - no further fishing in this dataset.
