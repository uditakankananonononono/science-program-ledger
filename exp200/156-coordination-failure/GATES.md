# DOC-2-056 Early Disease = Coordination Failure - locked gates (23:17 IST, before any expression data download)

## Sandbox-fit slice
Ulcerative colitis (UC) colon mucosa, public microarrays (GEO series matrices): discovery GSE87466 (GPL13158, UC vs normal), replication GSE38713 (GPL570, active UC / non-active UC / non-IBD controls), second "subtle disease" cohort GSE9452 (GPL570, UC mucosa without macroscopic inflammation vs controls). Pathways: Reactome GMT (current), size 15-100 genes after mapping. Probes collapsed to one per gene (highest mean).

## Metric
Coordination of a pathway in a group = mean pairwise Pearson r among its genes. Delta = cases - controls. Permutation null: 200 label shuffles within the cohort; empirical two-sided p per pathway; Benjamini-Hochberg FDR.

## Gates
G1 (discovery) >= 20 pathways with coordination change at FDR < 0.10 in GSE87466.
G2 (replication) in GSE38713 active UC vs controls, >= 70% of the G1 pathways change in the same direction (binomial p < 0.01).
G3 (early / subtle disease - the actual claim) in the non-inflamed groups (GSE38713 non-active UC vs controls AND GSE9452 non-inflamed UC vs controls), the mean Delta over the G1 pathway set has the same sign as discovery with set-level permutation p < 0.05, in BOTH cohorts.
Reported, not gated: the same analysis for mean expression shift (mean |t| of member genes), to test whether coordination change exceeds expression change in subtle disease.
Group labels are parsed from GEO sample characteristics; the parsed group sizes are recorded as Amendment A before any expression value is read.
Failure policy: negative preserved; pivots appended with new locked gates.

## Amendment A (23:18, labels parsed, no expression value read)
GSE87466: 21 Normal vs 87 UC. GSE38713: 13 controls; active involved 15 (G2 cases); non-inflamed = remission involved 8 + active non-involved 7 = 15 (G3 cases; subgroups reported separately). GSE9452: 5 controls; non-inflamed UC 13 (G3 cases); inflamed 8 (reported). Warning recorded in advance: 5 controls give very noisy correlation estimates, so GSE9452 is a weak test.
Probe mapping: GPL13158 / GPL570 GEO annot files (Gene symbol column); probes with multiple symbols dropped.

## Primary result (23:18) - G1 FAIL, preserved, with a design defect identified
0 of 1,169 pathways at FDR < 0.10. Defect (arithmetic, independent of the data): with 200 permutations the smallest p is 1/201 = 0.005. BH at FDR 0.10 over 1,169 tests needs p <= 0.0017 for 20 hits, so G1 could not pass whatever the data. The p-value distribution was NOT inspected before this pivot.

## Pivot 1 (locked 23:19): same metric, same gates G1-G3, 2,000 permutations for the discovery cohort (p floor 0.0005). Replication set tests keep 200 permutations (set-level p, no multiple testing). Everything else unchanged.

## Pivot 1 result (23:43) - FAIL, preserved
G1: 7 pathways at FDR < 0.10 (< 20, fail); 6/7 are coordination GAINS in UC, not losses. G2: 6/6 of the G1 pathways that could be mapped went the same direction in GSE38713 active UC (binomial p = 0.016; set p = 0.040). G3: GSE38713 non-inflamed set p = 0.010 (pass), GSE9452 non-inflamed set p = 0.37 (fail; 5 controls). G3 fails because it requires both cohorts. The "coordination failure" hypothesis is not supported: the replicated signal is coordination gain.

## Pivot 2 (locked 23:46, before computation; experimental re-angle per user steering relayed by parent): a trained cross-platform biomarker for UC mucosa that looks normal
Train: GSE87466 (GPL13158) UC vs Normal. Features: genes shared by GPL13158 and GPL570, converted to within-sample ranks (platform-robust), top 2,000 by variance in the training set. Model: L1 logistic regression, C chosen by 5-fold CV inside the training set only. Frozen, then applied without refitting to:
 - E1 GSE38713 non-inflamed UC (remission + non-involved, n = 15) vs controls (n = 13)
 - E2 GSE9452 non-inflamed UC (n = 13) vs controls (n = 5)
P2-G1 E1 AUROC >= 0.75, and the bootstrap 95% CI lower bound > 0.5.
P2-G2 E2 AUROC >= 0.70.
P2-G3 The trained model beats a 1-gene baseline chosen in training (the single gene with the largest training |t|) on E1 AUROC by >= 0.05.
Reported: AUROC on the inflamed groups (sanity check), and the selected genes.

## Pivot 2 result (23:46) - FAIL on P2-G3, preserved
E1 AUROC 0.779 (CI 0.571-0.941) PASS; E2 0.800 (CI 0.511-1.0) PASS; P2-G3 FAIL: the 1-gene baseline (SLC6A14, picked in training) scored 0.826 on E1, above the 19-gene model. Sub-groups (reported only, not gated): remission mucosa 0.981 (model) / 1.00 (SLC6A14); non-involved mucosa 0.549 / 0.626.
Closed as a documented boundary after the primary and two pivots (the second was the required experimental angle).
