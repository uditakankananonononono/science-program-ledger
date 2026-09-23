---
id: P14-08
title: "MorphoKinetic Ploidy: Predicting Euploidy From Time-Lapse Parameters and Omic Anchors"
parent: "CBIO043 - Digital Embryo: Multi-Omic Arrest Prediction (ISEF 2026 Grand Award)"
---

# MorphoKinetic Ploidy

**Parent project:** CBIO043 Digital Embryo (arrest prediction; multi-omic state system).

## Premise
Aneuploidy is the largest single cause of embryo arrest, but PGT-A requires biopsy. Time-lapse incubators record every embryo's morphokinetics (cleavage timings, fragmentation, multinucleation), and published datasets link these parameters to ploidy outcomes. This project builds the best possible non-invasive ploidy predictor from morphokinetics alone, anchors it against omic signatures from the parent's framework where paired data exists, and - critically - measures its true clinical ceiling: can morphokinetics triage which embryos need biopsy, or is the signal fundamentally too weak? An honest ceiling number would reshape how labs allocate PGT-A.

## Data sources
- Published time-lapse morphokinetic datasets with PGT-A outcomes (open supplements from multiple IVF centers).
- Public embryo-imaging datasets released with deep-learning embryo papers.
- Embryo scRNA references for the omic-anchor analysis.
- Published commercial morphokinetic score algorithms (public parameter lists) as baselines.

## Method outline
1. Harmonize morphokinetic parameter tables and ploidy labels across centers.
2. Train gradient-boosted and sequence models on parameter trajectories; leave-one-center-out validation.
3. Benchmark against published commercial scores reimplemented exactly.
4. Compute the triage operating point: sensitivity/specificity tradeoffs for "biopsy vs. transfer without biopsy."
5. Where paired omic data exists, measure how much the molecular layer adds over morphology.

## Success gates (locked before results)
- G1: cross-center AUC >= 0.68 for euploidy, or certified ceiling below that with the number defended.
- G2: learned model matches or beats commercial-score reimplementations, or commercial scores win and are recommended (honest outcome).
- G3: triage analysis shows a net-benefit-positive operating point on >= 1 held-out center, or certifies that morphokinetic triage is not net-positive.
- G4: per-center CIs mandatory; no pooled-only claims.

## Expected deliverable
A "MorphoPloidy" open predictor with triage operating points, the cross-center benchmark vs. commercial scores, and the clinical-ceiling analysis.

## Failure/pivot rule
If cross-center transport fails (annotation drift), pivot to an annotation-standard study: inter-grader and inter-center variability quantified, plus a minimal annotation protocol shown to restore transport - gates re-locked.
