# M6 durable segmented timing freeze candidate

Prereg17e563ad72896c773f93976fd95b4031b7a3b36a, lockedM5failurebf846e0fa2f6ee47c449e6b2f1797c534881455d citedunchanged.
Freshglobal1200slots, oldunknownM5prefixnotreused. T9corpus reused200cases,
M5timing/analysis/classrules unchanged; explicitoriginalbindings. Subjectreceipt
validator replays original checked stdout/schema/oracle/witness/proofs/identity,
no solverrelaunch. Atomic fsync file+directory, immutable receipts; POSIXflock
heldduringreconciliation/launch/synthesis,releasedonprocessdeath,no lockunlink.

Crashmatrix tested: receiptpersisted/ledgerold/inflightpresent; ledgeradvanced/
inflightpresent; receiptpersisted/inflightabsent; bothreceipts/pairmarkerabsent;
partialpair safechunkreturn; completednoop; inflightunreceipted locksFAIL; corrupt/
truncatedreceipt/ledger, wrongsource/order/input/slot/coverage,foreignfilesfail.
Validcrashtransitions reconcile exactstoredreceipt withoutoverwrite/relaunch;
bothreceiptvalidated beforepairmarker; FAILsentinelstopsfutureinvocations.
Setup/source validation timer begins beforecontext, notresetbeforelaunchbudget.
Chunksmax40subjects/20pairs,60sinternalceiling/7sheadroom; ordinarychunks fit
wellunder120scap, NOTabsolute bound on kill/drain/fsync/setup/storage/synthesis.
Outerinterruption preservesprefix; uncertaininflightneverretried. Atomictemp
bytesneverpromoted/trusted; onlyrecognizednames allowed. Finalsummary separate
lockedinvocation, exact1200/600coverage/ledger/noinflight required, atomicimmutable
report and DONE; interruptionidempotent, reportbytesneveroverwritten.

Real synthetic subprocess kill/continuation/concurrency/death-release controls
show savedreceiptbytesunchanged, eachslotlaunchedonce, repeatedreconcile no
newtiming. Guardstop/chunkelapsed andfullscale validation/synthesis measurements
inoperational-evidence.json (synthetic/devreceipts, NOT1200corpusmethods).
InitialdevsuccessPRE-finalmanifest immutable; realBOTHFINALgate rerun required.
No timedcorpus beforepublishedfreeze. One-localenvironment/no-warmup/minCPU/
classorderimbalance/no stablemagnitude inference; slowerresultspublish.
M4slower446/600negative andallfailures/rejections remain, no invention/science/
productionclaim. No hazard-elimination-by-construction absolutepromise.
Afterreview/publication: controller.py chunk /tmp/m6-frozen-run repeatedly,
thencontroller.py finalize /tmp/m6-frozen-run. Eachinvocationinspected, no retry
ofreceipted/uncertainslot. Completionrequiresexactallreceipts thenresultreview.

Pre-freeze fullscale synthetic DEV-receipt benchmark hit outer cap because saved
receipt validation rehashed entire pinned source inventory for every receipt.
No corpus timing/M6freeze existed. Repaired parser accepts an already validated
identity only inside controller invocation after actual gate; receipt source
identity still exact-bound, every payload/oracle/witness/proof rechecked. Live
worker launch retains its independent gate. Fullscale validation/synthesis must
be measured again in separate bounded development invocations before readiness.

Measured source/parser DEVreceipt cost before0.0177346774s vs single-invocation
sourcegate0.0003220141s perreceipt; context0.040346475s. All prior/newreceiptbytes
andexactslot/case/repeat/method/order/input/source plusfullcheckedpayload are
reverified EACHinvocation, no trusted incrementalprefix/cache. Canonicalencoded
binding rejects bool/float value-equality in entries. Synthetic1200-slotDEVreceipt
storage/revalidation maxchunk6.349389115s, finalsynthesis5.133545946s,
repeat6.3830499s, reportbytesunchanged. These are size-controls, notcorpus timings,
not absolutecapguarantees. No source/proof validation skipped. All actual future
chunkelapsedtimes retained and inspected; sourcepreflight refusal consumesno slot.

REJECTED freeze301ea612192af0b4db7e206cd4f980e6f9987507 retained UNEXECUTED:
review reproduced saved result.worker int0->False andrssint->equalfloataccepted
by Python checked!=result despite unchangedstrict stdout. Repaired controller
compares canonical serialized reconstructedcheckedresult toserializedsavedresult,
notPythonvalueequality; every savedworker/check/counter type binds tostdout.
Realpersisted non-corpusworker receipt mutations bool/equalfloat counter/rss/check
withstdoutunchanged nowdurableFAIL before newlaunch, repeatedinvocationlaunchesnone.
No corpusmethods/evaluation/refreeze-rescore, original rejectedcandidate retained.

Operational scope disclosure requested in rereview: real kill tests kill the child
CONTROLLER with a synchronous synthetic execute, NOT an actual long-running
solver subprocess killed mid-call. They establish receipt-boundary recovery and
no duplicate launch, NOT absence of an orphan worker after arbitrary controller
kill. Missing receipt still locks, so no retry/double-timing path. No absolute
lifetime/crash guarantees. Arbitrary interruption during setup/fsync can fail
closed, not seamless resume.
Reviewer minimal-synthetic real-filesystem1200-slot benchmark: maxchunk0.721s /
final0.302s /repeat0.270s, no duplicates; NOTfullpayloadcost. Prior copied-DEV
fullpayload6.349/5.134/6.383s are observed artifacts, not independently reproduced.
Postcanonicalrepair sizebenchmark repeats below retained as separate measurements,
not substitutes for actual runtime or broad safetyproof.

Postcanonicalrepair copied-DEV fullpayload1200slot benchmark actual maxchunk
5.964506318s, final5.499309416s, repeat6.030794767s, context0.057108054s;
immutable reportbytesunchanged. All30elapsedchunkrecords retained in
repaired-size-evidence.json. Syntheticpayload/devinputs, nottimedcorpus subjects.
Reviewer minimalnumbers above are attributed to parent's08:11:12 review relay;
our independently observed fullpayload benchmark is separate, no authorityclaim.
