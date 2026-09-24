# ADDENDUM C - locked 2026-09-24 07:16 IST BEFORE P1 outcomes
G1 result (dev, 17 genes): reference-free DDPM mean Spearman 0.205 vs SpaGE 0.6775 (margin -0.47):
FAIL decisively. Locked tree: P1 executes now.
P1 form (locked): same DDPM architecture/training/inference, conditioning extended with the
spatial cell's 30 SpaGE principal-vector coordinates (reference PCA over shared genes, same
PCA as the baseline - information equalization, no leakage of the held-out gene: PVs are
computed from the 32 other genes only). Margins unchanged: P1 passes G1' iff dev mean >
SpaGE mean + 0.02. If P1 fails -> P2 coordinate-free ablation runs next wake; if no arm
passes -> documented boundary (generative imputation needs scale this envelope lacks).
Implementation errata recorded: torch.no_grad fix (OOM), torch threads capped at 2.
