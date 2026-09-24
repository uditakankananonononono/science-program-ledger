# algo50/44 - Mendelian randomization: IVW vs MR-Egger under directional pleiotropy

Status: LOCKED before any results (lock in results/lock.txt). Lane RES-3. Algorithm study.

## Question
How much does directional pleiotropy bias the standard IVW causal estimate, and how much precision does MR-Egger give up to remove that bias?

## Data (simulated summary statistics)
J=30 variants. True SNP-exposure effects bx_j ~ U(0.05, 0.20); causal effect 0.3. SNP-outcome: by_j = 0.3*bx_j + alpha_j. Observed bx_hat = bx + N(0, 0.01^2), by_hat = by + N(0, 0.02^2). Scenarios: NONE alpha=0; DIR alpha_j ~ U(0, 0.04) independent of bx (InSIDE holds). 1000 replicates, seed 1.

## Methods
- IVW: weighted regression of by_hat on bx_hat through the origin, weights 1/0.02^2.
- EGGER: same weighted regression with intercept (bx oriented positive).

## Gates
- G1: NONE, |IVW bias| <= 0.03.
- G2: DIR, IVW bias >= 0.10.
- G3: DIR, |EGGER bias| <= 0.05.
- G4: DIR, EGGER empirical SD >= 2x IVW empirical SD (precision cost).
PASS if G2+G3; G1/G4 reported either way.

## Failure policy
Negatives preserved; pivots via locked amendments only.
