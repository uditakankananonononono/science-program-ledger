# SP-004 Round 5 locked feasibility protocol

**Title:** PRIDE-native matched experimental opportunity for small-protein detection
**Locked:** 2026-09-21 22:11 IST before PRIDE project selection or peptide outcome retrieval

## Question
Across human, mouse and yeast proteomics studies, are canonical proteins <=100 aa underdetected relative to 101-200 aa proteins after matching experimental opportunity, while reviewed status and annotation age are modeled rather than used for inclusion?

## Feasibility gate before scientific outcomes
R5 proceeds to an outcome model only if each species has >=2 independent public PRIDE/ProteomeXchange studies that simultaneously provide: (1) processed peptide-spectrum or peptide identification files downloadable without credentials; (2) target-decoy/FDR metadata sufficient to enforce peptide FDR <=1%; (3) peptide sequences and protein accessions supporting reproducible protein inference; (4) canonical reference proteome mapping including reviewed and unreviewed proteins; (5) >=200 detectable proteins in each length arm after opportunity filtering; and (6) at least 10 shared Pfam/sequence families with >=5 detected-or-detectable proteins per arm across studies.

If file metadata cannot prove these conditions without downloading raw instrument files, R5 stops cleanly as infeasible at the processed-evidence layer. Raw vendor files will not be downloaded or reprocessed in this round.

## Prespecified processing if feasible
Unique peptides are sequences mapping to one canonical protein in the frozen species reference proteome. Shared peptides do not assign detection alone. Protein detection requires >=2 unique peptides, each <=1% PSM/peptide FDR, within a study. A one-peptide sensitivity is secondary. The theoretical opportunity set requires >=2 unique tryptic peptides of 7-35 aa, zero missed cleavages; TM/signal status, length, peptide opportunity, study/batch, Pfam/cluster, reviewed status and UniProt creation year are fixed covariates. Study-specific estimates precede random-effects synthesis; no species is pooled if fewer than two studies are estimable.

## Scientific gate
A species supports underdetection only if study-clustered adjusted detection RD <=-5 pp, 95% CI excludes zero, both independent studies agree in direction, family-matched direction agrees, and one-peptide sensitivity does not reverse. R5 succeeds only if >=2 species support underdetection. Reviewed-status mediation is descriptive unless prospective temporal ordering is available.
