# DOC-1-012 PROVENANCE
UniProtKB REST API (https://rest.uniprot.org/uniprotkb/), public, no auth. Downloaded 2026-09-24 ~05:36 IST. Split definitions per GATES.md. Seeded RNG seed 42. File SHA-256s: data/SHA256SUMS.txt. Exact accession->class assignments: data/splits.json.
- Pre-2022 pool: reviewed:true AND ec:* AND date_created:[* TO 2021-12-31] AND length:[40 TO 2000]. 10,000 candidates pulled from the first 20 default-ordered pages of 274k+ (documented approximation, same as 011). Natural class mix: 1:1429, 2:4013, 3:3327, 4:360, 5:338, 6:270, 7:263.
- Train: proportionally stratified seeded sample n=3,000 (mix: 2:1204, 3:998, 1:429, 4:108, 5:101, 6:81, 7:79). Dev: disjoint n=800. Multi-EC entries: first EC used (per gates).
- Frozen: reviewed:true AND ec:* AND date_created:[2022-01-01 TO *] AND length:[40 TO 2000] (4,470 pulled of 4,649), seeded sample n=1,200.
Model: ESM-2 esm2_t6_8M_UR50D (Lin et al., Science 2023; weights dl.fbaipublicfiles.com). Baseline: MMseqs2 15-6f452 (Steinegger & Soding, Nat Biotechnol 2017; github.com/soedinglab/MMseqs2/releases). Context: CLEAN (Yu et al., Science 2023), DeepEC (Ryu et al., PNAS 2019).
