# DOC-1-060: Sequence aggregation proxies do not add meaningful discrimination beyond composition

**Experiment:** Predicting neurodegeneration from protein aggregation propensities  
**Date:** 21 September 2026  
**Outcome:** Locked primary gate failed (honest negative)

## Abstract
We tested whether a prespecified sequence aggregation proxy distinguishes reviewed human proteins with curated neurodegenerative-disease involvement from length-matched reviewed human proteins without UniProt disease annotations. Live UniProt REST queries yielded 352 eligible positive proteins and 14,097 eligible negative candidates. Deterministic one-to-one length matching produced 352 pairs (704 proteins). In repeated nested cross-validation, the aggregation-feature model achieved mean fold AUROC 0.6278 versus 0.6236 for length/composition covariates. Using averaged out-of-fold predictions, the paired improvement was 0.0069 (protein bootstrap 95% CI -0.0117 to 0.0255), far below the locked +0.05 success threshold. The random-label control AUROC was 0.4975 and passed its gate. Therefore this simple sequence proxy did not add useful discrimination beyond composition in this benchmark. This is a negative result, not evidence that aggregation is unimportant in neurodegeneration.

## Locked question and gate
The protocol was SHA-256 locked before cohort retrieval, feature generation, or outcome modeling. The primary success rule required the aggregation-feature model to exceed the covariate model by at least 0.05 AUROC and for the paired bootstrap 95% interval to exclude zero. ESM-2 was explicitly secondary and could not rescue primary failure.

## Live data and cohort
UniProt REST was queried for reviewed Homo sapiens proteins, length 50-1,200 amino acids. Positive candidates required curated disease text matching a frozen list: Alzheimer, Parkinson, Huntington, amyotrophic lateral sclerosis, frontotemporal dementia, prion disease, spinocerebellar ataxia, neurodegeneration, or neurodegenerative. Negative candidates had no UniProt disease comment. Only canonical sequences containing the 20 standard amino acids were eligible; exact sequence duplicates were collapsed. Positives were sorted by accession and matched without replacement to the unused negative minimizing absolute log-length difference, with a required length ratio of 0.8-1.25.

All 352 gated positives obtained matches. The resulting class means were almost identical in length: 488.08 residues for positives and 488.09 for negatives. Raw query responses, exact query strings, timestamps, URLs, response hashes, cohort rows, disease text, and screening decisions are included.

## Features and evaluation
A seven-residue sliding window used a frozen score: Kyte-Doolittle hydrophobicity, +0.5 for beta-branched/aromatic residues (V, I, F, Y, W), and -1.0 for charged residues (D, E, K, R). Protein summaries were maximum score, fraction of windows >=2.0, and mean of the highest 5% of windows. Covariates were length, hydrophobic fraction, charged fraction, aromatic fraction, and low-complexity fraction.

Class-weighted logistic regression was evaluated with repeated stratified 5-fold cross-validation (10 repeats). Standardization and regularization selection were training-only. The primary comparison used predictions for every held-out protein, averaged over repeats. Uncertainty used 10,000 paired protein bootstrap resamples with seed 60060.

## Results

| Model | Mean fold AUROC | Mean fold AUPRC | Mean balanced accuracy |
|---|---:|---:|---:|
| Covariates only | 0.6236 | 0.6036 | 0.5980 |
| Aggregation summaries + covariates | 0.6278 | 0.6032 | 0.6128 |
| Labels permuted within length quartiles | 0.4975 | 0.5112 | 0.4952 |

Averaged out-of-fold AUROC was 0.6230 for covariates and 0.6299 for aggregation plus covariates. Difference: **0.0069**, 95% CI **-0.0117 to 0.0255**. The primary gate failed. The null control was within the required 0.45-0.55 AUROC band, so there was no indication of gross pipeline leakage.

The top-5%-window aggregation score differed only slightly before adjustment: positive mean 2.194 versus negative mean 2.136. That descriptive gap did not translate into material incremental prediction.

## ESM secondary analysis status
The protocol included frozen ESM-2 pooled embeddings as a secondary analysis. Two deterministic CPU-only implementations were attempted: per-protein pooling and length-sorted padded batching. Both exceeded the environment's 120-second execution ceiling before producing an output artifact. No partial or fabricated embedding result was used. `results/esm_secondary_status.json` preserves this failure. Because ESM was secondary and barred from rescuing the primary gate, the experiment's primary negative conclusion is complete and unchanged.

## Interpretation
Simple hydrophobic/charge-based aggregation summaries did not add practically meaningful classification over coarse composition and length. Several explanations remain open: in-vivo aggregation depends on concentration, cellular context, disorder, cleavage, post-translational modification, proteostasis, and specific structural states; the proxy may be too crude; and the label is curated disease involvement, not experimental aggregation.

## Negative evidence and limitations
- The locked effect-size gate failed decisively.
- The 95% interval includes zero and excludes the required +0.05 improvement.
- UniProt "no disease comment" is annotation absence, not proof of no disease relevance.
- Disease annotations favor heavily studied proteins, creating ascertainment bias.
- Related protein families may occur across folds; the benchmark estimates protein-level, not unseen-family, transfer.
- The positive class spans mechanistically diverse diseases and includes proteins involved in disease without necessarily being the aggregating species.
- The hand-specified propensity is a comparative sequence proxy, not an experimentally calibrated aggregation probability.
- The secondary ESM analysis could not be completed within the execution ceiling and is reported as a failure, not omitted silently.

## Conclusion
Under the frozen protocol, this explicit sequence aggregation proxy did not materially improve discrimination of curated neurodegeneration-associated proteins beyond length and composition. The result argues against treating generic hydrophobic/charge windows as a sufficient neurodegeneration predictor. It does not argue against protein aggregation biology.

## Reproduction map
- `scripts/fetch_uniprot.py`: exact live UniProt queries and hash ledger.
- `scripts/build_cohort_features.py`: gates, deterministic matching, and frozen features.
- `scripts/analyze_primary.py`: repeated nested cross-validation, null control, bootstrap inference.
- `scripts/embed_batched.py`: retained unsuccessful ESM implementation for transparent continuation.
- `data/raw/`: complete live UniProt TSV responses.
- `data/processed/cohort_features.csv`: exact cohort, sequences, labels, features, and positive disease comments.
- `results/`: screening log, fold metrics, predictions, primary inference, and ESM failure record.
