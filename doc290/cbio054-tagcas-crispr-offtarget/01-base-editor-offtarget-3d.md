---
id: P17-01
title: "Base3D: 3D-Aware Off-Target Prediction for Adenine and Cytosine Base Editors"
parent: "CBIO054 - 3D-Aware CRISPR Off-Target Prediction (source abstract, 2026)"
---

# Base3D

**Parent project:** CBIO054 TAG-Cas (3D-topology-gated off-target prediction for Cas9 nuclease).

## Premise
TAG-Cas proved 3D genome topology gates Cas9 cleavage; base editors are what is actually entering clinics, and their off-targets work differently - deamination without double-strand breaks, plus a separate RNA off-target channel from the deaminase itself. Whether chromatin topology gates base-editing the same way is unknown. Public base-editor off-target datasets (genome-wide DNA assays and transcriptome-wide RNA screens) now exist. This project ports the parent's multi-scale Hi-C gating to base editors, quantifies how much 3D structure matters for deamination vs. cleavage, and builds the first 3D-aware base-editor off-target predictor with separate DNA and RNA channels.

## Data sources
- Published genome-wide base-editor off-target datasets (ABE/CBE; SRA deposits).
- Published transcriptome-wide RNA off-target datasets for deaminases (public).
- crisprSQL (public): sequence-level baseline data.
- ENCODE/4D Nucleome (public): K562 and other cell-line Hi-C/ATAC tracks.

## Method outline
1. Harmonize public ABE/CBE off-target datasets with cell-type metadata.
2. Port TAG-Cas's multi-scale topological features to deamination contexts.
3. Train separate DNA and RNA off-target models; shared vs. separate 3D gating tested by ablation.
4. Compare 3D-feature importance between nuclease and base-editor settings (the science question).
5. Validate leave-one-guide-out and leave-one-study-out.

## Success gates (locked before results)
- G1: base-editor DNA off-target PR-AUC >= best published flat-sequence baseline + 0.03, or 3D value certified absent for this modality.
- G2: 3D-feature importance comparison between nuclease and base editor completed and reported either direction.
- G3: RNA off-target channel modeled with held-out AUC >= 0.75, or the boundary documented.
- G4: honest-negative clause: "3D topology does not gate base editing" is a full publishable result with the ablation evidence.

## Expected deliverable
The Base3D predictor (DNA + RNA channels), the nuclease-vs-base-editor 3D-gating comparison study, and an open evaluation harness over the harmonized public datasets.

## Failure/pivot rule
If public base-editor off-target data proves too sparse for G1, pivot to the transfer-learning variant: initialize from nuclease models and measure how little base-editor data is needed - a data-efficiency study, gates re-locked.
