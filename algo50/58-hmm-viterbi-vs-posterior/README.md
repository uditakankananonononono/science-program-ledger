# algo50/58 - HMM decoding: Viterbi vs posterior (MPM)

Lane RES-2. Algorithm study. Protocol hashed before results (`results/lock.txt`). Topic lane-chosen (no list past 55).

## Bottom line
Decoders are NOT interchangeable in hard regimes: Viterbi and MPM disagree on 36% of positions at delta=0.05/stay=0.90 (G2), shrinking to 0.6% at delta=0.30/stay=0.99. MPM is never materially worse and consistently beats Viterbi on per-position state accuracy (G3) - as theory predicts, since MPM maximizes expected per-position accuracy while Viterbi optimizes whole-path probability. But G4 FAILS: at delta=0.30, stay=0.90 both decoders stall at ~87-88% - with mean run length 10, boundary localization is emission-limited and 98% is unreachable by ANY decoder using the same emissions (both decoders pass 98% at stay=0.99: 0.9825/0.9838). The limit is information-theoretic, not algorithmic.

## Bug fixed before final scoring (documented)
First forward-backward run underflowed to zero over 2000 positions (linear-space probabilities), collapsing MPM to chance. Fixed with per-step rescaling; all scored numbers from the scaled implementation. G1's brute-force enumeration check (length-8, exact) guards correctness of the scaling.

## Data
Simulated 2-state HMM, seed 13; delta in {0.05,0.15,0.30} x stay in {0.90,0.99}; 60 sequences x 2000 bp per cell.

## Gates
G1 PASS, G2 PASS, G3 PASS (MPM >= Viterbi - 0.005 in all cells; direction: MPM wins), G4 FAIL (stay=0.90 cell unreachable; stay=0.99 passes). Overall: FAIL on G4 - documented boundary, no pivot (the failure is information-theoretic, not fixable by another algorithm).

## Caveats
- 2-state emissions over ACGT only; richer HMMs (CpG, gene finders) have more state structure where Viterbi-vs-MPM trade-offs (path consistency) matter more.
- MPM can produce state sequences that are impossible under the transition matrix; not scored here.

## Reproduce
`python3 code/run.py` (numpy only; ~1 min).
