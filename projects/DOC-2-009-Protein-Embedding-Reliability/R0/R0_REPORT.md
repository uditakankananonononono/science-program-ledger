# DOC-2-009: Protein Embedding Reliability Map
## Locked R0 feasibility report

**Verdict: NO-GO under the locked protocol.** The transparent sequence embedding did not predict ESM2-650M DMS reliability across held-out InterPro family components. This is an informative negative result: basic composition and sequence-complexity coordinates are not an adequate reliability map, despite ample nominal coverage.

## Why this matters
Mutation-effect models are often reported as one global leaderboard score. A deployer instead needs to know when a score for a new protein family is likely to be trustworthy. DOC-2-009 tests that missing layer: predict model reliability from the wild-type protein before using any target-family DMS labels. The design separates reliability estimation from effect prediction and blocks family leakage.

## Frozen question and estimand
The protocol was SHA-256 locked before outcome analysis (`LOCKED_PROTOCOL.sha256`). For protein i, the outcome Y_i was the official ProteinGym assay-level Spearman correlation between ESM2-650M zero-shot mutation scores and measured DMS effects, averaged across assays for the same UniProt protein. The estimand was family-held-out association between a reliability score learned solely from the wild-type sequence and Y_i.

## Data and strict holdout
ProteinGym v1.3 official substitution reference and assay-level benchmark supplied 217 assays mapping to 186 unique proteins. UniProt returned InterPro annotations for 163 proteins. Proteins sharing any InterPro accession were joined into a connected component; each component stayed wholly inside one fold. Unannotated proteins were singletons. This yielded 102 indivisible components.

The pre-specified transparent embedding used 20 amino-acid frequencies, 400 dipeptide frequencies, log length, entropy, and fixed physicochemical fractions. Nested group cross-validation selected ridge alpha in training folds only; every outer fold selected alpha 100. No DMS result, taxonomy, assay class, MSA statistic, or model score entered the features.

## Locked gates and observed results

| Gate | Locked threshold | Result | Pass? |
|---|---:|---:|:---:|
| 1. Discrimination | held-out Spearman rho >= 0.35 | 0.120 | No |
| 2. Absolute generalization | held-out R2 >= 0.10 | -0.224 | No |
| 3. Practical gain | MAE >=10% below fold-mean baseline | 5.8% worse (0.180 vs 0.171) | No |
| 4. Coverage | >=150 proteins; >=120 annotated; >=25 components | 186; 163; 102 | Yes |
| 5. Uncertainty | bootstrap lower 95% bound for rho > 0 | 95% CI -0.038 to 0.275 | No |
| 6. Cross-taxon direction | rho >0 in >=3/4 eligible strata | not met | No |

Taxon diagnostics available from the first run were heterogeneous: Human n=81, rho=-0.042; other eukaryote n=34, rho=-0.175; Prokaryote n=43, rho=-0.040; Virus n=28, rho=0.536. The positive virus result is exploratory only and cannot rescue the failed locked study.

## Interpretation
R0 falsifies the narrow hypothesis that low-cost compositional sequence embeddings alone carry a grant-useful, family-general reliability signal for ESM2-650M. The negative R2 and worse-than-mean MAE rule out claiming that a weak rank correlation merely needs a different threshold. The virus-specific pattern could reflect biology, assay mix, or small-sample structure; it was not a locked subgroup hypothesis.

## Grant-defensible next experiment, not part of this result
R1 is justified only as a new locked study, not post-hoc tuning of R0. It should replace composition features with pretrained residue embeddings and explicit distance-to-training-manifold features; retain connected-component InterPro holdouts; add leave-one-taxon-out stress tests; and reserve a later ProteinGym release or newly published DMS assays as temporal external validation. A useful grant claim would be a calibrated abstention layer that improves decision quality by refusing predictions on low-reliability families, not a universal improvement in variant-effect prediction.

## Reproducibility package
- `LOCKED_PROTOCOL.md`: pre-outcome protocol and gates.
- `LOCKED_PROTOCOL.sha256`: lock digest.
- `run_r0.py`: complete analysis.
- `results.json`: machine-readable results.
- `oof_predictions.csv`: all out-of-fold predictions and family component labels.

## Sources
- ProteinGym official repository and v1.3 resource documentation: https://github.com/OATML-Markslab/ProteinGym
- ProteinGym official reference table: https://github.com/OATML-Markslab/ProteinGym/blob/main/reference_files/DMS_substitutions.csv
- ProteinGym official assay-level Spearman benchmark: https://github.com/OATML-Markslab/ProteinGym/blob/main/benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv
- UniProt REST API used for InterPro cross-references: https://rest.uniprot.org/
- ProteinGym v1.3 archive: https://zenodo.org/records/15293562
