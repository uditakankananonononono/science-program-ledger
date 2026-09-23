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
