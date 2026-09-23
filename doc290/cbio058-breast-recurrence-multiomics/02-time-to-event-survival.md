---
id: P20-02
title: "Time Matters: Survival Modeling Instead of Binary Recurrence Labels"
parent: "CBIO058 - Deep-Learning to Predict Breast Cancer Recurrence (source abstract, 2023)"
---

# Time Matters

**Parent project:** CBIO058 Breast Recurrence (AIME autoencoder integrating expression + CNV with ER-status confounder adjustment, random forest recurrence classifier, 25-gene list).

## Premise
The parent classified patients as "disease-free" or "recurred." That throws away when recurrence happened and mislabels censored patients - someone followed for only one year who has not recurred yet is not truly disease-free. Survival models handle censoring directly and answer the question clinicians ask: risk over time.

## Hypothesis
Time-to-event models (Cox-PH, DeepSurv, random survival forest) on AIME-style multi-omic embeddings beat the binary random-forest approach in time-dependent AUC at 5 years by >= 0.05, mainly by correctly using censored patients.

## Data sources (free/public)
- TCGA-BRCA open-tier expression, CNV, miRNA and mutation data; Liu 2018 curated PFI/DFI endpoints.
- METABRIC (cBioPortal) with long follow-up for external testing (expression + CNA).
- scikit-survival and pycox (free).

## Method outline
1. Rebuild the parent pipeline (integrated embedding + random forest binary label) as baseline.
2. Fit Cox-PH (elastic net), random survival forest and DeepSurv on the same embeddings, using PFI with censoring.
3. Train on TCGA, test on METABRIC using expression + CNA (the shared layers).
4. Report Harrell's C, time-dependent AUC at 3/5/10 years, and calibration.

## Success gates (locked before results)
- G1: best survival model beats the binary baseline by >= 0.05 time-dependent AUC at 5 years in METABRIC.
- G2: C-index >= 0.65 in METABRIC.
- G3: calibration slope within 0.8-1.2 at 5 years; all numbers with 95% bootstrap CIs.

## Expected deliverable
A survival-model benchmark on multi-omic embeddings and a risk calculator returning 5-year recurrence probability.

## Failure/pivot rule
If survival models do not beat the binary approach (G1 fails), quantify how much censoring mislabeling exists in TCGA binary labels and publish corrected label sets.
