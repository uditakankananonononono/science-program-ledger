# algo50/28 - Palindromic hexamer and restriction-site depletion across four bacterial genomes

Lane RES-2. Algorithm study. Protocol + Amendment 1 hashed before the results they gate (`results/lock.txt`).

## Bottom line
- Under a naive order-1 (dinucleotide) null the picture is muddy and partly artifactual: palindromes look depleted only in E. coli/Shigella (o/e ~0.76), and M. tuberculosis looks restriction-site ENRICHED (1.44) - but the null itself fails (median |o/e-1| ~0.35 on non-palindromes; G4 FAIL).
- Under an order-2 (trinucleotide) null - adequate everywhere (P1 PASS, |o/e-1| 0.14-0.19) - palindrome depletion is real in 3/4 genomes (0.64/0.65/0.84; mtb 0.94), restriction sites are depleted BEYOND other palindromes in the same 3/4 (most strongly E. coli/Shigella: ~0.45 vs ~0.67), and the mtb "enrichment" disappears: it was a null-model artifact.
- Genome-specificity stands: depletion strength tracks E. coli ~ Shigella > B. subtilis > M. tuberculosis, consistent with differing RM-system histories.

## Data
NC_000913.3, NC_004741, NC_000964.3, NC_000962.3 (sha256 `data/SHA256_raw.txt`). All 4096 6-mers, order-1 and order-2 Markov expectations; 10 common type-II restriction sites vs 54 other palindromes.

## Gates
- Original (order-1 null): G1 FAIL (2/4 depleted), G2 PASS (3/4 RS-specific), G3 FAIL (mtb reversed - later shown artifact), G4 FAIL (null inadequate).
- Pivot (order-2 null): P1 PASS, P2 PASS (3/4), P3 PASS (3/4).

Original FAILS G1/G3/G4 with G2 PASS; pivot PASSES fully. Net: restriction avoidance is real but genome-specific, and the choice of sequence null can reverse the apparent direction in GC-extreme genomes.

## Caveats
- Forward-strand counting (palindromes are revcomp-symmetric; non-palindromes compared on the same basis).
- The 10 restriction enzymes are mostly absent from these genomes; "avoidance of foreign sites" is the mechanism proposed, not demonstrated here.
- Order-2 null still ignores codon-frame periodicity beyond two bases; an order-3/codon null might erase more of the "palindrome" effect (it shrank from 0.76 to 0.64-0.84 medians when the null improved - some of the order-1 "depletion" was null failure too).

## Reproduce
`python3 code/run.py` then the order-2 block (in git history of `code/run.py`; needs biopython, numpy; ~1 min).
