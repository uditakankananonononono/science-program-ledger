---
id: P22-06
title: "Show the Doubt: Visualizing Segmentation Uncertainty in 3D Renderings"
parent: "CBIO064T - Automated 3D Cell Visualization (source abstract, 2025)"
---

# Show the Doubt

**Parent project:** CBIO064T Automated 3D Cell Visualization (Cellpose 2.0 auto-outlining of z-stack slices, cross-height/time cell linking, mesh rendering and side-by-side comparison).

## Premise
A 3D rendering looks equally confident everywhere, even where segmentation was a guess. Users then measure or interpret wrong cells. If the software could color each cell by how sure the model was, users could check only the doubtful ones. This requires an uncertainty score that actually tracks errors.

## Hypothesis
Per-cell uncertainty from test-time augmentation disagreement ranks segmentation errors with AUROC >= 0.80, so reviewing the 10% most uncertain cells catches >= 50% of errors.

## Data sources (free/public)
- CTC, PlantSeg and Allen Cell datasets with ground truth.
- Cellpose (free); napari for 3D display (free).

## Method outline
1. Segment with test-time augmentation (flips, rotations, slight rescaling); compute per-cell IoU disagreement across runs.
2. Also compute Cellpose's cell probability and flow error as alternative scores.
3. Label each predicted cell as correct/incorrect against ground truth (IoU >= 0.5 match).
4. Rank cells by each score; measure error-catch curves; render uncertainty as color in 3D.
5. Small user test: time and errors caught with vs without uncertainty coloring (volunteers, no personal data).

## Success gates (locked before results)
- G1: best score AUROC >= 0.80 for error detection on >= 3 datasets.
- G2: top-10% review catches >= 50% of errors.
- G3: user-test results reported with sample size stated; labeled exploratory if n < 10.

## Expected deliverable
An uncertainty-coloring feature for 3D viewers and error-catch curves.

## Failure/pivot rule
If no score reaches AUROC 0.80 (G1 fails), train a small error-prediction model on shape and intensity features and test it on a held-out dataset.
