# GATES - DOC-1-029 (locked 2026-09-24 08:20 IST, BEFORE any model fitting or scoring)

## Claim
The foundation-model PROTOCOL - self-supervised masked pretraining on RNA, then a linear probe -
predicts surface-protein abundance from RNA better than the published direct-supervised baseline,
on held-out cells AND zero-shot on an independent donor. Topic: "A Foundation Model for
Single-Cell Multi-Omics" - tested at envelope scale with the field's standard benchmark pair.

## Data (eligibility verified BEFORE this lock)
scvi-tools hosted totalVI benchmark h5ads (Gayoso et al 2021, Nat Methods 18:1209):
- DEV: pbmc_10k_protein_v3.h5ad (6,855 cells x 16,727 genes, raw integer counts verified,
  14 TotalSeqB proteins in obsm['protein_expression']).
- FROZEN (independent donor): pbmc_5k_protein_v3.h5ad (3,994 cells x 16,581 genes, 29 proteins).
Verified pre-lock: all 14 dev proteins present in the frozen panel; 15,792 shared genes;
protein counts raw (0-12,908). URLs in PROVENANCE.md; files hashed in results/data_manifest.json
before any scoring.

## Arms (all fit on DEV-train only; FROZEN is zero-shot application)
- BASELINE: multi-output ridge regression, HVG-2000 log1p RNA -> log1p protein. The documented
  simple baseline of the NeurIPS 2021 Multimodal Single-Cell Integration competition
  (Luecken et al 2022) and the totalVI benchmark supplements - named published baseline.
- FM (linear probe): masked denoising autoencoder (MLP 2000->256->256->2000, mask 25% of gene
  entries per draw, MSE reconstruction), pretrained on DEV-train RNA only; then ridge from the
  frozen 256-dim embedding -> 14 proteins. Encoder never sees protein or frozen-donor data.
- P1 (pre-registered rescue, runs only if G2 fails): end-to-end fine-tune of the pretrained
  encoder + probe head on DEV-train (standard alternative protocol), same data, same gates.

## Preprocessing (locked)
Genes = intersection(15,792) ordered by dev variance; HVG-2000 selected on DEV-train only.
RNA: log1p(counts/library*1e4). Protein: log1p(raw ADT). Identical transforms for both arms and
both donors. Dev split: 80/20 train/test, seed 17, stratified-free (cells iid).

## Metric
Per-protein Pearson r (predicted vs true log1p ADT on held-out cells), mean over the 14 proteins.

## Gates
- G1 (sanity halt): ridge DEV-test mean r >= 0.50. Else pipeline problem - document, stop.
  Premise: published per-protein correlations on this exact dataset (totalVI paper) are high for
  abundant markers; ridge should exceed 0.50 mean. If it fires, check preprocessing not the gates.
- G2 (dev): FM dev-test mean r >= ridge dev-test mean r + 0.02.
- G3 (frozen): FM frozen mean r >= ridge frozen mean r + 0.02 AND FM frozen >= FM dev - 0.10.
- Failure tree: G2 fail -> P1 (end-to-end fine-tune), same gates; P1 fail or G3 fail ->
  DOCUMENTED BOUNDARY (no further arms).
- G4 (mechanism, runs regardless): per-protein breakdown (which markers transfer, which do not);
  does the self-supervised embedding recover major PBMC structure unlabeled (marker-gene
  separation in embedding space); comparison to totalVI published values as literature context.
- G5: working CLI fm_embed.py (embed new RNA h5ad with the pretrained encoder) + lab nomination.

## Prospective lab nomination (locked)
A single-cell core running CITE-seq immune profiling (e.g. vaccine-response PBMC cohorts):
embed their RNA with the pretrained encoder for cross-modality QC and marker prediction.

## Scoring discipline
Manifest + hashes committed before ANY training. Thresholds never relax after seeing results;
errata in GATES_ADDENDUM files locked before the outcomes they govern.
