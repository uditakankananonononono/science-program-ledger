# algo50/20 - Hardy-Weinberg exact test vs chi-square at small allele counts

Status: LOCKED before any results (lock in results/lock.txt). Lane RES-2. Algorithm study.

## Question
The chi-square HWE test is anti-conservative at low minor-allele counts. Quantify: type-I inflation of chi2 vs the exact (Wigginton 2005) test across MAF and n, and the power cost of exactness under real inbreeding.

## Data (simulated)
Genotype counts drawn multinomial. Null: HWE at MAF p. Alternative: inbreeding F=0.1 (genotype probs: AA=p^2+Fpq, Aa=2pq(1-F), aa=q^2+Fpq). Replicates: 2000 per condition, seed 1.
Conditions: (A) null, MAF 0.05, n=500; (B) null, MAF 0.01, n=200; (C) F=0.1, MAF 0.2, n=500.

## Methods
- CHI2: Pearson chi-square, 1 df, no continuity correction.
- EXACT: Wigginton exact SNP-HWE test (probability of genotype configuration given allele counts, sum over configurations as or less probable).
alpha = 0.01.

## Gates
- G1: condition A, CHI2 type-I >= 2x EXACT type-I.
- G2: condition A, EXACT type-I in [0.003, 0.02].
- G3: condition C, EXACT power >= CHI2 power - 0.05.
- G4: condition B, EXACT type-I <= 0.05.
PASS if G1+G2; G3/G4 reported either way.

## Failure policy
Negatives preserved; pivots via locked amendments only.
