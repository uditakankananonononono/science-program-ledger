---
id: P05-06
title: "Are mcSTRs Just MSI in Disguise? Disentangling Micro-Changing STRs from Microsatellite Instability"
parent: "CBIO013 - Micro-Changing Tandem Repeats in 10 Human Cancers (source abstract, 2023)"
---

# Are mcSTRs Just MSI in Disguise?

**Parent project:** CBIO013 - claims mcSTRs are a novel mutation class lacking overlap with known cancer repeats; MSI-high tumors genome-wide STR instability is the obvious alternative explanation.

## Premise
If mcSTR signal concentrates in MSI-high samples, the novelty claim collapses. MSI status is publicly callable, making this a clean, decisive test.

## Hypothesis
In MSI-high tumors mcSTR loci behave like background STRs; in MSS tumors the mcSTR signal either survives (novel class confirmed) or vanishes (MSI artifact).

## Data sources (free/public)
- TCGA MSI status (public MANTIS/MSIsensor calls + MMR expression).
- Genotypes from P05-01; POLE mutation annotations as an orthogonal hypermutator control.

## Method outline
1. Stratify all tumors by MSI status; compare mcSTR length-deviation rates at panel loci vs matched background STR loci within strata.
2. MSS-only re-test of all published mcSTR-cancer associations.
3. POLE-mutant control: does a non-MMR hypermutator also show the signal (instability-general) or not (MMR-specific)?

## Success gates (locked before results)
- G1: panel-vs-background effect in MSS tumors reported with CI; MSS survival of >= 50% of the original effect = novelty supported.
- G2: MSI-high behavior quantified separately; pooling across strata prohibited in headline claims.
- G3: POLE control result reported as mechanistic context either way.

## Expected deliverable
`msi-audit`: the stratification dataset + a novelty certificate per mcSTR locus (MSI-independent / MSI-linked).

## Failure/pivot rule
If the MSS signal vanishes, publish the artifact finding: mcSTRs largely restate MSI - with the corrected, narrower claim stated exactly.
