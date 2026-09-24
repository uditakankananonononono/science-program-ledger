# algo50/62 - Local (SW) vs global (NW): what local alignment actually buys

Lane RES-2. Algorithm study. Protocol + 2 amendments hashed before the results they gate (`results/lock.txt`). Topic lane-chosen (no list past 55).

## Bottom line
Against length-matched nulls, local and global alignment have nearly IDENTICAL detection power for an embedded domain (F=1000, 80% identity: SW 0.43 vs NW 0.37 detected) - the null score distribution shifts up with sequence length for both, swallowing the domain's ~100-point contribution; detection collapses for both as flanks grow (17% at 60% identity, F=1000). What local alignment actually buys is LOCALIZATION: SW traceback recovers >=50% of the true 60 bp domain in 30/30 pairs (median 100% coverage) even at F=1000, while NW's forced full-length alignment has 2.9% domain precision by construction. Detection vs localization is the real distinction - the original detection-framed gates (G2, G3) failed because the premise was wrong.

## Gates
- Original: G1 PASS (SW>=NW on all 540 pairs; sanity 120=120), G2 FAIL (SW detection 0.43 at F=1000), G3 FAIL (NW 0.37 - no dilution difference), G4 PASS (null FPR 0.033-0.067).
- Amendment 1: compute-budget vectorization + reduced N (locked; thresholds unchanged).
- Amendment 2 (localization pivot): P1 PASS (30/30 both identities), P2 informational.
Original FAILS G2+G3 with a documented false premise; pivot PASSES and states the corrected claim.

## Caveats
- Linear gap penalty +2/-1/-2 only; affine gaps change flank costs.
- E-value-style length-corrected statistics (what BLAST actually uses) would change detection conclusions - not tested here; that is the natural follow-up.

## Reproduce
`python3 code/run2.py && python3 code/pivot.py` (numpy; ~2.5 min).
