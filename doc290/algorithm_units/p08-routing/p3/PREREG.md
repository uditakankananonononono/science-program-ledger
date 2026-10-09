# P3 reverse-scenario admissible pruning method/comparator

Parenta681b402fcf660de511f65f9f1b9da9606b24d22. RoutingREADME runtime/frontier
measurement gap; R3 characterizes unchanged solver, no optimization variant.
This is standard admissible-bound pruning, NOT originality/invention credit.
No published-prior-art superiority/newalgorithm/science claim.

## Method and admitted model

Separate explicit scenario-only exactinteger JSONgraph/start/goal interface.
1..32stringvertices/128originaledges, homogeneousedge-established1..4scenarios;
parallel/self/asymmetric/zero edges allowed, positive dimension required even
identity query. Edge time/exposure/scenarios strictintnotbool0..floor((2^53-1)/32).
Graph caps make simplepath objective <=2^53-1. No budget/turn/compression/units.
No decimal tolerance; unchanged productionkernel untouched. Unsupportedtypes/
model reject, not silencenumericdomain conversion. InputJSON128KiB/depth10.

Compute reverse Dijkstra independently for eachscenario -> d_i(v), shortest
remaining cost (None if goalunreachable). Scalar distance onlyadmissiblebound,
not common-scenario pathobjective. Generate initial feasibleincumbent by forward
Dijkstra minimizing scenario0, reconstruct indexed simplepath; independently
recompute whole-scenario totals/W beforeusing incumbent. Sourceidentity=>zero
route, absentforwardpath=>None. Reversezero cycles deterministicstrict-relaxation.

Exact Pareto label search like unchanged scenario_robust_route, but generated
candidate (v,t_i) pruned if goalunreachable or max_i(t_i+d_i(v))>incumbentW.
Strict > keeps all equal-bound candidates. Incumbent remains fixed suppliedby
method, not baseline/oracle. Retain componentwise dominance; nonnegative cycles
are dominated, simplepath witness <=32. Firstgoalpopped lowestmaxpartial gives
optimum; if queueemptyreturn validatedincumbent, which search/pruning preserves.
Pruning safe because anycontinuation eachcomponent >=d_i independently; common
minima neednotsharepath. No cached incumbent/status-as-proof/manualrescue.
ExactPythoninteger intermediate lowerbounds mayexceedMAX; objectiveonlybounded
by simplepaths underedgecap. No float regrouping claim.

Counters clearlyscoped: reverserelaxations, incumbentre laxations, candidateedges,
LBpruned, dominancepruned, labelsinserted,pop/stalepop,maxlivequeue. Baseline
unchanged kernel result only; no inventedbaselineoperationcounter. Deterministic
work counts fromvariant, notrelativeperformanceproof. If route differs ties,
compareobjective+independentwitness notexactpath. CPUtime optionaldescriptive,
no speedup requirement/inference. Variant+baseline eachfreshboundedworker128MiBAS/
verifiedsingleCPU beforekernelreads, parent5s timeout kill/drain/reap. Imported
R3controls/gates may bereusedpinned, no modifiedR3outputs/source. Allattempts
retained FAIL timeout/import/cap/parse/wrongwitness/objective; noretry/drop/rescue.

## Frozen corpus and success

100 directedfour-vertex graphs seed314159, orderedverticesa,b,c,d, eachordered
nonselfedge probability0.35 (random.Random.random), twoscenariocostrandint0..9,
time1/exposure0, querya->d. Ifzeroedges addirrelevant d->d [0,0] todimension.
Exact exhaustive simple-path oracle minmax orNone, plusindependentoriginalindexed
witness reconstruction. This includescycles/zero/disconnectedpaths; syntheticonly.
Four curated: parallel[a->g(1,5),(5,1)]W5, identitya->a withedge[a->g(2,3)]W0,
correlatedchain[1,5]+[5,1]W6, unreachable(a->b[1,1],g[])None.
Two tradeofffamilies n8/n10 as R3; oracle128/512, separatesizecap<=32.
Exactly106 casepairs variant+baseline=212subjects. Freeze generatedcorpus + all
exactoracleanswers beforeevaluation, no gate basedon variantperformance.
Primary all106 independent objective/witness agreements BOTHmethods, nofailures;
all106records includinglosses retained. Pruning/countersdescriptive secondary,
zeroprunes/noimprovementnotrescued orclaimedwin. No moredatasetacquisition.

Development literalgraphs outside106: reverseadmissibility/componentminima not
sharedpath, strict-equalityprune boundary, zero-cycle/revisit/dominance/identity/
missingdimension/types/caps; independent tiny enumeration, countersdeterminism,
falseincumbent/refusal and controlledresultdisagreement. No106solvercallsbefore
exactfreeze review/publication. Prereg->freeze->one-shot->resultreview/publication.
PriorI3CbaselineFAIL/K1K2FAILs/R3rejectedfreeze/gaps/floatloss remainunchanged.
ASnotRSS/solver-only/container/tree guarantee; sourcepinsnotOS/sharedlibrary/
scheduler guarantee. Standard methodartifact +synthetic comparator, notnovel
invention/publicbaseline superiority/clinical/physicalcalibration/sciencegate.
