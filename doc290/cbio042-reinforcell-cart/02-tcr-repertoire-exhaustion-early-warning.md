---
id: P13-02
title: "TCR-Repertoire Early Warning: Predicting T-Cell Exhaustion From Repertoire Dynamics"
parent: "CBIO042 - ReinforCell: CAR-T Cell Optimization Solution (ISEF 2026 Grand Award)"
---

# TCR-Repertoire Early Warning

**Parent project:** CBIO042 ReinforCell (predicting CAR-T exhaustion trajectories from longitudinal single-cell data).

## Premise
ReinforCell predicts exhaustion from single-cell transcriptomics, which is expensive and slow to run clinically. T-cell exhaustion has a repertoire-level fingerprint: clonal collapse, loss of TCR diversity, and expansion of terminally differentiated clones precede functional failure by weeks. This project tests whether exhaustion and therapy failure can be predicted earlier and cheaper from longitudinal bulk TCR-beta repertoire sequencing alone, using diversity dynamics (clonality, turnover, motif-level convergence) rather than per-cell transcriptomes. If it works, monitoring costs drop by two orders of magnitude; if it fails, the boundary (what repertoire data structurally cannot see) is the publishable result.

## Data sources
- Adaptive Biotechnologies immunoSEQ public datasets (open access sample sets).
- VDJdb and McPAS-TCR: curated antigen-specific TCR databases for motif labeling.
- iReceptor public repositories: longitudinal repertoire time series from checkpoint-blockade and infection cohorts.
- Emerson et al. 2017 immunoSEQ cohort (public) for baseline healthy repertoire statistics.

## Method outline
1. Assemble longitudinal TCR-beta repertoires from cohorts with known clinical outcomes (response vs. relapse/progression).
2. Compute repertoire dynamics features: Shannon/Gini diversity trajectories, clone turnover rates, top-clone dominance curves, public-motif enrichment against VDJdb.
3. Train a sequence-of-repertoires model (temporal convolution or transformer over per-timepoint repertoire embeddings) to predict outcome and time-to-failure.
4. Benchmark against transcriptome-derived exhaustion scores from the parent's Ledergor-style cohorts where paired data exists.
5. Quantify lead time: how many days before clinical failure does the repertoire signal cross threshold?

## Success gates (locked before results)
- G1: held-out cohort AUC >= 0.75 for outcome prediction from repertoire features alone.
- G2: prediction lead time >= 14 days before clinical assessment detects failure.
- G3: diversity features beat a clone-count-only baseline by >= 0.05 AUC (dynamic features carry the signal).
- G4: model transports to >= 1 cohort from a different disease context with AUC degradation <= 0.10; if transport fails, document the non-transport boundary as the primary result.

## Expected deliverable
An open "RepertoireWatch" early-warning tool (input: two or more longitudinal immunoSEQ exports; output: exhaustion risk score with lead-time estimate), benchmark report vs. transcriptomic scoring, and a transport/non-transport analysis across cohorts.

## Failure/pivot rule
If repertoire-only prediction fails G1, pivot to *monitoring triage*: repertoire screening as a cheap gate that selects which patients need expensive single-cell profiling - a two-tier cost model with its own locked gates.
