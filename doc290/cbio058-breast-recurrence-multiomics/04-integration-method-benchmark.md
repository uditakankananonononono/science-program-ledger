---
id: P20-04
title: "Integration Face-Off: Does Fancy Multi-Omic Integration Beat Simple Baselines for Recurrence"
parent: "CBIO058 - Deep-Learning to Predict Breast Cancer Recurrence (source abstract, 2023)"
---

# Integration Face-Off

**Parent project:** CBIO058 Breast Recurrence (AIME autoencoder integrating expression + CNV with ER-status confounder adjustment, random forest recurrence classifier, 25-gene list).

## Premise
The parent used AIME, a specialized autoencoder, to merge expression and copy number. Benchmarks of multi-omic integration (e.g., Cantini et al. 2021 Nat Commun) often find that simple methods match complex ones, and that expression alone carries most prognostic signal in breast cancer. Nobody has tested AIME against simple alternatives on the same recurrence task.

## Hypothesis
Expression-only elastic-net Cox matches AIME-embedding models within 0.02 C-index, and no integration method adds >= 0.03 over expression alone.

## Data sources (free/public)
- TCGA-BRCA open-tier expression, CNV, miRNA, methylation, mutation; Liu 2018 endpoints.
- METABRIC expression + CNA for external testing.
- MOFA+, mixOmics DIABLO, and autoencoder code (all free).

## Method outline
1. Methods: single-omic baselines (each layer), early concatenation, MOFA+, DIABLO, a plain autoencoder, and an AIME-style confounder-adjusted autoencoder.
2. Same outcome (PFI), same folds, same downstream survival model for every method.
3. External test on METABRIC for methods using expression + CNA.
4. Report runtime and number of tunable settings as practical costs.

## Success gates (locked before results)
- G1: every method evaluated on identical folds with 95% CIs (10 x 5-fold CV).
- G2: the claim "integration helps" requires >= 0.03 C-index over the best single layer in both TCGA CV and METABRIC; otherwise the null is the result.
- G3: ranking stability reported across folds (Kendall tau).

## Expected deliverable
A fair benchmark table, reusable fold definitions, and practical guidance on when integration is worth it.

## Failure/pivot rule
If no method beats expression alone (G2 fails), pivot to finding which patients (subtype, stage) benefit from CNA information, testing for subgroup-level gains.
