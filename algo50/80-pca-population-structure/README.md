# algo50/80 - PCA of genotypes: when do PCs recover population structure?

Lane RES-2. Algorithm study. Protocol hashed before results (`results/lock.txt`). Topic lane-chosen (no list past 55).

## Bottom line
All gates PASS. Under a 3-island Balding-Nichols model, PCA recovers population structure strongly even at Fst=0.01 given 5000 SNPs (silhouette 0.83), and is under-resolved only at the low corner (Fst=0.01, 200 SNPs: 0.076). Separation improves monotonically with SNP count, and the structure-vs-noise variance ratio (PC1/PC3) rises 1.1 -> 14.7 across the grid. SNP count substitutes for divergence: the L-dose-response is the practical takeaway for study design.

## Data
Simulated (seed 79): 3 islands x 60 diploids, Balding-Nichols drift, L in {200,1000,5000}, Fst in {0.01,0.05,0.15}.

## Gates
G1 PASS (0.94), G2 PASS (0.076), G3 PASS (monotone in L), G4 PASS (14.7 > 2). Overall PASS.

## Caveats
- Balanced islands, no admixture, no relatedness - real datasets add all three, and PC interpretation gets harder (known: PCs can reflect relatedness or sampling artifacts).
- Silhouette on PC1-PC2 only; higher-dimensional structure (4+ populations) untested.

## Reproduce
`python3 code/run.py` (numpy+sklearn, ~20 s).
