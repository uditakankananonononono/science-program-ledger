# P2 preregistration (locked before any test-file outcome use)
Data: UCI461 zip sha256 3500936fb8473414b731c89d8c4395ab2dd65e2a99e9d79ee998328408a7ddcc. Train = drugLibTrain_raw.tsv (3107), Test = drugLibTest_raw.tsv (1036), the files as shipped. Test file used exactly once, after model selection on train.
Task: predict `rating` (1-10) from the three free-text fields only (benefitsReview, sideEffectsReview, commentsReview). Structured fields effectiveness/sideEffects/condition/urlDrugName are NOT used.
Baseline B: TF-IDF (word 1-2gram, min_df=2, sublinear_tf) on the concatenation of the 3 fields + Ridge; alpha chosen from {0.3,1,3,10} by 5-fold CV (KFold shuffle seed 0) on train.
New method ASL (aspect-sparse-lexicon stack): one TF-IDF+Ridge model per field (alpha by same CV), out-of-fold predictions (5-fold, seed 0) from the 3 field models -> nonnegative least squares combiner with intercept (scipy.optimize.nnls on centred data) fit on out-of-fold predictions; a lexicon-sparsity step keeps for each field only the top 2000 features by |coef| and refits (ridge, same alpha) before prediction. Final fit on all train.
Metric (primary): test RMSE, paired bootstrap over test reviews (10000, seed 7) of RMSE_B - RMSE_ASL. Secondary: Spearman, MAE.
WIN: RMSE_B-RMSE_ASL >= 0.05 and 95% CI lower > 0. NEGATIVE: CI upper < 0. Else NULL. Verbatim, no re-banding. Also report a constant-mean predictor RMSE as a floor.
Equivalence check: ASL with single-field concatenation and no sparsity must reproduce B exactly (asserted on train CV score).
