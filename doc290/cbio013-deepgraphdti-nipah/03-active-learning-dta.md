---
id: P06-03
title: "Learning Faster: Active Learning to Cut DTA Training-Data Needs for the Next Outbreak"
parent: "CBIO013 - Fighting Future Pandemics with Novel DeepGraphDTI (source abstract, 2024)"
---

# Active Learning to Cut DTA Training-Data Needs

**Parent project:** CBIO013(2024) - pandemic response means new targets with zero affinity labels; sample efficiency is the bottleneck.

## Premise
Active learning (uncertainty/disagreement-driven acquisition) can reach a fixed cold-target performance with far fewer labels - quantifying how few is a direct pandemic-readiness experiment.

## Hypothesis
An ensemble-disagreement active learner reaches 90% of full-data cold-target AUC using <= 30% of available affinity labels, beating random acquisition by >= 15% label efficiency.

## Data sources (free/public)
- BindingDB/DAVIS/KIBA (public); simulated "new target" scenario via target holdout.
- DeepGraphDTI-class model + deep ensembles.

## Method outline
1. Simulate outbreak scenario: hold out entire target families as "new pathogen."
2. Run acquisition curves: random vs uncertainty vs disagreement vs diversity strategies, 5 seeds each.
3. Measure labels-to-threshold (90% of full-data performance) per strategy; cost model in assay counts.

## Success gates (locked before results)
- G1: full acquisition curves with seed variance published for all strategies.
- G2: best strategy reaches the 90% threshold at <= 30% of labels AND beats random by >= 15% efficiency, else active learning is declared non-beneficial here.
- G3: threshold and metrics locked before curves are generated.

## Expected deliverable
`al-dta`: an active-learning toolkit for DTA models with the frozen benchmark - outbreak teams get the measured answer to "how many assays do we need?"

## Failure/pivot rule
If no strategy beats random meaningfully, publish the null - label efficiency in DTA comes from data diversity, not acquisition strategy - with evidence.
