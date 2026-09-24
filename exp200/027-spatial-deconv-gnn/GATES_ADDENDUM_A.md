# ADDENDUM A (2026-09-24 08:13): implementation errata on the locked simulation description

1. GRF implementation: GATES.md locked "latent Gaussian random field (length-scale 0.15)". The
   implementation uses an 8x8 coarse grid of standard normals with bilinear interpolation - a smooth
   regional field with effective length-scale ~1/8 of the unit square, not a literal parametric GRF
   at 0.15. Functionally equivalent purpose (regional spatial structure); sim_simulation.json
   (committed pre-scoring, with hashes) records the implementation as grf_grid: 8.
2. Region bands: first generation used 6 bands (only 6 of 10 types ever region-dominant), detected
   via proportion means and REGENERATED to 10 bands to match the locked "cycling the 10 types" spec.
   Regeneration happened BEFORE any metric was computed on the final artifacts; the 6-band artifacts
   were overwritten and never scored. sim_simulation.json hashes are of the final 10-band artifacts.
3. Timeline: artifacts frozen + spec committed (08:12) BEFORE NNLS baseline scoring (08:12). This
   addendum is locked before GNN training and before any G2/G3 adjudication. No gate, margin, seed,
   split, or arm is changed by this addendum. G1 already computed at 0.6856 (pass, no halt) and is
   unaffected.
