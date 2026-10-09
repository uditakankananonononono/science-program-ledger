# P4 bounded beam feasible incumbent for exact pruning

Parent29fd76a138ce7712444419e04d4c54635d2fda7e. Documentedruntime/frontiergap;
P3tradeoff8/10zeroLBprunes, preservedscenario0incumbent extremes. Standardbeam
heuristic upperbound proposal +existingexactpruning, NOTnewinvention/novelty.

Admitted strict originalinteger graph/domain/model/witness EXACTLYP3 unchanged.
SeparateP4method imports pinnedP3model/reverse/incumbent/route/prunable helpers,
fullParetoexactsearch sameP3logic except bettervalidatedincumbent selection.
Compute scenario0incumbent unchanged. Beam startszero/source simplepath; breadth
layers1..V-1. At eachdepth expand previousbeam simplepaths (no vertex revisit),
collect goalcandidates into bestgoal; othercandidates grouped bydestination,
retain up towidth2 pervertex sorted(maxwholeprefix,wholeprefixtuple,path,indices).
Duplicates identicalpath/indices removed; no dominance deletion acrossvisitedsets
(thebeam is approximate anyway). No reversebounds prune beam. Beamcosts exactint,
routecap checked; allproposedgoalpaths originalindexed/whole-scenariorecomputed.
Continue boundeddepth even afterfindinggoal; beamreturnsbestvalidatedgoal by
(worst,scenariotuple,path,index). Identityzeropath. No beamroute =>use oldincumbent.
Compare old/beam worst: choosebeam onlystrictlybetter; ties preserveold path.
Beamexception/invalidcandidate propagates FAILURE, never silentlyold fallback.
Beam output NOToptimalityproof; fullParetosearch with strict>LBprune unchanged.
Losingbeam paths affects onlyupperbound quality, cannotremoveoptimum; validated
old/beam upperbound remains>=optimum. Sourceunreachable mayreturnNone beforebeam
underpinnedincumbent authority, notbeamabsence-as-infeasibility. NO solverfallback
exceptions/rescue/oracle-informedincumbent. Allcandidate routes caller costs only.

Beam deterministic boundedcandidatecounts/depths, up to2pathspervertexperdepth;
predecessorvisitedsets make incompleteheuristic explicit. Counters beamexpansions/
beamgoalcandidates/beamkept/beamdepths and selectedsource/oldW/beamW plusP3exact
searchcounters. P3comparison counters are actualpinnedP3method outputs thisunit,
notinventedunchangedproductionkernel counters. Comparelower labelsinserted/
candidateedges as pairedsynthetic work observables; not runtime superiority or
novelty. Report wins/ties/losses for eachcounter, no cherry-pickorprimarygatebywins.
Extraheuristiccost mayoutweighpruning; nounequaltiming speedupinference.

Freeze copyEXACTP3cases.json106inputs/oracles byte-identical. P4vsP3freshbounded
workers percase =>212subjects. Primary106objective/originalindexedwitness+oracle
agreementsbothmethods, all losses/fails retained. Timingboundaries samebothsolve
includesmodel/incumbent/reverse/witness; P4 additionallybeam; stillsingleobservations
no speedclaim. Parent+workersource/runtimegates;128MiBAS/singleCPU beforeimports/
reads,5s timeoutkill/drainonce/reap, all212attempts. No modificationP3failed/fresh
results, method/corpus/production/R3 bytes. Preregreview/publication->freeze->
212subjects->exactresultreview/publication. No retune width/order/corpus/rescue.

Development literalgraph outside106: beamstrictimprovement and loss/detour /
visited-setincompleteness/zero cycles/identity/parallelindices/tiepreserve/invalid
beamproposal/exceptionpropagation, exacttinyindependentoracle, deterministic
counters. Real successfulP4/P3worker literal outsidecorpus parsercontrols andreal
kill/cap/gate/badJSON controls; devfreshoutputs /tmp immutablefrozenreceipts.
No106subjectcallsbeforefreeze; modelproperties/proposedincumbent inputs notoutput
success canbeinspected. source/runtimepinsnotOS/sharedlib/tree/container/RSS/
schedulerproof. Beamstandardmethodnotnovel/physiological/clinical/scienceclaim.
PriorP3lockedFAIL/I3CFAIL/K1K2/gaps/float/rejectedhistory retainedunchanged.
