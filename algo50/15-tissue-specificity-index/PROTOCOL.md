# algo50/15 - Tissue-specificity indices: does collapsing redundant GTEx tissues make tau a better predictor of protein-level restriction?

Status: LOCKED before any index was scored against labels (UTC time + sha256 in results/lock.txt). Lane RES-1.

## Question
Tissue-specificity scores (tau, Gini, entropy, TSI, max z) are computed over whatever tissue panel is at hand. GTEx over-samples some organs (13 brain regions, 3 arteries, 2 adipose, 2 colon, 3 esophagus, 2 heart, 2 skin...). A brain-only gene looks "expressed in 13 tissues". Does computing tau on an organ-collapsed profile predict independent protein-level tissue restriction better than tau on the raw panel and better than the other common indices?

## Data
- RNA: GTEx v8 gene median TPM (54 tissues), https://storage.googleapis.com/adult-gtex/bulk-gex/v8/rna-seq/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct.gz. The 2 cultured cell types (fibroblasts, EBV lymphocytes) are dropped for all methods.
- Independent protein truth: Human Protein Atlas normal tissue immunohistochemistry (antibody staining, not RNA), https://www.proteinatlas.org/download/tsv/normal_ihc_data.tsv.zip. Times and sha256 in data/.

## Labels
Per gene and HPA tissue: detected if any cell type has Level Low/Medium/High with Reliability not "Uncertain". Genes need >= 30 assessed tissues and >= 1 detection. Restricted = detected in <= 3 tissues; Broad = detected in >= 20 tissues; genes in between are excluded. Genes joined by Ensembl ID; genes with max GTEx TPM < 1 excluded.

## Methods (all on log2(TPM+1))
- Raw panel (52 tissues): tau, Gini, TSI (max/sum), max z-score, entropy specificity (log2 N - Shannon entropy of the TPM distribution).
- tau_organ (proposed): collapse tissues sharing the GTEx prefix before " - " (e.g. all "Brain - *") to their median, then tau over organs.
- Higher score = more specific for all.

## Metrics
AUROC for Restricted vs Broad. Paired bootstrap, 2000 resamples of genes, 95% CI. Robustness: across 100 random draws of half the organs, Spearman correlation of tau_organ on the half vs on all organs.

## Success gates (declared before scoring)
- G1: AUROC(tau_organ) - AUROC(tau_raw) >= 0.01, CI lower bound > 0.
- G2: AUROC(tau_organ) > the best raw-panel index other than tau (by point AUROC), CI lower bound > 0.
- G3: mean half-panel Spearman for tau_organ >= 0.80.
All results reported pass or fail; one post-hoc pivot allowed, locked before scoring.
