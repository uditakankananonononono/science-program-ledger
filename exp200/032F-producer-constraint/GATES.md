# DOC-1-032F: Producer-Annotated Constraint Model — GATES (locked before any scoring)

Follow-up to DOC-1-032 (documented boundary: dev ridge 85.0% collapses to 30.0% on frozen
HMP2 vs ARM A MelonnPan 37.1%, ENVIM anchor matched exactly). Parent-approved follow-up
queue 2026-09-24 10:59:00; approved sketch: "mechanism-constrained model — restrict features
to producer-annotated reactions (G4's butyrate-driver finding generalized: only taxa
annotated to produce the metabolite), frozen HMP2. Gate: frozen >= ARM A + 5pp."
Fresh experiment, fresh gates; NOT a retry of any 032 gate (008->METENG pattern).

## Bar correction (disclosed, locked)
The sketch's "ARM A 45.0%" is the DEV ARM A number. Frozen ARM A = 37.1%. All bars below
use FROZEN numbers from 032's committed artifacts (armA_frozen_rho.json,
armB_frozen_rho.json), restricted to the same evaluable compound set.

## Eligibility findings (locked in as facts, all verified pre-gate)
- Stratified UniRef90 not retained in 032's workspace; design uses SPECIES-LEVEL taxa
  abundances + producer-annotation constraint (the approved sketch's "only taxa annotated
  to produce the metabolite").
- Producer annotations: AGORA2/DEMETER experimentally-curated flat tables (opencobra
  COBRA.papers 2021_demeter/input: secretionProductTable, FermentationTable,
  BileAcidTable, PutrefactionTable; 7,302 strains, literature-referenced 0/1 flags).
  Species = first two tokens of MicrobeID (NCBI-style, matches MetaPhlAn naming).
- Evaluable compounds: 12 of the 70 frozen-mapped metabolites carry any producer
  annotation (propionate, butyrate/isobutyrate, cholate, chenodeoxycholate, deoxycholate,
  lithocholate, lithocholic.acid, deoxycholic.acid, chenodeoxycholate.deoxycholate,
  putrescine, glutamate, N.acetylspermidine). Producer-species counts range 1-169
  (coverage032F.json, committed). Small-count compounds retained with disclosed caveat;
  no outcome-driven subsetting.
- Train join: seqgroup ibd_taxa (201 species x 155 PRISM samples) + ibd_metadata
  SRA_metagenome_name column = the G-number key joining PRISM.XXXX taxa columns to
  MelonnPan mpcomp.txt metabolite rows (verified: keys match 1:1 in order).
- Frozen features: HMP2 per-sample taxonomic_profile.biom from the official IBDMDB Globus
  endpoint (URL scheme verified live) for the 388 paired samples (paired_ids.json).
- Frozen labels: 032's committed hmp2_meas.npy + hmp2_final_map.json rows for the 12.

## Design
- Features: log1p(relative abundance x 1e6) of species-level taxa.
- Constraint (the claim): for metabolite M, features = ONLY species annotated as producers
  of M in the DEMETER tables (union across the mapped table/columns per M, locked in
  coverage032F.json). No other features.
- Model: per-metabolite RidgeCV, 032 ARM B's exact protocol (alphas logspace(-3,3,13),
  inner LOO pick). Train on PRISM (155). Score frozen on HMP2 (388).
- Metrics (032's locked metrics): per-compound Spearman rho; "well-predicted" = rho >= 0.3;
  headline = fraction well-predicted over the 12 compounds.

## Gates
- G1 (sanity halt): PRISM 5-fold CV (seed 0) mean rho over the 12 >= 0.10. Else incoherent
  - document, stop, report to parent.
- G2 (the claim, frozen): constrained model well-predicted fraction over the 12 >= BOTH
  frozen ARM A's fraction on the same 12 + 5pp AND frozen ARM B's fraction on the same 12
  + 5pp. (Named published baseline = the executed MelonnPan protocol, per 032's Addendum B;
  ENVIM 37% cross-cohort anchor already reproduced by 032.)
- G3 (mechanism repair, frozen): propionate rho >= 0.3 AND butyrate rho >= 0.3 (032's G4
  named SCFA transfer the weak point: propionate -0.03 ARM B / -0.06 ARM A; butyrate below
  threshold both arms). This is the mechanism-targeted test.
- G4 (provenance, runs regardless): per-compound driver species (top |coefficient|) vs
  literature producer lists (e.g., butyrate: Faecalibacterium/Roseburia/Agathobacter);
  producer-coverage per compound (how many annotated producers are present at >0.1%
  mean abundance); wrong-compound taxonomy.
- G5: CLI metabolite_predict_constrained.py (producer-constrained, 12 compounds) +
  prospective lab nomination.
- Failure tree: G1 fail -> halt to parent. G2 fail -> DOCUMENTED BOUNDARY (the constraint
  IS the mechanism-targeted fix; no further rescue pre-registered). G3 fail with G2 pass
  -> report both, parent adjudicates (constraint transports overall but SCFA mechanism
  remains broken would itself be the finding).

## Prospective lab nomination (locked)
An IBD metabolomics unit imputing SCFAs and bile acids from metagenomes-only cohorts:
producer-constrained predictors for the 12 annotated compounds, validated against targeted
assays.

## Scoring discipline
GATES + coverage032F.json + PROVENANCE committed BEFORE any model is fit or scored.
Thresholds never relax after seeing outcomes.
