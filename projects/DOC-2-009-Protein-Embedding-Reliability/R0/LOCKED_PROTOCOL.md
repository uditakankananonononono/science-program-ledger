# DOC-2-009 Protein Embedding Reliability Map - locked R0 protocol

**Lock time:** 2026-09-22 13:00 IST. **Status:** frozen before outcome analysis.

## Scientific claim under test
A protein's location in a sequence-representation space contains enough information to predict, for a previously unseen protein family, whether a fixed protein language model's zero-shot missense-effect scores will agree with DMS measurements. The output is a reliability map, not a new variant-effect predictor.

## Estimand
For target protein/assay i, let Y_i be ProteinGym's assay-level Spearman correlation between ESM2-650M zero-shot scores and experimental DMS_score. Let X_i be a representation derived only from the wild-type sequence, with no DMS values, assay labels, MSA statistics, taxonomy, or model scores. The primary estimand is the family-held-out predictive association between a reliability model r(X_i), fitted on all other family components, and Y_i. The operational estimates are out-of-fold Spearman(r,Y), R2 against held-out Y, and MAE reduction versus a training-fold-mean predictor.

## Data and cohort
- ProteinGym v1.3 substitutions benchmark reference table and assay-level Spearman benchmark, official repository, all assays with ESM2-650M result and usable sequence.
- InterPro annotations retrieved from UniProt by ProteinGym UniProt entry name.
- Unit: UniProt protein. If several assays map to one UniProt ID, Y is their unweighted mean. This prevents assay-rich proteins dominating.
- Strict family groups: make a graph linking proteins that share any InterPro accession; each connected component is indivisible. Unannotated proteins are singleton groups. All assays for a UniProt stay together.

## Representation and model
R0 deliberately uses a transparent sequence embedding to test identifiability before GPU work: length-normalized 1-mer frequencies (20), length-normalized 2-mer frequencies (400), log sequence length, Shannon entropy, aromatic fraction, charged fraction, hydrophobic fraction, glycine/proline fraction and cysteine fraction. No target-derived feature.

Within each training fold only: standardize features and fit ridge regression. Choose alpha from {0.1,1,10,100} by inner GroupKFold on training family components, minimizing MAE. Outer evaluation: deterministic GroupKFold with 5 folds, assigning whole InterPro connected components; if fewer than 5 viable groups, use leave-one-group-out. Fixed random seed 2009 wherever needed.

## Locked primary success gates (all must pass)
1. **Discrimination:** outer-family-held-out Spearman rho >= 0.35.
2. **Absolute generalization:** outer-family-held-out R2 >= 0.10.
3. **Practical gain:** MAE at least 10% lower than the training-fold-mean baseline.
4. **Coverage:** >=150 unique UniProt proteins with outcomes, >=120 with InterPro annotation, and >=25 independent family components; no protein/family leakage.

## Locked robustness gates (both must pass)
5. Protein-level bootstrap (10,000 resamples of frozen OOF predictions) lower 95% percentile bound for rho > 0.
6. Direction is preserved (rho > 0) separately in at least 3 of 4 strata with >=15 proteins: Human, other eukaryote, prokaryote, virus. This gate is declared not evaluable, hence R0 cannot pass, if fewer than three strata qualify.

## Interpretation locked in advance
- All primary and robustness gates pass: feasible; proceed to R1 with pretrained ESM embeddings and a temporally newer external DMS set.
- Any gate fails: negative R0. Do not tune gates/features after seeing results. Diagnose only; a new protocol/version is required for another test.
- This study supports selective-use calibration, not causal claims and not clinical validity.
