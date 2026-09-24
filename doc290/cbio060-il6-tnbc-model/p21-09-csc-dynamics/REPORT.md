# P21-09 Build Report: Does Blocking IL-6 Shrink the Stem-like Pool? (Nazari 2018 CSC model + chemo)

**Parent:** CBIO060 IL-6 TNBC Model | **Spec:** doc290/cbio060-il6-tnbc-model/09-csc-population-dynamics.md
**Built:** 2026-09-24 (lane D) | **Status:** BOUNDARY RESULT. Spec hypothesis falsified in this model: IL-6
blockade adds no stem-fraction benefit to chemotherapy. G1 NOT MET (no data), G2 FAIL (null reported),
G3 NOT EVALUABLE. Protocol locked in `PROTOCOL_LOCK.md` (551296a2) before any treatment simulation.

## What was built
`tool/csc.py` loads the public Nazari et al. 2018 IL-6 / cancer-stem-cell model (BIOMD0000000819; stem S,
progenitor E, differentiated D; IL-6 raises S self-renewal and survival through receptor occupancy phi). It adds
first-order chemotherapy kill terms (0.3/day on E and D, 10x lower on S) and IL-6 blockade (IL-6/IL-6R binding
K_f x 0.02, i.e. P21-07's tocilizumab-level suppression). Tumours grow for 100 days, get 21 days of treatment,
and are followed to day 142. There are four arms, a blockade-strength sensitivity check, and 200 perturbed
parameter sets.
Run: `python3 tool/csc.py results/results.json` (~5 s).

## Results vs locked gates
| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1 | reproduce published conversion data | no digitisable data (A5) | **NOT MET** - sign-level predictions only |
| G2 | combination benefit on stem fraction >= 30%, robust in >= 80% | nominal -0.4% (day 121), -0.1% (day 142); in 0% of sets >= 30%; median -0.3% [5-95%: -2.3%, -0.006%]; positive in 2.4% of evaluable sets; 73/200 sets failed to integrate | **FAIL - null reported** |
| G3 | baseline stem fraction in atlas range | atlas not processable (A7); model baseline SF = 2.3% (untreated, day 121) | **NOT EVALUABLE** |

Stem fraction at the end of treatment (day 121): untreated 2.3%; blockade alone 2.4%; chemo 14.3%;
chemo + blockade 14.4%. Blockade strength sensitivity (b = 0.5 / 0.9 / 0.98): benefit -0.01% / -0.08% / -0.4%.

## What the boundary tells us
1. **Chemo enriches stem cells 6-fold, as the premise says** (2.3% -> 14.3%). The enrichment relaxes back to
   3.3% within 3 weeks after treatment.
2. **Blocking IL-6/IL-6R binding does nothing to that enrichment in this model, and the reason is ligand
   build-up.** Receptor uptake is the main route of IL-6 clearance here. With binding cut 50-fold, free IL-6
   climbs about 40-fold (1.4 -> 58.8), and stem-cell receptor occupancy drops only 16% (0.122 -> 0.103). The
   IL-6 lever on self-renewal is weak anyway (myu = 0.04). A rise in IL-6 during receptor blockade is also seen
   clinically with tocilizumab, so this compensation may be real. It means occupancy, not dose, has to be the
   design variable.
3. **Sign-level prediction (spec failure rule):** within this model class, IL-6/IL-6R blockade alone does not
   lower the post-chemo stem fraction. Only a mechanism with explicit IL-6-driven dedifferentiation
   (Iliopoulos 2011), which this model lacks, could.

## Measurements needed (spec failure rule)
- Time courses of stem-marker fraction (e.g. CD44+/CD24- or ALDH+) in TNBC lines after IL-6 addition and
  after IL-6R blockade, with free IL-6 in the medium measured at the same time points.
- Non-stem -> stem conversion rates with and without IL-6 (sorted-population experiments), to add a
  dedifferentiation term.
- Chemo kill rates on sorted stem vs non-stem cells (the 10x resistance ratio here is an assumption).

## Honesty notes
- Host model is from head-and-neck cancer (Nazari 2018), not TNBC, and has no dedifferentiation (A1). Coupling
  to the P21-01 signaling model is only through the blockade strength (A2).
- 73/200 perturbed sets failed to integrate even with the fresh-solver retry. As locked, they count as not
  meeting the criterion. Among the 127 that ran, the benefit is still near zero, so the verdict does not depend
  on the failures.
- A smoke run of the untreated model (day-400 SF ~2%) was done before locking and is disclosed in the lock.
