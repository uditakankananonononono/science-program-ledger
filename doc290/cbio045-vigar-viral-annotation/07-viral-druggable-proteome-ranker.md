---
id: P15-07
title: "Viral Druggable Proteome: Ranking Antiviral Targets Across Annotated Viral Genomes"
parent: "CBIO045 - Viral Genome Annotation with RNNs (source abstract, 2024)"
---

# Viral Druggable Proteome

**Parent project:** CBIO045 ViGAR (annotation to identify proteins and discover drug therapies).

## Premise
ViGAR's stated goal is drug-therapy research; this project completes that arc at scale. For every annotated viral protein across priority human pathogens, compute a druggability stack: essentiality evidence (conservation, mutational intolerance), structural tractability (pocket prediction on AlphaFold models), existing-chemical starting points (ChEMBL/PubChem similarity), and resistance risk (known variant sites). The output is a cross-virus target-priority atlas: which viral proteins, across which pathogens, are the best computational bets for antiviral development - with pandemic-preparedness weighting for viral families with spillover history.

## Data sources
- RefSeq viral genomes/annotations (public).
- AlphaFold DB viral structures; pocket-prediction tools (open).
- ChEMBL/PubChem (public): antiviral chemical matter.
- NCBI Virus / VIPR-style resources for variant and conservation data.

## Method outline
1. Define priority pathogen set (WHO R&D blueprint + outbreak-history weighting).
2. Compute per-protein features: conservation, structure quality, pocket scores, known-drug proximity, resistance annotations.
3. Build a transparent weighted ranking (no black box - every score decomposable).
4. Validate: do ranked-high proteins recover known successful antiviral targets (held-out)?
5. Release the atlas with per-target evidence pages.

## Success gates (locked before results)
- G1: ranking recovers >= 80% of held-out known antiviral targets in the top quintile.
- G2: atlas covers >= 50 priority pathogens.
- G3: every score decomposes into named evidence channels (auditability requirement).
- G4: >= 20 high-ranking targets with no current drug project in ChEMBL (genuine-gap list), or the certified finding that the obvious targets are all taken.

## Expected deliverable
The cross-virus druggability atlas with evidence pages, the transparent scoring tool, and the genuine-gap target list for antiviral programs.

## Failure/pivot rule
If validation shows conservation features dominate everything (ranking = trivial proxy), pivot to the analysis of what conservation misses: known targets that look unconserved - gates re-locked around a corrected feature design.
