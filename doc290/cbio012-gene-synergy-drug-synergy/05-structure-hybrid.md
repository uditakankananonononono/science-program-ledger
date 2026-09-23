---
id: P04-05
title: "Genes Plus Structures: A Controlled Ablation of What Drug Chemistry Adds to Gene-Embedding Synergy Models"
parent: "CBIO012 - The Usage of Gene Synergy to Predict Drug Synergy (source abstract, 2025)"
---

# Genes Plus Structures: A Controlled Hybrid Ablation

**Parent project:** CBIO012 - uses only gene-function similarity; ignores drug chemical structure entirely.

## Premise
Chemistry matters: drugs with similar targets or scaffolds interact predictably. A controlled hybrid - gene embeddings + molecular fingerprints/GNN encodings - measures what each view contributes under identical splits.

## Hypothesis
Adding structure features improves cold-drug AUC by >= 0.08 (where gene embeddings are blind for novel targets), while adding nothing on warm splits - defining exactly when each view earns its place.

## Data sources (free/public)
- DrugComb with drug SMILES; RDKit Morgan fingerprints; pretrained open molecular GNN (e.g., Chemprop public weights).
- GoBERT embeddings (parent pipeline).

## Method outline
1. Build three models on identical data: gene-only (parent), structure-only, hybrid; identical CV design across all four split regimes from P04-01.
2. Per-regime ablation deltas with CIs; interaction analysis (does structure help more when targets are unannotated?).
3. Error analysis: characterize combinations where the views disagree.

## Success gates (locked before results)
- G1: per-regime ablation table with CIs - published regardless of direction.
- G2: hybrid beats gene-only by >= 0.08 AUC on cold-drug splits, else structure declared non-additive for this framework.
- G3: no split-regime result hidden because it disfavors the hybrid.

## Expected deliverable
`hybridsynergy`: the three-model benchmark + a recommendation tool that picks the right feature view given a user's split scenario.

## Failure/pivot rule
If structure adds nothing anywhere, publish the null - gene-function embeddings already capture the chemistry-relevant signal - simplifying future models.
