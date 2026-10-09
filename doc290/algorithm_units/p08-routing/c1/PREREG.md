# C1 checked integer chain-route expansion

Parent f78cff383918ea4044a88cd3542b224faac8bd6e. Documented README gap: anchor-only
and turn-free preconditions not enforced for arbitrary expand_route results.
Existing float regrouping counterexample retained, no repair/equivalence claim.
New validator checks representation and supplied route, NOT optimality/infeasibility.

## Input and independent checks

Fixed JSON statement: original graph adjacency lists of target/time/exposure/
scenario_times, supplied compressed graph same format, supplied witness paths keyed
by compressed source/list-index, start, goal, budget, forbidden, penalties, route.
Route normalized keys path, edges (source/edge_index/target), time, exposure,
scenario_totals,worst_time. Explicit integer costs only (type int, not bool),
nonnegative <=2^53-1; accumulated totals <=2^53-1. Scenario count homogeneous
positive1..4; graph verticesstrings, <=32vertices/128directededges; path<=256steps.
Original topology reciprocal simple adjacency, no self/parallel originals; directed
costs may be asymmetric. Compressed parallel/self edges allowed. Budget nonnegative
integer. Turns forbidden/penalties MUSTempty, never ignored or inferred. No float
costs, anatomy, radius, physical edge length, calibration or interpolation inferred.
Strict UTF8 JSON128KiB/depth10/duplicate/nonfinite refusal; exact object key/shape.

Independently determine anchors: original vertices degree!=2, plus lexicographic
minimum vertex of each all-degree-two connected component. Supplied compressed
keys must exactly anchors. Each compressed edge has matching witnesspath >=2nodes,
source/target consistent, internal nodes nonanchors degree2; adjacent steps present
in original graph, each directed original edge covered exactly once across ALL
witnesses, including both pure-cycle directions. Refuse unknown/duplicated coverage,
missing edge, invented cost, heterogeneous vector. Sum original integer step costs
must equal compressed time/exposure/scenario vector exactly. No production chain
builder consulted as validation oracle. Original lookup preserves adjacency index.

Query start/goal MUSTanchors. Missing route null returns UNAVAILABLE, not proof
of no feasible route. Route path first/last matchquery and each listed edge links
consecutive compressed pathnodes via exact source/index/target; indices intnotbool,
nonnegative inbounds (negative indexing refused). Expand checked witnesses, validate
full original directededge continuity and costs independently. Route totals exactly
match original expanded sums, worst_time=max(scenario_totals), exposure<=budget.
FEASIBLE_WITNESS on all checks; malformed/unsupported/falsewitness INVALID with
reason. Never certify minimum cost or global original/compressed equivalence.

## Fixed exposed evaluation, 20 rows

Four valid constructions with explicit compressed graph/witnesses, not baseline
solver outputs used as oracle:
A asymmetric chain a-b-c, forward costs time2,1/exposure1,0/scenarios(3,4),(2,1);
reverse b-a time7/exposure4/scenarios(5,6), c-b time9/exposure2/scenarios(7,8).
Anchor query a->c budget1, route forwardcompressededge0, totals3/1/(5,5),worst5.
B same map reverse c->a budget6, totals16/6/(12,14),worst14.
C purecycle a-b-c-a, reciprocal original eachtime1/exposure1/scenario(1),anchor a;
compressed two self-directions eachthree steps. Query a->a with explicit one full
cycle edge0, totals3/3/(3),worst3,budget3. Feasible witness, not optimalidentityroute.
D theta graph anchors a,z, three paths a-b-z,a-c-z,a-d-z, reciprocaleachstep
 time1/exposure1/scenarios(1,2). Compressed3parallel edges eachdirection; query
 a->z viaedge1 middlec, totals2/2/(2,4),worst4,budget2.

Each valid plus three fixed mutations: compressed route index -1, route exposure+1,
first witness interior node replaced unknownvertex. 4+12=16rows. Four standalone
controls A interiorquery b->c INVALID; A nonempty turnrule INVALID; A float original
cost INVALID; A nullroute UNAVAILABLE. Total20. Allrows/inputdigests/verdicts/reasons/
expandededgeidentity/costs retained, expected/actual disagreement MISMATCH. Strict
success20/20expectedagreement. No postfreeze mutation/tolerance/parameter rescue.

Four production aggregate_chains + exposure_budget_route + expand_route descriptive
calls on original fixtures, reported separately, NOT route construction proof or
novelty/compression speed claim; C may return zero-length identityroute, retain it.
Pin unchanged routing/chain_aggregate/chain_costs/chain_compress/topology_audit;
helper dependencies/source/runtime/executable gates before any case/baseline calls.
Development separate literal independent topology/coverage, cycles/parallel direction,
wrong costs/route shape/negative index/turn/interior/null refusal and disagreement/
source-before-load controls, not full20-row battery.

Prereg review/publish BEFOREimplementation; executable/fixtures/schema/source/env
freeze review/publish BEFORE20rows/fourbaselinecalls; resultsreview/publish.
No scientific/clinical/hardware/invention/optimality/general routing-equivalence
claim. Anchor integer turn-free scope only. Caps not peak memory/sandbox/timeout;
runtime pins not full OS/shared-library provenance. Known float non-equivalence
unchanged. Research technical reviews do not establish user permission.
