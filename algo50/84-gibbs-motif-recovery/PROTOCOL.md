# algo50/84 - Gibbs sampling for de novo motif recovery

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study. Topic lane-chosen (no list past 55).

## Question
Gibbs site sampler: recovery of a planted motif as a function of motif strength (information content) and the number of background sequences. Where is the recovery boundary?

## Data (simulated, seed 87)
Motif width 10; position weights: preferred base at probability q (others (1-q)/3), q in {0.5, 0.65, 0.8, 0.95} (IC ~ 0.4-8.6 bits). N sequences length 300, N in {10, 30}; each contains the motif instance at a random position with probability 0.9 (ZOOPS). 20 replicates per cell.

## Methods
Standard Gibbs site sampler: init random sites; iterate 300 sweeps: drop one sequence, build PWM from rest (pseudocount 0.5), sample new site proportional to PWM odds; track max-shift MAP estimate.
Metric per replicate: fraction of sequences whose chosen site overlaps the true instance by >= 5bp (site recall); replicate succeeds if recall >= 0.6.

## Gates
- G1: success rate >= 0.8 at q=0.8 and q=0.95, N=30.
- G2: success rate at q=0.5, N=30 <= 0.3 (weak-motif boundary exists).
- G3: N=10 >= N=30 success - 0.2 at every q (more sequences don't hurt much).
- G4: monotone: success non-decreasing in q at both N.
PASS if G1+G4; G2/G3 boundary.

## Failure policy
Negatives preserved; pivots via locked amendments.
