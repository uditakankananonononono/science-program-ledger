---
id: P02-03
title: "How Reliable Is Computational Antibody Design? A Public Benchmark of the Parent's Exact Pipeline"
parent: "CBIO006 - Biclonal Antibodies to Prevent Ferroptosis in AD (source abstract, 2025)"
---

# How Reliable Is Computational Antibody Design?

**Parent project:** CBIO006 - ProABC-2 paratope prediction + MODELLER homology modeling + MD + HADDOCK docking to design anti-ferroportin mAbs.

## Premise
The parent chains four computational steps, each with known but rarely quantified error. End-to-end reliability of this exact workflow must be certified on public ground truth before its outputs guide therapeutic claims.

## Hypothesis
The sequence-only antibody-design chain reaches acceptable dock quality (median DockQ >= 0.23) on held-out complexes, but affinity ranking is the weakest stage.

## Data sources (free/public)
- SAbDab (experimental antibody-antigen complexes); AB-Bind and SKEMPI 2.0 affinity datasets.
- Open tools: ImmuneBuilder/ABodyBuilder, Parapred, pyDock/ClusPro, HADDOCK web (free tier).

## Method outline
1. Build a non-redundant SAbDab test set (sequence-only inputs, crystal structures hidden).
2. Run the parent's chain end to end: paratope prediction, Fv modeling, docking; score paratope F1, interface RMSD, DockQ.
3. Affinity-rank correlation on SKEMPI antibody subset; error-propagation analysis from paratope F1 to dock quality.

## Success gates (locked before results)
- G1: end-to-end DockQ distribution on >= 200 non-redundant complexes with CI; usability gate median DockQ >= 0.23.
- G2: affinity ranking Spearman rho >= 0.4 on SKEMPI antibodies, else affinity prediction declared unreliable.
- G3: per-stage metrics published alongside end-to-end; no headline number without stage attribution.

## Expected deliverable
`abbench`: containerized benchmark harness running any sequence-to-dock antibody pipeline against SAbDab/SKEMPI, emitting a signed reliability certificate.

## Failure/pivot rule
If the chain fails G1, publish the error bars for the exact workflow with the breaking stage identified - protecting downstream claims from overconfident docking.
