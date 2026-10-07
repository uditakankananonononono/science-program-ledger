# P2 robustness/boundary check (locked before any robustness compute)
Original result (commit 32fe41b): ASL beat TF-IDF+Ridge by RMSE 0.1702 (CI [0.0941,0.2473]) on the shipped test file. Questions here: (1) does it hold on fresh random re-splits of the pooled 4,143 reviews, (2) which ASL component carries it (stack vs sparsity), (3) boundary: how does it behave at small training sizes.
Data: same pooled UCI461 train+test (sha256 3500936f...).
Re-splits: 10 random 75/25 splits (RandomState seeds 101..110). Alpha grid {0.3,1,3,10} chosen by 3-fold CV (KFold shuffle seed 0) on each split's training part for every model.
Arms per split: B (concat TF-IDF+Ridge); ASL (per-field Ridge, top-2000 sparsity refit, NNLS stack as original); A1 = per-field Ridge + NNLS stack WITHOUT sparsity; A2 = concat Ridge WITH sparsity (top-2000 features by |coef| then refit). Metric: test RMSE per split.
Primary robustness verdict: ROBUST if mean (RMSE_B - RMSE_ASL) over the 10 splits >= 0.05, 95% bootstrap CI over splits (10000, seed 7) lower > 0, and ASL beats B on >= 8 of 10 splits. NOT ROBUST if CI upper < 0.05 or fewer than 6 of 10 splits. Otherwise MIXED. Ablation reported as mean RMSE per arm and paired differences.
Boundary: ASL vs B at training fractions 10%, 25%, 50% of the training part of split seed 101 only (one split, descriptive, no verdict).
Disclosure: splits ignore any drug/patient grouping (not available), reviews of the same drug may occur in both parts.
