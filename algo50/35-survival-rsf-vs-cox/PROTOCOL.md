# 35 - Random survival forest vs Cox proportional hazards on five public clinical cohorts

Locked before any model is fit.

Data (bundled with scikit-survival 0.25.0; original sources: GBSG2 German Breast Cancer Study Group; WHAS500 Worcester Heart Attack Study; FLCHAIN Dispenzieri et al. 2012 / Kyle et al.; ACTG 320 AIDS trial; Veterans' Administration lung cancer trial):
gbsg2 (n=686, 299 events), whas500 (500, 215), flchain (7874, 2169), aids (1151, 96), veterans (137, 128).
Preprocessing: one-hot categoricals (drop first); flchain: drop "chapter" (cause of death - outcome leakage), median-impute creatinine inside each training fold, follow-up time in days converted to 30-day units (ceil) for all models to keep forest memory within 2 GB. Features standardized inside each training fold for Cox.

Models:
- Baseline: Cox PH (Cox 1972), sksurv CoxPHSurvivalAnalysis, ridge alpha=1e-4 for numerical stability, ties="breslow".
- Method: Random survival forest (Ishwaran et al. 2008), 300 trees, min_samples_leaf=15, max_features="sqrt", seed 35.
- Secondary (reported, not gated): gradient-boosted Cox (GradientBoostingSurvivalAnalysis defaults, seed 35).
Evaluation: 5x repeated 5-fold stratified (by event) CV per dataset (seed 35); 3x5 for flchain (runtime). Harrell's C on the test fold; integrated Brier score (IBS) on a grid of 50 times between the 10th and 80th percentile of training event times, clipped to the test fold's follow-up range.

Gates (pooled = unweighted mean over the 5 datasets of per-dataset mean paired difference):
- G1 (headline): pooled delta C (RSF - Cox) >= 0.01, and 95% CI lower bound > 0. CI: 2000 bootstraps resampling fold-level paired differences within each dataset (seed 35). Fold differences are correlated, so per-dataset Nadeau-Bengio corrected CIs are also reported.
- G2: pooled delta IBS (Cox - RSF) > 0, CI lower bound > 0.
- G3: RSF mean C > Cox mean C in >= 4 of 5 datasets.
If G1 fails: one post-hoc pivot, locked and pushed before scoring.
Caveats declared: small cohorts; default (untuned) forest hyperparameters; Cox is linear with no interactions or splines.
