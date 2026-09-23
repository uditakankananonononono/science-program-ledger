---
id: P18-03
title: "Oral Window: Salivary and Stool Microbial Function for Pancreatic Cancer Detection"
parent: "CBIO055 - Early Cancer Detection Using Microbial Information (source abstract, 2023)"
---

# Oral Window

**Parent project:** CBIO055 Microbial Cancer Detection (taxonomy + microbial function features from >2000 tumor and blood samples; 18% synergy gain in tissue, weaker in cfDNA).

## Premise
Pancreatic cancer is where early detection matters most and where the parent's cancer set is weakest. Kartal et al. 2022 (Gut) released paired saliva and stool shotgun metagenomes from Spanish and German PDAC cohorts and found a stool signature, while saliva added little at the taxonomic level. Nobody has asked whether microbial function in saliva carries signal that taxonomy misses - the exact question the parent asked for tissue.

## Hypothesis
Functional profiles from saliva add >= 0.05 AUROC over salivary taxonomy for PDAC vs control, and a saliva+stool combined function model beats stool taxonomy alone in an external cohort.

## Data sources (free/public)
- Kartal et al. 2022 PDAC saliva and stool metagenomes (ENA; accessions in paper; code at github.com/psecekartal/PDAC).
- Nagata et al. 2022 (Gastroenterology) Japanese PDAC stool metagenomes for external validation (public accession in paper).
- MetaPhlAn 4 and HUMAnN 3 databases (free).

## Method outline
1. Profile saliva and stool reads with MetaPhlAn 4 (taxonomy) and HUMAnN 3 (pathways, gene families) on a free compute tier, or use authors' processed tables where available.
2. Train per-site taxonomy, function and combined models on the Spanish cohort; validate on the German cohort, then the Japanese stool cohort.
3. Test whether oral taxa enriched in PDAC stool (oral-gut translocation) carry distinct functions.
4. Adjust for diabetes, PPI use and jaundice as known confounders.

## Success gates (locked before results)
- G1: saliva function adds >= 0.05 AUROC over saliva taxonomy in external validation, or the null is the result.
- G2: combined saliva+stool function model reaches external AUROC >= 0.80.
- G3: signal survives confounder adjustment (AUROC drop <= 0.05).
- G4: per-cohort 95% CIs; no pooled-only claims.

## Expected deliverable
Open pipeline, per-site feature importance, and a list of oral-origin microbial functions linked to PDAC.

## Failure/pivot rule
If saliva adds nothing (G1 fails), pivot to a translocation map: quantify which oral strains appear in PDAC stool and whether translocation rate itself is the biomarker.
