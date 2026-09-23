---
id: P06-01
title: "Cold-Split Honesty Audit of DeepGraphDTI: Unseen Drugs, Unseen Targets, Both"
parent: "CBIO013 - Fighting Future Pandemics with Novel DeepGraphDTI (source abstract, 2024)"
---

# Cold-Split Honesty Audit of DeepGraphDTI

**Parent project:** CBIO013(2024) - DeepGraphDTI, a GNN drug-target-affinity model used to screen 1,040 drugs against Nipah glycoproteins.

## Premise
DTA models are typically benchmarked on random splits where drugs and targets appear in training. Pandemic repurposing is the exact opposite: novel target, mostly unseen pairs. The model's real operating regime must be measured.

## Hypothesis
DeepGraphDTI-class models drop >= 0.2 AUC (or equivalent regression degradation) from random to cold-both splits; sequence-similarity-clustered splits reveal further inflation.

## Data sources (free/public)
- DAVIS, KIBA, BindingDB benchmarks (public); DeepGraphDTI architecture reproducible from the paper/repo if public.
- PDB/AlphaFold for target structures in graph construction.

## Method outline
1. Reproduce the model with locked hyperparameters on the standard benchmarks.
2. Four split regimes: random, cold-drug, cold-target, cold-both; plus target-sequence-cluster splits (30% identity threshold).
3. Report per-regime metrics with CIs; compare against simple baselines (similarity-weighted nearest neighbor).

## Success gates (locked before results)
- G1: full regime table published - the audit is the deliverable regardless of direction.
- G2: cold-both performance must beat the nearest-neighbor baseline by >= 10%, else the deep model's value in the pandemic regime is declared unproven.
- G3: sequence-cluster split results reported separately from identity-random splits.

## Expected deliverable
`dtacert`: a benchmark harness issuing four-regime generalization certificates for any DTA model, pre-run for DeepGraphDTI-class architectures.

## Failure/pivot rule
If the model fails cold regimes, publish the operating-envelope map - exactly when DTA screening is trustworthy and when docking must lead instead.
