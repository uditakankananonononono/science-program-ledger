---
id: P01-07
title: "The Harder, Useful Task: Detecting Pre-Cancerous Adenomas from the Gut Microbiome"
parent: "CBIO003 - Colorectal Cancer Detection From Gut Microbiome (source abstract, 2025)"
---

# The Harder, Useful Task: Detecting Pre-Cancerous Adenomas

**Parent project:** CBIO003 - CRC-vs-healthy classifier; carcinoma is already clinically late.

## Premise
Screening value comes from detecting advanced adenomas before malignancy. The adenoma signal is weaker and may live in different features (inflammatory/genotoxic pathways) than the carcinoma signal.

## Hypothesis
A stage-aware classifier detects advanced adenomas above a locked usefulness bar, and adenomas sit on a continuum between healthy and carcinoma scores.

## Data sources (free/public)
- Adenoma-arm cohorts in curatedMetagenomicData (Zeller 2014, Feng 2015).
- Yachida 2019 multi-stage sampling (MP/0/I-IV) - the key stage-resolved resource.

## Method outline
1. Three-group ordinal classifier (healthy / adenoma / carcinoma); stage-resolved marker trajectories along the Yachida MP-to-IV axis.
2. Continuum test: do carcinoma-trained scores place adenomas strictly between healthy and carcinoma?
3. Pathway-restricted model (genotoxin + inflammation modules) vs full model, LOCO throughout.

## Success gates (locked before results)
- G1: advanced-adenoma-vs-healthy mean LOCO AUC >= 0.65 with CI lower bound > 0.55 ("screening-useful" bar).
- G2: continuum confirmed (paired test p < 0.05) in >= 3 cohorts, else discontinuity declared.
- G3: >= 3 stage-consistent markers replicate in >= 2 cohorts (same direction, FDR < 0.1).

## Expected deliverable
`adenoma-ceiling`: stage-resolved marker atlas plus a decision-support notebook reporting the achievable adenoma detection limit and required sample size for a new cohort.

## Failure/pivot rule
If G1 fails, publish the powered negative: current stool microbiome signal does not support pre-cancer screening, with the exact detection ceiling.
