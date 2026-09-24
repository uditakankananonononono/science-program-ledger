# P13-09 CART-Triage - locked protocol (summary-level pivot)

Locked 2026-09-24 11:42 IST, before any effect size was extracted or pooled.

## Data availability finding (drives the design)
A bounded search for open patient-level CAR-T cohorts with pre-infusion routine labs and response found none.
Searched: web; AACR figshare supplements for two multicenter LBCL cohorts (Bachy-style axi-cel vs tisa-cel,
n=427, and the immune-reconstitution cohort, n=263); CAR-HEMATOTOX papers; EGA (controlled access only).
All open supplements are aggregate: univariable ORs/HRs and baseline tables. Patient-level MIMIC-IV
pretraining isn't possible without credentialed access. The labs-only ML model therefore can't be trained on
real patients. Simulating patients would amount to fabrication, so this build doesn't do it.

## Pivot, per the spec's failure rule plus a summary-level information ceiling
1. Evidence table: every open-access cohort (>=3 targeted) reporting pre-infusion routine labs (CRP, ferritin, LDH,
   albumin, ALC/platelets/Hb, CAR-HEMATOTOX) against response (ORR/CR) with an OR or AUC plus CI. Each entry is
   extracted verbatim with its source URL.
2. Implied discrimination: convert each OR (per stated contrast) to an implied single-marker AUC under a binormal
   equal-variance model (d = ln(OR) / (contrast in SD units); AUC = Phi(d/sqrt2)), or use the reported AUC directly.
   Pool per marker (random-effects on logit-AUC) with per-cohort CIs.
3. Labs-only ceiling: an upper bound for a combined labs model, using the best single-marker AUC plus a
   correlation-aware combination bound, reported with its assumptions. Compared against published inflammatory-protein /
   cytokine panels where they exist (the feature-cost step).
4. Reporting-standard proposal: a minimal common dataset, audited cohort-by-cohort for which fields each published
   cohort would have needed to answer the triage question.

## Gates (spec gates, applied at summary level)
- G1: implied labs-only cross-cohort AUC >= 0.70, OR the certified finding that routine labs can't triage (measured ceiling).
- G2: the labs combination beats CAR-HEMATOTOX by >= 0.03 implied AUC, or matches it.
- G3: an expensive-profiling gain >= 0.05 AUC over labs-only where paired data exist, or the finding that it doesn't.
- G4: per-cohort CIs, no pooled-only claims.
Each gate is marked "summary-level" and states which evidence rows support it. No patient-level claim is made.
