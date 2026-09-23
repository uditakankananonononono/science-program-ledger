---
id: P04-07
title: "Certified or Lucky? Permutation and Negative-Control Certification of Gene-Embedding Synergy Claims"
parent: "CBIO012 - The Usage of Gene Synergy to Predict Drug Synergy (source abstract, 2025)"
---

# Certified or Lucky? Negative-Control Certification

**Parent project:** CBIO012 - reports strong performance without negative controls against annotation-bias and degree shortcuts.

## Premise
Gene-function prediction tracks annotation popularity: well-studied genes get better embeddings, and drug targets are well-studied genes. Permutation designs can certify whether performance is biology or annotation bias.

## Hypothesis
A measurable fraction of the parent's performance survives only because targets of tested drugs are annotation-rich; after degree/annotation-matched permutation, the certified effect size is smaller but real - or is not.

## Data sources (free/public)
- Same as parent pipeline (GoBERT, DrugComb).
- GO annotation counts per gene (GOA) for matching.

## Method outline
1. Build annotation-matched random embedding sets: for each drug target, sample genes with matched GO-annotation count and network degree.
2. Re-run the full pipeline on >= 100 matched permutation sets; distribution of permuted performance vs real.
3. Report certified effect size (real minus 95th percentile of null) per split regime.

## Success gates (locked before results)
- G1: certified effect size > 0 on cold splits, else the framework's edge is declared annotation-bias, published as such.
- G2: null distributions published with the matching algorithm - reusable by others.
- G3: certification computed before any further model tuning.

## Expected deliverable
`nullcert`: a negative-control certification package for gene-embedding models - input embeddings + task, output a permutation certificate.

## Failure/pivot rule
If the certified effect is null, the deliverable is the certified-negative report, following the pivot rule: locked gates, honest negative, no fishing.
