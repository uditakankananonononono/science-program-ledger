# Corridor transfer-operator invention admission: REJECT generic claim

2026-10-08. Narrow prior-art/existing-code memo, not exhaustive novelty or patent
clearance. NO implementation authorized by this finding. Generic proposal - reusable
boundary/incoming-edge transfer operators retaining Pareto costs and witnesses -
is a composition of established contraction/overlay/state-expansion methods. Local
missing functionality is real but is not algorithmic invention. No specific uncovered
claim survived this screen. Do not turn the local gap into a novelty claim by renaming
shortcuts "operators" or by citing only scalar routing.

## Checked existing code at b7b5af869e4f1d42005ab741ec539c9865f19dd6

chain_compress.compress_chains calls topology_audit.audit_topology, which explicitly
rejects self/parallel edges and requires reciprocal adjacency (simple graph). Degree-2
chains/pure cycles get topological witnesses. chain_costs.serialize_chain_costs uses
neighbor-keyed lookup under those preconditions; it is not a silently losing general
parallel-edge adapter. chain_aggregate.aggregate_chains sums exposure/scenario/time
per direction, returns anchor graph/witnesses, expressly anchor-only/turn-free.
It has no incoming-edge boundary signature, internal forbidden-turn test or penalty
composition. integrated_route separately uses (node,incoming-original-edge-ID) and
Pareto (exposure,scenario totals), checks forbidden turns and adds scalar turn delay
to every scenario. Thus feeding aggregated graph plus original turn IDs is NOT an
admitted integration. A turn-aware compressor would be new local engineering, not
new theory. Existing witness output already makes path reconstruction non-novel.

## Claim-by-claim primary-source evidence

| Proposed component | Established evidence | Important limit |
| --- | --- | --- |
| Reusable boundary-to-boundary transfer summaries | Customizable Route Planning (2011), S1, explicitly builds cell-boundary cliques whose costs equal restricted shortest paths, reuses overlay for queries and supports turn costs | Scalar arbitrary metrics are not a full multiobjective Pareto solver |
| Incoming-edge boundary/turn state | CCH with Turn Costs (2020), S2, covers edge-based expansion (road segments become vertices, allowed turns become arcs) and compact turn tables | Does not alone certify our resource/scenario combination or constant-size summaries |
| Preserve internal Pareto/resource alternatives during contraction | Exact Constrained Shortest Paths via CH (2012), S3, says maintain all Pareto-optimal local paths, shortcut witness domination, additive cost/resource shortcuts | Paper problem is cost+resource; do not claim direct theorem for our all-scenario minimax interface |
| Preprocess many queries and return full Pareto frontier | Bi-objective CH (2023), S4, explicitly computes Pareto frontiers with preprocessing/partial expansion | Two objectives, not arbitrary-dimension bounded memory |
| Multicriteria overlay retaining cost-vector alternatives | Fast One-to-Many Multicriteria Search (2022), S5, cover extraction creates overlay edges with path cost vectors, non-simple overlay alternatives, redundancy pruning | One-to-many road-network context; timings not transferable to our repo |
| Multi-criteria CH, caution on scalarization | Funke/Storandt (2014 extended abstract), S6, query-time conic combinations | Not evidence of all unsupported Pareto points, unlike S3/S4 |
| Query witnesses/path recovery | RoutingKit CH docs, S7, node and arc path APIs; composable extra-weight links | Extra weights are explicitly NOT optimized, so this is not a Pareto-baseline replacement |

Scenario costs in our code form additive vectors; taking max only at final objective
is not a new contraction concept by itself. Retaining incoming-edge state and
componentwise nondominated vectors is the standard safe composition direction, not
an admitted invention. None of the sources alone proves a ready-to-drop-in combined
solver for our exact interface. Nevertheless the generic contribution is covered by
established components and closely related full-vector overlays. Need a specific
new invariant, complexity reduction, query/update result or nonstandard constraint
with a justified published-baseline distinction before proceeding as invention.
No such claim offered here. Completeness/size bounds cannot be inferred: frontiers
and summaries may grow exponentially. No performance/correctness result scored.

## Source ledger: fetched, not highlights

S1 primary full paper, Daniel Delling et al., Customizable Route Planning (2011):
http://tpajor.com/assets/paper/dgpw-crp-11.pdf
Fetched boundary clique/customization/turn-cost sections. High confidence on stated
architecture, no claim of full Pareto capability or imported code/license admission.

S2 primary full paper, Customizable Contraction Hierarchies with Turn Costs (2020):
https://drops.dagstuhl.de/storage/01oasics/oasics-vol085-atmos2020/OASIcs.ATMOS.2020.9/OASIcs.ATMOS.2020.9.pdf
Fetched abstract/model discussion. Edge-based/compact representation established.

S3 primary full paper, Sabine Storandt, Route Planning for Bicycles - Exact Constrained
Shortest Paths made Practical via Contraction Hierarchy (2012):
https://ad-publications.cs.uni-freiburg.de/ICAPS_constrainedch_S_2012.pdf
Fetched local Pareto preservation/witness-search and cost-resource shortcut text.

S4 primary publisher abstract, Efficient Multi-Query Bi-Objective Search via CH (2023):
https://ojs.aaai.org/index.php/ICAPS/article/view/27225
Fetched abstract only, not full algorithm admission. Explicit frontier claim verified;
no detailed implementation/complexity assertion based on unseen full paper.

S5 primary full preprint, Fast One-to-Many Multicriteria Shortest Path Search (2022):
https://ar5iv.labs.arxiv.org/html/2201.12684
Fetched cost-vector cover/overlay construction and alternative-path discussion.

S6 primary publisher abstract, Polynomial-Time Construction of CH for Multi-Criteria
Objectives (2014 extended abstract referencing 2013 full paper):
https://ojs.aaai.org/index.php/SOCS/article/view/18273
Fetched conic-combination scope, not misrepresented as full Pareto.

S7 public implementation documentation, RoutingKit ContractionHierarchy.md:
https://github.com/RoutingKit/RoutingKit/blob/master/doc/ContractionHierarchy.md
Fetched node/arc extraction and explicit extra-weight-not-optimized warning.
Institutional routing publication page also fetched as bibliographic cross-check:
https://ae.iti.kit.edu/1862.php
Technical decision relies on primary publications plus code docs and local bodies;
community commentary not needed. Seven sources, not seven independent confirmations
of a single universal combined algorithm. No external repository/data imported.

## Decision and next options

1. REJECT generic proposal as invention. Stop before implementation/comparison; no
uncovered claim survived. Retain this negative admission finding, not pretend novelty.
2. If separately wanted, turn-aware local compression can be established-baseline
engineering with explicit edge identities, boundary state and exact witness replay.
Not approved here, no promised speedup, no scientific invention count.
3. For invention search, start from a demonstrable structural bottleneck and propose
a specific new property before implementation. Prior-art screen would have to revisit
that exact claim. Do not invent novelty by adding microrobot naming/constraints or
claim absence from these bounded search results.
