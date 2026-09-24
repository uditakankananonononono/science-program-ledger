# 37 - Nuclei segmentation: RF 3-class pixel classifier vs Otsu + watershed on BBBC039 (headline FAIL, narrow)

BBBC039 (U2OS Hoechst nuclei), official split 100/50/50. Both methods tuned on validation; test scored once. Gates locked before any segmentation (commit cae6527e).

| Gate | Result | Value (95% CI, 2000 paired bootstraps over 50 test images) |
|---|---|---|
| G1 mean F1@IoU0.5 RF - Otsu+WS >= 0.03 | FAIL | +0.024 (0.016, 0.033) |
| G2 mean F1@IoU0.75 RF - Otsu+WS > 0 | PASS | +0.030 (0.013, 0.045) |
| G3 RF >= Otsu+WS on >= 70% of images | PASS | 86% |

Test F1@0.5: Otsu+watershed 0.884, RF 0.909. F1@0.75: 0.811 vs 0.840.

Post-hoc pivot (Amendment 1, locked and pushed before scoring, commit 8a772d86): both validation choices sat at grid edges, so both grids were extended outward (validation only). Otsu stayed at min_distance 10 (larger was worse); RF moved to t=0.7. Test: F1@0.5 +0.026 (0.018, 0.034) - P1 FAIL against the unchanged 0.03 bar; F1@0.75 +0.034 (0.018, 0.050) - P2 PASS.

Takeaway: a classical random-forest 3-class pixel classifier is reliably better than a tuned Otsu + watershed pipeline (CI clearly above zero, better on 86% of images, larger gain at the stricter IoU), but the gain (+0.025 F1) is below the pre-declared 0.03 bar. The bar was not moved.

Caveats: one cell line and stain; deep models (U-Net, ~0.9+ in Caicedo et al. 2019 with different metric details) are stronger and out of scope; the Otsu pipeline is one standard variant.
