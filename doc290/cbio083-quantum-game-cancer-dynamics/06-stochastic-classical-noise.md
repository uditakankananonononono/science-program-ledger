---
id: P23-06
title: "Noise Model Check: Stochastic Classical Dynamics vs Lindblad Dissipation"
parent: "CBIO083 - Quantum Game Theory to Simulate Cancer Dynamics (source abstract, 2026)"
---

# Noise Model Check

**Parent project:** CBIO083 Quantum Game Theory Cancer Dynamics (Lindblad master-equation QGT model with leaky integrator fit to the Kaznatcheev alectinib/fibroblast NSCLC game assay; beat classical replicator models by 10-20%).

## Premise
The Lindblad master equation includes dissipation and decoherence - mathematically, a structured way of adding noise and damping. Classical stochastic models (Moran processes, stochastic differential equations with demographic noise) also add noise and damping. If the QGT gain comes from better noise handling, a well-built stochastic classical model should match it.

## Hypothesis
A classical SDE replicator model with fitted demographic and environmental noise matches QGT likelihood on held-out wells within 5%.

## Data sources (free/public)
- Kaznatcheev 2019 GameAssay replicate-level time series.
- Farrokhian 2022 data for a second check.
- Tools: SciPy/sdeint, PyMC or Stan for likelihood-based fitting (free).

## Method outline
1. Estimate replicate-to-replicate variance per condition and time point.
2. Fit SDE replicator models (demographic + environmental noise) by likelihood; fit QGT with a matching observation-noise model.
3. Compare held-out log-likelihood and predictive interval coverage, not only mean error.
4. Simulate synthetic data from each model and check which model family recovers the other's data.

## Success gates (locked before results)
- G1: held-out log-likelihood difference reported with CI; within 5% counts as match.
- G2: 90% predictive intervals cover 85-95% of held-out points for the preferred model.
- G3: cross-recovery simulation reported (can each model mimic the other?).

## Expected deliverable
A noise-aware comparison of classical and quantum game models with calibrated uncertainty.

## Failure/pivot rule
If QGT still wins on likelihood, report which noise structure (correlated, non-Gaussian) the Lindblad form encodes, and build that into a classical model as a final test.
