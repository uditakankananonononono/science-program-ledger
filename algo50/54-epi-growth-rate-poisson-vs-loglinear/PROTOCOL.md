# algo50/54 - Early epidemic growth rate: log-linear regression vs Poisson GLM on low counts

Status: LOCKED before any results (lock in results/lock.txt). Lane RES-3. Algorithm study.

## Question
Outbreak dashboards often estimate the growth rate by regressing log(cases+1) on day. At low counts (early outbreak, small region), how biased is that versus a Poisson GLM?

## Data (simulated)
Daily cases C_t ~ Poisson(c0 * exp(r t)), t=0..29, true r=0.10. Low start c0=2; high start c0=50. 2000 replicates each, seed 1.

## Methods
- LOGLIN: OLS slope of log(C_t + 1) on t.
- POISGLM: Poisson regression log E[C_t] = a + r t, fit by Newton-IRLS (50 iterations).

## Gates
- G1: c0=2, |LOGLIN bias| >= 0.01.
- G2: c0=2, |POISGLM bias| <= 0.005.
- G3: c0=2, POISGLM RMSE <= 0.8 x LOGLIN RMSE.
- G4: c0=50, |LOGLIN bias| <= 0.005 (the problem is a low-count problem).
PASS if G1+G2; G3/G4 reported either way.

## Failure policy
Negatives preserved; pivots via locked amendments only.
