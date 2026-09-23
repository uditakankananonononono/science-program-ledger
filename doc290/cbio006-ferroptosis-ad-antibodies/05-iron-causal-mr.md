---
id: P02-05
title: "Is Iron Causal in Alzheimer's? Pre-Registered Mendelian Randomization on Public GWAS"
parent: "CBIO006 - Biclonal Antibodies to Prevent Ferroptosis in AD (source abstract, 2025)"
---

# Is Iron Causal in Alzheimer's? Mendelian Randomization

**Parent project:** CBIO006 - iron-dysregulation premise underlying the whole therapeutic program.

## Premise
Correlational iron-AD links may be reverse causation. Genetic instruments for iron status offer a causal test the premise needs - an experiment nature already ran.

## Hypothesis
Lifelong genetically higher iron status (at least one of serum iron, ferritin, transferrin saturation, TIBC) causally raises AD risk with concordant estimates across MR methods.

## Data sources (free/public)
- Iron biomarker GWAS summary stats (IEU OpenGWAS: deCODE/UK Biobank).
- AD GWAS (Kunkle 2019, Bellenguez 2022); FinnGen AD endpoints; 1000 Genomes LD reference.

## Method outline
1. Pre-register the full analysis plan in the repo before computing any result.
2. Two-sample MR per biomarker (IVW primary; MR-Egger, weighted median, MR-PRESSO sensitivity).
3. Reverse MR (AD liability vs iron traits); colocalization at SLC40A1/HAMP loci; APOE-region-exclusion sensitivity.

## Success gates (locked before results)
- G1: causal support requires IVW p < 0.05, concordant direction in >= 2 sensitivity methods, MR-Egger intercept p > 0.05.
- G2: reverse MR reported; bidirectionality declared if significant.
- G3: all deviations from the pre-registered plan logged and reported.

## Expected deliverable
`ironmr`: fully scripted re-runnable MR pipeline (TwoSampleMR + OpenGWAS) with the locked plan, all code, and a living results page.

## Failure/pivot rule
A null or pleiotropy-violated result is the headline: population genetics does not support iron as causal in AD, so the ferroptosis premise must rest on mechanistic evidence only - stated without softening.
