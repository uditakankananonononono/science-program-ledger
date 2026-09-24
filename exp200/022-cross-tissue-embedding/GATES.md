# GATES (LOCKED 2026-09-24 07:32, BEFORE any outcomes) - DOC-1-022: A Unified Cell Embedding for Cross-Tissue Integration

## Claim tested
Can ONE lightweight, batch-blind embedding (a single small autoencoder trained once across tissues) integrate
cells across tissues well enough to transfer cell-type labels at named-baseline level - i.e., is a "unified
embedding" feasible without per-dataset iterative correction (Harmony) or foundation-scale pretraining?

## Data (public, frozen at download)
- Tabula Muris FACS subset (Smart-seq2), figshare article 5715040 (Schaum et al 2018, Nature 562:367).
  Tissues: Pancreas, Liver, Spleen, Lung (mouse). Raw-count CSVs range-extracted from FACS.zip; labels from
  annotations_FACS.csv (cell_ontology_class). Hashes + member list in PROVENANCE.md.
- Cap 3000 cells/tissue (seed 7 subsample). Gene space: genes shared by all 4 tissues, log1p, top-2000 HVG
  computed on the THREE DEV TISSUES ONLY.

## Splits (committed pre-run to results/split.json)
- DEV tissues: Liver, Spleen, Pancreas - everything fitted on these only (HVG, scaler, PCA, Harmony, AE).
- FROZEN tissue: Lung - single final run, no iteration.
- Shared label set: cell_ontology_class values present in >=2 of the 4 tissues with >=30 cells each; the exact
  list is committed to results/class_list.json BEFORE any model is scored. Only these labels are scored.

## Protocol
Cross-tissue kNN (k=5, cosine) leave-one-tissue-out label transfer on the DEV tissues: fit kNN on the other
two tissues' embeddings, score held-out tissue's shared-label cells. Metric: mean accuracy across held-out
tissues (macro per-class accuracy also reported).

## Gates (ISEF-aligned)
- G1 (named published baseline): Harmony-on-PCA (50 PCs, harmonypy; Korsunsky et al 2019 Nat Methods 16:1289;
  top performer in Luecken et al 2022 Nat Methods 19:41). Dev mean accuracy recorded as THE baseline.
  Sanity halt: if Harmony dev < 0.30, treat as data problem, document, stop.
- G2 (topic arm): unified embedding = symmetric MLP autoencoder 2000-512-128-512-2000 (GELU), 128-d
  bottleneck is "the unified embedding", batch-blind, Adam 1e-3, <=15 epochs, dev tissues only. Same transfer
  protocol. PASS: dev mean accuracy >= Harmony dev - 0.03 (match-or-beat named baseline within locked margin).
- G3 (frozen external validation): one run with frozen Lung as target; winners refit per protocol. PASS:
  winner frozen accuracy >= its dev - 0.05 AND winner frozen >= Harmony frozen - 0.03. If Harmony won G2,
  G3 validates the baseline and the topic arm's loss stands (boundary).
- G4 (biological interpretation): per-class transfer map (immune/endothelial/epithelial shared classes vs
  literature markers: Ptprc/CD45, Pecam1/CD31, Epcam, collagen genes); do immune classes transfer best across
  tissues (conserved identity)? Silhouette-by-celltype vs silhouette-by-tissue on a 4000-cell subsample.
- G5 (tool + nomination): embed_cells.py CLI (counts CSV -> 128-d embedding + transferred labels, honest
  about which arm), smoke-tested on a held-out chunk. Lab nomination: Satija lab (NYGC, integration).

## Pre-registered failure tree
- G2 FAIL -> P1: supervised-contrastive fine-tune of the bottleneck (same-class cross-tissue positive pairs,
  temperature 0.1, 5 epochs), re-evaluate G2 at the SAME margin -> FAIL again -> DOCUMENTED BOUNDARY:
  batch-blind lightweight unified embedding cannot match iterative per-dataset correction (Harmony) for
  cross-tissue label transfer at this scale; unified-embedding claims require foundation-scale pretraining.
  P1 is defined NOW; no other pivots; thresholds never relax after outcomes.

## Constraints
Real public data only; sources + hashes in PROVENANCE.md; 2CPU/1.9GB envelope (float32, subsample,
torch.set_num_threads(2), no_grad); no money; no sending as the user.
