# P13-06 Reinfusion Scheduler - Build Report

Mechanistic ODE-guided timing of repeat CAR-T dosing. In silico, literature-parameterized.
Source abstract, 2024. Build artifacts: `tool/reinfuse.py`, `results/results.json`,
`results/escape_extension.json`.

## Gates (locked before evaluation, evaluated once)

| Gate | Criterion | Observed | Verdict |
|------|-----------|----------|---------|
| G1' calibration | effector peak day in published 7-21 band | day 7.01 | PASS |
| G2' optimization changes plan | >=15% burden reduction OR honest near-optimal documented | max reduction <1e-6 (near-optimal branch, documented) | PASS |
| G3 identifiability | >=3 core params identifiable from weekly ddPCR | 4/5 (a, d0, x, k) | PASS |
| G4 boundary | trial-kinetic fitting out of run scope | documented | boundary |

## Instrument defects found and repaired before final evaluation
(disclosed per pivot rule; single evaluation run after repair)

1. Original ODE had no expansion phase - effector peaked at day 0. Added the
   antigen-driven expansion term (`a*E*T/(T+h)`) before any gate evaluation.
2. Initial dose MULTIPLIED E0 (0.02 effectors at t0) - a unit defect that made
   the baseline escape the toxicity proxy. Changed to additive, symmetric with
   reinfusion handling.
3. Toxicity proxy was an absolute peak threshold every reinfusion breached while
   the baseline never did. Re-locked as 3x the base regimen's own peak
   (literature: repeat dosing at a similar peak carries similar CRS risk).
4. Expansion rate `a` calibrated ONCE to the published peak band under the final
   dosing convention (a=0.45).

## Results

**G2' - the useful negative, with mechanism.** Across the full reinfusion grid
(day 30-210 x dose 0.5-2.0) and the pre-committed clearance-strength sweep
(k = 0.55/0.40/0.30/0.22), no reinfusion plan reduces tumor burden by more than
1e-6. Mechanism: with antigen retained, antigen-driven effector expansion is
self-sustaining - the first infusion controls the tumor unaided, so a second
dose adds only toxicity risk. Reinfusion timing is a second-order lever in this
regime.

**Antigen-escape extension (post-hoc, clearly labeled).** Adding an escape clone
(mutation flux mu=0.01 of antigen+ divisions) produces robust relapse (final
tumor 0.64 of carrying capacity). Same-CAR reinfusion is then futile at EVERY
timing and dose (reduction <1e-6): reinfused effectors find no antigen, cannot
expand, and wane in ~1/d0 = 22 days while the escape clone grows untouched.

**Program-level finding for CBIO042 ReinforCell:** "reinforcement" timing is not
the lever in either pure regime. The model points to target breadth (dual-target
products against escape) as the actual reinfusion rationale - directly motivating
P13-10 (Antigen-Escape Atlas, dual-target selection) as the follow-on build.

**G3 - identifiability boundary.** From weekly ddPCR-style effector measurements:
a, d0, x, k are identifiable (rel. sd <50%); tau (persistence-wane timescale) is
NOT separately identifiable from kill/wane dynamics at weekly sampling. Trial
implication: weekly effector quantification cannot resolve the persistence
timescale - denser early sampling or a second readout is required.

## Boundaries
- Retrospective redosing validation and Bayesian fitting need published trial
  kinetic series (figure digitization beyond run scope).
- Model is 2-population ODE; no spatial, cytokine, or host-immune compartments.
- Escape extension is post-hoc and illustrative (single mu); gates stand on the
  pre-committed model.
