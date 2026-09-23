---
id: P16-05
title: "LigaseFrontier: Expanding Glue Recruitment Beyond CRBN and VHL"
parent: "CBIO046T - Expanding the Druggable Human Proteome Five-Fold (source abstract, 2026)"
---

# LigaseFrontier

**Parent project:** CBIO046T (candidates recruit CRBN and VHL - the two ligases the entire field uses).

## Premise
The degrader field's dirty secret: ~600 human E3 ligases exist and nearly everything recruits the same two. Tissue-restricted ligases could give tissue-restricted degradation - built-in safety. Public chemoproteomics studies have mapped covalent-fragment engagement of underused ligases (DCAF16, RNF114, FEM1B), and ligase-expression atlases are public. This project builds the first open tractability ranking of the ligaseome for glue recruitment: expression breadth, structural availability, existing chemical handles, and tissue-selectivity potential - then screens glue candidates against the top underused ligases with the parent's latent framework.

## Data sources
- Published chemoproteomics covalent-fragment datasets (PRIDE deposits; Cravatt-lab open data).
- Human Protein Atlas + GTEx (public): ligase tissue expression.
- AlphaFold DB: ligase structure availability.
- UniProt/ESN annotations: the ~600-ligase census.

## Method outline
1. Build the ligaseome census with per-ligase evidence channels (structure, expression, chemical handles, literature).
2. Score tractability with a transparent rubric; rank for glue-recruitment potential.
3. Tissue-selectivity map: which ligases are tumor-lineage-restricted.
4. Adapt the parent's latent model to score recruitment by top underused ligases (transfer-learning test).
5. Publish the ranking + candidate recruiters per ligase.

## Success gates (locked before results)
- G1: census covers >= 90% of annotated E3s with complete evidence channels.
- G2: ranking reproduces the known order (CRBN/VHL/IAPs top-tier by evidence) as sanity - then the interesting part is the next 20.
- G3: >= 5 underused ligases proposed with tissue-selectivity rationale and candidate recruiter molecules, or the honest finding that chemical handles genuinely don't exist beyond the known set.
- G4: transfer-learning honesty: recruitment scores for underused ligases flagged as extrapolations, never validated-looking numbers.

## Expected deliverable
The ligaseome tractability atlas (interactive), the top-20 underused-ligase report with candidate recruiters, and the tissue-selectivity map - a roadmap for the post-CRBN era.

## Failure/pivot rule
If chemical-handle evidence is too thin for G3, pivot to the experimental agenda: which covalent-fragment screens against which ligases would most expand the recruitome - prioritized by tractability score, gates re-locked.
