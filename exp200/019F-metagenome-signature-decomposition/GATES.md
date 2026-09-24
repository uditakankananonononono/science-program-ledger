# DOC-1-019F: Metagenome Signature Decomposition — GATES (locked 2026-09-24 13:36 IST, before any scoring)

Follow-up to DOC-1-019 (boundary: canonical halophile D+E acidic-proteome signature
ABSENT/inverted in the only v5.0 hypersaline metagenome; open question: ecology vs
metagenomic mixing dilution). 019F decomposes metagenomes by protein origin to decide
which. Parent-approved sketch 13:35:27 ("lock G0-G3 numerically pre-scoring (margins,
e-value/coverage thresholds, assignment-rate floor)... If G0's organismal premise fails,
halt and report"). All thresholds numeric below.

## Data (live counts 13:34-13:35)
- HALOPHILE PANEL: 100 Halobacteria proteomes (rng seed 7) from UniProt proteomes
  (988 live, query Halobacteria; list pulled 13:35).
- CONTROL PANEL: 100 non-halophile proteomes (rng seed 7) from UniProt reference
  proteomes (proteome_type:1), excluding taxonomy_id:183963 (Halobacteria) and any
  organism with "halo" in its name (audit-logged).
- THERMOPHILE PANEL (G0 second clause only): 100 proteomes (rng seed 7) from
  Thermococcales + Sulfolobales + Methanococcales (662 live).
- DEV METAGENOME: 019's committed hypersaline assembly MGYS00005861 protein set
  (019's fetch_proteins.py, results/hypersaline_dev.fasta or rebuilt identically).
- FROZEN METAGENOME: Santa Pola Saltern assembly MGYS00000384 (MGnify, independent
  study/system), fetched with the same pipeline and 30-300aa filter.

## Locked mechanics
- D+E fraction = (D+E)/length over all proteins of a set; IVYWREL fraction likewise.
- ORIGIN ASSIGNMENT: MMseqs2 -s 7.5 search of each metagenome protein against the
  100-proteome Halobacteria protein DB; origin = halophile iff best hit has
  e-value <= 1e-5 AND query coverage >= 0.5. All other proteins = non-halophile-origin.
  Parameters identical for dev and frozen; single search pass per metagenome.
- Proteome downloads failing retrieval are dropped and counted in REPORT.

## Gates
- G0 (premise, halt-no-patch per parent 13:35:27): (i) median D+E fraction of the
  Halobacteria panel >= control panel median + 5 percentage points; AND (ii) median
  IVYWREL fraction of the thermophile panel > control panel median (directional). If
  either fails -> organismal premise broken; HALT, report to parent.
- G1 (dev decomposition): assignment rate in MGYS00005861 must be >= 10% (disclosed; if
  < 10% the decomposition is uninformative -> halt-disclose, report). Among assigned
  proteins: D+E fraction of halophile-origin >= D+E fraction of non-halophile-origin
  + 3 percentage points.
- G2 (frozen transport): same decomposition on MGYS00000384, same +3pp margin, single
  pass; assignment rate disclosed with the same 10% floor.
- G3 (mechanism, documented): dilution quantification - predicted bulk D+E from origin
  fractions vs observed bulk (does mixing arithmetically explain 019's inversion?);
  consistency of MMseqs2 origin assignments vs MGnify SSU phylum downloads; literature:
  Oren halophile proteomics, Fukuchi 2003, Zeldovich 2007, 019's atlas result.
- G4: signature_decompose.py CLI + REPORT.md + one prospective nomination.
- Failure tree: G0 halt -> report (no patch). G1 fail -> the inversion is ecology
  (community not salt-in), documented with numbers; parent adjudicates. G2 fail ->
  decomposition does not transport; boundary documented.

## Addendum A (locked 2026-09-24 13:45 IST, BEFORE any G0/G1/G2 outcome computation)
Sampling-frame repair. Discovery during data build: UniProtKB `proteome:` queries return zero sequences for proteomes with proteomeType 'Excluded' (no UniProtKB sequence coverage). 67/100 of the original rng-seed-7 halo100 drew Excluded proteomes; no outcome data have been computed.
Amended frame (no threshold, judge, or outcome changes):
- Eligibility: a proteome is G0/G1-eligible iff its UniProt proteomeType is not 'Excluded' (i.e., UniProtKB-covered). Halobacteria: 746/988 eligible (Reference 283 + Non Reference 463). Thermophile pool filtered the same way.
- Samples re-drawn: rng-seed-7 over each eligible pool (halo100; therm100), same procedure as locked. Control100 unchanged (all reference proteomes, all covered).
- Proteomes already downloaded that remain in the re-drawn samples are reused; compositions recomputed identically.
- Audit: eligibility lists, draws, and any residual empty-stream proteomes recorded in PROVENANCE.md.

## Addendum B (locked 2026-09-24 13:51 IST, BEFORE any gate scoring on the amended samples)
Sampling-frame repair, second stage. Discovery: UniProtKB `proteome:` sequence queries cover Reference proteomes only - 'Non Reference proteome' records carry proteinCount but have zero UniProtKB entries indexed (verified: UP000297053, UP000011618, UP000011673 all x-total-results 0). Addendum A's non-Excluded filter is therefore insufficient for data retrieval.
Amended frame (no threshold, judge, or outcome changes):
- Eligibility: proteomeType == 'Reference proteome'. Halobacteria eligible: 283/988. Thermophile eligible: 83/662.
- halo100: re-drawn rng-seed-7 from the 283 eligible (unchanged procedure). G0(i) bar unchanged (median D+E >= control median +5pp).
- Thermophile panel: all 83 eligible reference proteomes (pool smaller than 100 - no sampling possible). G0(ii) bar unchanged (median IVYWREL > control median, strict).
- Control100 unchanged.
- Diagnostic partial medians computed during frame debugging (halo n=40, therm n=35, pre-amendment frames) are recorded in PROVENANCE.md as diagnostics only and are NOT gate outcomes.
- Audit: eligibility lists, draws, download coverage recorded in PROVENANCE.md.
