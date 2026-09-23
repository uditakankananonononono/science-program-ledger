# DOC-2-099 The Discovery Graph of Biology - locked gates (21:54 IST, before v12 download)

## Sandbox-fit slice
Full multimodal KG (OpenAlex+UniProt+Reactome+ENCODE+HCA+ClinVar) does not fit 1 GB. Slice: time-split link recovery on the human protein association graph. Old evidence = STRING v11.0 (Jan 2019); later discoveries = STRING v12.0 (2023) edges.

## Question
Do graph paths in the 2019 graph recover protein-protein associations that were only established later - beyond trivial degree effects?

## Protocol
Nodes mapped between versions by preferred_name (gene symbol) via protein.info files; unmapped dropped.
Old graph G11: combined_score >= 700.
Positives: pairs with v12 combined >= 700 whose both genes exist in G11 and whose v11 combined score was < 400 (absent or weak in 2019). Sample 5000 (seed 0).
Negatives A: 5000 random gene pairs absent from v12 at >= 400. Negatives B: degree-matched - for each positive, a pair (u, w) keeping u and choosing w with G11 degree within +/-10% of v, absent from v12 at >= 400.
Scores: Adamic-Adar (AA) and common neighbours on G11; baseline preferential attachment (PA = deg u * deg v).
## Gates
G1 AA AUROC vs negatives A >= 0.80 AND exceeds PA by >= 0.05.
G2 AA AUROC vs degree-matched negatives B >= 0.70.
G3 Precision among top-decile AA pairs (pos vs B pooled) >= 0.70.
Failure policy: negative preserved; pivots appended with new locked gates before computation.

## Primary result (21:54) - FAIL, preserved
AA AUROC vs random negatives 0.753 (< 0.80) and equals preferential attachment 0.750 (G1 fail). AA vs degree-matched negatives 0.699 (G2 fail by 0.001 - reported as fail, gates are not rounded). G3 pass: top-decile AA precision 0.883 vs degree-matched negatives. 45% of later-discovered edges had zero common neighbours in the 2019 graph (vs 81% of degree-matched non-edges).

## Pivot 1 (locked 21:56, before computation): sub-threshold "whispers"
Hypothesis: later-established associations were already present in 2019 as weak (150-399) STRING v11 evidence, invisible to thresholded graph paths.
Same positives and degree-matched negatives B (same seeds, regenerated identically).
Feature W = v11 combined score for the pair (0 if < 150/absent).
P1-G1 W alone AUROC vs B >= 0.75.
P1-G2 logistic(AA, W), 5-fold CV, AUROC vs B >= 0.80 and >= AA alone + 0.05.
P1-G3 fraction of positives with W >= 150 at least 2x that of negatives B.

## Pivot 1 result (21:56) - FAIL on locked gates, preserved
W alone AUROC vs B 0.721 (< 0.75, fail). logistic(AA, W) 0.781 (< 0.80, fail; it does beat AA alone by 0.08). G3 pass: 48.3% of later-established pairs had v11 evidence >= 150 vs 5.3% of degree-matched non-pairs (9.2x). 31% of the path-invisible positives (zero common neighbours) had a whisper.

## Pivot 2 (locked 21:58, before computation): realistic-base-rate discovery yield
AUROC on balanced samples does not match how a hypothesis list is used. New question: ranking ALL 2019 sub-threshold pairs (v11 combined 150-399, both genes in G11), what fraction of the top of the list became high-confidence (v12 >= 700) by 2023?
Pre-declared score S = (W/1000) * (1 + AA). Comparators: W alone, AA alone, random pool member (base rate).
P2-G1 yield in top 1000 by S >= 0.20.
P2-G2 >= 5x the pool base rate.
P2-G3 S top-1000 yield >= 1.5x both W-alone and AA-alone top-1000 yields.
Ties are broken by random jitter (seed 0).

## Pivot 2 result (21:57) - FAIL on P2-G1, preserved
Pool 3.98M sub-threshold 2019 pairs, base rate 0.31% became v12 >= 700. Top-1000 yield by S = 4.6% (< 20%, fail); 15.1x base (pass); vs W-alone 2.4% and AA-alone 2.0% = 1.9x / 2.3x (pass). Top-10,000: S 3.96%, W 1.6%, AA 2.7%.
Closing decision: after two pivots on the same time split, further pivots on this data would be fishing. Topic closed as a documented boundary.
