# exp200 Cross-Experiment Findings

Program-level findings that recur across experiments. Every entry cites the experiments whose
locked-gate reports support it; numbers are from the frozen/final scores in each REPORT.md.
Lanes append their entries as experiments close. Created 2026-09-24 (EXP-1 seed).

## 1. Dev-to-frozen inversion: mechanistic baselines win out-of-domain
The program's strongest cross-cutting finding. Learned models that beat mechanistic baselines
in dev cross-validation LOSE to them on frozen independent cohorts; dev-CV gains routinely
invert. Five instances:

- **026 viral-infection-atlas**: learned NMF top-50 signature wins dev (AUROC 0.6189 vs 0.5886)
  but loses frozen cross-virus transfer to the plain ISG signature (0.5605 vs 0.6193).
- **027 spatial-deconv-gnn**: NNLS baseline beats the locked GNN on BOTH dev (0.6856 vs 0.409)
  and frozen (0.7273 vs 0.363); pre-registered P1 rescue failed too (0.299 frozen).
- **030 drug-response-transfer**: simple ERBB2+EGFR biomarker (+0.415 dev / +0.478 frozen PCC)
  beats both learned transfer arms (ridge +0.163/+0.214; quantile-aligned +0.214/+0.213).
- **032 microbiome-metabolite**: dev ARM B ridge 85.0% / MCC 0.454 collapses to 30.0% on the
  frozen 388-sample HMP2 cohort, below the mechanistic ARM A protocol (45.0% / 0.289).
  Harness validated by reproducing the published ENVIM 37% cross-cohort rate EXACTLY (37.1%).
- **033 phage-host-gnn**: dev graph gains (20.95%, +7.3pp over no-graph, all 10 folds) collapse
  frozen to 12.20% vs ARM A KNN-d2 59.35%; CRISPR-spacer rescue real but neutral (+0.00pp).

Rule: out-of-domain, prefer the mechanistic baseline; treat dev-CV gains of learned models as
evidence ABOUT the dev distribution only.

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
