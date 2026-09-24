# DOC-1-021 PROVENANCE
- Zenodo record 10.5281/zenodo.3967291 (SpaGE paper benchmark datasets, single 1,173,368,797-byte zip). Members extracted via HTTP range requests (central-directory parse + per-member deflate), 2026-09-24: osmFISH_SScortex_mouse_all_cells.loom (1,122,355 bytes), osmFISH_Cortex_scvi.csv (260,169 bytes), RNA_Cortex_scvi.csv (135,555,705 bytes). Raw files gitignored in results/local/; code/prep_data.py regenerates matrices.
- Spatial: osmFISH mouse somatosensory cortex, Codeluppi et al., Nat Methods 2018;15:932 (33 genes x 6471 cells; Valid==1 -> 4839 cells; library-size 1e4 + log1p).
- Reference: Zeisel et al., Science 2015;347:1138 cortex scRNA (1691 cells x 32 shared genes).
- Named baseline: SpaGE (Abdelaal et al., NAR 2020;48(18):e107), faithful lightweight reimplementation (30 PVs, kNN k=50 cosine, distance-weighted).
- Gene split seed 7 committed in results/gene_split.json BEFORE any model run: dev 17 / frozen 15 of 32 shared genes.
- torch 2.14.0+cpu, sklearn, numpy/scipy. No money spent; all sources free public.
