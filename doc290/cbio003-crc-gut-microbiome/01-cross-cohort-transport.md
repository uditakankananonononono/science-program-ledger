---
id: P01-01
title: "CRC Microbiome Classifier Cross-Cohort Transport Stress Test"
parent: "CBIO003 - Colorectal Cancer Detection From Gut Microbiome (source abstract, 2025)"
---

# CRC Microbiome Classifier Cross-Cohort Transport Stress Test

**Parent project:** CBIO003 - Random Forest CRC classifier on Indian-population gut microbiome data (AUC 0.992, accuracy 0.947; genus biomarkers Ruminococcaceae UCG-002, Christensenellaceae R-7, Streptococcus, Prevotella-2, Escherichia-Shigella).

## Premise
The parent validated on one population. Microbiome classifiers are notorious for cohort overfitting; nobody has measured whether an Indian-cohort-trained model transports to other populations, or which biomarkers replicate.

## Hypothesis
LOCO (leave-one-cohort-out) AUC will drop well below the single-cohort figure, but a core set of taxa replicates across cohorts and defines the portable signal.

## Data sources (free/public)
- curatedMetagenomicData R package: Wirbel 2019, Zeller 2014, Yachida 2019, Thomas 2019, Feng 2015, Vogtmann 2016 CRC cohorts.
- GMrepo and NCBI SRA for published Indian CRC 16S/metagenomic cohorts.

## Method outline
1. Harmonize all cohorts to genus-level relative abundance with one locked pipeline.
2. Train the parent's Random Forest recipe per cohort; evaluate full LOCO AUC matrix.
3. Baselines: age/BMI/geography-only models to quantify confounding.
4. SHAP feature ranks per cohort; transport score = Spearman rank correlation of top-20 features per cohort pair, with 1000-permutation null.

## Success gates (locked before results)
- G1: mean LOCO AUC >= 0.75 (95% CI) across >= 6 cohort pairs for a "transportable" verdict.
- G2: >= 5 taxa with cross-cohort SHAP rank correlation rho >= 0.6 (permutation p < 0.05).
- G3: geography-only baseline AUC < 0.70, else cohort confounding dominates and G1 is void.

## Expected deliverable
`crc-transport-audit`: CLI + notebook returning the LOCO matrix, transport scores, and a one-page certificate of which biomarkers replicate; frozen harmonized 6-cohort benchmark included.

## Failure/pivot rule
If LOCO AUC < 0.75 or no taxa replicate, the deliverable becomes a certified non-transport report quantifying where single-cohort CRC microbiome models break - a publishable negative, no post-hoc feature engineering.
