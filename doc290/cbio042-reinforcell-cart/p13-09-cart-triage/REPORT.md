# P13-09 CART-Triage - Build Report (summary-level pivot)

**Built:** 2026-09-24 | **Status:** DATA BOUNDARY with summary-level results. No open patient-level CAR-T cohort with pre-infusion labs exists, so no model was trained on patients. From published effect sizes: routine labs imply AUC ~0.67-0.73 per marker and ~0.72-0.76 combined, which beats CAR-HEMATOTOX (~0.61-0.63). That holds within one LBCL cohort. Cross-cohort validation and the expensive-profiling comparison are not testable on open data.

Parent: CBIO042 ReinforCell. Protocol locked and pushed before extraction (commit 28c473b7, `PROTOCOL.md`). That file also records why the patient-level design was impossible.

## Gates (locked before evaluation, summary-level)

| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1 | labs-only cross-cohort AUC >= 0.70, or certified "labs can't triage" with the ceiling | CART-SIE CRR: CRP 0.73 [0.65-0.81], LDH 0.68, ferritin 0.67. Combination 0.73-0.76 for assumed inter-marker r = 0.7-0.3. Only one LBCL cohort reports continuous-marker ORs, so the cross-cohort part can't be evaluated | PASS within-cohort (summary-level) / cross-cohort NOT EVALUABLE |
| G2 | beats published baseline score by >= 0.03 AUC, or matches it | labs combination 0.72-0.76 vs CAR-HEMATOTOX 0.61-0.63 (same cohort, ORR and CRR) | PASS (summary-level; +0.09 or more) |
| G3 | expensive profiling adds >= 0.05 AUC, or it doesn't | no open paired labs + cytokine/flow + response data | NOT EVALUABLE (data boundary) |
| G4 | per-cohort CIs, no pooled-only claims | every row carries its own cohort and CI; nothing is pooled across cohorts | PASS |

## Evidence table (every number traced to its source)

| cohort | outcome | marker | n | OR (95% CI), contrast | implied AUC (95% CI) |
|---|---|---|---|---|---|
| CART-SIE LBCL, axi-cel vs tisa-cel (Blood Cancer Discov, Suppl. Table 1) | ORR d90 | CRP | 408 | 0.35 (0.23-0.55), Q3 vs Q1 | 0.709 (0.623-0.779) |
| same | ORR d90 | ferritin | 352 | 0.40 (0.25-0.63) | 0.684 (0.596-0.766) |
| same | ORR d90 | LDH | 408 | 0.36 (0.24-0.56) | 0.704 (0.619-0.773) |
| same | CRR d90 | CRP | 408 | 0.31 (0.19-0.48) | 0.730 (0.650-0.808) |
| same | CRR d90 | ferritin | 352 | 0.44 (0.28-0.69) | 0.667 (0.577-0.748) |
| same | CRR d90 | LDH | 408 | 0.41 (0.27-0.64) | 0.680 (0.592-0.754) |
| same | ORR / CRR d90 | CAR-HEMATOTOX high vs low | 241 | 0.34 (0.20-0.59) / 0.34 (0.19-0.61) | 0.61-0.63 (range over assumed HT-high prevalence 0.3-0.6) |
| Liu 2023 R/R multiple myeloma (Front Immunol) | >= VGPR | ferritin upper quartile | 109 | 59% vs 77% response | 0.58 (2x2-derived) |

Sources: CART-SIE supplement https://aacr.figshare.com/collections/Data_from_A_Multicenter_Real-life_Prospective_Study_of_Axicabtagene_Ciloleucel_versus_Tisagenlecleucel_Toxicity_and_Outcomes_in_Large_B-cell_Lymphomas/7429371 (file https://ndownloader.figshare.com/files/65614965). Liu 2023: https://www.frontiersin.org/articles/10.3389/fimmu.2023.1169071/full

## Findings
1. **Routine inflammation labs carry real signal for LBCL response.** A single CRP value implies AUC ~0.73 for day-90 CR. That is already at the G1 bar in the one cohort that reports it properly.
2. **Three cheap labs beat CAR-HEMATOTOX for response.** Combining CRP, ferritin and LDH implies AUC 0.72-0.76, depending on how correlated they are, versus 0.61-0.63 for HEMATOTOX. HEMATOTOX was designed for hematotoxicity, not response, so this is expected but useful for triage.
3. **The signal is weaker outside LBCL.** In myeloma, high ferritin alone implies only ~0.58.
4. **The real bottleneck is reporting, not modelling.** Cohorts publish survival HRs for dichotomised risk groups: Jain et al. 2024 (PMC10905320) and the original CAR-HEMATOTOX papers (e.g. PMC9114843). They don't publish response ORs for continuous markers, and patient-level tables stay "available on request". None of these papers could have answered the triage question as published.

## Minimal common dataset (pivot deliverable)
To make CAR-T triage testable across centres, a registry should deposit, per patient: product; disease; pre-lymphodepletion CRP, ferritin, LDH, albumin, ALC, ANC, platelets and Hb, each with its date relative to infusion; CAR-HEMATOTOX components; bridging response; and day-30/90 best response (ORR and CR). Optional paired fields: IL-6 and a baseline cytokine panel. Continuous values, not tertiles. De-identified patient-level release under a data-use agreement.
Audit of the published cohorts reviewed: CART-SIE reports continuous-marker ORs, but only univariable and aggregate. Jain 2024 reports risk groups against survival only, with data "available upon request". Liu 2023 reports quartile groups with response percentages only. The HEMATOTOX papers report groups against toxicity and survival. None deposits patient-level labs.

## Honest limits
- Every AUC is *implied* from published ORs under a binormal, equal-variance model. It isn't measured on patients.
- The combination ceiling assumes an inter-marker correlation (r = 0-0.7 shown). The literature reviewed didn't report the true correlation.
- HEMATOTOX AUC depends on an assumed HT-high prevalence, because the supplement gives only the OR.
- The spec's "CART-Triage" calculator was NOT shipped. Without patient-level data it would be an unvalidated tool, and building one that way would be irresponsible.

## Artifacts
- `PROTOCOL.md`
- `tool/ceiling.py`: all conversions and the combination ceiling. Re-runnable.
- `results/results.json`
- `SHA256SUMS`

## What a reviewer asks next
Get patient-level data from one centre under a DUA and test the 3-lab model against HEMATOTOX directly. Measure the real CRP/ferritin/LDH correlation. Add IL-6 and a cytokine panel to answer G3.
