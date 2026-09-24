# 031F PROVENANCE
- AmPEP train: github.com/ShirleyWISiu/AmPEP M_model_train_AMP/nonAMP_sequence.zip
  (hash-verified vs 031 manifest: 4ea306a654433e4b / 00f6dffd1ccd9fee).
- iAMP-2L Supp-S2: github.com/BigDataBiology/macrel2020benchmark
  homology_effects/old_files/AMP.test.faa.gz (hash-verified 5ef4d00a679274e2).
- Frozen positives: 031 committed results/dramp_frozen_pos.json (2,068 sequences, pinned).
- Frozen negatives: rebuilt per locked procedure (GATES) from UniProt reviewed proteins via
  UniProt REST; seed 42; decontamination BLASTP-short 80% identity vs positives+train+dev.
- DRAMP 3.0 download site 404 on 2026-09-24 (http(s)://dramp.cpu-bioinfor.org/downloads/*) -
  documented; 031's pinned positives make the site non-blocking for this follow-up.
- All sources free/public; no money spent; nothing sent as the user.

## Addendum (2026-09-24 12:05, negative-set rebuild executed)
- UniProt reviewed proteins length 8-200 ID list: rest.uniprot.org/uniprotkb/stream?query=
  reviewed:true AND length:[8 TO 200]&format=list -> 180,056 IDs (11:36 IST).
- Seed-42 pick of 8,000; FASTAs via rest.uniprot.org/uniprotkb/accessions?accessions=<CSV>&format=fasta
  (batches of 200; all 8,000 fetched, 11:38 IST).
- Locked draw: 2,068 segments length-matched 1:1 per pinned positive, iterative seeded redraw
  until decontaminated (BLASTP-short pident>=80 & qcovs>=80 vs 2,068 pos + 3,268 train AMP +
  920 dev AMP). All 2,068 accepted unique; frozen_neg.json in workspace.
- Non-AMP dedupe rule verified against Macrel source: github.com/BigDataBiology/macrel
  train/build-AMP-table.py (AMP-first seen-set; fetched 11:42 IST).
- DRAMP site remained 404 throughout (positives pinned in-repo per GATES).
