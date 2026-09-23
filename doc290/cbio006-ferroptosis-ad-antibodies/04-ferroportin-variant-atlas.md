---
id: P02-04
title: "The Ferroportin Structure and Variant Atlas: Population Diversity, Disease Mutations, Safe Epitope Surfaces"
parent: "CBIO006 - Biclonal Antibodies to Prevent Ferroptosis in AD (source abstract, 2025)"
---

# The Ferroportin Structure and Variant Atlas

**Parent project:** CBIO006 - antibodies against ferroportin's hepcidin-binding site; binding must not block iron efflux and must work across ancestries.

## Premise
SLC40A1 is the only mammalian iron exporter. Its structures, hemochromatosis mutations, and population variants define where an antibody can bind safely - a question answerable computationally before any wet work.

## Hypothesis
At least two exposed, cross-population-conserved epitope patches exist > 15 A from the iron conduit; energy calculations can rank them for safe antibody targeting.

## Data sources (free/public)
- PDB SLC40A1 structures + AlphaFold DB; gnomAD v4 variants; ClinVar disease mutations; 1000 Genomes.
- Open energy tools: FoldX / Rosetta flex ddG.

## Method outline
1. Map all gnomAD + ClinVar variants onto the structure; classify by region (hepcidin site, conduit, extracellular loops); per-residue missense tolerance.
2. Identify candidate safe epitopes: exposed, >99% allele concordance across populations, > 15 A from conduit residues.
3. FoldX/Rosetta ddG scan of variant effects on hepcidin binding (AlphaFold model with confidence masking); ancestry equity report for any epitope-affecting variant AF > 0.1%.

## Success gates (locked before results)
- G1: complete published variant map - every gnomAD/ClinVar SLC40A1 variant classified with structural rationale.
- G2: >= 2 safe epitope patches clearing all criteria, or the safe-epitope hypothesis declared false.
- G3: ancestry equity flags included in the headline output, not an appendix.

## Expected deliverable
`ferroportinatlas`: interactive 3D variant/epitope viewer (Mol*) + scoring API ranking arbitrary epitope surfaces for safety and population equity.

## Failure/pivot rule
If no patch clears the criteria, flag the antibody approach as structurally risky at this target and publish why - a real constraint finding.
