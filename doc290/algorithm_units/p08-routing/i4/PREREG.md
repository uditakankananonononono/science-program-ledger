# I4 bounded exact integrated certificate generation

Parent01c3b24c47c5eb5426f2766cfb54157c9e3da649. I3 accepts supplied proof and
explicitly excludes generation; I4 fills that method-artifact gap against the
UNCHANGED pinned I3 checker. Established finite exact certificate search, not
complete optimizer/newsolver/invention/novelty/science orphysicalcalibration.
Earlier forward-source-distance construction was a design hypothesis, withdrawn
before implementation: full unreachable-state constraints require derivation.

## Scope and candidate protocol

Input original graph/query/budget/forbidden/penalties/route only. I3 full strict
integer model, 32vertices/128edges/128rules each/path256, edge-established1..4
scenarios, everyoriginal edge/rule/goal-outgoing/identity/unreachableincoming
state retained. No compression/float/unit/domain translation. Originalprimal
validated via pinned T1checked first; model before missingroute. Invalidprimal/
model INVALID, missingroute UNAVAILABLE aftermodelchecks. No oracle/solverroute
construction, no inputweights/multiplier/potential override. JSON128KiB/depth10/
duplicate/nonfinite rejection inherited; exactFraction grammar/caps unchanged.

Fixed candidate weights: each unitvector in originalscenario order, then uniform
simplex [1/n]*n, deduplicated in that order(n1 yieldsone). Multiplier order
[0,1/2,1,2]. Cartesian weight-major order, atmost20candidates. No adaptive search,
postfreeze candidateaddition, earlystop/drop aftercertificate. EACHcandidate gets
full ledger including failure/unavailability. Nonnegative weighted arc cost=
sum_i(w_i*(originalscenario_i+scalar turndelay)) +lambda*originalexposure,
sinkarcs0, delay once per scenario, no edgewise-worst replacement.

Full-state reverse Dijkstra Fraction minima to canonical sink over originalallowed
arcs; independently rebuild from raw original graph/rules (NOTmethodarcs) and
synchronous Fraction Bellman-Ford ALLstates beforepotential authority. Costs,
potential values, weightedprimal/budgetcharge/LB enforce unchangedI3supported
rational caps <=2^53-1; canonicalrepresentation <=80chars. Finite primal implies
finite source distance D; Nonecontradiction FAIL, no rescue. Candidateoutside
supportedcertificate numericdomain recorded UNAVAILABLE_DOMAIN, notfalseproof;
malformedinput remainsINVALID. Auditmismatch/internalcheckerINVALID onadmitted
candidate propagatesFAIL, never reclassified successful search.

Potential construction: let d(v) shortest weighted remainingcost to sink;
M=max(allfinite d), including sink0. For finite d(v), h(v)=D-d(v); for None,
h(v)=D-M. Thus h(source)=0 andh(sink)=D. Proof forEVERYallowedarc(a,b,c>=0):
finite->finite shortestpath inequality d(a)<=c+d(b) yields h(b)<=h(a)+c;
finite->None uses M>=d(a), hence d(a)<=c+M;
None->finite cannotoccur (then a would reachsink), explicitly verified PERcandidate on concrete originalarcs at generation time;
any None->finite arc records candidate UNAVAILABLE_TOPOLOGY and emitsNOproof,
never assume reachability property or repair ledger;
None->None constantpotential andnonnegativecost. Goaloutgoingarcs/unreachable
fromsource-but-sinkreachable states NOTexcluded. This handles I3C's rejected
hEb0=0->sink5 trap by includingthatstate's actualsuffix/potential.

Emit canonical h/weights/lambda only afteroriginaltopology/distance/potential
checks; pass EVERYemittedcandidate through unchanged pinnedI3check. Recompute
primal/weightedcost/slacks/LB exactlyindependently; no acceptstatus-as-proof.
Matching feasible worst W==LB ->CERTIFIED_INTEGRATED via unchangedchecker;
LB<W remainsUNAVAILABLE(validincompletebound). LB>W contradictionFAIL. Always
return completecandidateledger; select highestLB, tiesfirstcandidateorder;
outputoverallCERTIFIED onlyifsomecandidatecertifies elseUNAVAILABLE withbestgap
orUNAVAILABLE_DOMAIN ifallcandidatesdomainunavailable. No completenessclaim:
finite setmaymissvalidcertificates anddiscretebudgetdualitygapmayremain even
withunbounded multipliers. Missingroute notinfeasibilityproof.

## Fixed20 evaluation rows, preregistered BEFORE execution

All edge.time1; two scenarios, unlessidentityfixture. Originalindexedroutes:
A I3A: a-b[1,1]/r1,b-g[1,1]/r1,delay2,budget2,route[4,4]/r2/turn2/W4 CERTIFIED.
B I3B: [1,5]+[5,1],delay1,budget2,route[7,7]/r2/turn1/W7 CERTIFIED(uniformonly).
C I3C: a-b[1,1]/r0,a-g[5,5]/r0,b-g[1,1]/r0, forbid(a0,b0),budget0,
routea-gindex1[5,5]/r0/W5 CERTIFIED, allincomingstates retained.
D I3D: a-g[1,1]/r2,[3,3]/r0,budget1,routeindex1W3/r0 UNAVAILABLE;
bestlambda1 LB2/gap1, genuine discretebudgetdualitygap.
E identity a->a witha-g[2,3]/r0,g-a[1,1]/r0,budget0,route[a]/[]/[0,0]/r0
CERTIFIED, dimensionedge-established, zero sink/source retained.
F active budget0: a-g[0,0]/r2,[3,3]/r0,routeindex1W3/r0 CERTIFIED(lambda2).
G finite-setmiss: a-g[0,0]/r2,[7,7]/r1,[11,11]/r0,budget1,routeindex1W7/r1
UNAVAILABLE; selectedlambda2 LB2/gap5. Lambda4 (OUTSIDEfrozen search) would
certificateLB7: development algebra only, never added inresult asrescue.
H unreachable-extension: a-g[2,2]/r0,x-y[1,1]/r0,y-x[0,0]/r0,budget0,
routea-gW2/r0 CERTIFIED; x/yincomingstates cannotreachsink, constantD-M applies.

Each8base plus1mutation route.reportedworst+1 INVALID =16rows. Fourcontrols:
Anullroute UNAVAILABLE aftermodel; ArouteindexTrue INVALID; Ano positiveedge
scenario dimension(emptyvectors) INVALID; Agraphnegativeexposure INVALID.
Exactly20rows; expected8bases=6CERTIFIED/2UNAVAILABLE,8INVALIDmutations,
additional1UNAVAILABLE+3INVALID. Allfixedrows/digests/candidateweights/lambda/
fullstates/distances/potential/transitioncost/slack/primal/LB/gap/checkverdict
retained, no rowdrop/candidaterescue/checkermodification. Genuinegaps firstclass.
No productionkernelcalls; independent originalstate budgetDFS confirms8primal
optima but is not generatorauthority/proof. This20battery notrun beforefreeze.

Developmentoutside20: Fraction telescoping/maxextension/goaloutgoing/unreachable
source-vs-sink/identity/zero/forbidden/parallel/repeatedvertex, clampboundary
state d(v)==M and nonuniquemaxfinite distance controls/mutations, injected
None->finite arc guardUNAVAILABLE/noemission, differentminima/
correlatedcost/budgetgap/finitecandidatemiss, domainoverflow/grammar/types,
strict independentoracle, falseledger/potential/witness/candidateorder rejection,
auditexceptionpropagation, allcandidates enumerated evenaftercertificate. Real
boundedworker128MiBAS/singleCPU beforehelpers/sourcegate,5skill/drain/reap,
parser/malformed/memory/kill/gatecontrols; fulltransitiveI3/B3/T2/T1/C1/F3pins
andactuallyloadedpaths/runtime beforeexecution. ASnotRSS/tree/OS/sharedlibproof.

Prereg exactreview/publication -> executablefreeze exactreview/publication ->
20one-shotrows -> exactresultreview/publication. No fixed20subjects before
publishedfreeze, no postfreeze code/candidate/oracle/rescore/tolerance/rescue.
AllpriorI3CbaselineFAIL/P3FAIL/K1K2/M4negative/M5harnessFAIL/M6rejectedhistory
unchanged; noautomaticproductionintegration/CI/completion/physiology/scienceclaim.
One-shotprocessreported, notcryptographicallyprovedbyGitancestry.

## Prereg design clarification before implementation
Parent08:24:06 requires the None->finite topology implication as concrete
per-candidate guard (UNAVAILABLE_TOPOLOGY/noemission) and clamp-boundary/nonunique
M controls; added here before any fixedrow/generator execution. Initial25a2bf19
prereg draft retained locally as ancestor, notpublished/evaluated.
