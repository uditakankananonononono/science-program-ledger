# DOC-1-025: Predicting Cell-Cell Communication from Spatial Transcriptomics
Status: DOCUMENTED BOUNDARY - reported to main for adjudication (never self-counted). 2026-09-24.

## Question
Does constraining ligand-receptor predictions to spatially adjacent cluster pairs make them MORE
reproducible across matched tissue sections than unconstrained CellPhoneDB-style scoring?

## Design (GATES.md + Addendum A locked pre-outcome)
DEV = 10x Visium mouse brain sagittal ANTERIOR (2,695 spots, 15 Leiden clusters); FROZEN = matched
POSTERIOR section (3,355 spots, 17 clusters), cross-validated in both directions (A2P, P2A).
955 single-gene CellPhoneDB LR pairs (416 genes present). CellPhoneDB-style permutation scoring
(100 label perms, p<=0.05). Metric: cross-section replication precision@100 (Addendum A: validation
spots assigned to fit clusters by nearest PCA centroid - independent clusterings otherwise have no
shared index). Arms: baseline (all cluster pairs) vs spatial (Delaunay contact >= 10 edges).

## Results (replication precision)
| direction | baseline P@100 | spatial P@100 | P1 soft-weight P@100 | baseline full | spatial full |
|---|---|---|---|---|---|
| A2P | 0.82 | 0.70 | 0.68 | 0.374 | 0.368 |
| P2A | 0.52 | 0.42 | 0.33 | 0.317 | 0.356 |

- G1: sanity PASS (0.82 >= 0.20).
- G2: FAIL - spatial LOSES by 0.12 (A2P) and 0.10 (P2A) against the +0.10 margin.
- P1 (locked, soft contact weighting): FAIL - 0.68 / 0.33.
- G3: both directions agree; boundary stands without adjudication ambiguity.
- G4 (payload): known brain signaling pairs (NRG1->ERBB4, BDNF->NTRK2, FGF1->FGFR2) are broadly
  significant in the baseline (37/89/63 cluster pairs) but the spatial filter DELETES 60-70% of them -
  it removes real signal, not noise. Why: contact-degree correlates 0.757 with cluster SIZE, so the
  adjacency filter is a size filter - it keeps big-cluster interactions and kills small-cluster biology.
  (VEGFA->KDR, NRXN1->NLGN1 absent from the 416-gene LR set; documented.)
- G5: ccc_spatial.py CLI (winning unconstrained arm, honest banner about the tested-and-removed
  spatial filter) smoke PASS: 398 pairs, 5,460 predictions on a 400-spot subset. Teichmann lab.

## Boundary statement (program summary)
Spatial contact information does not improve CCC reproducibility at Visium resolution: contact graphs
on 55-micron multi-cell spots are dominated by cluster-size geometry (corr 0.757), so contact
constraints select anatomy, not signaling. LR co-expression alone replicates better (0.82/0.52 P@100).
The useful spatial signal for CCC lives at single-cell resolution (osmFISH/MERFISH), not spot
resolution. Task-type map, sixth entry: adding a physically-motivated constraint fails when the
constraint's measurement proxy is confounded by geometry (025) - complementing scale-mismatch (024),
augmentation-prior (023), reference-carries-signal (021), library-design (020), and the alignment win
(022).

## Engineering notes
Disk-full (100%) mid-prep caused two silent deaths (exit 120/23) - purged 1.4GB of re-fetchable raw
caches; CellPhoneDB protein_input uses UniProt entry names (ESR1_HUMAN), mapped by suffix strip;
two index bugs caught by assertions/bounds errors before any scoring.

## Reproduce
code/prep_data.py + prep_lr.py (downloads per PROVENANCE.md), code/score_ccc.py, code/score_p1.py,
code/g4_mechanism.py, code/ccc_spatial.py. GATES.md + GATES_ADDENDUM_A.md locked pre-outcome.
