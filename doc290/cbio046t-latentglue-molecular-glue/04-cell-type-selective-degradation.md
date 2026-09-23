---
id: P16-04
title: "SelectiveDegrade: Predicting Cell-Type-Selective Protein Degradation From Proteomics"
parent: "CBIO046T - Expanding the Druggable Human Proteome Five-Fold (source abstract, 2026)"
---

# SelectiveDegrade

**Parent project:** CBIO046T (screening glues against disease targets; the selectivity question is where toxicity lives).

## Premise
A glue that degrades its target everywhere is often a poison; the same glue degrading in one cell type is a drug. IMiDs showed degradation can be startlingly cell-type-selective (IKZF1 in myeloma, not everywhere), driven by ligase expression, target levels, and cell state. Public proteomics of hundreds of cell lines (CCLE) plus degrader-treatment proteomics studies make selectivity computable. This project predicts per-cell-type degradation response from baseline proteome state, tests which features drive selectivity, and produces a selectivity-by-design scoring tool: given a target and desired indication, which cell types degrade and which are spared.

## Data sources
- CCLE proteomics (Nusinow et al. 2020, public): baseline proteomes of ~375 lines.
- Published degrader-treatment proteomics datasets (PRIDE deposits).
- DepMap (public): lineage and dependency context.
- Human Protein Atlas (public): tissue-level expression for safety translation.

## Method outline
1. Harmonize degrader-treatment proteomics studies into treatment-response matrices.
2. Train per-degrader response models from baseline proteome features.
3. Feature-attribution analysis: ligase abundance vs. target abundance vs. cell-state signatures.
4. Validate leave-one-study-out; then transport to tissue-level predictions via Protein Atlas.
5. Build the selectivity scorer with a toxicity-side panel (which normal tissues predicted to degrade).

## Success gates (locked before results)
- G1: response prediction cross-study R^2 >= 0.4 for degradation magnitude, or certified ceiling.
- G2: ligase/target abundance features shown necessary (ablation drops R^2 by >= 30%), or the honest finding that selectivity is not abundance-explained.
- G3: tissue-level safety panel produced for >= 3 well-studied degraders, consistent with their known clinical toxicity profile direction.
- G4: all models published with uncertainty; no single-number selectivity claims.

## Expected deliverable
The SelectiveDegrade tool (baseline proteome in; per-lineage degradation prediction + safety panel out), the harmonized degrader-response dataset, and the selectivity-mechanism attribution study.

## Failure/pivot rule
If transport across studies collapses (G1), pivot to the batch-structure audit: which proteomics platforms carry the degradation signal comparably - a platform-harmonization protocol, gates re-locked.
