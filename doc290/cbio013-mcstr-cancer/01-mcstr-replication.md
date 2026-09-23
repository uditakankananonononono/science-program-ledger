---
id: P05-01
title: "Do the 182 mcSTRs Replicate? Out-of-Catalog Validation on Fully Public Cancer Genomes"
parent: "CBIO013 - Micro-Changing Tandem Repeats in 10 Human Cancers (source abstract, 2023)"
---

# Do the 182 mcSTRs Replicate?

**Parent project:** CBIO013 - 182 micro-changing STRs across 10 cancer types found using an unpublished ActiveSTRs catalog (174,323 STRs) and ExpansionHunter on 2,622 genomes.

## Premise
The catalog is unpublished - the finding cannot be independently verified as published. Rebuilding the analysis on fully public STR catalogs and genomes tests whether the core result survives open replication.

## Hypothesis
>= 60% of the published mcSTR loci (or their public-catalog equivalents) re-show cancer-type association on independent public WGS data; the rest are catalog-specific.

## Data sources (free/public)
- TCGA WGS (open tier via GDC/ISB-CGC public tables); 1000 Genomes + HGDP WGS (public).
- Public STR catalogs: GangSTR/ExpansionHunter reference panels, Tandem Repeats Finder tracks, STRchive/disease-locus lists.

## Method outline
1. Map the 182 published mcSTRs to public-catalog loci (liftover + motif match); report mapping rate.
2. Genotype with ExpansionHunter (open) on public cancer + control WGS; association test per locus with ancestry PCs and coverage covariates.
3. Replication criteria locked: same direction, FDR < 0.1, effect within 2x of reported.

## Success gates (locked before results)
- G1: >= 90% of loci mapped to public equivalents, else non-mappability is itself the reported reproducibility gap.
- G2: >= 60% replicate under locked criteria; below that, catalog dependence is declared a first-order concern.
- G3: all genotyping parameters version-locked and published.

## Expected deliverable
`mcstr-rep`: the open replication dataset (genotypes at all 182 loci across public genomes) + a reproducibility scorecard per locus.

## Failure/pivot rule
If replication is weak, publish the per-locus scorecard - an honest audit distinguishing catalog artifacts from real cancer STR biology.
