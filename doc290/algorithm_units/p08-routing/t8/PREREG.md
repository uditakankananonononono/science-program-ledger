# T8 integrated turn-state scenario suffix pruning

Parent result 7799cdecbfacf7ce4cba7722e2e4eb3abe7e1bc4. Documented gap:
T7 method.py has exposure/dominance pruning but no whole-scenario suffix bound
against a validated goal. Established bound composition, not an invention.

## Model, method and proof

Separate unchanged T7 admitted graph/query/budget/turn/scenario model: strict
integers, positive edge-established 1..4 scenarios, 32 vertices/128 original
edges, full canonical source/incoming-original-edge/sink states and every allowed
transition including unreachable/goal-outgoing/identity/zero sink arcs. T7 caps
and inherited unused scalar time+delay admission retained. Scalar delay is added
once to EACH scenario, never exposure. Original indexed witness <=130 vertices,
no repeated incoming-edge state; vertex revisits allowed. No compression/units.

Reuse pinned T7 exposure reverse ledger and independent original-topology audit
BEFORE early None. Same source None/>budget reasons, all eight exact-phase counters
zero there. No new scenario/upper-bound preprocessing on an early exit. Feasible
branch: compute reverse Dijkstra separately for EACH scenario over all full states;
arc cost is original edge scenario_i + allowed scalar delay, sink arcs zero.
Strict relaxation handles zero cycles. Independent original-edge/rule topology
rebuild and synchronous Bellman-Ford recompute ALL state minima, not method arcs,
BEFORE pruning and again in parent receipt. Full strict typed states, ordered
scenario dimensions, nonnegative integer/None distances and zero sinks required;
false unreachable, lowered distances, bool/float indices and partial ledgers reject.
Independent minima need not share a path; max_i(prefix_i+d_i(state)) is a LOWER
bound on whole-scenario minimax for any allowed continuation, not a route score.

Generate a feasible incumbent by forward full-state Dijkstra minimizing EXPOSURE
only, with deterministic heap serial and strict relaxation, original arc order.
Reconstruct original indexed walk from predecessor transitions to the sink; zero
sink arc is not a traversed edge. Independently recompute all scenario totals,
turn penalty and exposure against actual budget with pinned original witness
validator BEFORE using W. Finite/nonnegative source exposure minimum <=budget guarantees this
path exists; absence/reconstruction/audit contradiction propagates FAIL. Incumbent
is produced by this method, not T7/oracle/beam, and remains fixed. Identity gives
zero empty-edge walk. Return/store the full incumbent witness, not only a number.

Preserve T7 full exact heap/serial/vector/incoming-state dominance and first-goal
loop. After forbidden/exposure feasibility and before dominance/insertion, prune
candidate ONLY if max_i(new_i+d_i(outgoing_state)) > incumbent W. No >=, all ties
retained. Feasible exposure suffix with any scenario None is a contradiction FAIL,
not authority to discard. No pop-bound reorder or incumbent updates. The incumbent
route remains reachable under the bound, so feasible queue exhaustion is FAIL,
not fallback or oracle/status rescue. First popped goal still owns the optimum;
return its original indexed witness. Path tie identity may differ; objective and
independent witness equality are primary, not identical route choice.

Existing T7 reverse exposure counter unchanged; separate counters for scenario
reverse arc inspections, forward incumbent arc inspections, objective_bound_pruned.
All original exact-phase counters retain their meanings. Same exposure audit is
single-use as inside T7, not double-counted overhead. New scenario audit and
incumbent work reported as extra work, never hidden in labels saved. Receipts
recheck exposure certificate, scenario ledger and incumbent witness/W. Model,
audit errors and malformed receipts fail; no catches that turn failures into None.

## Frozen comparator and success

Copy pinned T7 fixtures generator/oracle, seed ONLY changed to 264575. Exactly
200 four-vertex/three-scenario graphs, single Random draw order unchanged including
forbidden THEN penalty random draw for every valid turn even if forbidden;
original edges/scenario costs/exposure/penalties and budget last unchanged.
Freeze actual inputs plus independent original-incoming-edge simple-state DFS
budget/turn/minimax oracle BEFORE method subjects. No solver-derived expected
answers, no performance gate, no row selection. Fresh synthetic, not external,
held-out, strong blind or physiological validation.

400 sequential fresh bounded workers T8/pinned T7; exact independent oracle and
original witness agreement for every subject, all attempts/failures retained.
Parent GATE_FAIL distinct. Report 200-pair labels/candidate wins/ties/losses and
failure exclusions, source class counts, actual objective-bound prunes and all
new preprocessing separately. Zero prunes or losses remain results, no rescue.
Optional whole-worker single timing/RSS observations not speed/total-work proof.
128MiB AS + verified single CPU before core/kernel/source reads; parent+worker
transitive source/loaded-path/runtime gates; 5s kill/drain once/reap/no retry/drop.
AS not RSS/tree/container/OS/shared-library/scheduler guarantee.

## Development and review gates

Outside-corpus literals: scenario minima on different paths, correlated costs,
turn delay once per scenario, forbidden route, parallel/zero/cycles, repeated
vertex/incoming-state identity, identity/budget equality/infeasible classes,
strict-bound equality and genuine strict-bound exclusion, absent incumbent,
false incumbent/W, full-state/scenario-ledger mutations and audit exceptions.
Small independent brute oracle, deterministic counters, parent disagreement,
loaded alternate/modified transitive helper refusal, strict types/caps/JSON.
Real BOTH-method FINAL-gate success with nonempty forbidden turns; malformed,
kill/memory/gate/badJSON controls. Immutable initial PRE-final receipts explicitly
labelled, final real rerun after manifest regeneration. Pin unchanged T7/T6/T2/
T1/C1/F3/production plus prior results/failures. Explicit proof-module binding for
imported baseline, never rely on a same-name local module; no baseline edit.

Exact prereg review/publication -> executable freeze review/publication -> one
frozen evaluation -> exact result review/publication. No 400 subjects before
published freeze, no post-freeze method/oracle/rule edit or silent rescue. Prior
M4 slower 446/600 negative and P3/I3/K1/K2/rejected histories remain untouched.
No automatic production integration, prior-art-screened novelty, invention,
science completion, clinical/calibration or speed superiority claim.
