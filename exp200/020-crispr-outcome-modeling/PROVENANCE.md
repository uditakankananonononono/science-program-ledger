# DOC-1-020 PROVENANCE
- Data: SupplementaryData.xlsx from github.com/maxwshen/indelphi-dataprocessinganalysis (652,001 bytes, downloaded 2026-09-24), the published supplement of Shen et al., Nature 2018;563:646-651 (inDelphi). Dev = Supplementary Table 2 (LibA, 2000 guides, 55nt context, mESC unique-indel counts); frozen = U2OS labels of LibA (same table) and Supplementary Table 3 (designed repeat library, 2000 guides, mESC). MD5 of downloaded file recorded in results/local/ (gitignored with parsed npz caches; parse_liba.py regenerates).
- Abandoned source (Addendum B documents why): L1-Lindel mirror txt files were model-input feature vectors, not outcome labels.
- Named baseline: Bae et al. 2014, Nat Methods 11:705-712 microhomology score, computed from full 55nt context.
- Evo 2 feasibility: huggingface.co/arcinstitute/evo2_1b_base (1B smallest checkpoint) - fine-tuning infeasible on 2 CPU/1.9GB; Addendum E1 head-to-head parked.
- No money spent; all sources free public.
