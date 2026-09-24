# algo50/53 - BACE inhibition: does the BBBP descriptor pattern replicate, and does anything transfer across tasks?

Lane RES-1. Direct follow-up to algo50/51.

## Question
algo50/51 found that under a Murcko-scaffold split, three physicochemical
descriptors carried most of BBBP's linearly recoverable signal. This study
asks: does that pattern replicate on a different target (BACE-1 inhibition),
does a model trained on one task (BBB penetration) transfer to another
(BACE), and does the boosted-vs-linear gap hold for the regression arm
(pIC50)?

## Data
BACE from MoleculeNet/DeepChem S3 (bace.csv): ~1,513 compounds with SMILES,
classification label (active/inactive at the assay threshold) and pIC50.
BBBP.csv re-used for the transfer arm (same prep as algo50/51). SMILES that
fail to parse are dropped and counted; largest-fragment desalting. Raw CSVs
not committed; sha256 + retrieval time in `data/`.

## Split
Same Murcko-scaffold greedy 5-fold scheme as algo50/51 (seed 0), applied
independently to BACE. All BACE metrics are scaffold-held-out pooled.

## Arms
- Classification (BACE label): B0 = 3-descriptor logistic; B1 = binary ECFP4
  logistic (C from inner scaffold CV); M1 = GBM on count-ECFP4+MACCS+8
  descriptors (fixed hyperparameters, same as algo50/51).
- Transfer: M1 trained on ALL of BBBP (same feature space), scored on every
  BACE compound, no refit. Comparator: B0 within-BACE.
- Regression (pIC50): ridge on the 8 descriptors vs GBM on the full M1
  feature set, scaffold-held-out, Spearman.

## Gates (declared before any model is run)
- G1 (pattern replication, linear side): AUROC(B1) >= AUROC(B0) + 0.05 on
  BACE. (algo50/51 predicts FAIL; the gate stands as declared either way.)
- G2: AUROC(M1) >= AUROC(B1) + 0.02 on BACE.
- G3 (cross-task transfer): AUROC(M1 BBBP->BACE) >= 0.60 (above noise, no
  refit) AND reported against within-BACE B0 for context.
- G4 (regression): Spearman(GBM, pIC50) >= Spearman(ridge-8desc, pIC50) + 0.05.

## Pivot plan (only if gates fail, pre-registered as amendments before results)
- P1: if G3 fails, per-task descriptor-only transfer (8 descriptors, logistic,
  trained on BBBP): gate P1 = AUROC >= 0.60.
- P2: if G4 fails, rank-based ablation: GBM on descriptors only: gate P2 =
  Spearman(GBM-desc) >= Spearman(ridge-desc) + 0.05.

## Honest-negatives policy
Every gate outcome is reported PASS/FAIL as declared. Failed gates and
mis-specifications stay in the README with their numbers.
