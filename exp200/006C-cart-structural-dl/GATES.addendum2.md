# 006C ADDENDUM 2 (erratum, locked 2026-09-24 ~01:16 IST)
Addendum 1's parenthetical test-set names "(1WEJ, 2JEL, 5LHQ)" were a drafting error:
the locked RULE is "13 lowest-PDB-ID complexes train / 3 highest test, by sorted ID",
which yields test = 5JMO, 5LHN, 5LHQ. The code implemented the sorted rule correctly;
the rule (not the miswritten names) is the gate of record. Corrected after the fixed-split
AUROC (0.511) was computed but BEFORE the permutation nulls exist and before any
threshold/selection use of the split; no design element changed in response to that value.
