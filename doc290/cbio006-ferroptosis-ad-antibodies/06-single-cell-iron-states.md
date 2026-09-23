---
id: P02-06
title: "Which Brain Cells Accumulate Iron in AD? Single-Cell Iron States and a Cell-Type Targeting Classifier"
parent: "CBIO006 - Biclonal Antibodies to Prevent Ferroptosis in AD (source abstract, 2025)"
---

# Which Brain Cells Accumulate Iron in AD?

**Parent project:** CBIO006 - cell-agnostic antibody targeting; delivery and safety depend on which cells actually carry the iron pathology.

## Premise
Iron dysregulation in AD is likely cell-type-specific (microglia/astrocyte sub-states). Public snRNA-seq atlases can localize it and train a classifier that identifies iron-high cell states in new data.

## Hypothesis
>= 1 disease-associated cell state with iron-module dysregulation replicates across >= 3 atlases, and a cell-state classifier transfers between datasets.

## Data sources (free/public)
- Public AD snRNA-seq: Mathys 2019/2023, Zhou 2020, Lau 2020, SEA-AD (Allen) via CELLxGENE census and synapse.
- Locked FerrDb-derived iron/ferroptosis module.

## Method outline
1. Score every cell for the locked iron-handling module; pseudobulk + state-level disease association, covariate-adjusted, per atlas.
2. Ligand-receptor analysis (CellChat): which cells send hepcidin-like signals, which express SLC40A1.
3. Train a cell-state classifier (logistic on module scores + marker genes) on one atlas; test transfer AUC on the others.

## Success gates (locked before results)
- G1: >= 1 replicating iron-high disease cell state across >= 3 atlases (FDR < 0.05), else "no replicating cell state" declared.
- G2: cross-atlas cell-state classifier transfer AUC >= 0.75, else state definition declared dataset-specific.
- G3: pseudobulk effect sizes published alongside state-level results to block single-dataset artifacts.

## Expected deliverable
`ironstates`: census-query package + precomputed module scores for 5 atlases + the transferable cell-state classifier and a cell-target ranking report for therapeutic design.

## Failure/pivot rule
If dysregulation does not localize reproducibly, publish the cross-atlas negative with power analysis - cell-agnostic targeting is then as justified as cell-specific.
