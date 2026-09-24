# algo50/40 - Kaplan-Meier vs naive median survival under censoring

Status: LOCKED before any results (lock in results/lock.txt). Lane RES-3. Algorithm study.

## Question
How badly do naive median-survival estimates (drop censored patients, or treat censoring as death) miss the true median compared with Kaplan-Meier, as censoring grows?

## Data (simulated)
Survival T ~ Exponential(rate 0.1), true median ln2/0.1 = 6.931. Independent censoring C ~ Uniform(0, Cmax); Cmax chosen for about 30% censoring (Cmax=30) and about 60% censoring (Cmax=10). n=200 patients, 1000 replicates, seed 1.

## Methods
- KM: Kaplan-Meier product-limit, median = first time S(t) <= 0.5 (NaN if never reached).
- DROP: median of event times only (censored removed).
- ASDEATH: median of observed times treating censoring as events.
Relative bias = mean(estimate)/true - 1 over replicates where the estimate exists.

## Gates
- G1: 30% censoring, |KM rel. bias| <= 0.05.
- G2: 30% censoring, ASDEATH rel. bias <= -0.15.
- G3: 60% censoring, |KM rel. bias| <= 0.10 and KM median reached in >= 90% of replicates.
- G4: 30% censoring, |DROP rel. bias| >= 0.10.
PASS if G1+G2; G3/G4 reported either way.

## Failure policy
Negatives preserved; pivots via locked amendments only.
