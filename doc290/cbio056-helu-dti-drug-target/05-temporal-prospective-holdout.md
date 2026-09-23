---
id: P19-05
title: "Time Machine Test: Prospective Validation on Interactions Discovered After Training"
parent: "CBIO056 - HeLU-DTI: Drug Target Prediction via Deep Learning (source abstract, 2023)"
---

# Time Machine Test

**Parent project:** CBIO056 HeLU-DTI (protein/drug language-model embeddings + disease knowledge graph in a heterogeneous GNN; beat baselines on BindingDB and BioSNAP).

## Premise
The strongest test of "finds targets not previously known" is time: train on what was known up to a date, then check predictions against interactions published later. ChEMBL records the document year for each measurement, so this can be done with public data. Random splits cannot show this; time splits can.

## Hypothesis
A HeLU-style model trained on ChEMBL data up to 2019 ranks interactions first reported in 2020-2024 in its top 1% at >= 5x the rate expected by chance, and beats a similarity baseline.

## Data sources (free/public)
- ChEMBL (open), using document year per activity record.
- PrimeKG, restricted to edges whose sources predate the cutoff where possible (to avoid future-knowledge leakage).
- ESM-2 / ChemBERTa embeddings.

## Method outline
1. Build a ChEMBL-derived interaction set (active if pChEMBL >= 6); split by first-report year: train <= 2019, test 2020-2024.
2. Keep only test pairs where both drug and target existed before the cutoff, so the task is "new link," not "new entity."
3. Train HeLU-style, DrugBAN-style and nearest-neighbor baselines; score all candidate pairs for test drugs.
4. Measure enrichment of true future links at top 1% and top 100 per drug.

## Success gates (locked before results)
- G1: top-1% enrichment >= 5x chance.
- G2: beats the similarity baseline by >= 20% relative enrichment, or that is reported as the finding.
- G3: results broken down by target family (kinase, GPCR, other) with 95% CIs.

## Expected deliverable
A time-split DTI benchmark others can reuse and a list of current model predictions for 2025+ follow-up.

## Failure/pivot rule
If enrichment is near chance (G1 fails), pivot to characterizing what future discoveries look like (novel scaffolds, understudied targets) to explain why models miss them.
