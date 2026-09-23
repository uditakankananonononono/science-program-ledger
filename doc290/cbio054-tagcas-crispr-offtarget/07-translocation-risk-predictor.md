---
id: P17-07
title: "TranslocaScan: Predicting Chromosomal Translocations From Multi-Guide Cutting"
parent: "CBIO054 - 3D-Aware CRISPR Off-Target Prediction (ISEF 2026 Grand Award)"
---

# TranslocaScan

**Parent project:** CBIO054 (off-targets as point mutations; the scarier 3D-mediated failure is rearrangement).

## Premise
Single off-target mutations are the measured risk; translocations are the catastrophic one. When two cuts happen simultaneously - two guides, or one guide plus an off-target - free ends rejoin across chromosomes, and 3D genome contact frequency is the physics that determines which ends meet. Published translocation-capture datasets (LAM-HTGTS-class assays) give ground truth. This project predicts translocation junction landscapes from cut positions + Hi-C contact maps + repair-context features, quantifies how much 3D contact frequency alone explains (the mechanistic claim), and scores multiplex editing protocols for rearrangement risk before they reach patients.

## Data sources
- Published translocation-capture sequencing datasets (LAM-HTGTS and successors; SRA deposits).
- 4DN/ENCODE Hi-C for the assayed cell types.
- crisprSQL: off-target cut-site candidates feeding the pair enumeration.
- Published multiplex-editing safety reports (open literature) for validation.

## Method outline
1. Harmonize translocation-junction datasets with bait/prey metadata and cell-type Hi-C.
2. Feature set: contact frequency at multiple resolutions, cut-site distance-to-loop-anchors, repair-signature tracks.
3. Train junction-frequency predictor; ablate to isolate 3D contribution.
4. Protocol scanner: given a multiplex guide set + predicted off-targets, enumerate dangerous cut pairs and rank protocols by rearrangement risk.
5. Validate against published multiplex-safety findings.

## Success gates (locked before results)
- G1: junction-frequency prediction R^2 >= 0.5 held-out, with 3D ablation showing >= 30% of explained variance from contact features - or the honest alternative driver named.
- G2: >= 3 public translocation datasets harmonized and modeled.
- G3: protocol scanner's risk ranking agrees with published multiplex-safety results in >= 70% of comparisons.
- G4: all risk scores shipped with confidence tiers; no unscored protocols.

## Expected deliverable
TranslocaScan (multiplex guide set in; rearrangement-risk ranking + dangerous-pair list out), the 3D-contribution study for rearrangements, and the harmonized junction dataset.

## Failure/pivot rule
If public junction data is too assay-biased for G1, pivot to the assay-comparability study first: which capture methods yield combinable junction frequencies - gates re-locked around a cleaned subset.
