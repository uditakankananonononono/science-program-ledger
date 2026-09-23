# DOC-2-075 Function From Structure's Outliers - locked gates (22:08 IST, before EC data download)

## Sandbox-fit slice
PDB/AlphaFold local-topology comparison does not fit the sandbox. Proxy: members of one Pfam family share a fold ("structural twins"). Local feature = whether a member keeps the family's conserved motif set (the frozen top-5 4-mers from exp200/180, derived without any function labels). Outcome = "different job": the member has no EC number, or its EC 3-level prefix differs from the family's modal 3-level EC.

## Data
Same 20 Pfam families, reviewed UniProt members, re-fetched with the ec field (UniProt REST). Families where < 50% of members carry an EC are excluded (no clear "job" baseline).

## Hypothesis
Twins that lost the conserved motifs are enriched for different jobs (pseudo-enzymes / neofunctionalised members).

## Gates
G1 pooled Mantel-Haenszel odds ratio (motif-lost vs motif-kept, stratified by family) >= 3, p < 0.001.
G2 >= 70% of eligible families (with >= 5 motif-lost members) have OR > 1.
G3 >= 8 eligible families.
Failure policy: negative preserved; pivots appended with new locked gates.

## Result (22:07): PASS on locked gates. Post-hoc robustness, labeled as such: Breslow-Day heterogeneity p < 1e-10; leave-one-family-out MH OR 2.62-4.16 (dropping some families falls below 3). The pass is fragile.
