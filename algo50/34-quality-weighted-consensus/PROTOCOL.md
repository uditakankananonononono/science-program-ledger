# algo50/34 - Quality-weighted vs majority-vote consensus base calling

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study.

## Question
Does Phred-quality-weighted consensus calling beat majority vote, and how does the advantage scale with coverage and error rate?

## Data (simulated, seed 5)
Reference: 20,000 random bases. At coverages c in {3,5,8,15,30}: simulate c reads per position; each observed base wrong with prob e drawn per-read from a quality distribution: Q ~ uniform {10,20,30,40} (e = 10^(-Q/10)); errors choose uniformly among the 3 other bases.

## Methods
- MAJ: most frequent observed base.
- QW: pick base maximizing sum over reads of log-likelihood: log(1-e) if read base == candidate else log(e/3).
Metrics: consensus error rate vs truth, per coverage, 20k positions.

## Gates
- G1: QW error rate <= MAJ error rate at every coverage (never worse).
- G2: at c=3, QW error rate <= 60% of MAJ's (big low-coverage win).
- G3: at c=30, both error rates < 1e-4 (convergence).
- G4: QW error rate at c=8 <= MAJ error rate at c=15 (quality buys ~2x coverage). Boundary gate.
PASS if G1+G2+G3.

## Failure policy
Negatives preserved; pivots via locked amendments.
