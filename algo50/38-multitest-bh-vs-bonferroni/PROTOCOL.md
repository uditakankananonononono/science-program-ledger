# algo50/38 - Benjamini-Hochberg vs Bonferroni in genome-scale testing

Status: LOCKED before any results (lock in results/lock.txt). Lane RES-3. Algorithm study.

## Question
In a GWAS/DE-style screen, how much power does BH-FDR buy over Bonferroni, and does BH keep FDR near nominal when test statistics are positively correlated?

## Data (simulated)
m=1000 z-tests, 10% true signals with mean shift 3.0, rest null N(0,1). Two regimes: independent; equicorrelated rho=0.5 (one-factor model). 500 replicates each, seed 1. One-sided p-values.

## Methods
UNC: p<0.05. BONF: p<0.05/m. BH: step-up at q=0.05.
FDR = mean(false discoveries / max(1, discoveries)); power = mean(true discoveries / 100).

## Gates
- G1: independent, BH FDR <= 0.055.
- G2: independent, BH power >= 2x BONF power.
- G3: rho=0.5, BH FDR <= 0.055 (PRDS theory says controlled).
- G4: independent, UNC FDR >= 0.20 (motivation check).
PASS if G1+G2; G3/G4 reported either way.

## Failure policy
Negatives preserved; pivots via locked amendments only.
