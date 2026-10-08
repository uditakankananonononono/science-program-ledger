# B2 actual contiguous-pipeline development timing

Fifteen fresh workers (five per mask) passed correctness on the unchanged B1 ten-query lists. Artificial time=1, exposure=0, scenarios=(1,2). Named comparator is heap Dijkstra; candidate wall timing includes aggregation plus all ten queries/expansions. Shared pixel-graph build is excluded from both.

| Dataset | Baseline median s | Actual candidate pipeline median s | Observed reduction |
|---|---:|---:|---:|
| HRF | 1.396239 | 1.164210 | 16.618% |
| FIVES | 0.316883 | 0.279156 | 11.905% |
| FOVEA | 0.145025 | 0.133029 | 8.272% |

Recorded deltas are single-environment OBSERVATIONS, not reproducible magnitude, and no statistical or stable superiority claim survives. B1 FOVEA originally recorded 10.417% reduction; independent review rerun was 1.103%. B2 here records 8.272% under a different actual-pipeline measurement protocol. These are not interchangeable samples or evidence that instability was fixed.

Only one development mask per source, ten farthest-anchor queries from one lexical source. Proportional scenarios reduce to shortest steps. NOT difficult minimax, physiology, novelty or arbitrary-workload superiority. No RAM cap; no performance ceiling. Query correctness checked after each timed pipeline. Freeze/harness commits precede this recorded run, but history does not prove no private pre-freeze experiment. Raw samples retained; no post-freeze tuning.
