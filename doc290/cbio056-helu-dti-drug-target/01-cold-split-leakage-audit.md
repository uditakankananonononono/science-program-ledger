---
id: P19-01
title: "Cold-Split Audit: How Much DTI Accuracy Survives Leakage-Free Splits"
parent: "CBIO056 - HeLU-DTI: Drug Target Prediction via Deep Learning (source abstract, 2023)"
---

# Cold-Split Audit

**Parent project:** CBIO056 HeLU-DTI (protein/drug language-model embeddings + disease knowledge graph in a heterogeneous GNN; beat baselines on BindingDB and BioSNAP).

## Premise
DTI benchmarks like BindingDB and BioSNAP are usually split at random, so the same drugs and near-identical proteins appear in training and test. Models then look strong by memorizing. The parent tested one unseen-dataset transfer (BindingDB to NR), which is a good start. This project measures accuracy under fully cold splits: unseen drugs, unseen proteins, and both.

## Hypothesis
Under cold-drug + cold-target splits with <= 30% protein sequence identity and scaffold separation, HeLU-style models lose >= 0.15 AUROC, and the knowledge-graph branch accounts for most of the random-split gain.

## Data sources (free/public)
- BindingDB and BioSNAP benchmark versions used in DTI papers (public, e.g., via the MolTrans/DrugBAN repositories).
- UniProt sequences; MMseqs2 for identity clustering; RDKit Bemis-Murcko scaffolds.
- PrimeKG (Harvard, public) as the knowledge-graph source.
- ESM-2 and ChemBERTa pretrained weights (free).

## Method outline
1. Rebuild a HeLU-style model (LM embeddings + KG embeddings + heterogeneous GNN + MLP) and simpler baselines (DrugBAN, embedding + MLP).
2. Build four splits: random, cold-drug (scaffold), cold-target (<= 30% identity), cold-both.
3. Ablate the KG branch and the GNN message passing separately.
4. Check KG edge leakage: remove KG drug-target edges that overlap test labels.

## Success gates (locked before results)
- G1: random-split reproduction within 0.03 AUROC of the parent's reported numbers, or the gap is documented.
- G2: cold-both AUROC reported for all models with 95% CIs (5 seeds); a collapse to < 0.65 is published as the finding.
- G3: KG-leakage check done; any drop > 0.02 after removing overlapping edges is reported as leakage.
- G4: at least one model beats a nearest-neighbor similarity baseline on cold-both, or that is the headline.

## Expected deliverable
Reusable leakage-free split files, an ablation table, and a clear statement of what DTI models can do on truly novel drugs and targets.

## Failure/pivot rule
If every model collapses on cold-both (G4 fails), pivot to measuring the similarity threshold at which prediction stops working - a "reach" curve for DTI models.
