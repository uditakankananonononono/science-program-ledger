# DOC-1-002 — Perturbation-Aware GRN: do control-cell correlation networks predict perturbation effects?
# GATES locked 2026-09-23 ~22:44 IST, before any outcome inspection. Lane EXP-1.
# Compute-feasible redesign of "Perturbation-Aware Gene Regulatory Network Inference"
# (2 CPU / 2GB RAM): the testable core is whether network structure visible in
# UNPERTURBED cells predicts which genes move when a regulator is knocked down.

## Data (public; URLs + hashes in results/provenance.md after download)
- Datlinger et al. 2017 CROP-seq K562 (scPerturb harmonized h5ad, Zenodo record 13350497).
- Single dataset, honest scope; no cross-dataset transport claimed at this scale.

## Frozen design (pre-outcome)
- Cells: guide-bearing cells with a confidently assigned target gene + non-targeting
  controls. Pseudobulk log2 fold-change per perturbation vs controls on the top 500
  most variable genes (selection on control cells only - no leakage).
- Perturbation set rule (frozen): all perturbations targeting a gene with >=25 assigned
  cells and measurable self-knockdown (target gene log2FC < -0.25), capped at the 20
  perturbations with the largest self-effect magnitude if more qualify.
- Predictor (network-aware): predicted DE of gene X under knockdown of T =
  corr_control(T, X) * observed self-effect of T. Correlations from control cells ONLY.
- Baselines: (a) all-perturbation mean DE profile; (b) 20x label-permutation null.
- Metrics per perturbation: Pearson r between predicted and observed DE across the 500
  genes; precision@20 overlap of top-|predicted| and top-|observed| genes.

## Success gates
- G1 (primary): median Pearson r across perturbations exceeds baseline (a) by >= 0.05
  AND >= 50% of perturbations beat the permutation null (p <= 0.05).
- G2 (payload): median precision@20 for the network predictor exceeds baseline (a).
- Failure policy (pivot rule): if G1 fails on magnitude, pivot to SIGN-only prediction
  (does the network at least predict direction of movement? same null), gates re-locked
  in GATES-v2.md before sign-level results are inspected. If sign also fails, the
  boundary (control correlations do not read perturbation response in K562 CROP-seq)
  ships documented, NOT counted (per meta/boundary steering).
- Payload regardless: per-perturbation predictability table + a small CLI that, given a
  control expression matrix and a target gene, outputs the predicted affected-gene list.

## Reviewer questions (pre-registered)
- Circular? Control-only correlations; perturbation data never builds the network.
- Single dataset? Declared scope limit; transport is the named next experiment.
- 500-gene restriction? Compute ceiling declared; selection is control-only and frozen.
