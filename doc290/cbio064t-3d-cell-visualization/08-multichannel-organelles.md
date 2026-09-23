---
id: P22-08
title: "Inside the Cell: Extending Automated 3D Visualization to Nuclei and Organelles"
parent: "CBIO064T - Automated 3D Cell Visualization (source abstract, 2025)"
---

# Inside the Cell

**Parent project:** CBIO064T Automated 3D Cell Visualization (Cellpose 2.0 auto-outlining of z-stack slices, cross-height/time cell linking, mesh rendering and side-by-side comparison).

## Premise
The parent visualizes whole cells. Many biology questions are about what is inside: nuclear shape, mitochondrial networks, organelle positions. The Allen Cell collection images many tagged structures (mitochondria, Golgi, ER, nucleoli and more) in 3D with segmentations. Extending automation to multiple channels would let users see and measure where organelles sit inside each cell.

## Hypothesis
Organelle position relative to the nucleus (radial distribution) differs between cell-cycle stages for >= 3 structures, detectable from automated 3D segmentations.

## Data sources (free/public)
- Allen Cell WTC-11 hiPSC dataset: tagged structures with 3D segmentations and cell-cycle labels.
- Allen Cell Structure Segmenter (free) and Cellpose nuclei model.

## Method outline
1. Use provided cell, nucleus and structure segmentations; also run an automated pipeline (Cellpose + Structure Segmenter) to test the tool path.
2. Compute radial organelle distributions in a normalized cell coordinate frame (nucleus center to membrane).
3. Compare distributions across cell-cycle stages (Wasserstein distance with permutation tests).
4. Add multichannel rendering (per-structure color toggles, as in the parent's color on/off feature).

## Success gates (locked before results)
- G1: >= 3 structures with stage-dependent radial shifts (permutation p < 0.01, FDR-controlled).
- G2: automated segmentations reproduce >= 80% of the curated-segmentation effects.
- G3: effect sizes with 95% CIs; imaging-session-held-out checks.

## Expected deliverable
Multichannel 3D rendering, an organelle-position analysis module, and a stage-by-structure effect map.

## Failure/pivot rule
If few structures shift with stage (G1 fails), report the null and test cell-to-cell variability (which structures vary most in position) as the descriptive result.
