---
id: P05-05
title: "STR Burden and DNA Repair Expression: Mechanism or Confounding? A Mediation Audit with Matched Controls"
parent: "CBIO013 - Micro-Changing Tandem Repeats in 10 Human Cancers (source abstract, 2023)"
---

# STR Burden and DNA Repair Expression: Mechanism or Confounding?

**Parent project:** CBIO013 - global mcSTR burden associated with altered TOP1 and MSH2 expression, implying repair-pathway influence.

## Premise
Tumor purity, proliferation rate, and MSI status all shift both STR burden and repair expression. The mechanistic claim needs confounder-adjusted and mediation-tested reanalysis.

## Hypothesis
After adjusting for purity, proliferation, and MSI status, the mcSTR-burden/TOP1-MSH2 association attenuates >= 50% - or survives as a candidate causal link; mediation analysis separates direct from confounded paths.

## Data sources (free/public)
- TCGA expression + WGS-derived STR burden (from P05-01); purity estimates (ABSOLUTE public); MSI calls (public MANTIS/MSIsensor results).

## Method outline
1. Reproduce the burden-expression association per cancer type with locked covariate sets (none / purity / +proliferation / +MSI).
2. Attenuation curve per association; causal mediation analysis with MSI as mediator vs confounder under explicit DAGs.
3. Negative-control outcomes: expression of non-repair genes matched for baseline level.

## Success gates (locked before results)
- G1: attenuation quantified and published per covariate set; no single-adjustment-only reporting.
- G2: association declared mechanistically plausible only if it survives full adjustment (FDR < 0.05) AND exceeds negative-control outcomes.
- G3: DAGs and mediation assumptions published before results.

## Expected deliverable
`burdenaudit`: a reproducible confounding-audit notebook + adjusted association atlas for all burden-expression pairs tested.

## Failure/pivot rule
If associations vanish under adjustment, publish the corrected interpretation: the burden-repair link is largely confounded - protecting downstream target claims.
