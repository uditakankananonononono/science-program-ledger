---
id: P03-04
title: "Do VAE-Generated Drug Candidates Survive Reality? Synthesizability, Docking, and Novelty Audit of Generative Chemistry"
parent: "CBIO008T - Deep Learning Pipeline for EZH2 Drug Discovery (source abstract, 2023)"
---

# Do VAE-Generated Drug Candidates Survive Reality?

**Parent project:** CBIO008T - variational autoencoder generates drug-like compounds after pocket discovery.

## Premise
Generative chemistry models produce plausible-looking molecules that often fail synthesizability, stability, or docking. The MOSES/GuacaMol public benchmarks exist exactly to measure this - the parent's generator should be scored on them, then on the actual EZH2 pocket.

## Hypothesis
An open generative stack passes standard MOSES distribution metrics, but < 20% of generated EZH2-targeted molecules survive a full synthesizability + docking + PAINS filter - quantifying the real yield of generative design.

## Data sources (free/public)
- MOSES and GuacaMol benchmarks; ChEMBL training sets; SA score and PAINS filters (RDKit, open).
- PDB EZH2 structures for pocket-conditioned generation (e.g., open pocket-conditioned models like Pocket2Mol weights if license permits).

## Method outline
1. Train/run an open VAE + a pocket-conditioned generator on public weights; generate 10k molecules per mode.
2. Score: validity, uniqueness, novelty, FCD, scaffold diversity (MOSES standard), SA score, PAINS/reactive filters.
3. Dock survivors into the EZH2 SET domain; report survival funnel from 10k generations to docking-passing candidates.

## Success gates (locked before results)
- G1: MOSES validity >= 95%, uniqueness >= 90%, novelty vs ChEMBL >= 80% - else generator declared below field standard.
- G2: full-funnel survival rate reported; "useful yield" gate: >= 50 molecules passing all filters with docking score better than the known-inhibitor median.
- G3: every reported molecule shipped as SMILES with its full filter trace - no cherry-picked examples.

## Expected deliverable
`genaudit`: a generative-chemistry auditing tool that runs any SMILES generator through the full reality funnel and returns calibrated yield statistics.

## Failure/pivot rule
If useful yield is < 1 in 1000, publish the funnel analysis showing where generative chemistry loses molecules - redirecting the parent to virtual screening over enumerated libraries instead.
