# algo50/17 - Predicting a microbe's optimal growth temperature from proteome composition: IVYWREL vs a learned composition model

Status: LOCKED before any proteome composition was computed (UTC time + sha256 in results/lock.txt). Lane RES-1.

## Question
Zeldovich et al. 2007 (PLoS Comput Biol) showed the proteome fraction of 7 amino acids (I,V,Y,W,R,E,L) tracks optimal growth temperature (OGT). Does a regularized model over all 20 amino-acid fractions predict OGT better than the IVYWREL line, when whole taxonomic families are held out?

## Data
- OGT labels: TEMPURA (https://togodb.org/release/tempura.csv), Topt_ave in C.
- Proteomes: UniProt reference proteomes of Bacteria and Archaea (list query URL in data/source_url.txt), matched to TEMPURA by genus+species name.
- Selection (seed 17): one matched species per genus (random pick), then a random 120 with Topt >= 50 C and a random 120 with Topt < 50 C, 240 organisms total (balanced so thermophiles are not under-represented). The composition of each proteome = amino-acid counts over all its UniProt entries (FASTA stream), stored in results/composition.tsv with proteome IDs and UniProt release.

## Methods
- B (IVYWREL baseline): OGT = a + b x IVYWREL fraction, least squares fitted on training folds.
- L (learned): ridge regression on the 20 amino-acid fractions (standardized), alpha picked from {0.01,0.1,1,10,100} by inner 5-fold CV on the training fold only.
- Split: 5-fold GroupKFold grouped by taxonomic family (TEMPURA 'family'; missing -> genus), group order shuffled with seed 17.

## Metrics
MAE and Pearson r, out-of-fold. Paired bootstrap over organisms (2000) for MAE differences.

## Success gates (declared before any composition was computed)
- G1: MAE(B) - MAE(L) >= 1.0 C, 95% CI lower bound > 0.
- G2: Pearson r(L) >= 0.85.
- G3 (domain transfer): train on Bacteria only, test on Archaea: MAE(L) <= MAE(B), both refit on Bacteria.
All reported pass or fail; one post-hoc pivot allowed, locked before scoring.

## Amendment 1 (implementation only, before any score was produced)
model.py crashed on a missing family value read back from selected.tsv (pandas reads the literal family name as NaN). Fix: fill missing family with genus as already stated in the split rule. No method change.
