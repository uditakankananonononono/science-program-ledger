# P21-07 Build Report: Dose to Signal (label PK coupled to the IL-6 pathway model)

**Parent:** CBIO060 IL-6 TNBC Model | **Spec:** doc290/cbio060-il6-tnbc-model/07-pkpd-dosing.md
**Built:** 2026-09-24 (lane D) | **Status:** BOUNDARY RESULT - G1 FAIL (simple PK modules miss label values
for both antibodies); G2 reported (no ranking reversal: spec failure rule applies); G3 PASS (95%).
Protocol locked in `PROTOCOL_LOCK.md` (a608c232); amendment A5b (peak/trough window) locked before the
gated run (eabca04a), with the deviation that prompted it disclosed there.

## What was built
`tool/pkpd.py` - 1-compartment PK for ruxolitinib (oral, 20 mg BID), tocilizumab (8 mg/kg IV q4w; two
elimination arms) and siltuximab (11 mg/kg IV q3w), with parameters from the current FDA labels. PK is coupled
to the P21-01 surrogate IL-6 model (BIOMD0000000535) through quasi-equilibrium PD: ruxolitinib inhibits JAK
catalysis (IC50 3.3 nM, free fraction 3%), tocilizumab blocks IL-6R binding (Kd 2.54 nM), siltuximab
neutralises IL-6 (host-model antibody affinity 2.5 pM, since no verified public Kd was found). Everything runs
for 4 weeks from untreated steady state and is compared with static constant-Cmax screens, at nominal
parameters and across 100 P21-01 ensemble members.
Run from repo root: `python3 doc290/cbio060-il6-tnbc-model/p21-07-pkpd-dosing/tool/pkpd.py <out.json>` (~4 min).

## Results vs locked gates
| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1 | PK Cmax and t1/2 within 20% of label | rux Cmax 627 vs 710 nM (-12%), t1/2 2.5 vs 3 h (-16%) PASS; toc ss Cmax 294 vs 176 ug/mL (+67%) FAIL; toc t1/2 21.5 d (input, circular); sil ss Cmax 260 vs 332 ug/mL (-22%) FAIL; sil t1/2 13.6 vs 20.6 d (-34%) FAIL | **FAIL** |
| G2 | static vs dynamic ranking reported, all pairs | static and dynamic order are the same: siltuximab > tocilizumab > ruxolitinib; 0/3 pairs reversed (arm B tocilizumab: same) | **PASS (reported)** |
| G3 | conclusions hold in >= 80% of ensemble | same dynamic order in 100/100 members; order + all verdicts in 95/100 | **PASS** |

Tissue pSTAT3 suppression at nominal parameters:
| drug | static (Cmax) | dynamic 4-week mean | peak / trough, last complete interval | verdict |
|------|---------------|--------------------|-----------------------------|---------|
| siltuximab | 1.000 | 0.591 | 0.952 / 0.952 (0-504 h) | sustained |
| tocilizumab (arm A) | 0.998 | 0.577 | 0.981 / 0.981 (0-672 h) | sustained |
| tocilizumab (arm B) | 0.998 | 0.559 | 0.944 / 0.944 | sustained |
| ruxolitinib | 0.364 | 0.105 | 0.143 / 0.052 (660-672 h) | rebound |

Spec hypothesis: part 1 (antibodies sustained, JAK inhibitor rebounds between doses) **supported**. Part 2
(at least one pair's ranking reverses) **not supported**. Per the spec's failure rule: for this pathway model,
static screens give the right drug ranking. PK changes how much suppression you get, not the order.

## What this means
1. **Ruxolitinib at label dosing barely touches tissue pSTAT3 in this model.** Free Cmax is ~19 nM (97% bound),
   which is ~85% JAK inhibition at peak. Because the pathway is saturated (P21-01), that gives only 14% peak
   suppression, and it falls to 5% before each dose. The static screen (36%) overstates it about 3.5x.
2. **The antibodies are slow to start, then durable.** Suppression takes ~18 days (432-444 h) to reach 90% of
   peak, because the model's receptor/pSTAT3 turnover is slow. So the 4-week mean (0.58-0.59) is far below the
   static value (~1.0). Once established, it holds through the dosing interval.
3. The ordering is robust: every ensemble member gives siltuximab > tocilizumab > ruxolitinib.

## Honesty notes
- **G1 failures are real limits of 1-compartment linear PK.** Tocilizumab has nonlinear (MM) elimination, so a
  linear 21.5-day half-life over-accumulates (arm B, with a 7.6-day effective half-life, gets the label trough
  right: 14.8 vs 13.4 ug/mL). Siltuximab is 2-compartment in the label, so a 1-compartment model with label
  Vc/CL gives too short a half-life. The tocilizumab V was set from the label Cmax, so its single-dose Cmax is
  circular. Needs next: 2-compartment/MM popPK models (published parameters).
- The ranking conclusion survives both tocilizumab arms. Antibody occupancy is ~100% throughout, so the PK
  error does not change the PD verdicts.
- **A5b deviation:** the first code measured siltuximab's peak/trough over 168-672 h, mixing the onset with the
  second dose (trough 0.20, flagged "rebound"). I found this while smoke-testing, before the gated run, and fixed
  it to match the locked text ("last complete dosing interval"). The first values stay in results.json
  (`deviating_first_impl_peak_trough`).
- **Solver plumbing:** in gated run 1, a CVODE failure left the solver instance failing for every later member
  (34/100 "fail"; G3 0.61 as executed; kept as `results/results_run1_sticky_solver.json`). The fix creates a fresh
  solver and retries a failed member once. Nothing about the method changed. In the rerun one member needed the
  retry and there were 0 failures. The G3 verdict above comes from the fixed run. The parent may prefer to
  record run 1.
- The regenerated ensemble matches the P21-01 sampler (300 members) but is not bit-identical: nominal chi2 is
  26.527 vs 26.525 (solver-state rounding). Members saved in `results/results_ensemble.npy`.
- Siltuximab potency is the host model's own anti-IL-6 affinity, not a verified siltuximab Kd.
- Same scope caveats as P21-01: surrogate public model, not the unpublished CBIO060 48-ODE model.

## Sources
- Jakafi label: https://www.accessdata.fda.gov/drugsatfda_docs/label/2017/202192s015lbl.pdf (sec. 2, 12.3)
- Actemra label: https://www.accessdata.fda.gov/drugsatfda_docs/label/2025/125276s147lbl.pdf (sec. 12.3)
- Sylvant label: https://www.accessdata.fda.gov/drugsatfda_docs/label/2019/125496s018lbl.pdf (sec. 12.3)
- Ruxolitinib JAK1 IC50 3.3 nM: https://pmc.ncbi.nlm.nih.gov/articles/PMC5147419/ (citing Quintas-Cardama 2010, https://doi.org/10.1182/blood-2009-04-214957)
- Tocilizumab Kd 2.54 nM: https://pubmed.ncbi.nlm.nih.gov/16102523/
- Host model: BIOMD0000000535 (PMID 24402116) via github.com/sys-bio/temp-biomodels
