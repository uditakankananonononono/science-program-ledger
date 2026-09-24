# algo50/52 - Missing clinical data under MAR: complete-case vs mean vs regression imputation vs IPW

Status: LOCKED before any results (lock in results/lock.txt). Lane RES-3. Algorithm study.

## Question
When a lab value is missing more often for some patients (missing at random given an observed covariate), how biased are the common quick fixes for estimating its population mean and SD?

## Data (simulated)
n=500. x ~ N(0,1) (always observed, e.g. age z-score). y = 1 + 0.8x + N(0, 0.6^2); true mean 1, true SD 1.0. y missing with P = logistic(-0.5 + 1.5x) (sicker/older more often missing; ~40% missing). 2000 replicates, seed 1.

## Methods
- CC: mean/SD of observed y.
- MEANIMP: fill missing y with observed mean.
- REGIMP: fill with OLS prediction from x (fit on observed).
- IPW: weight observed y by 1/P(observed | x), P from a logistic fit of observedness on x (Newton, 25 iterations).

## Gates
- G1: |CC mean bias| >= 0.20.
- G2: |REGIMP mean bias| <= 0.03.
- G3: MEANIMP SD underestimated by >= 20% (mean SD <= 0.80).
- G4: |IPW mean bias| <= 0.05.
PASS if G1+G2; G3/G4 reported either way. REGIMP SD also reported (expected to be too small; not gated).

## Failure policy
Negatives preserved; pivots via locked amendments only.
