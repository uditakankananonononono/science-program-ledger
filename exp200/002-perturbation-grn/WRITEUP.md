# DOC-1-002 — Perturbation-Aware GRN, attempt 1 (Datlinger CROP-seq Jurkat): documented boundary, project steered to a new dataset

**Status: boundary (NOT counted). v4 direction locked, running next.**

## What was asked
Do gene-gene correlations visible in unperturbed control cells predict which genes move
when a regulator is knocked out (the testable core of perturbation-aware GRN inference
on a 2-CPU/2GB lane)?

## Gate chain (all locked before the outcomes they govern)
- v1: self-knockdown QC gate (target mRNA log2FC < -0.25). FAILED at panel construction:
  1/27 targets pass. Documented: CRISPR KO is a protein-level lesion; target mRNA rarely
  drops (both conditions). The gate measured the wrong molecule.
- v2 + addendum-2: effect-presence panel via size-matched control-split null. Result:
  0/27 targets (unstimulated) exceed noise on top-500 control-variable genes.
- v3: same design in the TCR-STIMULATED condition (locked before stimulated metrics).
  Result: 0/30 targets pass.

## The boundary (measured, real)
In this CROP-seq screen, mRNA-level pseudobulk effects of TF knockouts do not exceed
size-matched sampling noise in EITHER resting or stimulated Jurkat cells, and the
target's own mRNA is invisible in 26/27 cases. Network-from-controls prediction is not
falsifiable on this dataset at this power. Per program steering this is a documented
boundary and does NOT count as a useful result.

## Steering the project (pivot rule)
v4: same question, a dataset whose biology guarantees strong transcriptional KO effects -
Adamson & Weissman 2016 Perturb-seq (K562, UPR regulators; scPerturb/Zenodo 13350497,
32MB). GATES-v4.md locked before its outcomes. The mRNA-vs-protein QC lesson carries
over as a pre-registered QC note.
