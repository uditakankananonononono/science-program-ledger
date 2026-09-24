# algo50/28 - Palindromic hexamer and restriction-site depletion across four bacterial genomes

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study.

## Question
Bacterial genomes are reported to avoid restriction-enzyme recognition sites (and palindromes generally) - "restriction avoidance". Quantify observed/expected for palindromic vs non-palindromic 6-mers under a dinucleotide null, across 4 genomes (E. coli, S. flexneri, B. subtilis, M. tuberculosis), and whether 10 common type-II restriction sites (EcoRI GAATTC, BamHI GGATCC, HindIII AAGCTT, PstI CTGCAG, EcoRV GATATC, KpnI GGTACC, SacI GAGCTC, SalI GTCGAC, XbaI TCTAGA, SphI GCATGC) are MORE depleted than other palindromes.

## Data
Same four GenBank genomes as algo50/26 (sha256 in data/).

## Methods
- Counts of all canonical 6-mers (forward count, both strands equivalent for palindromes; non-palindromes counted as canonical min(s,revcomp) and halved... locked simplification: count forward strand only; palindromes are their own revcomp so counts are comparable per-instance).
- Expected: dinucleotide Markov (order-1) estimate per 6-mer: P = f(b1) prod P(b_{i+1}|b_i), times (genome length - 5).
- o/e per 6-mer; compare distributions: palindromic (32 canonical... 4^6/... forward-strand palindromes = 4^3=64) vs non-palindromic; and the 10 restriction sites vs the other 54 palindromes.

## Gates
- G1: median o/e of palindromic 6-mers < 0.9 in >= 3 of 4 genomes (general palindrome avoidance).
- G2: median o/e of the 10 restriction sites < median o/e of other palindromes in >= 3 of 4 genomes (restriction-site-specific avoidance).
- G3: M. tuberculosis (different RM systems) shows the same direction (boundary, not gated as pass criterion).
- G4: control - non-palindromic 6-mers: median |o/e - 1| < 0.2 (dinucleotide null is adequate for non-palindromes).
PASS if G1+G2; G3/G4 boundary/control.

## Failure policy
Negatives preserved; pivots via locked amendments.

## Notes locked in advance
- The restriction sites' enzymes are mostly NOT present in these four genomes; avoidance of "foreign" RM sites is the interesting direction, absence of effect is a fine negative.
- Codon usage drives hexamer frequencies; the dinucleotide null does not model coding frame - documented limitation.
