# K2 offline RTS numerical/isolation audit: locked aggregate FAIL

Publishedfreezed24602b28106f6d5324ca85217d8d92eeabbba74/tree
9f6418c73cf7ecaf609b1ef743e9dc80378da050. Source/runtime114/thread/versiongates
passedbefore12productioncalls. Publish-before-scoring tool-log recorded, notproved
solelybythistext/replay. Productionsmoother/kalman/metrics unchanged; K1FAILretained.

11PASS/1MISMATCH underLOCKEDrule, overall strictsuccessNOTmet. All12rows retained
with actualreturns/exceptions,warnings,genuine5inputbuffersnapshots/bytes/dtype/
shape/strides/SHA, outputfiniteflags/shape/oracles/alias/probes. All3validPASS:
V1two-timeFractionoracle, V2single-recordemptyshapesindependentcopies,
V3prediction-onlycovarianceidentity. Allvalidshape/finite/oracle/noalias/cross-
isolationprobesPASS, actuallychangedlarge/zeroelementsrestoredbyteidentically.

Eightofnineexpectedrefusals actuallyEXCEPTION/inputspreserved. R4expectedREFUSE
actuallyRETURN, thereforeMISMATCH retained (finite-but-unexpected), notrescued.
R4meansfirst[5e307,0,0,0],last[-1e308,0,0,0], covariances[.75I,I]; allfinite,
noalias, inputpreserved and isolationprobesPASS. Diagnostic attribution: transition
I,gain1/2, predictedmean0. Backwardcorrection is1e308 + .5*(-1e308-0)=5e307,
which staysfinite. OppositefilteredmeansdoNOTrequiretheir differenceinthisformula;
prereg builder expectedrefusal withoutgroundedoverflowarithmetic. Not evidenceof
productiondefect. Frozenrefusalexpectationstillfails; no parameter/input/oracle/
exception/tolerancechange orcorrectedscore. Freshfollowupneedsnewprereg.

Actualrefusaltypes/messages: R1ValueError(predictedPpositive-definite),
R2ValueError(filteredmeansfinite),R3ValueError(smoothedPPSD),
R5FloatingPointError(matmuloverflow),R6ValueError(predictedmeanshape),
S1LinAlgError(injected),S2ValueError(smoothingoverflow),
S3FloatingPointError(invalidmatmul). Exactmessages retained. All12inputspreserved,
warningcount0, acceptednonfinite0. Solveinjections restored, no postfreezechanges/
droppedlosses. SevenseparatedtoytestsPASS. Boundedinputpreservation/isolation
positives don't establish allerrorpaths or numericalrobustness.

Offlinefuture-dataestimator notcausalcontroller; suppliedGaussianrecordsnot
physicalcalibration/independenttruth. Noinvention/benchmarkwin/CI/blindholdout/
physiology/sciencecompletion. RuntimepinsnotOS/sharedlib/loaderclosure;
capsnotpeakmemory/adversarialsandbox/hardtimeoutproof. HonestlockedFAIL retained.
