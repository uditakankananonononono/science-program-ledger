---
id: P02-08
title: "Peptide Disruptors of the Hepcidin-Ferroportin Interaction: Docking + MD Screen for a BBB-Friendly Modality"
parent: "CBIO006 - Biclonal Antibodies to Prevent Ferroptosis in AD (source abstract, 2025)"
---

# Peptide Disruptors of the Hepcidin-Ferroportin Interaction

**Parent project:** CBIO006 - monoclonal antibodies, which barely cross the blood-brain barrier.

## Premise
The interaction-blocking goal may be met by helical peptides/macrocycles with far better CNS exposure. The co-crystal interface and open design tools make an in silico screen feasible on free compute.

## Hypothesis
>= 5 peptides achieve predicted interface ddG <= -8 kcal/mol with stable binding over 100 ns MD and CNS-appropriate descriptors.

## Data sources (free/public)
- Hepcidin-ferroportin complex structures (PDB); AlphaFold DB.
- ChEMBL/PDSP known hepcidin binders; SwissADME/open ADMET predictors; GROMACS (open MD).

## Method outline
1. Extract interface hot spots from the co-crystal structure.
2. Generate candidates by (a) truncation/alanine-scan of hepcidin's binding helix and (b) FlexPepDock-style docking of a virtual peptide library.
3. Filter by predicted ddG, solubility/aggregation predictors, and CNS MPO descriptors; top 20 to 100 ns GROMACS triage (contact-occupancy stability).

## Success gates (locked before results)
- G1: >= 5 peptides with ddG <= -8 kcal/mol AND >= 70% key-contact occupancy over 100 ns, else the peptide route declared intractable in silico.
- G2: all carried candidates within locked CNS MPO descriptor ranges (score >= 4).
- G3: thresholds locked before any simulation; no post-hoc loosening.

## Expected deliverable
`pepblock`: open pipeline (structure -> hotspot -> peptide library -> MD triage) with the candidate library, all scores, and a ranked shortlist for experimental follow-up.

## Failure/pivot rule
If no peptide passes, quantify why (interface too flat/large for peptide capture) - a design-relevant negative steering back to antibody or small-molecule routes.
