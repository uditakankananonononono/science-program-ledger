# algo50/32 - FM-index (BWT backward search) vs suffix-array binary search vs naive scan

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study.

## Question
Do all three exact-match engines agree on hit counts over the real E. coli genome, what is the per-query speed ordering, and is the BWT self-consistent (LF-mapping inversion roundtrip)?

## Data
NC_000913.3 (already in repo, hashed, from 04). Queries: 400 substrings of length 30 sampled from the genome (guaranteed >=1 hit) + 100 random 30-mers (mostly 0 hits). Seed 3.

## Methods
- Suffix array: prefix-doubling with numpy radix passes (O(n log n)).
- BWT from SA; Occ checkpoints every 64 symbols; LF backward search.
- SA binary search: two-sided bound on pattern prefix comparisons.
- Naive: str.find scan loop (C-speed reference for counts).
Metrics: hit-count agreement (all four engines, all 500 queries); wall time per query (median); BWT inversion check (reconstruct full genome from BWT via LF and compare sha to original).

## Gates
- G1: hit counts identical across all four engines for 500/500 queries.
- G2: BWT inversion reproduces the genome exactly (hash match).
- G3: FM and SA per-query median time <= 1% of naive scan.
- G4: FM per-query median <= 50% of SA per-query median (FM has no per-comparison string slicing). Boundary gate: informational.
PASS if G1+G2+G3.

## Failure policy
Negatives preserved; pivots via locked amendments.
