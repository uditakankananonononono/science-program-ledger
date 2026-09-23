---
id: P05-04
title: "Tissue-of-Origin from 182 Numbers: A Held-Out-Cancer-Type Classifier on mcSTR Genotypes"
parent: "CBIO013 - Micro-Changing Tandem Repeats in 10 Human Cancers (source abstract, 2023)"
---

# Tissue-of-Origin from 182 Numbers

**Parent project:** CBIO013 - 98% of mcSTRs reported subtype-specific, permitting tissue-of-origin detection.

## Premise
Subtype specificity is exactly what a tissue-of-origin classifier needs - and exactly what must be validated with cancer types fully held out, not random sample splits.

## Hypothesis
A multinomial classifier on mcSTR genotype features assigns cancer type with top-1 accuracy >= 3x chance on held-out samples, and degrades gracefully (rank accuracy) on entirely unseen cancer types.

## Data sources (free/public)
- Genotypes from P05-01's open replication (TCGA WGS + controls).
- ICGC/PCAWG public WGS as an external validation cohort.

## Method outline
1. Build features (length deviations from population mode per locus) with locked normalization.
2. Train multinomial logistic / gradient boosting; nested CV by patient; then leave-one-cancer-type-out evaluation for the unseen-type regime.
3. Calibration analysis; confusion by cancer type; comparison vs mutation-signature-based tissue classifiers as baseline.

## Success gates (locked before results)
- G1: held-out top-1 accuracy >= 3x chance with CI; below that, the tissue-of-origin claim is downgraded.
- G2: unseen-cancer-type behavior reported separately - no pooling with seen types.
- G3: external validation on PCAWG reported; cross-cohort drop > 0.1 AUC declared as transport failure.

## Expected deliverable
`str-origin`: trained classifier + a small API that takes STR genotypes and returns calibrated cancer-type probabilities with the validation certificate.

## Failure/pivot rule
If accuracy fails G1, publish the null: mcSTR subtype specificity is statistical, not classifier-grade - re-scoping the diagnostic claim honestly.
