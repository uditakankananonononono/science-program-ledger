# algo50/58 - HMM decoding: Viterbi vs posterior (MPM) under mismatch

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study. Topic lane-chosen (no list past 55).

## Question
Viterbi finds the single most likely path; posterior (MPM) decoding picks the most likely state per position. On simulated data from a known 2-state HMM: how much do they disagree, and which recovers the true state path better - as a function of emission separation and transition stickiness?

## Data (simulated, seed 13)
2-state HMM (G/C-rich vs AT-rich emission over ACGT), emission divergence delta in {0.05, 0.15, 0.30} (mixture coefficient between uniform and state-preferred base), self-transition p_stay in {0.90, 0.99}. 200 sequences of length 2000 per cell; true states recorded.

## Methods
Implement forward-backward (posterior decoding) and Viterbi (log-space) from scratch; verify against each other (posterior marginal of state at t from F-B vs brute-force enumeration on tiny sequences, n=8, all 2^8 paths).
Metrics per cell: state accuracy of Viterbi vs MPM vs truth; path-disagreement fraction between decoders; also MPM expected accuracy (mean max posterior) vs realized.

## Gates
- G1: implementation check: F-B posterior marginals match brute-force enumeration on 50 random length-8 sequences to < 1e-8.
- G2: Viterbi and MPM disagree on >= 0.5% of positions at delta=0.05, p_stay=0.90 (hard regime) - decoders are NOT interchangeable there.
- G3: Viterbi state accuracy >= MPM accuracy - 0.5% in every cell (Viterbi never materially worse) OR the reverse with a documented regime - direction reported honestly.
- G4: at delta=0.30 both decoders reach >= 98% accuracy (easy regime sanity).
PASS if G1 + G4 + (G2 or documented boundary on G2).

## Failure policy
Negatives preserved; pivots via locked amendments.
