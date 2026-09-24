# GATES - DOC-1-027 (locked 2026-09-24 08:12 IST, BEFORE any model fitting or scoring)

## Claim
A graph neural network that exploits spatial neighborhood structure (DSTG-style, He et al 2021)
deconvolves spatial spot mixtures better than per-spot non-negative least squares, the published core
of SPOTlight (Elosua-Bayes et al 2021 NAR) / Stereoscope (Andersson et al 2020 Nat Commun), on
simulated Visium-like spots with known ground truth, and the advantage survives a frozen held-out
cohort (disjoint cells, shifted mixture regime).

## Data (eligibility verified BEFORE this lock)
Tabula Muris FACS Lung, raw counts (verified integer-like, 1620 cells x 23433 genes, log1p copy
matches), 16 annotated types. Types with >= 20 cells (10 types: B cell, T cell, dendritic cell,
endothelial cell, leukocyte, macrophage, monocyte, natural killer cell, stromal cell,
type II pneumocyte) retained; rare types (<=14 cells) excluded from BOTH signature and spots.
Cells of retained types split 50/50 stratified by type: half A = signature + DEV spots,
half B = FROZEN spots (disjoint cells). Split committed before any scoring.

## Simulation (ground truth known)
Spots at random coords in unit square; latent Gaussian random field (length-scale 0.15, seed-locked)
discretized into regions; each region assigned a dominant type (cycling the 10 types); spot mixture =
Dirichlet(alpha=2) centered on region profile (dominant type weight 0.45, rest shared) x 5-10 cells
sampled from that region's available pool. Spot counts = sum of member cell raw counts. kNN graph
k=6 on coords. DEV = 2000 spots (half A cells, seed 11, Dirichlet alpha 2). FROZEN = 2000 spots
(half B cells, seed 23, Dirichlet alpha 0.5 - sparser, harder mixtures).

## Arms
- BASELINE: NNLS per spot against signature matrix (mean log1p-normalized expression per type over
  half A cells, top 2000 HVGs). Published core of SPOTlight/Stereoscope - the named baseline.
- GNN: 2-layer GraphSAGE (hidden 128, ReLU, dropout 0.1), input = spot log1p-normalized expression
  (same 2000 genes), softmax output over 10 types, cross-entropy against true mixture, Adam lr 1e-3,
  <= 60 epochs, early stop on 20% held-out dev spots. torch threads=2, no_grad at eval.
- MLP ABLATION (G4 only): identical architecture/training WITHOUT message passing.

## Metric
Per-cell-type Pearson r between predicted and true proportions across spots; mean over the 10 types.
Also JSD per spot (secondary, reported).

## Gates
- G1 (sanity halt): NNLS dev mean r >= 0.50. Else pipeline problem - document, stop.
  (Published simulated-benchmark NNLS values are 0.6-0.8; premise = structured mixtures are
  deconvolvable from a 10-type lung signature. Sanity-check this premise BEFORE relying on it:
  half of the types are immune and share markers.)
- G2 (dev): GNN dev mean r >= NNLS dev mean r + 0.05.
- G3 (frozen): GNN frozen mean r >= NNLS frozen mean r + 0.05 AND GNN frozen mean r >= GNN dev - 0.10.
- Failure tree: if G2 fails -> ONE pre-registered rescue P1 = k=12 graph + hidden 256, same data
  split, same gates; if P1 also fails, or G3 fails -> DOCUMENTED BOUNDARY (no further arms).
- G4 (mechanism, runs regardless): MLP ablation delta (GNN - MLP); report honestly if < 0.02
  ("graph contributes nothing"). Biological interpretation: spatial autocorrelation of tissue
  composition (regions of shared type abundance) vs literature (STAGATE, GraphST, DSTG).
- G5: working CLI spot_deconv.py + one prospective lab nomination.

## Prospective lab nomination (locked)
A spatial transcriptomics core running Visium mouse lung sections (e.g. lung fibrosis consortiums)
with matched scRNA reference: apply frozen GNN + NNLS to their real sections, marker-concordance readout.

## Scoring discipline
sim_simulation.json (splits, seeds, GRF field params) committed before ANY metric is computed.
Thresholds never relax after seeing results; any erratum goes in a GATES_ADDENDUM file locked
before the outcomes it governs.
