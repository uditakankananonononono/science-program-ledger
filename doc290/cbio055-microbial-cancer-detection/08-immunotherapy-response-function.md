---
id: P18-08
title: "Response Function: Gut Microbial Function as a Predictor of Immunotherapy Response"
parent: "CBIO055 - Early Cancer Detection Using Microbial Information (source abstract, 2023)"
---

# Response Function

**Parent project:** CBIO055 Microbial Cancer Detection (taxonomy + microbial function features from >2000 tumor and blood samples; 18% synergy gain in tissue, weaker in cfDNA).

## Premise
The parent used microbial signal to detect cancer. A closely related, clinically urgent question is whether it predicts who responds to immune checkpoint inhibitors. Taxonomic response signatures have failed to replicate across cohorts (Lee et al. 2022 Nat Med). The parent's idea - adding function to taxonomy - has not been tested systematically here.

## Hypothesis
Combined taxonomy + function models predict ICI response in melanoma with higher cross-cohort AUROC (>= +0.05) than taxonomy alone.

## Data sources (free/public)
- Lee et al. 2022 Nat Med melanoma ICI stool metagenomes (5 cohorts, public ENA accession in paper).
- Gopalakrishnan 2018, Matson 2018, Frankel 2017 and Routy 2018 ICI stool metagenomes (public SRA/ENA; several also in curatedMetagenomicData).
- McCulloch et al. 2022 Nat Med melanoma ICI cohort (public).

## Method outline
1. Uniformly profile all cohorts with MetaPhlAn 4 + HUMAnN 3 (or curatedMetagenomicData tables where present).
2. Train taxonomy, function and combined models; evaluate leave-one-cohort-out.
3. Test response-linked functions (e.g., SCFA, inosine, bile-acid pathways) as prior-driven features vs data-driven.
4. Adjust for antibiotic and PPI use where recorded.

## Success gates (locked before results)
- G1: combined LOCO AUROC exceeds taxonomy-only by >= 0.05 (paired bootstrap p < 0.05).
- G2: combined LOCO AUROC >= 0.65 in at least 3 held-out cohorts.
- G3: prior-driven function set reported separately; per-cohort 95% CIs.

## Expected deliverable
A harmonized ICI microbiome table, cross-cohort benchmark, and a ranked list of response-linked functions.

## Failure/pivot rule
If nothing replicates (G2 fails), pivot to a power analysis: how many patients a future cohort needs to detect the effect sizes seen in any single study.
