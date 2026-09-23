---
id: P22-04
title: "Shape Tells State: Predicting Cell-Cycle Stage From 3D Morphology Alone"
parent: "CBIO064T - Automated 3D Cell Visualization (source abstract, 2025)"
---

# Shape Tells State

**Parent project:** CBIO064T Automated 3D Cell Visualization (Cellpose 2.0 auto-outlining of z-stack slices, cross-height/time cell linking, mesh rendering and side-by-side comparison).

## Premise
The parent's software makes 3D meshes for looking at. The same meshes contain numbers: volume, surface area, curvature, nuclear shape. The Allen Cell WTC-11 dataset has over 200,000 3D hiPSC cells with manual cell-cycle stage labels. If 3D shape alone predicts cell-cycle stage, the visualization tool becomes a measurement tool.

## Hypothesis
3D nuclear and cell shape features (spherical harmonics coefficients plus basic morphometrics) classify interphase vs mitotic sub-stages with balanced accuracy >= 0.85, and 3D features beat features from a single middle 2D slice by >= 0.05.

## Data sources (free/public)
- Allen Cell WTC-11 hiPSC single-cell image dataset with cell-cycle annotations (Viana et al. 2023 Nature; public).
- aicsshparam (spherical harmonics shape parameterization, free).

## Method outline
1. Extract 3D features from provided segmentations (volume, surface area, sphericity, spherical harmonics) and 2D features from the middle slice.
2. Train gradient-boosted classifiers for cell-cycle stage; split by imaging session/plate to avoid batch leakage.
3. Repeat using segmentations produced by the parent-style Cellpose stitching pipeline, to test whether the tool's own output is good enough.
4. Identify which shape features separate stages (SHAP).

## Success gates (locked before results)
- G1: 3D balanced accuracy >= 0.85 with plate-held-out splits.
- G2: 3D beats middle-slice 2D by >= 0.05.
- G3: parent-pipeline segmentations lose <= 0.05 accuracy vs curated segmentations.

## Expected deliverable
A shape-feature extraction add-on for 3D viewers and a cell-cycle classifier.

## Failure/pivot rule
If 2D does as well as 3D (G2 fails), report that; it tells biologists when 3D imaging is unnecessary for this readout.
