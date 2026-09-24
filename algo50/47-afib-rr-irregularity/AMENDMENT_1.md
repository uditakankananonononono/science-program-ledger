# algo50/47 - AMENDMENT 1 (locked after G1 FAIL, before P2 is run)

G1 FAILED: pooled record-held-out AUROC(M1) 0.9872 vs AUROC(B1) 0.9742 is
+0.013, below the declared +0.02. The pre-declared pivot P2 from PROTOCOL.md
now applies, unchanged:

- P2: window-length ablation. Rebuild windows at 120 consecutive clean beats
  (stride 60) and rerun the identical pipeline. Gate P2: pooled
  record-held-out AUROC(M1) >= AUROC(B1) + 0.02 at 120 beats.

Rationale recorded for the README regardless of outcome: 60-beat windows may
already saturate the classic features (B1 0.974 leaves little headroom);
longer windows give entropy/turning-point features more signal but smooth out
short paroxysms.

No other gates change. G2, G3, G4 passed and stand.
