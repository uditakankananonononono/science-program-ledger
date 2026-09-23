---
id: P16-08
title: "TernaryBench: How Well Do Structure Predictors Really Do on Glue Ternary Complexes?"
parent: "CBIO046T - Expanding the Druggable Human Proteome Five-Fold (ISEF 2026 Grand Award)"
---

# TernaryBench

**Parent project:** CBIO046T (glue candidates rest on predicted recruitment - predicted structures are the load-bearing claim).

## Premise
Every computational glue pipeline - including the parent's - ultimately trusts that structure predictors can model the glue-induced ternary complex. AlphaFold-Multimer and successors were trained and benchmarked mostly on natural complexes; induced complexes with a small molecule at the interface are a different distribution. This project builds the definitive public benchmark: all published glue/degrader ternary structures, strict deduplication against training cutoffs, multiple predictors, and honest metrics. The output decides what the whole field can claim: where structure-based glue design is reliable, where it is decoration, and a confidence calibration every pipeline should adopt.

## Data sources
- PDB (public): all glue/PROTAC ternary-complex structures (CRBN, VHL, others).
- AlphaFold DB + open predictor weights (AlphaFold-Multimer/Boltz-class) with documented training cutoffs.
- Published benchmark efforts (open) for methodology alignment.
- Binding-affinity datasets for the structure-to-activity correlation arm.

## Method outline
1. Curate the ternary-complex set with ligand identity and publication-date metadata.
2. Strict train/test hygiene: exclude anything inside predictor training windows.
3. Run predictor panel; score interface accuracy (DockQ-class metrics) with/without the ligand provided.
4. Calibrate: does predicted confidence track actual accuracy for induced complexes?
5. Structure-to-activity arm: do better-predicted complexes show better activity correlation?

## Success gates (locked before results)
- G1: benchmark covers >= 80% of published ternary complexes meeting quality thresholds.
- G2: predictor accuracy on induced complexes reported with CIs and compared to natural-complex baselines - the headline number, whatever direction it lands.
- G3: confidence-calibration curve published; a recalibration table shipped if confidence is miscalibrated (likely).
- G4: honest-negative clause: "structure prediction is not yet reliable for induced ternary geometry" is a full primary result if that's what the data says.

## Expected deliverable
TernaryBench (dataset + evaluation harness + leaderboard-ready tool), the reliability study with calibration tables, and pipeline-integration guidance for every glue-discovery team.

## Failure/pivot rule
If the published complex set is too small/redundant for G2 power, pivot to expanding it synthetically: systematic mutation/variant complexes predicted and cross-checked against the measured subset - with clear synthetic/real stratification, gates re-locked.
