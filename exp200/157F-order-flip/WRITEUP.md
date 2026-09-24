# 157F - order-flip negative space (follow-up to 157): BOUNDARY (not counted), but the transport failure is fixed

Gates were locked before results (commit 1a579c7f).
Task: quiescent UC mucosa vs control. Trained on GSE87466 using 100 gene pairs that are stably ordered in normals (>= 95%) and flip most in UC.

| external | order-flip | k-TSP (Tan 2005) | 157 coupling score |
|---|---|---|---|
| GSE38713 (15 v 13) | 0.74 | 0.67 | 0.84 |
| GSE9452 (13 v 5) | 0.71 | 0.77 | 0.46 |
| GSE59071 NEW (23 inactive UC v 11) | 0.91 | 0.85 | - |
| mean (gated three) | 0.785 | 0.765 | - |
| GSE16879 healed responders (8 v 6, not gated) | 0.87 | 0.85 | - |

- G1 FAIL: GSE38713 is 0.74, just under 0.75, and the mean margin over k-TSP is +0.02 against the locked +0.03.
- G2 PASS: on the new cohort GSE59071 (a different platform) the score is 0.91 vs 0.85 for k-TSP.
- G3 FAIL: no Hallmark enrichment. Inflammatory p = 0.18; fatty-acid and OXPHOS show nothing.
- G4: scorer in code/run.py (flip()). The nominated two-gene test NPY<=PRRX1 fails to transport (0.51 / 0.57 / 0.73 / 0.38), so it is recorded as a negative nomination.

## What changed vs 157 (mechanism)
- Rewriting "negative space" as broken orderings instead of broken regressions removed the collapse. The worst external went from 0.46 to 0.71, and 157's range of 0.46-0.84 narrowed to 0.71-0.91. Order rules transport; residual rules do not (consistent with FINDINGS section 7).
- The advantage over k-TSP is small (+0.02). Many stable-order flips carry about the same information as k-TSP's 9 best pairs.
- The flipped pairs are mostly stromal and inflammatory (PRRX1, TGFB3, IL1RN, S100A12, CXCL8, ICAM1), not epithelial-metabolic. In "quiescent" UC mucosa the detectable residue looks like remodelling and low-grade inflammation, not metabolic loss. The 157 epithelial-metabolic reading (ACSF2) is not reproduced by order flips; ACSF2 appears in only one top pair.

## Data
GEO matrices for GSE87466, GSE38713, GSE9452, GSE59071 and GSE16879, plus GPL annotations and Hallmark sets. Checksums in SHA256SUMS. GPL570 cohorts GSE38713/GSE9452 are mapped with GPL96 as in 157.
