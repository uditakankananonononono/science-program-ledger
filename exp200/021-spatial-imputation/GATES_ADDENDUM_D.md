# ADDENDUM D - locked 2026-09-24 07:27 IST BEFORE P2 outcomes
P1 result (dev): PV-conditioned DDPM mean 0.272 vs SpaGE 0.6775: FAIL (second arm).
Locked tree: P2 coordinate-free ablation runs now. Same reference-free DDPM with (x,y) removed
from conditioning (genes-only input). Purpose: attribute what little signal the DDPM has to
coordinates vs gene-gene structure; this is diagnostic for the boundary statement, not a
rescue arm - P2 "passing" G1 margins remains the locked criterion for any G2 frozen run
(dev mean > SpaGE mean + 0.02). If no arm passes: documented boundary stands.
