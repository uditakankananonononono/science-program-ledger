---
id: P03-08
title: "Pre-Computing Resistance: An In Silico Mutation Atlas for EZH2 Inhibitor Binding"
parent: "CBIO008T - Deep Learning Pipeline for EZH2 Drug Discovery (source abstract, 2023)"
---

# Pre-Computing Resistance: EZH2 Inhibitor Resistance Mutation Atlas

**Parent project:** CBIO008T - optimizes initial binding only; clinical EZH2 inhibitors already face resistance mutations.

## Premise
Resistance can be prospected in silico: saturating the SET domain with mutations and scoring binding/stability effects predicts which variants break which inhibitors - before they appear in patients.

## Hypothesis
Open energy tools (FoldX/Rosetta ddG + docking) recover known tazemetostat resistance mutations in the top decile of a saturation scan, and the atlas ranks inhibitor scaffolds by resistance vulnerability.

## Data sources (free/public)
- PDB EZH2-inhibitor co-crystal structures.
- Published resistance mutations (tazemetostat/valemetostat literature, COSMIC public tier).
- FoldX / Rosetta (academic-free) for ddG.

## Method outline
1. Saturate all SET-domain residues within 8 A of the binding site (19 substitutions each) on the co-crystal structure.
2. Score per mutation: stability ddG + docking-score shift for >= 3 inhibitor scaffolds; combine into resistance-risk scores.
3. Validate against the locked literature resistance list (recovery rank); cluster mutations into resistance hot spots; compare scaffolds for shared vulnerability.

## Success gates (locked before results)
- G1: known resistance mutations recovered in the top decile of the risk ranking (enrichment >= 5x vs random, p < 0.05).
- G2: per-scaffold vulnerability profiles published; a scaffold with significantly lower predicted vulnerability is identified, or all declared equally vulnerable.
- G3: mutation list and labels frozen before scoring.

## Expected deliverable
`resistatlas`: interactive EZH2 resistance heat map + a tool scoring any new inhibitor pose for mutational vulnerability.

## Failure/pivot rule
If known resistance is not enriched in predictions, publish the calibrated failure of energy-based resistance prospecting at this target - capping how the method should be used.
