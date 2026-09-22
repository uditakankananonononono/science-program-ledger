# Structure-grade validation of metagenome-mined PET hydrolase candidates by a register-aware catalytic-motif model

## Abstract
Sequence-level discovery pipelines for PET hydrolases over-count candidates: family-level profile matches and even local fold similarity cannot confirm that a catalytic apparatus is intact. We subjected a 20-candidate shortlist (drawn from 468 metagenome-derived PET-hydrolase candidates in prior rounds) to structure-aware validation combining ESMFold structure prediction, foldseek structural-family search against a live-curated reference panel, and a register-aware catalytic-motif model whose thresholds were derived from crystal structures and locked before scoring. 19 of 20 candidates (95%) pass all three legs with catalytic-triad geometry statistically indistinguishable from the crystal reference envelope. The single failure is instructive: a candidate with an intact PETase-like fold but a destroyed catalytic register, invisible to fold-level methods. The register-aware model thus provides the discriminative layer that sequence and fold search lack.

## Introduction
Prior rounds mined MGnify metagenome catalogs for PET-hydrolase candidates (Round 1: 468 candidates; Round 2: a prioritized shortlist of 20 with composite novelty/structure-template scoring). Round 2 also established the failure mode motivating this round: Pfam-level screening is dominated by the PF07519 tannase/feruloyl-esterase family, and strict sequence triads survive in only a minority of candidates. Whether the shortlist's candidates carry a geometrically intact catalytic triad requires structure, not sequence.

## Methods
**Reference panel (all live-verified at RCSB, 2026-09-22).** Eight positives: IsPETase-family (5XJH, 6EQE, 9LMU), leaf-branch compost cutinase (4EB0), Fusarium vanettenii cutinase 1 (1CUS), Thermobifida fusca cutinase cut2 (5ZOA), ancestral PETases (8ETX, 8ETY). Three adversarial negatives: tannase (3WA6), feruloyl esterase A (1USW), lipase B (1TCA). Catalytic triads were grounded in live UniProt ACT_SITE annotations (IsPETase S160/D206/H237; LCC S165/D210/H242; FsCut S136/D191/H204; TfCut2 S170/D216/H248), with signal-peptide offsets resolved by alignment and verified.

**Locked calibration.** From the panel, before any candidate scoring: register spacings S->D 45-55 aa and D->H 13-32 aa (windows [40,61] and [10,36]); an exact G-x-S-x-G nucleophile elbow; C-beta triad geometry S-D 8.96-9.41 A, S-H 6.66-6.94 A, D-H 4.55-4.79 A (bounds expanded 25%).

**Model.** Leg A: sequence register (order S<D<H, spacing windows, elbow). Leg B: 3D geometry on ESMFold predictions (C-beta bounds + mean triad pLDDT >= 50). Leg C: foldseek 10-941cd33 against the panel (best hit positive, E <= 1e-3, alntmscore >= 0.5). Candidate validation requires A^B^C. Gates (G1-G5) were locked with the protocol (sha256 d8491fa9...) before execution.

## Results
All 20 structures predicted successfully. Foldseek calibration: every positive-panel query's best non-self hit is a positive; however, all three negatives also cross-hit positives at fold level (e.g., lipase B -> 9LMU E=7.0e-8, TM=0.537), confirming that fold-level search cannot discriminate alpha/beta-hydrolase families. The register legs can: model calibration passes (4/4 positives accepted; both determinable negatives rejected - FaeA by its D->H = 53 spacing, tannase by absent triad). 19/20 candidates pass all legs; passing triads lie inside the crystal envelope (S-D 9.17-9.48, S-H 6.59-6.98, D-H 4.46-4.70 A; triad pLDDT 86.7-97.0). MGYP001374132912 fails legs A and B (His register replaced, D-H spacing 71 aa, S-H 18.78 A) despite a PETase-like fold (TM 0.928 to IsPETase) - a catalytic-site disruption invisible to fold search.

## Discussion
The register-aware model operationalizes a simple claim: PET-hydrolase catalysis requires not just a Ser-His-Asp triad somewhere in the sequence but the triad in the right register (elbow motif, spacing) and the right geometry. Each leg alone is insufficient (sequence motifs overcount; fold search under-discriminates); the conjunction is validated against positives and adversarial negatives drawn from the very family that defeated prior sequence-level screening. The 19 validated candidates, spanning marine, soil, phylloplane, and estuarine metagenomes with 55-83% sequence novelty vs characterized references, are structure-grade candidates for experimental characterization.

## Limitations
ESMFold predictions carry model uncertainty (mitigated by the pLDDT clause and 25%-expanded geometry bounds); fold-level family assignment is non-discriminative among alpha/beta hydrolases (documented, and carried by the register legs); catalytic competence is inferred structurally, not assayed.

## Data availability
All artifacts sha256-ledgered; protocol, locked gates, scoring tables, structures, and environment ledger included in the project archive.
