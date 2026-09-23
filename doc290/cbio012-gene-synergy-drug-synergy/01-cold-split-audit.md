---
id: P04-01
title: "Cold-Split Audit: Does Gene-Embedding Drug-Synergy Prediction Survive Unseen Drugs and Unseen Cell Lines?"
parent: "CBIO012 - The Usage of Gene Synergy to Predict Drug Synergy (source abstract, 2025)"
---

# Cold-Split Audit of Gene-Embedding Drug-Synergy Prediction

**Parent project:** CBIO012 - GoBERT gene-function embeddings + cosine similarity to predict drug-drug synergy.

## Premise
Synergy models are usually evaluated on random splits where both drugs and the cell line appear in training - inflating accuracy. The clinically meaningful tests are cold-drug, cold-combination, and cold-cell-line generalization.

## Hypothesis
The parent's framework loses >= 0.15 AUC moving from random to cold-combination splits, and loses most remaining signal on cold-cell-line splits - quantifying where gene-function embeddings actually help.

## Data sources (free/public)
- DrugComb (public synergy screens); NCI-ALMANAC.
- GoBERT embeddings reproducible from the public model; DepMap expression for cell-line features.

## Method outline
1. Reproduce the parent pipeline end to end with locked hyperparameters.
2. Evaluate under four split regimes: random, cold-combination, cold-drug, cold-cell-line; identical metrics (AUC, AUPRC) with CIs.
3. Ablate: GoBERT embeddings vs GO one-hot vs random embeddings of matched dimension, under each regime.

## Success gates (locked before results)
- G1: full split-regime performance table with 95% CIs published - the audit is the deliverable regardless of direction.
- G2: GoBERT beats degree/dimension-matched random embeddings by >= 0.05 AUC on cold-combination splits, else embedding value is declared uncertified.
- G3: cold-cell-line AUC reported separately; no pooling that hides cross-context failure.

## Expected deliverable
`synergyaudit`: reproducible benchmark harness with frozen splits, so any synergy model gets the same four-regime certificate.

## Failure/pivot rule
If GoBERT fails to beat random embeddings, publish the shortcut finding - model performance is dataset memorization, not function biology - with full evidence.
