# K1 numerical tracking audit result: locked aggregate FAIL

Publishedfreezedd68dbf22745a3176da22145572c8bf0569c8dd1/tree
3d244e6e7b6fe81d813fd1e4c578651b9f5175d9. Allsource/runtime114/thread/version
gatespassed before15productioncalls. Publish-before-scoring tool-log recorded,
notestablished solely by this text or replay. Unchangedproductionkalman.py.

14PASS/1MISMATCH underLOCKEDrule; overall strictsuccess NOTmet. All15calls retained
withwarninglists, snapshots/bytes/hashes/metadata, callerchecks, actualreturns/
exceptions/finitechecks. Noexceptiontype/tolerance/inputreclassification orrescore.
V1/V3valid PASS; V2validMISMATCH from covariance oracle only. State/innovation/NIS/
observedagree, everyreturnedfieldfinite, nowarnings. LockedV2oraclevelocitydiagonal
5/6 differsfromactual2/3 (bothvelocitycoordinates). KeptasMISMATCHandaggregateFAIL.

Diagnostic attribution, not rescue: forV2 eachaxis Pminus=[[2,1],[1,1]], H=[1,0],
R=1, S=3, K=[2/3,1/3]. Posterior Pminus - [2,1]^T[2,1]/3 hasvelocityvariance
1-1/3=2/3, not5/6. Thus preregclosed-form V2oracle contains a builder arithmetic
error; returned2/3 matches statedKalmanmodel inthis directcalculation. This is not
anobservedproductiontrackingdefect. Parentreview initiallysaid expectationsagree;
thatdoesnotchange lockedoracle. Nofixture/codefixinsideK1. Any correctedfreshunit
needsnewprereg/freeze/review, not silentlychanging this loss into PASS.

All12refusalcontrols were actualSTEPexceptions, ownedstate/Pbyte+metadataunchanged:
E1OverflowError; E2FloatingPointError; E3ValueError(predictionoverflow);
E4/E5/E6FloatingPointError; I1/I2/I3ValueError; S1LinAlgError;
S2ValueError(updateoverflow); S3FloatingPointError. Exactmessages retained.
Constructorrefusals0; acceptednonfiniteoutputs0; warningcount0; callerarraysall
preserved. This supports boundedfailed-stepatomicityinthesecases, notallpossible
numericfailures/constructors/externalbufferaliases/generalnumericalreliability.

No postfreezechanges/drop/patch, allsolveinjectionsrestored. Sevenseparatedtoy
harnesstests pass. SnapshotCcopies/stride/dtype/shape/hex/hash andnonfinite-tag
serialization retained without erasing rawfiniteverdicts. Caps/runtimepinsnot
completeOS/sharedlib/dynamicloaderclosure orpeakmemory/sandbox/timeoutproof.
Exposed4x4/2x2softwareauditonly, noheldout/CI/speed/physiologicalnoise/calibration/
benchmarkwin/newtracker/invention/sciencecompletion. Numericalrefusal+atomicity
positivescarried honestly alongside frozenoraclefailure; K1overall remainsFAIL.
