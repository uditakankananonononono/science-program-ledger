# P3 locked frozen evaluation failure

Freeze2ec6d251ce2162b7c354bfae9caaa075bedcf5d2 published before scoring.
First random000 variant worker was launched; parsing its successful payload in
core.launch reached undefined integer(payload['rss_kib']) and raised NameError.
The parent comparator terminated with rc1; no report.json was written. There is
no retained successful first-worker payload/rc because launch raised before
returning its in-memory record. First subject launched, remaining211 NOTATTEMPTED;
all-attempt protocol unmet. Do not call any of the106 pairs scored/PASS. The first
worker result remains unverified here. No code/oracle/protocol edits or retry.

Frozen dev tests exercised failure/timeout/gate/badJSON worker paths, not successful
subject payload parsing. Undefined integer was copied from R3 after its definition
was removed during adaptation. This is a comparator harness defect, not evidence
that pruning method or unchanged routing kernel disagrees with exact optimum.
No automatic rescue, no replacement frozen result; any future repaired unit needs
its own prereg/freeze/evaluation preserving this locked failure.

Exact traceback saved TRACEBACK.txt; production/method/corpus/oracles remain
freeze-identical. No invention/performance/science claim. Prior failures retained.
