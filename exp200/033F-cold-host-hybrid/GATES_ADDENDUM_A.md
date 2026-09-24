# 033F GATES ADDENDUM A — locked 2026-09-24 11:18 IST, after G1/G2/G3 outcomes, BEFORE HYBRID-2 is scored

## Locked-design outcomes (facts, scored under the original gates)
- Harness: rebuilt KNN-d2 reproduces 033 ARM A at 0.5919 vs 0.5935 reported (1 pair,
  tie-break noise) — harness validated.
- G1 PASS: ARM A' cold-subset species top-1 = 0.0000 <= 5% (structural blindness verified).
- G2 PASS: HYBRID cold = 36.11% (26/72) >= bar 5.00%. CRISPR exact signals recover hosts
  KNN-d2 cannot name BY CONSTRUCTION.
- G3 FAIL: HYBRID warm = 48.80% vs ARM A' warm = 67.03% (bar >= -2pp = 65.03%). Naive
  CRISPR-override everywhere destroys the warm regime: spacer votes are less accurate than
  a warm KNN vote (48.8% vs 67.0%), but uniquely capable when KNN is structurally blind.

## Failure reading (documented before new design)
The locked failure tree routes G2 fail -> boundary and is silent on G3 fail. G2 PASSED, so
the core claim (exact signals rescue the cold regime) is PROVEN. The G3 failure isolates a
design flaw, not a mechanism flaw: applying the exact signal where the compositional signal
is strong. Documented failed direction: universal CRISPR-override.

## HYBRID-2 (regime-gated; locked now, scored next)
For each test virus v:
1. If max cosine k-mer similarity of v to any train virus >= tau -> ARM A' KNN-d2 vote.
2. Else if v has >= 1 qualifying CRISPR edge -> CRISPR panel-species vote (as locked).
3. Else -> ARM A' KNN-d2 vote (best available).
- tau selection: chosen on TRAIN pairs only (leave-one-out over the 1,260 train viruses with
  their own kmer profiles and CRISPR edges; candidate grid tau in {0.50, 0.55, ..., 0.99}),
  maximizing train species top-1 of the gated rule; tau then FROZEN before any test-pair
  scoring. No frozen-outcome information enters tau.
- Operational honesty: the gate uses only computable-from-sequence quantities (similarity to
  train, spacer hits), never the unknown true host. Deployable on a genuinely new phage.

## Gates for HYBRID-2 (locked, same numbers as the original where applicable)
- G2': HYBRID-2 cold-subset species top-1 >= ARM A' + 5pp (over all 72 cold pairs).
- G3': HYBRID-2 warm species top-1 >= ARM A' warm - 2pp.
- G4 (unchanged, runs regardless): provenance of correct cold calls; per-signal contribution;
  wrong-call taxonomy. Additionally: tau selected on train + the train-CV curve reported.
- Failure tree: G2' fail -> DOCUMENTED BOUNDARY. G3' fail -> DOCUMENTED BOUNDARY (regime
  gating is the mechanism-correct design; no further rescue pre-registered).
- G5 unchanged: CLI + nomination.
