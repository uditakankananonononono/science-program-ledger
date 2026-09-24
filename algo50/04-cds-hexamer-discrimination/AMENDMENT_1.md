# algo50/04 - AMENDMENT 1: small combined logistic model

Locked after the original gates failed (G2, G3, G4 FAIL; G1 PASS), before any combination results were inspected. Original gates stand as scored; nothing is re-tuned.

## Direction
The original protocol showed the 5th-order hexamer LLR (HEX, Glimmer-style) loses badly to a trivial amino-acid-usage LLR (DI) in the shadow-ORF setting. Pivot: does a small logistic model over all five features (GC, GC3, LEN, DI, HEX) do better than DI alone, and does it transfer?

## Method
- COMBO: sklearn LogisticRegression (default L2, features z-scored on train) over [GC, GC3, LEN, DI-score, HEX-score]; DI/HEX LLR models refit per training fold as before; 5-fold locus-held-out CV per genome; transfer = fit on all E. coli, test on B. subtilis and M. tuberculosis.

## Gates (locked)
- P1: within E. coli, COMBO AUROC >= DI AUROC - 0.001 (combination must not lose to the single best feature beyond noise).
- P2: within E. coli, COMBO AUROC >= 0.98.
- P3: COMBO trained on E. coli, tested on M. tuberculosis: AUROC >= 0.95.
Pivot PASSES if P1 and P2 pass; P3 is the transfer boundary.
