# algo50/80 - PCA of genotypes: when do PCs recover population structure?

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study. Topic lane-chosen (no list past 55).

## Question
PCA on SNP genotypes recovers ancestry axes when divergence is enough. Map the Fst threshold: at what between-population differentiation do PC1/PC2 separate clusters, and how many SNPs are needed?

## Data (simulated, seed 79)
Balanced 3-island model: 3 populations, 60 individuals each. L SNPs, L in {200, 1000, 5000}. Ancestral freq p ~ U(0.1,0.5); island freq = ancestral + drift with Fst in {0.01, 0.05, 0.15}: simulate via Beta((1-Fst)/Fst * p, (1-Fst)/Fst * (1-p)) (Balding-Nichols). Genotypes binomial(2, p_island).

## Methods
Standardize genotypes (center by mean freq, scale by sqrt(p(1-p))), SVD via numpy. Metrics: (a) cluster separation on PC1-PC2: silhouette score vs true labels; (b) correlation of PC1 with the first population contrast; (c) scree: variance ratio PC1/PC3 (structure vs noise).

## Gates
- G1: at Fst=0.05, L=5000: silhouette >= 0.5 (clear separation).
- G2: at Fst=0.01, L=200: silhouette < 0.3 (under-resolved regime exists).
- G3: silhouette non-decreasing in L at fixed Fst=0.05.
- G4: variance ratio PC1/PC3 > 2 at Fst=0.15 (structure dominates noise).
PASS if all.

## Failure policy
Negatives preserved; pivots via locked amendments.
