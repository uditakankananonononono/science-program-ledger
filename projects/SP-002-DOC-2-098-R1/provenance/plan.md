# SP-002 research plan

Candidate source topic: second list #98, "A Universal Confounder Stress Test for Bio-AI."

Goal: create a professional, reusable audit system that measures how much apparently strong biomedical AI performance survives realistic confounder, site, batch, missingness, prevalence, and temporal shifts. The contribution must be more than a benchmark: a locked evaluation protocol, multi-dataset evidence, independent validation, tested audit package, professional documentation, and sober deployment/commercial analysis.

Research questions:
1. How often do random-split biomedical classifiers overstate performance relative to group/site/time-aware splits?
2. Can a compact, model-agnostic audit predict which models will fail under external validation?
3. Which stress tests are most informative across tabular, expression, and imaging-derived feature datasets?

Before outcomes: lock datasets, endpoints, split units, baselines, stressors, primary metrics, statistical units, success/failure thresholds, and exclusions.

Current phase: literature and dataset feasibility only. Do not inspect endpoint-model outcomes before protocol lock.

Capacity rule: SP-002 is its own 12-month-equivalent research program. Parallel pipeline work cannot weaken its locked protocol, source ledger, multi-dataset validation, product testing, or professional deliverables. Outcome modeling starts only after protocol freeze.

Delivery decision (2026-09-21): The user does not want the science experiments turned into a git repository. SP-002 remains a standalone research workspace. Completed milestones will be transferred as professional files for Google Drive: protocol, literature/source ledger, data provenance manifest, executable analysis package, processed results, figures, technical report, paper, product documentation, and integrity manifest. No repo overlay packaging.

Deliverable clarification: the deliverable is the completed experiment - real computation on real open data, actual results, honest negatives, figures, reproducible analysis, and research writeup. Planning and protocol files are controls and supporting evidence, not substitutes for the experiment.
