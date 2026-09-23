# ADDENDUM 1 - erratum (locked 2026-09-23 ~23:15 IST, before corrected G2 computation)
The G2 code drew PLAIN random pairs, but GATES.md froze EXPRESSION-DECILE-MATCHED random
pairs. This is an implementation erratum, not a gate change: the corrected run implements
exactly the frozen matching (each random pair's first gene drawn from the same mean-
expression decile as an LR ligand, second from the receptor deciles). Plain-random
result (LR median 0.022 vs random q95 0.056, FAIL) is preserved as-run; the corrected
matched-null comparison is the gate-of-record for G2.
