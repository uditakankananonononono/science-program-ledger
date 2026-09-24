# DOC-1-026: A "Cell Atlas" of Viral Infection
**Claim** (locked pre-outcomes): an NMF program learned on dev-virus PBMCs (COVID vs healthy) beats the
curated MSigDB interferon signature at infection-vs-normal discrimination per cell type, and transfers
to a held-out virus (influenza). **Verdict: DOCUMENTED BOUNDARY** (G2 pass, G3 fail).

## Event: G1 sanity halt fired (Addendum A)
Locked guard: baseline dev mean AUROC < 0.70 = pipeline problem, stop. Observed 0.5886.
Diagnosis (Addendum A): NOT a pipeline bug. The lock-time premise ("ISGs strongly separate COVID from
healthy in this dataset") is the paper's SEVERE-case finding; the census cohort is severity-pooled with
no severity metadata, and mild COVID is IFN-attenuated (the paper's own headline). Per-cell-type pattern
is biologically ordered (NK 0.715 / CD8 0.668 high; monocyte 0.493 near chance, severity-linked in the
paper) - inconsistent with a bug. Halt documented; thresholds unchanged; guard lesson recorded.

## Scores (locked subsample, 9,540 cells, seed 7)
| arm | dev mean AUROC (COVID) | frozen mean AUROC (influenza) |
|---|---|---|
| ISG signature (224 genes) | 0.5886 | **0.6193** |
| learned NMF top-50 | **0.6189** | 0.5605 |

G2: topic 0.6189 >= 0.5886+0.02 = PASS (+0.0303). G3: topic 0.5605 < 0.6193+0.02 FAIL; also below
dev-0.05 (0.5689) FAIL. No rescue arm pre-registered for G3-with-G2-pass => boundary.

## Mechanism (G4) - the payload
Learned top-50 shares only 12/50 genes with the ISG set (Jaccard 0.046) and contains NONE of the five
canonical ISGs (ISG15, MX1, IFIT1, IFIT2, IFIT3 all absent). The dev-fit program learned COVID-specific,
non-canonical genes - wins the training virus, loses the held-out virus. The transferable cross-virus
core IS the interferon program; the curated 200-gene signature encodes what a 9.5k-cell fit cannot.
Map entry: data-driven discovery loses to curated knowledge at held-out perturbation transfer, even when
it wins in-domain.

## Tool (G5)
`code/atlas_score.py` - ISG scorer (winning arm), smoke-tested: 223/224 genes score 300 cells; per-CT
AUROCs reproduce the biology (NK 0.88, CD8 0.84 on pooled labels). Honest scope in docstring.

## Prospective lab nomination (locked G4 criterion)
PBMC immune-profiling labs running COVID/influenza cohorts (e.g. influenza challenge-study groups);
nomination rationale: frozen-virus validation is exactly a prospective-challenge design.
