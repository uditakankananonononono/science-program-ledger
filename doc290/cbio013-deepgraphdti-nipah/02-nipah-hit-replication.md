---
id: P06-02
title: "Re-Testing the 7 Nipah Hits: Orthogonal Open Docking and Consensus Scoring"
parent: "CBIO013 - Fighting Future Pandemics with Novel DeepGraphDTI (source abstract, 2024)"
---

# Re-Testing the 7 Nipah Hits

**Parent project:** CBIO013(2024) - 7 drugs selected against NiV attachment (G) and fusion (F) glycoproteins after DTA screening + docking verification.

## Premise
Single-pipeline hits carry single-pipeline artifacts. An independent re-test with open docking stacks, multiple protein conformations, and consensus scoring either hardens or deflates the hit list - for free.

## Hypothesis
<= 4 of the 7 hits reproduce across >= 2 orthogonal docking methods and >= 2 glycoprotein conformations; the reproducible subset is the defensible hit list.

## Data sources (free/public)
- NiV G and F structures (PDB) + AlphaFold models; multiple conformations/states where available.
- Open docking: AutoDock Vina/smina, Gnina (CNN scoring), plus consensus rescoring; the parent paper's hit identities.

## Method outline
1. Prepare the 7 hits + 50 property-matched decoys (hidden labels) per target.
2. Dock with two open engines against >= 2 conformations each; ensemble/consensus scoring; measure hit-vs-decoy separation.
3. Pose plausibility check against known glycoprotein functional sites (receptor-binding, fusion peptide regions).

## Success gates (locked before results)
- G1: a hit "replicates" only if it scores in the top decile vs decoys in >= 2 engines on >= 2 conformations; per-hit verdicts published.
- G2: decoy separation (EF10%) reported per engine/conformation - proving the assay can discriminate at all.
- G3: decoy list generated and frozen before docking.

## Expected deliverable
`nivrecheck`: the frozen re-test dataset + per-hit consensus verdicts + a reusable ortho-docking protocol for any DTA-screen hit list.

## Failure/pivot rule
If the assay cannot separate known binders from decoys (G2 fails), publish the assay limitation first - hit verdicts are then withheld as uninterpretable, honestly.
