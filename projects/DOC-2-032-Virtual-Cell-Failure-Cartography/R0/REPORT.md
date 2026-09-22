# DOC-2-032 - Virtual Cell Failure Cartography
## R0 feasibility report

**Verdict: LOCKED NEGATIVE (data feasibility failure).** The scientific question remains promising, but this R0 source/sample cannot support the locked test because it contains only 6 control cells versus the predeclared minimum of 200. The protocol therefore stops at F0. I did not relax the gate, swap datasets after seeing the outcome, or promote downstream diagnostics to evidence.

## Why the question matters
Virtual-cell benchmarks can look reassuring when dominated by genes whose absolute expression is easy to reconstruct, even while missing the perturbation-induced change that a biologist needs. DOC-2-032 asks for a failure taxonomy: which perturbations create metric mirages, transparent collapses, or directional failures? The estimand is the prevalence of the metric-mirage regime, not another average leaderboard score. If validated across models and cohorts, this could support model cards that state where a virtual cell fails, not merely its mean performance.

## Locked estimand
For each eligible perturbation, compare a predicted perturbation pseudobulk with observed pseudobulk on control-selected genes. The primary estimand is the proportion satisfying both:

- absolute-expression Pearson correlation `r_abs >= 0.90`, and
- top-50 perturbation-response sign accuracy `<= 0.55`.

This is the locked **metric-mirage** regime. Cell-level half-splits test whether the label reproduces.

## Exact gates
- **F0:** at least 8 eligible non-control perturbations (each >=50 cells), at least 200 control cells, and at least 1,000 eligible genes.
- **S1:** metric-mirage prevalence >=25% in each half-split, and pooled Wilson 95% lower bound >10%.
- **S2:** taxonomy-label agreement across half-splits >=80%, and median absolute split difference in `r_abs` <=0.03.
- **S3:** at least 2 taxonomy classes occupied in either split.
- **Overall:** F0 + S1 + S2 + S3.

## Feasibility result
Downloaded the open scPerturb-harmonized Adamson et al. 2016 `GSM2406675_10X001` H5AD from Zenodo record 7041849.

- 5,768 cells
- 35,635 genes
- 8 non-control perturbations with >=50 cells
- 2,000 analysis genes available under the locked filter
- **6 control cells**

Thus: perturbation-count arm PASS; gene-count arm PASS; control-count arm **FAIL**; F0 **FAIL**; overall **FAIL**. Success gates S1-S3 are not formally tested because the stop rule fired.

The included script also emits downstream diagnostic rows for auditability. They must not be interpreted as pilot evidence: splitting six controls leaves only three controls per half, so correlations and labels are unstable by design. Those rows show 0/16 metric mirages and one occupied class, but they are explicitly post-stop diagnostics, not a rescue analysis.

## Grant-defensible next step
Run a new, separately locked R1 on an open source with a verified control population before outcome access, preferably the larger Adamson `GSM2406677_10X005` sample or Norman 2019. First perform metadata-only reconnaissance to verify controls and condition counts; then freeze the same estimand and gates or justify changes without viewing expression outcomes. A strong grant package would then add:

1. model diversity: no-response, linear/additive, and a modern virtual-cell model;
2. external replication in a second perturbation modality or cell context;
3. a preregistered decision rule for when conventional metrics materially overstate response fidelity;
4. pathway-level enrichment of failure classes, treated as follow-up rather than used to redefine classes.

This R0 is useful precisely because it caught a source/sample mismatch before a low-control analysis could be oversold.

## Reproducibility
- Data SHA-256: `119e3c1cf7dede4e13f887b86f9bcd797a9dc29213ee57d36aa80012d93f1c1c`
- Random seed: `32032`
- Protocol lock recorded in `LOCKED_PROTOCOL.md`
- Code: `run_r0.py`
- Machine-readable result: `pilot_summary.json`
- Diagnostic table: `pilot_metrics.csv`

## Sources
- scPerturb resource: https://www.sanderlab.org/scPerturb/
- Zenodo record and file: https://zenodo.org/records/7041849
- Adamson et al. 2016: https://doi.org/10.1016/j.cell.2016.11.048
- scPerturb paper: https://doi.org/10.1038/s41592-023-02144-y
