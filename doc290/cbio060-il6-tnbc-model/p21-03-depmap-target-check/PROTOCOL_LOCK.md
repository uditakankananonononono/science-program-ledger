# P21-03 Protocol and Gates - LOCKED BEFORE RESULTS (lane D, 2026-09-24 ~12:56 IST)

Spec: doc290/cbio060-il6-tnbc-model/03-depmap-target-check.md. Spec gates kept; amendments locked before
any dependency value is read. (Only Model.csv metadata was inspected, to define the line groups.)

## Data
DepMap 24Q2 Public (figshare article 25880521): CRISPRGeneEffect.csv (Chronos),
OmicsExpressionProteinCodingGenesTPMLogp1.csv, Model.csv.

## Pre-locked amendments
- A1 targets. The P21-01 nominal top-5 model parameters are mapped to genes: kcatSTATPhos -> JAK1 (JAK2 reported
  alongside, not gated), ksynthIL6Gut -> IL6, kRLOn -> IL6R, kRShedding -> ADAM17, kCRPSecretion -> CRP.
  The model is the P21-01 surrogate (BIOMD0000000535), not the unpublished CBIO060 model.
- A2 TNBC lines: breast lines with LegacyMolecularSubtype in {basal_A, basal_B, basal} that have CRISPR data.
  Sensitivity analysis: expression-defined TNBC (breast lines with ESR1 and PGR log2(TPM+1) < 1 and ERBB2
  below the breast median), reported but not gated.
- A3 IL-6 context: median split on IL6 log2(TPM+1) within the TNBC lines that have both CRISPR and expression
  data. Ties at the median go to the low group.
- A4 test per gene: difference = mean Chronos(IL-6-high) - mean Chronos(IL-6-low). One-sided Mann-Whitney U
  (high more negative). BH-FDR across the 5 genes. A gene counts iff difference <= -0.1 AND FDR q < 0.05.
  G1 passes iff at least 2 of the 5 count. Genes missing from the CRISPR matrix count as not meeting it.
- A5 G2: Spearman rho, with a 2,000-sample bootstrap CI over genes, between each gene's best model score
  (P21-01 nominal 50%-inhibition pSTAT3 drop, max over parameters mapped to that gene) and the IL-6-context
  difference (sign flipped, so a larger value means more context-specific dependency). Mapped gene set:
  JAK1 (kcatSTATPhos, KmSTATPhos), IL6 (ksynthIL6Gut, ksynthIL6), IL6R (kRLOn, kRLOff, kRsynth),
  IL6ST (kgp130On, kgp130Off, ksynthsgp130), ADAM17 (kRShedding), CRP (kCRPSecretion, ksynthCRP),
  PTPN2 (VmSTATDephos). Negative or null results are kept.
- A6 G3: line counts per group stated; any group with < 5 lines is labelled exploratory.
- PRISM sensitivity is not used in this build (needs next).
