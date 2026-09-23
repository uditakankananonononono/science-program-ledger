---
id: P23-08
title: "What the Parameters Mean: Mapping Quantum Model Parameters to Measurable Biology"
parent: "CBIO083 - Quantum Game Theory to Simulate Cancer Dynamics (source abstract, 2026)"
---

# What the Parameters Mean

**Parent project:** CBIO083 Quantum Game Theory Cancer Dynamics (Lindblad master-equation QGT model with leaky integrator fit to the Kaznatcheev alectinib/fibroblast NSCLC game assay; beat classical replicator models by 10-20%).

## Premise
A model that predicts better is more useful if its parameters mean something. The QGT model has decoherence rates, coupling terms and integrator time constants. If they change systematically across the four environments (drug on/off, fibroblasts on/off) in ways that match known biology - e.g., fibroblast-secreted HGF rescuing sensitive cells - they become interpretable. If they vary randomly, they are fitting noise.

## Hypothesis
At least two QGT parameters shift consistently with drug and fibroblast conditions (same direction in all replicates, bootstrap CI excluding zero), and these shifts line up with shifts in the classical game matrix entries.

## Data sources (free/public)
- Kaznatcheev 2019 GameAssay data (four environments, replicates).
- Published game matrices from the original paper for comparison.

## Method outline
1. Fit the QGT model separately per environment and replicate; bootstrap over wells.
2. Test each parameter for environment effects (two-way design: drug x fibroblast).
3. Correlate QGT parameter shifts with classical game-matrix shifts from the original analysis.
4. Check identifiability first (profile likelihood), so non-identifiable parameters are not interpreted.

## Success gates (locked before results)
- G1: identifiable parameters listed; only those are interpreted.
- G2: >= 2 parameters with consistent environment effects (CI excludes zero), or "parameters are not interpretable" is the finding.
- G3: correlation with classical matrix shifts reported with CI.

## Expected deliverable
A parameter interpretation table and a plain-language mapping from quantum terms to biological effects.

## Failure/pivot rule
If parameters are not interpretable (G2 fails), reframe QGT as a flexible predictor and compare it to other black-box predictors (Gaussian processes) on equal footing.
