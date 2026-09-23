---
id: P01-05
title: "Distilling the Metagenome: A Minimal qPCR-Ready CRC Microbial Panel for Low-Resource Screening"
parent: "CBIO003 - Colorectal Cancer Detection From Gut Microbiome (source abstract, 2025)"
---

# Distilling the Metagenome: A Minimal qPCR-Ready CRC Microbial Panel

**Parent project:** CBIO003 - full-metagenome CRC classifier, accurate but sequencing-dependent.

## Premise
Sequencing is unavailable where CRC screening is most needed. A sparse qPCR panel selected for cross-cohort stability could retain most of the signal at a small fraction of the cost.

## Hypothesis
<= 8 microbial qPCR targets, selected by cross-cohort stability, retain >= 90% of full-metagenome LOCO AUC under realistic qPCR noise.

## Data sources (free/public)
- Harmonized 6-cohort shotgun matrices (curatedMetagenomicData).
- 16S cohorts for cross-platform penalty estimation.
- Published qPCR validation studies of F. nucleatum / pks as external references.

## Method outline
1. Stability selection (1000 subsamples) restricted to markers replicating in >= 3 cohorts.
2. Greedy forward selection under an 8-target budget optimizing LOCO AUC.
3. Simulate qPCR quantization (Ct SD 1.0, 5% limit-of-detection dropout) to estimate real-world degradation.
4. Cost model: per-sample price vs 16S vs shotgun with sensitivity curves; primers drafted via Primer-BLAST-compatible references.

## Success gates (locked before results)
- G1: <= 8-target panel reaches LOCO AUC >= 0.90 x full-model AUC and absolute >= 0.70.
- G2: under simulated qPCR noise, AUC degradation < 0.05.
- G3: panel excludes any marker flagged batch-confounded in P01-02.

## Expected deliverable
`panelpick`: web calculator + R package proposing a minimal qPCR panel per target cohort, with primer references, expected AUC, and per-sample cost.

## Failure/pivot rule
If no <= 8-target panel holds G1, publish the minimal-panel ceiling curve (accuracy vs panel size) and the cost point where screening stops being viable.
