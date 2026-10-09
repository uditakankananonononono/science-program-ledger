# PREREG unit 194 (locked before any model is fitted)
## Question
On the Ames mutagenicity benchmark with its official scaffold-split test set, does a scaffold-group-bootstrap random forest generalise to unseen scaffolds better than a standard random forest on the same features?
## Benchmark (verified reachable and loadable just now)
TDC ADMET benchmark group, task AMES (Hansen et al. 2009 data via Therapeutics Data Commons, PyTDC 1.1.15, admet_group.get('AMES')): train_val 5,821 compounds, official scaffold-split test 1,457 compounds (7,278 total). Metric = AUROC (the TDC metric for AMES). Official TDC protocol: 5 seeds (1-5) of get_train_valid_split(default scaffold) on train_val; test fixed.
Disclosure: while checking the data loads I printed one scalar from the TEST labels (positive rate 0.597 vs 0.533 in train_val). No model was fit, no other test statistic seen. Test compounds are otherwise unopened.
## Features (identical for both arms)
RDKit Morgan fingerprint radius 2, 2048 bits, binary; invalid SMILES dropped (count reported).
## Baseline B (named): sklearn RandomForestClassifier, 500 trees, Morgan2/2048 bits. Tuned on VALID only over a 4-cell grid: max_features in {sqrt, 0.2} x min_samples_leaf in {1, 2}.
## Candidate C: scaffold-group-bootstrap random forest. Same hyperparameter grid and tree count. Each tree is trained on a bootstrap that resamples Bemis-Murcko SCAFFOLD GROUPS (RDKit MurckoScaffoldSmiles, acyclic compounds = one group) with replacement and includes all compounds of each sampled group; each tree is a DecisionTreeClassifier with the chosen max_features/min_samples_leaf; prediction = mean of tree probabilities. Rationale: scaffold-split test sets are scaffold-novel; compound-level bootstrap leaves every tree seeing every scaffold, group-level bootstrap decorrelates trees across scaffolds.
## Protocol
For each of seeds 1-5: TDC train/valid split of train_val (scaffold), grid chosen per arm on valid AUROC, then refit on the seed's train only (not train+valid) and scored ONCE on the fixed test. Result per arm = mean test AUROC over the 5 seeds. Seeds also fix model random_state.
## Gates (DEV only, TEST sealed)
D0: B mean VALID AUROC >= 0.75 (headroom/pipeline sanity). D1: C mean VALID AUROC - B mean VALID AUROC >= +0.005, else DROP with TEST sealed. (VALID is scaffold-split inside train_val, so it is a fair OOD proxy.)
## TEST rule (fixed before any run)
WIN iff (mean over seeds) C - B test AUROC >= +0.010 AND paired scaffold-cluster bootstrap 95% CI (2000 resamples of test scaffold groups, seed 194, using the 5-seed mean predictions) excludes 0. NULL if the difference CI includes 0; LOSS if C < B with CI excluding 0. Report also AUROC per seed and AUPRC.
## Disclosures
Group-bootstrap/bagging-by-group ideas exist in the ML literature (group-aware ensembling); this is an incremental application test, not a new method class. Hansen data are a curated public set; label noise is documented. One benchmark only: no claim beyond AMES.
