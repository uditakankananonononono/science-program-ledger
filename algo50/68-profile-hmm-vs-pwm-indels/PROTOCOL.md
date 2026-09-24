# algo50/68 - Profile HMM vs PWM: the indel regime where HMMs should win

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study. Topic lane-chosen (no list past 55). Extends algo50/24 (pwm-vs-consensus) into the indel regime.

## Question
PWMs model position-specific substitutions but not indels; profile HMMs add insert/delete states. Quantify the detection gap as a function of indel rate inside motif instances: at what indel rate does the profile HMM's AUROC advantage exceed 0.05?

## Data (simulated, seed 37)
Motif: 12 positions, each with a preferred base at 70% (others 10% each). Training: 60 instances with mutation noise only. Test: 400bp sequences; positives contain one motif instance with per-position indel probability r in {0, 0.02, 0.05, 0.10} (50/50 insertion/deletion, insertion = random base); negatives are pure background (iid uniform). 150 pos + 150 neg per cell.

## Methods
- PWM: log-odds with 0.01 pseudocount from training instances; score = max over 12-windows.
- Profile HMM (plan7-lite): match states 1..12, insert states, silent delete states; transitions from training + pseudocount (match->match 0.95, ->delete 0.025, ->insert 0.025; insert->match 0.9, insert->insert 0.1; delete->match 0.95, delete->delete 0.05). Viterbi score vs null (single-state iid background model); score = max over end positions.
- Metric: AUROC (pos vs neg scores) per cell, both methods.

## Gates
- G1: at r=0, PWM AUROC >= 0.95 and |PWM - HMM| <= 0.03 (no-indel regime: parity).
- G2: at r=0.05, HMM AUROC - PWM AUROC >= 0.05 (HMM advantage appears).
- G3: at r=0.10, HMM AUROC >= 0.95 (HMM robust to high indel rate).
- G4: PWM AUROC at r=0.10 <= 0.90 (PWM degrades).
PASS if all.

## Failure policy
Negatives preserved; pivots via locked amendments.

---

# AMENDMENT 1 (locked before pivot run on FRESH seed 41)
All detection gates failed as locked, and the cause is design, not method: a 12-position motif at 70% preference carries ~7.7 bits, but locating it in 400 bp needs ~log2(400)=8.6 bits - NO scorer can exceed ~0.7-0.85 AUROC there (both PWM and HMM landed at 0.69-0.73). One pre-scoring bug fixed and documented: HMM begin state unreachable past j=0 (M[0,j] never initialized; fixed to free-start local mode).
Pivot P (fresh seed 41): motif length 18 (70% preference, ~11.6 bits), background 200 bp, same indel rates and methods, HMM match-state count 18.
- P1: at r=0, PWM AUROC >= 0.95 and |PWM-HMM| <= 0.03.
- P2: HMM-PWM AUROC gap monotone non-decreasing across r = 0, 0.02, 0.05, 0.10.
- P3: at r=0.10, HMM >= 0.95 AND PWM <= 0.95 (divergence at high indel rate).
PASS if P1+P2.
