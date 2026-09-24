# algo50/10 - AMENDMENT 1: close-relative setting where GC must fail

Locked after the original gates were scored (G1, G2 FAIL - GC already at 0.928 with three GC-spread genomes makes a +0.30 margin mathematically near-impossible; K4 still monotonically best), before the new 4-genome results are computed. Original gates stand.

## Change
Add Shigella flexneri 2a str. 301, NC_004741 (~4.6 Mb, GC ~51%, a very close E. coli relative) as a fourth genome. Same 5 kb fragmentation, same A/B halves, same methods (GC, K2, K3, K4, TETRA-style z + correlation). New data fetched after this lock.

## Gates (locked)
- P1: 5 kb GC accuracy on the 4-genome set <= 0.75 (GC collapses on close relatives).
- P2: 5 kb K4 accuracy >= GC accuracy + 0.15 on the 4-genome set.
- P3: 5 kb K4 accuracy >= 0.90 on the 4-genome set.
Pivot PASSES if P2 and P3 pass; P1 is the mechanism check.
