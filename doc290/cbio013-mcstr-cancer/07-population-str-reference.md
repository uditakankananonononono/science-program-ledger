---
id: P05-07
title: "The Missing Baseline: An Ancestry-Stratified Population Reference for Cancer STR Loci"
parent: "CBIO013 - Micro-Changing Tandem Repeats in 10 Human Cancers (source abstract, 2023)"
---

# The Missing Baseline: An Ancestry-Stratified STR Reference

**Parent project:** CBIO013 - calls "micro-changing" relative to population norms, but no ancestry-stratified public reference exists for these loci - a fairness and correctness gap.

## Premise
STR length distributions differ by ancestry. Without stratified baselines, deviation calls - and any diagnostic built on them - misfire disproportionately in non-European patients.

## Hypothesis
>= 15% of the 182 mcSTR loci show significant ancestry-stratified length distributions (after multiple-testing control), and ancestry-aware baselines change deviation calls for >= 10% of non-European samples.

## Data sources (free/public)
- 1000 Genomes (2,504 samples, 26 populations) + HGDP WGS (public).
- Simons Genome Diversity Project where accessible.

## Method outline
1. Genotype all 182 loci across 1000G/HGDP with the benchmarked tool from P05-02.
2. Model per-locus length distributions per super-population; test stratification (locked FDR).
3. Re-call deviations in TCGA tumors under continental vs ancestry-matched baselines; quantify changed calls by patient ancestry.

## Success gates (locked before results)
- G1: complete per-locus ancestry-stratified reference published (this ships regardless of direction).
- G2: stratified-loci fraction and changed-call fraction reported with CIs; equity impact section is mandatory.
- G3: genotyping pipeline identical to P05-02's benchmarked settings.

## Expected deliverable
`strref`: open ancestry-stratified reference database + a deviation-calling API that requires ancestry-aware baselines by default.

## Failure/pivot rule
If stratification is negligible, publish the well-powered null - a single global baseline is justified, and that simplification is now evidence-based.
