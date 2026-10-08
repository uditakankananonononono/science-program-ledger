# Unit161 recording-prefix endurance pivot: DEV candidate closure

Verdict: DROPPED-DEV-candidate / NULL, observed-effect power gate fails. Headroom exists; this candidate did not improve it. No TEST outcomes, final-stage lock or push. This is a same-dataset SECOND LOOK following the archived timed-RPE negative.

Boundary: first10seconds of the PROVIDED RECORDING origin, whose relationship to task onset is UNVERIFIED. Do not call this early-task prediction, before-fatigue measurement or causally deployable endurance prediction. Prior sensor-end/endurance discrepancy [-0.166,+12.080]s, median2.899s outsideflaggedpartial is not start metadata. Recordingoriginprefix can include preparation; no normalizedfilelength or trueendurance alignment. NativeTask_Times target only. No synchronizedRPE claim.

Precompute protocol/code freeze was explicitly granted by parent October8,2026 16:16:09IST. PREREG_ENDURANCE_DRAFT.md SHA256 b6f1ed33b2c3315726abbe043fc9f4474b6cfaf81cd09f37efb9eda6999a7670; run_endurance.py SHA256 4b2cd767296846c4b56a99a534774d34775c5a2c8d4b19d7ec4f62b63aa88cee. Original code submission had a SyntaxError, explicitly rejected and corrected before this lock; neither failed version nor candidate was executed before lock. These exact hashes were rechecked before execution. No amendment after results. DEV lock only, not permission for TEST.

## Eligibility
16DEVsubjectclusters,125subjecttasks, allprefixquality checks pass. MissingSub7/StSh25, partialSub11/StEl45 and commentflaggedSub21/StEl25 excluded, per commentcolumn+fill policy. Target distribution afterthese exclusions: median90s, IQR60-130s, range11-462s, n125. Parent5sabsoluteWINband conditionmedian>=60s metbeforelock. NumericalnaturalDEVoddSub3..33; TESTeven4..34sealed.

## All DEV outcomes
Nested4outer/3innerGroupKFold bysubject; equalweightsbysubject(andtaskwithin eachsubject), RFseed161.

| Run | Strongest selected baselineMAE(s) | CandidateMAE(s) | NullMAE(s) | Gain(s) | Subjectbootstrap95%CI |
|---|---:|---:|---:|---:|---:|
| Real, perm=false | 42.1326 | 42.2607 | 47.0313 | -0.1281 | [-5.9077,+5.9161] |
| GlobalDEVshuffle, perm=true | 51.7996 | 48.6418 | 45.0513 | +3.1578 | [-0.9067,+8.2207] |

Gain=baseline-candidate, lowerMAEbetter. No gain>=5s withCI lower>0 in either run. Permutedmodels do notbeatnull: cleannoskillsmoke, notproofofperfectlabelsecurity. Noise-inducedmodel-overfit can yield apparentrelativegain3.16s; recorded atsameprominenceasrealresult. Onefixedseedpermsmoke, notrepeateduntilclean.
Sixof16subjects improve inrealrun, tenworsen. Selectedrealbaselines perouterfold: halvesridgealpha100, rawridgealpha100, metaridgealpha10, metaridgealpha100. Candidate ridgealpha100, RFleaf5, ridgealpha100, ridgealpha100. Grid-edgealpha100/leaf5 reported, noextension. Allfolds/grids/predictionsattached.
The strongestbank includes metadata+rawprefix+bothhalves, so candidatehasnotwon fromextraacquisition. Itisactivationproportionsanddrift featureengineering, notnewphysics/sensor. Baselinehasmodestskill4.8986s vsmedianconstantnull and42.1326>2x5s: headroomgate passes, not universalinformationlimit.

## Power at16subjects
Label-free assumednormal subject-error differences, effectfixed5s,10000drawsseed161. AssumedSD5/10/20/40s yields positivepairedtintervalpower .9609/.4628/.1520/.0673; FULL WIN includingpointestimategain>=5s yields .5000/.4226/.1520/.0673. At trueeffectexactlytheband, pointestimateconstraintcaps fullWIN around50%; significancepower alone is not the fullWINprobability.
SelectedDEVobservedeffect -0.128s givesoptimisticpositiveintervalpower .0237; approximate80%-significanceMDE9.6665s. Candidatefails beforeTEST. Thisdoesnotproveallmethods impossible or thatthe datasetcannot supportlargereffects. OOFclusterbootstrapdoesnotmodeloverlappingtrainingcovariance, soCIareexploratory, notconfirmatoryTESTinference.

## Provenance, priornegative and closure
ExactZenodo15172815 displayedv5/APIindex4; original13771675 displayedv3/APIindex2. FullarchivepublisherMD5 6a29192232b45d1f59ef16cf45c09145 matched23,571,527,628streamedbytes; seven smallfilespublisherMD5 matched. Extracted127DEVEMGfiles exactchunkSHA/CRC/localSHA readbackverified, rawsignalsnotinpacket. CC BY4.0 API+README. Includedtimed-RPE closureZIP alreadycontainsfullreceipts/sourceledger/split/quality/alignment/code/versions; thispacket nestsit unchanged. LocalSHA256 notcalledpublisherSHA. Fullsuppliedclaimssnapshotread; latestregistryreconciliation belongsparent/holder, no sharedledgerwritehere. Oneadvisoryjudge roundpending. No thirdcandidate/retuning, TEST, pushes, browserleaseormonitor remains. NegativeRPEandNULLendurance findings given equalrigorandprominence.
