---
id: P19-02
title: "Affinity, Not Yes/No: From Binary Interaction Labels to Calibrated Binding Affinity"
parent: "CBIO056 - HeLU-DTI: Drug Target Prediction via Deep Learning (source abstract, 2023)"
---

# Affinity, Not Yes/No

**Parent project:** CBIO056 HeLU-DTI (protein/drug language-model embeddings + disease knowledge graph in a heterogeneous GNN; beat baselines on BindingDB and BioSNAP).

## Premise
The parent's title says "affinities" but the benchmarks it used (BioSNAP, binarized BindingDB) are yes/no labels. Drug programs need to know how strongly a compound binds (pKd/pKi), because a 10 uM hit and a 1 nM hit are very different leads. This project turns the HeLU architecture into a regression model and tests whether the knowledge graph helps predict strength, not just presence.

## Hypothesis
A HeLU-style regressor reaches Pearson r >= 0.80 on DAVIS/KIBA random splits and keeps r >= 0.55 on cold-target splits, with the KG branch adding >= 0.03 r only in the cold setting.

## Data sources (free/public)
- DAVIS (kinase Kd) and KIBA benchmark sets (public).
- ChEMBL (open) for pKi/pKd/pIC50 measurements; BindingDB affinity values.
- PrimeKG for graph context; ESM-2 / ChemBERTa embeddings.

## Method outline
1. Replace the classification head with a regression head (plus heteroscedastic variance output).
2. Train on DAVIS, KIBA and a curated ChEMBL kinase/GPCR set with assay-type harmonization (Kd vs Ki vs IC50 kept separate or corrected).
3. Evaluate on random, cold-drug and cold-target splits; ablate the KG branch.
4. Check calibration of predicted variance against actual errors.

## Success gates (locked before results)
- G1: random-split Pearson r >= 0.80 on DAVIS and KIBA.
- G2: cold-target r >= 0.55, or the ceiling is reported.
- G3: KG ablation effect reported per split with 95% CIs over 5 seeds.
- G4: expected calibration error of the variance head <= 0.1.

## Expected deliverable
An open affinity predictor with uncertainty, a harmonized ChEMBL affinity subset, and a split-by-split ablation report.

## Failure/pivot rule
If assay-type noise dominates (large Kd vs IC50 disagreement), pivot to quantifying the noise floor of public affinity data - the best r any model could reach given replicate disagreement.
