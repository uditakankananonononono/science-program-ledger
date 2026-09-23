---
id: P16-09
title: "GlueScope: Proteome-Wide Off-Target Degradation Prediction for Molecular Glues"
parent: "CBIO046T - Expanding the Druggable Human Proteome Five-Fold (ISEF 2026 Grand Award)"
---

# GlueScope

**Parent project:** CBIO046T (screened 104M molecules for intended targets; unintended degradation is the unscreened risk).

## Premise
Molecular glues degrade what they recruit - including proteins nobody intended. Thalidomide's teratogenicity was an off-target glue effect (SALL4 degradation) discovered decades after the damage. Modern pipelines screen candidates against the target, not the proteome. Public degrader-treatment proteomics now shows the true neosubstrate spectrum of clinical glues. This project trains a neosubstrate predictor (which proteins will a given glue degrade?) from that public data, builds a degron-motif-aware model of the proteome's degradable surface, and ships a safety screen: candidate glue in; ranked off-target degradation risk panel out.

## Data sources
- Published degrader-treatment mass-spec proteomics (PRIDE deposits): ground-truth neosubstrate lists.
- UniProt (public): proteome sequences for degron-motif scanning.
- PDB/AlphaFold DB: surface-availability of candidate degrons.
- Published clinical-glue selectivity studies (lenalidomide-class) as validation anchors.

## Method outline
1. Harmonize public treatment-proteomics into glue-to-neosubstrate response sets.
2. Learn degron features from confirmed neosubstrates (motif, surface, structure, expression).
3. Train glue-conditioned neosubstrate predictor; validate leave-one-glue-out.
4. Scan the proteome per candidate glue; produce ranked off-target panels with confidence.
5. Retrospective validation: does the model flag SALL4 for thalidomide-class compounds blind?

## Success gates (locked before results)
- G1: leave-one-glue-out recall of known neosubstrates >= 60% in top-100 predictions (the hard, honest bar for this problem).
- G2: retrospective SALL4/thalidomide-class flag recovered blind (positive control).
- G3: proteome degradable-surface map released with per-protein degron evidence.
- G4: false-positive burden quantified and reported - a safety tool that over-alarms is useless, so precision at fixed recall is a headline metric.

## Expected deliverable
GlueScope (candidate in; off-target panel out), the proteome degradable-surface map, and the retrospective validation study - a reusable preclinical safety screen.

## Failure/pivot rule
If G1 fails (likely-hard problem), pivot to the narrower validated core: degron-motif scanner + expression filter as a conservative screen, with the ML layer marked experimental - honest capability labels, gates re-locked.
