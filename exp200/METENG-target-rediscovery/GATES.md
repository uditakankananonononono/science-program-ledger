# METENG-insert — Blind Knockout-Priority Scan for Metabolic-Engineering Target Rediscovery
# GATES locked 2026-09-24 ~03:38 IST, BEFORE any scoring. Main-approved design (03:32).
# Origin: DOC-1-008's supplementary growth-coupled scan blind-rediscovered FUM1/SDH2/SDH3
# for succinate. This experiment tests whether that was luck or a general capability.

## Question
Does a blind growth-coupled single-knockout scan (max product export at biomass >= 90%
of the strain's OWN max growth, "gc90") rank PUBLISHED, experimentally validated yeast
metabolic-engineering knockout targets above seeded decoys, across a held-out product panel?

## Model + the ONE locked model edit
- Yeast8 (same SHA-pinned file as DOC-1-008; provenance there and in PROVENANCE.md).
- ONLY model edit (locked, mirroring published secretion physiology): the three JEN1
  monocarboxylate transporters (r_1254 pyruvate, r_1136 D-lactate, r_1207 L-lactate; gene
  YKL217W) are made REVERSIBLE, as shipped they are irreversible uptake-only which makes
  lactate/pyruvate export impossible - contradicted by every pdc-negative / LDH-engineered
  strain. Verified after edit: WT growth unchanged (0.0811); product tmax > 0 for all panel
  products (pyruvate 1.86, D-lactate 1.57, L-lactate 1.52, fumarate 1.42, ethanol 1.86,
  2,3-butanediol 0.93, succinate 1.29 mmol/gDW/h at 10% biomass floor).
- Solver: HiGHS via scipy linprog (008 Addendum A pipeline), GPR-aware KOs, 20s time limit.

## Panel (frozen)
EVALUATED (5): pyruvate (r_2033), L-lactate (r_1551), fumarate (r_1798), ethanol (r_1761),
(R,R)-2,3-butanediol (r_1549).
CALIBRATION ONLY - EXCLUDED FROM SCORING: succinate (r_2056) - it generated the method.

## Frozen benchmark target sets (published, experimentally validated; gene IDs verified
## against SGD phenotype_data.tab; citations in PROVENANCE.md)
- pyruvate: {PDC1 YLR044C, PDC5 YLR134W, PDC6 YGR087C}  (van Maris 2004 AEM 70:159, PMC321313)
- L-lactate: {PDC1 YLR044C, ADH1 YOL086C}  (bbb 70:1148 doi:10.1271/bbb.70.1148; PubMed 19122995)
- fumarate: {FUM1 YPL262W}  (PLoS ONE 2012 7:e52086 PMC3530589; fumarase-deficient mutants)
- ethanol: {GPD2 YOL059W, GPD1 YDL022W, FPS1 YLL043W, ADH2 YMR303C, DLD3 YEL071W}
  (gpd2Δ ethanol-yield literature incl. PMC9375381, J Biol Eng 12:29, Microb Cell Fact 2022 s12934-022-01885-3)
- (R,R)-2,3-butanediol: {PDC1 YLR044C, PDC5 YLR134W}  (OSTI 1401461; s13068-018-1176-y)
- DISCLOSED correlations: PDC1 appears in 3 sets (pyruvate/lactate/BDO share the pyruvate
  node - real biology, disclosed). FUM1 is calibration-adjacent (succinate top hit): fumarate
  is an independent objective with independent literature, retained, but the gate verdict
  must hold WITH and WITHOUT fumarate (sensitivity check, frozen).

## Rules (frozen)
- R1 Eligibility: product needs tmax > 0 after the locked edit (verified above, pre-lock).
- R2 Essential targets: a published target essential/unsolvable in the edited model is
  excluded from its set and reported; product scored on the remaining set (all 12 target
  genes verified NON-essential pre-lock in the unedited scan; essentiality is recomputed
  on the edited model before scoring).
- R3 Statistic: per product, gc90 scan over all non-essential genes; rank by export desc
  (ties: average rank); target score = mean percentile of the product's target set.
  Null = 200 seeded random same-size subsets of the non-target scanned genes (seed 20260924).
  Product PASSES iff target score exceeds ALL 200 null scores (strict perm criterion).
- R4 GATE: >= 3 of 5 evaluated products pass, AND the with/without-fumarate sensitivity
  gives the same verdict.
- R5 Named-baseline arm (beat-or-document): published computational-method target lists on
  overlapping products - OptGene (Otero 2012: sdh3/ser3/ser33 for succinate, calibration
  context) and the in-silico-aided fumarate study (PMC3530589) - compared on overlap@k with
  our top-ranked lists; agreement or documented loss, honestly.
- R6 Ablation disclosure: the non-growth-coupled scan (008 G2 style, 10% floor) is
  degenerate (all-tie) and is reported as the documented ablation showing growth coupling
  carries the signal.
- R7 Tool: meteng_scan.py CLI (product exchange -> ranked KO list), smoke-tested vs WT.
- R8 Nomination: highest-ranked gene NOT in any literature set, from the strongest-passing
  product, nominated for wet-lab validation.
- R9 FAILURE TREE: < 3 products pass (or sensitivity flips the verdict) -> documented
  boundary ("008's rediscovery was succinate-specific luck"), no relaxation, no new arms.
