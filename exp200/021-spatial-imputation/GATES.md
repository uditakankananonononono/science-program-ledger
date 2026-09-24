# DOC-1-021 GATES - locked 2026-09-24 07:13 IST BEFORE any expression analysis
Topic: Imputing Spatial Transcriptomics with a Diffusion Model.
Question: can a tiny CPU-trainable conditional diffusion model of the SPATIAL data itself beat
reference-transfer imputation (SpaGE, named published baseline) at panel scale?

## Data (locked; downloaded from Zenodo 10.5281/zenodo.3967291 via range extraction, SpaGE paper benchmark)
- Spatial: osmFISH mouse somatosensory cortex loom (osmFISH_SScortex_mouse_all_cells.loom,
  1,122,355 bytes; 33 genes x 6471 cells with X/Y coords, Region, Valid flags; Codeluppi et al.,
  Nat Methods 2018). Cells: Valid==1. Preprocessing (locked): per-cell library-size normalize to
  1e4, log1p - standard scanpy-style, applied to both arms.
- Reference (SpaGE arm only): Zeisel cortex scRNA (RNA_Cortex_scvi.csv, 135,555,705 bytes,
  cells x 19,972 genes; Zeisel et al., Science 2015), same normalization.
- Checksums of raw files recorded in PROVENANCE.md.

## Arms (locked)
A) SpaGE kNN baseline (Abdelaal et al., NAR 2020;48(18):e107 - named published baseline):
   30 principal vectors from the scRNA reference over shared genes, spatial cells projected,
   kNN k=50 cosine, impute = distance-weighted mean of reference neighbors' target expression.
B) Tiny conditional DDPM (the topic's method, envelope-honest): per held-out gene g, MLP denoiser
   (2 hidden x 256, SiLU) predicting noise; input = other 32 genes (normalized) + (x,y) coords
   scaled to [-1,1] + sinusoidal t embedding; T=100 train timesteps, linear beta schedule
   1e-4..0.02, 3 epochs Adam 1e-3 batch 256; inference: 16 posterior samples/cell, 50 reverse
   steps, average. Reference-free by design (information asymmetry documented; P1 equalizes).

## Benchmark protocol (locked)
Leave-one-gene-out over the 33-gene panel (SpaGE paper protocol). Gene split: seed-7 random,
dev = 17 genes, frozen = 16 genes (list committed with code before any model run).
Metric: per-gene Spearman across cells (imputed mean vs measured); set score = mean over genes.

## Gates
G1 (dev, 17 genes): diffusion mean Spearman > SpaGE mean + 0.02. Else document loss.
G2 (frozen, 16 genes; methods transported, identical protocol, single scoring pass):
   diffusion mean >= SpaGE frozen mean + 0.00 AND diffusion mean >= 0.30 absolute.
G3 (mechanism): per-gene advantage (diffusion - SpaGE) vs gene spatial structure (Moran's I on
   the x,y grid) and detection rate. Locked hypothesis: diffusion wins on locally-structured
   genes (coords informative), SpaGE wins on cell-type markers (reference identity informative).
   Report Spearman(advantage, Moran's I) and sign vs hypothesis.
G4: impute_gene.py CLI (gene -> imputed map + Spearman vs measured) smoke test + prospective
   lab nomination (Theis lab, Helmholtz Munich - spatial + generative modeling).

## Failure tree (locked)
G1 fail -> P1: diffusion conditioned on scRNA principal vectors as well (equalize information).
P2: coordinate-free diffusion ablation. If no diffusion arm beats SpaGE by the locked margin ->
documented boundary: tiny CPU diffusion is not competitive with reference kNN at panel scale -
generative imputation needs scale/compute this envelope lacks. Thresholds never relax after outcomes.
