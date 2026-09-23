---
id: P19-07
title: "Selectivity Map: Predicting Kinome-Wide Selectivity, Not Single Interactions"
parent: "CBIO056 - HeLU-DTI: Drug Target Prediction via Deep Learning (source abstract, 2023)"
---

# Selectivity Map

**Parent project:** CBIO056 HeLU-DTI (protein/drug language-model embeddings + disease knowledge graph in a heterogeneous GNN; beat baselines on BindingDB and BioSNAP).

## Premise
For kinase drugs, the question is rarely "does it bind its target" but "what else does it hit." Davis et al. 2011 profiled 72 inhibitors against 442 kinases, and later large kinome scans (e.g., Klaeger et al. 2017 Science, 243 drugs by chemoproteomics) are public. This project asks whether a HeLU-style model can predict a whole selectivity profile for a new compound.

## Hypothesis
For held-out inhibitors, predicted kinome profiles reach Spearman rho >= 0.5 with measured profiles and rank the true primary target in the top 5 for >= 50% of compounds.

## Data sources (free/public)
- Davis 2011 kinome Kd matrix (public; the DAVIS benchmark).
- Klaeger 2017 chemoproteomic kinase inhibitor profiles (public supplement / ProteomicsDB).
- ChEMBL kinase data; KinMap/KinHub kinase family annotations.

## Method outline
1. Hold out whole compounds (leave-compound-out) from Davis and Klaeger sets.
2. Predict each held-out compound against all profiled kinases; compare to measured profiles.
3. Compute selectivity scores (Gini, S(10)) from predicted vs measured profiles.
4. Test cross-dataset transfer: train on Davis, predict Klaeger compounds.

## Success gates (locked before results)
- G1: median per-compound Spearman rho >= 0.5 on leave-compound-out.
- G2: primary target in top 5 for >= 50% of held-out compounds.
- G3: predicted vs measured Gini selectivity correlation >= 0.4; cross-dataset numbers reported regardless.

## Expected deliverable
A kinome selectivity predictor, a leave-compound-out benchmark, and predicted profiles for unprofiled ChEMBL kinase inhibitors.

## Failure/pivot rule
If whole-profile prediction fails (G1 fails), pivot to predicting only selectivity class (selective vs promiscuous), which may be learnable when exact profiles are not.
