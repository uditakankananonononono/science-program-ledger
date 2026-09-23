---
id: P01-08
title: "Signal or Snapshot? Longitudinal Stability of CRC Microbiome Markers, and a Stability-Weighted Classifier"
parent: "CBIO003 - Colorectal Cancer Detection From Gut Microbiome (source abstract, 2025)"
---

# Signal or Snapshot? Longitudinal Stability of CRC Microbiome Markers

**Parent project:** CBIO003 - single-stool-sample classifier.

## Premise
A screening marker is only useful if it is stable within a person across weeks and robust to diet and antibiotics. Marker volatility is measurable from public longitudinal cohorts.

## Hypothesis
A measurable fraction of top CRC markers are volatile; a stability-weighted classifier is more robust to perturbation at small accuracy cost.

## Data sources (free/public)
- iHMP-IBD (Lloyd-Price 2019) multi-timepoint metagenomes.
- David 2014 diet-perturbation cohort; antibiotic time series on SRA/MGnify.
- Repeat-sampling subsets of CRC cohorts where available.

## Method outline
1. Per-taxon intraclass correlation (ICC) over time in healthy and perturbed arms.
2. Score the top-50 CRC markers (from P01-01/P01-03) for temporal ICC, diet-response and antibiotic-response fold-changes.
3. Train a stability-weighted classifier (features downweighted by volatility) vs the parent's unweighted RF under simulated perturbation.

## Success gates (locked before results)
- G1: stability scorecard published for all top-50 markers; none used downstream without an ICC.
- G2: >= 60% of top markers with ICC >= 0.4, else "snapshot signal" declared a major limitation.
- G3: stability-weighted model loses < 0.03 AUC under perturbation while the unweighted model loses >= 0.05, else weighting declared non-beneficial.

## Expected deliverable
`stabl`: a taxon-level stability database (ICC + perturbation responses) plus a plug-in weighting layer for any microbiome classifier.

## Failure/pivot rule
If CRC markers prove broadly unstable, publish the stability audit with concrete repeat-sampling design guidance - no silent restriction to stable markers before reporting the failure rate.
