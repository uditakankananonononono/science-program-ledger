---
id: P01-10
title: "Microbiome + FIT: Does the Microbiome Add Net Benefit to the Screen We Already Have?"
parent: "CBIO003 - Colorectal Cancer Detection From Gut Microbiome (source abstract, 2025)"
---

# Microbiome + FIT: Net Benefit Over the Incumbent Screen

**Parent project:** CBIO003 - microbiome CRC classifier proposed for screening.

## Premise
FIT is the existing cheap CRC screen. A microbiome model only matters if it adds net benefit on top of FIT, measured by decision-curve analysis rather than raw AUC.

## Hypothesis
A fused FIT + microbiome model yields higher net benefit than FIT alone across clinically relevant colonoscopy-referral thresholds.

## Data sources (free/public)
- Cohorts with paired FIT results and metagenomes (subsets of Wirbel/Zeller collections with FIT metadata).
- Published FIT performance distributions (sensitivity/specificity by cutoff) from meta-analyses as simulation priors.

## Method outline
1. In paired data: FIT-only vs microbiome-only vs fused classifier, LOCO evaluation.
2. Where unpaired: probabilistic fusion - sample FIT outcomes from published distributions conditional on case status, combine with microbiome scores.
3. Decision-curve analysis across 1-20% risk thresholds; number-needed-to-scope with and without the microbiome layer; cost per additional advanced neoplasia detected.

## Success gates (locked before results)
- G1: fused model net benefit > FIT-alone across the 2-10% threshold range (paired data or >= 90% of fusion simulations).
- G2: incremental AUC delta >= 0.05 to claim added value.
- G3: cost-effectiveness stated in USD with sensitivity analysis.

## Expected deliverable
`fitplus`: decision-curve web tool - clinicians input prevalence and FIT cutoff, get net-benefit curves and number-needed-to-scope with/without the microbiome layer.

## Failure/pivot rule
If net benefit does not exceed FIT alone, publish the curves saying so - microbiome screening does not currently beat the cheap incumbent. No reframing of the negative.
