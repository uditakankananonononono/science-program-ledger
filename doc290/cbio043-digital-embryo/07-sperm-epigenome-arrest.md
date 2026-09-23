---
id: P14-07
title: "Paternal Layer: Sperm Epigenome and Small-RNA Contributions to Embryo Arrest"
parent: "CBIO043 - Digital Embryo: Multi-Omic Arrest Prediction (ISEF 2026 Grand Award)"
---

# Paternal Layer

**Parent project:** CBIO043 Digital Embryo (six-omic integration - all of it effectively maternal/embryonic).

## Premise
The Digital Embryo's six omics all measure the embryo and its maternal context; the paternal contribution is a blind spot. Sperm delivers more than DNA: methylation patterns, small RNAs, and protamine-bound chromatin state influence preimplantation development, and public sperm epigenome/small-RNA datasets with IVF outcomes exist. This project adds the missing seventh layer: quantify how much embryo-arrest variance is paternally predictable, identify the paternal epigenetic programs involved, and test the field's working assumption that sperm contributes ~nothing measurable beyond aneuploidy.

## Data sources
- GEO: sperm methylome and small-RNA datasets with IVF/embryo outcomes (multiple public cohorts).
- Published sperm chromatin (protamine/histone retention) datasets.
- Human embryo scRNA references for mapping paternal-effect programs onto arrest stages.
- gnomAD for population variant context.

## Method outline
1. Harmonize sperm epigenome datasets with embryo-outcome labels (fertilization, blastocyst, arrest stage).
2. Build paternal-only predictors; establish the variance ceiling vs. embryonic/maternal models.
3. Identify candidate paternal programs (imprinted regions, tRNA-derived small RNAs, retained-histone loci).
4. Cross-reference paternal-effect loci with embryo-stage expression to propose mechanisms.
5. Meta-analyze against published negative studies; report the field-level evidence balance.

## Success gates (locked before results)
- G1: paternal-only prediction beats chance with cross-cohort AUC >= 0.65, or the certified result bounds the paternal contribution below a named threshold - both are field-relevant.
- G2: >= 1 paternal program replicates across >= 2 independent cohorts at FDR < 0.1.
- G3: meta-analysis quantifies publication bias in this literature (or certifies its absence).
- G4: honest-negative clause strongly applies: "sperm epigenome adds < X% predictive variance" is a complete publishable result.

## Expected deliverable
The paternal-variance ceiling estimate, a "PaternalLayer" analysis package, the replicated-program report, and a field-level evidence-balance paper.

## Failure/pivot rule
If cohort labels are too inconsistent (outcome definitions vary), pivot to a methods paper on outcome-definition harmonization for paternal-effect studies, with the reanalysis showing how conclusions flip under harmonized labels.
