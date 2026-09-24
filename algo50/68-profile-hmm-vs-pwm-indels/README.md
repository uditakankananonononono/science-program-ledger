# algo50/68 - Profile HMM vs PWM: the indel regime where HMMs should win

Lane RES-2. Algorithm study. Protocol + Amendment 1 hashed before the results they gate (`results/lock.txt`). Topic lane-chosen (no list past 55). Extends algo50/24.

## Bottom line
The textbook "profile HMMs beat PWMs when instances have indels" survives only weakly: the HMM's AUROC edge was <= +0.03 and non-monotone across indel rates 0-0.10 in both designs. Two robust findings instead: (1) detectability is information-limited before it is model-limited - a 7.7-bit motif in 400 bp caps BOTH scorers at ~0.72 AUROC, an 11.6-bit motif in 200 bp caps at ~0.85; (2) the HMM never loses materially and gains most at mid indel rates (+0.028 at r=0.05). At r=0.10 both degrade together (emission evidence lost, not alignment flexibility).

## Gates
- Original (seed 37, 12-mer/400bp): G1-G3 FAIL, G4 PASS - but all four AUROCs ~0.7 because the design is information-starved (7.7 bits < log2(400)=8.6); gates unreachable by ANY scorer. Pre-scoring bug fixed+documented: HMM free-start initialization.
- Amendment 1 (seed 41, 18-mer/200bp): P1 FAIL (PWM 0.89 < 0.95), P2 FAIL (gap -0.038/+0.012/+0.028/-0.005, not monotone), P3 FAIL (both ~0.80 at r=0.10).
Net: documented negative on a clean HMM advantage; robust information-limit finding.

## Caveats
- 150 pos/150 neg per cell: AUROC noise ~+-0.02-0.03, same magnitude as the HMM edge - a larger study might resolve a small consistent gain.
- Plan7-lite transitions hand-set, not Baum-Welch trained; trained transitions might help slightly.

## Reproduce
`python3 code/run.py` (seed 37) and `python3 code/pivot.py` (seed 41); numpy only, ~2 min each.
