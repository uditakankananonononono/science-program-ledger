# QC audit: cbio056-helu-dti-drug-target

Audited 2026-09-24 by doc290 lane D. Checks: required sections present (Premise, Hypothesis where the spec format includes it, Data sources, Method, locked Success gates, Failure/pivot rule), numbered method steps, and data-source verification (GEO/figshare accessions and named papers resolved live; well-known public resources confirmed by name).

| spec | structure | data sources | verdict |
|------|-----------|--------------|---------|
| 01-cold-split-leakage-audit | steps=4 sources=4 | checked | PASS |
| 02-affinity-regression | steps=4 sources=3 | checked | PASS |
| 03-conformal-hit-prioritization | steps=4 sources=3 | checked | PASS |
| 04-pocket-aware-structure | steps=4 sources=3 | checked | PASS |
| 05-temporal-prospective-holdout | steps=4 sources=3 | checked | PASS |
| 06-offtarget-side-effects | steps=4 sources=3 | checked | PASS |
| 07-kinase-selectivity | steps=4 sources=3 | checked | PASS |
| 08-dark-target-ligands | steps=5 sources=3 | checked | PASS |
| 09-antibacterial-cross-kingdom | steps=4 sources=3 | checked | PASS |
| 10-kg-contribution-attribution | steps=4 sources=3 | checked | PASS |
