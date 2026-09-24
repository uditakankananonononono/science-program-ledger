# 019F PROVENANCE
All public, free sources; pulled 2026-09-24 13:34-13:58 IST.
- UniProt proteomes endpoint (rest.uniprot.org/proteomes/search, JSON/TSV):
  Halobacteria 988 proteomes (Reference 283, Non-Reference 463, Excluded 242);
  Thermococcales 111 + Sulfolobales 482 + Methanococcales 69 = 662 (Reference 83);
  control frame: first 500 reference-proteome records in UniProt cursor order for
  query "bacteria", organism names containing "halo" excluded (485 eligible),
  rng-seed-7 sample 100. Frames re-drawn per Addendum B: halo100 = rng-seed-7 over
  283 Halobacteria reference proteomes; thermophile panel = all 83 eligible
  reference proteomes (pool < 100, no sampling).
- Protein sequences: rest.uniprot.org/uniprotkb/stream?query=(proteome:UP...)&
  format=fasta. UniProtKB indexes Reference proteomes only (verified: Non-Reference
  UP000297053, UP000011618, UP000011673 return x-total-results 0) - this constraint
  drove Addenda A (13:45) and B (13:51), both locked BEFORE gate scoring on the
  amended samples. Diagnostic partial medians computed during frame debugging
  (halo n=40, therm n=35, pre-amendment frames) are diagnostics only, not gate
  outcomes. Final downloads achieved 100/100 halo, 83/83 therm, 100/100 control.
- Dev cohort: 019's committed results/hypersaline_dev.fasta (MGnify MGYS00005861,
  pipeline 5.0 assemblies, 30-300aa filter, rng-7; see 019 PROVENANCE).
- Frozen cohort: MGnify MGYS00000384 (Santa Pola Saltern) analyses MGYA00002654 +
  MGYA00002655, download *_CDS.faa.gz (pipeline 1.0 metagenomic reads; the study
  has no v5.0 assemblies - pipeline difference from dev documented), same 30-300aa
  filter, dedup, rng-seed-7 shuffle, capped at 3000 (mirrors 019's construction).
- SSU consistency: MGnify analysis MGYA00002654 download SRR944625_FASTQ_otu.tsv
  (483 SSU assignments; k__Archaea 8.9%).
- MMseqs2 16-747c6 (static avx2 build), search -s 7.5 -e 1e-5 -c 0.5 --cov-mode 0,
  best hit per query by e-value. G2 run once (single pass, locked).
- SANDBOX LOSS NOTE: the compute sandbox was rebuilt at ~14:00 IST, destroying raw
  intermediates (proteome fastas, hits.m8 files). Aggregate gate outcomes in
  results/*.json were recorded at scoring time (13:54-13:58 IST) and are
  deterministically regenerable: all frames, seeds, endpoints, and filters are
  specified above; code/g0_download.py logic is described in this file and the CLI
  reproduces G1/G2 searches exactly (validated against the recorded dev numbers).
