# DOC-1-060 locked protocol: neurodegeneration and sequence aggregation propensity

Locked 2026-09-21 20:56 IST before cohort retrieval, feature computation, or outcome modeling.

## Question
Among reviewed human proteins, do sequence-derived aggregation features and frozen protein-language-model representations distinguish proteins with curated neurodegenerative-disease involvement from length-matched proteins without any curated disease annotation?

This is a retrospective annotation benchmark. It does not predict individual risk, disease onset, or aggregation in vivo.

## Live sources
UniProt REST supplies reviewed human sequences and curated disease comments. RCSB PDB supplies structure-availability metadata for descriptive provenance only, not labels or features. The frozen representation is `facebook/esm2_t6_8M_UR50D`. Every HTTP response is retained and hashed in a request ledger.

## Cohort gate
1. Retrieve all reviewed Homo sapiens proteins from UniProt whose disease comments contain at least one prespecified phrase: Alzheimer, Parkinson, Huntington, amyotrophic lateral sclerosis, frontotemporal dementia, prion disease, spinocerebellar ataxia, neurodegeneration, or neurodegenerative. These are positive candidates.
2. Include canonical sequences 50-1,200 aa, composed only of the 20 standard amino acids, with explicit UniProt disease text containing one of those phrases.
3. Retrieve reviewed human proteins with no disease comment as negative candidates, under the same sequence gates.
4. Sort by accession. For each positive, select one unused negative minimizing absolute log-length difference; ties break lexicographically. Require length ratio 0.8-1.25. Preserve every exclusion and unmatched positive. At least 40 positive-negative pairs are required or the experiment stops as a feasibility failure.
5. Proteins, not isoforms, are units. Duplicate sequences are collapsed, retaining the lexicographically first accession. Exact sequence duplicates never cross classes.

## Features
A prespecified classical aggregation profile is computed in 7-residue windows. Each residue contributes Kyte-Doolittle hydrophobicity plus 0.5 for beta-branched/aromatic residues (V,I,F,Y,W) minus 1.0 for charged residues (D,E,K,R). The window mean is the propensity score. Protein summaries are maximum window score, fraction of windows >=2.0, mean of top 5% windows, sequence length, hydrophobic fraction, charged fraction, aromatic fraction, and low-complexity fraction (fraction of 12-residue windows with <=6 distinct amino acids). Thresholds are locked now; this is a comparative proxy, not an experimentally calibrated aggregation probability.

Frozen ESM-2 representations are mean and max pooled final-layer residue embeddings. No fine-tuning.

## Evaluation and leakage control
Three class-weighted logistic models are compared: (A) length/composition covariates only; (B) classical aggregation summaries plus covariates; (C) ESM representation reduced to <=32 training-only PCs plus covariates. Evaluation is repeated stratified 5-fold cross-validation (10 repeats, seed 60060). Exact duplicate sequences share a group; after deduplication each group is one protein. All scaling, PCA, and regularization selection occur inside training folds. C is chosen from {0.01,0.1,1,10} by 4-fold CV in training data.

Primary metric is out-of-fold AUROC, aggregated over all repeats. Secondary metrics are average precision and balanced accuracy at a threshold selected in training data by Youden's J. Uncertainty uses 10,000 paired bootstrap resamples over proteins (seed 60060). Primary success requires model B to improve AUROC over A by >=0.05 with a paired 95% bootstrap interval excluding zero. ESM is a secondary analysis and cannot rescue failure of the aggregation-feature gate.

Sanity control: permute labels within length quartiles and rerun model B once per repeat. Mean control AUROC must be 0.45-0.55 or the inference is invalidated. Preserve null and adverse outcomes.

## Claims boundary
A positive result means this explicit sequence proxy enriches curated neurodegeneration-associated proteins relative to disease-unannotated, length-matched reviewed human proteins. Disease annotation is incomplete, negatives are not proven healthy, and sequence association is not causal aggregation. Literature popularity and protein-family structure may influence annotations. No clinical claim is allowed.
