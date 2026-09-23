---
id: P03-06
title: "The EZH1 Problem: Structure-Based Selectivity Screening to Avoid Paralog Toxicity"
parent: "CBIO008T - Deep Learning Pipeline for EZH2 Drug Discovery (source abstract, 2023)"
---

# The EZH1 Problem: Structure-Based Selectivity Screening

**Parent project:** CBIO008T - designs against EZH2; its paralog EZH1 is near-identical at the catalytic site and off-target inhibition drives toxicity.

## Premise
Selectivity is where EZH2 inhibitors fail clinically. Public EZH1/EZH2 structures and inhibitor data allow a computational selectivity screen before any compound is advanced.

## Hypothesis
Structure-based docking against both paralogs predicts measured selectivity ratios with rank correlation >= 0.6, and identifies sequence-divergent residues exploitable for selective design.

## Data sources (free/public)
- PDB/AlphaFold EZH1 and EZH2 SET domains; ChEMBL inhibitors with dual EZH1/EZH2 potency measurements (selectivity ratios).
- Tazemetostat and analog SAR series (published).

## Method outline
1. Curate all compounds with measured dual potency; lock the selectivity-ratio labels.
2. Dock every compound into both paralog structures (multiple conformations each); compute score deltas as selectivity predictors.
3. Map paralog-divergent residues within 6 A of the site; test whether delta-score correlates with measured selectivity; propose selective substitutions in silico.

## Success gates (locked before results)
- G1: docking-delta vs measured selectivity Spearman rho >= 0.6 (p < 0.01), else docking declared unable to rank selectivity at this paralog pair.
- G2: >= 3 divergent pocket residues identified with in silico substitution proposals predicted to shift selectivity >= 10x.
- G3: conformations and labels frozen before scoring.

## Expected deliverable
`paralogpick`: a dual-target docking tool that takes a compound library and returns predicted selectivity with calibrated confidence for any paralog pair.

## Failure/pivot rule
If docking cannot rank selectivity (G1 fails), publish the negative and pivot to free-energy methods on the top-10 compounds only - with the cost caveat stated.
