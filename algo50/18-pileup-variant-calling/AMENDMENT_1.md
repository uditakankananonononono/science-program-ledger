# algo50/18 - AMENDMENT 1: 4x coverage, where the methods should actually separate

Locked after original scoring (G1 FAIL - 30x is a ceiling: FT het F1 0.9987 leaves no headroom for +0.02; G2+G3+G4 PASS; at 8x BB het recall +0.22 over FT), before 4x results are inspected. Original gates stand.

## Method
Identical simulation and callers, coverage 4x (same seeds pattern).

## Gates (locked)
- P1: 4x BB het F1 >= FT het F1 + 0.05.
- P2: 4x BB het precision >= 0.95.
- P3: 4x BB FP calls on non-variant sites <= 10.
Pivot PASSES if P1 and P2 pass.
