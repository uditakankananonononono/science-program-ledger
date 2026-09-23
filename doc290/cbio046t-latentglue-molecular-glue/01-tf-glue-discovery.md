---
id: P16-01
title: "TF-Glue: Molecular Glue Discovery for Transcription Factor Oncoproteins"
parent: "CBIO046T - Expanding the Druggable Human Proteome Five-Fold (source abstract, 2026)"
---

# TF-Glue

**Parent project:** CBIO046T LatentGlue (635M-parameter glue model; screened a-Synuclein and KRAS G12D).

## Premise
LatentGlue screened a synucleinopathy target and a GTPase; the highest-value undruggable class is transcription factors - MYC, mutant p53, fusion drivers like EWS-FLI1 - long called undruggable because they lack pockets. Molecular glues are the one modality with proven TF precedent (e.g., the clinical degradation of IKZF1/3 by IMiDs). This project retrains the parent's latent framework on glue-activity data and screens against priority TF oncoproteins, using dependency data (DepMap) to prioritize which TF degradations would actually kill which cancers - target selection driven by measured essentiality, not fashion.

## Data sources
- DepMap (Broad, public): CRISPR dependency scores for TF essentiality ranking.
- ChEMBL/PubChem (public): known glue and degrader activity data for retraining.
- AlphaFold DB / PDB: TF structure availability (and honest disorder assessment).
- PRISM drug-repurposing screens (public): unexpected degradation signals.

## Method outline
1. Rank TF oncoproteins by dependency x prevalence across DepMap lineages.
2. Retrain latent glue-activity model with public degrader datasets; validate on held-out known glues.
3. Screen top-3 TF targets; score candidates with activity + predicted E3 recruitment.
4. Disorder-aware filtering: flag candidates whose predicted binding region is structurally unresolvable (honesty constraint).
5. Cross-check top candidates against PRISM for serendipitous existing signals.

## Success gates (locked before results)
- G1: retrained model matches parent's reported gains (RMSE/Spearman within 10% of published deltas) on held-out glue data before new screens.
- G2: TF priority ranking completed with full dependency evidence per target.
- G3: >= 3 candidate glues per top target with predicted recruitment mechanism, or the certified negative that TF surfaces resist the current chemical space (with the evidence).
- G4: disorder-honesty: no candidate reported for regions without structural/confidence support.

## Expected deliverable
The TF-glue candidate report with per-target evidence, the dependency-driven target-ranking tool, and the retrained model with benchmarks.

## Failure/pivot rule
If G3 returns the certified negative, pivot to mapping *why*: which chemical-space regions glue models never explore for disordered targets - a design-gap paper that steers library synthesis, gates re-locked.
