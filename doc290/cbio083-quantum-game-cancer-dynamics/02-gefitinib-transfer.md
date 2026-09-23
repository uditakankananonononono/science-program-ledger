---
id: P23-02
title: "Second Assay Test: Out-of-Sample Transfer to the Gefitinib Game Assay"
parent: "CBIO083 - Quantum Game Theory to Simulate Cancer Dynamics (source abstract, 2026)"
---

# Second Assay Test

**Parent project:** CBIO083 Quantum Game Theory Cancer Dynamics (Lindblad master-equation QGT model with leaky integrator fit to the Kaznatcheev alectinib/fibroblast NSCLC game assay; beat classical replicator models by 10-20%).

## Premise
The parent fit and tested on one dataset: alectinib-sensitive vs resistant NSCLC with and without fibroblasts. Farrokhian et al. 2022 (Science Advances) ran a related game assay on NSCLC with gefitinib, sensitive vs resistant, measuring competitive exclusion. If the quantum model captures general tumor dynamics, its structure should transfer to a second drug and cell system with refitting of parameters only.

## Hypothesis
With the same model structure, the QGT model keeps a >= 5% prediction-error advantage over classical EGT on the gefitinib dataset.

## Data sources (free/public)
- Farrokhian et al. 2022 Sci Adv game assay data (public supplement/repository linked in paper).
- Kaznatcheev 2019 GameAssay data (training reference).

## Method outline
1. Extract frequency time series per well and condition from the gefitinib dataset.
2. Fit classical EGT, memory-classical (P23-01) and QGT models with the parent's fixed structure; only parameters refit.
3. Evaluate with leave-one-well-out and leave-one-condition-out prediction error.
4. Compare fitted game matrices with those reported in the original paper.

## Success gates (locked before results)
- G1: QGT advantage >= 5% on leave-one-condition-out error, or the loss of advantage is the finding.
- G2: memory-classical comparison reported alongside.
- G3: fitted classical game matrices agree in sign with the published analysis (sanity check).

## Expected deliverable
A two-dataset comparison showing whether the QGT advantage generalizes.

## Failure/pivot rule
If data format prevents time-series fitting (only endpoint fitness reported), switch to fitting endpoint fitness functions and state the reduced test clearly.
