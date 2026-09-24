# DOC-1-022: A Unified Cell Embedding for Cross-Tissue Integration
Status: ALL LOCKED GATES PASSED - reported to main for adjudication (never self-counted). 2026-09-24.

## Question
Can one lightweight, batch-blind embedding (a single small autoencoder trained once across tissues)
integrate cells across tissues at named-baseline level for cell-type label transfer - without per-dataset
iterative correction (Harmony) or foundation-scale pretraining?

## Data (public, hashed in PROVENANCE.md)
Tabula Muris FACS (Smart-seq2, Schaum et al 2018 Nature 562:367), figshare 5715040, members range-extracted.
DEV tissues Marrow/Lung/Heart (fit everything), FROZEN Spleen (single final run). 23,433 shared genes,
top-2000 HVG on dev only, log1p(CPM1e4), dev-fitted standardization, PCA-50.
6 shared classes (>=30 cells in >=2 tissues, then >=30 in the split's training pool - Addendum A):
B cell, T cell, endothelial cell, leukocyte, monocyte, natural killer cell.

## Protocol
Cross-tissue kNN (k=5, cosine) leave-one-tissue-out label transfer; mean accuracy across held-out tissues.

## Results
| Gate | Check | Result | Verdict |
|---|---|---|---|
| G1 | Harmony (Korsunsky 2019 Nat Methods, scIB top tier) dev mean | 0.817 (Marrow 0.798 / Lung 0.941 / Heart 0.712); PCA-only context 0.834 | recorded (sanity >0.30) |
| G2 | Unified AE (2000-512-128-512-2000, batch-blind, 15 ep) dev mean | 0.844 >= 0.817-0.03 | PASS (also beats Harmony outright, +0.027) |
| G3 | FROZEN Spleen: AE 0.909 vs dev-0.05=0.794 AND vs Harmony frozen 0.892-0.03 | both | PASS (beats Harmony frozen outright too) |
| G4 | Mechanism (below) | | done |
| G5 | embed_cells.py CLI smoke (300 Spleen cells) | acc 0.901 on 292 shared-class cells, shapes OK | PASS |

Winner stability: frozen 0.909 > dev 0.844 (transfer to Spleen is easier: its B/T cells have strong
Marrow support). Note the asymmetry we disclose: Harmony's frozen number comes from an unsupervised
refit that includes the frozen cells (scIB practice); the AE embeds Spleen as a pure out-of-sample
transform and still wins.

## G4 mechanism (results/g4_mechanism.json)
- Per-class transfer (AE, mean across held-out tissues): endothelial 0.987, B cell 0.963, monocyte 0.856,
  NK 0.853 - conserved identity programs transfer. T cell 0.604 and the hierarchical parent label
  "leukocyte" 0.481 (Heart 0.027) fail exactly where biology predicts: coarse labels spanning tissue-
  resident subtypes (Heart leukocytes = tissue-resident macrophages) do not map across tissues.
- Embedding geometry (subsample, cosine silhouette): cell-type 0.190 > tissue 0.119 - the unified
  embedding organizes by biology over tissue of origin.
- Marker loadings (encoder W1): Pecam1/Cd79a/Col1a1/Ptprc all in-HVG but low absolute weight
  (Ptprc bottom 2.5%) - a dense 512-wide first layer spreads signal; weight magnitude is not feature
  importance here. Recorded as an interpretation caveat, not a finding.

## Findings for the program summary
1. A 2-layer batch-blind autoencoder embedding, trained once, matches/beats Harmony at cross-tissue
   label transfer on same-platform atlas data - a positive counterpoint to the 021 generative boundary:
   small models win when the task is compression/alignment of an existing signal, lose when asked to
   generate signal a reference already carries (021) or to correct across library designs (020).
2. Harmony < uncorrected PCA on this cohort (0.817 vs 0.834): when batches ARE tissues, aggressive
   batch correction erases the tissue-private variation that helps distinguish coarse types.
3. Label granularity, not embedding quality, bounds cross-tissue transfer: the failure modes are the
   hierarchical/coarse labels (T cell 0.60, leukocyte 0.48), not the conserved programs.
4. Engineering: addendum-driven cohort eligibility repair (label-presence artifact caught by a
   Harmony-vs-PCA prediction-diff sanity check before any outcome was used); streaming HVG/standardization
   to stay in the 1.9GB envelope.

## Tool + nomination
embed_cells.py: counts CSV -> 128-d unified embedding + transferred labels (honest scope banner).
Smoke PASS. Prospective lab: Satija lab (NYGC) - integration/atlas transfer methods.

## Reproduce
code/prep_data.py (range-extract + prep; needs results/local/ caches, re-fetch per PROVENANCE.md),
code/score_baseline.py, code/score_ae.py, code/score_frozen.py, code/g4_mechanism.py, code/embed_cells.py.
GATES.md + GATES_ADDENDUM_A.md locked before outcomes; thresholds never relaxed.
