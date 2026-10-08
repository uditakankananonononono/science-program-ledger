# Frozen B1 development software benchmark

All three fixed masks passed objective/expanded-adjacency checks for ten deterministic anchor targets, five timed repetitions. Unit costs only; this is not a novel algorithm, medical finding, difficult scenario-minimax task or external validation.

| Mask | Baseline ten-query median s | Candidate query median s | Candidate preprocess+query median s | End-to-end reduction |
|---|---:|---:|---:|---:|
| HRF | 1.420013 | 0.123444 | 1.105319 | 22.2% |
| FIVES | 0.339442 | 0.036695 | 0.275211 | 18.9% |
| FOVEA | 0.136132 | 0.021578 | 0.121951 | 10.4% |

Named comparator: independent heap Dijkstra on uncompressed pixel graph. Candidate: existing chain aggregation and scalar budget solver with expansion. No post-freeze tuning. Baseline and candidate share graph construction; candidate preprocessing is included in the final column. Query medians alone exclude that cost. No losses observed on these three ten-query workloads; that does not predict other workloads.

Timing samples are serial local observations, not confidence intervals or statistical superiority. Lexical first anchor and farthest-ten targets bias workload toward long paths by the pre-frozen design. No single-query, random-endpoint, interior-endpoint, turn-rule, nonuniform-cost or adversarial-frontier claims. Whole-graph creation memory not measured/capped.

Source skeleton hashes in RESULTS.json. Full originals and skeleton pixels delivered previously for independent reproduction. All data exposed development. Frozen protocol and implementation commits precede this scoring run; any later changes require a labeled rerun.

## Independent rerun and instability

Independent review reports a fresh-worker FOVEA rerun on the exact frozen ten
queries: baseline 0.142817s versus paired preprocessing+query 0.141242s, a 1.103%
reduction, NOT the recorded 10.417% reduction. Correctness gates still passed.
The performance delta is NOT stable across environments. Recorded deltas are
single-environment OBSERVATIONS, not reproducible magnitude; no statistical or
stable superiority claim survives. The artifact is a reproducible protocol and
record, not a validated performance win. Independent numbers are review-reported,
not a replacement for the original run. Five upfront preprocessing timings paired
arithmetically with query timings estimate amortization, not a wall-timed pipeline.
Git history proves protocol/harness/result ordering; it cannot prove no private
scoring ever occurred before freeze.
