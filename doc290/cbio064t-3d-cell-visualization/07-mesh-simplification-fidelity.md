---
id: P22-07
title: "Lighter Meshes: How Much Can 3D Cell Meshes Be Simplified Without Losing Shape Information"
parent: "CBIO064T - Automated 3D Cell Visualization (source abstract, 2025)"
---

# Lighter Meshes

**Parent project:** CBIO064T Automated 3D Cell Visualization (Cellpose 2.0 auto-outlining of z-stack slices, cross-height/time cell linking, mesh rendering and side-by-side comparison).

## Premise
The parent converts wireframes to meshes for clearer shape. Full-resolution meshes of thousands of cells are heavy to render and share, especially in browsers or on laptops. Mesh simplification cuts triangles, but at some point it changes measured shape. Nobody has put a number on that trade-off for cell morphometrics.

## Hypothesis
Meshes can be reduced to 10% of their triangles while keeping volume within 2% and curvature-based features within 10%, and the break point scales with cell size in voxels.

## Data sources (free/public)
- Allen Cell WTC-11 segmentations; PlantSeg 3D tissue segmentations.
- Tools: marching cubes (scikit-image), quadric decimation (Open3D / PyMeshLab, free).

## Method outline
1. Generate full meshes from segmentations; decimate to 50%, 25%, 10%, 5%, 1% of triangles with quadric and uniform methods.
2. Measure volume, surface area, sphericity, mean curvature and spherical harmonics shape coefficients at each level.
3. Test whether a downstream task (cell-cycle classification from P22-04) keeps accuracy at each level.
4. Measure file size and browser render frame rate (three.js) at each level.

## Success gates (locked before results)
- G1: fidelity curves for all metrics on >= 2 datasets.
- G2: at 10% triangles, volume error <= 2% and downstream accuracy drop <= 0.02; otherwise the safe level is reported.
- G3: size and frame-rate gains quantified.

## Expected deliverable
A recommended simplification level per use (viewing vs measuring) and an export setting for the parent tool.

## Failure/pivot rule
If curvature features break early, recommend dual export (light mesh for viewing, full mesh for measuring) and report the break point.
