# DOC-2-099 The Discovery Graph of Biology - sandbox slice (exp200/199)

**Outcome: documented boundary. Primary and both pivots failed at least one locked gate. Not counted as a pass.**

## Setup
Time-split link recovery on the human protein association graph. Old evidence: STRING v11.0 (Jan 2019). Later discoveries: STRING v12.0 edges at >= 700 whose 2019 score was < 400. 17,999 genes mapped by symbol, 25,469 later-discovered pairs.

## Results
| Test (gates locked in advance) | Result | Gate |
|---|---|---|
| Primary: Adamic-Adar vs random pairs | AUROC 0.753, same as preferential attachment 0.750 | fail (needed >= 0.80 and +0.05 over PA) |
| Primary: AA vs degree-matched pairs | 0.699 | fail (>= 0.70) |
| Primary: top-decile precision, degree-matched | 0.883 | pass |
| Pivot 1: 2019 sub-threshold score W alone | 0.721 | fail (>= 0.75) |
| Pivot 1: AA + W | 0.781 | fail (>= 0.80) |
| Pivot 1: whisper enrichment | 48.3% vs 5.3% (9.2x) | pass |
| Pivot 2: top-1000 yield from 3.98M candidate pairs | 4.6% (15x the 0.31% base rate; 1.9-2.3x either signal alone) | fail on absolute yield (>= 20%) |

## What is useful from the failure
1. **Graph paths mostly measure hub-ness.** On random pairs, 2019 path scores do no better than degree product. Once degree is controlled, they lose most of their power (0.70). Any "the knowledge graph predicts discoveries" claim that is not degree-matched is inflated. This is a concrete check for hypothesis-generation benchmarks.
2. **Nearly half of later discoveries were already whispered.** 48% of pairs that became high-confidence by 2023 had weak (150-399) evidence in 2019, vs 5% of matched non-pairs. 45% had no common neighbour at all, so path-based methods cannot see them in principle. Weak evidence and paths catch different discoveries.
3. **The realistic ceiling.** Ranking all 4M weak 2019 pairs gives about 4-5% yield at the top of the list: 15x chance, but most suggestions are still wrong. That is the honest number to quote for this kind of hypothesis engine.

## Limits
- STRING is a curated aggregate. v12 edges reflect new data plus method changes (new channels, scoring), not only new biology.
- Mapping is by symbol.
- This is a single graph type, not the multimodal graph the topic proposes.

## Reproduce
python3 code/run.py; python3 code/pivot1.py; python3 code/pivot2.py. Data URLs are in GATES.md.
