# algo50/24 - PWM log-odds vs consensus best-match for motif scanning

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study.

## Question
For finding weak motif instances in sequence, how much does a position weight matrix log-odds score beat matching to the consensus string, and how does the edge change as instance strength drops?

## Data (simulated, seed 1)
Background: 400 sequences x 500 bp, iid at GC 0.45. Motif: 8-mer with consensus CACGTGCA, per-position information decreasing from the center (positions 1-8 match probs 0.62,0.80,0.95,0.98,0.98,0.95,0.80,0.62), non-consensus bases uniform. 200 sequences get one planted instance (random position), 200 get none. Additionally a WEAK copy of the same set: all match probs scaled 0.85x.

## Methods
- CONS: best consensus match count to CACGTGCA over all 8-mers in the sequence.
- PWM: max log-odds (trained PWM = true generative probabilities + 1e-4 pseudocount vs background mononucleotide) over all 8-mers.
Unit = sequence; score = best 8-mer.

## Gates
- G1: PWM AUROC >= CONS AUROC + 0.03 (standard strength).
- G2: PWM TPR at 1% FPR >= CONS TPR at 1% FPR + 0.10 (standard).
- G3: weak set, PWM AUROC >= CONS + 0.05 (edge grows when instances weaken).
- G4: PWM AUROC on standard set >= 0.85 (absolute bar).
PASS if G1+G2; G3/G4 boundary.

## Failure policy
Negatives preserved; pivots via locked amendments.
