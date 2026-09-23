---
id: P19-09
title: "Cross-Kingdom DTI: Transferring Human-Trained DTI Models to Bacterial Drug Targets"
parent: "CBIO056 - HeLU-DTI: Drug Target Prediction via Deep Learning (source abstract, 2023)"
---

# Cross-Kingdom DTI

**Parent project:** CBIO056 HeLU-DTI (protein/drug language-model embeddings + disease knowledge graph in a heterogeneous GNN; beat baselines on BindingDB and BioSNAP).

## Premise
DTI models are trained almost entirely on human proteins. Antibiotic discovery needs predictions on bacterial proteins, where data is thin and resistance makes new targets urgent. Protein language models are trained across all life, so the sequence branch might transfer. This project tests whether HeLU-style models generalize across kingdoms.

## Hypothesis
A model trained on human DTI data reaches AUROC >= 0.65 on bacterial targets zero-shot, and fine-tuning on <= 20% of bacterial data brings it to >= 0.80.

## Data sources (free/public)
- ChEMBL bacterial single-protein targets (e.g., E. coli, M. tuberculosis, S. aureus enzymes).
- CO-ADD (Community for Open Antimicrobial Drug Discovery) public screening data.
- UniProt reference proteomes; ESM-2 embeddings.

## Method outline
1. Build a bacterial DTI set from ChEMBL (pChEMBL >= 6 actives, matched inactives).
2. Zero-shot: apply the human-trained model directly; drop the human-disease KG branch or replace it with a pathogen KG stub.
3. Few-shot: fine-tune with 5%, 10%, 20% of bacterial pairs; learning curve.
4. Separate targets with close human homologs from bacteria-specific ones (the ones that matter for selectivity).

## Success gates (locked before results)
- G1: zero-shot AUROC >= 0.65 on bacteria-specific targets.
- G2: 20% fine-tune reaches >= 0.80 AUROC.
- G3: homolog vs bacteria-specific split reported with 95% CIs.

## Expected deliverable
A cross-kingdom DTI benchmark, fine-tuning curves, and scored candidates for bacteria-specific targets.

## Failure/pivot rule
If zero-shot is near chance (G1 fails), report the minimum bacterial data needed for useful performance, as guidance for open antimicrobial screening efforts.
