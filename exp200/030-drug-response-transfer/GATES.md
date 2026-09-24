# GATES - DOC-1-030 (locked 2026-09-24 08:31 IST, BEFORE any model fitting or scoring)

## Claim
Bulk-to-single-cell TRANSFER LEARNING predicts cell-line drug sensitivity from single-cell
profiles, and domain alignment improves the transfer: a ridge model trained on CCLE bulk
expression with GDSCv2 potency labels and applied to single-cell pseudo-bulk beats the published
cognate-target biomarker, and per-gene distribution alignment of the single-cell features onto the
bulk feature space improves over naive (unadapted) application. Frozen validation on a second,
held-out drug of the same family.

## Data (eligibility verified BEFORE this lock)
- scRNA: Gambardella 2022 (Nat Commun 13:2394) Breast Cancer Single-Cell Atlas, 35,276 cells,
  32 lines; figshare 15022698 (matrix.mtx.gz 342MB + barcodes + features; line identity from
  barcode sample tags).
- Bulk expression: CSA benchmark (Zenodo 15258883) cancer_gene_expression.tsv (IMPROVE format,
  CCLE lines by improve_sample_id) - cross-checked against DepMap 23Q4.
- Potency labels: CSA y_data/response.tsv, source=GDSCv2, AUC; lapatinib = Drug_435,
  afatinib = Drug_520. Coverage VERIFIED: all 32 atlas lines map to ACH IDs (DepMap 23Q4
  Model.csv); lapatinib GDSCv2 = 25/32 lines, afatinib GDSCv1 = 25, GDSCv2 = 25, CTRPv2 = 20.
  DEV = lapatinib GDSCv2; FROZEN = afatinib GDSCv2 (held-out drug, same HER2 family; if afatinib
  GDSCv2 overlap < 20 lines after final manifest, Addendum switches FROZEN to GDSCv1 - locked
  contingency, not a post-hoc choice).
- Named published baseline: Gambardella 2022 cognate-target-expression biomarker (their Fig 3F /
  Supp Dataset 02): per-line ERBB2+EGFR expression vs potency. Published PCCs on this same cohort:
  lapatinib -0.395 (CTRPv2) / -0.423 (GDSC); afatinib -0.530 (CTRPv2) / -0.716 (GDSC).
  Sign convention: AUC higher = more resistant; gates use |Spearman|.

## Arms (bulk model: ridge, HVG-2000 log-TPM features selected on TRAINING lines only;
leave-one-atlas-line-out CV so no atlas line leaks into its own training set)
- BASELINE: sc pseudo-bulk mean log1p(ERBB2, EGFR) per line -> Spearman vs AUC (the published
  biomarker, recomputed on the locked label source).
- ARM A (no-adapt transfer): bulk-trained ridge applied directly to sc pseudo-bulk HVG features.
- ARM B (domain-aligned transfer): same model, but each sc pseudo-bulk gene feature is
  rank-normalized onto the bulk training feature's quantile distribution (per-gene quantile map)
  before prediction.
- P1 (pre-registered rescue if G2 fails): per-cell scoring - apply ARM B's model to each cell of
  the atlas, predicted-sensitive fraction per line as the line-level score; same gates.

## Metric
Spearman rho between predicted sensitivity score and GDSCv2 AUC across the labeled atlas lines
(LODO predictions for ARMs A/B; sign aligned so that higher score = more sensitive).

## Gates
- G1 (sanity halt): BASELINE |Spearman| >= 0.30 on lapatinib (published PCC -0.395/-0.423 on the
  same cohort). Else labels/features incoherent - document, stop.
- G2 (dev, lapatinib): ARM B rho >= BASELINE + 0.10 AND ARM B rho >= ARM A rho + 0.05.
- G3 (frozen, afatinib): ARM B rho >= BASELINE_frozen + 0.05 AND ARM B rho >= ARM B dev rho - 0.15.
- Failure tree: G2 fail -> P1, same gates; P1 fail or G3 fail -> DOCUMENTED BOUNDARY (no further arms).
- G4 (mechanism, runs regardless): MDAMB361 HER2+/- per-cell prediction (paper's wet-lab-validated
  case: HER2- subpopulation is afatinib-resistant); top bulk-model genes vs HER2-pathway biology;
  comparison of recomputed vs published baseline PCCs.
- G5: working CLI drep_predict.py + one prospective lab nomination.

## Prospective lab nomination (locked)
A breast-cancer functional-genomics unit running scRNA + drug screens on cell-line panels
(e.g. HER2-heterogeneity studies): apply the aligned transfer model with in-vitro AUC readout.

## Scoring discipline
Line manifest (atlas line -> ACH ID -> label availability) + file hashes committed before ANY
training. n ~= 25 lines per drug: disclosed; all arm comparisons are paired on the same lines.
Thresholds never relax after seeing results; errata in GATES_ADDENDUM files locked before the
outcomes they govern.
