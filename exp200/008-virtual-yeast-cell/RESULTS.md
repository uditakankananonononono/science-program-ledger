# DOC-1-008 — A Virtual Yeast Cell for Metabolic Engineering: RESULTS

**Outcome: BOUNDARY on G1 (validation) — NOT submitted for counting. G2 gate passed literally but
degenerately; a supplementary growth-coupled analysis produced literature-validated engineering designs.**

## G1 — frozen external essentiality validation (SGD truth, 807-gene common set)

| arm | medium | Yeast8 BA | iMM904 BA (named baseline) | gate BA>=0.85 | beat baseline |
|---|---|---|---|---|---|
| G1 (locked) | minimal glucose (model default) | 0.747 (sens 0.629, spec 0.865; tp83 tn584 fp91 fn49) | 0.6177 | FAIL | YES (+0.129) |
| G1-rich (Addendum B, fresh gate locked before results) | YPD-matched rich | 0.6979 (sens 0.409, spec 0.987; tp54 tn666 fp9 fn78) | 0.6031 | FAIL | YES (+0.095) |

**Diagnosis.** The locked minimal-medium arm's dominant error was 91 false positives: amino-acid /
nucleotide biosynthesis genes are essential in minimal medium but the SGD/Giaever deletion viability
truth was measured on rich YPD, where those auxotrophs are viable. The parent-approved Addendum B arm
corrected the condition mismatch (rich medium, mechanical definition, same thresholds). Under rich
medium false positives collapsed (91 -> 9, specificity 0.987) but false negatives rose (49 -> 78):
imports rescue genes that are inviable on YPD in reality, so sensitivity fell to 0.409 and the
0.85 bar was not met in either arm.

**Boundary statement (per locked failure tree + Addendum B4):** the virtual cell does NOT validate at
the locked bar on frozen external essentiality in either medium. It DOES beat the named published
baseline iMM904 on the same frozen set in both arms. No thresholds were relaxed; no further arms.

## G2 — succinate engineering

- Locked gate: >=1 non-essential single KO with succinate export >= 5% of theoretical max at
  biomass >= 10% WT. Theoretical max = 1.294 mmol/gDW/h (exchange r_2056; no model edit needed).
- **Literal result: PASS but DEGENERATE** — all 949 non-essential KOs achieve exactly the theoretical
  max. With a 10% biomass floor and a succinate-maximizing objective, flux redirection is free; the
  gate cannot discriminate designs. Recorded as a gate-design lesson, not a win.
- **Supplementary growth-coupled analysis (post-hoc characterization, not a gate):** max succinate
  export at biomass >= 90% of each strain's own max growth. WT reference = 0.1438.

| rank | KO | gene (verified vs SGD) | gc90 succinate | growth | vs WT |
|---|---|---|---|---|---|
| 1 | YPL262W | FUM1 (fumarase) | 0.1648 | 97.8% WT | +14.6% |
| 2 | YKL141W | SDH3 | 0.1516 | 99.4% WT | +5.4% |
| 3 | YLL041C | SDH2 | 0.1516 | 99.4% WT | +5.4% |
| 4-5 | YNL241C / YJL121C | ZWF1 / RPE1 (pentose-phosphate, NADPH) | 0.1465 | ~99% WT | +1.9% |

Only 6 of 949 non-essential KOs beat WT.

**Mechanism check vs published literature: STRONG AGREEMENT.**
- FUM1 deletion: Arikawa et al. 1999 — SDH1+FUM1 double deletion gave 2.7-fold higher succinate
  (reviewed in FEMS Yeast Res 2017, doi:10.1093/femsyr/fox057).
- SDH3 deletion: Otero et al. PLoS ONE 2012 (doi:10.1371/journal.pone.0054144) — OptGene-identified
  SDH3 (primary succinate-consuming reaction) as the key target; their 8D strain (sdh3+ser3+ser33)
  reached a 43-fold succinate-yield improvement with evolution.
- SDH1/SDH2 disruption: Biosci Biotechnol Biochem 2014 (doi:10.1080/09168451.2014.877816) —
  aerobic succinate production in S. cerevisiae.
- Model-internal consistency: r_1021 (succinate dehydrogenase) GPR has three subunit-composition
  variants; SDH2 and SDH3 appear in ALL three (their KOs disable the complex and are exactly the two
  SDH hits), while SDH4/SDH1/SDH9 are each absent from at least one variant (their KOs show WT-level
  succinate, matching the scan). Gene identities verified against SGD phenotype_data.tab.
- Honest caveat: in vivo, sdh3 deletion ALONE did not increase succinate (Otero) — growth coupling
  required the ser3/ser33 combination plus evolution. The model recovers the published TARGETS as
  top-ranked; magnitudes are modest and directional, not titer predictions.

## Tool + wet-lab nomination

`yeast_cell.py` (smoke-tested: WT growth 0.0811 = locked reference; SDH3 KO 99.4% WT, non-essential;
FUM1 SUCC gc90 0.1648, 97.8% WT). Commands: WT | KO <genes...> | SUCC <genes...>.

**Nominated for wet-lab validation:** (1) FUM1Δ single knockout — top single-gene growth-coupled
design, minimal fitness cost; (2) SDH3Δ+SER3Δ+SER33Δ triple (Otero-validated architecture) as the
benchmark combination; both in S. cerevisiae CEN.PK background, aerobic glucose batch, succinate titer
by HPLC.

## Errata
- E1: naive GPR-blind prototype scan (275 genes) and its 02:31 metrics INVALIDATED and replaced by
  GPR-aware HiGHS pipeline (Addendum A; GLPK hung on specific KO LPs, first at YDR044W/HEM13;
  WT verified identical under both solvers).
- E2: rich-medium uptake-bound direction bug found by auxotroph-rescue diagnostic before any rich
  results were used; the affected 600-gene parts file was discarded and the arm fully rerun.
  Addendum B text was correct; the implementation was aligned to it.

## Data & reproducibility
See PROVENANCE.md (URLs + SHA-256 for all inputs, gates, code, and key result files).
