---
id: P02-10
title: "A Blood/CSF Ferroptosis Biomarker Panel to Stratify Patients for Anti-Ferroptosis Trials"
parent: "CBIO006 - Biclonal Antibodies to Prevent Ferroptosis in AD (source abstract, 2025)"
---

# A Blood/CSF Ferroptosis Biomarker Panel for Trial Stratification

**Parent project:** CBIO006 - any anti-ferroptosis AD therapy needs to identify and track "ferroptosis-high" patients.

## Premise
A peripheral panel of ferroptosis-pathway proteins/metabolites, derived from public cohort omics, could stratify patients and serve as a target-engagement readout.

## Hypothesis
A <= 4-analyte panel replicates association with cognitive decline in >= 2 cohorts and adds discriminative value over age/sex/APOE4.

## Data sources (free/public)
- AMP-AD / Emory Goizueta public CSF and plasma proteomics; ADNI public data use tier.
- UK Biobank Olink neurodegeneration subset; lipid-peroxidation marker literature.

## Method outline
1. Lock candidate analytes from the FerrDb pathway (GPX4, ferritin subunits, transferrin, ceruloplasmin, 4-HNE/MDA proxies, acylcarnitines).
2. Per cohort: association with diagnosis and longitudinal decline slope (covariate-adjusted).
3. Stability selection of a minimal panel; evaluate as enrichment diagnostic and decline predictor; brain-periphery concordance where matched tissue exists.

## Success gates (locked before results)
- G1: >= 4-analyte panel replicating decline association in >= 2 independent cohorts (FDR < 0.1, same direction), else stratification declared unsupported.
- G2: panel adds >= 0.03 AUC over age/sex/APOE4 baseline, else clinical utility rejected.
- G3: brain-periphery discordance reported explicitly where testable.

## Expected deliverable
`ferrostrat`: harmonized multi-cohort analyte matrix, locked panel-selection code, and a stratification-score calculator for trial designers.

## Failure/pivot rule
If no panel replicates, publish the powered stratification negative with the exact effect sizes excluded at achieved power - the field currently lacks a peripheral ferroptosis readout.
