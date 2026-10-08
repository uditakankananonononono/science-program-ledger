# F6 exact discrete-corridor certificate adapter

Parent9bfe14e58723130f8230c80c27f8ca90597aa759. CORRIDOR.md documents missing
independent dualcertificate forsolverstatus2; exactterminal/F4/F5 omitintermediate
stateboxes. Newvalidatorartifact fordiscreteconstraints, notnewplanningalgorithm.

Modelkeys x,target,dt,B,lower,upper,limit,slew,previous. Constantd-by-m map, node
boxeslower/upper (n+1)-by-d includingfixedinitialnode0; terminal equality separate.
Positive dt/limits, nonnegative slew, previous-in-limit, consistentnonemptyshapes,
node lower<=upper. n<=8,m<=4,d<=4. F3rationalgrammar/helpers unchangedpinned:
integernotbool<=80chars orcanonicalreducedn/d, positivedenominator,no plus/leading/
signedstringzero; integer-0normalizes0. StrictUTF8JSON128KiB/depth10/duplicate/
nonfinite refusal. Loadedruntime/source/executable/thread/versionidentity gates
beforecases/baselinecalls. No units/calibration/continuous interpolation inferred.

Freeflattenedstep-majorcontrols u, reconstructedAu<=b roworder: allactuatorupper/
lowerperstepactuator, allslewupper/lowerperstepactuator withfirstpreviousoffset,
allnode upper/lowerpernodecoordinate usingprefixsum k<node dt[k]*B[i,j], including
zerocoefficientnode0; terminalupper/lowerpercoordinate(targetequality) usingallsteps.
Nodeupperrhs upper[node,i]-x[i], lower x[i]-lower[node,i]. No F3epigraph.

Primalwitnesskind primal/keycontrolsflat -> exactassembledconstraints AND independent
control/slew/allnode/path/terminalreplay -> FEASIBLE. Farkaswitnesskind farkas/key
multipliers -> exactnonnegative/rowdimension/A^Tlambda0 andb^Tlambda<0 ->INFEASIBLE.
Wellformednonnegative stationary butnonnegativeRHS UNAVAILABLE. Missingwitness
UNAVAILABLEonlyAFTERvalidmodel; malformed/nonstationary/negative/wrongprimalINVALID.
No autosearch/directionflip/floatwitnessconversion/solverstatusproof.

## Fixed exposed fixtures and comparator

Defaultscalar B1,x0,dt[1,1],limit1,slew2,previous0,target0. Fourvalidmodels:
C1 feasibleexcursion boxesnode0[0,0],node1[1,1],node2[0,0],controls[1,-1].
C2 terminalfeasible-but-intermediate-impossible: samenodesbutnode1[2,2]. Certificate
actuatorstep0upperlambda1 +node1lowerlambda1; combinedcoeff0,RHS-1; others0.
Terminal-onlytarget0 feasiblecontrols[0,0], notcorridorfeasible.
C3 initialboxcontradiction node0[1,1],node1[-1,1],node2[0,0]. Certificateonly
node0lowerlambda1(zerocoefficients,RHS-1), others0. Validmodelwithinboxshape,
fixedinitialnotinbox is logicalinfeasibility, not malformedmodel.
C4 asymmetric2x2 nonuniform: x[1,-1],dt[1/2,3/2],B[[1,-2],[3,1]],limit[2,2],
slew[1,2],previous[1/2,-1/2],controls[1/2,-1/2,1/2,-1/2],target[4,1].
Allnodeboxes exactpoints [1,-1],[7/4,-1/2],[4,1].

Fourvalid + fourmutations each: primalC1/C4 firstcontrol+10(outbound), first0
(node/terminalwrong), removelast(shape), firstbool. FarkasC2/C3 firstlambda-1,
allzeros(noncontradictoryUNAVAILABLE), firstlambda+1(nonstationary), removelast.
Eight standalone: missingwitnessUNAVAILABLE,floatdt, badnodeshape, invertednodebox,
extra witnesskey,badkind, zero-time,signedzerolambda. OthersINVALID. 28rows total.
Four unchangedcorridor.pycallsdescriptive rawstatus/controls/residuals/exception,
nevercertificate. Allrows/digests/reasons retained. No speed/CI/holdout/ranking.

Development independentallprefix/sign/node0/terminal/control/slewrowresiduals on
signed2x2/nonuniformdt/asymmetricpreviousmodel, strictFarkascontradiction/zeroRHS/
negative/nonstationary andinitialzerorow, validpathreplay plusintermediate-only
violatingwitness, keys/shapes/grammar/model-first; source/runtimebeforeloadrefusal
and comparator disagreement. EarliermodulesF3-F5/corridor etcunchangedpinned.

Prereg review/publicationbeforeimplementation; executable/schema/code/inputs/env/
sourcefreeze review/publicationbefore28rows/fourfloatingcalls; resultsreviewbefore
publication. Exactsuppliedmodeldiscretenodes only, no continuous-timecollision,
anatomy/hardware/physicaltruth/invention/sciencegate. Noautomaticcertificatefind.
Runtimepins notcompleteOS/sharedlib/loaderprovenance; capsnotpeakmemory/sandboxproof.
