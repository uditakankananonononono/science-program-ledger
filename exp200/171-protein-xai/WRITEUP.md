# DOC-2-071 Explainable protein AI vs known catalytic residues (exp200/171)

**Outcome: PASS on Pivot 1. The primary failed and is kept. Counted.**

## Primary (failed)
- Setup: a 1D CNN trained to predict enzyme class (EC 1-6) from sequence, with 5,014 training proteins and whole families held out. Integrated-gradients attributions were compared with UniProt active sites.
- Result: test macro-F1 was 0.27 (gate 0.50), so the model was too weak.
- Its attributions still preferred catalytic residues over same-type residues (AUROC 0.61, p=1e-37). Localization missed its gate by 0.001 (0.699 vs 0.70).

## Pivot 1: protein language model + trained catalytic-residue head (passed)
- Model: frozen ESM-2 (8M) embeddings with a small per-residue MLP. It was trained on 3,000 UniProt enzymes. Every M-CSA protein and every protein in an M-CSA family was removed from training.
- External validation, frozen: M-CSA, the literature-curated Mechanism and Catalytic Site Atlas (Ribeiro et al., NAR 2018). This covers 932 proteins and 4,564 catalytic residues.

| method | pooled AUPRC |
|---|---|
| **this model** | **0.205** |
| Bartlett et al. 2002 residue propensity | 0.045 |
| ESM-2 zero-shot wt-marginal (Meier et al. 2021) | 0.036 |

- Gain over the best named baseline: +0.16 (bootstrap 95% CI 0.15-0.18).
- Median per-protein AUROC: 0.90.
- Beyond residue identity: the model ranks true catalytic His/Asp/Ser/etc. above non-catalytic residues of the same types (mean AUROC 0.78, p=2e-144).

## Mechanism check
- Residues that directly do chemistry (M-CSA "reactant": nucleophiles, proton donors/acceptors) are found in the per-protein top 5 twice as often as residues that only stabilize (0.41 vs 0.20). This matched the hypothesis locked before scoring. The model is picking up chemical function, not just site proximity.
- The zero-shot baseline is weak. That fits Meier et al., where masked-marginal signal tracks fitness and conservation, not catalytic role specifically.

## Tool and prospective nomination
- `code/predict.py SEQUENCE` returns ranked candidate catalytic residues.
- Nomination: in human ABHD4 (Q8TB40, a lyso-NAPE lipase in endocannabinoid-precursor metabolism), UniProt has no active-site annotation. The model's top picks are S146 (inside the GHSLG motif, the classic alpha/beta-hydrolase GXSXG nucleophile), H320 and D170, a complete Ser-His-Asp triad. Proposed test: S146A, H320A and D170A mutants in an N-acyl-lysoPE hydrolysis assay; the prediction is loss of activity. A quick literature search found no mutant study; this is not an exhaustive search.

## Limits
- The nomination follows from homology, so it is plausible rather than surprising.
- Many UniProt ACT_SITE labels are inferred by similarity; family exclusion reduces overlap with M-CSA but does not remove it.
- Small 8M model, CPU only.
- The label-shuffled control for the primary was still running when this was written.

## Reproduce
code/train.py (primary), code/pivot1.py, code/nominate.py. Data: UniProt REST and M-CSA API, checksums in data/SHA256SUMS.
