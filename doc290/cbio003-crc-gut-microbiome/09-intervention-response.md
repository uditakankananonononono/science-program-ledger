---
id: P01-09
title: "Can CRC-Linked Microbiome Features Predict Who Responds to Diet and FMT Interventions?"
parent: "CBIO003 - Colorectal Cancer Detection From Gut Microbiome (source abstract, 2025)"
---

# Can CRC-Linked Microbiome Features Predict Intervention Response?

**Parent project:** CBIO003 - biomarkers proposed as therapeutic targets.

## Premise
The protective taxa the parent found (Ruminococcaceae, Christensenellaceae) are fiber-fermenters implicated in diet/FMT response. If baseline microbiome features predict intervention response, trials can be responder-enriched.

## Hypothesis
CRC-linked taxa and pathway modules predict responder status in public diet and FMT intervention cohorts, portably across studies.

## Data sources (free/public)
- Wastyk 2021 fiber/fermented-food trial metagenomes (SRA).
- Mediterranean-diet Prevotella studies; public FMT cohorts (IBD/metabolic) with responder labels via MGnify/SRA.

## Method outline
1. Extract parent marker taxa + P01-04 pathway modules as candidate predictors.
2. Per cohort, test baseline features vs locked responder definitions; random-effects meta-analysis across studies (I^2 heterogeneity).
3. Train a responder-prediction gradient-boosted model on the largest cohort; LOCO-test on the rest.

## Success gates (locked before results)
- G1: >= 3 CRC-linked markers associate with response in >= 2 independent cohorts (same direction, FDR < 0.1).
- G2: responder-prediction LOCO AUC >= 0.70 on at least one intervention type, else prediction declared non-portable.
- G3: if I^2 > 75% for all markers, context-dependence is the declared conclusion.

## Expected deliverable
`respmod`: meta-analysis package for microbiome intervention cohorts, harmonized public dataset, and a responder-enrichment calculator for trial designers.

## Failure/pivot rule
Non-portability or high heterogeneity is a locked valid outcome: intervention response is idiosyncratic and precision-microbiome trials lack stratification biology - stated with evidence.
