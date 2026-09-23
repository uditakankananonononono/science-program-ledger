---
id: P22-09
title: "Whole-Tissue 4D: Scaling Automated Visualization to Developing Embryos and Organoids"
parent: "CBIO064T - Automated 3D Cell Visualization (source abstract, 2025)"
---

# Whole-Tissue 4D

**Parent project:** CBIO064T Automated 3D Cell Visualization (Cellpose 2.0 auto-outlining of z-stack slices, cross-height/time cell linking, mesh rendering and side-by-side comparison).

## Premise
The parent's examples are small cell groups. Light-sheet microscopy now images whole developing embryos and organoids with thousands of cells over time. Public datasets exist with tracked lineages. The question is whether the parent's pipeline design (2D segmentation, linking, rendering) scales, and what breaks first: memory, segmentation, or linking.

## Hypothesis
The parent-style pipeline handles >= 1,000 cells per time point with linking accuracy (TRA) >= 0.85 on sparse early stages, but accuracy drops below 0.7 once cell density passes a measurable threshold.

## Data sources (free/public)
- Cell Tracking Challenge embryo datasets (e.g., C. elegans, Tribolium light-sheet; public).
- BioImage Archive / IDR public light-sheet organoid and embryo datasets.
- Ultrack for comparison.

## Method outline
1. Run the parent-style pipeline on embryo time series; record memory, runtime and TRA per time window.
2. Plot accuracy vs cells per time point and local density.
3. Replace the weakest step (by error attribution) with a scalable alternative (chunked processing, Ultrack linking) and re-measure.
4. Render lineage-colored 4D views as the user-facing output.

## Success gates (locked before results)
- G1: accuracy-vs-density curve reported on >= 2 embryo datasets.
- G2: density threshold where TRA < 0.7 identified, or none within the data range.
- G3: the replacement step improves TRA by >= 0.05 past the threshold, or the null is reported.

## Expected deliverable
A scaling report, a chunked processing mode, and lineage-colored 4D renderings.

## Failure/pivot rule
If memory fails before accuracy does, focus on out-of-core processing (Zarr/OME-NGFF chunking) and report the achievable dataset size on a laptop.
