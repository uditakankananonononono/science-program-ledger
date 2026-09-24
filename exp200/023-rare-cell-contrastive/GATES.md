# GATES (LOCKED 2026-09-24 07:41, BEFORE any outcomes) - DOC-1-023: Detecting Rare Cell Types with Contrastive Learning

## Claim tested
Does a contrastive-learning (SimCLR-style) cell embedding detect a rare pancreatic cell type better than the
standard published pipeline (PCA + Leiden clustering) as the type gets rarer?

## Data (public, frozen at download, hashes in PROVENANCE.md)
- DEV cohort: Tabula Muris FACS (Smart-seq2) Pancreas, 1,327 labeled cells / 9 classes (Schaum 2018).
- FROZEN cohort: Tabula Muris droplet (10x) Pancreas, annotations_droplets.csv (platform-shift validation).
- Rare target: pancreatic PP cell (107 cells = 8.1% of FACS Pancreas; hormone Ppy).

## Controlled rarity (committed pre-run to results/rarity_grid.json)
Background = all non-PP cells (1,220). Rarity grid r in {0.5%, 1%, 2%, 5%}: n_PP = 6, 12, 25, 64 sampled
seed 7 (nested subsets: each larger grid point contains the smaller one's cells). Evaluation at each r:
dataset = background + that PP subset.

## Representations (fit per rarity grid point on that grid point's cells only)
- BASELINE (named published pipeline): log1p(CPM1e4) -> HVG-2000 -> PCA-50 -> kNN graph (k=15) -> Leiden
  (resolution 1.0, seed 7). Wolf et al 2018 Genome Biol 19:15 (scanpy pipeline); Traag et al 2019 Sci Rep
  9:5233 (Leiden). Implemented faithfully with sklearn + igraph + leidenalg.
- TOPIC ARM: SimCLR-lite encoder MLP 2000-256-64; augmentations = 10% gene-dropout mask + Gaussian noise
  sigma 0.1; NT-Xent tau 0.5; Adam 1e-3, 30 epochs, batch 128; same HVG input; then THE SAME Leiden
  pipeline on the 64-d embedding.

## Scoring (locked)
Per grid point: Leiden clusters -> each cluster assigned the majority ground-truth label among its cells
(standard benchmark convention, identical for both arms; deployment claims are NOT made from this).
PRIMARY metric: PP-class F1. Secondary: PP recall. Report per grid point; summary = mean F1 over the grid.

## Gates (ISEF-aligned)
- G1 (named baseline): baseline PP F1 curve over the grid recorded. Sanity halt: if baseline F1 at r=5%
  < 0.5, treat as data/pipeline problem, document, stop (PP cells are transcriptionally distinct).
- G2 (topic arm): PASS if contrastive mean-F1 over the grid >= baseline mean-F1 + 0.03.
- G3 (frozen external validation): full protocol refit on the 10x Pancreas cohort (own background/PP pool,
  same grid, same margins vs ITS OWN baseline). PASS: contrastive frozen mean-F1 >= frozen baseline + 0.03
  AND winner frozen mean-F1 >= its dev mean-F1 - 0.10 (platform-shift allowance). If baseline wins G2, G3
  validates the baseline and the topic arm's loss stands.
- G4 (biological interpretation): neighbor purity of PP cells (fraction of each PP cell's 15 nearest
  neighbors that are PP, per representation, at r=1%); PP marker check (Ppy, Ppy expression vs background,
  Sst for D-cell contamination); pre-registered augmentation ablation at r=1%: dropout-mask-only vs
  noise-only, same protocol.
- G5 (tool + nomination): detect_rare.py CLI (counts CSV + target marker or label column -> Leiden clusters
  on the better representation, rare-cluster report), smoke-tested. Nomination: Regev lab (Broad) -
  rare cell type discovery.

## Pre-registered failure tree
- G2 FAIL -> P1: projection 64->128 + epochs 30->60, same margin -> FAIL -> DOCUMENTED BOUNDARY:
  contrastive pretraining gives no rare-type detection advantage over PCA+Leiden at single-tissue scale;
  detection is bounded by clustering granularity, not representation. No other pivots; thresholds never
  relax after outcomes.

## Constraints
Real public data only; sources + hashes in PROVENANCE.md; 2CPU/1.9GB (float32, torch.set_num_threads(2));
no money; no sending as the user.
