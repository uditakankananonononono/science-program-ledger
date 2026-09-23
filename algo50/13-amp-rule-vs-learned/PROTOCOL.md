# algo50/13 - Spotting antimicrobial peptides: physicochemical rule vs learned composition model vs homology transfer

Status: LOCKED before any method was scored (UTC time + sha256 in results/lock.txt). Lane RES-1.

## Question
Antimicrobial peptides (AMPs) are often described as short, cationic and amphipathic. Among short secreted peptides, does a simple learned composition model separate AMPs from other peptides better than a cationic-amphipathic rule, and does it beat plain nearest-neighbour homology transfer once homologs are kept out of the test folds?

## Data
UniProt reviewed (release 2026_03), length 10-60. Positives: keyword Antimicrobial (KW-0929). Negatives: location Secreted, NOT antimicrobial, NOT antibiotic (KW-0044), NOT toxin (KW-0800) - mostly hormones and neuropeptides, a hard control because all are short secreted peptides. Sequences with non-standard letters dropped. Query URLs, time, sha256 in data/.

## Split (homology-aware)
Groups = connected components linking two peptides if they share a UniProt family name OR their 3-mer sets have Jaccard >= 0.3. 5-fold GroupKFold, component order shuffled with seed 13.

## Methods
- R rule: score = net charge (K+R-D-E) x Eisenberg hydrophobic moment (100 deg, whole peptide). No training.
- L learned: logistic regression (C=1, balanced) on amino-acid composition (20) + dipeptide composition (400) + length, net charge, hydrophobic moment, standardized.
- NN homology baseline: score = max 3-mer Jaccard to a training AMP minus max to a training non-AMP.

## Metrics
AUROC and AUPRC, out-of-fold. Paired bootstrap (2000 resamples of groups) 95% CIs.

## Success gates (declared before scoring)
- G1: L AUROC - R AUROC >= 0.05, CI lower bound > 0.
- G2: L AUROC - NN AUROC > 0, CI lower bound > 0.
- G3: on the cysteine-rich subset (>= 4 Cys, both classes), L AUROC >= 0.80.
All reported pass or fail; any pivot is a timestamped post-hoc amendment.
