# 007 ADDENDUM 1 (locked 2026-09-24 ~01:48 IST, BEFORE any evaluation outcomes)
Implementation constraints on this 2-CPU/1.9GB box, no science change:
1. batch 64 -> 32 (memory ceiling); threads pinned to 1.
2. Training runs as sequential checkpointed chunks over the SAME single pass in
   first-come file order (459 batches of 32 over the 14,669-transcript frozen 30M-nt
   corpus); chunk boundaries do not reshuffle or resample.
3. Each transcript contributes its first 256 nt per pass (ctx=256), as implied by the
   locked architecture; the 30M-nt budget measures corpus composition, unchanged.
4. Adam optimizer state carries across chunks (standard resume).
Model, layers, lr, dropout, corpus, split, and all gates unchanged from GATES.md.
