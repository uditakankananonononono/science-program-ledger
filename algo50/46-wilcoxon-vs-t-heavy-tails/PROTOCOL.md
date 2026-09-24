# algo50/46 - Wilcoxon rank-sum vs Welch t-test on heavy-tailed assay data

Status: LOCKED before any results (lock in results/lock.txt). Lane RES-3. Algorithm study.

## Question
For small two-group lab comparisons, how much power does the t-test lose to Wilcoxon when data have heavy tails, and how much does Wilcoxon cost when data are normal?

## Data (simulated)
Two groups, n=20 each, location shift delta=0.8. Distributions: NORMAL N(0,1); T3 Student t with 3 df. Null (delta=0) also run under T3. 4000 replicates per condition, seed 1. alpha=0.05, two-sided.

## Methods
- WELCH: Welch two-sample t-test.
- WRS: Wilcoxon rank-sum / Mann-Whitney U (asymptotic, continuity-corrected).

## Gates
- G1: NORMAL, WRS power >= WELCH power - 0.05.
- G2: T3, WRS power >= WELCH power + 0.05.
- G3: T3 null, both type-I rates <= 0.06.
- G4: NORMAL, WELCH power >= WRS power (t is optimal under normality).
PASS if G1+G2; G3/G4 reported either way.

## Failure policy
Negatives preserved; pivots via locked amendments only.
