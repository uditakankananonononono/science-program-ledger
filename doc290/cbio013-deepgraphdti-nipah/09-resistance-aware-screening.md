---
id: P06-09
title: "Escape-Proof Hits: Resistance-Aware Screening Against NiV Glycoprotein Mutant Panels"
parent: "CBIO013 - Fighting Future Pandemics with Novel DeepGraphDTI (source abstract, 2024)"
---

# Escape-Proof Hits: Resistance-Aware Screening

**Parent project:** CBIO013(2024) - screened against wild-type glycoproteins only; a drug that a single mutation defeats is a fragile pandemic asset.

## Premise
Escape-mutation panels can be built in silico: natural henipavirus variation + predicted tolerable mutations at the drug-binding surface. Screening against the panel ranks hits by mutational robustness.

## Hypothesis
The parent's 7 hits differ widely in robustness: >= 2 lose predicted binding against >= 30% of escape-panel mutants, while >= 2 remain robust - and robustness correlates with binding to conserved (low-tolerance) residues.

## Data sources (free/public)
- Natural henipavirus G/F sequence variation (NCBI Virus, public).
- Tolerance prediction via ESM-2 likelihoods / open stability tools; AlphaFold mutant models for docking.

## Method outline
1. Build the locked escape panel: natural variants + top predicted-tolerable substitutions within 8 A of each hit's docked pose.
2. Re-dock/re-score each hit across its mutant panel (batch AlphaFold + docking on free compute).
3. Robustness score per hit = fraction of panel retaining predicted binding; correlate with residue conservation.

## Success gates (locked before results)
- G1: escape panel frozen before scoring (composition published).
- G2: per-hit robustness ranking published; conservation-robustness correlation reported either direction.
- G3: >= 2 hits separated into distinct robustness classes (non-overlapping CIs), else robustness discrimination declared unresolvable in silico.

## Expected deliverable
`escapescan`: an escape-panel builder + robustness-scoring pipeline for any viral target-hit pair.

## Failure/pivot rule
If in silico robustness cannot discriminate hits, publish the resolution limit - wet-lab escape selection is the only way, said plainly.
