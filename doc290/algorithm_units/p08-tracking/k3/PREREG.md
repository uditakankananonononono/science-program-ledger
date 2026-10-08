# K3 metric numerics/missing-truth/input-preservation audit

Parent000e51dbcaf1c6339268cba078b81184695007fa. README metrics contract: excluded
missingtruth/count/None semantics, covariancevalidation evenexcludedrows. Broad
numerical/errorcoverage unresolved. Pinnedunchangedmetrics.py/kalman.py, no K1/K2
rescore; theirlockedFAIL records retained. Artifact audit, notnewtrackingalgorithm.

## Fixed12 exposed calls and exact arithmetic

DefaultN1 truth[[0,0,0,0]],estimate[[3,4,0,0]],P[I4],availability[true].
V1 default: squaredpositionerror25 -> RMSE5; velocity0; NEES25,meanNEES25;
 total1/scored1/excluded0. Exactinteger/Fraction derivation, notGaussian calibration.
V2 N2 truthzeros,estimates[[3,4,0,0],[0,0,0,5]],P[I4,2I4],availabletrue,true:
 positionRMSE sqrt(25/2),velocityRMSEsqrt(25/2),NEES[25,25/2],mean75/4;
 total2/scored2/excluded0. Compare positiveirrationalRMSEviaindependentmath.sqrt
 of Fraction25/2 float, not inventeddecimaloracle; atol1e-12/rtol0 allnumbers.
V3 N2,truthrow0zeros,row1allNaNexplicitfixturetags; estimates[[3,4,0,0],[1,2,3,4]],
 P[I,I],availabletrue,false: RMSEposition5,velocity0,NEES[25],mean25;
 total2/scored1/excluded1. Excludedtruthnonfiniteallowed, notzero-filled.
V4 N1 truthallNaN, estimate[3,4,0,0],P[I],availablefalse:
 total1/scored0/excluded1,position/velocity/meanNEESNone,NEES[]; nofalseperfectscore.

R1 defaultavailability[1]numericnotbool ->REFUSE.
R2 defaulttruthfirstNaNandincludedtrue ->REFUSE.
R3 V3butexcludedrowcovariancezero4x4 ->REFUSE (allrowsvalidatedincludingexcluded).
R4 defaultsingularPzero4x4 ->REFUSE.
R5 defaultestimate[1e200,0,0,0] ->REFUSE. Exactpath: error1e200,identitysolve
 gives1e200; error^Tsolveerror=1e400 exceedsbinary64max~1.8e308, overflowunder
 errstate inNEESmatmul; evenifimplementationorderchanged, error^2 RMSEsameoverflow.
R6 defaulttruth[-1e308,0,0,0],estimate[1e308,0,0,0] ->REFUSE. Error subtraction
 outsideerrstate computes2e308 (>binary64max), likelywarning/Inf; later NEESdot
 nonfinite and/orRMSEpowers leadexception or metricfinite-refusal. Mustactually
 refuse; allwarningsretained, exceptiontypeNOTlocked. Notassumelargealonebad.
S1 defaultnp.linalg.solve raisesLinAlgError; S2 defaultsolve returnsNaNsameRHSshape.
BothREFUSE; noS3Infextraoutside12. NaNNEESmean leadsmetricfinitecheckrefusal, not
successfulscore. Total12:4valid+6invalid/extreme+2injections.

## Locked verdicts and preserved evidence

Everycallretainsactualreturnoractualexceptiontype/message,warningsaroundwholecall,
genuine4inputbuffers before/after(dtype/shape/strides/C-orderbyteshex/SHA), allcaller
inputsunchanged. Returnfinitechecks position/velocity/eachNEES/meanBEFOREtagged
serialization; NoneexplicitperV4. Counts/NEESlength/order/None exactsemanticcheck;
numericoraclesV1-V4 independentFraction/sqrt, notproductionmetricsreplay. All12rows
retainedinputdigests/expectedactual/assessment. FourVALIDmustmatchallfields/finite/
inputpreservation; eightREFUSEmustactuallyEXCEPTION/inputspreserved. Anyfinite
unexpected/nonfiniteaccepted/inputmutation/oracleerrorMISMATCHandaggregateFAIL,
no exception/tolerance/parameterreclassification. Constructorstageabsent.

Strictsuccess12PASS only. No score correctionafterfreeze; K1wrong5/6oracle and
K2unsupportedR4refusalexpectation lessons inform THISnewprospectivescope, nottheir
rescoring. Alllosses/warnings/exceptionsandpostfreezechangesdisclosed. No NEESchi-
square/independence/physiologicalnoise/calibration/benchmarkwin/invention/CI/holdout/
scienceclaim. Suppliedcovariancespositive-definitecontract notcalibrationtruth.

## Route/bounds

StrictJSON128KiB/depth10/duplicates/nonfiniteconstantsrefused; NaNintentionaltruth
explicitfixturetag onlyV3/V4/R2. Decimalfiniteextremescanonicalstringsconvertedfloat,
noexpressioneval/measuredprecisionclaim. AvailabilityboolornumericR1 preserved
asactualdtype, notcoercedbool. N1/2,4states,4x4Pfixed. Source/runtime/executable/
loadedNumPy/module/native/version/threadpins BEFOREinputconstruct/injection.
Warningswholecall, solvepatchcontextrestoredallexits. RuntimepinsnotOS/sharedlib/
dynamicloaderclosure,capsnothardtimeout/peakmemory/adversarialsandboxproof.

Developmentseparatetoycounts/None/finite-tag/snapshotmutatingfailure/restore/gate/
comparator-oracledisagreement controls, NOT12productioncalls. Prereg exactreview/
publishbeforeimplementation; executable/schema/fixtures/source/environmentfreeze
review/publishBEFORE12calls; resultreviewbeforepublication. Productionunchanged.
