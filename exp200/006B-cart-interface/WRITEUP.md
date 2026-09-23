# DOC-1-006B — CAR scFv-antigen interface prediction (B43-CD19 / PDB 6AL5)
**Verdict: DOCUMENTED BOUNDARY (candidate useful negative - adjudication requested).**

## Design (gates + 2 amendments locked before outcomes)
Train an epitope predictor on OTHER antibody-protein complexes (16 curated PDB
complexes, 3,295 antigen residues, 11.5% interface), validate FROZEN on the real
B43-CD19 CAR-target complex (PDB 6AL5; B43 = clinical anti-CD19 CAR scFv - FMC63
mislabel in v1 gates corrected by addendum). Features: published propensity scales
(Parker, Kyte-Doolittle, Karplus-Schulz, Emini, Chou-Fasman, window-5) + Atchley
factors + CA-burial. Truth: antigen residues within 5A of antibody atoms.

## Results
| gate | result | verdict |
|---|---|---|
| G1 v1 logistic | perm p=0.005 (obs 0.585 > all 200 nulls) but CV 0.585 < 0.70 | FAIL (magnitude) |
| G1 v2 GBM | perm p=0.005 (obs 0.671 > all 200 nulls, max 0.545) but CV 0.671 < 0.70 | FAIL (magnitude) |
| G2 (6AL5 frozen) | NOT RUN - G1 never cleared; 6AL5 stays untouched per discipline | - |

## Honest findings
1. Generic sequence+geometry features carry REAL epitope signal (permutation p=0.005
   in both arms - this is not noise), but the magnitude (0.671 GBM) sits below the
   locked 0.70 bar.
2. Field context (stated, not used to relax gates): published epitope predictors of
   this class score ~0.6-0.65 AUROC (BepiPred-2 literature); the locked bar was above
   the field's demonstrated level for sequence-scale features. Structural deep models
   (graph nets on full atoms) are the known step beyond - outside free compute here.
3. GroupKFold is deterministic (no shuffle), so the "20-rep" protocol collapses to one
   estimate; reported honestly, permutation testing carried the statistical weight.
4. early_stopping=True added to the GBM as a documented implementation detail (makes
   the model if anything weaker).

## Shipped
- code/featurize.py: PDB -> frozen per-residue features + 5A interface truth (reusable
  for any Ab-Ag complex; processes 25 complexes in ~2s).
- data/*.feat.json (16 training complexes + 6AL5), results/g1_metrics.json,
  g1_v2_metrics.json + g1_v2_cv.json, GATES.md + addendum + v2 (all SHA-256'd).
- No CLI, no nomination: nothing cleared the gates. 6AL5 remains pristine for a future
  structural-DL arm if the program approves one.
