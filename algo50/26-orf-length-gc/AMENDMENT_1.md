# algo50/26 - AMENDMENT 1: dinucleotide-corrected stop probability

Locked after original scoring (G1 FAIL - iid model underpredicts ORF length by 13-27%, worst at extreme GC (mtb 1.27, gate 1.25); G2 PASS; G3 FAIL trivially - the 04 negative set is CDS-length-matched by construction, a documented bias that voids the bracket test), before corrected results are inspected.

## Method
Same genomes. P_stop computed from dinucleotide conditionals: P(xyz) = P(xy)*P(yz)/P(y) with genome-observed di- and mononucleotide frequencies. Everything else unchanged.

## Gates (locked)
- P1: dinucleotide-corrected |observed/predicted - 1| <= 0.25 for all four genomes.
- P2: corrected M.tb/E. coli predicted ratio within +/-15% of observed ratio.
- P3 (supersedes voided G3): freshly enumerated shadow ORFs (as in algo50/04, no length matching) mean length within [0.5x, 2x] of the corrected prediction, 4/4 genomes.
Pivot PASSES if P1 and P2 pass.
