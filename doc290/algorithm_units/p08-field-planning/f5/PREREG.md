# F5 exact shared-schedule scenario feasibility certificate adapter

Parent535309d235be8289053e5f4808d7f8e2ee0e42cc. SCENARIOS.md documents that
floatingjointLP solver_infeasible lacks independentcertificate, individually
feasible scenarios neednot admitsharedschedule. F3checks minimaxoptimality, F4
singlemapintegral/support; neither substitutes forjointscenariointersectionproof.
Newvalidatorartifact, notnewrobustoptimizer/invention or physicalvalidation.

## Statement and proof convention

Modelkeys x,dt,maps,lower,upper,limit,slew,previous. Sharedinitialstate/time/control
schedule; finiteenumeratedconstantmaps. Exactrationalgrammar/helper pinnedF3:
integersnotbool<=80chars orcanonicalreducedn/d, positivedenominator, nosignedstring
zero/leadingzero/plus; integer-0normalizes0. Listsnonempty; n<=8,m<=4,d<=4,s<=8;
mapdimensionsconsistent, terminal lower/upper eachsxd, lower<=upper. Positive
steps/limits, nonnegative slew, previous withinlimits. No physicalunitsinferred.
StrictUTF8JSON128KiB/depth10/duplicates/nonfinite refusal. Loadedexecutable/source/
moduleidentity andthread/version gates beforecomparison/baselinecalls.

Freevariable u vector step-major, constraints Au<=b reconstructedindependently:
allactuator upper/lowerperstepactuator; allslew upper/lowerperstepactuator including
firstpreviousoffset; terminal upper/lowerperscenario-coordinate, coefficients
±dt[k]*B[s,i,j], rhsupper-x and x-lower. No epigraph/objective. No recourse.
Witnesskind primal, keycontrolsflat: exactdimension then A u<=b AND separately
replay everycontrol/slew, allscenariotrajectories/terminalbox beforeFEASIBLE.
Witnesskind farkas, keymultipliers: nonnegative/correctrowdimension, exact
A^Tlambda=0; strict b^Tlambda<0 -> INFEASIBLE. Ifwellformed nonnegative stationary
multipliers but b^Tlambda>=0 -> UNAVAILABLE, neverjointfeasibility inference.
Negative/nonstationary/malformedmultipliers INVALID. Missingwitness UNAVAILABLE
onlyAFTER validmodel. Noautomaticcertificatefind/solverstatusproof/floatmanufacture.

## Fixed exposed comparator cases

Allx0,dt[1],limit1,slew2,previous0unlessnoted. Roworderabovereconstructionpinned.
J1 sharedcompatible: scalar maps1,2; lower=upper targets1/2,1; controls[1/2].
J2 separatelyfeasiblejointimpossible: maps1,2; targets1,1. Eachalone feasiblewith
u1 oru1/2; multipliers terminal scenario0lower=2, scenario1upper=1; sumrhs=-1,
stationarity0. Allotherrowslambda0.
J3 incompatibleintervals: maps1,1; scenario0box[1/2,1],scenario1box[-1,-1/2];
scenario0lowerlambda1,scenario1upperlambda1, sumrhs=-1, others0.
J4 asymmetricmultistep2x2: x[1,-1],dt[1/2,3/2],limit[2,2],slew[1,2],
previous[1/2,-1/2], maps[[[1,-2],[3,1]],[[-1,4],[2,-3]]];
sharedcontrolsstep0[1/2,-1/2],step1[1/2,-1/2]. Integrated[1,-1]; exacttargets
[4,1],[-4,4], eachlower=upper. Fullschedule nonuniform/previousoffset.

Each4validcase +4fixedmutations: primalJ1/J4 controlsfirst+10(outbound), first0
(wrongterminal), removedlast(shape), firstbool. FarkasJ2/J3 firstmultiplier-1,
allzeros(noncontradictoryUNAVAILABLE), scenario0loweractive+1(nonstationary),
removedlast(shape). Eightstandalonecontrols: missingwitnessUNAVAILABLE, floatdt,
negativeinterval/shape (loweraboveupper), mapsbadshape, badkind, extrawitnesskey,
zero-time, signedzerostringmultipliers. OthersINVALID. 28rows total:4valid+16
mutations+8controls. Allretained expected/actual/digests/reasons; nolossdropping.
Fourunchanged scenarios.py callsdescriptiveonly, statuses/residuals/exceptions
retained, nofloatwitnessgeneration. SeparatelyfeasibleJ2subproblems are explicit
analyticfacts, not extraunfrozenfloatingcalls orjointclaim. No speed/CI/holdout.

Independentdevelopmentcontrols allsignedasymmetric/nonuniformdt/multiscenario
rows againstdirecttrajectory algebra; every firstpreviousoffset/control/slew/
terminal bound checked; explicitFarkascombinedinequalitycontradiction; strictzero
marginunavailable, kind/key/dimension/grammar/model-first/missingrefusal;
comparator disagreement andsource/runtimefailure beforeload. EarlierF3/F4 and
scenario/fieldmodulesunchangedpinned. Newassembler independent, notstatusreinterpret.

Prereg exactreview/publicationbeforeimplementation; executable/code/inputs/schema/
environment/sourcefreeze review/publicationbefore28rows/fourfloatingcalls;
resultsreviewbeforepublication. Exactfinite suppliedmodelonly, no unlistedmap/
uncertaintycontinuum/recourse/corridor/safety/hardware/physiology/inventionclaim.
Missingwitness remainsunavailable; noautosearch. Runtimecaps/pinsnotcompleteOS/
sharedlibrary/dynamicloaderprovenance, peakmemoryproof oradversarial sandbox.
