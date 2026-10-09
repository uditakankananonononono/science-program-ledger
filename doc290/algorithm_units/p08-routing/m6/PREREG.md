# M6 disclosed durable segmented M5 timing rerun

Parentbf846e0fa2f6ee47c449e6b2f1797c534881455d is the published LOCKED M5
harness failure: outer-call execution limit killed end-only reporting, attempted
prefix/results unknown. No M5 timing or payload reused/retried/rescored; original
record immutable. Fresh M6 global run, same explicitly reused T9 corpus200cases,
three balanced fresh repetitions/600pairs/1200subjects. Notfresh/heldout/blind.
Unchanged pinned M5 timing boundary/originalT9/T8bindings, fixedclasssidecar,
summaryrules/ratio/log/nearest-rank/all3completecase/exclusions/determinism,
actualclassordercounts andone-local-environment caveats. M4negative retained.

## Frozen execution route

Replace monolithic evaluation with inspected bounded invocations of a frozen
controller. Uniqueglobal plan200x3, same(caseindex+repeat)%2 order,1200ordered
subjectslots. Fresh run directory never overlaps M5; bind manifest/runtime/plan/
corpus/class digests. No arbitrary skip/startindex/force/rescore/reset operation.

Each chunk at most20pairs/40subjects AND60seconds internal wall ceiling. Before
starting a subject require at least7seconds headroom (parent5skill/drain+storage
margin). Finish current pair when safe, otherwise return with completed durable
subject position, without starting a new one. Network/reporting outside chunk.
Chunk ceiling plus short setup lies well below120second outercap; no detached
shell jobs needed. Entire evaluation lifecycle spans tool calls with persisted
state, not a hoped-for outliving process. Per-worker timeout/nonzero is a durable
FAIL subject, not controllerinterruption; continue plan without retry.

Exclusive nonblocking run lock prevents simultaneous invocation. Before every
subject: validate ledger/plan/source/currentcoverage, atomically persist+fsync
inflight marker exactslot/case/repeat/method/order/identity. Then launch once.
After subject: atomically write+fsync immutable indexedreceipt, fsync directory,
then advance atomic+fsync next-index ledger/clearinflight. Pair completion marker
only afterbothsubjectreceipts persisted and validated. Write-before-clear crash
can leave inflight+receipt: reconcile exact complete immutable receipt without
rerunning subject. Inflight without a durable complete receipt LOCKS
FAILED_INTERRUPTED_RUN, no resume/retry of missing subject or fallback. Malformed
receipt, slot/plan/source/identity mismatch, gaps/duplicates/ledger corruption
LOCKFAIL; never silently repair bytes or infer timings. Crash aftermarker before
launch also conservatively locks, not guessing that no subject ran.

No timing duplicate even on repeated controllerinvocation. Completed run is
read-only/idempotent; alreadyreceiptedslots neverlaunchedagain. Freshness refers
to1200M6subjectcalls, not corpus freshness. No old unknown M5prefix reuse.
Atomic rename/fsync controls local durability, not arbitrary hardware/OS/power
proof. Controller failure atany point retains all durableprefixreceipts and
inflightmetadata, unknowns separate from recordedmethodFAILs. An explicit new
reviewed run is required after locked controllerfailure, never a resume override.

Final synthesis allowed only afterexact1200uniqueorderedreceipts/600pairmarkers,
noinflight/failedstate, validatedsource/plan/corpus/class identity andledgerindex
1200. Build checked rowsfrom receipts then frozen M5summarizer. Exclusionaccounting
exhausts600pairs, complete+incomplete=200cases; deterministicrepeatchecks includes
route/counters/proofs/incumbent/certificate/identity/affinity/cap. Alllosses,
failures/ties/zero/numeric/CPUexclusions retained. Slowerresults publish too.
Actualclassordercounts: no-path200/205,budget17/19,equality79/74,strictgap4/2;
aggregate300/300 NOTperclassbalance. No warmup/minCPU/no loadcontrol notstability
proof, no reliable magnitude/general speed/novelty/invention/scienceclaim.

## Required development operational proof

Synthetic non-corpus controls, no timed corpusbeforepublishedfreeze: smallplan
completion andcontinuation acrosschunks, bound/guardstop, eachslotlaunchcount1,
completedinvocation no newlaunch, concurrentlockrefusal, immutableconflict/gap/
wrongidentity/plan/order/ledger corruption refusal. Kill childcontroller midchunk
AFTER firstdurablereceipt, verify it survives; inflightwithmissingreceipt locks
withoutduplicate timing. Kill afterreceiptbeforeledgeradvance, resume ONLYby
recognizing exactpersistedreceipt andnextslot; no replay. Pairmarkerrequiresboth,
partialvalidpair survives safechunkreturn andcontinues once. Fsync/renameorder
inspected. Realcontroller/worker controls required, notmock-only assertions.
Inherited actualoriginalT9/T8BOTHFINALgate success/nonemptyforbidden andstrictgap,
malformed/kill/memory/gate controls. Freeze plan/controller/summarizer/proofs/
transitivepaths/runtime beforeany1200subject. InitialPRE-finalreceiptslabelled,
finalrealrerun aftermanifest. Classsidecar independentlyrederived, casesbyteexact.

Exactnewprereg review/publication -> executablefreeze including operational
review/publication -> segmentedone-shotglobalrun -> exactresultreview/publication.
No postfreeze method/oracle/analysis/operationalrule rescue; lockedM5 andallprior
negative/failed/rejectedhistories remain. One-shotreportedprocessnotGitproof.
128MiBAS/verifiedsingleCPU beforeworkerimports,5skill/drainonce/reap,
ASnotRSS/tree/container/OS/sharedlib/schedulerproof. Comparator/harnessartifact,
no automaticproductionintegration/clinical/physiology/providercompletion.
