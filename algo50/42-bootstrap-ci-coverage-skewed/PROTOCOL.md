# algo50/42 - Bootstrap percentile vs t confidence intervals on skewed biomarker data

Status: LOCKED before any results (lock in results/lock.txt). Lane RES-3. Algorithm study.

## Question
Biomarker levels are often log-normal and studies are small. Does the percentile bootstrap fix the t-interval's undercoverage for the mean at small n, or is it worse?

## Data (simulated)
X ~ LogNormal(0, 1), true mean exp(0.5)=1.6487. n in {15, 100}. 2000 replicates per n, B=999 bootstrap resamples, seed 1. Nominal 95%.

## Methods
- T: mean +/- t(0.975, n-1) * sd/sqrt(n).
- PCT: percentile bootstrap, 2.5/97.5 percentiles of resampled means.

## Gates
- G1: n=15, T coverage <= 0.925 (undercoverage exists).
- G2: n=15, PCT coverage >= T coverage + 0.02 (bootstrap fixes it).
- G3: n=100, both coverages >= 0.92.
- G4: n=15, PCT mean width <= 1.10 x T width.
PASS if G1+G2; G3/G4 reported either way.

## Failure policy
Negatives preserved; pivots via locked amendments only.
