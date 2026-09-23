---
id: P06-07
title: "Protein Language Models vs Atomic Graphs: A Fair Encoding Bake-Off for DTA"
parent: "CBIO013 - Fighting Future Pandemics with Novel DeepGraphDTI (source abstract, 2024)"
---

# Protein Language Models vs Atomic Graphs

**Parent project:** CBIO013(2024) - converts sequences to SMILES-like strings then atomic graphs to gain "high-resolution structural attributes"; protein language models (ESM-2) now offer a competing encoding trained on far more data.

## Premise
The encoding choice should be decided by controlled comparison on identical splits, not architecture preference.

## Hypothesis
ESM-2 embeddings match or beat atomic-graph encodings on cold-target splits (where structure prediction uncertainty hurts graphs), while graphs win on warm splits - defining where each encoding earns its cost.

## Data sources (free/public)
- DAVIS/KIBA/BindingDB; ESM-2 public weights; the reproduced graph encoder.
- AlphaFold structures where graphs need geometry.

## Method outline
1. Hold the downstream model fixed; swap only the protein encoding (graph vs ESM-2 vs both).
2. Evaluate across the P06-01 split regimes; compute cost (training/inference time on free-tier GPU) per encoding.
3. Performance-cost frontier per regime; publication of all numbers.

## Success gates (locked before results)
- G1: per-regime, per-encoding table with CIs - all cells published.
- G2: an encoding "wins" a regime only at >= 0.03 AUC with non-overlapping CIs; otherwise regime declared a tie (ties are publishable).
- G3: free-compute cost per encoding measured and published.

## Expected deliverable
`encodeoff`: the controlled bake-off harness + recommendation table (given your split regime and compute, use encoding X).

## Failure/pivot rule
If everything ties, publish the equivalence result - encoding choice matters less than split design, refocusing the field's effort.
