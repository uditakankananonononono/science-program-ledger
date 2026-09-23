---
id: P20-05
title: "Slides Plus Omics: Fusing H&E Whole-Slide Images With Multi-Omics for Recurrence"
parent: "CBIO058 - Deep-Learning to Predict Breast Cancer Recurrence (source abstract, 2023)"
---

# Slides Plus Omics

**Parent project:** CBIO058 Breast Recurrence (AIME autoencoder integrating expression + CNV with ER-status confounder adjustment, random forest recurrence classifier, 25-gene list).

## Premise
Every breast cancer patient gets an H&E slide; few get multi-omic profiling. TCGA diagnostic slides are open-tier on GDC. Pathology foundation models now produce strong slide embeddings for free (e.g., UNI, CONCH, Virchow with academic access; open alternatives such as CTransPath). This project tests whether slides can replace or add to the parent's omic inputs.

## Hypothesis
Slide-only models reach within 0.03 C-index of omics-only models for recurrence, and slide + omics fusion beats either by >= 0.03.

## Data sources (free/public)
- TCGA-BRCA diagnostic H&E whole-slide images (GDC open access).
- TCGA-BRCA open-tier omics and Liu 2018 endpoints.
- Open pathology feature extractors (CTransPath or other openly licensed weights); CLAM for attention-based multiple-instance learning.

## Method outline
1. Tile slides at 20x, extract tile features with an open pathology encoder, aggregate with attention MIL.
2. Train slide-only, omics-only and late-fusion survival models on identical patient folds.
3. Visualize attention maps for high-risk predictions; have tiles reviewed against known risk morphology (grade, necrosis, lymphocytes).
4. Check site-of-origin leakage: slides carry tissue-source-site staining signatures, so use site-stratified splits.

## Success gates (locked before results)
- G1: slide-only C-index within 0.03 of omics-only under site-stratified CV.
- G2: fusion beats best single modality by >= 0.03 C-index.
- G3: site-stratified vs random split gap reported; a large gap is declared as stain/site leakage.

## Expected deliverable
Slide embeddings for TCGA-BRCA, a fusion benchmark, and attention-map examples.

## Failure/pivot rule
If site leakage dominates (G3), pivot to stain-normalization and site-adversarial training and report how much real signal remains.
