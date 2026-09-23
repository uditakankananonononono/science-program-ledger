---
id: P01-03
title: "Strain-Level Oncomicrobe Markers Beat Genus Calls: pks+ E. coli, bft+ B. fragilis, F. nucleatum Clades"
parent: "CBIO003 - Colorectal Cancer Detection From Gut Microbiome (source abstract, 2025)"
---

# Strain-Level Oncomicrobe Markers Beat Genus Calls

**Parent project:** CBIO003 - genus-level biomarkers including Escherichia-Shigella, which mixes pathogenic and commensal strains.

## Premise
The carcinogenic action of gut bacteria lives at strain/virulence-locus resolution: the pks island (colibactin), bft (fragilysin), and F. nucleatum subspecies. Genus calls dilute this signal.

## Hypothesis
A classifier trained on strain/virulence-locus features beats the parent's genus-resolution model by a locked margin and links mechanistically to pks-associated mutational signatures in tumor genomes.

## Data sources (free/public)
- Shotgun metagenomes: Yachida 2019, Wirbel 2019, Thomas 2019 (SRA).
- GTDB references; VFDB; pks/bft/clb locus sequences from NCBI.
- PCAWG tumor WGS mutational-signature (SBS88) annotations where paired.

## Method outline
1. StrainPhlAn 4 / inStrain strain profiling; ShortBRED + hmmsearch quantification of pks, bft, clb families per sample.
2. Train identical gradient-boosted classifiers at genus, species, strain, and virulence-locus resolutions on identical nested CV folds; LOCO evaluation.
3. Correlate pks+ abundance with SBS88 burden in the paired tumor subset (orthogonal validation).

## Success gates (locked before results)
- G1: strain/locus-resolution LOCO AUC exceeds genus-resolution by >= 0.05 absolute on >= 4 of 6 cohorts (paired bootstrap p < 0.05).
- G2: pks+ abundance vs SBS88 signature Spearman rho >= 0.4, p < 0.01 in the paired subset.
- G3: all resolution levels compared on identical folds; no metric cherry-picking.

## Expected deliverable
`strainpanel`: Nextflow pipeline from raw reads to virulence-locus CRC risk score, with a static offline reference bundle (pks/bft/clb HMMs).

## Failure/pivot rule
If strain resolution fails G1, publish the redundancy finding - genus calls capture the portable signal and strain pipelines add cost without accuracy.
