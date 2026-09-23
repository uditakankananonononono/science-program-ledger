---
id: P03-01
title: "An Honest EZH2 Virtual-Screening Benchmark: Open Docking on Public Structures with Real Enrichment Numbers"
parent: "CBIO008T - Deep Learning Pipeline for EZH2 Drug Discovery (source abstract, 2023)"
---

# An Honest EZH2 Virtual-Screening Benchmark

**Parent project:** CBIO008T - deep learning CADD pipeline (GNN cofactor ID, VAE generation, simulation validation) targeting EZH2 in neuroblastoma.

## Premise
The parent asserts a production-ready pipeline but never measures prospective-style enrichment on public ground truth. A locked benchmark on known EZH2 actives vs property-matched decoys establishes what open docking + learned rescoring can actually do.

## Hypothesis
An open docking stack (AutoDock Vina/smina + a GNN rescoring model) achieves EF1% >= 10 on EZH2 actives, and the learned rescorer adds >= 30% enrichment over docking score alone.

## Data sources (free/public)
- PDB EZH2/PRC2 structures (SET domain and EED complexes).
- ChEMBL EZH2 actives (IC50 labels); DUD-E-style property-matched decoys generated with the open DUD-E server/DeepCoy.

## Method outline
1. Curate actives/decoys with locked potency cutoffs; standardize structures.
2. Dock against >= 3 EZH2 crystal conformations; train a GNN rescorer on BindingDB general set, freeze, then rescore the EZH2 screen.
3. Report ROC AUC, EF1%, BEDROC with bootstrap CIs; per-conformation sensitivity.

## Success gates (locked before results)
- G1: EF1% >= 10 for docking alone on at least one conformation, else the structure set is flagged unsuitable for screening.
- G2: rescorer improves EF1% by >= 30% over docking score alone (paired bootstrap p < 0.05), else rescoring declared non-additive for this target.
- G3: all decoy generation and splits frozen before the first enrichment number is computed.

## Expected deliverable
`ezh2bench`: frozen benchmark dataset + leaderboard tooling that scores any submitted screening function on the hidden decoy labels.

## Failure/pivot rule
If enrichment is poor across conformations, publish the benchmark with the failure analysis (which chemotypes dock false-positive) - the benchmark is the product either way.
