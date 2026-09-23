---
id: P18-05
title: "Redundancy Test: Quantifying Why Microbial Function Predicts Cancer Worse Than Taxonomy"
parent: "CBIO055 - Early Cancer Detection Using Microbial Information (source abstract, 2023)"
---

# Redundancy Test

**Parent project:** CBIO055 Microbial Cancer Detection (taxonomy + microbial function features from >2000 tumor and blood samples; 18% synergy gain in tissue, weaker in cfDNA).

## Premise
The parent's most interesting result was negative: function predicted worse than taxonomy, which she attributed to tumor-microbiome function being more conserved than composition. That was a proposed explanation, not a test. Functional redundancy can be measured directly (Tian et al. 2020 Nat Ecol Evol defined a taxonomic-functional redundancy index). This project tests the parent's explanation head-on.

## Hypothesis
Across cancer types, the ratio of functional to taxonomic between-group variance (PERMANOVA R2) predicts the per-cancer gap between function-only and taxonomy-only accuracy (Spearman rho >= 0.5).

## Data sources (free/public)
- Poore 2020 / Narunsky-Haziza 2022 processed tables (tissue), decontaminated versions from P18-01 where available.
- curatedMetagenomicData stool cohorts across multiple cancers (CRC, adenoma, others available).
- Functional redundancy index method (Tian et al. 2020) and vegan R package.

## Method outline
1. For each cancer type (tissue) and stool cohort, compute taxonomic and functional PERMANOVA R2 for cancer vs control.
2. Compute the functional redundancy index per sample and compare cancer vs control.
3. Retrain taxonomy-only and function-only classifiers with identical settings; record the accuracy gap per group.
4. Correlate the R2 ratio and redundancy with the accuracy gap across groups.
5. Control for feature count by subsampling both views to equal dimensionality.

## Success gates (locked before results)
- G1: Spearman rho >= 0.5 (p < 0.05) between R2 ratio and accuracy gap, or the redundancy explanation is reported as unsupported.
- G2: result holds after equal-dimension subsampling.
- G3: all group-level numbers with 95% CIs.

## Expected deliverable
A per-cancer redundancy map and a tested answer to "when does microbial function add diagnostic value?"

## Failure/pivot rule
If redundancy does not explain the gap (G1 fails), test the alternative: annotation depth. Re-run with UniRef90 gene families vs coarse pathways to see if the gap is an artifact of functional resolution.
