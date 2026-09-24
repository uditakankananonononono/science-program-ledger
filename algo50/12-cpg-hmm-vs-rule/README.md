# algo50/12 - Two-state dinucleotide HMM vs the Gardiner-Garden window rule for CpG islands

Lane RES-2. Algorithm study (not counted toward the flagship 100). Protocol and Amendment 1 each hashed before the results they gate (`results/lock.txt`).

## Bottom line
- The 2-state dinucleotide HMM improves window-level F1 over the Gardiner-Garden rule (0.639 vs 0.565) but misses the locked +0.10 margin, and it over-segments badly (median call 201 bp vs annotated 710 bp). Original primary gates FAIL.
- The window LLR alone (no segmentation) exactly ties the rule (F1 0.563) - segmentation, not better scoring, is where the HMM's gain comes from.
- Pivot (Amendment 1, all gates PASS): trivial length-aware post-processing (merge gaps <200 bp, drop segments <200 bp) lifts F1 to 0.684 (+0.119 over the rule) and fixes segment lengths (median 439 bp, within [0.5x, 2x] of annotated), with island-level recall still 1.0.
- Circularity caveat (locked in the protocol): UCSC cpgIslandExt labels are themselves rule-derived, so all methods are partly graded against the rule's own definition.

## Data
Human chr22 (hg38, NC_000022.11) 20-22 Mb via NCBI efetch FASTA; UCSC hg38 cpgIslandExt track (68 islands in region). Timestamp `data/retrieved_at.txt`, sha256 `data/SHA256_raw.txt`; raw files not committed (re-fetch by the URLs in PROTOCOL.md/code). First 1 Mb trains emissions/transitions; second 1 Mb is the test bed; 200 bp windows every 100 bp.

## Results (results/results.json, results/pivot_metrics.json)
| method | window F1 | precision | recall | island recall | median segment |
|---|---|---|---|---|---|
| RULE (GC>=0.5, o/e>=0.6) | 0.565 | 0.418 | 0.874 | - | - |
| LLR (window dinucleotide LLR>0) | 0.563 | 0.403 | 0.935 | - | - |
| HMM (2-state Viterbi) | 0.639 | 0.480 | 0.956 | 1.000 (34/34) | 201 bp |
| HMM-PP (pivot) | 0.684 | 0.532 | 0.959 | 1.000 | 439 bp |

## Gates
- G1 FAIL: HMM 0.639 < RULE 0.565 + 0.10.
- G2 PASS: island recall 1.000 >= 0.70.
- G3 FAIL: LLR 0.563 < RULE + 0.05 (exact tie with the rule).
- G4 FAIL: median segment 201 bp < 0.5x annotated 710 bp.
- Pivot: P1 PASS (0.684 >= 0.665), P2 PASS (439 in [355, 1419]), P3 PASS (recall 1.0).

Original project FAILS G1/G3/G4; pivot PASSES. Net claim: a dinucleotide HMM plus length cleanup beats the classic rule; the HMM alone without length discipline does not.

## Caveats
- Labels are rule-derived (circularity, locked in protocol): an independent label set (unmethylated domains, promoter annotation) could change the ranking.
- One 2 Mb region of gene-rich chr22; no cross-region transfer tested.
- Development note: the first HMM run had a state/transition index mismatch (island columns crossed); it decoded 94% of sequence as island and was fixed before gate scoring - the scored numbers come from the corrected decoder only.

## Reproduce
`python3 code/run.py && python3 code/pivot.py` (needs numpy; ~1 min plus downloads).
