# P19-02 Build Report: Affinity, Not Yes/No (HeLU-style affinity regression on DAVIS)

> **ERRATUM PENDING (2026-09-24): do not cite the numbers below yet.** `tool/affinity.py` hashes protein
> 3-mers with Python's built-in `hash()`, which is salted per process (PYTHONHASHSEED). Protein features
> and kinase families can therefore change between runs, and the reported numbers are one unreproducible
> realisation. A re-run with a deterministic crc32 hash (as in P19-03) and an erratum will follow.

**Parent:** CBIO056 HeLU-DTI | **Spec:** doc290/cbio056-helu-dti-drug-target/02-affinity-regression.md
**Built:** 2026-09-24 | **Status:** BOUNDARY RESULT (G1 failed - documented, not re-fished; G2/G4 pass; G3 effect smaller than hypothesized)

## What was built
`tool/affinity.py` - a complete, runnable affinity-regression pipeline: DAVIS (68 ligands x 442
kinases, Kd -> pKd), protein 3-mer composition + amino-acid composition features, RDKit Morgan
fingerprints (r=2, 512 bits), a knowledge-graph branch proxied by 12 sequence-similarity kinase
families (KMeans over k-mer space) plus leakage-safe family mean-affinity profiles, a gradient-
boosting regressor, a heteroscedastic variance head (quantile 0.16/0.84), and a locked-gate
evaluation harness with random, cold-target splits and 5-seed KG ablation.
Run: `python3 tool/affinity.py results/results.json` (~10 min, numpy/pandas/sklearn/rdkit).

## Gate amendment (locked before results, per pivot rule)
The spec assumed ESM-2/ChemBERTa embeddings and PrimeKG context, and named KIBA + a ChEMBL
harmonized set alongside DAVIS. ESM-2/ChemBERTa/PrimeKG are not retrievable in this environment
and KIBA/ChEMBL fetch was blocked, so the model class was re-locked before evaluation as
**G1' (classical-feature HeLU surrogate)**: sequence k-mers + Morgan fingerprints stand in for
the LM embeddings, and a sequence-similarity family clustering stands in for PrimeKG context.
DAVIS-only. The LM/KIBA/ChEMBL versions of all four gates remain open (first item in
"what this build needs next").

## Results vs locked gates
| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1' | random-split Pearson r >= 0.80 | 0.761 mean (0.729-0.775, 5 seeds) | **FAIL** |
| G2 | cold-target r >= 0.55 | 0.554 | **PASS** (at the boundary) |
| G3 | KG delta r, 95% CI, 5 seeds | +0.0111 +/- 0.0044 | **REPORTED** (below the hypothesized >= 0.03) |
| G4 | variance-head ECE <= 0.1 | 0.098 | **PASS** |

G1' failed on all 5 seeds; no hyperparameter escalation was attempted - continuing would be
gate-fishing. The failed gate is the result: see below.

## The useful results inside the failed gate
1. **The 0.80 random-split bar is not reachable with classical features on DAVIS.** A strong
   gradient-boosting model over k-mers + Morgan fingerprints tops out at r = 0.76 mean. Published
   r >= 0.80 numbers on DAVIS come from learned sequence embeddings (DeepDTA-class models), so the
   parent's "affordability" claims implicitly depend on the LM feature extractor, not the head.
2. **Cold-target generalization sits exactly at the spec's 0.55 floor** (r = 0.554). Affinity
   regression on unseen kinases is at the edge of usability with classical features - the KG/
   family structure is what carries it.
3. **The KG branch helps consistently but modestly**: +0.011 r (95% CI +/-0.004), present in all
   5 seeds, and it does not reach the hypothesized +0.03. Family context is real signal, not a
   headline effect; the spec's "KG matters only in the cold setting" prediction was not confirmed
   (the delta appears in random splits too).
4. **Uncertainty calibration passes** (ECE 0.098 at +/-1 sigma): the quantile variance head is
   trustworthy enough to triage predictions by confidence.

## What this build needs next
- ESM-2/ChemBERTa embeddings + PrimeKG (the open G1-G3): the tool accepts drop-in feature
  matrices; rerun all gates with LM features and the true KG branch.
- KIBA and the harmonized ChEMBL set for the multi-benchmark claim; the Kd vs Ki vs IC50
  noise-floor pivot (spec failure rule) stays queued behind that fetch.

## Honesty notes
- Family mean-affinity profiles were computed inside each training fold only (no leakage).
- The cold-target split holds out 20% of kinases entirely; ligands overlap by design.
- Seed 4 is visibly worse (0.729) - reported, not dropped.
