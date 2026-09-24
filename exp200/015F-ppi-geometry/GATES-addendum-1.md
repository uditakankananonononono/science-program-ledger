# ADDENDUM 1 (locked 2026-09-24 12:39 IST, before any gate scoring)

Coverage/alignment rule for per-residue geometry (gap discovered during mapping; locked
before outcomes):
- Mapping result: 360/418 survivor proteins (86.0%) mapped at the locked rule
  (identity>=0.95, evalue<=1e-20, first result_set entity). Per-set: dset72 65/71,
  dset164 133/164, dset186 162/183. The 58 zero-hit proteins are dropped-and-disclosed per
  GATES (NOT a short-sequence artifact: median len 169 vs 164 mapped); drops apply to BOTH
  arms same-set. No AlphaFold/homolog fallback: zero-hit means no >=95% experimental chain.
- Residue alignment: Dset sequence (<=512) aligned to the chain's entity sequence
  (pdbx_seq_one_letter_code from the mmCIF) by exact-k-mer-anchored local alignment (k=8
  anchor seeds, banded fill; deterministic, code in tools/). Only residues aligned to a
  RESOLVED CA atom receive computed geometry values; all other residues receive 0.0 in all
  4 geometry channels (disclosed; same zeros in every arm so no arm advantage).
- Coverage guard: a mapped protein with <50% of its (truncated) residues aligned to resolved
  CA atoms is dropped-and-disclosed (both arms same-set), counts reported in REPORT before
  gate verdicts.
