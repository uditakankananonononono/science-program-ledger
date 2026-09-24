# algo50/38 - Exact-seed hit probability: simulation vs iid theory

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study.

## Question
For a read of length L with per-base error rate e, the probability that at least one exact k-mer seed survives is P = 1 - P(no error-free window of length k). Under iid errors, P(no error-free k-window) is computable exactly by a DP (probability no run of k successes in L Bernoulli trials). Does simulation match theory, and how sharply does hit probability fall with e and k?

## Data (simulated, seed 9)
L=100; e in {0.01,0.02,0.05,0.10,0.15,0.20}; k in {11,15,18,21,25}. 20,000 reads per (e,k): each base corrupted iid with prob e; a read is a "hit" if it retains >= 1 error-free window of length k.

## Methods
- Simulation: hit fraction per cell.
- Theory: DP for no-run-of-k-correct-bases probability with p=1-e per base.
- Also spaced-seed contrast: 1 seed of length 15 vs 2 independent seeds of length 11 (hit if EITHER survives): simulated only.

## Gates
- G1: |sim - theory| <= 2*SE in >= 24/30 cells (SE from binomial).
- G2: at e=0.05, hit probability >= 0.99 for k=11 and <= 0.60 for k=25 (steep k-dependence).
- G3: two 11-mers beat one 15-mer at every e (spaced/multi-seed redundancy wins).
PASS if all.

## Failure policy
Negatives preserved; pivots via locked amendments.
