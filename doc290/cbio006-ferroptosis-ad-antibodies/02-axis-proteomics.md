---
id: P02-02
title: "Quantifying the Hepcidin-Ferroportin Axis in Public AD Proteomics, and a Protein-Panel Disease Classifier"
parent: "CBIO006 - Biclonal Antibodies to Prevent Ferroptosis in AD (source abstract, 2025)"
---

# Quantifying the Hepcidin-Ferroportin Axis in Public AD Proteomics

**Parent project:** CBIO006 - premise that ferroportin is depleted (or hepcidin elevated) in AD, justifying axis-targeting antibodies.

## Premise
The premise must hold at protein level in human tissue. Public brain/CSF proteomics can confirm or kill it directly - and the same proteins can be tested as a disease-panel classifier.

## Hypothesis
SLC40A1/HAMP-axis proteins are measurably, consistently dysregulated across orthogonal proteomics platforms, and a small panel of them discriminates AD from control out of sample.

## Data sources (free/public)
- AMP-AD TMT proteomics (ROSMAP, Banner, Mount Sinai); CSF SomaScan/Olink AD datasets (synapse).
- PRIDE-hosted AD brain proteomes; Human Protein Atlas reference levels.

## Method outline
1. Extract SLC40A1, HAMP, ceruloplasmin, transferrin, ferritin subunits per dataset; covariate-adjusted contrasts (age/sex/pH/PMI).
2. Cross-platform concordance (TMT vs SomaScan vs Olink); brain-CSF correlation.
3. Train a <= 6-protein elastic-net panel classifier on the largest dataset; locked threshold; external validation on the remaining datasets.

## Success gates (locked before results)
- G1: premise verdict from locked criteria: consistent axis dysregulation in >= 2 orthogonal platforms at FDR < 0.1 = supported.
- G2: panel classifier external AUC >= 0.70 on >= 2 held-out datasets, else panel utility rejected.
- G3: below-detection proteins reported as missingness, never silently imputed.

## Expected deliverable
`axisaudit`: reproducible proteomics re-analysis capsule + trained panel classifier + a target-validation scorecard template reusable for any neurodegeneration target premise.

## Failure/pivot rule
If the axis is not measurably dysregulated, report that the antibody program targets the wrong node, with the full evidence table - the negative redirects the parent.
