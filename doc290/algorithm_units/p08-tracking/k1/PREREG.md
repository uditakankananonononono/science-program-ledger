# K1 numerical tracking failure and atomic-state audit

Parent356726d4b42d09b81338b69602fc9b1c57723d57. TrackingREADME documents unresolved
overflow/error-contract coverage. Existing ConstantVelocity.step commits state/P
only after calculations; no robust claim follows without numerical-failure checks.
Pinnedunchangedkalman.py only, harness artifact, not newtracker/invention/calibration.

## Fixed 15 exposed calls

Default filter state[0,0,0,0], covarianceI4,q0,dt1,missingmeasurement/Runlessnoted.
Constructfilterfreshpercase, snapshotsafterconstruct/beforestep. Cases:
V1 prediction: state[1,2,3,4],P=I,q0,dt1/2 -> state[5/2,4,3,4],
 Ppositiondiagonal5/4,velocitydiagonal1,crossposition-velocity1/2,other0.
V2 observed: default,z[3,-3],R=I2 -> state[2,-2,1,-1],Ppositiondiagonal2/3,
 velocitydiagonal5/6,cross1/3,other0; innovation[3,-3],NIS6.
V3 process: defaultstate,Pzero,q3,dt1 -> state0,Qpositiondiag1,velocitydiag3,
 cross3/2,other0,missinginnovation/NIS. These3valids expectedreturn, independent
Fraction analyticarrays, npallcloseatol1e-12,rtol0; nophysicalprobabilityclaim.
E1 dt1e308; E2 state[1e308,0,1e308,0],dt2; E3 q1e308,dt2;
E4 P=1e308*I4,dt2; E5 default,z[1e200,-1e200],R=I2;
E6 P=5e307*I4,z[1,1],R=1e308*I2,dt1.
These6finiteextremes expectrefusalornonfiniteoutputdiagnostic, no predictedexception
class locked; actualtype/message/warnings retained. No exactreal-arithmetic oracle
for overflowoutcomes. Constructorfailure retained separately, notsuccessfulstep.
I1 dt0; I2 measurement[1]; I3 missingmeasurementwithR=I2. Expectedrefusal.
S1 defaultobserved z[1,1],R=I2, monkeypatchnp.linalg.solve raisesLinAlgError;
S2 same, solve returns allNaNofsecondargumentshape; S3 same, solve returns allInf.
Expectedrefusal; injectedfailurecontrols not natural solverbehaviour or resilience.
Total15calls:3valid,6extreme,3invalid,3injected. No postresultcasechanges.

Everycase retainsconstructor/stepreturnoractualexceptiontype/message, allwarnings,
state/Pbefore/afterdtype/shape/strides/C-orderbyteshex/SHA256, returnedstate/P/
innovation/NIS/observed andfinitechecks, equalityofbefore/after snapshots. Returning
NaN/Inf encodedexplicit taggedstrings notinvalidJSONnumber. Forfailedsteps atomic
contract: allbefore/afterownedstate/Pbytesunchanged. Validcalls expectedmodifyexcept
V3zero-state, stillno-mutationnotrequiredforsuccess. Allcallerinputsnotmutatedalso
checkeddescriptively, bufferidentity notsameasvaluepreservation; implementationmay
replaceownedarraysaftervalidreturn. Exceptiondoesnotbyitselfmeanpassedfailurebar.

Fixedsuccess: all3validanalytictestswithinlockedtolerance; all12refusalcontrols
mustactuallyrefuse (constructor refusal distinguished, notcalledsteprefusal), failed
stepsmustpreservebefore/afterbytes; noacceptednonfinitereturn (includingNIS).
Mismatchretainedasanobserveddefect, notpatched/reclassifiedtomeetsuccess. All15rows
retainedwithindividualexpectedactual/resultdiagnostics, noaggregatebenchmarkwinner.
Zero runtimeperformanceclaim, no stochasticCI/heldout/physiology/noisecalibration.

## Route and implementation bounds

StrictJSONinputs/finiteparameterstrings parseexplicitly, no expressioneval; exact
modelshapes/case IDs fixed, <=128KiB/depth10/duplicates/nonfinite refusal. Inputfinite
extremes canonical decimalstrings parsedfloat, notclaimexactmeasuredprecision.
Frozenprotocol/harness/test/fixture/source/executable/dependencies/versionpins;
verifyallbeforecaseconstruction/monkeypatch. PinnedNumPy Python/module/native
loadedsource identities, notcompleteOS/sharedlib/loaderclosure. OneBLASthread,
only4x4/2x2operations, all15synchronouscalls; nohardtimeout/sandbox/resourceclaim.

Developmentseparatetoyvalidprediction andmockfailure/resultserialization/atomic-
diagnostic/disagreement/sourcebeforeload controls, NOTfull15battery. No production
modulepatch exceptscopedrestoredsolveinjection insideexpectedS1-S3; kalman.pybytes
unchanged. Noextremebattery beforefreeze review/publication. Prereg review/publish,
executablefreeze review/publish,15callaudit, resultreview/publish. Alllosses/exceptions/
postfreezechangesdisclosed; no baselinefix orparameter/tolerance rescueinsideK1.
