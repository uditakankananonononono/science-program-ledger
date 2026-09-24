# 86 - EM transcript quantification (kallisto-lite)

**Bottom line: all gates PASS.** EM over k=31 equivalence classes recovers simulated abundances tightly: Spearman rho 0.976 at 200k reads, median |log2 error| 0.23, and isoforms with >=30% unique k-mers attributed within 2x (max 0.83 log2). Error already saturates at 50k reads (0.240 -> 0.232 -> 0.231): residual error is isoform-sharing ambiguity, not sampling noise - more depth does not help.

## Data
Simulated, seeds 86/861/862/863. 200 transcripts (10 isoform pairs sharing a 400bp constitutive region, 180 singletons), geometric abundances (p=0.15), 75bp reads at 1% substitution, depths 50k/200k/800k.

## Method
k-mer (k=31) index; read equivalence class from 3 evenly-spaced k-mers; EM 100 iterations on class counts with length-weighted redistribution.

## Gates (locked in results/lock.txt before scoring)
| Gate | Expectation | Result | Verdict |
|---|---|---|---|
| G1 | Spearman rho >= 0.95 @200k | 0.976 | PASS |
| G2 | median \|log2 err\| <= 0.5 @200k (>=50 expected reads) | 0.232 | PASS |
| G3 | isoforms with unique-kmer frac >= 0.3: \|log2 err\| <= 1.0 | max 0.83 | PASS |
| G4 | G2 error non-increasing 50k->200k->800k | 0.240/0.232/0.231 | PASS |

## Caveats
- Boundary documented: error saturates by 50k reads; isoform ambiguity (shared 400bp) is the irreducible term. Depth cannot fix what sequence sharing removes.
- Random-sequence transcripts are easier than real transcriptomes (paralogs, repeats); rho would drop with real gene families.
- 3-k-mer class calls discard ~unmappable reads silently; multi-mapping beyond the simulated pairs not stress-tested.

## Reproduce
python3 code/run.py  (seeds 86/861/862/863, ~90s)
