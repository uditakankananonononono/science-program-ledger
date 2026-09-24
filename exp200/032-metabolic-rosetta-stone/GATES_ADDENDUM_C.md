# GATES ADDENDUM C - DOC-1-032 (locked 2026-09-24 09:17 IST, BEFORE any frozen HMP2 scoring)

## Trigger (documented eligibility finding, not a result)
The locked FROZEN cohort (NLIBD) is unavailable in practice:
- Metabolite mapping succeeded (57/80 MelonnPan compounds map to ST001000 annotated
  metabolites after name normalization, >50% so the locked <50% contingency did NOT fire).
- Sample-ID mapping failed: the repo's NLIBD UniRef90 table (melonnpan.test.data.txt) uses
  G-series IDs (G83321-style) while Metabolomics Workbench ST001000 measurements use numeric
  sample IDs (7122xxx-style). Documented hunt, all negative: Workbench metadata tabs
  (SamplePrep/Subject/Collection) contain no G-IDs; mwTab SUBJECT_SAMPLE_FACTORS carries
  clinical fields only; positional/middle-digit hypotheses tested and rejected (9/222 match
  = coincidence level); Mallick 2019 supplement MOESM4 carries model PREDICTIONS keyed by
  LLDeep-style IDs, not measurements; ibdmdb tunnel paths 404; HMP DACC host unreachable;
  ENVIM repo (jialiux22/ENVIM) is code-only with no data in any commit.
No public bridge between the two ID namespaces exists. NLIBD frozen scoring is therefore
impossible without fabricating a mapping, which is not permitted.

## Change (locked)
The locked GATES contingency ("if NLIBD frozen is unavailable, switch FROZEN to
HMP2/Lloyd-Price public tables with the same gates") is INVOKED, extended from the literal
metabolite-mapping trigger to the equivalent sample-mapping failure (same root cause: public
NLIBD tables are not joinable). FROZEN = HMP2 / Lloyd-Price 2019 IBDMDB cohort (independent
of PRISM and of the shipped weight matrix's training data):
- Metabolite measurements: HMP2_metabolomics_w_metadata.biom(.gz), served anonymously from
  the official IBDMDB Globus endpoint (g-227ca.190ebd.75bc.data.globus.org/ibdmdb/products/
  HMP2/MBX/), VERIFIED LIVE 2026-09-24 (HTTP 206 range GET).
- UniRef90 features: per-sample HUMAnN2 output bundles (func_profiles/<SAMPLE>_humann2.tar.bz2,
  1338 samples listed on the official IBDMDB MGX products page 2026-09-24); the unstratified
  genefamilies table of each paired sample is converted to relative abundance (column total =
  1 over unstratified UniRef90 rows), matching the PRISM training table's units (verified:
  PRISM training.data values are relative abundances, e.g. col-max 3.3e-3).
- Sample pairing: HMP2 metadata (hmp2_metadata_2018-08-20.csv, official Globus endpoint,
  VERIFIED LIVE) joins MGX sample IDs to metabolomics samples by subject+visit; pairing rate
  and final n disclosed in the manifest. Multiple visits per subject are kept (published
  anchors likewise used all paired samples); disclosed in the manifest.
- Metabolite mapping: HMP2 biom metabolite names mapped to the locked 80-compound set by name
  normalization, same procedure as dev; mapping rate disclosed. CONTINGENCY (locked now): if
  <50% of the 80 compounds map to HMP2 measured metabolites, the frozen arm is a DOCUMENTED
  BOUNDARY (data availability), not a model failure.
- 028/031 eligibility: label granularity = per-sample metabolite abundance vs per-sample
  prediction (match); cohort disjointness = HMP2 subjects are a different study/clinic system
  from PRISM and NLIBD, verified by ID namespaces at manifest.

## Unchanged
Everything else stands as locked in GATES.md + ADDENDUM B: ARM A(frozen) = shipped published
weight matrix applied cross-cohort (now to HMP2); ARM B(frozen) = full-PRISM-trained ridge;
G3 numbers unchanged (ARM B >= ARM A + 3pp AND >= ARM B dev fraction - 15pp); G1 frozen
coherence band [0.10, 0.50] unchanged. Published anchors for the new frozen cohort:
ENVIM paper Table 2 Lloyd-Price DNA: MelonnPan 37%, ENVIM 62% (cross-cohort application of
PRISM-trained models, same protocol as ARM A/B frozen); Mallick 2019 HMP2 within-cohort CV
53.8% is an upper reference only (different protocol, within-cohort).
