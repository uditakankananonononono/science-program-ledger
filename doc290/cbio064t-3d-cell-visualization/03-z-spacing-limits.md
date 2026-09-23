---
id: P22-03
title: "Fewer Slices: How Coarse Can Z-Sampling Be Before 3D Reconstruction Fails"
parent: "CBIO064T - Automated 3D Cell Visualization (source abstract, 2025)"
---

# Fewer Slices

**Parent project:** CBIO064T Automated 3D Cell Visualization (Cellpose 2.0 auto-outlining of z-stack slices, cross-height/time cell linking, mesh rendering and side-by-side comparison).

## Premise
Every extra z-slice costs imaging time and light exposure, which damages live cells (phototoxicity). Biologists often take more slices than needed, or too few, without a rule. With high-resolution public stacks, we can drop slices on purpose and measure when segmentation and 3D shape measurements break. That gives a practical rule for how to image.

## Hypothesis
Cell volume and surface-area estimates stay within 10% of full-resolution values until z-spacing exceeds about one-third of the median cell diameter, then degrade quickly.

## Data sources (free/public)
- Allen Cell WTC-11 hiPSC single-cell image dataset (high-resolution 3D, public).
- Cell Tracking Challenge and PlantSeg 3D datasets with ground truth.

## Method outline
1. Take full-resolution stacks; simulate coarser acquisition by dropping slices (every 2nd, 3rd, ... 10th) with matching blur.
2. Segment each version (parent-style stitch and native 3D); reconstruct meshes.
3. Compare volume, surface area, sphericity and cell count to full-resolution ground truth.
4. Express the failure point relative to cell diameter so it transfers across sample types.

## Success gates (locked before results)
- G1: error curves for each metric across >= 5 spacing levels on >= 3 datasets.
- G2: a spacing threshold (as fraction of cell diameter) with <= 10% volume error identified and consistent (+/- 30%) across datasets, or dataset-specific thresholds reported.
- G3: upsampling/interpolation methods tested as a rescue, results kept whether or not they help.

## Expected deliverable
A "how many slices do I need" calculator and error curves for common cell types.

## Failure/pivot rule
If no consistent threshold exists (G2 fails), publish per-dataset curves and the features (shape, density) that explain differences.
