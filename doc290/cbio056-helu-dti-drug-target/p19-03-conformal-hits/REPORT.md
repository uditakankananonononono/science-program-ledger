# P19-03 Build Report: Trustworthy Hits (conformal DTI classification on DAVIS)

**Parent:** CBIO056 HeLU-DTI | **Spec:** doc290/cbio056-helu-dti-drug-target/03-conformal-hit-prioritization.md
**Built:** 2026-09-24 (lane D) | **Status:** BOUNDARY RESULT. G1 PASS; G2 FAIL (errors are mostly NOT flagged
as low-confidence); G3 NOT EVALUABLE (no prospective ChEMBL release). Protocol locked in `PROTOCOL_LOCK.md`
(18f0f602) before any model was trained.

## What was built
`tool/conformal.py` does split-conformal and Mondrian (class-conditional) classification at alpha = 0.10 on
DAVIS (30,056 pairs, label pKd >= 7, 8.6% positive). The model is the P19-02 classical HeLU surrogate: protein
composition/3-mer features + Morgan fingerprints, gradient-boosted classifier. There are random, cold-drug and
cold-target splits, each with a calibration set drawn the same way as its test set. A similarity-weighted
conformal pivot is included but only runs if cold coverage drops below 0.85.
Run: `python3 tool/conformal.py results/results.json` (~25 s; DAVIS files from the DeepDTA release in /tmp/davis).

## Results vs locked gates (split-conformal, alpha = 0.10)
| split | coverage | mean set size | low-confidence share | point error rate | errors flagged low-conf |
|-------|----------|---------------|----------------------|------------------|-------------------------|
| random | 0.896 | 0.94 | 6.4% | 6.5% | 37% |
| cold-drug | 0.897 | 0.96 | 4.1% | 7.8% | 20% |
| cold-target | 0.896 | 0.94 | 5.6% | 7.0% | 32% |
Mondrian coverage: 0.906 / 0.864 / 0.886; it flags 23% / 42% / 28% of errors, with much larger sets
(1.19-1.51).

| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1 | random-split coverage 0.90 +/- 0.02 | 0.896 | **PASS** |
| G2 | cold coverage loss reported; >= 70% of errors in low-confidence sets on both cold splits | coverage loss 0.3-0.4 points (none); errors flagged 20% (cold-drug), 32% (cold-target) | **FAIL** |
| G3 | prospective top-100 hit rate >= 2x raw score | no post-cutoff ChEMBL release available | **NOT EVALUABLE** |
The weighted-conformal pivot was not triggered (cold coverage >= 0.85).

## What this means
1. **Coverage holds, even cold**, when the calibration set is drawn the same way as the test split. Exchangeability
   holds by construction, so the spec's feared cold-split breakdown does not appear. The practical lesson:
   calibrate on held-out drugs/targets when you will predict on new drugs/targets.
2. **Conformal sets at alpha = 0.10 cannot flag most errors on this data, and that is arithmetic, not a model
   flaw.** The point error rate (6.5-7.8%) is below alpha, so the guarantee is met while the model stays wrong
   inside confident singleton sets. Many sets are even empty (mean size < 1). To use sets as an error flag,
   alpha has to sit below the model's error rate. The 70% target in the spec cannot be reached at alpha = 0.10 here.
3. Mondrian (class-conditional) coverage protects the rare positive class but costs larger sets, and still
   flags at most 42% of errors.

## Honesty notes
- DAVIS only. Classical-feature surrogate, no LM embeddings or knowledge graph (as in P19-02).
- Reproducibility fix: the 3-mer hash here is crc32. **P19-02 used Python's built-in hash(), which is salted per
  process (PYTHONHASHSEED), so P19-02's protein features and kinase families can differ between runs.** Its
  reported numbers came from one realisation. Flagged for the ledger, not changed here.
- Needs next: a post-cutoff ChEMBL kinase set for G3; an alpha sweep (pre-locked) to find where flagged-error
  share reaches 70%.
