# P08-B1 frozen software benchmark protocol

Question: does degree-two chain preprocessing amortize for repeated anchor-only
shortest-step queries on these three development skeletons versus heap Dijkstra
on the uncompressed pixel graph? No algorithmic novelty or medical claim.

Inputs: the exact full skeleton bool hashes in
 data_audit/three_first_mask_unit_cost_routes.json (HRF/FIVES/FOVEA).
Versions: numpy 2.2.6, scipy 1.15.3, skimage 0.25.2, Pillow 12.3.0.
Masks are development, not fresh validation. No new data selection after scores.

Comparator: independent standard heap-based Dijkstra, unit positive edge costs,
original graph adjacency, early-stop at goal. Candidate: aggregate_chains once,
then exposure_budget_route on compressed Edge graph with budget 0 and witness
expansion. Artificial costs time=1, exposure=0, scenarios=(1,2). Primary task is
scalar shortest steps, NOT difficult scenario minimax, physiology or superiority.

Queries: lexical first anchor as source; all reachable other anchors ordered by
coordinate BFS distance descending, lexical descending for equal distances;
first ten targets, or all if fewer. Query selection uses topology only. One fixed
query set per mask, never changed after timing. BFS supplies objective oracle.

Timing: one warm-up per implementation/query, then five serial repetitions,
alternating implementation order by repetition. Record each raw query wall time,
including path reconstruction/expansion. Candidate preprocessing measured once
per each of five repetitions, retaining raw values; original graph creation is
shared and excluded from both query timings. Median reported, no confidence or
stable resource ceiling claims. No concurrency. No RAM measurement claim.

Correctness gate: every query result equals independent coordinate BFS steps and
valid original pixel adjacency. On any mismatch, preserve result and report FAIL,
do not report speedup for that dataset. No silent timeout/mismatch removal.

Runtime report: baseline vs candidate median query totals, candidate preprocessing,
candidate preprocessing+query totals, and amortization at these ten queries only.
Losses and preprocessing penalties reported. No projected workloads or break-even
claims unless supported by the actual observed fixed queries. One small benchmark
is not arbitrary-graph proof or external validation. No tuning after scoring.

Execution constraint: each mask is evaluated in a fresh subprocess, 90-second
wall timeout. Timeout counts as a retained benchmark failure, not a dropped mask.
This is a time cap, not a RAM cap. Exact implementation and input hashes must be
recorded before running. Any subsequent changes are separately labeled reruns.
