---
id: P06-05
title: "One Screen, Whole Genus: Cross-Reactivity Prediction Across Henipavirus Glycoproteins"
parent: "CBIO013 - Fighting Future Pandemics with Novel DeepGraphDTI (source abstract, 2024)"
---

# One Screen, Whole Genus: Henipavirus Cross-Reactivity

**Parent project:** CBIO013(2024) - screened only NiV; Hendra, Cedar, Langya, and Ghana virus share the G/F architecture - a broad-spectrum opportunity.

## Premise
A hit that binds conserved glycoprotein surfaces across henipaviruses is worth more than a NiV-only hit. Conserved-pocket mapping + cross-species docking can rank candidates by breadth.

## Hypothesis
>= 2 conserved, druggable surface patches exist across henipavirus G/F proteins, and >= 3 of the screened 1,040 drugs score well across >= 3 species at those patches.

## Data sources (free/public)
- PDB/AlphaFold structures for NiV, HeV, Cedar, Langya, GhV G and F proteins.
- The parent's 1,040-drug boxes (MMv Priority/Pandemic/Pathogen boxes - open compound lists).

## Method outline
1. Multiple-structure alignment; conservation scoring per surface residue (locked alignment).
2. Pocket detection across all species; cluster into conserved patch candidates; druggability scoring.
3. Cross-species docking of the full 1,040-drug set at the top patches; breadth-ranked hit list.

## Success gates (locked before results)
- G1: >= 2 conserved patches with druggability score above the locked threshold, or genus-wide targeting is declared unsupported.
- G2: >= 3 drugs in the top decile across >= 3 species at one patch, else the breadth hit list is declared empty.
- G3: conservation map published independent of docking outcomes.

## Expected deliverable
`henipabroad`: the conserved-patch atlas + breadth-ranked screening tool reusable for any viral genus.

## Failure/pivot rule
If no conserved druggable patch exists, publish the conservation map showing why broad-spectrum henipavirus small molecules are structurally unlikely - redirecting to per-species or biologic approaches.
