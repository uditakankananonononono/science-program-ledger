---
id: P20-10
title: "More Than ER: Generalizing Confounder Adjustment in Recurrence Embeddings"
parent: "CBIO058 - Deep-Learning to Predict Breast Cancer Recurrence (source abstract, 2023)"
---

# More Than ER

**Parent project:** CBIO058 Breast Recurrence (AIME autoencoder integrating expression + CNV with ER-status confounder adjustment, random forest recurrence classifier, 25-gene list).

## Premise
AIME's key idea was to adjust the embedding for one confounder, ER status. But recurrence predictions are also confounded by age, tumor purity, treatment era and batch (tissue source site). A model that learns "low purity sample" or "treated in 2005" is not learning tumor biology. This project extends the adjustment to several confounders and measures how much the recurrence signal changes.

## Hypothesis
Adjusting for tumor purity and tissue source site, in addition to ER, changes the top-25 gene list by >= 40% but reduces C-index by <= 0.02 - meaning part of the original list reflected confounding.

## Data sources (free/public)
- TCGA-BRCA open-tier omics; ABSOLUTE/ESTIMATE purity estimates (public).
- Tissue source site codes from TCGA barcodes; Liu 2018 endpoints.
- METABRIC for external check.

## Method outline
1. Rebuild an AIME-style autoencoder with an adversarial or residualization head for multiple confounders (ER, purity, age, source site).
2. Compare embeddings: no adjustment, ER only, ER + purity, all confounders.
3. For each, fit the same survival model and extract top genes by importance.
4. Measure how well each embedding still predicts the confounders (lower is better).

## Success gates (locked before results)
- G1: confounder predictability from the fully adjusted embedding drops to near chance (AUROC <= 0.60 for binary confounders).
- G2: C-index change reported with 95% CI for each adjustment level.
- G3: gene list overlap (Jaccard) between adjustment levels reported; validated genes in METABRIC flagged.

## Expected deliverable
A multi-confounder integration method, a gene-list stability analysis, and guidance on which confounders matter for recurrence modeling.

## Failure/pivot rule
If adjustment removes most recurrence signal (C-index falls > 0.05), report that the original signal was largely confounded and identify which confounder was responsible.
