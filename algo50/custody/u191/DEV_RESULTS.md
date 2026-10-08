# Unit 191 pre-lock DEV window results

**Locked design references**
- Preregistration SHA-256: `32b6093dc97268a769b204d3559d8581bac93cd7b3c2808fea69ca21ba4af0b1`
- Runner SHA-256: `c27387b43e9d948dd62a87e0964b7bc3a6824f316fead27f09be75129fceae29`
- Split manifest SHA-256: `fcc31bad5de5057fcd34cb01dd0034401c61e2e5bee7a7627a98585279a07413`
- DEV n=53,636; positive=8,072; negative=45,564. TEST was not read.

## DEV headroom and comparator lock

| Model | ROC AUC | PR AUC | Brier | Sensitivity @0.5 | Specificity @0.5 | Precision @0.5 |
|---|---:|---:|---:|---:|---:|---:|
| Sparse additive logistic candidate | 0.7109443537 | 0.2810819859 | 0.1189231080 | 0.0084241824 | 0.9980686507 | 0.4358974359 |
| LightGBM | 0.7322285852 | 0.3064821643 | 0.1166563219 | 0.0079286422 | 0.9984856466 | 0.4812030075 |
| Demographic LR | 0.6396590208 | 0.2125669005 | 0.1239228960 | 0 | 1 | null |

Best DEV comparator locked as LightGBM (epsilon 0.001 tie rule). Candidate minus comparator AUC = -0.0212842315; +0.03 win = false. Best-comparator headroom to 1.0 = 0.2677714148. No-skill and near-ceiling drop gates both false; proceed to final evaluation.

## DEV label-shuffle smoke

Single deterministic permutation, seed 42; pooled OOF predictions from five patient-grouped folds. AUC values shown against shuffled labels / original labels:
- Candidate: 0.4978159648 / 0.5151264609
- LightGBM: 0.4992575802 / 0.5155623655
- Demographic LR: 0.4997314574 / 0.4870280006

The shuffled-label AUCs are near 0.50. This is a leakage smoke, not an inferential permutation test.

## Convergence warnings

Prespecified settings were unchanged. Candidate original-label OOF: folds 0, 1, 2, and 4 each had `ConvergenceWarning: The max_iter was reached which means the coef_ did not converge`; fold 3 had no warning. Candidate permutation OOF: all five folds had the same warning. LightGBM and demographic LR: no convergence warnings in any original or permutation fold. Warnings were captured in the atomic per-fold outputs; no reruns/settings changes were made.

Detailed atomic stage JSONs: `/tmp/unit191/prelock_stages/`; DEV window aggregation: `/tmp/unit191/prelock_stages/headroom_gate.json` and `/tmp/unit191/prelock_stages/permutation_aggregation.json`.
