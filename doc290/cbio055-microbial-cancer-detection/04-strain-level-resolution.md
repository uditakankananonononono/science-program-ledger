---
id: P18-04
title: "Strain Resolution: Do Strain-Level Markers Beat Species and Function for Cancer Detection"
parent: "CBIO055 - Early Cancer Detection Using Microbial Information (source abstract, 2023)"
---

# Strain Resolution

**Parent project:** CBIO055 Microbial Cancer Detection (taxonomy + microbial function features from >2000 tumor and blood samples; 18% synergy gain in tissue, weaker in cfDNA).

## Premise
The parent compared two levels of resolution: species/genus taxonomy and function. A third level sits between them - strains. Known cancer links are strain-specific: pks+ E. coli (colibactin), enterotoxigenic B. fragilis, specific F. nucleatum subspecies (Zepeda-Rivera et al. 2024 Nature). Species-level tables blur these. This project asks whether strain markers carry the signal that species and function both miss.

## Hypothesis
Adding strain-level features (marker SNV haplotypes, presence of virulence gene clusters such as pks and bft) improves CRC detection by >= 0.03 AUROC over species + function in cross-cohort validation.

## Data sources (free/public)
- CRC stool shotgun cohorts from curatedMetagenomicData with raw reads on ENA/SRA (Zeller 2014, Feng 2015, Yu 2017, Wirbel 2019).
- StrainPhlAn 4 / inStrain for strain profiling; VFDB (virulence factor database, free).
- Zepeda-Rivera et al. 2024 F. nucleatum clade genomes (public NCBI).

## Method outline
1. Select a compute-feasible subset (about 600 samples, 4 cohorts); run StrainPhlAn 4 on key cancer-linked species and screen reads for pks, bft and FadA gene clusters.
2. Build three feature sets: species, function (HUMAnN), strain/virulence markers.
3. Train single and stacked models; evaluate leave-one-cohort-out.
4. Test whether strain markers explain away species-level biomarkers (conditional importance).

## Success gates (locked before results)
- G1: strain + species + function beats species + function by >= 0.03 LOCO AUROC (paired bootstrap p < 0.05).
- G2: pks+ E. coli prevalence higher in CRC than controls in >= 3 of 4 cohorts (positive control).
- G3: per-cohort 95% CIs; null strain gain reported as the result.

## Expected deliverable
Strain-marker feature tables, a cross-cohort gain analysis, and a short list of strain markers that could become targeted qPCR assays.

## Failure/pivot rule
If strain features add nothing (G1 fails) but the positive control passes, pivot to a prevalence atlas of cancer-linked strains across healthy global cohorts to set background rates for future assays.
