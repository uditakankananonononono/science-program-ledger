---
id: P19-10
title: "Graph or Shortcut: What the Disease Knowledge Graph Actually Contributes to DTI Prediction"
parent: "CBIO056 - HeLU-DTI: Drug Target Prediction via Deep Learning (source abstract, 2023)"
---

# Graph or Shortcut

**Parent project:** CBIO056 HeLU-DTI (protein/drug language-model embeddings + disease knowledge graph in a heterogeneous GNN; beat baselines on BindingDB and BioSNAP).

## Premise
HeLU-DTI's distinctive piece is the knowledge graph of diseases, phenotypes and drug effects. Knowledge graphs can help in two ways: real biology (drugs for the same disease hit related targets) or shortcuts (node degree - popular drugs and proteins get predicted as binders). Node-degree bias is a known problem in link prediction. This project separates the two.

## Hypothesis
At least half of the KG branch's gain on random splits is explained by node degree, and a degree-matched negative sampling scheme removes most of it.

## Data sources (free/public)
- PrimeKG and Hetionet (public).
- BioSNAP and BindingDB benchmarks.
- Integrated gradients / GNNExplainer (free) for attribution.

## Method outline
1. Build a degree-only baseline (predict from drug and target degree alone) and report its AUROC.
2. Re-train HeLU-style models with standard vs degree-matched negative sampling.
3. Replace the real KG with a degree-preserving randomized KG; measure what gain remains.
4. Use attribution to list which KG paths drive top predictions; check them against literature.

## Success gates (locked before results)
- G1: degree-only baseline AUROC reported for each benchmark.
- G2: KG gain under degree-matched sampling reported with 95% CI (5 seeds); if it drops by >= 50%, shortcut is declared.
- G3: real KG beats randomized KG by >= 0.02 AUROC for the KG to count as carrying biology.

## Expected deliverable
A shortcut-audit toolkit for KG-based DTI models and a clear verdict on the KG's value.

## Failure/pivot rule
If the KG carries only shortcut signal (G3 fails), pivot to a curated mechanism-only KG (pathways and protein interactions, no drug-disease edges) and test whether that version adds real signal.
