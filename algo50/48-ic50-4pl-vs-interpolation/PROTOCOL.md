# algo50/48 - IC50 estimation: four-parameter logistic fit vs linear interpolation

Status: LOCKED before any results (lock in results/lock.txt). Lane RES-3. Algorithm study.

## Question
Many labs read IC50 off a dose-response plot by interpolating between the two doses that bracket 50%. How much more accurate is a 4-parameter logistic (4PL) fit, for shallow and steep curves?

## Data (simulated)
8 doses log-spaced 0.01-100 (half-log steps would be 9; we use np.logspace(-2,2,8)), triplicate wells, response = bottom + (top-bottom)/(1+(dose/IC50)^h), bottom 0, top 100, IC50=1, noise N(0, 8^2). Hill h in {1, 3}. 1000 replicates each, seed 1.

## Methods
- INTERP: mean response per dose, linear interpolation in log10(dose) at the first crossing of 50.
- FOURPL: scipy curve_fit of 4PL on log10(dose), all wells, start (0,100,0,1); failure -> counted as non-converged and excluded.
Error = |log10(IC50_hat)|.

## Gates
- G1: h=1, median FOURPL error <= 0.8 x median INTERP error.
- G2: FOURPL converges in >= 95% of replicates at both h.
- G3: h=3, median FOURPL error <= median INTERP error.
- G4: h=1, median FOURPL error <= 0.10 (within ~26% on the dose scale).
PASS if G1+G2; G3/G4 reported either way.

## Failure policy
Negatives preserved; pivots via locked amendments only.
