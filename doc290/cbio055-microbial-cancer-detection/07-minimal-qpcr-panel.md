---
id: P18-07
title: "Minimal Panel: A Low-Cost Targeted Microbial Assay for CRC Screening"
parent: "CBIO055 - Early Cancer Detection Using Microbial Information (source abstract, 2023)"
---

# Minimal Panel

**Parent project:** CBIO055 Microbial Cancer Detection (taxonomy + microbial function features from >2000 tumor and blood samples; 18% synergy gain in tissue, weaker in cfDNA).

## Premise
Shotgun sequencing is too costly for population screening. The parent found 190 taxonomic and 118 functional biomarkers; a screening test needs fewer than 10 targets that a qPCR machine can read. This project asks how small a panel can be before accuracy falls apart.

## Hypothesis
A panel of <= 8 taxa and genes (for example F. nucleatum, pks, P. micra, bft) reaches >= 90% of full-metagenome AUROC for CRC vs control across cohorts.

## Data sources (free/public)
- curatedMetagenomicData CRC stool cohorts (taxonomy + HUMAnN gene families).
- Published FIT (fecal immunochemical test) performance numbers and any cohorts reporting FIT alongside metagenomes (e.g., Zeller 2014) as the clinical comparator.
- Published qPCR marker studies (e.g., Wong et al. 2017 Gut; Liang et al. 2017) for candidate targets.

## Method outline
1. Rank features by stability selection across cohorts (LASSO with bootstrap).
2. Greedy forward selection to build panels of size 1-15; LOCO AUROC at each size.
3. Simulate qPCR detection limits by thresholding relative abundance.
4. Compare best panel to FIT alone and FIT + panel where FIT data exist.

## Success gates (locked before results)
- G1: panel of <= 8 targets reaches >= 90% of full-model LOCO AUROC.
- G2: holds after simulated detection-limit thresholding (drop <= 0.03 AUROC).
- G3: FIT + panel beats FIT alone by >= 0.05 AUROC where FIT data exist, or the null is reported.
- G4: per-cohort 95% CIs.

## Expected deliverable
A panel-size vs accuracy curve, the chosen target list with primer-design notes from public sequences, and an open scoring script.

## Failure/pivot rule
If no small panel reaches 90% (G1 fails), report the minimum panel size that does and the cost crossover point where targeted sequencing beats qPCR.
