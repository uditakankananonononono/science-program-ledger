# DOC-1-021 REPORT - Imputing Spatial Transcriptomics with a Diffusion Model
EXP-1, 2026-09-24. GATES.md locked 07:13 BEFORE any expression analysis; ADDENDUM C locked 07:16 before P1; ADDENDUM D locked 07:27 before P2. VERDICT: DOCUMENTED BOUNDARY (submitted for adjudication) - tiny CPU diffusion is not competitive with reference kNN at panel scale.

## Design
Leave-one-gene-out over the osmFISH 33-gene cortex panel (32 shared with the Zeisel reference; split committed pre-run: dev 17 / frozen 15), SpaGE paper protocol. Named published baseline: SpaGE kNN (reference transfer). Topic arm: tiny conditional DDPM (MLP denoiser, T=100, 3 epochs, 16-sample posterior mean) - the envelope-honest version of "diffusion model".

## Results (single scoring passes)
- SpaGE baseline: dev mean per-gene Spearman 0.6775, frozen 0.6975 - reproduces the published benchmark's strong showing on this pair.
- G1 reference-free DDPM (32 genes + coords): dev mean 0.205. FAIL vs locked +0.02 margin.
- P1 (locked: + SpaGE principal-vector conditioning, information-equalized): dev mean 0.272. FAIL.
- P2 (locked: coordinate-free ablation): dev mean 0.232. FAIL - and ABOVE the coordinate version (0.205): the DDPM's meager signal is gene-gene structure, NOT spatial coordinates. No frozen run (locked: only an arm passing G1 advances).
- G3 (descriptive, dev genes): SpaGE wins every single gene (advantage always negative); advantage vs Moran's I rho = +0.07 (null - the locked hypothesis that diffusion wins on locally-structured genes is unsupported), vs detection rate +0.26 (weak). Even on Rorb (Moran's I 0.65, the most spatially structured gene in the panel) SpaGE 0.884 vs DDPM 0.292.
- G4: impute_gene.py CLI (SpaGE method, honestly labeled) smoke PASS: Rorb Spearman 0.884 vs measured. Lab nomination: Theis lab (Helmholtz Munich).

## The boundary statement
At panel scale (33 genes, 4839 cells) a reference-free generative model of the spatial data has almost nothing to work with: the information SpaGE exploits is cross-dataset cell-identity transfer (1691 reference cells x shared markers), which kNN captures directly and a 2-layer DDPM trained on 4839 cells cannot. Coordinates do not rescue it (P2 > coordinate arm), and giving it the reference PVs (P1) recovers only a third of the gap. Generative spatial imputation needs scale - larger panels (MERFISH 100s of genes), more cells, and more compute than this envelope. This extends the program's small-model map (011-015 PLM rule, 020 transport rule) to generative models: tiny generative models lose to simple nearest-neighbor transfer when a reference dataset carries the signal.

## Honest limits
Only 3 training epochs / 16 posterior samples / 50 reverse steps (locked for compute); SpaGE reimplementation, not the author's code (faithful to the paper's algorithm; scores in the published range for this pair); osmFISH is the easiest spatial benchmark (big cells, clear types) - the gap likely widens on harder tissues; 1 of 33 panel genes absent from the reference (excluded from both arms).
