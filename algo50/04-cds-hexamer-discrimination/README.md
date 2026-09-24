# algo50/04 - In-frame hexamer scoring for CDS vs shadow-ORF discrimination, and its cross-genome boundary

Lane RES-2. Algorithm study (not counted toward the flagship 100). Protocol and Amendment 1 each hashed before the results they gate (`results/lock.txt`).

## Bottom line
- The textbook gene-finder feature fails in the hard setting. A 5th-order in-frame hexamer log-likelihood model (Glimmer-style) separates real CDS from stop-to-stop shadow ORFs (>=150 nt, containing no annotated gene) at only AUROC 0.78 within E. coli - far below the 0.90 gate.
- The trivial model wins: amino-acid usage LLR (DI) hits 0.994 within E. coli and transfers almost untouched to B. subtilis (0.993) and even to 66%-GC M. tuberculosis (0.996). Frame-shifted shadows of real proteins have strongly non-protein amino-acid composition; hexamer statistics in shifted frames still look coding-like, so the Markov model is fooled where the composition model is not.
- Pivot (Amendment 1, all 3 gates PASS): a 5-feature logistic (GC, GC3, LEN, DI, HEX) reaches 0.998 within E. coli and transfers to M. tb at 0.996 - the combination learns to lean on DI.
- GC/GC3/LEN are worthless here (AUROC 0.41-0.50; GC below 0.5 because stop-free ORFs are GC-enriched - stop codons are AT-rich).

## Data
NC_000913.3 (E. coli), NC_000964.3 (B. subtilis), NC_000962.3 (M. tuberculosis) via NCBI efetch GenBank (timestamp `data/retrieved_at.txt`, sha256 `data/SHA256_raw.txt`; raw GenBank files not committed). Positives: annotated CDS >=150 nt, no internal stops, table 11 (4156/4131/3898). Negatives: shadow ORFs, maximal stop-to-stop >=150 nt in 6 frames, wholly containing no annotated CDS (39,663/31,301/51,375 found), subsampled 1:1 length-matched within 10% (seed 1). Final sets in `data/sets.json`.

## Results (results/results.json)
| method | E. coli CV | B. subtilis CV | M. tb CV | E. coli -> B. sub | E. coli -> M. tb |
|---|---|---|---|---|---|
| GC | 0.409 | 0.410 | 0.416 | - | - |
| GC3 | 0.438 | 0.426 | 0.719 | - | - |
| LEN | 0.504 | 0.504 | 0.505 | - | - |
| DI (aa usage) | 0.994 | 0.995 | 0.956 | 0.993 | 0.996 |
| HEX (hexamer Markov) | 0.781 | 0.800 | 0.846 | 0.791 | 0.849 |
| COMBO (pivot) | 0.998 | 0.999 | 0.977 | 0.997 | 0.996 |

## Gates
- G1 PASS: HEX 0.781 >= best single-feature baseline (LEN 0.504) + 0.05.
- G2 FAIL: HEX 0.781 < 0.90 within E. coli.
- G3 FAIL (transfer): E. coli-trained HEX on B. subtilis 0.791 < 0.85.
- G4 FAIL (boundary): within-M. tb HEX 0.846 < 0.90.
- Original project FAILS its primary gates: hexamer Markov scoring does not meet the bar in the shadow-ORF setting.
- Pivot P1 PASS (0.9981 >= DI-0.001=0.9929), P2 PASS (0.9981 >= 0.98), P3 PASS (0.9964 >= 0.95).

## Caveats
- Real gene finders train negatives on intergenic sequence, not frame-shifted shadows; this setting is deliberately the harder "is this ORF the gene?" decision, and conclusions are scoped to it.
- Stop-codon avoidance itself biases shadow-ORF composition (part of what DI exploits); on genomes with different stop usage the margin may shrink.
- Label noise: mis-annotated/predicted CDS among positives; some shadows may be real unannotated small genes.
- COMBO's cross-genome transfer works because it inherits DI's robustness, not because the GC-sensitive features transfer.

## Reproduce
`python3 code/prep.py && python3 code/run.py && python3 code/pivot.py` (needs biopython, numpy, scikit-learn; ~3 min plus downloads).
