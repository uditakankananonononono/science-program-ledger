# K2 offline RTS numerical/refusal/input-isolation audit

Parentec92f1d18f840223cbc548d7929c70ee5fd825b4. Documented smootherREADME/function
contract: independentreturnedarrays, unchangedallinputbuffers, singularpredictions
unsupported, inconsistentnegativeoutputsrefused. K1retainedFAILunchanged, norescore.
Pinnedunchanged smoother.py/kalman.py, offlinefuturedata NOTcausalcontroltracker.

## Fixed12 exposed cases

Inputs filteredmeans(N,4),filteredP(N,4,4),predictedmeans(N-1,4),predictedP(N-1,4,4),
transitions(N-1,4,4). DefaultN2, filteredmeans[[0,0,0,0],[2,-2,4,-4]],
filteredP[I4,I4],predictedmeans[[0,0,0,0]],predictedP[2I4],transition[I4].
V1 defaultvalidtwo-timeconditioning: gain1/2I, smoothedmeans[[1,-1,2,-2],[2,-2,4,-4]],
smoothedP[3/4I,I]. Terminalidentity explicit in fullarrayoracle.
V2 single-record: filteredmean[1,2,3,4],filteredP[I],otherthreearrays emptybutproper
shapes; identicalmean/P independentcopy, notviews.
V3 prediction-onlyconsistent defaultbutlastmean[0,0,0,0],lastfilteredP2I:
smoothedmeans0,smoothedP[I,2I]. These3closed-formoracles Fraction-derived,
lockedatol1e-12/rtol0, allfieldfinite; no recordconsistency/physicalcalibrationclaim.
R1 singularpredictedPzero; R2 nonfinitefilteredmeanNaN (intentionaltaggedinput);
R3 inconsistentnegativeoutput: defaultfilteredP[5I,I],predictedP[2I];
R4 finiteextremefilteredmeans[[1e308,0,0,0],[-1e308,0,0,0]];
R5 defaultfilteredP[1e308I,I],predictedP[I],transition2I;
R6 wrongpredictedmeansshape[[0,0,0]];
S1/S2/S3 defaultwithscopednp.linalg.solve raiseLinAlgError/NaN/Inf sameRHSshape.
All9expectedREFUSEactualexception, exacttype/message retained; anyacceptedfinite
unexpected/nonfiniteorinputmutation MISMATCH. No exceptionclass preselected.

All12rows retained: actualexceptionorreturn, warningsaroundwholecall, genuine
before/aftercopiesforallfiveinputarrays(dtype/shape/strides/C-orderbyteshex/SHA),
finiteoutputflags beforetaggedserialization, outputshape/oraclematch, aliasflags
shares_memoryoutputsversusallinputsandeachother, outputmutationisolation. Store
returnedvalues/snapshotsBEFOREisolationprobe: mutatefirstmeansscalar thencheck
allinputbytes/Poutputunchanged; mutatefirstPscalar thencheckinputs/meansunchanged.
Restoreoutputvaluesafterprobe. Refusalrequiresallinputbytesunchanged; validrequires
alloracle/finite/inputpreservation/noalias/probe checks. Constructorstageabsent,
functionvalidationfailure iscallrefusal, notcallerstaterecovery. No assertionthat
exceptions imply generalnumericalreliability. Zero-rowN1emptyshape explicitfixtures.

Strictsuccessall12PASS underlockedrules; losses/oracleerrorsretained, nofixture/
tolerance/parameterfix or productionpatchafterfreeze. No clinicalnoise/imaging/
calibration/benchmarkwin/invention/CI/blindholdout/sciencegate. Pureexposedsoftware
contractchecks, future-data estimator notreal-timecontrol. SuppliedGaussianrecords
not independentlyvalidated experimentaltruth.

## Route and bounded implementation

StrictJSON128KiB/depth10/duplicates/nonfiniteconstantsrefused; controllednonfinite
inputencodedexplicitNaNtag onR2 only, noarbitraryeval. Finiteextreme decimalstrings
explicitfloatparse, notmeasuredprecision. ArrayssmallN1/2 only, exactshapeprotocol.
Fullsource/runtime/executable/module/version/threadpinsbeforecaseconstruction/
injection. NumPynative/smootherdependency loadedsource identities, notcompleteOS/
sharedlib/loaderprovenance. Scopedsolvepatchrestoredoneveryexit. No hardtimeout/
peakmemory/adversarialsandboxclaim. Seven-ishseparatedtoydevelopmenttestscover
snapshots/finite-tagging/mutation/aliasdiagnostic/refusal/restore/gate, NOTfull12calls.

Prereg exactreview/publishbeforeimplementation; executable/fixtures/oracles/schema/
environment/sourcefreeze review/publishBEFORE12productioncalls; resultreviewbefore
publication. Existingproductionmodules unchanged. Everywarning/loss/exception/
postfreezechangedisclosed. K1priorlossneverremovedbyK2.
