# algo50/36 - DUST-style low-complexity masking

Lane RES-2. Algorithm study. Protocol + 2 amendments hashed before the results they gate (`results/lock.txt`).

## Bottom line
The masker itself works: 100% of 40 implanted low-complexity regions recovered (G1), 0.96% false-masking on random background (G2), and 100% of spurious low-complexity shared 25-mers removed (Amendment 2). The cost is real though: 2/50 legitimate orthologous 25-mers lost to background overmasking (96% retention vs 98% gate) - Q2 fails by one ortholog. Masking trades a small true-sequence loss for complete artifact removal at this threshold (mean+3sd, w=64, stride 16).

## What the two failed stages actually showed
- Original G3 FAIL and Amendment 1 P2 FAIL were harness artifacts, diagnosed and documented: independent implant coordinates collided (later implants overwrote orthologs), and set-based kmer bookkeeping counts stochastic flank-extension matches (~2/3 per implant by chance) as spurious shares. Only the position-based bookkeeping of Amendment 2 measures the masker rather than the harness.

## Gates
- Original: G1 PASS, G2 PASS, G3 FAIL (harness artifact).
- Amendment 1: P1/P2 FAIL (harness artifact persists: separate coordinate pools still collided).
- Amendment 2: Q1 PASS (recall 1.0, false-mask 0.0096), Q2 FAIL (spurious removal 60/60 but ortholog retention 48/50 < 49).
Net: masking achieves complete artifact removal at ~1% background cost and ~4% unique-kmer loss; the 98%-retention gate is not met at this threshold. Boundary documented, not hidden.

## Caveats
- Simulated background (iid uniform); real genomes have higher local redundancy, likely raising false-mask rates.
- Lowering the threshold would trade retention for removal; not explored (would require a new locked stage).

## Reproduce
`python3 code/run.py && python3 code/pivot.py && python3 code/pivot2.py` (numpy only, <1 min).
