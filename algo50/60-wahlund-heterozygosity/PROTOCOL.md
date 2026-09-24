# algo50/60 - Wahlund effect: heterozygosity deficit under hidden structure

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study. Topic lane-chosen (no list past 55).

## Question
When two isolated populations with different allele frequencies are sampled as one pool, observed heterozygosity falls below the pooled-HWE expectation (Wahlund effect), and F_IS = Var(p)/E[p](1-E[p]) recovers the theoretical value. Does the simulated deficit match the exact theoretical formula, and how does it scale with frequency divergence and mixture proportion?

## Data (simulated, seed 17)
Biallelic SNP: population A freq p, population B freq p+d. d in {0.1, 0.3, 0.5, 0.7}; mixture w in {0.5, 0.3}; p=0.2. 1000 loci per cell (independent frequency draws around the cell's (p,d) with p jittered U(0.15,0.25), d fixed); 500 diploid individuals per population sample, genotypes drawn under within-population HWE.

## Methods
- Pooled sample: w*N from A, (1-w)*N from B.
- Observed heterozygosity Ho; expected under pooled allele freq: He = 2*pq(1-pq), pq = w*pA+(1-w)*pB.
- F_IS = 1 - Ho/He. Theory: F_IS = w(1-w)*d^2 / (pq*(1-pq)).
Metrics: |F_IS_sim - F_IS_theory| per cell; Ho/He ratio.

## Gates
- G1: |F_IS_sim - F_IS_theory| <= 0.02 in all 8 cells.
- G2: F_IS increases with d^2 (rank correlation = 1 across the 4 d values at w=0.5).
- G3: at w=0.5, d=0.5, p=0.2: Ho/He <= 0.75 (big visible deficit).
- G4: control - single undivided population at the same pooled frequency: F_IS within +/-0.02 of 0.
PASS if all.

## Failure policy
Negatives preserved; pivots via locked amendments.
