# DOC-2-019: RNA Model Hallucination Detector
## Locked R0 feasibility protocol

**Lock status:** Locked before outcome inspection on 22 September 2026, IST. The lock was written to `/tmp/deep-research/doc-2-019/plan.md` before the Rfam file was parsed or the classifier run. **Outcome rule:** if any required gate fails, R0 is negative and no post-hoc model tuning, relabeling, alternative split, or threshold relaxation is allowed in this experiment.

## Scientific claim being tested
RNA generation systems can produce strings that look locally plausible while violating higher-order constraints. R0 asks a deliberately narrow, falsifiable question: can a family-disjoint, sequence-only detector distinguish curated ncRNA sequences from a prespecified low-order synthetic null that preserves length and local transition statistics? Passing would justify a later, preregistered benchmark against outputs from named RNA models. It would not establish that the detector recognizes "hallucinations" from any deployed model.

The grant-defensible novelty is the evaluation design rather than a claimed universal detector: family-disjoint testing, an explicit generative null, a nuisance-only control, macro averaging across RNA families, paired length strata, and frozen go/no-go gates. This turns an often rhetorical notion of biological hallucination into a measurable model-audit target.

## Estimand
Let an eligible Rfam family be sampled uniformly from held-out families; within that family let one authentic seed sequence and its matched first-order Markov surrogate be sampled. The primary estimand is the **mean family-specific AUROC** of a frozen sequence-complexity classifier for ranking the authentic sequence above the surrogate. Families, not individual sequences, are the unit of external generalization and bootstrap resampling.

## Data source and eligibility
- Source: `Rfam.seed.gz` from the Rfam CURRENT FTP release, downloaded from https://ftp.ebi.ac.uk/pub/databases/Rfam/CURRENT/Rfam.seed.gz.
- Rfam describes seed alignments as manually curated and distributes the resource under CC0.
- Canonicalize T to U and remove gaps/non-ACGU symbols.
- Eligible cleaned sequence length: 40-500 nt.
- Deduplicate exact sequences within family.
- Eligible family: at least five sequences after cleaning.
- Deterministic cap: eight sequences per family, chosen by SHA-256 ordering, to limit domination by large families.

## Locked synthetic null
For every authentic sequence, estimate its 4 x 4 first-order nucleotide transition matrix with add-0.5 smoothing and its smoothed initial nucleotide distribution. Sample one surrogate of identical length using a deterministic per-family/per-sequence seed. Thus the null retains length, approximate base composition, and dinucleotide transition tendencies but removes longer-range organization. Class labels are authentic = 1, surrogate = 0.

## Split and leakage control
Assign entire Rfam families by SHA-256 hash to 60% training, 20% validation, and 20% test partitions. No family can appear in more than one split. The validation partition is reserved and unused in R0. All reported outcomes are from the single frozen test partition.

## Frozen detector
Features are normalized counts of all 2-, 3-, and 4-mers (336 variables), normalized mononucleotide entropy, longest homopolymer fraction, and fraction of runs of length at least four. Fit L2-regularized logistic regression (`L2 = 1`) on training rows only. Standardization parameters are learned on training rows only. Optimization uses L-BFGS-B.

**Nuisance control:** the identical classifier family using only log sequence length and GC fraction. Because surrogates are length-matched, this tests whether trivial dataset imbalance explains discrimination.

## Locked success gates - all required
1. **Data sufficiency:** at least 100 eligible families and 1,000 authentic sequences.
2. **Primary discrimination:** test family-macro AUROC >= 0.75.
3. **Precision:** lower bound of a 2,000-resample family bootstrap 95% interval >= 0.70.
4. **Nuisance falsification:** family-macro AUROC of the length+GC control <= 0.60.
5. **Length robustness:** family-macro AUROC >= 0.70 in both strata split at the test-set median authentic length.

No single gate can compensate for another. A failure stops this R0 line as specified. Any revised feature set, generator, threshold, family eligibility rule, or model-output dataset is a new protocol and must be locked before outcomes are read.

## Reproducibility
Run:

```bash
python3 run_r0.py --seed Rfam.seed.gz --out results.json --bootstrap 2000
```

The program records the input SHA-256, sample sizes, test statistics, confidence interval, stratum results, and gate decisions. Dependencies: Python 3, NumPy, SciPy.

## Interpretation limits
This R0 uses a transparent synthetic corruption, not outputs from a named RNA foundation model. Rfam sequences are curated positives rather than a representative sample of all genomic RNA. Sequence-only signals do not prove structure, expression, or function. A positive R0 would only license the next study; a negative R0 is evidence that this frozen detector is not sufficiently discriminative even under the specified null.

## Sources
- Rfam Help and CC0 license: https://docs.rfam.org/en/latest/index.html
- Rfam FTP documentation: https://docs.rfam.org/en/latest/ftp-help.html
- Rfam CURRENT release README: https://ftp.ebi.ac.uk/pub/databases/Rfam/CURRENT/README
- Rfam CURRENT directory: https://ftp.ebi.ac.uk/pub/databases/Rfam/CURRENT/
