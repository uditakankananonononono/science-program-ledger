# PREREG unit 196 - REPLICATION R-01 (DRAFT for main review; no code from the target repo has been run)
## Target claim
Claim #1 of the strict-win list (research-portfolio-claim-ledger, Drive 14aVfnYV6WJOLVyvM78qP_ppd4wDrEIZV): "GCN AUC 0.831 vs FBA 0.697, delta +0.135 CI95 [0.114, 0.155]", repo uditakankananonononono/mega27-05-yeast-metabolic-twin @ commit 4b66f67, file results/cv_auc_delta.json (verified present; gcn mean_delta_auc 0.1346928, ci95 [0.1143784, 0.1549889]). Task: gene-held-out essentiality ranking, yeast-GEM, 1,143 model genes, 159 essential (data/raw/essentialGenes.tsv), FBA rule score = 1 - ko_ratio_complete, features = results/gene_features_partial.csv (11 structural/flux columns).
This is a re-execution replication by the same organisation, not an independent reimplementation. It tests reproducibility and seed-robustness of the claim, and one control. It is a replication, not a novel method.
## Materials (frozen)
Repo zip at commit 4b66f67 (codeload.github.com/uditakankananonononono/mega27-05-yeast-metabolic-twin/zip/4b66f67). Code unmodified; I call its own functions (yeasttwin.evaluate: make_folds, load_feature_table, load_graph, load_sequences-free path, score_logreg; yeasttwin.ml: train_gcn, auc_roc, normalized_adjacency; yeasttwin.labels: load_labels) from a driver script that is a copy of evaluate.run_cv with the CNN and ensemble branches removed (GCN seeds are BASE_SEED + 100*repeat + fold, independent of the CNN, so removal does not change GCN inputs). Packages: torch as installed, cobra 0.32.1 (not needed for scoring), scikit-learn 1.7.2. Hardware: 2-core CPU, free.
## Parts
A (exact-seed re-run): BASE_SEED 20260924, N_REPEATS 3, N_SPLITS 5, gcn_epochs 300, as in the repo. Per (repeat, fold) AUC for fba_rule and gcn; delta = gcn - fba. Mean delta; paired bootstrap 95% CI (2000 resamples of the 15 fold deltas, seed 7, same method as the repo).
B (fresh seeds): identical but BASE_SEED = 196196 (new folds and GCN seeds), 3 repeats.
C (feature-matched control, same folds as B): delta AUC = gcn - logreg (repo's score_logreg, same 11 features), same bootstrap.
## Pass/fail criteria (fixed now)
A passes iff |mean delta_A - 0.1347| <= 0.02 AND CI lower bound > 0.
B passes iff mean delta_B >= 0.10 AND CI lower bound > 0.
C passes ("GCN adds signal beyond a linear model on the same features") iff CI lower bound of the gcn-minus-logreg delta > 0.
Verdict on the claim as stated (GCN ranks essentials better than the FBA rule): REPLICATED iff A and B pass; PARTIAL iff exactly one passes; NOT REPLICATED iff neither passes. C is reported separately and decides only how the claim may be worded (a failing C means the gain is attributable to the extra features, not to graph learning).
## Exposure and disclosures
I read the repo README, results/cv_auc_delta.json and src/yeasttwin/evaluate.py before this prereg (needed to write the protocol). The expected numbers are therefore known. Nothing has been executed. Variance sources: torch CPU nondeterminism may move A by small amounts, which is why A has a +-0.02 tolerance. Whether any ignored 3rd-party dependency has changed since the original run cannot be controlled. Claims are limited to this one result (claim #1) on this one dataset; the other 9 strict wins are separate units.
## Outputs
Per-fold AUC table, deltas, CIs, verbatim logs, driver script, package versions, published as algo50/196-RESULT.md. A failure is published exactly like 192-195.
