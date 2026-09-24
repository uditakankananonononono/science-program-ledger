# P21-06 Protocol and Gates - LOCKED BEFORE RESULTS (lane D, 2026-09-24 ~13:37 IST)

Spec: doc290/cbio060-il6-tnbc-model/06-patient-specific-pathway-activity.md. Spec gates kept; amendments
locked before any expression or outcome value is fetched. (Only cBioPortal attribute names were listed.)

## Data (cBioPortal public API, fetched at run time)
- METABRIC (brca_metabric): mRNA profile brca_metabric_mrna (microarray log intensity). TNBC = sample
  ER_STATUS, PR_STATUS and HER2_STATUS all "Negative". Endpoint = RFS (RFS_MONTHS/RFS_STATUS).
- TCGA PanCancer Atlas (brca_tcga_pan_can_atlas_2018): brca_tcga_pan_can_atlas_2018_rna_seq_v2_mrna,
  log2(x+1). TNBC proxy = SUBTYPE == BRCA_Basal (IHC receptor status is not in the PanCan clinical table).
  Endpoint = PFS (PFS_MONTHS/PFS_STATUS; Liu 2018 PFI).

## Pre-locked amendments
- A1 host model: P21-01 surrogate (BIOMD0000000535, nominal parameters). Output = untreated steady-state tissue
  (gut compartment) pSTAT3 after 3000 h. Not the unpublished CBIO060 model.
- A2 gene -> model mapping: IL6 -> ksynthIL6Gut; IL6R -> kRsynth; JAK1 -> kcatSTATPhos; PTPN2 -> VmSTATDephos;
  ADAM17 -> kRShedding; STAT3 -> total tissue STAT3 pool (initial STAT3 and pSTAT3 of the gut compartment
  scaled together). IL6ST is left out (in this model gp130 has no synthesis parameter to scale).
- A3 scaling: per cohort, z = z-score of the gene's log expression across TNBC patients; parameter multiplier
  = 2^(s*z), with s = 0.5 as primary. s in {0.25, 1.0} is the G3 sensitivity analysis.
- A4 G1: patients split at the cohort median of simulated pSTAT3. Cox HR (high vs low), pre-declared direction
  high = worse. Pass iff HR >= 1.5 with p < 0.05 in >= 1 cohort AND HR > 1 in the other.
- A5 G2: Harrell C-index, with higher value = higher risk, for continuous simulated pSTAT3 vs the simple
  pathway score (mean z of the 6 mapped genes). Raw IL6 and raw STAT3 are reported too. Pass iff simulated
  C-index >= simple score + 0.02 in BOTH cohorts. Otherwise the result is "mechanistic modelling adds nothing
  here".
- A6 G3: HR and C-index reported for s = 0.25 / 0.5 / 1.0 in both cohorts (reporting gate).
- Patients with missing expression for any mapped gene or missing endpoint are excluded; counts reported.
