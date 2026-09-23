---
id: P23-03
title: "Patient Data Test: Testing Game Models on Intermittent Androgen Deprivation PSA Trajectories"
parent: "CBIO083 - Quantum Game Theory to Simulate Cancer Dynamics (source abstract, 2026)"
---

# Patient Data Test

**Parent project:** CBIO083 Quantum Game Theory Cancer Dynamics (Lindblad master-equation QGT model with leaky integrator fit to the Kaznatcheev alectinib/fibroblast NSCLC game assay; beat classical replicator models by 10-20%).

## Premise
Cell-culture wells are clean; patients are not. The parent's goal is to "mitigate the effects of drug resistance," which needs models that work on patient data. The Bruchovsky et al. 2006 phase II intermittent androgen suppression trial released PSA and testosterone time series per patient (public on figshare), and adaptive-therapy models have been fit to it before. This is a direct test on human longitudinal data.

## Hypothesis
Quantum-inspired game models predict next-cycle PSA trajectories no better than memory-classical models (difference < 5% error), because patient noise swamps structural differences.

## Data sources (free/public)
- Bruchovsky 2006 intermittent androgen suppression trial data (figshare, doi 10.6084/m9.figshare.16847362).
- Published adaptive-therapy models (Zhang et al. 2017 Nat Commun) as baselines.

## Method outline
1. Model androgen-dependent and independent cell populations as strategies; PSA as a weighted readout; treatment on/off from trial records.
2. Fit classical EGT, memory-classical and QGT variants per patient on early cycles.
3. Predict PSA for the next cycle(s); score error and time-to-resistance prediction.
4. Use hierarchical (population-level) fitting to limit overfitting per patient.

## Success gates (locked before results)
- G1: all models fit with the same number of patient-level free parameters.
- G2: next-cycle prediction error compared with paired tests across patients; any model beating others by >= 10% with p < 0.05 is declared better, otherwise tie is reported.
- G3: resistance-onset prediction evaluated in patients who progressed.

## Expected deliverable
A clinical-data benchmark for game-theoretic cancer models and per-patient forecasts.

## Failure/pivot rule
If all models fail at next-cycle prediction, report the forecast horizon at which any model beats a naive last-cycle baseline.
