---
id: P03-10
title: "CADD on Zero Budget: A Benchmarked, Fully Free-Compute Drug Discovery Pipeline"
parent: "CBIO008T - Deep Learning Pipeline for EZH2 Drug Discovery (source abstract, 2023)"
---

# CADD on Zero Budget: Benchmarked Free-Compute Pipeline

**Parent project:** CBIO008T - claims a production-ready pipeline; production-readiness includes cost and reproducibility on free compute.

## Premise
Student and low-resource labs need to know exactly what a full CADD pipeline (docking, generative model, MD triage) costs in time and accuracy on free tiers - nobody publishes those numbers.

## Hypothesis
A complete EZH2 case pipeline runs end to end on free compute (Colab/free-tier CPU) within a locked wall-clock budget while losing < 10% of the accuracy of a paid-GPU run.

## Data sources (free/public)
- All data from P03-01..P03-06 (PDB, ChEMBL, BindingDB, MOSES).
- Free tooling: AutoDock Vina, RDKit, GROMACS, Colab.

## Method outline
1. Implement the full pipeline (screen -> generate -> filter -> MD triage) as containerized steps.
2. Run identical workloads on free CPU, free-tier GPU, and a reference paid GPU; record wall-clock, queue limits, memory failures, and per-stage accuracy deltas (EF1%, MOSES metrics, MD stability agreement).
3. Publish the cost-accuracy frontier and a decision table: which stages are free-compute-safe and which are not.

## Success gates (locked before results)
- G1: end-to-end free-tier completion within 72 wall-clock hours, else the specific blocking stage is named with measured requirements.
- G2: per-stage accuracy delta < 10% vs reference run, else the stage is labeled paid-compute-required with evidence.
- G3: the pipeline reproduces from a fresh account using only the published repo (one-command run).

## Expected deliverable
`freecadd`: the containerized pipeline + published cost/accuracy ledger + decision table - itself the reusable tool for any target.

## Failure/pivot rule
If free compute cannot complete key stages, publish exactly which and what they truly require - a resource map that is itself the useful result.
