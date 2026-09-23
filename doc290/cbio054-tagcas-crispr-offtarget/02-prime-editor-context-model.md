---
id: P17-02
title: "PrimeContext: Chromatin- and 3D-Aware Prime-Editing Efficiency and Off-Target Modeling"
parent: "CBIO054 - 3D-Aware CRISPR Off-Target Prediction (source abstract, 2026)"
---

# PrimeContext

**Parent project:** CBIO054 TAG-Cas (3D-aware prediction; prime editing is the precision modality with the weakest context models).

## Premise
Prime editing installs arbitrary small edits without double-strand breaks, but pegRNA efficiency varies 100-fold between loci for reasons current models (trained on sequence and simple features) only partly capture. TAG-Cas's result - that 3D topology is a major driver for Cas9 - suggests prime editing, which requires reverse-transcription at the nick site, may be even more chromatin-sensitive. Public pegRNA screens (thousands of designs with measured efficiencies) make this testable. This project adds multi-scale 3D and chromatin features to prime-editing efficiency models, quantifies their contribution, and models prime editing's (different, nickase-based) off-target profile.

## Data sources
- Public large pegRNA efficiency screens (e.g., the PRIDICT dataset and successor screens).
- ENCODE/4DN: Hi-C, ATAC-seq, histone tracks for screen cell lines.
- Published prime-editor off-target datasets (nickase-based assays, public).
- crisprSQL: comparator models' training data.

## Method outline
1. Harmonize pegRNA screens with per-locus chromatin/3D features.
2. Extend published efficiency models with topological features; ablate rigorously.
3. Quantify 3D contribution vs. sequence and pegRNA-design features.
4. Build the nickase off-target model with 3D gating; compare to nuclease profiles.
5. Release a pegRNA scorer combining efficiency and off-target risk.

## Success gates (locked before results)
- G1: efficiency model R^2 improves >= 0.05 over the best published sequence-only model on held-out loci, or 3D value certified absent.
- G2: feature-attribution ranks named biological drivers (chromatin states, loop anchors) among top contributors, or the model is reported as sequence-dominated.
- G3: off-target model beats flat baselines by >= 0.03 PR-AUC or the modality difference is certified.
- G4: all claims leave-one-screen-out validated (screen-batch effects are notorious here).

## Expected deliverable
The PrimeContext scorer (pegRNA sequence + locus in; efficiency + off-target risk out), the 3D-contribution study, and the harmonized screen dataset.

## Failure/pivot rule
If screen batches dominate signal (G4 instability), pivot to the batch-harmonization study: which normalization makes pegRNA screens jointly usable - gates re-locked around a cross-screen benchmark.
