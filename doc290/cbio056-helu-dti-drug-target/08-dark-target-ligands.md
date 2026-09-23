---
id: P19-08
title: "Dark Targets: Ligand Prediction for Understudied Druggable Proteins"
parent: "CBIO056 - HeLU-DTI: Drug Target Prediction via Deep Learning (source abstract, 2023)"
---

# Dark Targets

**Parent project:** CBIO056 HeLU-DTI (protein/drug language-model embeddings + disease knowledge graph in a heterogeneous GNN; beat baselines on BindingDB and BioSNAP).

## Premise
Most DTI data covers a few hundred well-studied proteins. The NIH Illuminating the Druggable Genome (IDG) program lists hundreds of "Tdark" and "Tbio" kinases, GPCRs and ion channels with almost no known ligands. These are exactly where a model that "finds targets not previously known" would matter, and exactly where it is least tested.

## Hypothesis
Models trained on well-studied family members transfer to understudied members with AUROC >= 0.65 when evaluated on the few known ligands, and performance tracks sequence similarity to studied relatives.

## Data sources (free/public)
- Pharos / TCRD target development levels (IDG, public).
- ChEMBL and IUPHAR/BPS Guide to Pharmacology ligands (public).
- AlphaFold DB structures for understudied targets.

## Method outline
1. Split targets by IDG level: train on Tclin/Tchem, test on Tbio/Tdark members with >= 5 known actives.
2. Use property-matched decoys (DUD-E style) for negatives.
3. Compare sequence-only, pocket-aware (see P19-04) and family-transfer fine-tuning.
4. Model performance as a function of nearest-studied-relative identity.
5. Score a public library (e.g., ChEMBL approved drugs) against the top understudied targets to nominate repurposing candidates.

## Success gates (locked before results)
- G1: mean AUROC >= 0.65 on understudied targets with known actives.
- G2: performance vs identity trend reported with CI; a flat curve at chance is the finding.
- G3: nominated candidates filtered for PAINS and reported with confidence scores, not as claims.

## Expected deliverable
A dark-target benchmark, transfer curves, and a ranked nomination list for understudied proteins.

## Failure/pivot rule
If transfer fails (G1 fails), pivot to ranking which understudied targets are closest to "learnable" - a prioritization map for where new assays would most help models.
