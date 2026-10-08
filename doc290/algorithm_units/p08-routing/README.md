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

## V4 turn-constrained routing

Fourth unit: standard incoming-edge state expansion with Dijkstra search.
Explicit forbidden turns and nonnegative transition penalties are keyed by
(source vertex, adjacency index) edge identities. Parallel edges remain distinct.
A vertex may need to be revisited with a different incoming edge; this is covered
by a regression fixture. No anatomical turn rules are guessed.

16 test methods pass. The new unit matches independent exhaustive expanded-state
path enumeration on 100 fixed-seed four-vertex directed graphs, with returned edge
and turn costs also recomputed. Combined with the existing three-unit oracle,
there are 550 objective comparisons. This is correctness testing, not external
validation. No performance, invention or clinical claim is made. This unit does
not yet combine turn constraints with the other units' budget/scenario objectives.

## V5 integrated routing

Fifth unit integrates exposure budgets, common-scenario minimax times and explicit
incoming-edge turn rules. Turn delays are caller-supplied scalars added equally
to every scenario. Exposure remains deterministic and edge-additive. State is
(vertex, incoming edge); Pareto labels retain exposure and all scenario totals.
This composes standard methods, not a demonstrated algorithm invention.

19 test methods pass. Added 150 exact objective comparisons to an independent
expanded-state exhaustive oracle and 150 equivalence checks against the earlier
budgeted-scenario unit when turns are absent. Earlier oracle checks remain:
700 total independent-oracle objective comparisons plus 150 internal equivalence
checks. Returned edge, exposure, scenario and turn totals are recomputed in the
new randomized tests. A fixture requires revisiting a vertex and shows budget
infeasibility when that revisit cannot be afforded.

Scientific data ingestion, physiological calibration, performance evaluation and
prior-art investigation of any proposed invention remain outstanding. Synthetic
correctness checks are not scientific gate completion or medical validation.

## V6 strict JSON runner

Run `python3 runner.py input.json` or pipe JSON to `python3 runner.py -`.
Required fields: method, graph, start, goal. Graph maps vertex strings to lists of
edges with target, time, exposure, and optional scenario_times (number list).
Methods: budget, scenario, budget-scenario, turn, integrated. A budget is required
only for budget, budget-scenario and integrated. Turn rules are accepted only by
turn and integrated. All costs must be finite/nonnegative; no attributes inferred.

Optional forbidden rules: list of pairs of edge IDs. An edge ID is a JSON pair
[source_string, adjacency_index]. Optional penalties: list of objects containing
incoming edge ID, outgoing edge ID, and delay. Duplicate keys/rules, unknown fields,
unsupported parameters and non-standard NaN/Infinity JSON tokens are rejected.

Success or infeasible results are JSON on stdout with exit code 0. The tested
parse/validation/I/O failure classes, including decoder nesting RecursionError,
are JSON on stderr with exit code 2. This is not a guarantee for every possible
process failure. Infeasible is not a crash.
26 test methods pass, including a 1500-level decoder nesting regression and subprocess parsing/output/error checks and all
prior oracle comparisons. Input is loaded into memory; no large-file, security,
physiology or performance validation is claimed. This runner adds usability,
not a sixth optimization algorithm or a scientific discovery.

## V6.2 file-input coverage

30 test methods pass. The new subprocess checks cover a real JSON input file,
FileNotFoundError (missing path), IsADirectoryError (directory path), and invalid
UTF-8 text decoding. These checks exercise specific file/decoder failure classes;
permission failures and other OSError subclasses remain untested. No production
code or optimization-kernel changes in this update.

## V7 binary-mask adjacency ingestion

mask_graph.mask_to_graph builds exact foreground-pixel adjacency for an explicitly
chosen 4- or 8-neighbor binary mask; graph_payload converts it into runner input.
35 test methods pass, including 400 pairwise adjacency oracle checks (200 small
random masks at both connectivities), junction/diagonal cases, bad inputs and an
end-to-end integrated routing fixture on an extracted chain.

This is not skeletonization or a real vessel graph extraction pipeline. Inputs
must already be binary; callers supply all edge costs. Edges are bidirectional
and 8-neighbor diagonal edges use the same supplied cost as orthogonal edges.
No flow, radius, physical spacing, anatomical turn rules or diagonal correction
is inferred. IDs are row,column strings. Foreground absence returns an empty
graph, which cannot satisfy a routing request. Real data ingestion/calibration
and P08 scientific gates remain unpassed. This is another input component,
not an additional optimization algorithm or invention.

## V8 separate mask-file CLI

Run `python3 mask_runner.py input.json` or pipe JSON to `python3 mask_runner.py -`.
Input fields are mask, connectivity, costs and query. Costs require time and
exposure, plus optional scenario_times list. Query uses the graph runner's method,
start, goal and method-specific budget/turn parameters; callers cannot supply a
graph field here. Pixel endpoint IDs are row,column strings chosen by the caller.

mask_to_graph remains a Python API that raises Python exceptions. The separate
mask_runner CLI converts tested parse/schema/extractor/kernel failures into JSON
stderr with exit 2; runner.py remains graph-only and byte-unchanged.
40 test methods pass, including real mask-CLI subprocesses. Empty foreground is
accepted by extraction but missing endpoints fail routing with exit 2. All-isolated
masks retain vertices but scenario routing fails on absent scenario edge count;
scalar budget identity can succeed and disconnected scalar endpoints are infeasible.
Diagonal edges retain caller costs with no correction. A failed initial fixture
incorrectly expected an all-isolated scenario graph to return infeasible; it was
fixed to assert the inherited documented error boundary, without changing kernels.
No universal promise that extracted masks are immediately scenario-routable.
