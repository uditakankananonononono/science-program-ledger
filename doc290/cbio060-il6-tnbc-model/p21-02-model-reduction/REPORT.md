# P21-02 Build Report: Minimal IL-6 Model (greedy species-freezing reduction to 12 ODEs)

**Parent:** CBIO060 IL-6 TNBC Model | **Spec:** doc290/cbio060-il6-tnbc-model/02-model-reduction.md
**Built:** 2026-09-24 (lane D) | **Status:** BOUNDARY RESULT - G1, G2 and G3 all FAIL for the locked reduction
family (species freezing to <= 12 ODEs). Protocol locked in `PROTOCOL_LOCK.md` (commit b2513e31) before any
reduced model was built. Not re-fished.

## What was built
`tool/reduce.py` - greedy backward species-freezing on the P21-01 surrogate (Dwivedi 2014 IL-6 model,
BIOMD0000000535, 39 ODEs). Each step freezes the species (constant at its untreated steady state) whose
removal least disturbs tissue IL-6 and tissue pSTAT3 across 3 selection conditions (antibody 100/300/600 mg),
until 12 ODEs remain. The 12-ODE model is then scored on 20 disjoint gate conditions (50% inhibition of the
top-20 screened parameters), on the target screen, and by refitting to the P21-01 synthetic data (AIC).
Run: `python3 tool/reduce.py results/results.json` (~3 min).

## Results vs locked gates
| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1 | <= 12 ODEs, every nRMSE <= 0.1 (20 conditions x 2 outputs) | 12 ODEs; tissue IL-6 nRMSE 0.008-0.030 (all pass), tissue pSTAT3 0.18-0.24 (all fail); max 0.244, mean 0.116 | **FAIL** |
| G2 | same top-5 targets | reduced top-5 {kcatSTATPhos, ksynthIL6Gut, kRLOn, KmSTATDephos, kgp130On}; lost kRShedding and kCRPSecretion | **FAIL** (3/5 kept) |
| G3 | AIC(reduced) <= AIC(full) on refit | 203.2 vs 68.5 (weighted RSS 7286 vs 26.6) | **FAIL** |

## What the boundary tells us (the spec's pivot deliverable: which modules cannot be removed)
1. **Freezing works down to ~18 ODEs, then breaks.** Selection error stays <= 0.036 until 18 ODEs. The jump
   comes from freezing the serum IL-6/antibody species (17 -> 13 ODEs: error 0.10 -> 0.23) and finally gut
   total STAT3 (12 ODEs: 0.345). The drug experiment needs the antibody PK/binding module and the tissue
   STAT3 pool; those modules cannot be frozen.
2. **Freezing the STAT3 pool destroys the saturation.** In the full model a 50% cut to the best target lowers
   steady pSTAT3 by 6.5% (P21-01). In the 12-ODE model the same cut gives 73%. The reduced model is qualitatively
   wrong about how strong the drug targets are, even though it keeps the top-3 order.
3. **kRShedding and kCRPSecretion act through species that were frozen** (serum/liver receptor and CRP
   compartments), so they drop out of the reduced ranking. Their full-model effect on tissue pSTAT3 runs
   through the inter-compartment loop.
4. **G3 fails by construction of the reduction.** Serum IL-6 and serum CRP are frozen in the 12-ODE model,
   so two of the three observables are constant. As pre-declared, this counts against the reduced model.

## Honesty notes
- Same scope caveats as P21-01: surrogate public model (not the unpublished CBIO060 48-ODE model), synthetic
  data for G3.
- Only the freezing family was tried (locked A2). QSSA/lumping could do better; this is a boundary for
  freezing, not for model reduction in general.
- The 18-ODE model on the error path was NOT scored on the gate conditions. That would be a post-hoc change
  of the <= 12 target. Needs next: pre-lock a QSSA or <= 18-ODE variant as its own direction.
- The full-model refit started from the data-generating values (7 evaluations); the reduced refit stopped
  after 20 evaluations (budget 60). k = 33 for both.

## Data / sources
- Model: BIOMD0000000535 (PMID 24402116) via github.com/sys-bio/temp-biomodels; vendored in `tool/`.
- Results: `results/results.json` (full error path, kept/frozen species, per-condition nRMSE, screens, fits).
