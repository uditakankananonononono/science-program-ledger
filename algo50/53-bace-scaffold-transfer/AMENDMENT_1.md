# algo50/53 - AMENDMENT 1 (locked after G3 FAIL, before P1 is run)

G3 FAILED: the BBBP-trained M1 model scores BACE compounds at AUROC 0.368 -
below chance, i.e. anti-predictive. (BBB-permeable-like molecules are
anti-enriched for BACE activity; cross-task transfer is negative here, not
just weak.) The pre-declared pivot P1 from PROTOCOL.md now applies, unchanged:

- P1: descriptor-only logistic trained on ALL of BBBP (8 physicochemical
  descriptors, standardized on BBBP), scored on BACE, no refit. Gate P1:
  AUROC >= 0.60.

No other gates change. G1, G2, G4 passed and stand.
