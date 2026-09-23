# PPD-BIOMARKERS — Postpartum-depression biomarker panel, discovered and FROZEN-verified
# GATES locked 2026-09-24 ~00:12 IST, before any model fitting or outcome inspection.
# Lane EXP-1. User-steered insert (main 23:57): "identifying and verifying biomarkers
# associated with certain illnesses - maybe postpartum depression."

## Data (public; GEO; URLs + SHA-256 in results/provenance.md)
- DISCOVERY: GSE45603 (Mehta-style prospective PPD cohort; Illumina HT-12 v4 microarray,
  whole blood; series matrix, 15,457 probes). Prospective subset: 3rd-trimester samples of
  women labeled by postpartum outcome: PPD (n~53 total cohort) vs euthymic (n~86 total);
  exact 3rd-trimester cross-tab counted at parse time and recorded. Excluded: "always
  depressed", "control" (non-pregnant), NA labels, other timepoints.
- EXTERNAL (frozen, touched ONLY after the panel is locked): GSE290313 (PRAM-style RNA-seq
  blood cohort, GPL24676). Prospective subset: pregnancy samples of women with depressive
  symptoms ONLY postpartum (postpartum-onset) vs Controls. Per-sample read counts from
  GSE290313_RAW.tar (75MB, 301 files), merged to a counts matrix.

## Preprocessing (frozen)
- Microarray: series-matrix values as distributed (submitter-normalized); collapse
  multi-probe genes by mean after mapping probe->symbol via the matrix's gene-symbol column.
- RNA-seq: CPM + log1p per sample.
- Cross-platform harmonization: gene-symbol intersection (uppercase), then per-cohort
  z-score per gene. No batch correction across cohorts (honest transport test).

## Model (frozen)
- Discovery-only feature selection: per-gene limma-style two-sample t on discovery,
  keep top 200 by |t| with p<0.05 (fallback: top 200 by |t| if fewer pass).
- Classifier: L2 logistic regression (C=1.0) on the 200-gene panel, trained on ALL
  discovery samples once the panel is selected; nested estimate via 5-fold CV repeated
  20x (frozen seeds) for the discovery-gate metric.
- Panel: the final 200 genes + coefficients = the biomarker panel (shipped as CSV +
  scoring CLI).

## Success gates
- G1 (discovery signal): repeated-CV AUROC >= 0.70 AND permutation p<=0.01 (1000
  label-shuffles, same pipeline inside each shuffle).
- G2 (PRIMARY - external verification): frozen panel + frozen logistic model applied
  ONCE to the external cohort's pregnancy samples: AUROC >= 0.65 AND bootstrap 95% CI
  lower bound > 0.5 (10k bootstraps).
- G2b (single-feature baseline gate): panel external AUROC must exceed the best SINGLE
  panel gene's external AUROC by >= 0.03 (panel must be more than its best gene).
- Honest-negative clause: if G2 fails, exactly ONE pre-registered pivot is allowed -
  sign-concordance test (fraction of panel genes whose discovery effect sign matches the
  external effect sign, binomial test vs 50%) - locked as GATES_v2 BEFORE it is run.
  If that also fails: documented boundary (cross-platform PPD signal does not transport
  from this discovery cohort), reported honestly.

## Reviewer questions (pre-registered)
- Label leakage? Discovery labels are postpartum outcomes attached to 3rd-trimester
  samples = prospective prediction, not concurrent diagnosis. External cohort same design.
- Small n? 3rd-trimester PPD-vs-euthymic n is small; that is why the external gate is
  primary and discovery CV is only a sanity gate.
- Platform shift? Deliberately NOT corrected: a biomarker panel that only works after
  batch correction is not a validated panel.
