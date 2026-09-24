# algo50/12 - AMENDMENT 1: length-aware post-processing of HMM segments

Locked after the original gates were scored (G1 FAIL at +0.074 vs needed +0.10; G2 PASS recall 1.0; G3 FAIL - LLR ties the rule; G4 FAIL - median segment 201 bp vs annotated 710 bp, over-segmentation), before post-processed results are inspected. Original gates stand.

## Method
HMM-PP: take the same Viterbi decode (no retraining); merge island segments separated by gaps < 200 bp; drop resulting segments shorter than 200 bp. Same window-level evaluation as the original protocol.

## Gates (locked)
- P1: HMM-PP window-level F1 >= RULE F1 + 0.10.
- P2: HMM-PP median segment length within [0.5x, 2x] the median length of annotated test-half islands.
- P3: island-level recall stays >= 0.70.
Pivot PASSES if P1 and P2 pass.
