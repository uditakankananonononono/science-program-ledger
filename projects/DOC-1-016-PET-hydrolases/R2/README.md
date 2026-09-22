# SP-003 Round 2 - Deep Orthogonal Validation (DOC-1-016 continued)

Locked-gate deep validation of the 468 Round-1 metagenomic PET-hydrolase candidates.

**Outcome: 5/7 gates PASS (G1,G2,G5,G6,G7); G3 and G4 FAIL and are preserved verbatim; overall gate verdict FAIL. Deliverable: a 20-candidate experimental-ready shortlist that survives every hard check.**

- `protocol/protocol.json` - locked gates (sha256 f665fc0d...) + `PROTOCOL_LOCK.txt`
- `protocol/environment_ledger.json` - open-source tool pins (MMseqs2 18-8cc5c, DIAMOND 2.1.13, Foldseek 10-941cd33 [installed, N/A], Biopython 1.88) with sha256s and recorded compute ceilings
- `code/` - idempotent, cache-backed pipeline: run_hmmscan.py, run_triad.py, run_provenance.py, run_rcsb_extension.py, pubmed_grounding_r2.py, make_shortlist.py, evaluate_gates_r2.py
- `results/` - gate_evaluation_r2.json, shortlist_20.json (rationale cards), triad_check.json, redundancy_clusters.json, antipanel_screen.json, environmental_provenance.json, rcsb_extension_51_150.json, r2_provenance_ledger.jsonl, pubmed_grounding_r2.json
- `data/` - candidates_468.fasta (+manifest), raw hmmscan/provenance/rcsb caches, anti-panel panel + retrieval hashes
- `report/report.md` - full report; `report/literature_ledger.md` - live PubMed ledger; `paper/paper.md` - manuscript draft; `figures/` - verified figures

Reproduce gates: `python3 code/evaluate_gates_r2.py` (reads caches; no network needed for evaluation).
