---
id: P23-10
title: "Open Game Benchmark: A Standard Dataset Suite and Leaderboard for Cancer Evolutionary Dynamics Models"
parent: "CBIO083 - Quantum Game Theory to Simulate Cancer Dynamics (source abstract, 2026)"
---

# Open Game Benchmark

**Parent project:** CBIO083 Quantum Game Theory Cancer Dynamics (Lindblad master-equation QGT model with leaky integrator fit to the Kaznatcheev alectinib/fibroblast NSCLC game assay; beat classical replicator models by 10-20%).

## Premise
The parent compared models on one dataset with its own splits. Every new cancer-dynamics model (classical, quantum, spatial, ML) gets tested differently, so claims like "10-20% better" are hard to compare. Other fields moved forward once shared benchmarks existed. Enough public game-assay and clinical time-series data now exists to build one.

## Hypothesis
Across a standardized suite, no single model family wins on all datasets, and the ranking depends mostly on dataset noise and length - a result only a shared benchmark can show.

## Data sources (free/public)
- Kaznatcheev 2019 GameAssay; Farrokhian 2022 gefitinib assay.
- Bruchovsky 2006 PSA trial data (figshare).
- Microbial datasets from P23-09.

## Method outline
1. Convert all datasets into one format (time, condition, strategy frequencies or counts, replicate IDs) with fixed train/test splits.
2. Define metrics: held-out error, log-likelihood, interval coverage, and parameter count.
3. Submit baseline models: mean-field EGT, memory-classical, SDE, spatial ABM, QGT, and a Gaussian-process black box.
4. Publish a leaderboard with a script so others can add models.

## Success gates (locked before results)
- G1: >= 4 datasets harmonized with fixed splits and data licenses checked.
- G2: >= 6 model families scored on every dataset.
- G3: ranking-vs-dataset-feature analysis reported; "one model wins everywhere" or not is stated plainly.

## Expected deliverable
An open benchmark repository (data loaders, splits, metrics, baselines, leaderboard).

## Failure/pivot rule
If licensing blocks redistribution of some data, ship download scripts from the original sources instead of copies and note which datasets require that.
