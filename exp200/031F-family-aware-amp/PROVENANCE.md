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
