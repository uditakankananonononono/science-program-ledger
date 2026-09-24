# P01-10 data-condition check (2026-09-24, lane A)
- cMD sampleMetadata has a `fobt` field only for ZellerG_2014 (34 yes / 121 no), HanniganGD_2017 (14/67) and
  GuptaA_2019 (30 yes, CRC-only). This is guaiac FOBT, not FIT, and only Zeller is a usable paired cohort, so
  LOCO fusion (G1/G2 paired arm) cannot be run.
- The spec's fallback would be a pure simulation from published FIT distributions (needs sourced priors).
- Verdict: paired data condition not met. Documented and skipped per parent ruling.
