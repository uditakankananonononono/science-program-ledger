# Sculpted Project Summary - Drug Failure as Information

## Status
Bounded cohort resource retained; predictive mechanism route closed before modeling because source and mapping gates failed.

## Useful results
- A cutoff-safe 123,697-study trial cohort was frozen with audited status/history-derived labels and no duplicate NCT identifiers.
- Condition and chronology gates passed, but intervention-name to molecular-mechanism mapping failed the frozen coverage floor.
- A second cutoff-safe ChEMBL/PubMed route produced 4,815 mechanism records and 6,287 molecules, yet mapped only 49.51% of names and 66.64% of trial weight, again below the locked gate.
- Safety/regulatory failure labels were not reliable enough for prediction and were explicitly abstained.

No clustering, validation or predictive model was run. This is a useful source-identifiability result, not a failed model.

## What is new
The project treats reasons for drug-development failure as a prospective information source, but tests whether historical public records can support the estimand before training. Two cutoff-safe mapping routes independently show that trial-to-mechanism linkage is the limiting layer.

## Why it matters
A model trained after silently dropping one-third to one-half of trial evidence could learn name popularity, sponsor reporting and database coverage rather than failure biology. The stop prevents an attractive but invalid drug-repurposing claim.

## Working application
The retained tool/application is a trial-cohort and evidence-coverage auditor. It can:
- reconstruct status histories at a frozen cutoff;
- label only auditable study outcomes and abstain on unreliable classes;
- quantify intervention-name and trial-weighted molecular mapping coverage;
- produce missingness/coverage reports by condition, sponsor, phase and time;
- block predictive modeling when gates fail.

This can support data curation and source investment decisions. It cannot predict drug failure or recommend compounds.

## Top-lab reviewer questions
1. Can structured intervention identifiers from a newer prospective trial-registration era remove name-mapping bias?
2. How does unmapped trial weight vary by sponsor, therapeutic area and development phase?
3. Would a registered prospective cohort built from trials with verified compound identifiers yield an estimable mechanism question?
4. Can regulatory/safety reasons be independently reconstructed from versioned sources without leakage?

## Next direction
Do not repair thresholds on the same historical cohort. A future project needs a new estimand built around prospectively identifier-complete trials or a bounded descriptive study of mapping missingness and database bias.

## Drive artifacts
- R0 feasibility: https://drive.google.com/file/d/1F2KQPxKcwpXNQetN4TapqIoQf4nRcJlQ/view?usp=drivesdk&authuser=uditakankana%40gmail.com
- R1 checkpoint: https://drive.google.com/file/d/1XH_QVLuKdD2FWaqlXC16d9pV0SI_g-Pg/view?usp=drivesdk&authuser=uditakankana%40gmail.com
- R1 mappings: https://drive.google.com/file/d/1tyCojhary1u46-GXepzL1V-N_zQrNdzO/view?usp=drivesdk&authuser=uditakankana%40gmail.com
- R1 cohort labels: https://drive.google.com/file/d/1SSijr57p1aXXeF3BSGdW2mvQePzkQhmF/view?usp=drivesdk&authuser=uditakankana%40gmail.com
- R2 evaluation: https://drive.google.com/file/d/1H8R_waq-UGnl2KFCoY4_rCV4M_duBYu9/view?usp=drivesdk&authuser=uditakankana%40gmail.com
- R2 cutoff-safe mapping: https://drive.google.com/file/d/1RYvlbslSJs0_93f1AEsShXpDd1-nPoe2/view?usp=drivesdk&authuser=uditakankana%40gmail.com
