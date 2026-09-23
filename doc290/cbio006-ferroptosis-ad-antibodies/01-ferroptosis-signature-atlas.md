---
id: P02-01
title: "A Ferroptosis Score Classifier Across Alzheimer's Brain Atlases: Does the Signature Replicate and Discriminate?"
parent: "CBIO006 - Biclonal Antibodies to Prevent Ferroptosis in AD (source abstract, 2025)"
---

# A Ferroptosis Score Classifier Across Alzheimer's Brain Atlases

**Parent project:** CBIO006 - therapeutic premise that ferroptosis/iron dysregulation drives AD, targeted via hepcidin-ferroportin antibodies.

## Premise
Before building therapeutics on the ferroptosis-AD link, the dysregulation must replicate across independent cohorts - and a score built from it should actually discriminate AD brains out of sample.

## Hypothesis
A locked ferroptosis gene set (FerrDb-derived: GPX4, ACSL4, SLC7A11, FTH1, FTL, TFRC, SLC40A1) is consistently dysregulated across AD brain atlases, and a sparse classifier on it generalizes across cohorts.

## Data sources (free/public)
- AMP-AD: ROSMAP, MayoRNAseq, Mount Sinai Brain Bank (synapse, open tier).
- Allen Aging/Dementia (SEA-AD) and GEO AD series.
- FerrDb V2 (public ferroptosis gene database).

## Method outline
1. Lock the gene set from FerrDb before touching outcomes.
2. Per-cohort covariate-adjusted DE; random-effects meta-analysis per gene and region (I^2 heterogeneity).
3. Train an elastic-net ferroptosis-score classifier on the largest cohort; leave-one-cohort-out validation; compare against age/sex/APOE baseline.

## Success gates (locked before results)
- G1: set-level dysregulation (competitive test FDR < 0.05) in >= 3 cohorts with consistent direction for >= 60% of core genes.
- G2: ferroptosis-score classifier LOCO AUC >= 0.65 and adds >= 0.03 over the age/sex/APOE baseline.
- G3: if I^2 > 75% with inconsistent direction, "ferroptosis dysregulation is not a stable AD feature" is declared.

## Expected deliverable
`ferroatlas`: R package + frozen per-cohort result tables and the trained score classifier, with a web explorer for any user gene set across AMP-AD cohorts.

## Failure/pivot rule
If replication or the classifier fails, publish the powered negative meta-analysis as the basis for redirecting the parent project's target choice.
