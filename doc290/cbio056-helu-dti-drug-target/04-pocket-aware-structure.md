---
id: P19-04
title: "Pocket-Aware DTI: Adding Predicted Binding-Pocket Structure to Sequence Embeddings"
parent: "CBIO056 - HeLU-DTI: Drug Target Prediction via Deep Learning (source abstract, 2023)"
---

# Pocket-Aware DTI

**Parent project:** CBIO056 HeLU-DTI (protein/drug language-model embeddings + disease knowledge graph in a heterogeneous GNN; beat baselines on BindingDB and BioSNAP).

## Premise
HeLU-DTI reads proteins as sequences through a language model. Binding happens in 3D pockets. AlphaFold DB now gives predicted structures for nearly every UniProt protein, and pocket finders like P2Rank run on them for free. This project tests whether pocket-level structure adds signal beyond sequence embeddings, especially for unseen targets.

## Hypothesis
Pocket embeddings from AlphaFold structures improve cold-target AUROC by >= 0.04 over sequence-only HeLU-style models, with little gain on random splits.

## Data sources (free/public)
- AlphaFold Protein Structure Database (public).
- P2Rank and fpocket (free) for pocket detection.
- BindingDB/BioSNAP/DAVIS benchmarks; PDB co-crystal structures for checking pocket calls.

## Method outline
1. Download AlphaFold models for all benchmark targets; run P2Rank; keep top pockets with pLDDT >= 70.
2. Encode pockets with a small geometric GNN (residue graph) or pocket-residue ESM embedding pooling.
3. Add the pocket branch to the HeLU-style model; compare sequence-only, pocket-only, combined.
4. Validate pocket calls against PDB co-crystal ligands for a subset.

## Success gates (locked before results)
- G1: P2Rank top-3 pocket contains the co-crystal ligand for >= 70% of the validation subset.
- G2: combined model beats sequence-only on cold-target by >= 0.04 AUROC (5 seeds, 95% CI excludes 0).
- G3: gain reported separately for low-pLDDT targets; negative results kept.

## Expected deliverable
Pocket embedding files for benchmark targets, an open pocket-aware DTI model, and a split-wise gain table.

## Failure/pivot rule
If pockets add nothing (G2 fails), pivot to testing whether pocket similarity alone (no learning) predicts shared ligands - a structure-based nearest-neighbor baseline.
