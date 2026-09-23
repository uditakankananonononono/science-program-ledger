---
id: P22-10
title: "Quantified Comparison: Turning Side-by-Side Viewing Into Statistical 3D Shape Comparison"
parent: "CBIO064T - Automated 3D Cell Visualization (source abstract, 2025)"
---

# Quantified Comparison

**Parent project:** CBIO064T Automated 3D Cell Visualization (Cellpose 2.0 auto-outlining of z-stack slices, cross-height/time cell linking, mesh rendering and side-by-side comparison).

## Premise
The parent added side-by-side rendering so users can compare two structures by eye. Eyes are poor at judging small shape differences and cannot give a p-value. Shape-space methods (spherical harmonics, shape modes as in Viana et al. 2023) can compare whole populations of 3D cells and show where they differ. This project upgrades "look at two" into "test two groups."

## Hypothesis
A shape-mode comparison detects known perturbation effects (e.g., differences between tagged-structure cell lines or mitotic vs interphase cells) that visual side-by-side inspection by volunteers misses in >= 30% of cases.

## Data sources (free/public)
- Allen Cell WTC-11 dataset (multiple cell lines, cell-cycle stages).
- Public 3D perturbation datasets from IDR (drug-treated 3D cultures) where available.

## Method outline
1. Compute spherical-harmonics shape coefficients for cells; build shape modes by PCA.
2. Compare two groups with permutation tests on shape-mode distributions; render the mean shape difference as a 3D heat map on the mesh.
3. Create comparison pairs with known small and large differences; ask volunteers to judge side-by-side renders (no personal data collected).
4. Compare statistical detection vs human detection rates.

## Success gates (locked before results)
- G1: statistical method detects all known large differences and reports calibrated false-positive rate (<= 5% on same-group splits).
- G2: human miss rate on small differences reported; >= 30% miss rate supports the hypothesis, otherwise the null is reported.
- G3: volunteer count stated; labeled exploratory if n < 10.

## Expected deliverable
A "compare groups" feature that outputs a p-value and a 3D difference map, plus the human vs statistics comparison.

## Failure/pivot rule
If humans do as well as statistics (G2 fails), report that and focus the feature on speed: how many cells can be screened per minute each way.
