# DOC-1-032 - A "Metabolic Rosetta Stone" for Microbiome-Host Interactions: REPORT

**Outcome: DOCUMENTED BOUNDARY - G3 (frozen cross-cohort transfer) FAILS. Not submitted for
counting. Dev benchmark (G2) passed decisively; frozen validation on an independent cohort
(HMP2, n=388 paired samples) shows the dev gain does not survive cohort shift.**

## Locked protocol (GATES 09:00, Addendum B 09:01, Addendum C 09:17 - all pre-outcome)
- DEV: PRISM (n=157), 5-fold CV seed 0. ARM A = MelonnPan-Train protocol reimplemented
  in-envelope (Addendum B: shipped weights are PRISM-trained, so the honest dev baseline is the
  protocol, not the shipped matrix). ARM B = per-metabolite RidgeCV (alphas logspace(-3,3,13),
  inner LOO-CV pick) on log1p(x*1e6) UniRef90 relative-abundance features.
- FROZEN: switched NLIBD -> HMP2/Lloyd-Price by Addendum C (parent-approved 09:16:32) after the
  NLIBD sample-ID join proved publicly unrecoverable (hunt documented in Addendum C).
- Frozen data: official IBDMDB Globus endpoint - HMP2_metabolomics_w_metadata.biom.gz
  (546 samples) + per-sample HUMAnN2 bundles (MGX 2018-05-04) + hmp2_metadata_2018-08-20.csv.
- Frozen cohort: 388 stool samples with BOTH metabolomics and metagenomics (105 subjects;
  CD 181, UC 102, nonIBD 105). 70/80 MelonnPan compounds mapped to measured HMP2 metabolites
  (name-normalized + locked synonym table; duplicates collapsed to lowest pooled-QC-CV feature;
  10 unmapped documented). Features: unstratified UniRef90, relative abundance over all
  unstratified families (matches PRISM units). ARM B dev protocol was re-derived post-environment-
  rebuild and verified against committed dev_scores.json (max abs diff 0.0 over 80 compounds).

## Results
### Dev (PRISM 5-fold CV) - committed earlier (fe4ba51e)
| arm | well-predicted (rho>=0.3) | mean rho |
|---|---|---|
| ARM A (MelonnPan-Train protocol) | 45.0% | 0.289 |
| ARM B (ridge) | **85.0%** | **0.454** |
G2: PASS (both margins: >=+5pp, >=+0.05).

### Frozen (HMP2, 388 samples, 70 metabolites)
| arm | well-predicted | mean rho | median rho |
|---|---|---|---|
| ARM A (shipped MelonnPan weights, PRISM-trained) | **37.1%** (26/70) | 0.251 | 0.257 |
| ARM B (ridge, full PRISM fit) | 30.0% (21/70) | 0.236 | - |

- **G1 frozen coherence [0.10, 0.50]: PASS** - and ARM A's 37.1% matches the independently
  published cross-cohort anchor exactly (ENVIM paper, Lloyd-Price DNA: MelonnPan 37%).
- **G3: FAIL** - ARM B < ARM A + 3pp (30.0% vs required 40.1%) AND < dev - 15pp (70%).
- Per-compound rhos: results/armA_frozen_rho.json, results/armB_frozen_rho.json.

### G4 (mechanism, runs regardless)
Top |coefficient| ARM B drivers for host-relevant metabolites (results/g4_drivers.json,
annotation results/g4_uniref_ann.json). Most HUMAnN2-era UniRef90 IDs are retired from current
UniProt (35/40 unresolvable). The resolvable top butyrate drivers are organism-annotated to
known butyrate producers: Pseudoflavonifractor capillosus (A6P026, A6P028, A6P140),
Agathobacter rectalis (C4ZD95), Anaerotruncus colihominis (B0P655) - literature-coherent.
SCFA transfer is the weak point: propionate rho -0.03 (B) / -0.06 (A), butyrate below threshold
in both arms on HMP2.

### G5
- tools/metabolite_predict.py: working CLI (HUMAnN2 genefamilies.tsv -> 80 metabolite
  predictions); smoke-tested, reproduces the frozen pipeline (abs diff <= 0.006 from 6-digit
  vector storage rounding). Model weights: results/armB_prism_model.npz.
- Prospective lab nomination (locked): an IBD metabolomics unit running paired
  metagenome+metabolome profiling, using the cross-cohort predictor to impute metabolites where
  only metagenomes exist, validated against targeted assays.

## Interpretation
Within-cohort CV makes the compact ridge look dominant (85% vs 45%), but cross-cohort the
advantage inverts: the shipped MelonnPan model - regularized by its protocol's retention of only
well-predicted metabolites - transfers at its published rate (37.1%, matching the independent
ENVIM anchor of 37%), while the ridge falls to 30.0%. Dev-CV gains at this scale do not survive
cohort shift (consistent with the 026/027/030 out-of-domain rule). The "Rosetta Stone" as locked
does not beat the published model where it counts (independent cohort); the honest payload is
the frozen audit itself: a reproducible 388-sample paired HMP2 evaluation harness, a verified
positional compound-mapping for the shipped weights, and a documented quantification of
cross-cohort degradation for metabolite prediction (85% -> 30%).

## Failure tree
G2 passed; G3 failed -> DOCUMENTED BOUNDARY per locked tree (P1 rescue was pre-registered only
for G2 failure). No thresholds relaxed; all addenda locked before the outcomes they govern.
