---
id: P22-01
title: "Stitch or Native 3D: Benchmarking 2D-Stitched vs Native 3D Cell Segmentation"
parent: "CBIO064T - Automated 3D Cell Visualization (source abstract, 2025)"
---

# Stitch or Native 3D

**Parent project:** CBIO064T Automated 3D Cell Visualization (Cellpose 2.0 auto-outlining of z-stack slices, cross-height/time cell linking, mesh rendering and side-by-side comparison).

## Premise
The parent segments each 2D slice with Cellpose and then links outlines across heights. Native 3D methods (Cellpose 3D mode, StarDist-3D, PlantSeg) segment the volume directly. Nobody has measured, on shared ground truth, when slice-then-stitch is good enough and when it breaks - for example with touching cells, thin z-spacing, or elongated shapes.

## Hypothesis
Slice-and-stitch matches native 3D within 0.05 average precision (AP@0.5) for round, well-separated cells, but falls behind by >= 0.15 for dense or elongated cells.

## Data sources (free/public)
- Cell Tracking Challenge 3D datasets with ground truth (public).
- PlantSeg benchmark datasets (Wolny et al. 2020, public) for dense tissue.
- Allen Cell WTC-11 hiPSC single-cell image dataset (public) for nuclei/cell membranes.

## Method outline
1. Run Cellpose (2D per slice + stitching, the parent approach), Cellpose 3D mode, StarDist-3D and PlantSeg on each dataset.
2. Score AP at IoU 0.5 and 0.75, merge and split error counts, per dataset.
3. Stratify results by cell density, elongation and z-anisotropy.
4. Record runtime and GPU memory, since the parent's users may lack GPUs.

## Success gates (locked before results)
- G1: all methods scored on identical ground truth with 95% bootstrap CIs over cells.
- G2: the density/elongation crossover point where stitching falls >= 0.15 AP behind is identified, or no crossover is reported.
- G3: runtime table on CPU and free-tier GPU.

## Expected deliverable
A benchmark table and a decision guide: "for your sample type, use method X."

## Failure/pivot rule
If stitching is never worse (no crossover), report that and focus follow-up on linking errors across time instead (see P22-02).
