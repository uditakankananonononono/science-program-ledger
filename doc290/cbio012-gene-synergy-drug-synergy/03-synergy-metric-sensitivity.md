---
id: P04-03
title: "Bliss, Loewe, ZIP, HSA: How Much Do Synergy Rankings Depend on the Metric, and Does the Model Care?"
parent: "CBIO012 - The Usage of Gene Synergy to Predict Drug Synergy (source abstract, 2025)"
---

# How Much Do Synergy Rankings Depend on the Metric?

**Parent project:** CBIO012 - predicts synergy without auditing which synergy definition its labels encode.

## Premise
Four standard synergy models (Bliss, Loewe, ZIP, HSA) disagree on a substantial fraction of combinations. A predictor trained on one metric may just learn that metric's quirks.

## Hypothesis
>= 20% of DrugComb combinations flip synergy class across metrics; the parent framework's top predictions are enriched for metric-robust combinations only if it learned biology rather than metric artifacts.

## Data sources (free/public)
- DrugComb raw dose-response matrices (public).
- synergyfinder (open R package) for all four metrics.

## Method outline
1. Recompute all four metrics for every DrugComb combination with bootstrap CIs; quantify cross-metric flip rate and per-metric label noise.
2. Train the parent pipeline separately per metric; evaluate cross-metric transfer (train Bliss, test ZIP, etc.).
3. Define a metric-consensus gold set (all four metrics agree); re-evaluate the framework on consensus labels only.

## Success gates (locked before results)
- G1: cross-metric flip rate and confusion tables published.
- G2: cross-metric transfer AUC drop <= 0.10, else metric-dependence declared a first-order limitation.
- G3: consensus-set performance reported as the headline number, not best-metric performance.

## Expected deliverable
`metriccheck`: a tool computing all four metrics + consensus labels for any dose-response matrix, with the frozen DrugComb recomputation released as a reference dataset.

## Failure/pivot rule
If transfer collapses, publish the finding that synergy prediction is currently metric-definition-bound - with concrete guidance on consensus labeling.
