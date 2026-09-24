# algo50/22 - r2 vs D' decay with distance, and recovering the decay length

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study.

## Question
Under a known correlation-decay model, does the standard r2 estimator recover the decay length, how much slower does |D'| decay (saturation), and how badly does a small haplotype sample degrade the estimate?

## Data (simulated)
200 SNPs spaced 5 kb over 1 Mb. Latent AR(1) Gaussian chain X_i with correlation a_i = exp(-d_i/lambda), lambda = 50 kb; haplotypes = threshold(X_i) with per-SNP thresholds set for MAF uniform 0.1-0.4 (threshold from normal quantiles, seed 1). N=500 haplotypes (and N=100 for the small-sample boundary), seed 1.

## Methods
- Pairwise r2 and |D'| for all SNP pairs; binned means by distance.
- Decay length estimate: least-squares fit of mean-r2(d) ~ exp(-d/l) over all pairs (1-parameter fit on log scale).

## Gates
- G1: N=500 lambda_hat within +/-30% of 50 kb.
- G2: mean r2 at <10 kb >= 3x mean r2 at 90-100 kb.
- G3: mean |D'| at 90-100 kb >= 2x mean r2 at 90-100 kb (D' saturates / decays slower).
- G4: N=100 lambda_hat within +/-60%.
PASS if G1+G2; G3/G4 boundary.

## Failure policy
Negatives preserved; pivots via locked amendments.
