# DOC-1-011 PROVENANCE
All data from UniProtKB REST API (https://rest.uniprot.org/uniprotkb/), public, no auth. Downloaded 2026-09-24 ~05:04 IST. Pool definitions per GATES.md as amended by GATES_ADDENDUM_A.md (sha256 efbc3ec6325dc808...; see file). Exact ID lists: data/pool_ids.json + data/frozen_pos_ids.json (seeded RNG seed 42). File SHA-256s: data/SHA256SUMS.txt.

Queries (live counts at download time):
- Seeds/held-out: protein_name:Cas9 (1,768; seeds 150 + held-out 200), protein_name:Cas12a (27; 12/15), protein_name:Cas13a (44; 20/24) -> data/dev_cas.fasta (421 entries).
- Dev decoys: ((organism_id:83333) OR (organism_id:224308)) AND reviewed:true NOT "CRISPR" (8,698; sampled 1,500) -> data/dev_decoys.fasta.
- Hard decoys: reviewed:true AND ("restriction endonuclease" OR "DNA-directed DNA polymerase" OR "DNA-directed RNA polymerase") NOT CRISPR NOT cas9 NOT cas12 NOT cas13 (7,150; sampled 300) -> data/hard_decoys.fasta.
- Frozen positives: (cas9 OR cas12 OR cas13) AND date_created:[2022-01-01 TO *] (35,332 hits; sample drawn from first 2,500 default-ordered entries - documented approximation), filtered to name containing Cas9/Cas12/Cas13 and length 400-2000 aa (650 pass), seeded sample 300 -> data/frozen_pos.fasta. Family mix of sample: 298 Cas9 / 1 Cas12 / 1 Cas13 (post-2022 deposits are overwhelmingly Cas9; documented).
- Frozen decoys: reviewed:true AND taxonomy_id:2 AND date_created:[2022-01-01 TO *] NOT CRISPR (2,135; sampled 300) -> data/frozen_decoys.fasta.

Context citations: Altae-Tran et al., Science 2023, doi:10.1126/science.adi1910 (FLSHclust discovery pipeline, Zenodo archive referenced in paper); Makarova et al., Nat Rev Microbiol 2020;18:67-83 (Cas classification); Steinegger & Soding, Nat Biotechnol 2017 (MMseqs2 baseline, release 15-6f452 static AVX2 binary, github.com/soedinglab/MMseqs2/releases); Lin et al., Science 2023 (ESM-2, esm2_t6_8M_UR50D weights dl.fbaipublicfiles.com).
