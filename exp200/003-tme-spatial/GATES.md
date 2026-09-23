# DOC-1-003 — Tumor microenvironment as interacting agents: is spatial structure predictable?
# GATES locked 2026-09-23 ~23:10 IST, before any outcome inspection. Lane EXP-1.
# Redesign for 2 CPU/2GB: the multi-agent claim reduces to its testable core - do spots
# (agents) on the tissue lattice show interaction structure that simple covariates cannot
# explain, and do ligand-receptor pairs co-localize beyond chance?

## Data (public; URLs + checksums in results/provenance.md)
- 10x Visium V1 Breast Cancer Block A Section 1 (filtered feature-barcode matrix, 28MB)
  + spatial positions tarball. Single section, honest scope.

## Frozen design
- Spots: in-tissue only. Genes: top 1000 by variance after CPM+log1p (selection on ALL
  spots; no label leakage possible - unsupervised).
- Adjacency: 6-neighbor hex lattice from spot array coordinates.
- Train/test: genes split 500/500 by frozen RNG seed BEFORE any Moran's I computation.
- Metric A (structure predictability): Moran's I per gene on the lattice. Fit ridge
  (mean expression, dropout rate) -> Moran's I on 500 train genes; test on 500 held-out.
- Metric B (interaction payload): 50 pre-registered ligand-receptor pairs (from the
  curated list below) - spatial co-neighborhood correlation (Pearson of spot-level
  ligand vs 1-hop neighbor-mean receptor) vs 500 matched random pairs (matched on mean
  expression decile).

## Success gates
- G1: on held-out genes, predicted vs observed Moran's I Pearson r is BELOW the
  permutation-null 95th percentile - i.e., spatial structure is NOT explained by
  technical covariates (this direction locked: the interesting claim is that biology,
  not chemistry, carries the structure). If r exceeds null (covariates suffice), that
  is the honest negative and the claim inverts.
- G2: median co-neighborhood correlation of the 50 LR pairs exceeds the 95th percentile
  of the matched-random distribution.
- Failure policy (pivot rule): if G2 fails, pivot to receptor->ligand asymmetry or
  2-hop neighborhoods (GATES-v2 locked first). If both fail, documented boundary.
- Payload: per-gene Moran's I table, LR co-localization table, and a CLI that computes
  Moran's I + LR scores for any Visium filtered matrix (the reusable artifact).

## Pre-registered LR pairs (50, frozen now)
Classic TME pairs: CCL2-CCR2, CCL5-CCR5, CXCL12-CXCR4, CXCL9-CXCR3, CXCL10-CXCR3,
CXCL11-CXCR3, CCL19-CCR7, CCL21-CCR7, CXCL13-CXCR5, CCL17-CCR4, CCL22-CCR4, TGFB1-TGFBR1,
TGFB1-TGFBR2, IL6-IL6R, IL6-IL6ST, TNF-TNFRSF1A, TNF-TNFRSF1B, IFNG-IFNGR1, IFNG-IFNGR2,
IL1B-IL1R1, IL1A-IL1R1, CSF1-CSF1R, IL34-CSF1R, VEGFA-KDR, VEGFA-FLT1, VEGFB-FLT1,
PGF-FLT1, ANGPT1-TEK, ANGPT2-TEK, EGF-EGFR, TGFA-EGFR, AREG-EGFR, HGF-MET, FGF2-FGFR1,
FGF7-FGFR2, PDGFB-PDGFRB, PDGFA-PDGFRA, SPP1-ITGAV, SPP1-CD44, LGALS9-HAVCR2,
CD274-PDCD1, PDCD1LG2-PDCD1, CD80-CTLA4, CD86-CTLA4, CD40-CD40LG, TNFSF13B-TACI(*),
MIF-CD74, MDK-LRP1(*), SEMA3C-NRP1(*). (*)=aliases resolved at runtime: TACI=TNFRSF13B,
LRP1 ok, NRP1 ok. Pairs with a gene absent from the matrix are dropped and COUNTED as
missing, not replaced.
