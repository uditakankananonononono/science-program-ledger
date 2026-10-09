# 197 RESULT - Replication R-02 (yeast isozyme over-rescue, mega27-05 @ 4b66f67)
Prereg: algo50/197-PREREG.md (committed ~03:30 IST before any code; text sha256 b44dd4b20bd38c31892655a8be7cf0ac20c1be6922ca90afa587327d8f25d314, trailing newline aside). Same-organisation re-execution plus independent reimplementation of the key variable; replication, not a novel method.

## Verdict by preregistered mapping: REPLICATED (A pass, B pass)
- A exact re-run: counts 19/75/1/64, OR 16.2133, p 3.7525e-4, identical to committed. PASS.
- B independent re-derivation (own cobra KO ratios, GPR-syntax-tree "backed" definition, cutoff 1e-6): missed 16/74 backed vs caught 0/85 backed, Fisher p 1.84e-6, OR infinite (zero cell), Woolf CI lower (Haldane corrected) 2.84. Criterion OR>=5, p<0.01, CI lower>1: PASS. Same backed definition with the repo's committed ratios: 16/94 vs 0/65, p 2.04e-4, Woolf lower 1.62 (also meets the criteria).
- C cutoff robustness (1e-6, 1e-4, 1e-2, 0.05): identical tables at all four cutoffs (16/58/0/85), p 1.84e-6. PASS.
- D confound logistic (backed + log n_rxns + max_complex): literal criterion (backed p<0.05) FAILS - but only because of complete separation (0 caught genes are backed): coefficient 23.9, Wald p 0.9994, uninformative. Post-hoc, NOT preregistered: Mantel-Haenszel stratified by n_rxns>1: strata 9/37/0/54 and 7/21/0/31, pooled OR 24.9 (0.5-corrected), CI [3.2, 192], p 1.9e-5. D does not change the verdict.

## Wording consequence
The effect replicates and survives an independent backed definition and every viability cutoff, but the size is NOT "OR 16.2" under independent re-derivation: the caught set contains zero backed genes, so the OR is unbounded and the honest statement is "isozyme-backed genes are enriched among FBA-missed essentials (16/74 vs 0/85 in my recompute; 19/94 vs 1/65 in the repo's), p < 1e-3". Quote the repo's OR 16.2 only as the repo's number.

## Caveats / audit lines (published as found)
- My own KO ratios disagree with the repo's committed ratios on 111 of 1143 genes' viability calls @1e-6 (my missed set 74 vs repo's 94). No script in the repo generates fba_single_ko.json, so its medium/settings could not be reconstructed; I used the SBML's default bounds. This is a provenance gap in the original claim. My missed/caught split agrees with the labels-file FP/TN split for 137 of 159 essentials (repo's committed split is the one matching the file).
- Backed definition differs: repo flat regex marks 463 genes backed, my syntax-tree definition 412 (51 disagree).
- Solver note: first attempts with cobra single_gene_deletion / presolve stalled (glpk warm-start); final run used per-KO context, solver timeout 8 s, zero non-optimal statuses and zero solver resets. Earlier killed attempts produced no scored output.
- Same data/labels as the original; labels inherit upstream FBA outcomes; only claim #2 covered.

## Verbatim output (B197.json / A197.json / posthoc197.txt)
```
{
 "n_essential": 159,
 "n_missed": 94,
 "n_caught": 65,
 "missed_isozyme_backed_frac": 0.20212765957446807,
 "caught_isozyme_backed_frac": 0.015384615384615385,
 "fisher_odds_ratio": 16.213333333333335,
 "fisher_p": 0.0003752524889093159,
 "overrescued_genes": [
  "YAL038W",
  "YBL030C",
  "YBR002C",
{
 "ratio_source": "mine",
 "B": {
  "cut": 1e-06,
  "table": [
   16,
   58,
   0,
   85
  ],
  "OR": Infinity,
  "p": 1.8407554648629098e-06,
  "woolf_lo": 2.8373415316157375,
  "n_missed": 74,
  "n_caught": 85
 },
 "B_with_committed_ratios": {
  "cut": 1e-06,
  "table": [
   16,
   78,
   0,
   65
  ],
  "OR": Infinity,
  "p": 0.00020407170895106778,
  "woolf_lo": 1.6207045185064928,
  "n_missed": 94,
  "n_caught": 65
 },
 "C": [
  {
   "cut": 1e-06,
   "table": [
    16,
    58,
    0,
    85
   ],
   "OR": Infinity,
   "p": 1.8407554648629098e-06,
   "woolf_lo": 2.8373415316157375,
   "n_missed": 74,
   "n_caught": 85
  },
  {
   "cut": 0.0001,
   "table": [
    16,
    58,
    0,
    85
   ],
   "OR": Infinity,
   "p": 1.8407554648629098e-06,
   "woolf_lo": 2.8373415316157375,
   "n_missed": 74,
   "n_caught": 85
  },
  {
   "cut": 0.01,
   "table": [
    16,
    58,
    0,
    85
   ],
   "OR": Infinity,
   "p": 1.8407554648629098e-06,
   "woolf_lo": 2.8373415316157375,
   "n_missed": 74,
   "n_caught": 85
  },
  {
   "cut": 0.05,
   "table": [
    16,
    58,
    0,
    85
   ],
   "OR": Infinity,
   "p": 1.8407554648629098e-06,
   "woolf_lo": 2.8373415316157375,
   "n_missed": 74,
   "n_caught": 85
  }
 ],
 "audit_split_agreement": {
  "n": 159,
  "agree": 137,
  "mine_missed": 74,
  "file_FP": 94
 },
 "audit_backed_definition": {
  "repo_backed_n": 463,
  "mine_backed_n": 412,
  "disagree": 51
 },
 "D": {
  "backed_OR": 24831606743.712006,
  "backed_p": 0.9993603634723439,
  "n": 159,
  "params": {
   "const": -1.5907772842942698,
   "backed": 23.93538314414785,
   "logn": 0.4569101246152016,
   "cx": 0.7024475106676692
  },
  "pvalues": {
   "const": 2.621646829582179e-05,
   "backed": 0.9993603634723439,
   "logn": 0.057597253527748506,
   "cx": 0.004573280479940965
  }
 }
}
stratum n_rxns>1 = 0 [9, 37, 0, 54]
stratum n_rxns>1 = 1 [7, 21, 0, 31]
MH OR (0.5 corrected) 24.854480526726924 CI (3.211012255431836, 192.38332124346556) test p 1.8625984799625073e-05
missed backed 16 of 74 ; caught backed 0 of 85
```
