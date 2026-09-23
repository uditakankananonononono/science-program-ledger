---
id: P04-08
title: "Prospective Validation by Time Machine: Predict Synergy, Then Check Against Later-Published Screens"
parent: "CBIO012 - The Usage of Gene Synergy to Predict Drug Synergy (source abstract, 2025)"
---

# Prospective Validation by Time Machine

**Parent project:** CBIO012 - retrospective evaluation only; true prospective validation is the field's missing proof.

## Premise
DrugComb's version history enables a real time-split: train on everything published before a cutoff, freeze predictions, then score against combinations published after - the closest free approximation of prospective validation.

## Hypothesis
The parent framework's post-cutoff AUC stays within 0.07 of its pre-cutoff cross-validated estimate; its top-50 novel predictions are enriched >= 3x for later-confirmed synergies vs base rate.

## Data sources (free/public)
- DrugComb versioned releases / submission dates.
- NCI-ALMANAC as an independent later screen for overlapping combinations.

## Method outline
1. Reconstruct pre/post-cutoff datasets from release metadata; locked cutoff.
2. Train and tune ONLY on pre-cutoff data; freeze model and prediction list; publish the top-50 novel predicted synergies (hashed) before evaluation.
3. Evaluate on post-cutoff results; enrichment + calibration analysis.

## Success gates (locked before results)
- G1: post-cutoff AUC within 0.07 of pre-cutoff CV estimate, else generalization decay is the reported finding.
- G2: top-50 enrichment >= 3x base rate (binomial p < 0.05).
- G3: prediction list committed (hash + repo tag) before post-cutoff labels are touched.

## Expected deliverable
`timesplit`: a time-machine validation harness for any predictive biology model, plus the frozen prediction list and its scorecard as a worked example.

## Failure/pivot rule
If prospective performance decays, publish the decay curve - the honest measure of how much retrospective synergy benchmarks overstate readiness.
