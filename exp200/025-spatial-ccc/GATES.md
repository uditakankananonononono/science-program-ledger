# GATES (LOCKED 2026-09-24 07:55, BEFORE any outcomes) - DOC-1-025: Predicting Cell-Cell Communication from Spatial Transcriptomics

## Claim tested
Does constraining ligand-receptor (LR) interaction predictions to spatially adjacent cluster pairs make
them MORE reproducible across biological replicates (matched tissue sections) than unconstrained
CellPhoneDB-style scoring?

## Data (public, hashes in PROVENANCE.md; existence verified pre-lock)
- DEV section: 10x Visium V1_Mouse_Brain_Sagittal_Anterior (filtered_feature_bc_matrix 54MB + spatial 8MB).
- FROZEN section: V1_Mouse_Brain_Sagittal_Posterior (54MB + 9MB) - matched biological replicate.
- LR reference: CellPhoneDB-data interaction_input.csv (ventolab/CellphoneDB-data, Efremova et al 2020
  Nat Protoc 15:1484). Only interactions whose partners are both single genes present in the matrix
  (complexes dropped, documented). Curated set frozen at results/lr_pairs.json BEFORE scoring.

## Prep (per section, identical)
In-tissue spots only; log1p(CPM1e4); Leiden clusters (kNN k=10 on PCA-30, resolution 1.0, seed 7) -
cluster maps frozen per section at prep (results/clusters_*.json).

## Scoring (CellPhoneDB-style, faithful simplification, locked)
For LR pair (L,R) and ordered cluster pair (A,B): score = mean_L(A) * mean_R(B) on log-normalized
expression. Null: P=100 spot-label permutations; one-sided empirical p = P(null >= obs)/P.
Significant: p <= 0.05. Prediction set per arm per section: significant (LR, A->B) triples ranked by
observed score.
- BASELINE (named published method): all cluster pairs eligible (Efremova 2020).
- TOPIC ARM (spatial): cluster pair (A,B) eligible ONLY if A,B have >= 10 contact edges in the spot
  Delaunay contact graph of THAT section.

## Metric (locked)
Cross-section replication precision: fit predictions on one section, count fraction also significant
(p <= 0.05) on the other. PRIMARY: precision@100 (top 100 by score per arm). Secondary: full-set
precision + prediction-set sizes.

## Gates (ISEF-aligned)
- G1 (baseline): dev-anterior baseline precision@100 on frozen-posterior recorded. Sanity halt: < 0.20
  = pipeline problem, document, stop.
- G2 (topic arm): PASS if spatial precision@100 >= baseline precision@100 + 0.10 (locked margin).
- G3 (frozen/direction swap): fit posterior, validate anterior, same margin. Winner stability:
  |precision difference between directions| <= 0.15.
- G4 (biological interpretation): literature LR pairs in adult mouse brain (Nrg1-Erbb4, Vegfa-Kdr,
  Nrxn1-Nlgn1, Bdnf-Ntrk2, Fgf1-Fgfr2): which are significant per arm; contact-degree vs cluster-size
  bias check on the adjacency filter.
- G5 (tool + nomination): ccc_spatial.py CLI (matrix + coords + LR table -> prediction table with
  per-section replication fields), smoke-tested. Nomination: Teichmann lab (Sanger) - CellPhoneDB.

## Pre-registered failure tree
- G2 FAIL -> P1: soft distance-decay weighting (cluster-pair score weighted by contact count, no hard
  filter), same margin -> FAIL -> DOCUMENTED BOUNDARY: spatial contact constraint does not improve
  cross-section reproducibility at Visium spot resolution; spot multicellularity swamps contact
  information. No other pivots; thresholds never relax after outcomes.

## Constraints
Real public data only; hashes in PROVENANCE.md; 2CPU/1.9GB; no money; no sending as the user.
