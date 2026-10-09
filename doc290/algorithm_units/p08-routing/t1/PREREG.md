# T1 checked original-edge turn-aware integer route

Parent4f8874060b9646dbaf80350748d0dd762b941219. README chainturn equivalence unresolved,
expansionrepresentation notuniversalrouteauthority. T1validates ORIGINAL graph routes,
notcompressedturntranslation/equivalence; C1/C2turn-free unchanged. Separateexplicit
artifact, productionintegrated_route unchanged, nooptimality/newalgorithmclaim.

Statementkeys graph,start,goal,budget,forbidden,penalties,route. Graphstringvertices
<=32/nonempty; <=128directededges, parallel/selfedgesallowed, costsnonnegativeint
notbool<=2^53-1, scenariohomogeneouspositive1..4. Exactedgekeys target/time/exposure/
scenario_times, targetexists. Budgetsameintegerdomain. Start/goalexistingvertices.
JSON128KiB/depth10/duplicates/nonfinite refusal. No physicalunitsinferred.
Forbiddenlist ofpairs incoming/outgoingedgeIDs [sourcestring,indexint]; penaltylist
objects incoming,outgoing,delay. RuleIDs existing/consecutiveedges; no duplicate
ruleswithinlist, no negative/bool/floatdelay, no guessedfirst-edgepenalty. Samepair
mayhaveforbiddenandpenalty: forbiddenwins, no logicalinvalidityininput. Arbitrary
externalruleinstructionsnotauthority; suppliedrules onlywithinfrozenstatement.

Route exactkeys path,edges,exposure,scenario_totals,worst_time,turn_penalty (matching
integrated_route return). NullUNAVAILABLE onlyAFTERgraph/query/budget/ALLrulevalidation,
notinfeasibilityproof. Path1..256nodes/edges=pathlen-1, first/lastquery, everyedge
source/index/targetmatchesoriginaladjacency/consecutivenodes; negativeindexrefused,
parallelidentifiedbyindex. Revisitedvertexpermitted, neverrejectsolelyascycle.
Eachconsecutiveedgepair forbidden=>INVALID; scalardelay fromexactpair or0added
EQUALLYtoeachscenariototal, nofirstedgeorfinalartificialturn. Exposureedgeadditive
only. Replayalloriginaledges, exactinteger totals<=2^53-1, compareeveryreported
field andexposure<=budget; FEASIBLE_WITNESS iffpass. No claimedoptimum/global
feasibility/generalgraph-equivalence/physiology/clinical/invention/sciencegate.

## Fixed exposed20 rows, 4 valid +12mutations+4standalone

A parallel: grapha edges0b(time1,exposure1,scenarios[2,3]),1b(1,2,[5,1]);
b edge0c(1,1,[1,4]);c empty. Querya->c,budget3,routeedges(a1,b0),
 penalty(a1,b0)=2; exposure3,scenarios[8,7],worst8,turn2. Distinguishesparallelcost.
B revisit: a0b(1,1,[1]),b0c(1,1,[1]),b1d(1,1,[1]),c0b(1,1,[1]),dempty;
 forbidden(a0,b1). Querya->d,budget4,routea-b-c-b-d viaa0,b0,c0,b1,
 penalty(c0,b1)=3; exposure4,scenario[7],worst7,turn3. Revisitdifferentincoming
avoidsforbiddenturn; notsimplevertexpath. No routeoptimalityproof.
C selfcycle: a0a(1,1,[1,2]);querya->a,budget2,routea-a-a viaa0,a0,
 penalty(a0,a0)=4; exposure2,scenario[6,8],worst8,turn4; identityroutecheaper,
 explicitwalkstillvalidwitness. D Agraphidentitya->a,budget0,pat h[a]/edges[],
 exposure0,scenarios[0,0],worst0,turn0; nofirstedgeturn.

Eachvalidthree mutations negativefirstedgeindex,turn_penalty+1,scenariofirst+1.
Dnegativeindexmutation replacesroutewith Aactualtwo-edge routebutquerya->a;
strictpath/edge mismatchINVALID, notvalididentitycorruptioncreatingmissingindex.
16rows. FourstandaloneA: addforbiddenselected(a1,b0)INVALID; budget2INVALID;
nullrouteUNAVAILABLE; malformedruleID[-1]INVALID evenwithnull. Total20.
Allrows/digests/verdicts/reasons/expandededgeandturnledger/exacttotalsretained,
strict20/20expectedagreement; loss/exceptionkeptMISMATCH/norescue.

Fourunchangedintegrated_route baselinecallsdescriptive only; C/Dmaychooseidentity,
A/Bcanchooseothercostpaths, comparisonsnotoptimalityvalidationoracle. Allrawroutes/
exceptions/warningspercallretained. Independentlyreplay baselineoriginaledges/turns
ifreturned, no useofbaselineasvalidatortruth. Developmentseparateliteralasymmetric
parallel/revisit/turn-ledger/firstedge/identity/null-invalidrule controls, malformed
keys/types/dimensions andsourcegate/disagreement, notfull20battery.

Prereg review/publishbeforeimplementation; executable/fixtures/schema/source/runtime
freeze review/publishbefore20rows+4baselinecalls; resultreview/publish. Pinunchanged
routing/chain/C1C2/helper, loadedPython/executable/modules beforecases/solvers.
No floatregroupingrepair/turn-awarecompressedadapter/universalequivalence/CI/holdout/
speed/invention/physicalscienceclaim. RuntimepinsnotOS/sharedlibclosure;
capsnotpeakmemory/hardtimeout/adversarialsandbox. ExistingK1K2FAILsremainpublic.
