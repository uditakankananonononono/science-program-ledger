# algo50/53 - BACE inhibition: does the BBBP descriptor pattern replicate, and does anything transfer across tasks?

Lane RES-1. Direct follow-up to algo50/51. Protocol hashed and locked before any model ran; Amendment 1 locked before its pivot ran (`results/lock.txt`).

## Bottom line
- The algo50/51 descriptor-dominance pattern does NOT generalize - and that is the payload. On BACE, fingerprints add +0.180 AUROC over the 3-descriptor baseline (G1 PASS: B1 0.839 vs B0 0.659), where on BBBP they added only +0.017. Bulk physicochemistry suffices for a bulk-property task (barrier penetration); a binding-pocket task (BACE-1) needs substructure. Two matched studies, same pipeline, opposite answers - exactly why the comparison was worth running.
- G2 PASS: boosted count-ECFP+MACCS+descriptors reach 0.880 vs 0.839 for binary-ECFP logistic (+0.042 >= 0.02).
- G3 FAIL, and worse than expected: a BBBP-trained model scores BACE compounds at AUROC 0.368 - BELOW chance. P1 FAIL too (descriptor-only transfer 0.378). Cross-task transfer is not merely weak here, it is anti-predictive: BBB-permeable-like molecules are anti-enriched for BACE activity (consistent with BACE inhibitors being larger/greasier than CNS-friendly averages). Negative transfer, documented with its sign.
- G4 PASS: pIC50 regression, GBM Spearman 0.795 vs ridge-on-8-descriptors 0.453 (+0.342 >= 0.05).

## Data
BACE (MoleculeNet/DeepChem S3, bace.csv): 1,513 compounds, 0 parse failures, base active rate 0.457, pIC50 for the regression arm. BBBP re-used for the transfer arm (same prep as algo50/51). Murcko-scaffold greedy 5-fold split (seed 0) on BACE; all BACE metrics scaffold-held-out pooled. Raw CSVs not committed; `code/prep.py` re-downloads with provenance.

## Methods
Identical feature stack and hyperparameters to algo50/51 (B0 3-descriptor logistic; B1 binary ECFP4 logistic with inner-CV C; M1 GBM on count-ECFP4+MACCS+8 descriptors, fixed). Transfer arm: M1 trained on ALL of BBBP (2,028 parsed compounds), scored on BACE, no refit. Regression arm: ridge on the 8 descriptors vs GBM on the full M1 features, both scaffold-held-out.

## Results
| Arm | Model | Score |
|---|---|---|
| BACE classification (AUROC) | B0 / B1 / M1 | 0.659 / 0.839 / 0.880 |
| BBBP->BACE transfer (AUROC) | M1 / P1 desc-only | 0.368 / 0.378 |
| pIC50 regression (Spearman) | ridge-8desc / GBM-full | 0.453 / 0.795 |

Gate outcomes: G1 PASS, G2 PASS, G3 FAIL, G4 PASS; P1 FAIL. Figure: `results/fig_bace.png`. Full numbers: `results/results.json`, `results/amend1.json`, `results/predictions.csv`.

## Caveats
- BACE Class comes from one assay program; scaffold split controls structure leakage, not assay noise.
- The transfer direction is one-way (BBBP->BACE); the reverse was not declared and not run.
- BACE molecules are larger on average (medicinal-chemistry set) than BBBP's, so part of the anti-transfer is a domain shift in bulk properties - which P1's descriptor-only test was designed to isolate, and it fails the same way.
- The BACE CSV also ships PaDEL-style descriptor columns; they were not used (features come from RDKit only, matching algo50/51).

## Next steps
Matched-size analysis: does the descriptor/fingerprint gap track with "bulk property vs binding pocket" across more MoleculeNet tasks (ClinTox, SIDER, HIV)? Quantify the anti-transfer sign across task pairs (a transferability matrix) as its own study.

## Reproduce
`python3 code/prep.py && python3 code/run53.py && python3 code/amend1.py && python3 code/figure.py` (needs rdkit, numpy, pandas, scikit-learn, matplotlib, scipy).
