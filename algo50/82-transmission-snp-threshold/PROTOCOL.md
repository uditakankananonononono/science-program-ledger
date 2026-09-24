# algo50/82 - Outbreak transmission inference: SNP-distance threshold calibration

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study. Topic lane-chosen (no list past 55).

## Question
"Direct transmission if <= T SNPs" is the standard outbreak heuristic. Calibrate T against a known simulated transmission chain: what T maximizes F1, and how much do sampling times (generation intervals) move the optimum?

## Data (simulated, seed 83)
Outbreak: index case + 3 transmission generations, each case infects 1-3 (Poisson(1.2)+0.5 floor...) - concretely: chain tree with ~40 cases over 60 days. Genome 30 kb, mutation rate 0.5 substitutions/genome/generation-interval... realistic: 25 SNPs/genome/year => per 5-day generation ~0.34. Within-host: transmitted genotype = single random virion (bottleneck). Sampling: each case sequenced at detection, 0-15 days after infection.

## Methods
- Pairwise SNP distances between all sampled genomes.
- Truth: direct transmission pairs (infector-infectee).
- For T in 0..8: precision/recall/F1 of "pair is transmission pair iff distance <= T".
- Also: distance-vs-time-difference calibration: does adding sampling-date consistency (infector sampled earlier) improve F1?

## Gates
- G1: best-T F1 >= 0.60 (threshold method has real signal).
- G2: the optimal T is in {1,2,3} (matches field heuristics).
- G3: adding the time-consistency filter improves F1 by >= 0.05.
- G4: at T=best, precision >= 0.7 (low false-linkage).
PASS if G1+G4 plus one of G2/G3.

## Failure policy
Negatives preserved; pivots via locked amendments.

---

# AMENDMENT 1 (locked before pivot scoring)
All original gates failed with a real finding: in a slow-mutation outbreak, sibling and aunt-niece pairs are as close as direct pairs (at T=1, recall=1.0 but precision=0.13 - ~280 non-direct pairs within 1 SNP). A SNP threshold cannot isolate DIRECT transmission; it identifies epidemiological CLUSTERS. Time-filter added only +0.016.
Pivot P (same simulated outbreak, seed 83 - the finding is a metric re-aim, not a new dataset; no parameter of the sim is touched): truth = pairs within 2 transmission steps on the chain tree (direct OR share an infector OR grandparent).
- P1: best-T F1 >= 0.70 for within-2-steps linkage.
- P2: precision at best T >= 0.80.
- P3: best T in {1,2,3}.
PASS if P1+P2.
