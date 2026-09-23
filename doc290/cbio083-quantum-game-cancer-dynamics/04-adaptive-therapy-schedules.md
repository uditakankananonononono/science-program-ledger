---
id: P23-04
title: "Schedule Designer: Using Game Models to Design Alectinib On/Off Schedules"
parent: "CBIO083 - Quantum Game Theory to Simulate Cancer Dynamics (source abstract, 2026)"
---

# Schedule Designer

**Parent project:** CBIO083 Quantum Game Theory Cancer Dynamics (Lindblad master-equation QGT model with leaky integrator fit to the Kaznatcheev alectinib/fibroblast NSCLC game assay; beat classical replicator models by 10-20%).

## Premise
The practical payoff of predicting sensitive-resistant dynamics is choosing when to give and pause the drug (adaptive therapy), keeping sensitive cells around to suppress resistant ones. The parent's four environments include drug on/off and fibroblasts present/absent, so a fitted model can simulate switching. The key question: do classical and quantum models recommend different schedules? If not, the choice of model does not matter clinically.

## Hypothesis
Classical, memory-classical and QGT models agree on the optimal on/off threshold within 10% of resistant-fraction, so schedule recommendations are robust to model choice.

## Data sources (free/public)
- Kaznatcheev 2019 GameAssay data (fitted models from P23-01).
- Farrokhian 2022 gefitinib data for a second-drug check.

## Method outline
1. Use fitted models to simulate switching between drug and no-drug environments (with/without fibroblasts).
2. Optimize threshold-based and fixed-interval schedules for time until resistant fraction exceeds a cutoff.
3. Compare optimal schedules and predicted benefit across model families and parameter uncertainty.
4. Identify conditions (e.g., fibroblast presence) where models disagree most - these are the experiments worth running.

## Success gates (locked before results)
- G1: optimal threshold agreement within 10% across models, or disagreement quantified.
- G2: predicted adaptive-vs-continuous benefit reported with uncertainty bands for each model.
- G3: top-3 discriminating experiments listed with predicted outcomes per model.

## Expected deliverable
A schedule-design tool for game models and a list of experiments that would tell the models apart.

## Failure/pivot rule
If no schedule beats continuous dosing in any model, report that the fitted games do not support adaptive therapy for this system and explain which parameter would need to change.
