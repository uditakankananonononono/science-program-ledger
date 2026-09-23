# algo50/23 - Disease-gene prioritization on a physical interaction network: RWR vs neighbour counting, with a degree-bias correction

Protocol and gates locked before scoring (PROTOCOL.md, results/lock.txt). Network: STRING v12 human, EXPERIMENTAL channel >= 400 only (no text-mining or curated-database edges), 14,449 genes / 154,594 edges. Disease genes: HPO genes_to_disease, Mendelian, diseases with 5-50 network genes. Leave-one-out: 196 queries over 23 diseases.

## Results (results/metrics.json, results/per_query.tsv)
| method | mean AUROC | hidden gene in top 100 |
|---|---|---|
| Degree only (hub baseline) | 0.652 | 1.5% |
| Direct seed neighbours (DN) | 0.714 | 28.1% |
| RWR, restart 0.7 (Köhler 2008) | 0.807 | 30.1% |
| RWR / uniform-restart RWR (degree-corrected, proposed) | 0.805 | 25.5% |

## Gates
- G1 PASS: RWR beats neighbour counting by +0.093 AUROC (95% CI 0.057 to 0.137). This reproduces Köhler et al. on today's data, with experimental edges only.
- G2 FAIL: top-100 recall +0.020 (CI -0.040 to 0.087). At the very top, RWR is not clearly better than neighbour counting.
- G3 FAIL: the degree correction HURTS top-100 recall (-0.046, CI -0.077 to -0.016).

## What this means
RWR's advantage is real across the whole ranking: it pulls hidden disease genes up from deep in the list, where neighbour counting gives them no signal at all. But it does not clearly improve the short list a person would actually read (top 100). My hub correction, meant to stop RWR favouring well-studied hubs, makes the top of the list worse, so here hubness is partly real signal (disease genes are often well-connected) rather than pure bias. The replication (G1) holds; the new idea (G3) is an honest negative.

## Caveats
- Small evaluation: only 23 diseases have 5-50 Mendelian genes in HPO, and a few large ones dominate (e.g. OMIM:114500 with 21 queries). Several are OMIM susceptibility or phenotypic series, where genes may share pathways more than a typical disease.
- Leave-one-out within a disease can favour methods that exploit complexes.
- Experimental-only edges make the network sparser than full STRING; results with all channels could differ, but would risk leakage.

## Reproduce
Download the three URLs in data/source_url.txt into data/, check sha256, then python3 code/run.py (~2 min)
