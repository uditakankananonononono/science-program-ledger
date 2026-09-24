# algo50/22 - r2 vs D' decay with distance, and recovering the decay length

Lane RES-2. Algorithm study. Protocol + Amendment 1 hashed before the results they gate (`results/lock.txt`).

## Bottom line
- A naive single-exponential fit to mean pairwise r2 badly misses the true correlation decay length: 8.8 kb recovered vs 50 kb simulated (G1 FAIL). Two stacked mechanisms: r2 decays like correlation SQUARED (exp(-2d/lambda)), and the 1/N sampling floor bends the tail.
- The corrected fit r2(d) = A*exp(-d/l) + c recovers l = 18.8 kb - inside the gate bracket around lambda/2 = 25 kb - and c = 0.0025 ~ 1.2/N (the sampling floor), both N=500 and N=100 (pivot P1-P3 PASS). Amplitude A ~ 0.51, near the (2/pi)^2 thresholding attenuation.
- |D'| decays far slower than r2, as textbooks say: at 90-100 kb mean |D'| is 12x mean r2 (G3 PASS).

## Data
Simulated: 200 SNPs x 5 kb, thresholded AR(1) Gaussian haplotypes (lambda=50 kb, MAF 0.1-0.4, seed 1), N=500 and N=100.

## Gates
- G1 FAIL: naive lambda_hat 8.8 kb vs 50 kb (estimator inconsistent under squaring + floor).
- G2 PASS: r2 near/far = 0.400 / 0.009 (44x).
- G3 PASS: |D'| far 0.114 = 12.6x r2 far.
- G4 FAIL: N=100 naive lambda_hat 9.4 kb (same inconsistency, not small-sample noise).
- Pivot: P1 PASS (l=18.8 kb in [15,40]), P2 PASS (c=0.0025 <= 0.006), P3 PASS (18.9 kb in [10,60]).

Original FAILS G1/G4; pivot PASSES. Net: mean-r2 exponential fits must model amplitude and sampling floor, and even then they estimate lambda/2, not lambda.

## Caveats
- The AR(1)-probit model is a convenience correlation structure, not a coalescent; real LD has blockiness and gene conversion.
- Unweighted least squares on mean r2 is itself a choice; distance-bin weighting shifts l by ~10-20%.

## Reproduce
`python3 code/run.py` (needs numpy, scipy; ~2 min).
