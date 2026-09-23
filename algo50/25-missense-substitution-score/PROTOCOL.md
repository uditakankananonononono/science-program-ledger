# algo50/25 - How much does the amino-acid swap alone say about missense pathogenicity? BLOSUM62/PAM250 vs a ClinVar-learned substitution score

Status: LOCKED before any method was scored (UTC time + sha256 in results/lock.txt). Lane RES-1.

## Question
Substitution matrices built for protein alignment (BLOSUM62, Henikoff & Henikoff 1992; PAM250, Dayhoff 1978) are often used as a crude missense severity score. Does a substitution score learned directly from clinical labels, with whole genes held out, rank pathogenic missense variants better than these matrices?

## Data
ClinVar variant_summary.txt.gz (https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz; time and sha256 in data/). GRCh38 single-nucleotide missense (HGVS p.Xxx#Yyy), Pathogenic/Likely pathogenic (label 1) vs Benign/Likely benign (label 0), review status with assertion criteria (>= 1 star), deduplicated by VariationID. 60,482 P/LP vs 139,189 B/LB across 15,494 genes (counts checked before lock; no scoring done).

## Methods
- B62: score = -BLOSUM62(ref,alt) (Biopython matrix). PAM: -PAM250(ref,alt).
- M (learned): L2 logistic regression (C=1) on one-hot features for the (ref,alt) pair (380), ref (20) and alt (20). Uses nothing but the swap.
- Split: 5-fold GroupKFold by gene, seed 25 (gene order shuffled). Every gene's variants are scored by a model that never saw that gene.

## Metrics
Out-of-fold AUROC. 95% CIs by 2000 bootstrap resamples of genes, paired.

## Success gates (declared before scoring)
- G1: AUROC(M) - AUROC(B62) >= 0.03, CI lower bound > 0.
- G2: AUROC(M) - AUROC(PAM) >= 0.03, CI lower bound > 0.
- G3 (label-quality robustness): on the >= 2-star subset (multiple submitters no conflicts / expert panel / practice guideline), AUROC(M) - AUROC(B62) > 0 with CI lower bound > 0.
All reported pass or fail; one post-hoc pivot allowed, locked first.
