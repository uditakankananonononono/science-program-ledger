# 199 RESULT - R-04 conditional re-stack audit of the VC-2 virtual-cell ensemble (mega27-02-virtual-cell @ bb6b9fb2)
Prereg: algo50/199-PREREG.md (text sha256 af3506bc09b6fe4fffffa9f60bfca376a783055c295101e3a726f94ad7bba1be; committed per commit timestamps before the run, which was started after commit; commit dates are author-set metadata), driver algo50/199-r04_run.py.md (sha256 5ea52e30...299b), runner algo50/199-r04_outer.sh.md. Run once. Environment: python 3.10.12 sklearn 1.7.2 numpy 1.26.4 pandas 2.3.3 | exit 0. Same-organisation audit, base layers not retrained.

## Label (fixed in prereg): AUROC arithmetic reproduced. Tally label: PARTIAL - conditional re-stack, with failed: A2.
Base scores are out-of-fold only for the base models; the stacker is trained on genes whose base scores came from models trained on overlapping genes; leakage unquantified. No script in the repo regenerates ensemble_oof.csv.

## Sub-results
- A1 PASS: recomputed AUROC of committed ensemble_oof.csv = 0.722482 (claimed 0.7225; window 0.0005). Join 1249 genes; labels agree with data/gerdes_labels.csv on 100.0% (0 mismatches, 0 missing; gerdes_labels.csv has 3,689 rows with duplicated bnumbers, 1 conflicting, handled as missing/disagreement).
- A2 FAIL: re-stack (LR C=0.5 balanced, 3-fold seed 7) AUROC = 0.7636, outside [0.7125, 0.7325]; it is +0.0411 above the claimed 0.7225. So the committed ensemble is NOT what this specified stacker produces from the committed base scores; the stacker that made it is undocumented.
- B PASS: 20 CV seeds, stack AUROC mean 0.7612, min 0.7482, all above strongest single layer fba_min (0.6658).
- C PASS: stack minus fba_min = +0.0979, 95% CI [0.0577, 0.1398] (2000 gene resamples, seed 7).
- D PASS: 200 label permutations: mean 0.4975, p95 0.5352 (<0.55), max 0.5652; real A2 0.7636 above max. D2 PASS: shuffled base columns mean 0.5027. Neither detects second-order stacking leakage.
- F (report only, the leakage-free comparison): stacking only the two label-free FBA layers gives AUROC 0.6451 (20-seed values 0.643-0.661), which is below the better single label-free layer fba_min (0.6658); delta -0.0211, 95% CI [-0.0531, 0.0126]. All of the ensemble's gain over fba_min therefore comes from the supervised GNN/CNN/k-mer layers; label-free stacking adds nothing.
- Flag: single fba_min AUROC 0.6658 vs claimed 0.666 (difference -0.0002, within the 0.001 flag threshold).

## Wording consequence
Safe: "the committed OOF ensemble file has AUROC 0.7225; a plain logistic-regression stack of the committed base scores gives about 0.76 with 3-fold CV (seed-stable, beats fba_min by +0.098, CI [0.058, 0.140]), but the supervised base layers share genes with the stacker's training set, leakage is unquantified, and the label-free layers alone do not beat fba_min." Not safe: calling the 0.7225 reproduced as a pipeline result.

## Verbatim
```
{
 "A1_n_join": 1249,
 "A1_oof_auroc": 0.7224821195627726,
 "A1_oof_file_label_agree_with_aligned": 1.0,
 "A1_gerdes_rows": 3689,
 "A1_gerdes_conflicting_dup_bnumbers": 1,
 "A1_missing_in_gerdes": 0,
 "A1_label_mismatches": 0,
 "A1_label_agree_frac": 1.0,
 "A2_auroc": 0.7636138725203545,
 "single_auroc": {
  "fba_min": 0.6657865143268409,
  "fba_rich": 0.6327830506949754,
  "gnn": 0.6595789663083083,
  "cnn": 0.6263146057307364,
  "kmer": 0.64090684179749
 },
 "strongest_single": "fba_min",
 "fba_min_single_auroc_minus_claimed_0.666": -0.0002134856731591528,
 "B_auroc_by_seed": [
  0.7610723764113175,
  0.7651612613017859,
  0.7580360757500788,
  0.7666996536368135,
  0.7681210921685934,
  0.765377176015474,
  0.7624533309342811,
  0.7627457154424002,
  0.7642256308758041,
  0.7656920516396024,
  0.7626467545319598,
  0.7541496109036929,
  0.7616526472043542,
  0.7619585263820792,
  0.7613917502586479,
  0.748198461607665,
  0.7624308398182716,
  0.758409428275831,
  0.7613872520354459,
  0.7522963429445368
 ],
 "B_mean": 0.7612052989069318,
 "B_min": 0.748198461607665,
 "B_all_exceed_best_single": true,
 "C_delta_mean": 0.09793292616461192,
 "C_ci95": [
  0.05773498973320012,
  0.13979271148074973
 ],
 "D_perm_mean": 0.4974903738023481,
 "D_perm_p95": 0.5352138905132472,
 "D_perm_max": 0.5651612613017858,
 "D_real_above_max": true,
 "D2_shuffled_cols_mean": 0.5026676262876163,
 "F_labelfree_stack_auroc_seed7": 0.6451374207188161,
 "F_labelfree_by_seed_1001_1020": [
  0.6521231613512664,
  0.6463541900949126,
  0.6521748909180873,
  0.6529418379740002,
  0.6607440061175835,
  0.6567293419099456,
  0.647463002114165,
  0.6494107327605596,
  0.6554450991858216,
  0.653411902298592,
  0.646718546174261,
  0.643635014169403,
  0.6433426296612839,
  0.6473910305429356,
  0.6451711573928298,
  0.6283500517295668,
  0.6488731950879403,
  0.6483041698529081,
  0.6471706176060457,
  0.6408078808870497
 ],
 "F_best_labelfree_single": "fba_min",
 "F_delta_vs_best_labelfree_single": {
  "mean": -0.02114568673960106,
  "ci95": [
   -0.053070943892305336,
   0.012566832163475927
  ]
 }
}
```
