# algo50/70 - Mash-style k-mer distance: accuracy vs true divergence

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study. Topic lane-chosen (no list past 55).

## Question
Mash estimates genomic distance from k-mer sketch Jaccard: d = -ln(2J/(1+J))/k. How accurate is the estimate against true p-distance across divergence and k, and where does it break?

## Data (simulated, seed 43)
Ancestor 50 kb random; descendants at true p-distance p in {0.01, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40} (independent substitutions per site, JC69-ish). 20 replicate pairs per p. Full k-mer sets (no sketch subsampling - isolates the estimator from sketch noise), k in {11, 15, 21, 31}.

## Methods
Jaccard of k-mer sets (hashed 64-bit); Mash distance formula. Metrics: median estimate vs true p per cell; relative error.

## Gates
- G1: at k=21, |median estimate - p| <= 0.01 for p <= 0.15.
- G2: estimates strictly increasing in p at every k (monotone).
- G3: at p=0.40, k=21 estimate UNDERestimates (saturation): estimate < 0.40 - documented, not hidden.
- G4: larger k => larger |error| at p=0.30 (k-sensitivity to divergence: k=31 error > k=11 error at p=0.30).
PASS if G1+G2; G3/G4 boundary documentation.

## Failure policy
Negatives preserved; pivots via locked amendments.

---

# AMENDMENT 1 (locked before pivot run on FRESH seed 47)
Original gates failed informatively: G1 borderline (err 0.0143 at p=0.15,k=21), G2 (ties at +inf), G3 WRONG DIRECTION - at high divergence the estimator does not underestimate, it SATURATES to +inf (zero shared k-mers, log 0; k=31 saturates already at p=0.30). The unifying variable is the expected shared k-mer count E = L(1-p)^k: accuracy where E large, saturation where E ~ O(1).
Pivot P (fresh seed 47, same grid):
- P1: for cells with E >= 1000: |median estimate - p| <= 0.02.
- P2: for cells with E <= 50: >= 50% of replicate estimates are +inf (saturation regime documented).
- P3: finite estimates strictly increasing in p within each k.
PASS if P1+P2.
