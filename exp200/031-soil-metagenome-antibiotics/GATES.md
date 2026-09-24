# GATES - DOC-1-031 (locked 2026-09-24 08:39 IST, BEFORE any model fitting or scoring)

## Claim
A compact, in-envelope sequence model discovers antimicrobial peptides (the antibiotic
candidates of soil metagenomes) as well as or better than the published state of the art:
trained on the Macrel paper's exact training protocol, it beats Macrel's published MCC on the
paper's own frozen test set, generalizes to an independent frozen AMP cohort (DRAMP), and its
top-scoring soil-metagenome candidates are interpretable against known AMP biology.

## Topic fidelity
"Discovering Novel Antibiotics from Soil Metagenomes": the deliverable is an AMP-discovery
classifier + a run over soil-derived metagenomic AMP candidates (AMPSphere soil subset),
nominating novel candidates (no close DRAMP match) for prospective wet-lab screening.

## Data (eligibility verified BEFORE this lock)
- TRAIN: AmPEP training set (M_model_train_AMP/nonAMP zips, github.com/ShirleyWISiu/AmPEP,
  62KB zip verified 200 OK) + iAMP-2L Supp-S1 bench (AMP.train_bench.faa.gz, 3,887 seqs,
  pre-extracted in BigDataBiology/macrel2020benchmark homology_effects/old_files/, downloaded
  and counted 2026-09-24). Dedup per the Macrel build-AMP-table.py protocol (AmPEP pos/neg
  exact duplicates removed).
- DEV TEST (the paper's comparison point): iAMP-2L Supp-S2 test (AMP.test.faa.gz, same source;
  VERIFIED 920 AMP + 920 NAMP, balanced) - the exact set behind Macrel paper Table 1.
- FROZEN external cohort: DRAMP 3.0 natural AMPs (dramp.cpu-bioinfor.org natural_amps.txt,
  VERIFIED 13,546 rows with sequences+activities 2026-09-24), filtered to Antibacterial
  activity, length 10-100aa, valid amino acids, deduped, and homology-pruned at 80% identity
  vs ALL training+dev sequences (in-envelope word-based clustering). Negatives: length-matched
  random segments from UniProt reviewed proteins excluding any DRAMP entry - same "non-AMP"
  label granularity as the dev statistic (028 rule).
- NAMED PUBLISHED BASELINES on the same dev test set (Macrel paper Table 1, PMC7751412 XML
  extracted 2026-09-24): Macrel MCC 0.90, MacrelX 0.91, iAMP-2L 0.90; AmPEP 0.92 flagged by
  the paper itself as train/test-overlap-inflated - NOT the baseline, reported for context.
- SOIL APPLICATION: AMPSphere v2022-03 (ampsphere.big-data-biology.org) candidates annotated
  to soil samples; novelty = <=80% identity to any DRAMP entry (word-based clustering estimate).

## Arms
- ARM A (sanity anchor): in-envelope reimplementation of the Macrel feature set
  (macrel/AMP_features.py vendored: AAC, grouped AAC, charge, hydrophobicity moments, etc.) +
  random forest. Must reproduce published Macrel within tolerance -> G1.
- ARM B (the claim): compact 3-mer spectrum logistic regression (L2), interpretable weights,
  trained on the identical training pool. Fully in-envelope (sparse k-mer features, ~8k dims).
- P1 (pre-registered rescue if G2 fails): ARM B retrained after homology-pruning the training
  pool at 80% identity vs the dev test set (tests the paper's own leakage caveat), same gates.

## Metric
MCC (the paper's headline metric) at the 0.5 decision threshold; dev = iAMP-2L test (n=1,840),
frozen = DRAMP cohort (report n at manifest). All comparisons paired on the same sequences.

## Gates
- G1 (sanity halt): ARM A MCC >= 0.85 on dev (published Macrel 0.90 minus 0.05 tolerance).
  Else labels/features incoherent - document, stop.
- G2 (dev): ARM B MCC >= 0.92 (published Macrel 0.90 + 0.02) AND >= ARM A MCC + 0.02.
- G3 (frozen, DRAMP): ARM B MCC >= ARM B dev MCC - 0.10 AND >= ARM A frozen MCC + 0.02.
- Failure tree: G2 fail -> P1, same gates; P1 fail or G3 fail -> DOCUMENTED BOUNDARY (no
  further arms).
- G4 (mechanism, runs regardless): ARM B 3-mer weights vs known AMP biology (cationic Lys/Arg
  enrichment, amphipathic patterns); net charge / hydrophobic-moment distributions of true vs
  predicted AMPs; check top-weighted 3-mers against literature-described AMP motifs.
- G5: working CLI amp_predict.py + soil-metagenome candidate nomination (AMPSphere soil subset:
  top-ranked candidates with novelty evidence) + one prospective lab nomination.

## Prospective lab nomination (locked)
An antimicrobial-peptide wet-lab screening unit (MIC assays against ESKAPE panels): test the
top-ranked novel soil-metagenome candidates from the G5 run.

## Scoring discipline
Dataset manifest (file hashes, sequence counts per split, dedup counts) committed BEFORE any
training. Thresholds never relax after seeing results; errata in GATES_ADDENDUM files locked
before the outcomes they govern.
