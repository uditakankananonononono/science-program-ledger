# R3 bounded adversarial Pareto-family comparator

Parenta895447eae9a82b692cadee27e16c5750e569ba1. RoutingREADME V9 uniformgrid
observations explicitly not adversarial frontier test; remaining runtime/frontier
measurement motivates bounded comparator. Not new algorithm/invention/win.

## Fixed protocol

For n in [4,6,8,10], directed layered vertices v0..vn, each layer i two parallel
edges v_i->v_(i+1). p=2^i; edge0 time1/exposurep/scenarios[p,0], edge1 time1/
exposure0/scenarios[0,p]. Integer model, no turns, no compression. Every path
has subset sum X, exposureX, scenario totals[X,S-X], S=2^n-1. Distinct subsets
map bijectively to integers0..S, because powers2. Each k-layer terminal frontier
has exactly2^k incomparable (X,S_k-X) vectors: increasingX decreasessecondcost.
This is analytic model frontier cardinality, NOT an observed solver label counter;
early goal termination may avoid constructing full theoretical frontier. No
instrumentation/production change/claim that solver visits all2^n labels.

Methods unchanged scenario_robust_route and budgeted_scenario_route. First oracle
W=ceil(S/2)=2^(n-1), minimizers X in {2^(n-1)-1,2^(n-1)}. Budget B=2^(n-2)-1:
X<=B<S/2, optimum X=B, W=S-B. Exactly8 ordered size/method records. Oracle
derived analytically beforefreeze, notsolver-dependent; no choice/tie preference.
Independently recompute returned originaledge/query/indices/path/exposure/scenario/
worstcosts and compareobjective to oracle; retain route and inputdigest.

Each call fresh Pythonworker singlecore, parent sequential <=2cores. Set worker
RLIMIT_AS=128MiB before importingkernel/buildinggraph; inheritedOS/Python/address
spacepolicy restriction not isolatedsolvermemory guarantee. Parent subprocess
communicate timeout5sec then kill and reap that worker; no descendant process
creation in worker. TimeoutcountsFAIL, memory/error/refusalcountsFAIL, wrong
objective/witnesscountsFAIL; no missing success implied. All eight attempted
unless a source/runtime gate refuses the entire run, then reportgateFAIL. No
retries/drop/postfreezeedit/rescue. Timeout5includes workerstartup/import/build/
solve/output, parent kill/reap verification retained. No hard schedulerlatency/
containerlimit assurance. RLIMIT_AS may itself cause admitted workerfailure.

Worker records solveperf_counter duration separategraphbuild timing, ru_maxrss
wholeworkerlifetime LinuxKiB (imports/build/kernel), source/runtimeidentity,
objective/route/status. Parent records elapsed wallworker lifetime, rc, rawstdout/
stderr and timeout/kill/reap. Fresh-worker singleobservations, no CI/statistics/
speedup/scalability/superiority claim. No published externalbaseline comparison;
unchanged algorithms are subjects and analytic exact optima comparator. Theoretical
frontier adversarial does not imply exponential observedtime at these smallsizes.

Development checks family bijection/complement/exposure/cardinality enumerated
small n separate fromfixed n (n1,2,3), oracle independent enumeration; witness
mutation rejects, invalidtypes/caps, disagreecountsFAIL; real worker sleep-control
under short timeout confirms actual kill/reap outcome; worker sourcegatefailure
and resourcecap refusalcontrol. No8subjectsolvercalls beforefreezepublication.

Prereg review/publication->executable/source/schema/fixtures/runtimefreeze review/
publication->one-shot8records->result exactreview/publication. Earlier I3harness
CTypeError, K1K2FAILs/floatloss/gaps remain unchanged. Source/runtimepinchecks
notOS/sharedlib/fullsandboxproof. No clinical/physiological/invention/sciencegate/
productionintegration/novelalgorithm claims. Results remain useful characterization
with every fail disclosed, not demonstrated invention success.
