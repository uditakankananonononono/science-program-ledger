# DOC-2-056 Early Disease = Coordination Failure - UC colon mucosa (exp200/156)

**Outcome: documented boundary. The primary, Pivot 1 and Pivot 2 (a trained biomarker, the experimental angle) each failed at least one locked gate. Not counted.**

## Setup
Three public ulcerative colitis (UC) mucosal microarray cohorts: GSE87466 (discovery, 87 UC / 21 normal), GSE38713 (13 controls, 15 active, 8 remission, 7 non-involved) and GSE9452 (5 controls, 13 non-inflamed UC, 8 inflamed). 1,169 Reactome pathways.

## 1. Coordination hypothesis (primary + Pivot 1): fail
- The primary could not pass by design. With 200 permutations the p-value floor (0.005) sits above the BH threshold for 1,169 tests. I caught that arithmetic defect without inspecting the p-values, and reran with 2,000 permutations (Pivot 1).
- Pivot 1: 7 pathways at FDR < 0.10 (gate 20). **6 of 7 were coordination GAINS in UC, not losses.** Their direction replicated 6/6 in active UC in GSE38713 (p = 0.016). The set-level shift reached p = 0.010 in non-inflamed GSE38713 but not in GSE9452 (p = 0.37, only 5 controls).
- Finding: in this data, UC mucosa shows tighter co-regulation of a few pathways rather than a "coordination failure", and that shift persists in GSE38713 tissue that looks normal. The coordination-failure framing is not supported.

## 2. Trained cross-platform biomarker (Pivot 2, the experimental angle): fail on one gate
- L1 logistic model on within-sample gene ranks, trained only on GSE87466 (Affymetrix GPL13158) and applied frozen to the other platform (GPL570).
- Detecting UC in mucosa with no macroscopic inflammation: GSE38713 AUROC 0.78 (CI 0.57-0.94), GSE9452 AUROC 0.80 (CI 0.51-1.0). Both external gates pass.
- Failed gate: a single gene picked in training, **SLC6A14**, did as well or better (0.83 on GSE38713). The 19-gene model adds nothing over it here.
- Sub-groups (reported, not gated): remission mucosa is almost perfectly separable from controls (model 0.98; SLC6A14 alone 1.00, n = 8 vs 13). Non-involved mucosa from patients with active disease is near chance (0.55 / 0.63, n = 7 vs 13).

## What is useful
1. A molecular "scar" in UC tissue that was previously inflamed and is now in remission is strong and transfers across platforms. One gene (SLC6A14) captures it in these cohorts. Mucosa that was never involved looks like control tissue. That suggests the persistent signal marks tissue history, not a field defect across the whole colon.
2. Other selected genes include DUOX2, DEFA5, KLK10, HOXB13 and HOXD13, plus MEP1B lower in UC. These are candidates for a small targeted remission panel. The external cohorts are tiny (remission n = 8), so this is a hypothesis for a larger locked validation.
3. Methods note: permutation-based pathway FDR over ~1,000 pathways needs >= 2,000 permutations. This is a common silent failure mode.

## Limits
- Small validation groups: 5 controls in GSE9452 and 8 remission samples.
- Microarrays only.
- The remission and non-involved sub-analyses were not pre-specified as gates.
- No clinical claims.

## Reproduce
code/main.py (primary), code/pivot1.py, code/pivot2.py. GEO series matrices and annot files are listed in data/SHA256SUMS.
