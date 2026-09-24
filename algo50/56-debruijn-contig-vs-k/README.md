# algo50/56 - de Bruijn assembly: contig N50 vs k, and the repeat-resolving limit

Lane RES-2. Algorithm study. Protocol + Amendments 1-2 hashed before the results they gate (`results/lock.txt`).
Topics past 55 are lane-chosen (no topic list exists; per main 13:50 IST).

## Bottom line
de Bruijn contiguity is repeat-limited, not coverage-limited, exactly as theory says: with 8 implanted exact repeats (200-6400 bp) and error-free reads, the unresolved-repeat count equals #{repeats with R >= k} at EVERY k from 15 to 7000 (P1), N50 jumps each time k crosses a repeat length (18.0k -> 18.3k -> 31.9k -> 33.7k -> full-length 120 kb single contig at k=7000; P2, P3). Small-k assemblies are already repeat-dominated: N50(15) = 3.8 kb is set by repeat spacing, not by k - which is why the original G3 (expecting a 5x N50 range over k=15..99) and G4 (naive coverage fraction) were miscalibrated.

## Gates
- Original: G1 PASS (monotone N50), G2 PASS (8/8 repeats unresolved at k<=51), G3 FAIL (flat N50 - repeats exceed all tested k), G4 FAIL (coverage formula ignored repeat collapse).
- Amendment 1 (extended k range 15..7000, hashed graph): P2 PASS; P1+P3 FAIL on measurement defects (probe position bug when R<2k; coverage formula missing per-unitig k-1 padding) - documented.
- Amendment 2 (probe fixed; P3 = single-contig endpoint): P1 PASS, P2 PASS, P3 PASS.
Original FAILS G3+G4 on theory miscalibration; corrected pivot PASSES fully.

## Caveats
- Error-free single-strand reads; real assemblies add error tolerance, double-stranding, and coverage cutoffs.
- 64-bit rolling hash used for k>=250; collision probability ~1e-14 per pair, unobserved.
- Repeat copies were same-orientation; inverted repeats add palindrome edge cases not tested.

## Reproduce
`python3 code/run.py && python3 code/pivot.py` (numpy only; ~30 s).
