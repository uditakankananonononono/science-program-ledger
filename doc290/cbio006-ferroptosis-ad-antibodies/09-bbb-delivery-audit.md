---
id: P02-09
title: "The Delivery Problem: A Quantitative Brain-Exposure Model to Choose the Anti-Ferroportin Modality"
parent: "CBIO006 - Biclonal Antibodies to Prevent Ferroptosis in AD (source abstract, 2025)"
---

# The Delivery Problem: Brain-Exposure Modeling for Modality Choice

**Parent project:** CBIO006 - mAb modality chosen without a delivery analysis.

## Premise
Brain exposure differs by orders of magnitude across mAb, nanobody, peptide, and small molecule. A transparent PK/BBB model with public parameters can pick the modality before any wet work.

## Hypothesis
At least one modality achieves modeled brain target engagement >= 50% at published-safe doses for ferroportin blockade; the verdict is robust to 10x exposure uncertainty.

## Data sources (free/public)
- Published brain-to-plasma (Kp,uu) compilations for biologics; open BBB-permeability datasets.
- Transferrin-receptor shuttle enhancement factors from publications; public PK parameter records; ferroportin expression from P02-02/P02-06.

## Method outline
1. Locked evidence table of CNS exposure by modality class (every parameter cited).
2. Mechanistic exposure model: plasma PK + BBB permeation + target-engagement requirement; required dose and feasibility margin per modality.
3. Receptor-mediated-transcytosis shuttle scenarios; 10x Kp,uu sensitivity analysis; modality decision matrix.

## Success gates (locked before results)
- G1: quantitative exposure estimate per modality - no unsourced parameters.
- G2: a modality clears only at modeled engagement >= 50% at safe doses; the verdict table is the core deliverable.
- G3: verdict robust to 10x Kp,uu uncertainty or labeled fragile.

## Expected deliverable
`cnsreach`: transparent exposure-model web app - users adjust PK/BBB parameters and see modality feasibility for any CNS protein target, pre-loaded with the ferroportin case.

## Failure/pivot rule
If no modality reaches engagement at safe doses, publish the honest conclusion: the target is CNS-unreachable by current delivery - the project's core finding.
