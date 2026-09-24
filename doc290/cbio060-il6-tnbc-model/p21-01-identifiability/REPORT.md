# P21-01 Build Report: Which Conclusions Hold (identifiability + target-rank stability, IL-6/JAK/STAT3 ODE)

**Parent:** CBIO060 IL-6 TNBC Model | **Spec:** doc290/cbio060-il6-tnbc-model/01-identifiability-uncertainty.md
**Built:** 2026-09-24 (lane D) | **Status:** ALL GATES PASS on the locked protocol, with a major scope caveat
(surrogate public model + synthetic data; see A1/A2). Protocol + gates locked in `PROTOCOL_LOCK.md`
(commit f3f66a07); sampler amendment A6b locked before any G2/G3 evaluation (commit c7635112).

## What was built
`tool/ident.py` - runnable pipeline (libroadrunner + numpy/scipy) on the public Dwivedi et al. 2014 IL-6
multiscale model (BioModels BIOMD0000000535, SBML vendored as `tool/BIOMD0000000535.xml`; 39 ODEs,
71 reactions; 33 kinetic parameters estimated). Steps: numerical local structural identifiability (SVD of
dense noise-free sensitivities), Fisher-information practical identifiability under a realistic synthetic
anti-IL-6 antibody experiment (serum IL-6, serum CRP, tissue pSTAT3; 8 training + 3 held-out days), a
300-member plausible-parameter ensemble (RW-Metropolis inside the chi2 95% region, 1-decade prior),
a virtual 50%-inhibition target screen on steady-state tissue pSTAT3 per ensemble member, and held-out fit.
Run: `python3 tool/ident.py results/results.json` (~3 min).

## Results vs locked gates
| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1 | identifiability reported for all parameters | 33/33 structural + practical, table in results.json | **PASS** |
| G2 | top-5 targets stay in top-10 for >=80% of ensemble | 99.7% of 300 members (kcatSTATPhos rank 1 in 100%; ksynthIL6Gut rank 2 in 100%; kRLOn median 4 [IQR 3-5]; kRShedding 5 [4-5]; kCRPSecretion 6 [6-7]) | **PASS** |
| G3 | held-out nRMSE <= 0.2 | IL-6 0.028, CRP 0.051, pSTAT3 0.017 | **PASS** (self-consistency only, A2) |

Spec hypothesis: part 1 ("fewer than half identifiable") **supported, strongly**: 0/33 parameters are
practically identifiable (smallest FIM 95% half-width 1.96 x 4.4 decades, kintActiveR), although all 33
are locally structurally identifiable (full rank 33; smallest relative singular value 1.0e-4 - sloppy,
not singular). Part 2 (top-5 ranking robust in >=80%) **supported**.

## What this means
1. **Classic sloppy model.** With realistic clinical-style sampling of three readouts, none of the 33 rate
   constants is pinned down to within ~3-fold, yet predictions of the same readouts at held-out times are
   tight (nRMSE <= 0.05). Parameter values from this model class should not be quoted as measurements.
2. **Target rankings survive anyway.** The ensemble is genuinely wide (median per-parameter SD 0.63 decades;
   median member's largest deviation from nominal 1.9 decades), and the top-2 targets (STAT3 phosphorylation
   catalysis, local IL-6 synthesis) never move. Ranking conclusions are more robust than parameter values.
3. **Effect sizes are small.** 50% inhibition of the best single target lowers steady-state tissue pSTAT3 by
   only 6.5% (next 5.9%, then <= 3%). The pathway is saturated at the disease steady state; single-node
   inhibition barely moves pSTAT3 in this model. Robust ranking of weak levers is the honest headline.

## Honesty notes / caveats
- **Surrogate model (A1):** the CBIO060 48-ODE TNBC model is not public. Results speak for the published
  IL-6/JAK/STAT3 model class (Dwivedi 2014, a Crohn's/hepatic multiscale model; gut compartment used as the
  tumour analog), not for the CBIO060 model itself.
- **Synthetic data (A2):** data generated from the model at nominal values + 10-15% noise; G3 therefore tests
  self-consistency, not biological validity. Needs next: real TNBC pSTAT3 time courses (digitized figures).
- **FIM approximation (A5):** practical identifiability uses Fisher information instead of full profile
  likelihood (sandbox has no AMICI/pyPESTO). With half-widths of 4-50+ decades the qualitative verdict
  (non-identifiable) is not borderline for any parameter.
- **Sampler change (A6b):** the originally locked independence sampler accepted 3/20,000 draws (linear FIM
  picture breaks down along sloppy directions); replaced by MCMC before any gate evaluation. 254 unique
  members of 300 (post-burn acceptance 0.20); chain length is modest.
- **Tie at rank 5/6:** kCRPSecretion and VmProtSynth give identical pSTAT3 drops at nominal (0.02577) - the
  screen cannot separate them; locked top-5 kept kCRPSecretion by sort order. G2 would be unaffected in
  substance (both sit at rank 5-7).
- Nominal parameters are the data-generating values (near-MLE by construction); no multistart fit was run.
- Failure-rule OED not triggered (G2 passed); not run.

## Data / sources
- Model: BIOMD0000000535 (PMID 24402116), fetched from github.com/sys-bio/temp-biomodels (final/BIOMD0000000535)
  because www.ebi.ac.uk/biomodels returns 403 to the sandbox.
- Results: `results/results.json` (identifiability table, ensemble diagnostics, per-member-derived ranks, G1-G3).
