---
id: P18-02
title: "Stool Synergy Transfer: Does Taxonomy + Function Synergy Hold in Non-Invasive Stool Metagenomes"
parent: "CBIO055 - Early Cancer Detection Using Microbial Information (source abstract, 2023)"
---

# Stool Synergy Transfer

**Parent project:** CBIO055 Microbial Cancer Detection (taxonomy + microbial function features from >2000 tumor and blood samples; 18% synergy gain in tissue, weaker in cfDNA).

## Premise
The parent found strong taxonomy+function synergy in tumor tissue but weak synergy in blood, blaming fragmented cfDNA. Stool is the other non-invasive sample, and unlike cfDNA it yields full-length reads with complete gene content. If the synergy is real biology, it should reappear in stool shotgun metagenomes for colorectal cancer, where many independent public cohorts exist.

## Hypothesis
In CRC stool metagenomes, combined taxonomic + functional (gene family / pathway) models beat either alone by >= 5% relative balanced accuracy under leave-one-cohort-out validation.

## Data sources (free/public)
- curatedMetagenomicData (Bioconductor): MetaPhlAn taxonomy and HUMAnN pathway/gene-family tables for CRC cohorts (Zeller 2014, Feng 2015, Yu 2017, Vogtmann 2016, Wirbel 2019, Thomas 2019 and others).
- Wirbel et al. 2019 Nat Med meta-analysis signatures for comparison.
- SIAMCAT R package for standardized ML and cross-cohort evaluation.

## Method outline
1. Pull harmonized taxonomy and HUMAnN pathway tables for all CRC vs control stool cohorts in curatedMetagenomicData.
2. Train taxonomy-only, function-only and combined models (LASSO, random forest) with SIAMCAT.
3. Evaluate by leave-one-cohort-out (LOCO); compute relative balanced-accuracy gain of combined vs best single view.
4. Repeat for adenoma vs control to test whether synergy holds at the early-detection stage.
5. Compare synergy size in stool against the parent's tissue (18%) and blood numbers.

## Success gates (locked before results)
- G1: combined LOCO AUROC >= 0.80 for CRC vs control.
- G2: relative gain of combined over best single view >= 5% in at least 60% of held-out cohorts.
- G3: adenoma vs control reported regardless of outcome; a null adenoma result is recorded as the early-detection ceiling.
- G4: per-cohort 95% CIs; pooled-only claims prohibited.

## Expected deliverable
A cross-cohort synergy table (tissue vs blood vs stool), open SIAMCAT pipeline, and a ranked list of functions that add signal beyond taxonomy.

## Failure/pivot rule
If no synergy appears (G2 fails), pivot to explaining why: test the parent's functional-redundancy idea directly by comparing between-group variance explained by taxonomy vs function across the same cohorts.
