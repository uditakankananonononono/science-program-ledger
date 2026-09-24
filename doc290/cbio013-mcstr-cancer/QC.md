# QC audit: cbio013-mcstr-cancer

Audited 2026-09-24 by doc290 lane D. Checks: required sections present (Premise, Hypothesis where the spec format includes it, Data sources, Method, locked Success gates, Failure/pivot rule), numbered method steps, and data-source verification (GEO/figshare accessions and named papers resolved live; well-known public resources confirmed by name).

| spec | structure | data sources | verdict |
|------|-----------|--------------|---------|
| 01-mcstr-replication | steps=3 sources=2 | checked | PASS |
| 02-str-genotyper-benchmark | steps=3 sources=2 | checked | PASS |
| 03-cfdna-feasibility | steps=3 sources=2 | checked | PASS |
| 04-tissue-of-origin-classifier | steps=3 sources=2 | checked | PASS |
| 05-repair-expression-mechanism | steps=3 sources=1 (TCGA+ABSOLUTE+MANTIS/MSIsensor combined line) | verified | PASS |
| 06-msi-confound-audit | steps=3 sources=2 | checked | PASS |
| 07-population-str-reference | steps=3 sources=2 | checked | PASS |
| 08-survival-model-honesty | steps=3 sources=2 | checked | PASS |
| 09-liquid-biopsy-classifier | steps=3 sources=2 | checked | PASS |
| 10-str-at-scale | steps=3 sources=2 | checked | PASS |
