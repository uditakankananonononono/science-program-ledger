# 27 - Coexpression mutual rank vs Pearson for pathway co-membership (NEGATIVE)

Question: does mutual rank (MR; Obayashi & Kinoshita 2009, used by ATTED-II/COXPRESdb) beat plain Pearson (PCC) at ranking Reactome co-pathway partners from GTEx v8 median tissue TPM (8124 genes, 54 tissues, 1038 leaf pathways of 10-200 genes)?

Gates were locked and pushed before scoring (commit 10fb4d6). Per-gene bootstrap, 2000 resamples, 95% CI.

| Gate | Result | Value (95% CI) |
|---|---|---|
| G1 AUROC MR - PCC >= 0.01, CI > 0 | FAIL | +0.0029 (0.0020, 0.0039) |
| G2 P@50 MR - PCC > 0, CI > 0 | FAIL | -0.0011 (-0.0017, -0.0006) |
| G3 AUROC MR - CLR > 0, CI > 0 | PASS | +0.0025 (0.0022, 0.0029) |

Absolute: AUROC PCC 0.609, Spearman 0.593, MR 0.612, CLR 0.609. P@50 PCC 0.075, MR 0.074.

Post-hoc pivot (Amendment 2, locked and pushed before scoring, commit ff960cf): shared nearest neighbours (top-50 by PCC). Failed both gates: AUROC +0.0007 (0.0004, 0.0011), P@50 -0.0023 (-0.0030, -0.0016).

Takeaway: on tissue-median profiles, every rank transform lands within 0.003 AUROC of PCC. MR gives a statistically real but tiny AUROC gain and loses at the top of the list. The signal ceiling here is the data (54 tissue medians), not the similarity measure. The MR benefit reported in the literature was on thousands of array samples; this test does not contradict that, it just doesn't reproduce it on GTEx medians.

Caveats: Reactome co-membership is a noisy truth set; pathways overlap; medians hide within-tissue variation. Amendment 1 was a memory fix made before any output.

Files: code/run.py, code/pivot.py, results/metrics_original.json, results/pivot_metrics.json, per-gene TSVs, PROTOCOL.md, results/lock.txt.
