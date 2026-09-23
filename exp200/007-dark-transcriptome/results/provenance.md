# Provenance (DOC-1-007)
- GENCODE v45 protein-coding transcripts: https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_45/gencode.v45.pc_transcripts.fa.gz
  SHA-256 2b30d353f3fe36b45fa9d7ae0aab7755700f55067d1bff26dd9fe0f7c3e05cd5
- GENCODE v45 lncRNA transcripts: https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_45/gencode.v45.lncRNA_transcripts.fa.gz
  SHA-256 b0129aba06b75e93e05d69972ca7c1d9f4a9866803f958a65a7b0345fb7275b9
- NONCODE v6 human lncRNA (frozen external): http://www.noncode.org/datadownload/NONCODEv6_human.fa.gz
  SHA-256 67ded28c8744bbc6657b8c8273da31f7a2cb1504627bb8c02076d9b9f1a50fc9
- Split: md5-hash 90/10 (results/split.json); NONCODE deduped vs GENCODE by exact
  sequence match: 173,112 raw -> 138,348 kept (>=300nt, no exact GENCODE match).
- Controls: dinucleotide-block shuffles (locked implementation in code/prep.py).
- Env: torch 2.14.0+cpu, sklearn 1.7.2; seeds frozen.
