---
id: P21-08
title: "Ligand Response Check: Validating Pathway Dynamics Against LINCS MCF10A Ligand Perturbation Data"
parent: "CBIO060 - A Mathematical Model of IL-6 in Breast Cancer (source abstract, 2023)"
---

# Ligand Response Check

**Parent project:** CBIO060 IL-6 TNBC Model (48-ODE model of IL-6 signal transduction in triple-negative breast cancer; sensitivity analysis and virtual drug-target screening).

## Premise
The parent's model has not been tested against independent perturbation data. The LINCS MCF10A common project (HMS LINCS, public) measured transcriptomic, proteomic and phenotypic responses of breast epithelial cells to growth factors and cytokines over time, including the IL-6 family ligand oncostatin M (OSM), which signals through the same gp130/JAK/STAT3 axis. Cross-talk with other ligands (e.g., EGF, OSM, TNF) is also measured, so the data can test both the IL-6 core and its boundaries.

## Hypothesis
The model correctly predicts the direction of change for >= 70% of measured IL-6-pathway readouts after IL-6 family ligand stimulation, and fails systematically for readouts driven by cross-talk not in the model.

## Data sources (free/public)
- HMS LINCS MCF10A ligand response datasets (RNA-seq, RPPA, cyclic immunofluorescence; lincs.hms.harvard.edu/mcf10a).
- LINCS L1000 cytokine perturbation signatures (public, clue.io data downloads).

## Method outline
1. Adapt the model's receptor module to OSM (shared gp130/JAK/STAT3 core); keep downstream unchanged.
2. Simulate time courses matching LINCS sampling times; compare with RPPA pSTAT3 and target-gene RNA changes.
3. Score directional agreement and correlation per readout; classify failures by whether a missing cross-talk pathway explains them.
4. Test against other ligands (EGF, TNF-like) as negative/partial controls for model scope.

## Success gates (locked before results)
- G1: >= 70% directional agreement on IL-6/STAT3 core readouts.
- G2: failures concentrated in cross-talk readouts (chi-square p < 0.05), or failures are declared core-model errors.
- G3: MCF10A is non-tumorigenic; transfer to TNBC stated as a limitation.

## Expected deliverable
A validation scorecard and a prioritized list of missing model links.

## Failure/pivot rule
If core agreement is low (G1 fails), recalibrate on LINCS data and test on a held-out ligand dose/time to see whether the structure or the parameters were wrong.
