---
id: P01-04
title: "Does Microbial Function Out-Transport Taxonomy for CRC Detection?"
parent: "CBIO003 - Colorectal Cancer Detection From Gut Microbiome (source abstract, 2025)"
---

# Does Microbial Function Out-Transport Taxonomy for CRC Detection?

**Parent project:** CBIO003 - taxonomy-based Random Forest CRC classifier.

## Premise
Gut microbial function is more conserved across populations than taxonomic composition (functional redundancy). Pathway features - SCFA synthesis, secondary bile-acid transformation, genotoxin production, mucin degradation - should travel better between cohorts than genus names.

## Hypothesis
A function-based classifier beats taxonomy-based LOCO AUC, and combining both views adds further signal.

## Data sources (free/public)
- curatedMetagenomicData shotgun cohorts (Yachida, Wirbel, Thomas, Feng, Hannigan) with HUMAnN3 pathway tables.
- MetaCyc pathway reference.

## Method outline
1. One locked HUMAnN3 run for MetaCyc pathway + EC features per sample.
2. Train identical gradient-boosted models on (a) taxonomy, (b) function, (c) both, under LOCO evaluation.
3. Per-pathway transport scores as in P01-01; direct test of the functional-redundancy explanation (within- vs cross-cohort taxonomy-function correlation).

## Success gates (locked before results)
- G1: function-only mean LOCO AUC >= taxonomy-only by >= 0.03 (bootstrap CI excludes 0).
- G2: combined model beats the better single view by >= 0.02, else combination declared non-additive.
- G3: >= 10 pathways replicate as CRC-associated (FDR < 0.05) in >= 3 independent cohorts.

## Expected deliverable
`funtransport`: harmonized taxonomy+function matrices for 6 cohorts plus a benchmark script reproducing every figure - released as a reusable CRC metagenome benchmark.

## Failure/pivot rule
If function does not beat taxonomy, publish the negative: population-specific taxonomy carries non-redundant CRC signal. Margins locked before unblinding.
