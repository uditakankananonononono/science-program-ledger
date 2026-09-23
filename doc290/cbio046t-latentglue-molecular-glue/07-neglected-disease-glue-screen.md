---
id: P16-07
title: "Glue the Neglected: Degrader Discovery for Parasitic-Disease Targets"
parent: "CBIO046T - Expanding the Druggable Human Proteome Five-Fold (source abstract, 2026)"
---

# Glue the Neglected

**Parent project:** CBIO046T (glue screening against major disease targets - all high-income-market indications).

## Premise
Glue discovery has never been aimed at the diseases that kill the most people per research dollar: malaria, leishmaniasis, Chagas. Parasite proteomes are publicly annotated, essentiality data exists from large knockout screens (e.g., PlasmoDB piggyBac mutagenesis), and parasite-targeted degradation has a mechanistic shortcut - some parasites import host-like ubiquitin machinery or harbor divergent ligases humans lack (selectivity for free). This project adapts the parent's latent framework to parasitic essential proteins, screens for glue candidates exploiting both parasite and host recruitment machinery, and ranks by the selectivity angle that makes a hit developable.

## Data sources
- PlasmoDB/VEuPathDB (public): parasite genomes, essentiality screens, expression.
- ChEMBL (public): antimalarial/antiparasitic activity data.
- AlphaFold DB: parasite protein structures.
- PubChem/PDSP-style public screening data for repurposing signals.

## Method outline
1. Rank parasite essential proteins by knockout-screen evidence x druggability gap.
2. Map parasite ubiquitin-ligase machinery; flag human-divergent components (selectivity candidates).
3. Transfer the parent's glue model to parasite targets; benchmark on known antiparasitic degraders if any exist.
4. Screen; score candidates on predicted activity + selectivity (parasite vs. human machinery).
5. Cross-check candidates against public phenotypic-screen actives for hidden degradation mechanisms.

## Success gates (locked before results)
- G1: essential-target ranking completed for >= 3 parasite species with full evidence.
- G2: >= 10 candidate glues with predicted parasite-selective recruitment, or the certified negative that public parasite data can't support glue prediction yet.
- G3: >= 3 candidates overlap known phenotypic actives (repurposing-fast-track list), with mechanism hypotheses.
- G4: human-cross-reactivity risk panel completed for every reported candidate.

## Expected deliverable
The parasitic-disease glue candidate report, the parasite-ligase divergence map, and the repurposing-fast-track list - an open starting pack for neglected-disease drug programs.

## Failure/pivot rule
If G2 certifies the data gap, pivot to the enabling dataset: which parasite proteomics/chemoproteomics experiments would unlock computational glue discovery - costed and prioritized, gates re-locked.
