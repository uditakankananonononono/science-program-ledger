---
id: P23-05
title: "Space, Not Quantum: Testing Whether Spatial Structure Explains What the Quantum Model Captures"
parent: "CBIO083 - Quantum Game Theory to Simulate Cancer Dynamics (source abstract, 2026)"
---

# Space, Not Quantum

**Parent project:** CBIO083 Quantum Game Theory Cancer Dynamics (Lindblad master-equation QGT model with leaky integrator fit to the Kaznatcheev alectinib/fibroblast NSCLC game assay; beat classical replicator models by 10-20%).

## Premise
Mean-field replicator equations assume every cell interacts with every other cell. In a culture well, cells interact with neighbors, forming clusters. Spatial structure changes game outcomes (Kaznatcheev and others have noted this for the game assay). The quantum model's extra flexibility may be standing in for missing space. An agent-based spatial model tests that alternative.

## Hypothesis
A spatial agent-based model with the classical game matrix matches the QGT model's prediction error within 5%.

## Data sources (free/public)
- Kaznatcheev 2019 GameAssay data, including any time-lapse image-derived counts.
- PhysiCell or a simple lattice model in Python (free).

## Method outline
1. Build a lattice agent-based model where cells play the fitted classical game with neighbors only; vary neighborhood size and initial clustering.
2. Fit to the same frequency time series; compare prediction error to QGT and mean-field EGT.
3. Check whether spatial models reproduce the specific residual patterns QGT fixes (e.g., overshoot or lag).
4. If imaging-derived positions exist, test clustering predictions directly.

## Success gates (locked before results)
- G1: spatial model within 5% of QGT error (hypothesis supported) or not (QGT gain not explained by space).
- G2: residual-pattern comparison reported.
- G3: parameter count and stochastic replicate variance reported.

## Expected deliverable
A spatial game model for the assay and a verdict on whether space explains the quantum gain.

## Failure/pivot rule
If space explains nothing, combine space and memory (P23-01) as a final classical challenger before concluding for quantum structure.
