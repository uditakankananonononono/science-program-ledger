---
id: P03-03
title: "Cryptic Pocket Detection, Benchmarked: Do Open Predictors Find Real Hidden Pockets in PRC2 Proteins?"
parent: "CBIO008T - Deep Learning Pipeline for EZH2 Drug Discovery (source abstract, 2023)"
---

# Cryptic Pocket Detection, Benchmarked

**Parent project:** CBIO008T - cryptic pocket discovery feeds compound generation; unvalidated pocket calls poison the whole pipeline.

## Premise
Cryptic pockets are central to the parent's design strategy. Open predictors (PocketMiner, fpocket on MD ensembles, CryptoSite) exist but their real hit rate on held-out cryptic pockets is rarely measured.

## Hypothesis
Open cryptic-pocket predictors recover >= 60% of literature-validated cryptic sites at <= 2 false positives per structure, and short MD ensembles improve recall over static structures.

## Data sources (free/public)
- Curated public cryptic-pocket sets (CryptoSite dataset, PocketMiner paper test set, PDB holo/apo pairs).
- EZH2, EED, SUZ12 structures; GROMACS for MD ensembles.

## Method outline
1. Assemble the locked positive set of validated cryptic pockets (hidden from predictors' training where checkable).
2. Run PocketMiner + fpocket-on-ensemble on all structures; score site-level recall/precision against ligand-observed pockets.
3. Apply the validated stack to PRC2 proteins; rank candidate cryptic sites by druggability score.

## Success gates (locked before results)
- G1: recall >= 60% at <= 2 FP/structure on the held-out cryptic set, else cryptic discovery declared unreliable with current open tools.
- G2: MD-ensemble recall exceeds static-structure recall by >= 10 points (paired test), else MD declared non-worth its cost here.
- G3: PRC2 pocket predictions published with calibrated confidence, including explicit unknowns.

## Expected deliverable
`cryptocheck`: benchmark harness + a PRC2 pocket report, packaged so any protein can be screened with calibrated confidence.

## Failure/pivot rule
If predictors fail G1, publish the calibrated failure and pivot the parent pipeline to known-site docking only - an honest scope cut.
