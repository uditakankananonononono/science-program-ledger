---
id: P14-04
title: "RPL Signature: Maternal Multi-Omic Prediction of Recurrent Pregnancy Loss"
parent: "CBIO043 - Digital Embryo: Multi-Omic Arrest Prediction (ISEF 2026 Grand Award)"
---

# RPL Signature

**Parent project:** CBIO043 Digital Embryo (cross-omic failure signatures in early development).

## Premise
Recurrent pregnancy loss (RPL) affects ~2% of couples and ~50% of cases stay unexplained after standard workup. The Digital Embryo proved coordinated cross-omic failure is detectable in embryos; this project applies the same logic to the maternal side: integrate public decidua, maternal blood transcriptome, and immunophenotyping datasets to find cross-omic signatures that separate explained from unexplained RPL - and test whether "unexplained" RPL is molecularly heterogeneous (multiple distinct failure programs hiding under one label), which would redirect the entire diagnostic workup.

## Data sources
- GEO: decidua and endometrial datasets from RPL vs. control cohorts (multiple public studies).
- Maternal peripheral-blood transcriptome RPL datasets (public).
- Published immunophenotyping (NK-cell, Treg) RPL study data where deposited.
- ClinVar/gnomAD for the known-genetic-cause exclusion filter.

## Method outline
1. Assemble RPL datasets; apply strict phenotype curation (exclude explained cases using published criteria).
2. Unsupervised cross-cohort clustering: does unexplained RPL resolve into stable molecular subtypes?
3. Train subtype-vs-control classifiers with leave-one-cohort-out validation.
4. Map subtypes to proposed mechanisms (immune dysregulation, decidualization defect, thrombophilia signature) via gene-program enrichment.
5. Propose a subtype-directed workup algorithm; estimate what fraction of "unexplained" cases each subtype explains.

## Success gates (locked before results)
- G1: >= 2 stable molecular subtypes replicate across >= 3 independent cohorts, or the certified finding is that public-data RPL is not subtype-resolvable at current sample sizes.
- G2: subtype classifier cross-cohort AUC >= 0.72.
- G3: each subtype maps to a named, literature-supported mechanism (enrichment FDR < 0.05).
- G4: honest-negative clause: a certified "insufficient resolution" result includes the sample-size calculation for what would suffice.

## Expected deliverable
An RPL subtype map, an "RPL-Resolve" classifier (input: maternal blood/decidua profile; output: subtype with confidence + suggested workup), and the mechanism-enrichment report.

## Failure/pivot rule
If subtypes do not replicate (G1), pivot to the evidence-gap deliverable: a harmonization standard for RPL cohort deposition, demonstrated by showing which published cohorts would have been jointly analyzable under it.
