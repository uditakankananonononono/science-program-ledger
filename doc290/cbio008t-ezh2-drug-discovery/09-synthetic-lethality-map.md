---
id: P03-09
title: "Mapping MYCN-EZH2 Synthetic Lethality from Public Screens, with a Trainable Context Classifier"
parent: "CBIO008T - Deep Learning Pipeline for EZH2 Drug Discovery (source abstract, 2023)"
---

# Mapping MYCN-EZH2 Synthetic Lethality

**Parent project:** CBIO008T - high-risk NB is MYCN-driven and MYC factors are "undruggable"; the synthetic-lethal context around EZH2 is the actionable alternative.

## Premise
DepMap co-dependency analysis can map the full synthetic-lethal neighborhood of MYCN amplification and quantify where EZH2 sits in it - then a classifier can predict which tumors share that context.

## Hypothesis
MYCN-amplified lines show a replicating dependency signature (EZH2 among top partners), and a baseline-omics classifier predicts EZH2 sensitivity across held-out pediatric lines.

## Data sources (free/public)
- DepMap CRISPR co-dependency matrices (public); Pediatric DepMap.
- CCLE omics; published NB CRISPR screens (GEO/SRA supplements).

## Method outline
1. Compute MYCN-amplified vs non-amplified differential dependencies across all lineages; rank EZH2 and PRC2 partners with effect sizes.
2. Network analysis of the top dependency set (co-dependency clustering) - is EZH2 in the core MYCN module?
3. Train a classifier (expression + CNV) predicting EZH2 sensitivity; validate leave-one-lineage-out and on any public NB-specific screen.

## Success gates (locked before results)
- G1: EZH2 differential dependency in MYCN-amplified lines with FDR < 0.05 and effect size >= 0.3 Chronos units, else the synthetic-lethal claim is weakened and reported.
- G2: sensitivity classifier AUC >= 0.75 on held-out lines.
- G3: co-dependency module assignments computed with fixed seeds and published parameters.

## Expected deliverable
`synlethmap`: an interactive MYCN dependency-neighborhood map + the trained context classifier usable for patient stratification hypotheses.

## Failure/pivot rule
If EZH2 is not significantly differential in MYCN-amplified lines, publish the corrected target ranking - whichever dependencies actually lead the module.
