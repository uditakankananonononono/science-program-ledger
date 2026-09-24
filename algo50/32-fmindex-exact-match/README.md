# algo50/32 - FM-index vs suffix-array binary search vs naive scan

Lane RES-2. Algorithm study. Protocol hashed before results (`results/lock.txt`).

## Bottom line
Correctness gates pass: all three engines agree on hit counts for 500/500 queries over the E. coli genome, and BWT inversion reconstructs the genome byte-exactly. Speed gates fail: FM backward search costs 1.48% of naive per query (gate <= 1%) and is ~7x SLOWER than suffix-array binary search (gate <= 50%). At 4.6 Mbp, SA binary search's C-speed string slicing (~25 comparisons) beats pure-Python backward stepping; FM's asymptotic edge needs bigger alphabets, slower baselines, or native code.

## Bugs found and fixed before scoring (all scored numbers from the corrected build)
1. SA rank array uninitialized at sa[0] (nr[sa[0]] never set).
2. sa_search second binary-search loop inherited the exhausted r from the first loop - always returned 0.
3. C table offsets omitted the sentinel ('$' sorts before 'A'), shifting every FM/LF offset by 1 - broke both backward search and BWT inversion.
Each was caught by the gate machinery itself (disagreement with naive scan / failed inversion), which is the point of cross-engine agreement gates.

## Data
NC_000913.3 (hash in `data/SHA256_raw.txt`). 400 genuine 30-mers + 100 random 30-mers, seed 3.

## Gates
- G1 PASS (500/500 agreement), G2 PASS (byte-exact inversion), G3 FAIL (FM 1.48% vs <=1%), G4 FAIL (FM/SA = 7.25 vs <=0.50).
Overall: original gates FAIL on speed only; correctness fully confirmed. No pivot: the negative is the finding (FM's wall-time advantage does not materialize vs C-backed SA search at this scale/implementation); documented, not hidden.

## Caveats
- Pure-Python FM inner loop; a C FM implementation would change G3/G4. The claim is about this implementation regime.
- SA construction (numpy prefix-doubling) ~20 s for 4.6 Mbp - excluded from per-query metrics.

## Reproduce
`python3 code/run.py` (biopython, numpy; ~40 s).
