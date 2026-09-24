# exp200 Cross-Experiment Findings

Program-level findings that recur across experiments. Every entry cites the experiments whose
locked-gate reports support it; numbers are from the frozen/final scores in each REPORT.md.
Lanes append their entries as experiments close. Created 2026-09-24 (EXP-1 seed).

## 1. Dev-to-frozen inversion: mechanistic baselines win out-of-domain
The program's strongest cross-cutting finding. Learned models that beat mechanistic baselines
in dev cross-validation LOSE to them on frozen independent cohorts; dev-CV gains routinely
invert. Six instances:

- **026 viral-infection-atlas**: learned NMF top-50 signature wins dev (AUROC 0.6189 vs 0.5886)
  but loses frozen cross-virus transfer to the plain ISG signature (0.5605 vs 0.6193).
- **027 spatial-deconv-gnn**: NNLS baseline beats the locked GNN on BOTH dev (0.6856 vs 0.409)
  and frozen (0.7273 vs 0.363); pre-registered P1 rescue failed too (0.299 frozen).
- **030 drug-response-transfer**: simple ERBB2+EGFR biomarker (+0.415 dev / +0.478 frozen PCC)
  beats both learned transfer arms (ridge +0.163/+0.214; quantile-aligned +0.214/+0.213).
- **032 microbiome-metabolite**: dev ARM B ridge 85.0% / MCC 0.454 collapses to 30.0% on the
  frozen 388-sample HMP2 cohort, below the mechanistic ARM A protocol (45.0% / 0.289).
  Harness validated by reproducing the published ENVIM 37% cross-cohort rate EXACTLY (37.1%).
- **032F producer-constraint (boundary refinement of the 032 instance)**: restricting each
  metabolite's features to AGORA2/DEMETER-annotated producer species picks the biologically
  CORRECT drivers (Roseburia for butyrate, Megamonas for propionate; dev mean rho 0.42) but
  does NOT repair cross-cohort transfer (frozen well-predicted 2/10 vs ARM A 3/10 and ARM B
  5/10 on the same compounds; propionate -0.142). 032's collapse is a signal-strength
  problem, not a feature-selection problem: organism abundance is a weaker transported
  signal than gene-family dosage.
- **033 phage-host-gnn**: dev graph gains (20.95%, +7.3pp over no-graph, all 10 folds) collapse
  frozen to 12.20% vs ARM A KNN-d2 59.35%; CRISPR-spacer rescue real but neutral (+0.00pp).
- **035 dark-matter-function**: dev ARM B 3-channel model 32.22% vs ARM A Huynen-vote 27.76%
  (G2 FAIL, -0.54pp vs +5pp bar; P1 label-propagation rescue 28.32% also short) inverts on
  the temporally frozen newly-lit cohort: ARM A 24.34% > ARM B 20.45% (popularity 8.55%).
  G4 confirms Huynen hierarchy (neighborhood 26.69% > fusion 23.35% > co-occurrence 19.04%;
  fusion highest precision 33.58% at 7.7% coverage; 20% context-isolated = 0.00% - the real
  ceiling is coverage, not model capacity).

Rule: out-of-domain, prefer the mechanistic baseline; treat dev-CV gains of learned models as
evidence ABOUT the dev distribution only.

- **033F cold-host-hybrid** extends the 033 instance: CRISPR exact signals recover the cold
  regime (36.11% vs 0% structural floor) - and exposes a new finding class, section 8.

## 2. Task-type map
- **029 sc-multiomics-foundation**: foundation-model protocol strictly dominated at sub-atlas
  scale - ridge baseline 0.727/0.644 (dev/frozen) beats FM linear probe (0.670/0.587) and P1
  end-to-end fine-tune (0.394/0.354).
- **031 AMP discovery**: benchmark leakage dominates the AMP literature; homology-pruned model
  holds MCC 0.80 under 80%-identity control but 0.37 on an independent DRAMP cohort - reported
  literature numbers are largely leakage.
- **020-025** (see individual reports): transfer/small-panel tasks reward reference-simple
  methods; panel-scale generative approaches not competitive on CPU.

## 3. Small-PLM rule (011-015)
Small protein language models / PLM-derived features at CPU-feasible scale do not beat
domain baselines on discovery tasks: 011 (CRISPR-PLM discovery, headline G1 fail), 012
(enzyme-EC foundation, both headline gates fail), 014 (AMP generative design - 738M generator
RAM-infeasible, swapped to ESM-2 t6_8M pre-generation per Addendum A), 015 (PPI interfaces,
G2 fail). Rule: do not propose small-PLM arms where a domain mechanistic baseline exists.

## 4. Pre-lock eligibility rules (standardized)
Checked BEFORE gates are locked, alongside data availability:
- **028 label-granularity rule**: label granularity must match the statistic's granularity
  (tumor-level labels cannot validate section-level claims).
- **031 cohort-disjointness rule**: validation-cohort disjointness granularity must match the
  discovery claim's granularity (family-level claim => family-disjoint split).

## 5. Transport rule (010/019/020)
Signals that are real in their source cohort routinely fail to transport across batches,
studies, or mirror/relabelled data layouts: 019 (G2 batch-guard fail), 020 (mirror-data label
redefinition needed pre-lock, Addenda A/B). Rule: lock a batch/source guard as an early gate
whenever data crosses studies.

## 6. Small models: compress/align yes, generate no (021/022)
Small models win at compressing and aligning existing signal (021 kNN-style reference mapping
remains the bar tiny diffusion cannot beat; 022 cross-tissue embedding alignment - see report)
and lose at generating or cross-library synthesis. Matches finding 1's mechanism: alignment
stays in-domain; generation is evaluated out-of-domain.

## 8. Regime undetectability: the failure regime can be invisible to the feature space
A model can fail in a regime that its own features cannot identify, making regime-aware
gating impossible from sequence alone. First instance:

- **033F cold-host-hybrid**: KNN-d2 is structurally blind on cold hosts (0.00%) and CRISPR
  spacer votes name them (36.11% overall, 63.4% precision among the 41/72 covered). But
  cold test viruses are compositionally indistinguishable from warm (median max cosine to
  train 0.984 vs 0.997), the train panel contains no cold-regime analogs (1239/1260 LOO
  maxsim >= 0.95), and the train-LOO gate-selection curve is flat at every threshold - so
  no sequence-computable gate can route predictions between the regimes. Universal override
  bleeds the warm regime (48.8% vs 67.0%). Deployable form: two-output tool reporting both
  channels, not a gated single predictor.

Rule: before proposing a regime-gated hybrid, verify the regime is detectable in the
available features (e.g., train-CV separation); an undetectable regime means a two-output
tool, not a gate.

## 7. EXP-4 lane boundaries (DOC-2-051..100)
- **Single marker beats multi-gene cross-lab (151, 156, 154)**: 151 cfDNA 5hmC one gene 0.73 vs module model 0.61 / elastic-net 0.64 on a frozen other-lab cohort (train CV 0.76-0.79). 156 SLC6A14 alone 0.83 >= 19-gene model 0.78. 154 published Sweeney 7-gene >= trained genome-wide model (pooled -0.036). Matches finding 1.
- **Order-based rules transport; residual rules do not (157)**: k-TSP 0.76/0.78 stable across two external UC cohorts; broken-coupling residual score 0.84 then 0.46.
- **Raw docking scores carry receptor bias (165)**: Vina AUROC 0.66 imatinib / 0.53 erlotinib vs Davis Kd; ATP/ADP-crystallized non-binder pockets score near the top.
- **Mean-pooled small PLM: topology-simple folds only (172)**: fold 1-NN across superfamilies 0.14 vs Smith-Waterman 0.03; all-alpha 0.30, all-beta 0.22, alpha+beta 0. Extends finding 3.
- **Counterexample to finding 3 (171, PASS)**: frozen ESM-2 + trained per-residue head beats named baselines for catalytic residues on the literature-curated M-CSA atlas (AUPRC 0.205 vs 0.045). A small PLM works when the task is local (per-residue) and has dense labels.
- **Topology-only link prediction = degree (199)**: Adamic-Adar 0.753 vs preferential attachment 0.750 on the STRING v11->v12 time split.
- Terminal: 173 (clean null: AlphaMissense equally reliable on poorly and well studied genes); 179/079 (terminated on user instruction).
- **Pan-cancer cfDNA axis = liver signal (158)**: leave-one-cancer-out shared 5hmC axis 0.65 (elastic-net 0.65); top genes hepatocyte (PROX1, HNF4G, PLG, NR1H4); thyroid <= chance for all methods.
- **Injury barcode = repair clock (155)**: leave-one-organ-out 25-gene barcode 0.82 vs Hallmark inflammatory 0.79 (+0.03, below locked +0.05); external kidney RNA-seq 0.60; genes are proliferation + myeloid + matrix (days-scale repair), blind to 0-120 min jejunal ischaemia-reperfusion.
