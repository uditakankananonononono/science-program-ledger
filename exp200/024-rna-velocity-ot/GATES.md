# GATES (LOCKED 2026-09-24 07:47, BEFORE any outcomes) - DOC-1-024: Reconstructing Developmental Trajectories with RNA Velocity + Optimal Transport

## Claim tested
Does adding optimal-transport coupling to RNA velocity reconstruct a developmental trajectory better than
the velocity graph alone (scVelo, the named published baseline)?

## Data (public, hashes in PROVENANCE.md)
- DEV: pancreas endocrinogenesis E15.5 (Bastidas-Ponce et al 2019, Development 146:dev173849), via
  scvelo.datasets.pancreas (endocrinogenesis_day15.h5ad, 3,696 cells x 27,998 genes, spliced/unspliced
  layers, 8 annotated clusters).
- FROZEN: dentate gyrus neurogenesis (Hochgerner et al 2018, via scvelo.datasets.dentategyrus).
- Canonical lineage (locked, from the source papers):
  DEV edges (7): Ductal->Ngn3 low EP, Ngn3 low EP->Ngn3 high EP, Ngn3 high EP->Pre-endocrine,
  Pre-endocrine->{Alpha,Beta,Delta,Epsilon}.
  FROZEN edges: Radial-Glia-like->Astrocytes, Radial-Glia-like->nIPC, nIPC->Neuroblast,
  Neuroblast->Granule-immature, Granule-immature->Granule-mature (adjusted to the dataset's actual
  cluster names at prep time, committed to results/canonical_edges.json BEFORE scoring).

## Arms
- BASELINE (named published): scVelo stochastic velocity: scv.pp.filter_and_normalize + moments +
  scv.tl.velocity(mode='stochastic') + scv.tl.velocity_graph; cluster-level net transition flow from the
  velocity graph. Bergen et al 2020, Nat Biotechnol 38:1408-1414.
- TOPIC ARM: OT-refined trajectory. Same fitted velocity; expression pseudotime bins (50 bins on diffusion
  pseudotime, scanpy DPT, Haghverdi 2016 Nat Methods); Sinkhorn couplings (epsilon=0.05, 200 iters, numpy)
  between consecutive bins; cost C_ij = ||x_i - x_j|| - lambda * cos(v_i, x_j - x_i), lambda=1.0;
  cluster-level transitions from OT mass.

## Scoring (locked)
Canonical edge (A->B) recovered iff net flow from A's cells to B's cells EXCEEDS the reverse (forward >
backward). Score = #recovered / #canonical. Wrong = #canonical edges with backward > forward.

## Gates (ISEF-aligned)
- G1 (baseline): scVelo score recorded. Sanity halt: if baseline recovers < 4/7 on dev (its published
  behavior on this dataset is strong), pipeline problem - document, stop.
- G2 (topic arm): PASS if OT score > baseline score on dev, OR (both = 7/7 AND OT wrong <= baseline
  wrong AND OT spurious-mass fraction <= baseline's). Margin pre-registered, no relaxation.
- G3 (frozen): full protocol on dentate gyrus, same rule vs its own scVelo baseline; winner stability:
  winner frozen score >= winner dev score - 2 edges.
- G4 (mechanism): which canonical edges does the baseline mis-orient and does OT fix exactly those?
  Velocity magnitude vs OT mass on corrected edges; marker check (Neurog3 peaks in Ngn3 high EP; Ins1
  high in Beta).
- G5 (tool + nomination): trajectory_ot.py CLI (spliced/unspliced CSVs + labels -> cluster transition
  table + canonical-edge score), smoke-tested. Nomination: Theis lab (Helmholtz) - trajectory inference.

## Pre-registered failure tree
- G2 FAIL -> P1: lambda sweep {0.5, 2.0}, same margin -> FAIL -> DOCUMENTED BOUNDARY: OT coupling adds
  nothing over the raw velocity graph at single-timepoint scale; velocity alone carries the lineage
  signal. No other pivots; thresholds never relax after outcomes.

## Constraints
Real public data only; hashes in PROVENANCE.md; 2CPU/1.9GB; no money; no sending as the user.
