# GATES (LOCKED 2026-09-24 07:59, BEFORE any outcomes) - DOC-1-026: A "Cell Atlas" of Viral Infection

## Claim tested
Does a DATA-DRIVEN core antiviral program (learned from one viral infection) detect infection response in
a held-out virus better than the named curated ISG signature (MSigDB Hallmark Interferon Response)?

## Data (public, eligibility verified pre-lock)
- Lee et al 2020, Sci Immunol 5:eabd1554 ("Immunophenotyping of COVID-19 and influenza..."), via
  cellxgene census 2025-01-30 (dataset de2c780c): COVID-19 31,463 / influenza 10,519 / normal 17,590
  PBMC cells, 14 cell types.
- DEV: COVID-19 vs normal. FROZEN: influenza vs normal (held-out-virus external validation).
- Stratified subsample (seed 7, frozen pre-run to results/subsample.json): 6 most abundant cell types,
  up to 1,200 cells per disease x cell-type group.

## Arms
- BASELINE (named published): MSigDB HALLMARK_INTERFERON_ALPHA_RESPONSE + _GAMMA_RESPONSE gene sets
  (Liberzon et al 2015, Cell Systems 1:417; via Enrichr MSigDB_Hallmark_2020 GMT). Score = mean
  log-normalized expression of set genes per cell (alpha and gamma averaged, genes present only).
- TOPIC ARM: data-driven core program: NMF (k=10) on dev COVID+normal log-normalized matrix; component
  with the largest dev infection-AUROC is the "core program"; score = its top-50 genes' mean expression.

## Metric (locked)
Per-cell-type AUROC of infection (vs normal) from the arm's score; summary = mean AUROC across the 6
major cell types.

## Gates (ISEF-aligned)
- G1 (baseline): baseline dev mean AUROC recorded. Sanity halt: if < 0.70 (ISGs strongly separate
  COVID from healthy PBMCs in this dataset's paper), pipeline problem - document, stop.
- G2 (topic arm): PASS if topic dev mean AUROC >= baseline dev + 0.02 (locked margin).
- G3 (frozen, held-out virus): PASS if topic frozen mean AUROC >= baseline frozen + 0.02 AND topic
  frozen >= topic dev - 0.05. If baseline wins G2, G3 validates the baseline and the topic loss stands.
- G4 (mechanism): gene overlap learned-program vs ISG set (Jaccard); per-cell-type transfer pattern
  (monocytes expected strongest per Lee et al); presence of canonical ISGs (ISG15, MX1, IFIT1/2/3) in
  the learned top-50.
- G5 (tool + nomination): atlas_score.py CLI (counts CSV -> infection-response score + per-cell-type
  AUROC table if labels given, honest scope banner), smoke-tested. Nomination: Villani lab (MGH/Broad)
  - single-cell immunology of infection.

## Pre-registered failure tree
- G2 FAIL -> P1: per-cell-type data-driven program (top-30 DE genes by Wilcoxon within each cell type,
  scored within cell type), same margin -> FAIL -> DOCUMENTED BOUNDARY: data-driven programs add nothing
  over the curated ISG signature for cross-virus infection detection; the shared antiviral program IS
  the interferon program. No other pivots; thresholds never relax after outcomes.

## Constraints
Real public data only; hashes in PROVENANCE.md; 2CPU/1.9GB (stratified subsample, float32); no money;
no sending as the user.
