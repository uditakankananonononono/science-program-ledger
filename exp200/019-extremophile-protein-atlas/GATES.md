# DOC-1-019 GATES - locked 2026-09-24 06:59 IST BEFORE any protein content is inspected
Topic: A Metagenomic "Protein Atlas" of Extreme Environments.
Question: do extreme environments leave distinct, mechanistically-interpretable compositional
fingerprints on their metagenomic protein inventories, learnable from sequence composition alone?
Explicitly aligned with the program's 011-015 rule: NO PLM predictor; composition features only.

## Data (locked; eligibility probed via MGnify API metadata only - no protein sequences read yet)
MGnify v5.0 assembly analyses, "Predicted CDS (aa)" downloads, all free public:
- vent: MGYS00002304 (9 analyses) - hydrothermal vents
- hotspring: MGYS00005963 (5 analyses) + frozen-only studies MGYS00003602, MGYS00002328, MGYS00002327 (1 each)
- hypersaline: MGYS00005861 (6 analyses)
- control: MGYS00005863 (6 analyses) - marginal sea, non-extreme marine
Split rule (locked, deterministic): within each main study, analyses sorted by accession ->
first 60% dev / last 40% frozen. Hotspring frozen = the 3 separate studies (true study-level holdout).
Per biome per split: exact-sequence dedupe, keep length 30-300 aa, reservoir-sample 3000 (seed 7).

## Features (locked)
Dipeptide composition (400 dims, normalized) + length. No nucleotide features (aa-only downloads).

## Named published baselines (locked)
- Thermal arm: IVYWREL residue fraction (Zeldovich, Berezovsky & Shakhnovich 2007, PLoS Comput Biol -
  the published thermophile signature) as a single-feature score.
- Hypersaline arm: D+E residue fraction (the published halophile acidic-proteome signature, Lanyi 1974 / Oren 2013).

## Tasks & gates
G1 (dev, 5-fold stratified CV seed 7):
  Arm T: thermal (vent+hotspring dev) vs non-thermal (hypersaline+control dev).
  Arm S: hypersaline dev vs all other dev.
  Each arm: dipeptide-LR (L2 C=1.0, class_weight balanced) AUROC > named-baseline AUROC + 0.03.
  Document loss per arm otherwise.
G2 (frozen, model fit on dev only, single pass, no refit): each arm AUROC >= 0.70 absolute AND
  >= frozen named-baseline AUROC + 0.01. Hotspring side of Arm T frozen is study-level;
  vent/hypersaline/control frozen are sample-level (documented limitation - no second v5.0 study exists).
G3 (mechanism vs literature): (a) Spearman correlation of learned Arm-T dipeptide weights with
  IVYWREL membership of the dipeptide's residues; (b) Arm-S weights correlated with D/E content;
  (c) atlas table: IVYWREL and D+E fractions per biome with expected ordering vent/hotspring >
  control for IVYWREL, hypersaline >> others for D+E. PASS iff (c) ordering holds AND (a),(b) positive.
G4: results/atlas_signatures.tsv (top 20 discriminative dipeptides per biome vs rest) +
  classify_env.py CLI + prospective lab nomination (Banfield lab, UC Berkeley).

## Failure tree (locked)
G1 arm fail -> P1: add length + charged-run (>=4 consecutive D/E/K/R) features. P2: restrict to 60-200 aa.
Frozen collapse below baseline while dev passes -> documented boundary: signature is study-batch,
not environment (batch guard). All arms fail -> documented boundary: environment fingerprints not
learnable from composition at this scale/pipeline. Thresholds never relax after outcomes.
