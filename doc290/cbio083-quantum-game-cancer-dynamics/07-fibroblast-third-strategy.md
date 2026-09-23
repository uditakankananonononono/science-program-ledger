---
id: P23-07
title: "Three-Player Game: Adding Cancer-Associated Fibroblasts as an Explicit Strategy"
parent: "CBIO083 - Quantum Game Theory to Simulate Cancer Dynamics (source abstract, 2026)"
---

# Three-Player Game

**Parent project:** CBIO083 Quantum Game Theory Cancer Dynamics (Lindblad master-equation QGT model with leaky integrator fit to the Kaznatcheev alectinib/fibroblast NSCLC game assay; beat classical replicator models by 10-20%).

## Premise
The parent treats fibroblasts as an environment switch (present/absent). In tumors, fibroblast numbers change and respond to cancer cells, so they are players too. Three-strategy games can show cycling (rock-paper-scissors-like) and stable coexistence that two-strategy games cannot. This project tests whether a three-player model explains the fibroblast conditions better.

## Hypothesis
A three-strategy model (sensitive, resistant, fibroblast) with fibroblast dynamics fit to the co-culture wells reduces prediction error in fibroblast conditions by >= 10% compared with the two-strategy environment-switch model.

## Data sources (free/public)
- Kaznatcheev 2019 GameAssay data (fibroblast co-culture conditions; fibroblast counts if available in the image-derived data).
- Published CAF-NSCLC interaction studies for parameter priors.

## Method outline
1. Check whether fibroblast abundance is recorded over time; if not, treat it as a latent variable with priors.
2. Fit three-strategy replicator (classical) and three-level Lindblad (quantum) models.
3. Compare with the two-strategy models on fibroblast-condition wells (leave-one-well-out).
4. Analyze fixed points and stability to see whether coexistence or cycling is predicted.

## Success gates (locked before results)
- G1: >= 10% error reduction in fibroblast conditions for the three-strategy model, or the null is reported.
- G2: parameter identifiability checked (profile likelihood) since fibroblast data may be sparse.
- G3: predicted dynamical regime (coexistence, cycling, exclusion) stated with uncertainty.

## Expected deliverable
Three-strategy game models for tumor-stroma interaction and a regime map across drug conditions.

## Failure/pivot rule
If fibroblast parameters are unidentifiable (G2 fails), report which measurement (fibroblast counts over time) would resolve it and keep the two-strategy model.
