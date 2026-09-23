---
id: P20-07
title: "TNBC Relapse After Chemo: Predicting Distant Relapse in Triple-Negative Breast Cancer After Neoadjuvant Therapy"
parent: "CBIO058 - Deep-Learning to Predict Breast Cancer Recurrence (source abstract, 2023)"
---

# TNBC Relapse After Chemo

**Parent project:** CBIO058 Breast Recurrence (AIME autoencoder integrating expression + CNV with ER-status confounder adjustment, random forest recurrence classifier, 25-gene list).

## Premise
The parent adjusted for ER status and treated breast cancer as one disease. Triple-negative breast cancer (TNBC) has the highest early recurrence and the fewest targeted options. In neoadjuvant trials, patients with residual disease after chemotherapy relapse far more often. Public cohorts with pre-treatment expression and relapse outcomes exist for this setting.

## Hypothesis
A pre-treatment expression model predicts distant relapse-free survival in TNBC with C-index >= 0.65 across cohorts, and adds value beyond pathologic complete response (pCR) status.

## Data sources (free/public)
- GSE25066 (Hatzis et al. 2011, neoadjuvant taxane-anthracycline, DRFS outcomes).
- GSE58812 (TNBC cohort with outcomes) and METABRIC TNBC subset.
- TCGA-BRCA TNBC subset (open tier).

## Method outline
1. Define TNBC by ER/PR/HER2 clinical status where available, else by expression thresholds (documented).
2. Train elastic-net Cox and random survival forest on GSE25066 TNBC; test on GSE58812 and METABRIC TNBC.
3. Add Lehmann TNBC subtypes and immune signatures as candidate features.
4. Test added value beyond pCR in GSE25066 (pCR available).

## Success gates (locked before results)
- G1: external C-index >= 0.65 in >= 1 of 2 external cohorts.
- G2: adds value beyond pCR (likelihood-ratio p < 0.05) in GSE25066 internal CV.
- G3: platform differences documented; per-cohort 95% CIs.

## Expected deliverable
A TNBC relapse model and a comparison with pCR, immune score and TNBC subtypes.

## Failure/pivot rule
If external validation fails (G1), pivot to an immune-only model (TIL-like expression signature), since immune signal is the most replicated TNBC prognostic factor.
