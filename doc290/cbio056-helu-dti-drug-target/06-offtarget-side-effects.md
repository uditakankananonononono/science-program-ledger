---
id: P19-06
title: "Off-Target to Side Effect: Predicting Adverse Drug Reactions From Predicted Off-Target Profiles"
parent: "CBIO056 - HeLU-DTI: Drug Target Prediction via Deep Learning (source abstract, 2023)"
---

# Off-Target to Side Effect

**Parent project:** CBIO056 HeLU-DTI (protein/drug language-model embeddings + disease knowledge graph in a heterogeneous GNN; beat baselines on BindingDB and BioSNAP).

## Premise
The parent's model predicts which proteins a drug binds. Every unwanted binding event is a possible side effect. If predicted off-target profiles carry real information, they should predict known adverse reactions of marketed drugs. This turns the DTI model into a safety screen and gives an independent check of whether its off-target predictions mean anything.

## Hypothesis
Predicted proteome-wide binding profiles predict SIDER side effects with mean AUROC >= 0.70 across frequent side effects, beating chemical-fingerprint-only models by >= 0.03.

## Data sources (free/public)
- SIDER 4.1 side effect database (public).
- OFFSIDES (public FAERS-derived) for an independent label set.
- ChEMBL / BindingDB for training the DTI model; human proteome from UniProt.

## Method outline
1. Train a HeLU-style DTI model excluding SIDER drugs' known interactions from a held-out subset (to avoid label echo).
2. Score each SIDER drug against about 2,000 druggable human proteins to form a predicted binding vector.
3. Train side-effect classifiers on predicted profiles, on fingerprints, and on both; drug-level cross-validation.
4. Check known mechanisms (e.g., hERG binding and QT prolongation) as positive controls.

## Success gates (locked before results)
- G1: mean AUROC >= 0.70 over side effects with >= 50 positive drugs.
- G2: profiles + fingerprints beat fingerprints alone by >= 0.03 mean AUROC.
- G3: hERG/QT positive control significant (p < 0.01); results replicated on OFFSIDES labels.

## Expected deliverable
An off-target safety profiler and a list of side effects best explained by specific predicted off-targets.

## Failure/pivot rule
If predicted profiles add nothing over chemistry (G2 fails), pivot to using measured ChEMBL profiles as an upper bound, to separate "off-targets don't explain side effects" from "our predictions are too noisy."
