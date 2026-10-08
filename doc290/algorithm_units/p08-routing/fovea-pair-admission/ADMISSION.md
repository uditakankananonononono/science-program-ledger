# FOVEA paired connectivity: data and measurement-design admission

2026-10-08. No new algorithm implementation, query scoring or novelty claim. Existing
QC diagnostic aggregation only. Proposed query protocol UNEXECUTED, admission review
required before any measured query-disagreement statement. No anatomical consensus.

## Current source/byte/pairing validation

Live TLS JSON https://api.figshare.com/v2/articles/28329338 confirms version1, dataset
license name CC BY, https://creativecommons.org/licenses/by/4.0/, download_disabled=false,
file52512728 FOVEA.zip size3104936839 and supplied/computed MD5
36ca4a0cf119a63f8ff14de7a30ad91b. API web-fetch returned unexpected content type;
separate urllib TLS JSON read succeeded. Original 3.1GB archive NOT redownloaded or
MD5 recomputed today. Correspondence to publisher original rests on prior transfer
manifest evidence, not independent current full-original verification.

Current transferred mask-only ZIP CRC passes; SHA256
1931a07b2fad3d34a5f77409bd12238c4d131058fed635f32839d92466e54e38.
All160 per-mask byte sizes/SHA256 match transferred manifest; exactly80 patient-phase
groups, each annotator1+2,40 patient IDs. No raw annotation, image, optic-disc or video
byte admission expanded by this unit. Source naming and pairing verified against:
https://www.nature.com/articles/s41597-025-04965-2
Article confirms two independent clinical research fellows, no annotation consensus,
FOVEA001..040, preoperative p and intraoperative i, and separate annotator suffix.
Phases are same patients but images differ in orientation/scale/FOV; do not register
pre-vs-intra by common pixel coordinates. Only WITHIN-phase pair masks share image.
Dataset CC BY differs from article CC BY-NC-ND. No article figure adaptation imported.

Article already reports inter-annotator Dice, widths, skeleton coverage and thin-branch
ambiguity; merely measuring those again is NOT a new discovery. It also cautions that
intersection becomes fragmented for thin branches and does not qualitatively rank
annotators. Union/intersection are annotation combinations, not anatomical truth.

## Existing frozen QC diagnostic, not new query experiment

paired-existing-qc.json projects original full_extraction_qc.jsonl (hash recorded in
JSON); no masks re-extracted, endpoints routed or components recomputed. Both masks
passed original exact binary/extractor contract. Preoperative:8/40 paired images have
different 8-neighbor skeleton component counts; intraoperative:3/40. All80 pair rows
retained. These are80 phase pairs over40 patients, NOT80 independent patients,160
independent labels or CIs. Equal component count does not imply same connected sets,
paths/cycle structure/anatomy. Pixel connectivity is representation-specific.

Distribution (A1,A2): p:30(1,1),4(1,2),1 each(4,1),(4,2),(1,3),(3,1),(3,3),(2,2).
i:37(1,1),3(2,1). This establishes a real paired representation disagreement surface,
not query reachability disagreement or meaningful vascular disconnection rate.
Existing whole-QC provenance remains legacy without later archive/pipeline binding;
this memo does not retrofit it. Current mask hashes matched manifest; query protocol
will bind exact bytes/pipeline separately if admitted. All masks previously exposed
development data; no untouched test set or held-out claim.

## Proposed query endpoint protocol (design, not measured)

1. Use unchanged exact extraction (binary contract, Zhang skeleton,8-neighbor graph),
with source/pipeline/version and all input hashes pinned in a separately reviewed
executable+manifest before running queries. No annotation repair, threshold changes,
training or topology modification. Every patient-phase pair retained.
2. Primary endpoints are EXACT common skeleton pixels S1 intersect S2. Sort row,column
lexicographically; if M>=2 select up to16 endpoints at indices
floor(j*(M-1)/(K-1)), j=0..K-1, K=min(16,M). All K(K-1)/2 distinct unordered pairs.
If M<2, classify pair image insufficient_shared_endpoints, NOT zero disagreement,
not missing target=unreachable. Record M,K and coverage of both skeletons.
3. Query reachability in each original skeleton graph. For each endpoint pair, return
both_reachable, A1_only, A2_only or neither. Connectivity-only, no travel-time/flow
or shortest-path physical metric. BFS/component lookup established method, not
invention. Record endpoint component IDs and witness route only if later specified.
No nearest-mask projection in primary workload; no matching unequal pixels silently.
4. Report all raw patient/phase/endpoints/classifications and per-image numerators/
denominators. Keep phases separate and patient grouping explicit. No pooling pixel
queries as independent samples, no significance/CI claim from this deterministic
chosen workload. Shared-skeleton selection is biased toward overlap; its disagreement
rate cannot estimate all anatomical queries or annotation errors.
5. Nearest-mask projection is a DEFERRED alternative design: would require distance
cutoff,tie-break,semantic target validity,missingness and registration justification.
Do not mix it into primary results or treat off-mask as unreachable. No query workload
run until design/executable approval and publication. This plan maps only a restricted
representation question, not all branch correspondence disagreements.

## Fetched comparator/prior-art screen

P1 FOVEA primary article, above: already compares annotators, intersections, skeletons
and ambiguities. Prevents claiming paired disagreement itself as invention.

P2 clDice (CVPR2021), full primary paper:
https://openaccess.thecvf.com/content/CVPR2021/papers/Shit_clDice_-_A_Novel_Topology-Preserving_Loss_Function_for_Tubular_Structure_CVPR_2021_paper.pdf
Skeleton/mask intersection similarity and topology-preserving training objective.
Reported homotopy guarantee has assumptions, not universal ground-truth anatomy or
certification of our masks. Not a plug-in robust routing baseline; no training here.

P3 Ensuring a Connected Structure for Retinal Vessels Deep-Learning Segmentation
(ICCVW2023), full primary paper:
https://www.openaccess.thecvf.com/content/ICCV2023W/CVAMD/papers/Dulau_Ensuring_a_Connected_Structure_for_Retinal_Vessels_Deep-Learning_Segmentation_ICCVW_2023_paper.pdf
Vessel network retrieval/postprocessing and connected-component/path evaluation.
Discusses1000 connected paths per test image for another method. Query/path connectivity
metric or sparse reconnection alone not a new algorithm. Forced connectedness is not
verified anatomy; our memo does not admit these trained model outputs/weights.

P4 Fully automated tree topology estimation and artery-vein classification (2022),full:
https://ar5iv.labs.arxiv.org/html/2202.02382
Explicit2D crossing ambiguity; graph contraction, topology estimation, high-level
operations including detach/endpoints/flow direction with appearance/AV models.
This local mask-only dataset does not provide that information or anatomical truth.
No crossing reconnection/flow invention claim admitted from masks alone.

P5 Distance-Constraint Reachability Computation in Uncertain Graphs (VLDB2011),full:
http://www.vldb.org/pvldb/vol4/p551-jin.pdf
Possible-world reachability, independently existing probabilistic edges. Two correlated
expert segmentation hypotheses are NOT calibrated independent edge probabilities;
no p=.5 inferred just because one of two annotators includes a pixel/edge.

P6 An In-Depth Comparison of s-t Reliability Algorithms (VLDB2019),full:
https://www.vldb.org/pvldb/vol12/p864-ke.pdf
Reliability sampling/indexing and possible-world methods established; explicit
independent-edge model and complexity tradeoffs. Not guaranteed transfer to correlated
label worlds or small two-world enumeration, which is elementary itself.

P7 ProbTree: A Query-Efficient Representation of Probabilistic Graphs (2014),full:
http://www.sigmod2014.org/buda/papers/p1.pdf
Query-oriented graph representation for probabilistic source-target tasks. No novelty
in query-specific preprocessing by itself, no performance transfer to these masks.
Seven fetched primary sources; publication + source metadata/code/QC evidence used.
Community opinion not needed for technical admission. No imported external code/model.

## Potential claim admission and next decision

No algorithm invention ADMITTED. Generic intersection/union/possible-world reachability,
component lookup, connectivity metrics and reconstruction repairs already established.
Reject generic certificate saying "both observed graphs contain a path" as new: it is
finite hypothesis checking, not anatomical confidence or statistical calibration.

Data-tied research question that survives as a QUESTION, not a novel claim: after
fixed common-endpoint queries, does paired annotation disagreement yield a concrete
query-dependent ambiguity pattern not captured by component counts/pixel Dice?
Potential future algorithm would need a specific new query-local representation,
exact uncertainty/repair objective and proven property versus established graph/path
baselines. Actual query pattern unmeasured, so cannot name that claim honestly yet.
No implementation until this admission/design memo review. If protocol admitted,
first work is a frozen diagnostic measurement using established methods, not a
claimed invention or comparative superiority score. Stop if only established
composition is found, retain negative admission and avoid artificial abstraction.
All anatomy/flow/cost/calibration/novelty gates stay OPEN.
