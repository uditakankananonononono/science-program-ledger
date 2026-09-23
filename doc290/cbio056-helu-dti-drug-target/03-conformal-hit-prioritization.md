---
id: P19-03
title: "Trustworthy Hits: Conformal Prediction to Rank DTI Predictions for Wet-Lab Follow-Up"
parent: "CBIO056 - HeLU-DTI: Drug Target Prediction via Deep Learning (source abstract, 2023)"
---

# Trustworthy Hits

**Parent project:** CBIO056 HeLU-DTI (protein/drug language-model embeddings + disease knowledge graph in a heterogeneous GNN; beat baselines on BindingDB and BioSNAP).

## Premise
The parent highlights that HeLU-DTI finds "reasonable targets that were not previously known." But a list of novel predictions is only useful if we know which ones to trust. Conformal prediction gives each prediction a guaranteed error rate under exchangeability, and tells us when the model is outside its domain. This project turns raw DTI scores into ranked, error-controlled hit lists.

## Hypothesis
Conformal DTI prediction keeps the target error rate (e.g., 10%) within +/- 2 points on random splits, and flags >= 70% of the wrong predictions on cold splits as low-confidence.

## Data sources (free/public)
- BindingDB, BioSNAP, DAVIS (public).
- ChEMBL post-cutoff records (release notes give dates) as a prospective test set.
- MAPIE or crepes Python libraries (free) for conformal methods.

## Method outline
1. Train a HeLU-style model on a proper training set; hold out a calibration set drawn to match each split type.
2. Apply split-conformal and Mondrian (per-target-family) conformal classification.
3. Measure empirical coverage and set size on random, cold-drug and cold-target splits.
4. Prospective test: freeze on an older ChEMBL release, score interactions first reported in a later release.

## Success gates (locked before results)
- G1: coverage within +/- 2 points of nominal on random splits.
- G2: on cold splits, coverage loss is reported; >= 70% of errors fall in low-confidence sets.
- G3: prospective top-100 confident novel predictions have >= 2x the hit rate of top-100 by raw score, or the null is reported.

## Expected deliverable
A conformal wrapper for any DTI model, calibration plots, and a prospective hit-rate table.

## Failure/pivot rule
If coverage breaks badly on cold splits (exchangeability fails), pivot to weighted conformal with similarity-based weights and report how much it restores.
