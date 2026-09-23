---
id: P21-06
title: "Patient-Level IL-6 Models: Personalizing the Model With Tumor Expression and Testing Prognosis"
parent: "CBIO060 - A Mathematical Model of IL-6 in Breast Cancer (source abstract, 2023)"
---

# Patient-Level IL-6 Models

**Parent project:** CBIO060 IL-6 TNBC Model (48-ODE model of IL-6 signal transduction in triple-negative breast cancer; sensitivity analysis and virtual drug-target screening).

## Premise
The parent's model describes a generic TNBC cell. Tumors differ in how much of each pathway component they express. Scaling model parameters by each patient's expression (as done for other signaling models, e.g., Fey et al. 2015 Sci Signal for JNK in neuroblastoma) turns one model into many patient models. If the model captures real biology, simulated IL-6 pathway output should relate to outcomes.

## Hypothesis
Patient-specific simulated steady-state pSTAT3 separates TNBC survival (HR >= 1.5 high vs low) better than raw IL6 or STAT3 expression alone.

## Data sources (free/public)
- TCGA-BRCA TNBC subset (open-tier RNA-seq, Liu 2018 endpoints).
- METABRIC TNBC subset (cBioPortal).
- GSE25066 TNBC patients (see P20-07) for relapse outcomes.

## Method outline
1. Scale total-protein parameters (receptor, JAK, STAT3, SOCS3 levels) by each patient's expression relative to the cohort median.
2. Simulate steady state and IL-6 response per patient; extract pSTAT3 and IL-6 output.
3. Test association with survival (Cox, adjusted for stage and age) in METABRIC and TCGA TNBC.
4. Compare against single-gene expression and a simple pathway score (mean z-score) as baselines.

## Success gates (locked before results)
- G1: simulated output HR >= 1.5 (p < 0.05) in >= 1 cohort, with direction consistent in the other.
- G2: beats the simple pathway score in C-index by >= 0.02; otherwise "mechanistic modeling adds nothing here" is the result.
- G3: sensitivity to scaling choices reported.

## Expected deliverable
A patient-personalization pipeline for the IL-6 model and a prognostic comparison table.

## Failure/pivot rule
If no prognostic signal (G1 fails), test prediction of treatment response instead (pCR in GSE25066), where pathway state may matter more than baseline prognosis.
