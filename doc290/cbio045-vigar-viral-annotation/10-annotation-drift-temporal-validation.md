---
id: P15-10
title: "Annotation Drift: Temporal Validation of Viral Genome Annotators on Post-Training Deposits"
parent: "CBIO045 - Viral Genome Annotation with RNNs (source abstract, 2024)"
---

# Annotation Drift

**Parent project:** CBIO045 ViGAR (trained on a 2024 RefSeq snapshot; evaluated on random splits of the same snapshot).

## Premise
ViGAR's 96% recall was measured on random samples from the same database snapshot it trained on - the standard evaluation that systematically overstates real-world performance. The honest test is temporal: train on everything deposited before a cutoff, test on everything deposited after. New deposits include novel families, divergent sequences from new sampling campaigns, and shifting submission quality. This project runs temporal validation for the parent's architecture and classical baselines across multiple cutoff years, quantifying annotation-model decay as a function of sequence distance from the training set - and derives retraining-trigger rules for keeping annotation models current.

## Data sources
- GenBank/RefSeq viral with deposit-date metadata (public): the temporal axis.
- The parent's architecture (reimplemented) + classical baselines (Prodigal-style, HMM annotators).
- NCBI deposit-date snapshots via accession-version history.

## Method outline
1. Build temporal train/test splits at yearly cutoffs (2019-2024).
2. Train per cutoff; evaluate on subsequent-year deposits; measure decay curves.
3. Decompose decay by sequence novelty (distance-to-training-set bins) and taxonomy novelty.
4. Fit a decay model; derive retraining triggers (performance floor vs. deposit drift).
5. Compare architecture robustness: does the RNN decay differently than HMM/alignment methods?

## Success gates (locked before results)
- G1: decay curves produced for >= 5 cutoffs with CIs; random-split optimism gap quantified (the headline number).
- G2: decay decomposed: >= 60% of performance loss attributable to named novelty axes, or the residual reported as unexplained.
- G3: retraining-trigger rule proposed and back-tested across cutoffs (would have fired correctly >= 80% of the time).
- G4: architecture comparison reported fairly, including if classical methods decay less - the parent's approach must win on evidence, not loyalty.

## Expected deliverable
The temporal-validation study (optimism-gap headline + decay curves), the retraining-trigger rule, and a versioned evaluation harness the field can rerun every year.

## Failure/pivot rule
If deposit-date metadata proves too messy for clean cutoffs (G1 blocked), pivot to accession-space proxies and publish the metadata-quality findings - a data-hygiene report with the corrected methodology, gates re-locked.
