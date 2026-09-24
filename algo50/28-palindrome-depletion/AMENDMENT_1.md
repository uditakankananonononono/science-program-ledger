# algo50/28 - AMENDMENT 1: order-2 (trinucleotide) null

Locked after original scoring (G1 FAIL - palindrome depletion in 2/4 genomes only; G2 PASS - restriction sites specifically depleted in 3/4, REVERSED in M. tb (o/e 1.44); G3 FAIL; G4 FAIL - the order-1 dinucleotide null is inadequate even for non-palindromes, median |o/e-1| ~0.35, presumably from coding-frame trinucleotide structure), before order-2-null results are inspected.

## Method
Same counts; expected from order-2 Markov: P(s) = f2(s1s2) prod P(b_{i+1} | b_{i-1} b_i), frequencies from each genome.

## Gates (locked)
- P1: under the order-2 null, non-palindromic 6-mer median |o/e - 1| < 0.2 in 4/4 genomes (null adequacy).
- P2: under the order-2 null, palindrome median o/e < 0.9 in >= 3/4 genomes.
- P3: restriction-site median o/e < other-palindrome median o/e in >= 3/4 under the order-2 null.
Pivot PASSES if P1+P2 pass.
