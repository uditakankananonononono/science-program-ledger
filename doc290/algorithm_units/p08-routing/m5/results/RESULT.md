# M5 locked interrupted timing evaluation

Freeze0714ffdb97f8be9b135bb77e10c0cfe4e7cd8487 was published and verified before
launch. The foreground 1200-subject evaluation was killed by the outer bash
execution limit before compare.py wrote report.json. The runtime reported an
execution-limit kill. Two subsequent state checks found results empty and no
compare/worker processes; local HEAD remained the freeze. No report or per-row
receipts were persisted because the frozen harness writes only after all600pairs.

Attempted/completed prefix and method payloads are UNVERIFIED, notzero and not
1200. No objective/witness agreement, methodPASS/FAIL count, timing ratio, class
exclusion accounting or deterministic-repeat result is available. This is a
harness durability/execution-lifetime failure, not established T9/T8 algorithm
failure. No evaluation rerun, rescoring, drop or rescue. FAILED-RUN.json preserves
the unknowns rather than converting missing receipts into invented counts.

A fresh timing run would need a disclosed new freeze with incremental durable
receipts and execution independent of the outer call cap; it would not repair
or erase this failed run. M4 negative (P4slower446/600, medianratio1.5828593506719892)
and all prior failed/rejected histories remain. No speed/novelty/invention/science
or production completion claim. One-shot discipline is reported process, not
proof from Git ancestry.
