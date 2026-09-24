# algo50/51 - Blood-brain barrier penetration: boosted ECFP counts vs linear fingerprints vs Tanimoto lookup

Lane RES-1. Protocol hashed and locked before any model ran (`results/lock.txt`).

## Bottom line
- G1 PASS: histogram boosting on count-ECFP4 + MACCS + 8 descriptors reaches scaffold-held-out AUROC **0.906** vs 0.844 for logistic on binary ECFP4 (+0.062 >= 0.02).
- G2 FAIL (honest negative): binary-ECFP logistic beats the 3-descriptor baseline (MolLogP/MolWt/TPSA) by only +0.017 (0.844 vs 0.826, needed +0.05). Under a real Murcko-scaffold split, three physicochemical numbers carry most of the linearly recoverable signal in BBBP. (Random-split literature numbers are not comparable - no random split is reported here on purpose.)
- G3 PASS: M1 beats the field's default Tanimoto 1-NN chemical lookup by +0.127 (0.779).
- G4 FAIL - and it was UNSATISFIABLE as written: precision is capped at 1.0, but the gate demanded 1.5 x base rate = 1.148 at base rate 0.765. Declared before results, evaluated honestly, reported as a mis-specified gate rather than silently rescaled. Post-hoc observation (NOT a gate): M1's top-decile precision is 0.985, a 1.29x enrichment - near the achievable ceiling given the base rate.

## Data
BBBP via the MoleculeNet/DeepChem S3 mirror (`BBBP.csv`). 2,039 compounds; 11 dropped on SMILES parse failure (counted); salts desalted by largest fragment. Base permeant rate 0.765. 1,021 Murcko scaffolds, greedy size-balanced 5-fold scaffold split (seed 0; folds 405-418 compounds, no scaffold crosses folds). Raw CSV not committed; `code/prep.py` re-downloads with sha256 provenance.

## Methods
Features via RDKit: B0 = MolLogP+MolWt+TPSA logistic (C=1.0); B1 = binary ECFP4 (radius 2, 2048 bits) logistic, C in {0.1,1,10} by inner scaffold-grouped CV; B2 = 1-NN Tanimoto on binary ECFP4; M1 = HistGradientBoosting (fixed hyperparameters: 300 iters, lr 0.06, 31 leaves, min leaf 20, L2 1.0) on count-ECFP4 + 167 MACCS keys + 8 descriptors. Pooled AUROC over out-of-fold predictions.

## Results
| Model | AUROC (scaffold-held-out) |
|---|---|
| B0 3-descriptor logistic | 0.826 |
| B2 Tanimoto 1-NN | 0.779 |
| B1 binary-ECFP logistic | 0.844 |
| M1 GBM count-ECFP+MACCS+desc | 0.906 |

Gate outcomes: G1 PASS, G2 FAIL, G3 PASS, G4 FAIL (mis-specified ceiling, documented). Figure: `results/fig_bbbp.png`. Full numbers: `results/results.json`, `results/predictions.csv`.

## Caveats
- G4's mis-specification is reported, not patched: no retrofitted triage gate was run after seeing the top-decile number.
- BBBP labels mix several measurement sources; scaffold splitting controls structure leakage but not assay noise.
- 1-NN Tanimoto with binary outcome has a coarse score distribution (mostly 0/1), which depresses its AUROC; the P2 k-NN ablation was not needed since G3 passed.
- Desalting by largest fragment drops counterion information; 11 unparseable SMILES dropped.

## Next steps
Repeat on BACE and ClinTox to test whether G2's "descriptors carry the linear signal" pattern generalizes beyond BBBP; distance-to-model calibration for the triage ranking; compare against a message-passing NN under the same scaffold split.

## Reproduce
`python3 code/prep.py && python3 code/run51.py && python3 code/figure.py` (needs rdkit, numpy, pandas, scikit-learn, matplotlib).
