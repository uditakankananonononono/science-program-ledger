# GATES - DOC-1-032 (locked 2026-09-24 09:00 IST, BEFORE any model fitting or scoring)

## Claim
A compact, in-envelope model translates gut microbiome functional profiles (UniRef90 gene
families) into host-relevant fecal metabolite levels - the "metabolic Rosetta Stone" - beating
the published MelonnPan model on an external IBD cohort (PRISM), with frozen cross-cohort
validation on NLIBD and mechanistic attribution for host-relevant metabolites.

## Data (eligibility verified BEFORE this lock)
- DEV: PRISM cohort (IBD, n=157) as shipped in biobakery/melonnpan: melonnpan.training.data.txt
  (157 x 811 UniRef90 features) + melonnpan.training.compounds.txt (157 x N metabolites,
  matched IDs VERIFIED identical 2026-09-24). Dev evaluation = 5-fold CV within PRISM (seed 0,
  fold assignment locked at manifest).
- NAMED PUBLISHED BASELINE: MelonnPan (Mallick et al 2019 Nat Commun 10:3136, PMC6637180) -
  the published pre-trained weight matrix (melonnpan.trained.model.txt, trained on HMP2 human
  gut data per the paper; external to PRISM/NLIBD, zero leakage) applied directly. Published
  performance anchors (verbatim from papers): 53.8% metabolites well-predicted (Spearman >=0.3,
  HMP2, Mallick 2019); ENVIM paper (PMC8573316) Mallick-cohort DNA testing: MelonnPan 38%,
  ENVIM 48%; Lloyd-Price DNA testing: MelonnPan 37%, ENVIM 62%; PRISM->NLIBD transfer
  (Table 3): MelonnPan 26%, ENVIM 34%.
- FROZEN: NLIBD cohort (n=65, independent country/clinic, never used in dev): UniRef90 features
  shipped as melonnpan.test.data.txt (65 x 811, IDs disjoint from PRISM, VERIFIED 0 overlap
  2026-09-24); metabolite measurements from Metabolomics Workbench ST001000 ("Gut microbiome
  structure and metabolic activity in IBD", 220 samples = PRISM+NLIBD, CC BY 4.0, existence
  VERIFIED 2026-09-24). Metabolite set = the repo's PRISM compounds mapped to ST001000 features
  by cluster name; mapping rate disclosed at manifest. LOCKED CONTINGENCY: if <50% of compounds
  map to NLIBD features at the manifest, Addendum switches FROZEN to HMP2/Lloyd-Price public
  tables (ibdmdb.org) with the same gates - locked, not post-hoc.
- Standardized eligibility checks (028 + 031 rules): label granularity = per-sample metabolite
  abundance vs per-sample prediction (match); cohort disjointness = PRISM vs NLIBD vs HMP2 are
  three independent studies, verified by ID namespaces at manifest.

## Arms
- ARM A (named published baseline): shipped MelonnPan pre-trained weight matrix applied to the
  811 UniRef90 features (no fitting; it is the published model as distributed).
- ARM B (the claim): compact multi-output ridge on log-transformed UniRef90 features
  (per-metabolite ridge, shared alpha grid by inner CV on training folds only), in-envelope.
- P1 (pre-registered rescue if G2 fails): CLR-transformed features + per-metabolite elastic net
  with q-value feature prefilter (ENVIM-style), same gates.

## Metric
Per-metabolite Spearman correlation (predicted vs measured) across the cohort's samples;
headline = fraction of metabolites well-predicted (r >= 0.3, the published criterion) + mean r.
All comparisons paired on the same metabolite set.

## Gates
- G1 (sanity halt): ARM A on PRISM yields fraction well-predicted within [0.15, 0.60] (the
  published cross-cohort range 0.26-0.538). Else data/model incoherent - document, stop.
- G2 (dev, PRISM 5-fold CV): ARM B fraction well-predicted >= ARM A + 5 percentage points AND
  ARM B mean Spearman >= ARM A + 0.05.
- G3 (frozen, NLIBD): ARM B (trained on full PRISM) fraction well-predicted >= ARM A + 3 points
  AND >= ARM B dev fraction - 15 points.
- Failure tree: G2 fail -> P1, same gates; P1 fail or G3 fail -> DOCUMENTED BOUNDARY.
- G4 (mechanism, runs regardless): top ARM B driver UniRef90s for host-relevant metabolites
  (SCFAs incl. butyrate, bile acids) vs literature-expected biology (e.g. butyrate-production
  pathways in Faecalibacterium/Roseburia); agreement/disagreement documented.
- G5: working CLI metabolite_predict.py + one prospective lab nomination.

## Prospective lab nomination (locked)
An IBD metabolomics unit running paired metagenome+metabolome profiling: use the cross-cohort
predictor to impute metabolites where only metagenomes exist, validated against targeted assays.

## Scoring discipline
Sample manifest (ID namespaces, fold assignments, compound->ST001000 mapping, file hashes)
committed BEFORE any training. Thresholds never relax after seeing results; errata in
GATES_ADDENDUM files locked before the outcomes they govern.
