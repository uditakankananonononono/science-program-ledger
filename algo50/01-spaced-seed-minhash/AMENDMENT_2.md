# Amendment 2 - is the loss from the alphabet or from sketching? (locked before these results were computed)

## Outcome of Amendment 1 (not re-scored)
A1 FAIL (Cascade RA-SP 0.870 at k=50, needed 0.8811), A2 FAIL (both RA-SP and MH3 first reach 0.8811 at k=100), A3 FAIL (twilight 0.729 at k=50, needed 0.803).
Observation driving the pivot: the unsketched plain 3-mer Jaccard (K3) was the best prefilter at every k, beating the 256-hash MinHash of the same 3-mers (MH3) by 3-7 points. That points at bottom-s subsampling, not alphabet design, as the dominant loss.

## New direction
Remove the sketch. Compare exact Jaccard over the RA-SP feature set (Murphy-10, seeds 11011+1101011) against exact plain 3-mers (K3) as a prefilter, and quantify how much accuracy the 256-hash sketch costs.

New methods: RA-SP-X (exact Jaccard, RA-SP features); descriptive only: MH3-1024 and RA-SP-1024 (s=1024).

## Gates
- B1: Cascade(RA-SP-X) reaches >= 0.8811 (0.95 x SW) at some k <= 30.
- B2: Cascade(RA-SP-X) twilight accuracy at k=50 >= Cascade(K3) twilight at k=50 + 5 points (>= 0.790).
- B3 (mechanism): exact RA-SP-X 1-NN accuracy exceeds RA-SP (s=256) 1-NN accuracy by >= 3 points with McNemar p < 0.05.
