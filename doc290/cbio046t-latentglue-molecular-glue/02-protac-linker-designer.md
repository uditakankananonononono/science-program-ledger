---
id: P16-02
title: "LinkerSmith: Generative Optimization of PROTAC Linkers"
parent: "CBIO046T - Expanding the Druggable Human Proteome Five-Fold (source abstract, 2026)"
---

# LinkerSmith

**Parent project:** CBIO046T LatentGlue (latent molecular representations for induced-proximity therapeutics).

## Premise
LatentGlue works on molecular glues; their bigger cousins - PROTACs - fail on a component everyone treats as plumbing: the linker. Linker length, rigidity, and attachment vectors determine ternary-complex geometry, cell permeability, and oral exposure, yet linker design remains trial-and-error. PROTAC-DB 2.0 now publishes thousands of PROTACs with activities and linker structures. This project trains a generative linker designer conditioned on warhead and ligase ligand, predicts degradation-relevant properties, and distills the first open linker-design rules from the full public corpus.

## Data sources
- PROTAC-DB 2.0 (public): PROTAC structures, linkers, activities.
- ChEMBL (public): warhead/ligand activity references.
- PDB: ternary-complex structures for geometry validation.
- ADME benchmark datasets (TDC, public): permeability/exposure evaluation.

## Method outline
1. Parse PROTAC-DB into warhead-linker-ligand triples with activity labels.
2. Descriptive analysis first: linker property vs. activity landscapes (the rules paper).
3. Train a conditional generative model (fragment-constrained diffusion or VAE) for linker proposal.
4. Evaluate generated linkers: synthesizability (SA score), predicted permeability, geometry compatibility vs. known ternary structures.
5. Prospective-style validation: generate linkers for held-out warhead-ligand pairs, compare to the real optimized linkers.

## Success gates (locked before results)
- G1: corpus parsed with >= 80% of PROTAC-DB entries into clean triples.
- G2: linker-property rules reproduce known literature heuristics (sanity) AND surface >= 3 novel statistically-supported rules.
- G3: generated linkers for held-out pairs rank the real optimized linker in the top decile of the generated distribution >= 30% of the time (or the honest lower rate).
- G4: all generated candidates pass synthesizability and PAINS-style filters before reporting.

## Expected deliverable
The open linker-rules analysis, LinkerSmith generator + scorer (tool), and the ternary-geometry validation report.

## Failure/pivot rule
If activity labels prove too noisy for G3 (assay heterogeneity), pivot to the measurement-harmonization study: which activity endpoints in PROTAC-DB are actually comparable - plus a cleaned subset release, gates re-locked.
