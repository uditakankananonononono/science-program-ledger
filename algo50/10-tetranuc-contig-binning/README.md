# algo50/10 - Tetranucleotide composition for metagenomic contig binning

Lane RES-2. Algorithm study (not counted toward the flagship 100). Protocol and Amendment 1 each hashed before the results they gate (`results/lock.txt`).

## Bottom line
- Original setting (3 GC-spread genomes, 5 kb contigs): k-mer composition is monotonically better with k (GC 0.928 < K2 0.975 < K3 0.992 < K4 0.997), but the locked margin gates FAIL - with only three genomes this GC-spread, GC alone leaves no headroom for a +0.30 margin. Gate mis-calibration documented, not hidden.
- The informative boundary (Amendment 1): add Shigella flexneri (close E. coli relative, same GC) and GC collapses to 0.691 - but K4 only reaches 0.768, failing the +0.15 margin and 0.90 gates. Composition alone cannot bin close relatives; that needs alignment or marker genes.
- Stability holds: A-half centroids classify B-half contigs at 99.9% of same-half accuracy (G4 PASS); degradation at 1 kb is modest (0.979, G3 PASS).

## Data
NC_000913.3 (E. coli), NC_000964.3 (B. subtilis), NC_000962.3 (M. tuberculosis), NC_004741 (S. flexneri, added under Amendment 1 after its lock). GenBank via NCBI efetch; sha256 in `data/SHA256_raw.txt`; raw files not committed (fetch by accession). Non-overlapping 5 kb and 1 kb contigs; alternating A/B halves.

## Results
3 genomes (results/results.json):
| method | 5 kb | 1 kb |
|---|---|---|
| GC | 0.928 | 0.865 |
| K2 | 0.975 | 0.904 |
| K3 | 0.992 | 0.960 |
| K4 | 0.997 | 0.979 |

4 genomes with S. flexneri, 5 kb (results/pivot_metrics.json): GC 0.691, K2 0.747, K3 0.768, K4 0.768.

## Gates
- G1 FAIL: K4 0.997 < GC 0.928 + 0.30 (margin impossible at this ceiling).
- G2 FAIL: K4 0.997 < K2 0.975 + 0.10.
- G3 PASS: 1 kb K4 0.979 >= 0.70.
- G4 PASS: cross-half / same-half = 0.9992 >= 0.95.
- Pivot: P1 PASS (GC 0.691 <= 0.75), P2 FAIL (K4 0.768 < 0.841), P3 FAIL (0.768 < 0.90).

Original project FAILS its primary gates; pivot FAILS P2/P3. Documented boundary: TETRA is best-in-class among composition features but composition tops out ~0.77 on close-relative 4-way binning.

## Caveats
- Clean single-genome fragments, no assembly error or strain mixture; real metagenomes are harder.
- 3-genome setting is GC-confounded by design (noted in protocol); the 4-genome setting is the honest one.
- Shigella genome contains a few non-ACGT IUPAC bases; k-mers containing them are skipped.

## Reproduce
`python3 code/run.py && python3 code/pivot.py` (needs biopython, numpy; ~3 min).
