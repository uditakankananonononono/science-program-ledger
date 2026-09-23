---
id: P17-03
title: "Cas12-3D: Topological Off-Target Prediction for Cas12a Nucleases"
parent: "CBIO054 - 3D-Aware CRISPR Off-Target Prediction (source abstract, 2026)"
---

# Cas12-3D

**Parent project:** CBIO054 TAG-Cas (built for Cas9; Cas12a's different biophysics may gate differently).

## Premise
Cas12a is the second clinical nuclease - different PAM, staggered cuts, intrinsic guide processing, and higher intrinsic specificity. Whether 3D genome topology gates Cas12a off-targets the way TAG-Cas showed for Cas9 is an open mechanistic question with direct therapeutic relevance (Cas12a is chosen precisely when Cas9's profile fails). Public Cas12a off-target datasets (GUIDE-seq-class genome-wide assays) exist. This project ports the TAG-Cas architecture to Cas12a, tests cross-nuclease transfer of 3D gating, and answers: is topological gating a universal feature of CRISPR nucleases, or nuclease-specific?

## Data sources
- Published Cas12a genome-wide off-target datasets (GUIDE-seq and successors; public).
- crisprSQL (public): Cas12a subset where available.
- ENCODE/4DN: matched cell-line Hi-C/ATAC.
- Published Cas12a on-target activity screens (public) for the efficacy arm.

## Method outline
1. Harmonize Cas12a off-target datasets with cell-line-matched 3D features.
2. Retrain TAG-Cas-style architecture on Cas12a; ablate 3D branches.
3. Direct transfer test: apply Cas9-trained gating weights to Cas12a (does topology transfer?).
4. Compare topological feature importance Cas9 vs. Cas12a with statistical tests.
5. Combined specificity ranking: sequence + topology across both nucleases for therapeutic guide selection.

## Success gates (locked before results)
- G1: Cas12a model PR-AUC >= published flat baselines + 0.03, or 3D value certified absent for Cas12a.
- G2: universality verdict delivered with statistical support: gating transfers, partially transfers, or is nuclease-specific - each outcome is a finding.
- G3: leave-one-guide-out and leave-one-study-out validation both reported.
- G4: combined-nuclease guide-ranking tool shipped with per-nuclease confidence.

## Expected deliverable
The Cas12-3D predictor, the cross-nuclease universality study (the headline science), and the combined guide-ranking tool for therapeutic programs choosing between nucleases.

## Failure/pivot rule
If Cas12a public data is too thin for G1, pivot to pooled multi-nuclease training (Cas9 data helping Cas12a) and quantify the cross-nuclease data subsidy - itself an answer to the universality question, gates re-locked.
