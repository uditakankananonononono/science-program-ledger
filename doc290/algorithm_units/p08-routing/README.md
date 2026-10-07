# P08-01 routing implementation units

Status: three executable local algorithm units, not an invention or a validated
medical navigation system. All implement standard Pareto-label search. Neither
claims to improve a published baseline.

## Units added

1. Exposure-budget routing: minimum additive travel time on a directed graph,
   subject to a hard cumulative exposure budget.
2. Common-scenario robust routing: minimize the maximum *whole-path* travel
   time across supplied scenarios, preserving scenario correlation across edges.
   This differs from summing each edge's individual worst case.

All three return a concrete route and cost totals, return None for infeasible routing,
and reject malformed, negative or nonfinite edge costs. Zero-cost cycles do not
create unlimited duplicate labels. Pareto frontiers can grow exponentially.

3. Budgeted scenario routing: minimum worst-scenario total time subject to a
   deterministic cumulative exposure budget. This joint unit is also standard
   Pareto labeling, not a new algorithm.

See PRIOR_ART.md for the fetched literature screen.

## Reproduce

From this directory, run `python3 -m unittest -v`.
No third-party dependencies, downloads, credentials or GPU are needed.

## Verified locally

Six test methods passed. The randomized oracle test checks each algorithm against
independent exhaustive simple-path enumeration on 150 six-vertex directed graphs
with a fixed seed, including cyclic graphs: 450 objective comparisons. Additional
fixtures cover budget tradeoffs, correlated scenarios, zero-cost cycles,
unreachable vertices, identical source/destination, and invalid inputs.

These are synthetic SOFTWARE CORRECTNESS fixtures, not biological data or
external validation. Exact comparisons here use small integer costs. Floating
point tolerance, scalability and real anatomical segmentation ingestion are not
validated. Scenario values and exposure units must be supplied, never inferred
from the anatomy or treated as physiological evidence.

## Remaining work

Real public vessel-segmentation ingestion and graph extraction, calibration of
edge attributes, held-out anatomy evaluation, runtime/frontier growth measurement,
and a frozen comparison with published algorithms remain unbuilt. The parent
spec's G1-G4 gates are not passed by these unit tests. Before presenting any
algorithm variant as an invention, perform and record a prior-art review and
freeze the exact baseline and evaluation protocol.

## V3 correctness hardening

11 test methods pass, retaining the 450 small-graph oracle comparisons.
Returned routes now include source vertex and adjacency-list edge index for each
step, so parallel edges can be distinguished and cost totals independently
recomputed. Vertex IDs must be strings; edges must be Edge objects with tuple
scenario costs. Accumulated floating-point overflow raises OverflowError rather
than silently returning infinite costs. This is fail-fast behavior: even an
irrelevant overflowing explored branch can abort the search.

Numerics are explicit binary-float semantics, not exact decimal arithmetic:
0.1 + 0.2 exceeds a budget of 0.3. No tolerance is silently applied. The decimal
boundary fixture tests and documents this limitation. For exact budgets, use
integer-scaled costs. Empty graphs with no scenario-bearing edges remain rejected
by scenario solvers, including identity queries, because scenario count is absent.
