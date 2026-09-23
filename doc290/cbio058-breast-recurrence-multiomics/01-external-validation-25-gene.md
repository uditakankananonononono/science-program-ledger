---
id: P20-01
title: "Out-of-Cohort Test: Validating the 25-Gene Recurrence List in Independent Breast Cancer Cohorts"
parent: "CBIO058 - Deep-Learning to Predict Breast Cancer Recurrence (source abstract, 2023)"
---

# Out-of-Cohort Test

**Parent project:** CBIO058 Breast Recurrence (AIME autoencoder integrating expression + CNV with ER-status confounder adjustment, random forest recurrence classifier, 25-gene list).

## Premise
The parent derived 25 recurrence genes from TCGA-BRCA alone. TCGA has short follow-up for breast cancer and few recurrence events; Liu et al. 2018 (Cell) flagged its disease-free endpoints as weak for BRCA. A gene list is only useful if it predicts recurrence in other patients. METABRIC and SCAN-B give thousands of independent patients with long follow-up.

## Hypothesis
A score built from the 25 genes stratifies distant-recurrence or relapse-free survival in METABRIC and at least two GEO cohorts (hazard ratio >= 1.5 top vs bottom tertile), and adds prognostic value beyond PAM50 subtype and clinical stage.

## Data sources (free/public)
- METABRIC expression and clinical data (cBioPortal, public).
- SCAN-B RNA-seq cohort GSE96058 (GEO, public).
- GEO relapse cohorts: GSE2034, GSE7390, GSE1456.
- TCGA-BRCA open-tier data and the TCGA Pan-Cancer Clinical Data Resource (Liu 2018).

## Method outline
1. Map the 25 genes across platforms (Illumina arrays, Affymetrix, RNA-seq); drop genes missing from a platform and record coverage.
2. Build a fixed-weight score in TCGA (no refitting in validation cohorts).
3. Test with Cox models in each cohort; adjust for age, stage/size, nodes, grade, ER and PAM50.
4. Compare against random 25-gene sets (1,000 draws) - many random sets are prognostic in breast cancer (Venet et al. 2011), so this is the key control.

## Success gates (locked before results)
- G1: HR >= 1.5 (top vs bottom tertile, p < 0.05) in METABRIC and >= 2 of 4 other cohorts.
- G2: beats >= 95% of random 25-gene sets in METABRIC.
- G3: adds prognostic value beyond clinical + PAM50 (likelihood-ratio p < 0.05), or the null is reported.

## Expected deliverable
A cross-cohort validation report, a portable scoring script, and a random-signature comparison figure.

## Failure/pivot rule
If the list does not beat random sets (G2 fails), pivot to asking which parts of it are proliferation proxies, and whether any non-proliferation genes carry independent signal.
