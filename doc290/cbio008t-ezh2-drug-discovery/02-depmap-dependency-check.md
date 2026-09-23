---
id: P03-02
title: "Is EZH2 Really a Neuroblastoma Dependency? DepMap Verification and a Dependency-Prediction Model"
parent: "CBIO008T - Deep Learning Pipeline for EZH2 Drug Discovery (source abstract, 2023)"
---

# Is EZH2 Really a Neuroblastoma Dependency?

**Parent project:** CBIO008T - EZH2 chosen as target from CRISPR screens; the dependency claim deserves verification and quantification before drug design.

## Premise
Target selection is the highest-leverage decision in the pipeline. Public DepMap data can verify EZH2 essentiality in NB lines, identify which lines, and train a model predicting dependency from baseline omics.

## Hypothesis
EZH2 dependency is strong specifically in MYCN-amplified / PRC2-high NB lines, and a small expression-based classifier predicts it in held-out lines.

## Data sources (free/public)
- DepMap 24Q public releases (CRISPR Chronos scores, expression, copy number).
- CCLE annotations; pediatric dependency map (Pediatric DepMap) where available.

## Method outline
1. Extract EZH2 (and PRC2 partners EED/SUZ12) Chronos scores across all NB lines; compare vs other lineages and vs a null of non-essential genes.
2. Stratify by MYCN status, stage, PRC2 expression; effect sizes with CIs.
3. Train an elastic-net classifier (expression features) predicting EZH2-dependent lines; leave-one-lineage-out validation.

## Success gates (locked before results)
- G1: EZH2 mean Chronos in NB lines <= -0.5 with CI excluding 0, else the target premise is downgraded and reported.
- G2: dependency-prediction classifier AUC >= 0.75 on held-out lines, else dependency declared unpredictable from baseline expression.
- G3: stratification analysis pre-registered in the repo before results.

## Expected deliverable
`targetcheck`: a reusable DepMap target-verification tool - given any gene and cancer type, returns dependency evidence, stratification, and a trained predictor.

## Failure/pivot rule
If EZH2 fails G1 in NB, publish the verification negative and rank the top alternative PRC2-axis targets by the same locked criteria.
