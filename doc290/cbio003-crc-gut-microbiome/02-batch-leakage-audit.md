---
id: P01-02
title: "How Real Is AUC 0.99? Adversarial Batch and Leakage Audit of Single-Cohort CRC Microbiome Models"
parent: "CBIO003 - Colorectal Cancer Detection From Gut Microbiome (source abstract, 2025)"
---

# How Real Is AUC 0.99? Adversarial Batch and Leakage Audit

**Parent project:** CBIO003 - Random Forest CRC classifier reporting AUC 0.992 on an Indian-population cohort.

## Premise
Near-perfect AUCs in single-cohort microbiome studies often reflect technical confounding (sequencing center, extraction kit, read depth) more than biology. The confounded fraction is measurable with adversarial models.

## Hypothesis
A measurable share of the parent's headline accuracy is technical signal; after adversarial batch correction the biological AUC is substantially lower but still real.

## Data sources (free/public)
- curatedMetagenomicData cohorts with per-study metadata.
- SRA run tables (extraction kit, platform, read depth) via the SRA Run Selector API.

## Method outline
1. Train confound classifiers predicting CRC status from technical metadata alone (no sequences).
2. Train an adversarial MLP with gradient-reversal that predicts CRC while being unable to predict batch; measure AUC delta vs unprotected model.
3. ComBat batch correction + retrain as second arm.
4. Label-permutation null (100 permutations preserving batch structure) for a leakage-adjusted AUC per cohort.

## Success gates (locked before results)
- G1: metadata-only classifier AUC reported per cohort; any cohort with metadata AUC >= 0.80 flagged confounded in the headline output.
- G2: leakage-adjusted AUC with permutation CI; a cohort passes at adjusted AUC >= 0.70, p < 0.01.
- G3: per-cohort verdicts delivered before any pooled modeling; no merged hero number hiding a flagged cohort.

## Expected deliverable
`batchtruth`: R/Python package taking a feature table + SRA metadata and emitting a confounding report (metadata-only AUC, adversarial and ComBat adjusted AUCs, flagged batches) with a reproducibility capsule.

## Failure/pivot rule
If most cohorts fail G2 after correction, publish the audit of how much headline accuracy is technical signal - locked as a valid outcome; no selective cohort dropping after seeing adjusted scores.
