---
id: P14-02
title: "Mouse-to-Human Arrest Transport: Cross-Species Stress Test of Multi-Omic Embryo Signatures"
parent: "CBIO043 - Digital Embryo: Multi-Omic Arrest Prediction (source abstract, 2026)"
---

# Mouse-to-Human Arrest Transport

**Parent project:** CBIO043 Digital Embryo (multi-omic arrest prediction and cross-omic failure signatures).

## Premise
Nearly all embryo-intervention research happens in mouse first, but nobody has systematically certified which arrest biology transports from mouse to human and which is mouse-only. The Digital Embryo showed arrest is a coordinated cross-omic failure in human; public mouse embryo atlases are richer than human ones. This project builds matched multi-omic arrest classifiers in both species and tests cross-species transport directly: train mouse, test human; train human, test mouse. The output is either a validated cross-species core program (making mouse screens more predictive for human IVF) or a precise map of where the species barrier sits - either way, every mouse study citing human relevance gets an evidence grade.

## Data sources
- Mouse embryo single-cell atlases: Deng et al. 2014 (GSE45719) and successor atlases on GEO.
- Human embryo scRNA-seq: Yan et al. 2013 (GSE36552), Petropoulos et al. 2016 (E-MTAB-3929), Stirparo et al. 2018.
- Ortholog maps: Ensembl Compara / MGI (public).
- Published mouse arrest-induction studies (culture-stress, maternal-age models) for label construction.

## Method outline
1. Build ortholog-matched gene space (1:1 orthologs, Ensembl Compara) between mouse and human embryo datasets.
2. Define comparable arrest/failure labels in both species (developmental delay, degeneration, blastocyst failure).
3. Train species-specific classifiers; test bidirectional cross-species transport with and without batch correction.
4. Decompose failure: which gene programs transport (e.g., DNA-damage response) and which are species-specific (e.g., implantation machinery).
5. Grade published mouse-to-human intervention claims against the transport map.

## Success gates (locked before results)
- G1: within-species held-out AUC >= 0.80 in both species (baseline sanity).
- G2: cross-species transport certified only if AUC >= 0.70 in the harder direction; otherwise certified non-transport with the blocking programs named.
- G3: >= 1 named gene program shown to transport with effect-size replication across >= 3 independent dataset pairs, or none certified.
- G4: honest-negative clause: certified species-barrier map counts as full success.

## Expected deliverable
The bidirectional transport matrix, a "SpeciesBridge" auditor tool (input: mouse-study gene claims; output: transport-evidence grade for human relevance), and the conserved-vs-divergent arrest-program map.

## Failure/pivot rule
If comparable arrest labels cannot be constructed across species (label instability), pivot to a label-ontology paper: a cross-species developmental-failure nomenclature validated by inter-dataset consistency - gates re-locked.
