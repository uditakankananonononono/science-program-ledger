# algo50/02 - Minimizer sketches for long-read overlap detection across error rates

Lane RES-2. Algorithm study (not counted toward the flagship 100). Protocol hashed and timestamped before scoring (`results/lock.txt`).

## Bottom line
- A minimizer sketch (k=15, w=10, canonical, splitmix64 ordering) that keeps only ~18% of k-mers (median set 1,313 vs 7,236) loses almost no overlap signal: recall within a 2%-of-all-pairs candidate budget is 0.9978 overall and 1.000 on the 15%-error stratum; AUPRC 0.879 vs 0.893 for exact shared-k-mer counting (98.4% of it); AUROC 0.99967 vs 0.99975.
- But the speed story fails in pure Python: end-to-end scoring is only ~2.2x faster (median time ratio 0.462 over 5 clean reps, range 0.388-0.583), not the ~5.5x the set sizes promise. Hashing and window-min computation over every k-mer eats the sketching dividend; the win is in memory/candidate volume, not wall time, at this implementation level.

## Data
E. coli K-12 MG1655 reference NC_000913.3 via NCBI efetch (timestamp `data/retrieved_at.txt`, sha256 `data/SHA256_raw.txt`; raw FASTA and simulated reads not committed, regenerate with `code/prep.py`, seed 1). 600 simulated reads (200 each at 5/10/15% error, 90/5/5 sub/ins/del), length 3-12 kb, random strand. Ground truth: reference-interval overlap >= 1000 bp (457 true pairs of 179,700).

## Results (results/results.json, results/timing_reps.json)
| method | AUROC | AUPRC | recall@2% budget | recall@2%, 15% error | wall time (s) |
|---|---|---|---|---|---|
| EK exact k=15 shared count | 0.99975 | 0.893 | 1.000 | 1.000 | ~9.5-10.6 |
| MIN minimizers w=10 | 0.99967 | 0.879 | 0.9978 | 1.000 | ~4.1-5.5 |

## Gates
- G1 PASS: MIN recall@2% = 0.9978 (needed >= 0.95).
- G2 PASS: AUPRC ratio 0.984 (needed >= 0.95).
- G3 FAIL: median time ratio 0.462 (needed <= 0.35). Secondary product gate; noisy on 2 shared cores but the median is clearly above gate. Set size is 5.5x smaller; featurization cost eats it.
- G4 PASS: 15%-error stratum recall@2% = 1.000 (needed >= 0.90).

Project PASSES (G1+G2+G4; G3 secondary, failed and documented).

## Caveats
- AUROC is inflated for both methods by the 84-96% of negative pairs scoring exactly 0; AUPRC is the informative ranking metric here.
- AUPRC is capped ~0.89 by repeat-driven false positives (rRNA operons, insertion sequences): some non-overlapping pairs share hundreds of k-mers. No repeat masking, per protocol.
- Errors are synthetic and uniform (90/5/5 sub/ins/del; ~1/4 of substitutions are no-ops), so real ONT/HiFi error structure may stress sketches differently. Single small genome.
- Timings are pure Python on 2 shared cores: relative, noisy, not absolute.

## Reproduce
`python3 code/prep.py && python3 code/score.py` (needs numpy, scikit-learn; ~1 min on 2 cores). Timing reps: rerun the featurize+score block 5x as in results/timing_reps.json.
