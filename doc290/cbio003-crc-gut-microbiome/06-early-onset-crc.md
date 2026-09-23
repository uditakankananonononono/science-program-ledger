---
id: P01-06
title: "The Early-Onset CRC Microbiome: A Distinct Signal or a Younger Copy of the Same One?"
parent: "CBIO003 - Colorectal Cancer Detection From Gut Microbiome (source abstract, 2025)"
---

# The Early-Onset CRC Microbiome

**Parent project:** CBIO003 - CRC microbiome classifier without age stratification.

## Premise
Early-onset CRC (< 50 years) is rising globally. Whether it carries a distinct microbial signal - or the same signal at younger ages - determines whether screening models must be age-stratified.

## Hypothesis
EOCRC has a partially distinct, replicating microbiome signature that a shared model misses.

## Data sources (free/public)
- Yachida 2019 and Wirbel 2019 cohorts with age metadata.
- EOCRC-focused SRA submissions; TCGA-COAD/READ tissue microbiome (contamination-corrected) as an orthogonal layer.

## Method outline
1. Partition < 50 / >= 50; entropy-balance controls to case age/BMI distribution within strata.
2. Train three classifiers: shared-signal, shifted (shared features, stratum thresholds), distinct (independent features); nested CV + LOCO.
3. Quantify age confounding: predict age from the microbiome, partial it out, re-evaluate case-control AUC.

## Success gates (locked before results)
- G1: EOCRC case-control AUC on >= 2 cohorts with >= 30 EOCRC cases; power reported if below.
- G2: EOCRC-trained model beats late-onset-trained model on held-out EOCRC by >= 0.05 AUC, else the shared-signal null is accepted.
- G3: if case-control AUC drops below 0.60 after age partialling, age confounding is declared the primary finding.

## Expected deliverable
`eo-crc-atlas`: harmonized early/late-onset comparison dataset, three-model verdict, and a library for age-balanced case-control metagenomic testing.

## Failure/pivot rule
If no distinct replicating EOCRC signal emerges, publish the powered null - useful against a hypothesis the field keeps asserting without age-controlled evidence.
